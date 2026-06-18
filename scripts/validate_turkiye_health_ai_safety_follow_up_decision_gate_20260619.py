#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TURKIYE_HEALTH_AI_SAFETY_FOLLOW_UP_DECISION_GATE_20260619.md"
DATA = ROOT / "docs" / "turkiye_health_ai_safety_follow_up_decision_gate_20260619.json"


REQUIRED_DOC_PHRASES = [
    "Türkiye Health AI Safety Follow Up Decision Gate",
    "public follow up decision gate",
    "field action control surface",
    "when to wait",
    "when to send the public handoff index",
    "when to open a new non duplicative route",
    "TÜSEB route fit thread `19edcafe5c2dfa60`: sent message only, no reply.",
    "Hacettepe health informatics thread `19eda863ce89f083`: acknowledgement received earlier, no new substantive reply.",
    "State 1. Wait without new outreach",
    "State 2. Send the handoff index only after a direct trigger",
    "State 3. Open a new route only after a new factual trigger",
    "State 4. Escalate to prepared application package only after eligibility proof",
    "Today's state is State 1. Wait without new outreach.",
    "no new direct trigger exists for sending the handoff index",
    "No repeated outreach without a new trigger.",
    "make turkiye_health_ai_safety_follow_up_decision_gate",
]

FORBIDDEN_PHRASES = [
    "tuseb approved",
    "tuyze approved",
    "official role granted",
    "partner confirmed",
    "application submitted",
    "proposal submitted",
    "patient data used",
    "clinical deployment ready",
    "clinical validation complete",
    "score certification complete",
    "terms accepted",
    "payment completed",
    "silence means rejection",
    "send repeated outreach",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_tuseb_application": False,
    "claims_tbys_submission": False,
    "claims_tuyze_proposal": False,
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
    "allows_repeated_outreach_without_new_trigger": False,
}

REQUIRED_THREAD_IDS = {
    "19edcafe5c2dfa60",
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
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
    if payload.get("current_state") != "wait_without_new_outreach":
        errors.append("Expected current_state wait_without_new_outreach")
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    threads = payload.get("gmail_threads_checked", [])
    thread_ids = {thread.get("thread_id") for thread in threads}
    if thread_ids != REQUIRED_THREAD_IDS:
        errors.append("Gmail thread id set does not match required active thread set")
    states = payload.get("decision_states", [])
    if len(states) != 4:
        errors.append("Expected four decision states")
    state_names = {state.get("name") for state in states}
    expected_states = {
        "wait_without_new_outreach",
        "send_handoff_index_after_direct_trigger",
        "open_new_route_after_new_factual_trigger",
        "prepare_application_package_after_eligibility_proof",
    }
    if state_names != expected_states:
        errors.append("Decision state names do not match expected state set")
    for state in states:
        if not state.get("trigger"):
            errors.append(f"Decision state {state.get('name')} missing trigger")
        if not state.get("allowed_actions"):
            errors.append(f"Decision state {state.get('name')} missing allowed actions")
        if not state.get("blocked_actions"):
            errors.append(f"Decision state {state.get('name')} missing blocked actions")

    entry_points = payload.get("public_entry_points", [])
    for entry in entry_points:
        if not (ROOT / entry).exists():
            errors.append(f"Public entry point missing from tree: {entry}")

    if errors:
        print("FAIL Türkiye health AI safety follow up decision gate validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Türkiye health AI safety follow up decision gate validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"threads={len(threads)}")
    print(f"decision_states={len(states)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
