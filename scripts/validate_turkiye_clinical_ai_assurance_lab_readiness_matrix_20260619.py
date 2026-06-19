#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_CLINICAL_AI_ASSURANCE_LAB_READINESS_MATRIX_20260619.md"
DATA = ROOT / "docs" / "turkiye_clinical_ai_assurance_lab_readiness_matrix_20260619.json"

REQUIRED_DOC_PHRASES = [
    "Türkiye Clinical AI Assurance Lab Readiness Matrix",
    "public readiness matrix for a possible Türkiye clinical AI assurance lab route",
    "not a TÜSEB application",
    "not a TBYS submission",
    "not a TÜBİTAK application",
    "not a PRODİS submission",
    "not a TÜYZE partnership",
    "not a hospital partnership",
    "not an official role",
    "not a clinical validation claim",
    "not clinical deployment",
    "not patient data use",
    "TÜSEB A4 UM notice",
    "TÜSEB A group call document",
    "TÜBİTAK 1711 2026 call notice",
    "Ministry of Health Information Systems General Directorate public surface",
    "TÜSEB public institute listing",
    "Lane 1. Route owner and eligibility",
    "Lane 2. Non patient data assurance scope",
    "Lane 3. Turkish medical LLM evaluation",
    "Lane 4. Clinician AI literacy",
    "Lane 5. Health data quality and label audit",
    "Lane 6. Governance and no ranking report",
    "Lane 7. Sandbox readiness boundary",
    "Lane 8. Opportunity package",
    "TÜSEB A4 UM is time sensitive",
    "TÜBİTAK 1711 is live",
    "not ready for application language",
    "make turkiye_clinical_ai_assurance_lab_readiness_matrix",
]

REQUIRED_SOURCE_URLS = {
    "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
    "https://files.tuseb.gov.tr/tuseb/files/dokumanlar/tuseb-2026projecagrilari-agrubu.pdf",
    "https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi",
    "https://sbsgm.saglik.gov.tr",
    "https://www.tuseb.gov.tr/",
}

REQUIRED_FALSE_FLAGS = [
    "contains_patient_data",
    "contains_private_operational_data",
    "claims_tuseb_application",
    "claims_tbys_submission",
    "claims_tubitak_application",
    "claims_prodis_submission",
    "claims_tuyze_partner",
    "claims_hospital_partner",
    "claims_official_role",
    "claims_institutional_approval",
    "claims_budget",
    "claims_payment",
    "claims_terms_acceptance",
    "claims_model_ranking",
    "claims_score_certification",
    "claims_procurement_evidence",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_medical_advice",
    "claims_endorsement",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tuyze approved",
    "tubitak approved",
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
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    if payload.get("checked_gmail_before_build") is not True:
        errors.append("Expected Gmail checked flag")
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    for key in REQUIRED_FALSE_FLAGS:
        if payload.get(key) is not False:
            errors.append(f"JSON flag {key} expected False")

    urls = {item.get("source_url") for item in payload.get("source_anchors", [])}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")
    if len(payload.get("readiness_lanes", [])) != 8:
        errors.append("Expected eight readiness lanes")
    if len(payload.get("stop_conditions", [])) != 8:
        errors.append("Expected eight stop conditions")
    if payload.get("next_outward_action") != "if no route owner reply appears build one page hospital AI literacy collaboration packet":
        errors.append("Unexpected next outward action")

    if errors:
        print("FAIL Türkiye clinical AI assurance lab readiness matrix validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye clinical AI assurance lab readiness matrix validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_anchors={len(urls)}")
    print(f"readiness_lanes={len(payload.get('readiness_lanes', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
