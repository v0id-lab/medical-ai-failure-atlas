#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DEU_DIGITAL_MEDICINE_BOARD_ROUTE_OWNER_SCOUT_20260618.md"
DATA = ROOT / "docs" / "deu_digital_medicine_board_route_owner_scout_20260618.json"


REQUIRED_DOC_PHRASES = [
    "DEÜ Digital Medicine Board Route Owner Scout",
    "route owner scout, not an application",
    "digimed@deu.edu.tr",
    "safe and ethical use",
    "Artificial intelligence integration, monitoring, and performance evaluation.",
    "Responsible LLM use in research workflows.",
    "Training for clinical researchers.",
    "No application submission.",
    "No patient data.",
    "No clinical deployment claim.",
    "No clinical validation claim.",
    "make deu_digital_medicine_board_route_owner_scout",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "proposal submitted",
    "intent declaration submitted",
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
    "claims_application": False,
    "claims_proposal": False,
    "claims_intent_declaration": False,
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
    if payload.get("target_contact") != "digimed@deu.edu.tr":
        errors.append("target contact must be digimed@deu.edu.tr")
    if len(payload.get("official_sources", [])) != 4:
        errors.append("Expected four official source rows")
    if len(payload.get("route_gates", [])) != 4:
        errors.append("Expected four route gates")

    if errors:
        print("FAIL DEÜ digital medicine board route owner scout validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS DEÜ digital medicine board route owner scout validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"route_gates={len(payload.get('route_gates', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
