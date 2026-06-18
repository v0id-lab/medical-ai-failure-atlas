#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TEKNOFEST_PUBLIC_SHARE_CLEARANCE_PACKET_20260618.md"
DATA = ROOT / "docs" / "teknofest_public_share_clearance_packet_20260618.json"


REQUIRED_DOC_PHRASES = [
    "TEKNOFEST Public Share Clearance Packet",
    "public share clearance packet",
    "29 June 2026 at 17:00",
    "genetic variant",
    "Short public post",
    "Long public post",
    "Repository only note",
    "Do not post anything from this packet without explicit clearance",
    "No public post is made",
    "No official TEKNOFEST endorsement is claimed",
    "No patient data is used",
    "No clinical deployment is claimed",
    "No clinical validation is claimed",
    "make teknofest_public_share_clearance_packet",
]

FORBIDDEN_PHRASES = [
    "public post made",
    "email sent",
    "submission made",
    "application submitted",
    "official teknofest role confirmed",
    "teknofest endorsed",
    "team relationship confirmed",
    "patient data used for",
    "clinical deployment ready",
    "clinically validated",
    "payment completed",
    "terms accepted",
]

REQUIRED_FLAGS = {
    "requires_goktug_clearance_before_public_post": True,
    "contains_patient_data": False,
    "claims_submission": False,
    "claims_application": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_team_relationship": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
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
    source_facts = payload.get("source_facts", [])
    share_options = payload.get("share_options", [])
    if payload.get("source_fact_count") != 4 or len(source_facts) != 4:
        errors.append("Expected 4 source facts")
    if payload.get("share_option_count") != 3 or len(share_options) != 3:
        errors.append("Expected 3 share options")

    if errors:
        print("FAIL TEKNOFEST public share clearance packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TEKNOFEST public share clearance packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_facts={len(source_facts)}")
    print(f"share_options={len(share_options)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
