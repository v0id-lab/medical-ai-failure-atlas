#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_DATA_STEWARD_SCOUT_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_data_steward_scout_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health Data Steward Scout",
    "public route scout for health data quality and AI readiness, not an application",
    "not an official Ministry of Health document",
    "Büyük Veri Sistemleri ve Veri Yönetimi Koordinatörlüğü",
    "Yapay Zekâ ve Yenilikçi Teknolojiler Daire Başkanlığı",
    "Kayıt ve Tescil Birimi",
    "Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü",
    "Question 1: data source ownership",
    "Question 2: data permission and public boundary",
    "Question 3: schema and coding provenance",
    "Question 4: missingness and drift",
    "Question 5: label audit",
    "Question 6: AI readiness gate",
    "Question 7: public claim hygiene",
    "Route unknown",
    "No Ministry of Health endorsement claim.",
    "No TÜSEB endorsement claim.",
    "No patient data included.",
    "No clinical validation claim.",
    "No clinical deployment claim.",
    "make turkiye_health_data_steward_scout",
]

FORBIDDEN_PHRASES = [
    "ministry approved",
    "tuseb approved",
    "official role granted",
    "route access granted",
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
    "claims_ministry_endorsement": False,
    "claims_tuseb_endorsement": False,
    "claims_official_role": False,
    "claims_route_access": False,
    "claims_partner": False,
    "claims_application": False,
    "claims_proposal": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
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
    if len(payload.get("source_signals", [])) != 4:
        errors.append("Expected 4 source signals")
    if len(payload.get("steward_questions", [])) != 7:
        errors.append("Expected 7 steward questions")
    if len(payload.get("decision_states", [])) != 5:
        errors.append("Expected 5 decision states")

    if errors:
        print("FAIL Türkiye health data steward scout validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health data steward scout validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"questions={len(payload.get('steward_questions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
