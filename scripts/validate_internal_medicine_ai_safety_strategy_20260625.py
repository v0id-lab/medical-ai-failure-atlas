#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "internal_medicine_ai_safety_strategy_20260625.json"
BUILDER = ROOT / "scripts" / "build_internal_medicine_ai_safety_strategy_20260625.py"
FIELD_DOC = ROOT / "docs" / "MEDICAL_AI_FIELD_COMMAND_PLAN_20260625.md"
EVAL_DOC = ROOT / "docs" / "TURKISH_INTERNAL_MEDICINE_SAFETY_EVAL_V0_1_20260625.md"
EVAL_JSONL = ROOT / "data" / "turkish_internal_medicine_safety_eval_v0_1_20260625.jsonl"

REQUIRED_ROW_FIELDS = {
    "eval_id",
    "source_case_id",
    "language",
    "clinical_domain",
    "internal_medicine_lane",
    "setting",
    "prompt_seed",
    "failure_pattern",
    "risk_axis",
    "safety_gate",
    "severity_1_to_5",
    "scoring_focus",
    "source_support_requirement",
    "required_model_behavior",
    "why_this_row_matters",
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
    "review_status",
}

REQUIRED_PHRASES = [
    "Medical AI Field Command Plan",
    "Turkish Internal Medicine Safety Eval v0.1",
    "FDA AI enabled medical devices list",
    "OpenAI HealthBench",
    "Google MedGemma developer page",
    "MedHELM",
    "AgentClinic",
    "Sağlık Bakanlığı Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı",
    "TÜYZE RADİS technical launch",
    "NeyimVar award page",
    "Build the Turkish internal medicine safety evaluation lane",
    "missing information, urgent escalation, medication safety, laboratory interpretation, source support, and safe Turkish wording",
    "make internal_medicine_ai_safety_strategy",
]

FORBIDDEN_PHRASES = [
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used: true",
    "model superiority proven",
    "score certified",
    "source truth certified",
    "regulatory clearance secured",
    "institutional approval granted",
    "partner confirmed",
    "endorsement confirmed",
    "accepted contribution",
    "merged contribution",
    "terms accepted",
    "payment completed",
]


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"Line {line_number} is not valid JSON: {error}") from error
    return rows


def main() -> int:
    errors: list[str] = []
    if not CONFIG.exists():
        errors.append(f"Missing config: {CONFIG.relative_to(ROOT)}")
        config = {}
    else:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    try:
        rows = load_jsonl(EVAL_JSONL)
    except Exception as error:  # noqa: BLE001
        rows = []
        errors.append(str(error))

    if len(config.get("source_registry", [])) < 16:
        errors.append("Source registry must contain at least sixteen checked sources")
    if len(config.get("strategic_read", [])) != 3:
        errors.append("Strategic read must contain three rows")
    if len(config.get("operating_model", [])) != 2:
        errors.append("Operating model must contain two agent lanes")
    if len(config.get("six_hour_sprint", [])) != 3:
        errors.append("Six hour sprint must contain three work items")
    if len(config.get("thirty_day_targets", [])) != 5:
        errors.append("Thirty day targets must contain five targets")
    if len(rows) < 24:
        errors.append("Generated eval set must contain at least twenty four rows")

    seen_ids: set[str] = set()
    for row in rows:
        missing = REQUIRED_ROW_FIELDS - set(row)
        if missing:
            errors.append(f"{row.get('eval_id', 'unknown')}: missing fields {sorted(missing)}")
        if row.get("eval_id") in seen_ids:
            errors.append(f"Duplicate eval id: {row.get('eval_id')}")
        seen_ids.add(str(row.get("eval_id")))
        if row.get("synthetic_only") is not True:
            errors.append(f"{row.get('eval_id')}: synthetic_only must be true")
        if row.get("patient_data_used") is not False:
            errors.append(f"{row.get('eval_id')}: patient_data_used must be false")
        if row.get("clinical_use_allowed") is not False:
            errors.append(f"{row.get('eval_id')}: clinical_use_allowed must be false")
        if not str(row.get("source_support_requirement", "")).strip():
            errors.append(f"{row.get('eval_id')}: source support requirement is empty")

    combined = ""
    for path in [FIELD_DOC, EVAL_DOC]:
        if not path.exists():
            errors.append(f"Missing generated markdown: {path.relative_to(ROOT)}")
            continue
        combined += "\n" + path.read_text(encoding="utf-8")

    lower_combined = combined.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_combined:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_combined:
            errors.append(f"Forbidden phrase in generated docs: {phrase}")

    if errors:
        print("FAIL internal medicine AI safety strategy validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS internal medicine AI safety strategy validation")
    print(f"config={CONFIG.relative_to(ROOT)}")
    print(f"field_doc={FIELD_DOC.relative_to(ROOT)}")
    print(f"eval_doc={EVAL_DOC.relative_to(ROOT)}")
    print(f"eval_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
