#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TUSEB_A4_UM_PRIVATE_EVIDENCE_CLOSURE_NOTE_20260619.md"
DATA = ROOT / "docs" / "tuseb_a4_um_private_evidence_closure_note_20260619.json"


REQUIRED_DOC_PHRASES = [
    "TÜSEB A4 UM Private Evidence Closure Note",
    "not an application",
    "not TBYS action",
    "Live source signals checked on 2026 06 19",
    "PEC001: TÜSEB A4 UM official notice",
    "16 June 2026",
    "PEC002: TÜSEB A group call document",
    "15 June to 30 June",
    "10 July",
    "13 July to 14 August",
    "16 September",
    "PEC003: TÜSEB A group project support surface",
    "Closure states",
    "Private evidence closure rows",
    "PEC101: eligibility evidence",
    "PEC102: compulsory service evidence",
    "PEC103: institution authority evidence",
    "PEC104: TBYS role evidence",
    "PEC105: route fit evidence",
    "PEC106: non patient data evidence",
    "PEC107: clinical boundary evidence",
    "PEC108: budget evidence",
    "PEC109: terms evidence",
    "PEC110: final closure decision",
    "Current state is private evidence closure pending, not TBYS action.",
    "make tuseb_a4_um_private_evidence_closure_note",
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
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_private_answers": False,
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

REQUIRED_SOURCE_URLS = {
    "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
    "https://files.tuseb.gov.tr/tuseb/files/dokumanlar/tuseb-2026projecagrilari-agrubu.pdf",
    "https://proje-destek.tuseb.gov.tr/a-grubu-proje-destekleri",
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
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    if payload.get("gmail_checked_at_trt") != "2026 06 19 17:07":
        errors.append("Unexpected Gmail checked time")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    source_urls = {signal.get("source_url") for signal in payload.get("source_signals", [])}
    if source_urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")
    if len(payload.get("closure_rows", [])) != 10:
        errors.append("Expected 10 closure rows")
    if len(payload.get("required_private_closure_rows", [])) != 9:
        errors.append("Expected 9 required private closure rows")
    if len(payload.get("closure_states", [])) != 5:
        errors.append("Expected 5 closure states")
    if payload.get("current_decision") != "private evidence closure pending, not TBYS action":
        errors.append("Unexpected current decision")
    if payload.get("next_public_action") != "monitor Gmail before any new package":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL TÜSEB A4 UM private evidence closure note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS TÜSEB A4 UM private evidence closure note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"source_signals={len(payload.get('source_signals', []))}")
    print(f"closure_rows={len(payload.get('closure_rows', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
