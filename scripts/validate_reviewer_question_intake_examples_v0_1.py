#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md"
DATA = ROOT / "docs" / "reviewer_question_intake_examples_v0_1.json"

REQUIRED_PHRASES = [
    "Reviewer question intake examples v0.1",
    "SourceCheckup",
    "Failure Atlas",
    "sourcecheckup_review",
    "synthetic_failure_case",
    "benchmark_reviewer_question_id",
    "reviewer question fields",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "Add a maintainer triage board for these intake examples without scoring",
]

REQUIRED_IDS = ["RQINT001", "RQINT002", "RQINT003", "RQINT004"]
REQUIRED_BSRQ = ["BSRQ001", "BSRQ002", "BSRQ005", "BSRQ006"]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
]


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing markdown: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")
    if not DATA.exists():
        errors.append(f"Missing json: {DATA.relative_to(ROOT)}")
        payload = {}
    else:
        payload = json.loads(DATA.read_text(encoding="utf-8"))

    lower = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"Markdown missing phrase: {phrase}")
    for phrase in REQUIRED_IDS + REQUIRED_BSRQ:
        if phrase not in text:
            errors.append(f"Markdown missing id: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Markdown contains hyphen character")

    examples = payload.get("examples", [])
    if len(examples) != 4:
        errors.append(f"Expected 4 examples, found {len(examples)}")
    if payload.get("contains_patient_data") is not False:
        errors.append("JSON must set contains_patient_data false")
    if payload.get("no_endpoint_calls") is not True:
        errors.append("JSON must set no_endpoint_calls true")
    if payload.get("no_scoring") is not True or payload.get("no_ranking") is not True:
        errors.append("JSON must set no scoring and no ranking true")
    if payload.get("no_compatibility_claim") is not True:
        errors.append("JSON must set no_compatibility_claim true")

    templates = {row.get("template") for row in examples}
    if templates != {"sourcecheckup_review", "synthetic_failure_case"}:
        errors.append(f"Unexpected template set: {sorted(templates)}")

    ids = {row.get("intake_id") for row in examples}
    for row_id in REQUIRED_IDS:
        if row_id not in ids:
            errors.append(f"JSON missing intake id: {row_id}")
    bsrq = {row.get("benchmark_reviewer_question_id") for row in examples}
    for question_id in REQUIRED_BSRQ:
        if question_id not in bsrq:
            errors.append(f"JSON missing BSRQ id: {question_id}")

    for row in examples:
        for key in [
            "benchmark_lens",
            "reviewer_question",
            "blocked_claim_type",
            "required_checks",
            "track_a_value",
            "track_b_value",
        ]:
            if not row.get(key):
                errors.append(f"{row.get('intake_id')} missing {key}")
        unsafe = " ".join(str(row.get(key, "")) for key in ["reviewer_question", "blocked_claim_type", "proposed_public_action"])
        if "score" in unsafe.lower() or "ranking" in unsafe.lower():
            errors.append(f"{row.get('intake_id')} contains score or ranking wording")

    if errors:
        print("FAIL reviewer question intake examples validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question intake examples validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"examples={len(examples)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
