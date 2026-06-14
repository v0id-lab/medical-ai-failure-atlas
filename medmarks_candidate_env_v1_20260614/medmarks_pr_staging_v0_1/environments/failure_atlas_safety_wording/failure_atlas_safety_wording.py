#!/usr/bin/env python3
"""Verifiers style Medmarks proof pack for Failure Atlas safety wording cases."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path
from typing import Any

try:
    from .judge_prompts import build_judge_prompt
except ImportError:  # pragma: no cover - supports direct script smoke execution
    from judge_prompts import build_judge_prompt


def _optional_verifiers_imports() -> dict[str, Any]:
    try:
        from datasets import Dataset
        from medarc_verifiers.judging import MultiJudge, MultiJudgeRubric
        from verifiers.envs.singleturn_env import SingleTurnEnv
    except Exception as exc:  # pragma: no cover - dependency gate for local smoke mode
        raise RuntimeError(
            "Medmarks dependencies are not installed. Install in a Medmarks checkout with uv sync "
            "before calling load_environment(). Smoke mode does not require these packages."
        ) from exc
    return {
        "Dataset": Dataset,
        "MultiJudge": MultiJudge,
        "MultiJudgeRubric": MultiJudgeRubric,
        "SingleTurnEnv": SingleTurnEnv,
    }


def load_cases(path: Path, max_cases: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        if max_cases is not None and len(rows) >= max_cases:
            break
        row = json.loads(line)
        if row.get("data_provenance") != "synthetic":
            raise ValueError(f"line {line_number}: data_provenance must be synthetic")
        if row.get("contains_patient_data") is not False:
            raise ValueError(f"line {line_number}: contains_patient_data must be false")
        if row.get("not_for_clinical_use") is not True:
            raise ValueError(f"line {line_number}: not_for_clinical_use must be true")
        rubric = row.get("rubric")
        if not isinstance(rubric, list) or not rubric:
            raise ValueError(f"line {line_number}: rubric must be a non empty list")
        for item in rubric:
            if not item.get("criterion_id") or not item.get("positive_behavior"):
                raise ValueError(f"line {line_number}: rubric item missing criterion_id or positive_behavior")
        rows.append(row)
    if not rows:
        raise ValueError("no cases loaded")
    return rows


def case_to_dataset_row(case: dict[str, Any]) -> dict[str, Any]:
    criteria = [item["positive_behavior"] for item in case["rubric"]]
    criterion_ids = [item["criterion_id"] for item in case["rubric"]]
    points_list = [int(item.get("points", 2)) for item in case["rubric"]]
    return {
        "prompt": [{"role": "user", "content": case["prompt"]}],
        "info": {
            "case_id": case["case_id"],
            "source_scenario_id": case["source_scenario_id"],
            "clinical_domain": case["clinical_domain"],
            "task_family": case["task_family"],
            "expected_safety_focus": case["expected_safety_focus"],
            "failure_mechanism_tags": case["failure_mechanism_tags"],
            "clinician_review_question": case["clinician_review_question"],
            "criteria": criteria,
            "criterion_ids": criterion_ids,
            "points_list": points_list,
            "data_provenance": "synthetic",
            "contains_patient_data": False,
            "not_for_clinical_use": True,
            "review_status": case.get(
                "review_status",
                "single physician authored synthetic draft pending additional clinician review",
            ),
        },
    }


def build_dataset_rows(cases_path: Path, max_cases: int | None = None) -> list[dict[str, Any]]:
    return [case_to_dataset_row(case) for case in load_cases(cases_path, max_cases=max_cases)]


def _completion_text(completion: Any) -> str:
    if isinstance(completion, list) and completion:
        last = completion[-1]
        if isinstance(last, dict):
            return str(last.get("content", ""))
    return str(completion)


def _format_conversation(prompt: Any, completion: Any) -> str:
    prompt_text = ""
    if isinstance(prompt, list) and prompt:
        first = prompt[-1]
        if isinstance(first, dict):
            prompt_text = str(first.get("content", ""))
    return f"user: {prompt_text}\nassistant: {_completion_text(completion)}"


def _extract_first_json_object(text: str) -> str | None:
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for index, char in enumerate(text[start:], start=start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def _parse_score(raw: Any) -> tuple[int, str | None, str | None]:
    text = str(raw)
    payload_text = _extract_first_json_object(text)
    if payload_text is None:
        return 0, None, "judge response did not contain JSON"
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        return 0, None, "judge response JSON parse failed"
    try:
        score = int(float(payload.get("score", 0)))
    except Exception as exc:
        score = 0
        error = f"judge score parse failed: {exc}"
    else:
        error = None
    score = max(0, min(2, score))
    explanation = payload.get("explanation")
    return score, str(explanation) if explanation is not None else None, error


def load_environment(
    cases_path: str = "data/failure_atlas_external_sample_v0_1.jsonl",
    judge_model: str | list[str] = "openai/gpt-5-mini",
    judge_base_url: str | list[str] | None = None,
    judge_api_key: str | list[str] | None = None,
    judge_timeout: int | None = 300,
    max_parallel_judges: int = 3,
    make_dataset: bool = False,
    max_cases: int | None = None,
    **kwargs: Any,
) -> Any:
    imports = _optional_verifiers_imports()
    Dataset = imports["Dataset"]
    MultiJudge = imports["MultiJudge"]
    MultiJudgeRubric = imports["MultiJudgeRubric"]
    SingleTurnEnv = imports["SingleTurnEnv"]

    rows = build_dataset_rows(Path(cases_path), max_cases=max_cases)
    dataset = Dataset.from_list(rows)

    multi_judge = MultiJudge.from_env_args(
        judge_model=judge_model,
        judge_base_url=judge_base_url,
        judge_api_key=judge_api_key,
        judge_prompt="{question}",
        judge_timeout=judge_timeout,
    )
    rubric = MultiJudgeRubric(multi_judge)

    async def reward_failure_atlas(prompt: Any, completion: Any, info: dict[str, Any], state: dict[str, Any]) -> float:
        criteria = info.get("criteria", [])
        points_list = info.get("points_list", [])
        if not criteria or not points_list:
            return 0.0
        total_possible = float(sum(points_list))
        conversation = _format_conversation(prompt, completion)
        semaphore = asyncio.Semaphore(max_parallel_judges)
        judgments = []

        async def judge_one(index: int, criterion: str) -> dict[str, Any]:
            async with semaphore:
                full_prompt = build_judge_prompt(conversation=conversation, criterion=criterion)
                results = await rubric.judge([{"role": "user", "content": full_prompt}], "", "", state)
                judge_scores = []
                judge_payloads = []
                for result in results:
                    score, explanation, parse_error = _parse_score(getattr(result, "raw", ""))
                    judge_scores.append(score)
                    judge_payloads.append(
                        {
                            "model": getattr(result, "model", None),
                            "raw": getattr(result, "raw", None),
                            "error": getattr(result, "error", None) or parse_error,
                            "score": score,
                            "explanation": explanation,
                        }
                    )
                aggregate_score = sum(judge_scores) / len(judge_scores) if judge_scores else 0.0
                return {
                    "idx": index,
                    "criterion": criterion,
                    "score": aggregate_score,
                    "judges": judge_payloads,
                }

        tasks = [judge_one(index, criterion) for index, criterion in enumerate(criteria)]
        judgments = await asyncio.gather(*tasks)
        current_score = sum(float(item["score"]) for item in judgments)
        normalized = max(0.0, min(1.0, current_score / total_possible))

        if make_dataset:
            state.setdefault("failure_atlas_judge_feedback", []).append(
                {
                    "case_id": info.get("case_id"),
                    "score": normalized,
                    "judgments": sorted(judgments, key=lambda item: item["idx"]),
                }
            )
        return normalized

    rubric.add_reward_func(reward_failure_atlas, weight=1.0)
    return SingleTurnEnv(eval_dataset=dataset, system_prompt="", rubric=rubric)


def smoke(cases_path: Path) -> dict[str, Any]:
    rows = build_dataset_rows(cases_path)
    first = rows[0]
    return {
        "status": "smoke_pass",
        "cases": len(rows),
        "first_case_id": first["info"]["case_id"],
        "first_prompt_messages": first["prompt"],
        "first_criteria": first["info"]["criterion_ids"],
        "points_per_case": [sum(row["info"]["points_list"]) for row in rows],
        "review_status": first["info"]["review_status"],
        "contains_patient_data": any(row["info"]["contains_patient_data"] for row in rows),
        "not_for_clinical_use": all(row["info"]["not_for_clinical_use"] for row in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        print(json.dumps(smoke(args.cases), indent=2))
        return

    for row in build_dataset_rows(args.cases):
        print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
