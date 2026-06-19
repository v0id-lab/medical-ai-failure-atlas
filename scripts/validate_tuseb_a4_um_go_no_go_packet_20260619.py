#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_A4_UM_GO_NO_GO_PACKET_20260619.md"
DATA = ROOT / "docs" / "tuseb_a4_um_go_no_go_packet_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB A4 UM Go No Go Packet",
    "not an application",
    "not a TÜSEB application",
    "not a TBYS submission",
    "Live source signals checked on 2026 06 19",
    "GNG001: TÜSEB A4 UM official notice",
    "16 June 2026",
    "GNG002: TÜSEB A group call document",
    "15 June to 30 June",
    "10 July",
    "13 July to 14 August",
    "16 September",
    "GNG003: TÜSEB A group project support surface",
    "Private go conditions",
    "Private no go conditions",
    "Decision outcomes",
    "Outcome A: go",
    "Outcome B: conditional wait",
    "Outcome C: no go",
    "Minimal safe concept if outcome A is true",
    "Current state is private yes or no decision, not TBYS action.",
    "make tuseb_a4_um_go_no_go_packet",
]

FORBIDDEN_PHRASES = [
    "application submitted",
    "tbys submitted",
    "partner confirmed",
    "institution approved",
    "budget approved",
    "payment completed",
    "terms accepted",
    "patient data used",
    "ethics approved",
    "clinical validation complete",
    "clinical deployment ready",
    "ranking certified",
    "endorsement secured",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tuseb_application": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_budget_approval": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_ethics_approval": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_model_ranking": False,
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
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if len(payload.get("source_signals", [])) != 3:
        errors.append("Expected 3 source signals")
    if len(payload.get("private_go_conditions", [])) != 6:
        errors.append("Expected 6 private go conditions")
    if len(payload.get("private_no_go_conditions", [])) != 6:
        errors.append("Expected 6 private no go conditions")
    if len(payload.get("decision_outcomes", [])) != 3:
        errors.append("Expected 3 decision outcomes")
    if len(payload.get("minimum_concept_scope", [])) != 6:
        errors.append("Expected 6 minimum concept scope rows")
    if payload.get("current_decision") != "private yes or no decision, not TBYS action":
        errors.append("Unexpected current decision")

    if errors:
        print("FAIL TÜSEB A4 UM go no go packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB A4 UM go no go packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"private_go_conditions={len(payload.get('private_go_conditions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
