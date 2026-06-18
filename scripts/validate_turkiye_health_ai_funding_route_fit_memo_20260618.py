#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_FUNDING_ROUTE_FIT_MEMO_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_ai_funding_route_fit_memo_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Funding Route Fit Memo",
    "public route fit memo for funding and collaboration readiness, not an application",
    "not a TÜBİTAK application",
    "not a TÜSEB application",
    "not a TÜYZE proposal",
    "TÜBİTAK 1711 Yapay Zekâ Ekosistem 2026 call",
    "15 June 2026 to 18 September 2026",
    "14 September 2026 at 17:30",
    "smart education technologies",
    "TÜSEB 2026 project support details",
    "TÜSEB A group route surface",
    "TÜYZE public institute signal",
    "TÜBİTAK generative AI guide signal",
    "Route 1: TÜBİTAK 1711 smart education technology",
    "Route 2: TÜSEB A group health research support",
    "Route 3: TÜYZE education or report route",
    "Fit unknown",
    "Funding route possible",
    "No TÜBİTAK submission.",
    "No TÜSEB submission.",
    "No TÜYZE proposal.",
    "No patient data.",
    "No clinical validation claim.",
    "make turkiye_health_ai_funding_route_fit_memo",
]

FORBIDDEN_PHRASES = [
    "tubitak approved",
    "tuseb approved",
    "tuyze approved",
    "official role granted",
    "route access granted",
    "partner confirmed",
    "consortium confirmed",
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
    "claims_tubitak_submission": False,
    "claims_tuseb_submission": False,
    "claims_tuyze_proposal": False,
    "claims_official_role": False,
    "claims_partner": False,
    "claims_consortium": False,
    "claims_route_access": False,
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
    if len(payload.get("source_signals", [])) != 5:
        errors.append("Expected 5 source signals")
    if len(payload.get("route_decisions", [])) != 3:
        errors.append("Expected 3 route decisions")
    if payload.get("next_public_action") != "prepare one source checked route fit note if no route owner replies":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL Türkiye health AI funding route fit memo validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI funding route fit memo validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"routes={len(payload.get('route_decisions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
