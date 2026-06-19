#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUT = ROOT / "sourcecheckup" / "demo" / "sourcecheckup_medical_source_claim_walkthrough_v0_1.json"
BUILD_MD = ROOT / "sourcecheckup" / "build" / "sourcecheckup_medical_source_claim_walkthrough_v0_1.md"
DOC_MD = ROOT / "docs" / "sourcecheckup" / "SOURCECHECKUP_MEDICAL_SOURCE_CLAIM_WALKTHROUGH_V0_1.md"

REQUIRED_CASES = {
    "sc_v02_locator_inventory_003",
    "sc_v02_url_missing_inventory_004",
    "sc_v02_policy_sandbox_008",
    "sc_v02_clean_uncertainty_010",
}

REQUIRED_PHRASES = [
    "SourceCheckup Medical source claim walkthrough v0.1",
    "Status: public static demo.",
    "Synthetic examples only.",
    "not clinical advice",
    "not patient data",
    "not clinical validation",
    "not clinical deployment",
    "not a source truth judgment",
    "not model ranking",
    "not institutional approval",
    "not endorsement",
    "Claim detected.",
    "Source surface identified.",
    "Evidence not yet enough.",
    "Rewrite or hold.",
    "It does not clear the 16 verification queue items as evidence.",
    "Detector friction is a product signal",
    "Do not call any row verified evidence.",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "safe for clinical use",
    "approved for clinical use",
    "source truth certified",
    "best model",
    "endorsed by",
    "institutional approval received",
    "patient data used",
]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    payload = load_json(JSON_OUT)
    cases = payload.get("cases")
    if not isinstance(cases, list):
        errors.append("cases must be a list")
        cases = []
    case_ids = {str(case.get("answer_id")) for case in cases if isinstance(case, dict)}
    if case_ids != REQUIRED_CASES:
        errors.append(f"case ids mismatch: {sorted(case_ids)}")
    if payload.get("case_count") != 4:
        errors.append("case_count must be 4")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case row must be an object")
            continue
        if case.get("patient_data") is not False:
            errors.append(f"{case.get('answer_id')}: patient_data must be false")
        if case.get("external_action_ready") is not False:
            errors.append(f"{case.get('answer_id')}: external_action_ready must be false")
        if case.get("clinical_claim_cleared") is not False:
            errors.append(f"{case.get('answer_id')}: clinical_claim_cleared must be false")
        if not case.get("current_gate"):
            errors.append(f"{case.get('answer_id')}: current_gate missing")
        if not case.get("reviewer_question"):
            errors.append(f"{case.get('answer_id')}: reviewer_question missing")

    for path in (BUILD_MD, DOC_MD):
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        lower_text = text.lower()
        for phrase in REQUIRED_PHRASES:
            if phrase.lower() not in lower_text:
                errors.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in lower_text:
                errors.append(f"{path.relative_to(ROOT)} forbidden phrase: {phrase}")
        if "-" in text:
            errors.append(f"{path.relative_to(ROOT)} contains hyphen characters")

    if errors:
        print("FAIL SourceCheckup Medical source claim walkthrough validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical source claim walkthrough validation")
    print(f"json={JSON_OUT.relative_to(ROOT)}")
    print(f"build={BUILD_MD.relative_to(ROOT)}")
    print(f"doc={DOC_MD.relative_to(ROOT)}")
    print(f"cases={len(cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
