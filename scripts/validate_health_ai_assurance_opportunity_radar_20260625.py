#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HEALTH_AI_ASSURANCE_OPPORTUNITY_RADAR_20260625.md"
DATA = ROOT / "docs" / "health_ai_assurance_opportunity_radar_20260625.json"

REQUIRED_DOC_PHRASES = [
    "Health AI assurance opportunity radar",
    "TEKNOFEST Health AI report claim hygiene checklist",
    "TÜBİTAK 1711 AI ecosystem",
    "TÜSEB project surface",
    "HealthBench supports the atlas focus on clinician rubrics",
    "MedHELM makes workflow coverage and multi metric reporting central",
    "BRIDGE confirms that multilingual clinical text evaluation is active",
    "CHAI gives a governance vocabulary",
    "public evaluation tools must say they are not devices",
    "transparency rules come into effect in August 2026",
    "No application",
    "No benchmark compatibility claim",
    "No device or regulatory compliance claim",
    "validate_health_ai_assurance_opportunity_radar_20260625.py",
]

REQUIRED_SOURCE_URLS = {
    "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
    "https://tubitak.gov.tr/tr/duyuru",
    "https://proje-destek.tuseb.gov.tr/tr/haberler",
    "https://openai.com/index/healthbench/",
    "https://medhelm.org/",
    "https://github.com/YLab-Open/BRIDGE",
    "https://www.chai.org/",
    "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices",
    "https://health.ec.europa.eu/ehealth-digital-health-and-care/artificial-intelligence-healthcare_en",
}

REQUIRED_SUPPORTING_URLS = {
    "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
    "https://digital-strategy.ec.europa.eu/en/policies/ecosystem-ai-innovation-europe",
}

FORBIDDEN_PHRASES = [
    "application submitted",
    "partner confirmed",
    "official role granted",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "benchmark compatible",
    "score certified",
    "fda authorized",
    "eu compliant",
    "chai certified",
    "medhelm partner",
    "healthbench partner",
    "bridge partner",
    "teknofest finalist",
    "terms accepted",
    "payment completed",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tubitak_application": False,
    "claims_tuseb_application": False,
    "claims_teknofest_submission": False,
    "claims_chai_affiliation": False,
    "claims_medhelm_collaboration": False,
    "claims_healthbench_collaboration": False,
    "claims_bridge_collaboration": False,
    "claims_fda_authorization": False,
    "claims_eu_compliance": False,
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
    for key in [
        "checked_after_reading_baglam2",
        "checked_after_reading_trackers",
        "checked_gmail_before_build",
        "checked_github_before_build",
    ]:
        if payload.get(key) is not True:
            errors.append(f"Expected {key} to be true")

    if payload.get("recommended_next_build") != "TEKNOFEST Health AI report claim hygiene checklist":
        errors.append("Recommended next build mismatch")

    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    signals = payload.get("source_signals", [])
    urls = {signal.get("source_url") for signal in signals}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set mismatch")
    supporting_urls = set()
    for signal in signals:
        supporting_urls.update(signal.get("supporting_urls", []))
        if not signal.get("verified_claim"):
            errors.append(f"Signal {signal.get('id')} missing verified claim")
        if not signal.get("build_meaning"):
            errors.append(f"Signal {signal.get('id')} missing build meaning")
    if supporting_urls != REQUIRED_SUPPORTING_URLS:
        errors.append("Supporting URL set mismatch")

    if len(signals) != 9:
        errors.append("Expected nine source signals")
    if len(payload.get("priority_decisions", [])) != 5:
        errors.append("Expected five priority decisions")
    if len(payload.get("next_repo_artifacts", [])) != 3:
        errors.append("Expected three next repo artifacts")

    if errors:
        print("FAIL health AI assurance opportunity radar validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS health AI assurance opportunity radar validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(signals)}")
    print(f"priority_decisions={len(payload.get('priority_decisions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
