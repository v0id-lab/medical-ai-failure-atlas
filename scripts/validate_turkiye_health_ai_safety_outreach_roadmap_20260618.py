#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_OUTREACH_ROADMAP_20260618.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_outreach_roadmap_20260618.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Safety Outreach Roadmap",
    "public roadmap and outreach packet",
    "TÜYZE adjacent readiness route",
    "Turkish medical faculty clinician AI literacy route",
    "Turkish hospital AI readiness route",
    "TÜSEB proposal readiness route",
    "TÜBİTAK public AI ecosystem monitoring route",
    "TEKNOFEST health AI team safety route",
    "Open source medical AI contributor route",
    "No claim made",
    "no official TÜYZE status",
    "no hospital partner",
    "no application",
    "no submission",
    "no patient data",
    "no clinical validation",
    "make turkiye_health_ai_safety_outreach_roadmap",
]

FORBIDDEN_PHRASES = [
    "official tuyze partner",
    "official tuseb partner",
    "application submitted",
    "submission made",
    "contact made",
    "patient data used for",
    "medical advice provided",
    "clinical deployment ready",
    "clinically validated for",
    "benchmark winner",
    "model certified",
]

REQUIRED_FLAGS = {
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_partner_relationship": False,
    "claims_application": False,
    "claims_submission": False,
    "claims_contact_made": False,
    "contains_patient_data": False,
    "claims_medical_advice": False,
    "claims_clinical_deployment": False,
    "claims_clinical_validation": False,
    "claims_benchmark_ranking": False,
    "claims_model_certification": False,
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
    surfaces = payload.get("outreach_surfaces", [])
    sources = payload.get("sources", [])
    if payload.get("outreach_surface_count") != 7 or len(surfaces) != 7:
        errors.append("Expected 7 outreach surfaces")
    if payload.get("source_count") != 6:
        errors.append("Expected source_count 6")
    if len(sources) < 5:
        errors.append("Expected at least 5 source URLs")

    if errors:
        print("FAIL Türkiye health AI safety outreach roadmap validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI safety outreach roadmap validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"sources={len(sources)}")
    print(f"outreach_surfaces={len(surfaces)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
