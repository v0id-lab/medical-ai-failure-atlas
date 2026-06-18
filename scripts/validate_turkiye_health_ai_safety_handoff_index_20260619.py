#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_HANDOFF_INDEX_20260619.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_handoff_index_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Safety Handoff Index",
    "public handoff index for hospitals, medical faculties, health informatics units, ethics groups, education teams, and route owners",
    "not a partnership claim",
    "not a TÜSEB application",
    "National route owner scope",
    "TÜSEB A4 UM TÜYZE Non Patient Data Concept Note",
    "Hospital and medical faculty first read",
    "Clinician AI literacy and review",
    "Health data quality and label audit",
    "No ranking safety reporting",
    "Public tool and contribution entry point",
    "Reply ready summary",
    "TÜSEB route fit question is sent and waiting for reply.",
    "Hacettepe health informatics has acknowledged receipt and said they will review.",
    "Silence is not treated as rejection.",
    "Acknowledgement is not treated as endorsement.",
    "No patient data.",
    "No clinical validation claim.",
    "No model ranking.",
    "make turkiye_health_ai_safety_handoff_index",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tuyze approved",
    "official role granted",
    "partner confirmed",
    "application submitted",
    "proposal submitted",
    "patient data used",
    "clinical deployment ready",
    "clinical validation complete",
    "score certification complete",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tuseb_application": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_institutional_approval": False,
    "claims_budget": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_medical_advice": False,
    "claims_endorsement": False,
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
    groups = payload.get("route_groups", [])
    if len(groups) != 6:
        errors.append("Expected 6 route groups")
    for group in groups:
        if len(group.get("artifacts", [])) != 4:
            errors.append(f"Route group {group.get('name')} expected 4 artifacts")
    state = payload.get("current_external_state", {})
    if state.get("tuseb_route_fit_question_waiting") is not True:
        errors.append("Expected TÜSEB route fit waiting state")
    if state.get("silence_is_rejection") is not False:
        errors.append("Silence must not be marked as rejection")
    if state.get("acknowledgement_is_endorsement") is not False:
        errors.append("Acknowledgement must not be marked as endorsement")

    if errors:
        print("FAIL Türkiye health AI safety handoff index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI safety handoff index validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"route_groups={len(groups)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
