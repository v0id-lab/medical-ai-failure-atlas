#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUBITAK_1711_CONSORTIUM_READINESS_NO_PARTNER_GATE_20260619.md"
DATA = ROOT / "docs" / "tubitak_1711_consortium_readiness_no_partner_gate_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜBİTAK 1711 Consortium Readiness No Partner Gate",
    "public readiness gate, not an application",
    "15 June 2026",
    "18 September 2026",
    "14 September 2026 at 17:30",
    "smart education technologies",
    "does not list health as a direct priority area",
    "applications without a consortium are not evaluated",
    "Demand owner",
    "Education technology provider",
    "Research route",
    "YZE pre application interface",
    "Private authority",
    "No application submission.",
    "No PRODİS action.",
    "No partner claim.",
    "No health priority fit claim.",
    "repository name",
    "make tubitak_1711_consortium_readiness_no_partner_gate",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "PRODİS submitted",
    "intent declaration submitted",
    "YZE meeting requested",
    "partner confirmed",
    "institution confirmed",
    "health priority fit confirmed",
    "budget approved",
    "terms accepted",
    "payment completed",
    "patient data used",
    "clinically validated",
    "clinical deployment ready",
    "ranking certified",
    "score certified",
    "endorsed by",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "claims_application": False,
    "claims_prodis_action": False,
    "claims_intent_declaration": False,
    "claims_yze_meeting_request": False,
    "claims_partner": False,
    "claims_institution": False,
    "claims_health_priority_fit": False,
    "claims_budget": False,
    "claims_terms_acceptance": False,
    "claims_payment": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_ranking": False,
    "claims_score_certification": False,
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
        if phrase.lower() in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    official_facts = payload.get("official_facts", [])
    readiness_gates = payload.get("readiness_gates", [])
    if payload.get("official_fact_count") != 6 or len(official_facts) != 6:
        errors.append("Expected 6 official facts")
    if payload.get("readiness_gate_count") != 5 or len(readiness_gates) != 5:
        errors.append("Expected 5 readiness gates")
    if payload.get("boundary_count") != 16:
        errors.append("Expected 16 boundaries")
    gmail_check = payload.get("gmail_check", {})
    if len(gmail_check.get("threads", [])) != 9:
        errors.append("Expected 9 Gmail threads")
    if "No new route owner reply" not in gmail_check.get("result", ""):
        errors.append("Gmail result must state no new route owner reply")

    if errors:
        print("FAIL TÜBİTAK 1711 consortium readiness no partner gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜBİTAK 1711 consortium readiness no partner gate validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"facts={len(official_facts)}")
    print(f"gates={len(readiness_gates)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
