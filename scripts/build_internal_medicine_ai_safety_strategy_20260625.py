#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "internal_medicine_ai_safety_strategy_20260625.json"
FIELD_DOC = ROOT / "docs" / "MEDICAL_AI_FIELD_COMMAND_PLAN_20260625.md"
EVAL_DOC = ROOT / "docs" / "TURKISH_INTERNAL_MEDICINE_SAFETY_EVAL_V0_1_20260625.md"


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def dump_jsonl(path: Path, rows: list[dict]) -> str:
    return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n"


def numbered(values: list[str]) -> list[str]:
    return [f"{index}. {value}" for index, value in enumerate(values, 1)]


def domain_lane(domain: str, lane_map: dict[str, str]) -> str:
    normalized = domain.lower()
    for term, lane in lane_map.items():
        if term in normalized:
            return lane
    return "internal medicine safety review"


def source_family(row: dict) -> str:
    gate = str(row.get("safety_gate") or "")
    risk = str(row.get("risk_axis") or "")
    if "dosing" in gate or "medication" in risk:
        return "medication safety source support"
    if "escalation" in gate or "danger" in risk:
        return "urgent escalation source support"
    if "discharge" in gate or "reassurance" in risk:
        return "false reassurance source support"
    if "over_treatment" in risk:
        return "stewardship and over treatment source support"
    return "clinical reasoning source support"


def build_eval_rows(config: dict) -> list[dict]:
    selection = config["eval_selection"]
    source_path = ROOT / selection["source_jsonl"]
    source_rows = load_jsonl(source_path)
    terms = [term.lower() for term in selection["included_domain_terms"]]
    rows: list[dict] = []
    for source in source_rows:
        domain = str(source.get("clinical_domain", "")).lower()
        if not any(term in domain for term in terms):
            continue
        eval_id = f"TIMEV{len(rows) + 1:03d}"
        row = {
            "eval_id": eval_id,
            "source_case_id": source["case_id"],
            "language": source["language"],
            "clinical_domain": source["clinical_domain"],
            "internal_medicine_lane": domain_lane(source["clinical_domain"], selection["lane_map"]),
            "setting": source["setting"],
            "prompt_seed": source["turkish_prompt_seed"],
            "failure_pattern": source["failure_pattern"],
            "risk_axis": source["risk_axis"],
            "safety_gate": source.get("safety_gate"),
            "severity_1_to_5": source["severity_1_to_5"],
            "scoring_focus": "escalation, missing variable discipline, medication safety, source support, and safe Turkish wording",
            "source_support_requirement": source_family(source),
            "required_model_behavior": source["safe_answer_expectation"],
            "why_this_row_matters": source["clinical_rationale_annotation"],
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "review_status": source["review_status"],
        }
        rows.append(row)
        if len(rows) >= int(selection["max_rows"]):
            break
    return rows


def render_field_doc(config: dict) -> str:
    lines = [
        "# Medical AI Field Command Plan",
        "",
        f"Date: {config['date']}",
        "",
        f"Status: {config['status']}.",
        "",
        "## Decision",
        "",
        config["decision"],
        "",
        "## Position",
        "",
        config["position"],
        "",
        "## Current Field Read",
        "",
    ]
    for item in config["strategic_read"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"Claim: {item['claim']}",
                "",
                f"Evidence ids: {', '.join(item['evidence_ids'])}",
                "",
                f"Action: {item['action']}",
                "",
            ]
        )
    lines.extend(["## Two Agent Operating Model", ""])
    for item in config["operating_model"]:
        lines.extend(
            [
                f"### {item['agent']}: {item['lane']}",
                "",
                f"Job: {item['job']}",
                "",
                f"Output: {item['output']}",
                "",
            ]
        )
    lines.extend(["## Six Hour Sprint", ""])
    for item in config["six_hour_sprint"]:
        lines.extend([f"### {item['id']}", "", f"Work: {item['work']}", "", f"Proof: {item['proof']}", ""])
    lines.extend(["## Thirty Day Targets", ""])
    for item in config["thirty_day_targets"]:
        lines.extend([f"### {item['id']}", "", f"Target: {item['target']}", "", f"Measure: {item['measure']}", ""])
    lines.extend(["## Source Registry", ""])
    for item in config["source_registry"]:
        lines.extend(
            [
                f"### {item['id']}: {item['name']}",
                "",
                f"URL: {item['url']}",
                "",
                f"Verified use: {item['verified_use']}",
                "",
                f"Strategy signal: {item['strategy_signal']}",
                "",
            ]
        )
    lines.extend(["## Blocked Claims", "", *numbered(config["blocked_claims"]), ""])
    return "\n".join(lines)


def render_eval_doc(config: dict, rows: list[dict]) -> str:
    lines = [
        "# Turkish Internal Medicine Safety Eval v0.1",
        "",
        f"Date: {config['date']}",
        "",
        "Status: generated synthetic internal medicine safety lane.",
        "",
        "## Purpose",
        "",
        "Give model builders, open source eval maintainers, and Turkish health AI teams a small clinician reviewed path for missing information, urgent escalation, medication safety, laboratory interpretation, source support, and safe Turkish wording.",
        "",
        "## Data Source",
        "",
        f"Source JSONL: `{config['eval_selection']['source_jsonl']}`",
        "",
        f"Generated JSONL: `{config['eval_selection']['output_jsonl']}`",
        "",
        "All rows are synthetic. The generated file carries `patient_data_used: false` and `clinical_use_allowed: false` in every row.",
        "",
        "## Rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['eval_id']} from {row['source_case_id']}",
                "",
                f"Lane: {row['internal_medicine_lane']}",
                "",
                f"Clinical domain: {row['clinical_domain']}",
                "",
                f"Prompt seed: {row['prompt_seed']}",
                "",
                f"Failure pattern: {row['failure_pattern']}",
                "",
                f"Severity: {row['severity_1_to_5']}",
                "",
                f"Safety gate: {row['safety_gate']}",
                "",
                f"Source support requirement: {row['source_support_requirement']}",
                "",
                f"Required model behavior: {row['required_model_behavior']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Runnable Check",
            "",
            "`make internal_medicine_ai_safety_strategy`",
            "",
            "## Boundary",
            "",
            "This eval path is not clinical advice, clinical validation, clinical deployment, model ranking, score certification, source truth certification, regulatory clearance, institutional approval, partner status, endorsement, acceptance, merge, payment, or terms action.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    rows = build_eval_rows(config)
    output_jsonl = ROOT / config["eval_selection"]["output_jsonl"]
    rendered = {
        FIELD_DOC: render_field_doc(config),
        EVAL_DOC: render_eval_doc(config, rows),
        output_jsonl: dump_jsonl(output_jsonl, rows),
    }

    if args.check:
        errors: list[str] = []
        for path, expected in rendered.items():
            if not path.exists():
                errors.append(f"Missing generated file: {path.relative_to(ROOT)}")
                continue
            if path.read_text(encoding="utf-8") != expected:
                errors.append(f"Generated file is stale: {path.relative_to(ROOT)}")
        if errors:
            for error in errors:
                print(f"FAIL {error}")
            return 1
        print("PASS internal medicine AI safety strategy generated files are current")
        for path in rendered:
            print(f"file={path.relative_to(ROOT)}")
        print(f"rows={len(rows)}")
        return 0

    for path, text in rendered.items():
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
