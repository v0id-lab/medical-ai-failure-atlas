#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_CLINICIAN_AI_SAFETY_MINI_CURRICULUM_20260618.md"
DATA = ROOT / "docs" / "turkiye_clinician_ai_safety_mini_curriculum_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Clinician AI Safety Mini Curriculum",
    "public 30 minute clinician AI safety mini curriculum, not an official course",
    "not a clinical validation, and not a deployment package",
    "TÜBİTAK source:",
    "Akıllı Eğitim Teknolojileri",
    "18 September 2026 at 25:59 UTC+3",
    "pre registration due by 14 September 2026 at 17:30",
    "TÜSEB source:",
    "applications are received through TBYS according to the call calendar",
    "TÜYZE source:",
    "08 April and 20 May 2026",
    "Minute 0 to 3: boundary opening",
    "Minute 14 to 20: no ranking safety review",
    "Before this can be used outside a classroom or review exercise",
    "No application has been submitted.",
    "No patient data was used.",
    "No clinical validation exists.",
    "make turkiye_clinician_ai_safety_mini_curriculum",
]

FORBIDDEN_PHRASES = [
    "official course confirmed",
    "application submitted",
    "proposal submitted",
    "congress submitted",
    "partner confirmed",
    "official role confirmed",
    "endorsement confirmed",
    "clinical deployment ready",
    "clinically validated",
    "patient data used",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "claims_official_course": False,
    "claims_application": False,
    "claims_proposal": False,
    "claims_congress_submission": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_terms_acceptance": False,
    "claims_payment": False,
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
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    segments = payload.get("segments", [])
    if len(segments) != 6:
        errors.append("Expected six curriculum segments")
    if payload.get("duration_minutes") != 30:
        errors.append("duration must be 30 minutes")
    sources = payload.get("official_sources", [])
    if len(sources) != 3:
        errors.append("Expected three official source entries")

    if errors:
        print("FAIL Türkiye clinician AI safety mini curriculum validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye clinician AI safety mini curriculum validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"segments={len(segments)}")
    print(f"sources={len(sources)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
