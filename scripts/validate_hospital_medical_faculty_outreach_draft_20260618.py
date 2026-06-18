#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HOSPITAL_MEDICAL_FACULTY_OUTREACH_DRAFT_20260618.md"
DATA = ROOT / "docs" / "hospital_medical_faculty_outreach_draft_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Hospital and Medical Faculty Outreach Draft",
    "target adaptable outreach draft",
    "Not sent",
    "Target verification before send",
    "Turkish short message",
    "English short message",
    "No message sent",
    "No contact made",
    "No official role claimed",
    "No endorsement claimed",
    "No partnership claimed",
    "No patient data used",
    "No clinical deployment claimed",
    "No clinical validation claimed",
    "make hospital_medical_faculty_outreach_draft",
]

FORBIDDEN_PHRASES = [
    "message sent",
    "contact made",
    "official partner",
    "endorsed by",
    "partnership confirmed",
    "application submitted",
    "submission made",
    "patient data used for",
    "clinical deployment ready",
    "clinically validated for",
]

REQUIRED_FLAGS = {
    "claims_message_sent": False,
    "claims_contact_made": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_partner_relationship": False,
    "claims_application": False,
    "claims_submission": False,
    "contains_patient_data": False,
    "claims_medical_advice": False,
    "claims_clinical_deployment": False,
    "claims_clinical_validation": False,
}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text and f"no {phrase}" not in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if payload.get("source_count") != 6:
        errors.append("Expected source_count 6")
    if payload.get("message_count") != 2:
        errors.append("Expected message_count 2")
    if len(payload.get("target_types", [])) < 6:
        errors.append("Expected at least 6 target types")

    if errors:
        print("FAIL hospital medical faculty outreach draft validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS hospital medical faculty outreach draft validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"sources={len(payload.get('sources', []))}")
    print(f"target_types={len(payload.get('target_types', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
