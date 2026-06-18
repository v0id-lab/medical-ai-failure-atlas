#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "GLOBAL_HEALTH_AI_OPPORTUNITY_RADAR_20260619.md"
DATA = ROOT / "docs" / "global_health_ai_opportunity_radar_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Global Health AI Opportunity Radar",
    "public opportunity radar for Türkiye and global medical AI safety field action",
    "TÜBİTAK announced that the 1711 Yapay Zeka Ekosistem 2026 call opened on 16 June 2026.",
    "TÜSEB announced the 2026 A4 UM specialist compulsory service project call on 16 June 2026.",
    "TEKNOFEST Sağlıkta Yapay Zeka lists the project detail report deadline as 29 June 2026 at 17:00.",
    "Yapay Zeka ve Yenilikçi Teknolojiler Dairesi",
    "AI literacy obligations entered into application on 2 February 2025",
    "CHAI lists May 2026 governance playbooks",
    "MedHELM describes an open community led benchmark with 121 clinical tasks",
    "OpenAI HealthBench describes a health benchmark with 5000 realistic health conversations",
    "BRIDGE describes a multilingual benchmark with 87 clinical text tasks",
    "EU AI Act health AI sandbox readiness crosswalk",
    "MedHELM HealthBench BRIDGE compatibility note",
    "Send nothing new to TÜSEB while the active route fit thread is unanswered.",
    "make global_health_ai_opportunity_radar",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tubitak approved",
    "teknofest submitted",
    "chai member",
    "medhelm partner",
    "healthbench partner",
    "bridge partner",
    "official role granted",
    "partner confirmed",
    "application submitted",
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
    "claims_tubitak_application": False,
    "claims_teknofest_submission": False,
    "claims_chai_affiliation": False,
    "claims_medhelm_collaboration": False,
    "claims_healthbench_collaboration": False,
    "claims_bridge_collaboration": False,
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

REQUIRED_SOURCE_URLS = {
    "https://tubitak.gov.tr/tr",
    "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
    "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
    "https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html",
    "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
    "https://www.chai.org/",
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://github.com/YLab-Open/BRIDGE",
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
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    if payload.get("checked_gmail_before_build") is not True:
        errors.append("Expected Gmail checked flag")
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required live radar source set")
    if len(signals) != 9:
        errors.append("Expected nine source signals")
    for signal in signals:
        if not signal.get("action_meaning"):
            errors.append(f"Source signal {signal.get('name')} missing action meaning")
    priorities = payload.get("priority_decisions", [])
    if len(priorities) != 5:
        errors.append("Expected five priority decisions")

    if errors:
        print("FAIL global health AI opportunity radar validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS global health AI opportunity radar validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"priority_decisions={len(priorities)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
