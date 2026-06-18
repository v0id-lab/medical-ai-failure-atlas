#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_AI_ETHICS_STATUS_GATE_NOTE_V0_1.md"
DATA = ROOT / "docs" / "turkiye_ai_ethics_status_gate_note_v0_1.json"


REQUIRED_SOURCE_IDS = ["TAESG001", "TAESG002", "TAESG003"]
REQUIRED_GATE_IDS = [
    "TAESGATE001",
    "TAESGATE002",
    "TAESGATE003",
    "TAESGATE004",
    "TAESGATE005",
    "TAESGATE006",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_submission_claim": True,
    "no_application_claim": True,
    "no_ethics_approval_claim": True,
    "no_national_rule_claim": True,
    "no_official_role_claim": True,
    "no_endorsement_claim": True,
    "no_patient_data_claim": True,
    "no_clinical_validation_claim": True,
    "no_clinical_deployment_claim": True,
    "no_terms_acceptance": True,
    "no_payment": True,
}

REQUIRED_PHRASES = [
    "Türkiye AI ethics status gate note v0.1",
    "local ethics status signal",
    "not generalized into a Türkiye wide rule",
    "education, interoperability, collaboration, and AI process language only",
    "local ethics page scope",
    "study type scope",
    "patient data scope",
    "clinical validation scope",
    "institutional role scope",
    "public build route",
    "No ethics approval claim.",
    "No national rule claim.",
    "No submission claim.",
    "No application claim.",
    "No official role claim.",
    "No endorsement claim.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "make turkiye_ai_ethics_status_gate_note",
]

FORBIDDEN_PHRASES = [
    "ethics approval granted",
    "ethics submission completed",
    "national rule confirmed",
    "ministry endorsed",
    "official role secured",
    "clinical study approved",
    "patient data ready",
    "clinically validated",
    "deployed clinically",
    "route access granted",
    "terms accepted",
    "payment made",
]


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing Markdown: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")
    if not DATA.exists():
        errors.append(f"Missing JSON: {DATA.relative_to(ROOT)}")
        payload: dict = {}
    else:
        payload = json.loads(DATA.read_text(encoding="utf-8"))

    if payload.get("source_row_count") != 3:
        errors.append("source row count must be 3")
    if payload.get("gate_row_count") != 6:
        errors.append("gate row count must be 6")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"{key} must be {expected}")

    source_ids = [row.get("source_id") for row in payload.get("source_rows", [])]
    if source_ids != REQUIRED_SOURCE_IDS:
        errors.append("source ids must be TAESG001 through TAESG003")
    gate_ids = [row.get("gate_id") for row in payload.get("gate_rows", [])]
    if gate_ids != REQUIRED_GATE_IDS:
        errors.append("gate ids must be TAESGATE001 through TAESGATE006")

    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Markdown must not contain hyphen characters")

    if errors:
        print("FAIL Türkiye AI ethics status gate note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye AI ethics status gate note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_rows={payload['source_row_count']}")
    print(f"gate_rows={payload['gate_row_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
