#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_ROUTE_FIT_QUESTION_PACKET_20260619.md"
DATA = ROOT / "docs" / "tuseb_route_fit_question_packet_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB Route Fit Question Packet",
    "public route fit question packet for a non patient data medical AI safety concept, not an application",
    "not a TÜSEB application",
    "not a TBYS submission",
    "not a TÜYZE proposal",
    "TÜSEB A4 UM expert call notice",
    "16 June 2026",
    "compulsory state service",
    "TÜSEB A group project support page",
    "doctorate or medical specialty degrees",
    "TÜYZE health data and AI route surface",
    "Büyük Veri Birimi",
    "Tıbbi Karar Destek Sistemleri Birimi",
    "Yapay Zeka Bilim Kurulu",
    "TÜBİTAK open calls contrast",
    "15 June 2026 to 18 September 2026",
    "Subject: Non patient data medical AI safety concept route question",
    "Sorum tek cümleliktir",
    "A4 UM, TÜYZE, yoksa başka bir TÜSEB yüzeyi midir?",
    "No TÜSEB application.",
    "No TBYS submission.",
    "No patient data.",
    "No clinical validation claim.",
    "make tuseb_route_fit_question_packet",
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
    if len(payload.get("source_signals", [])) != 4:
        errors.append("Expected 4 source signals")
    if payload.get("target_email_to") != "info@tuseb.gov.tr":
        errors.append("Unexpected target e mail")
    if payload.get("target_email_subject") != "Non patient data medical AI safety concept route question":
        errors.append("Unexpected target e mail subject")

    if errors:
        print("FAIL TÜSEB route fit question packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB route fit question packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"target_email_to={payload.get('target_email_to')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
