#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_SEND_APPROVAL_PACKET_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_send_approval_packet_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_issue149_comment_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_public_post_seed_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_public_action_audit_20260619.md"
SOURCE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_manual_source_support_20260619.md"


REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, RELEASE_NOTES, PUBLIC_POST_SEED, AUDIT, SOURCE_SUPPORT]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Send Approval Packet",
    "No message has been sent from this packet",
    "Current reply state",
    "Decision rule",
    "Draft one: TUSEB and TUYZE route owner",
    "Draft two: Hacettepe health informatics warm follow up",
    "Public post seed",
    "Send state: not sent",
    "Goktug must approve exact text",
    "No mail was sent",
    "make medical_ai_safety_field_kit_send_approval_packet",
]

REQUIRED_COMMENT_PHRASES = [
    "Maintainer note for issue 149",
    "send approval packet",
    "Nothing in the packet has been sent or posted",
    "Which draft is too broad",
    "Which safety boundary is missing",
    "Please keep examples synthetic and free of patient data",
]

FORBIDDEN_PHRASES = [
    "official partner",
    "approved by",
    "authorized representative",
    "on behalf of",
    "clinical validation completed",
    "ready for deployment",
    "safe for patient care",
    "integrate into your hospital",
    "access patient data",
    "real patient cases",
    "diagnostic tool",
    "treatment recommendation",
    "regulatory compliant",
    "guaranteed compliant",
    "paid collaboration",
    "consulting terms",
    "procurement route",
    "application for",
    "formal appointment",
    "exclusive partnership",
    "AI " + "detector safe",
    "patient data used",
    "clinically validated",
    "clinical deployment ready",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "official guidance",
]

FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_THREADS = {
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

REQUIRED_FALSE_FLAGS = [
    "emails_sent",
    "social_posted",
    "contains_patient_data",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_diagnosis_or_treatment_advice",
    "claims_benchmark_ranking",
    "claims_score_certification",
    "claims_source_truth_certification",
    "claims_partner",
    "claims_institutional_approval",
    "claims_official_role",
    "claims_endorsement",
    "claims_formal_application",
    "claims_payment",
    "claims_terms_acceptance",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def add_text_checks(errors: list[str], label: str, text: str) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains internal process label: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing artifact: {path.relative_to(ROOT)}")

    texts = {
        "Doc": DOC.read_text(encoding="utf-8") if DOC.exists() else "",
        "Issue comment": ISSUE_COMMENT.read_text(encoding="utf-8") if ISSUE_COMMENT.exists() else "",
        "Release notes": RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else "",
        "Public post seed": PUBLIC_POST_SEED.read_text(encoding="utf-8") if PUBLIC_POST_SEED.exists() else "",
        "Audit": AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else "",
        "Manual source support": SOURCE_SUPPORT.read_text(encoding="utf-8") if SOURCE_SUPPORT.exists() else "",
    }

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in texts["Doc"].lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_COMMENT_PHRASES:
        if phrase.lower() not in texts["Issue comment"].lower():
            errors.append(f"Issue comment missing required phrase: {phrase}")

    for label, text in texts.items():
        add_text_checks(errors, label, text)

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}

    for key in ["checked_after_reading_baglam2", "checked_after_reading_trackers", "checked_gmail_before_build"]:
        if payload.get(key) is not True:
            errors.append(f"JSON flag {key} expected True")
    for key in REQUIRED_FALSE_FLAGS:
        if payload.get(key) is not False:
            errors.append(f"JSON flag {key} expected False")
    if payload.get("requires_goktug_clearance_before_send") is not True:
        errors.append("Goktug clearance must be required")
    if payload.get("issue_comment_prepared_not_posted") is not True:
        errors.append("Issue comment must be prepared but not posted")
    if payload.get("release_notes_prepared_not_published") is not True:
        errors.append("Release notes must be prepared but not published")

    if payload.get("source_issue_number") != 149:
        errors.append("source issue must be 149")
    if set(payload.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    if payload.get("targeted_search_count") != 6:
        errors.append("Expected six targeted Gmail searches")
    if "No new substantive route owner reply" not in payload.get("gmail_reply_state", ""):
        errors.append("Gmail reply state must state no new substantive route owner reply")

    drafts = payload.get("message_drafts", [])
    if len(drafts) != 2:
        errors.append("Expected two message drafts")
    for draft in drafts:
        for field in ["draft_id", "target", "recipient_state", "send_state", "requires_goktug_clearance", "subject", "body", "blocked_claims"]:
            if field not in draft:
                errors.append(f"Draft missing field: {field}")
        if draft.get("send_state") != "not sent":
            errors.append(f"Draft {draft.get('draft_id')} must not be sent")
        if draft.get("requires_goktug_clearance") is not True:
            errors.append(f"Draft {draft.get('draft_id')} must require Goktug clearance")
        if not draft.get("blocked_claims"):
            errors.append(f"Draft {draft.get('draft_id')} lacks blocked claims")
        add_text_checks(errors, f"Draft {draft.get('draft_id')}", draft.get("subject", ""))
        add_text_checks(errors, f"Draft {draft.get('draft_id')}", draft.get("body", ""))

    for phrase in [
        "TUSEB announced the 2026 A4 UM Uzman call",
        "TUSEB A group project support page routes active call details through TBYS",
        "SBSGM has a Yapay Zeka ve Yenilikci Teknolojiler Daire Baskanligi page",
        "TEKNOFEST Health AI competition pages show",
        "Hacettepe Bilisim Enstitusu pages show",
        "Issue 149 is the public intake surface",
        "Support limit",
    ]:
        if phrase.lower() not in texts["Manual source support"].lower():
            errors.append(f"Manual source support missing phrase: {phrase}")

    if errors:
        print("FAIL Medical AI Safety Field Kit send approval packet validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical AI Safety Field Kit send approval packet validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    print(f"release_notes={RELEASE_NOTES.relative_to(ROOT)}")
    print(f"public_post_seed={PUBLIC_POST_SEED.relative_to(ROOT)}")
    print(f"audit={AUDIT.relative_to(ROOT)}")
    print(f"manual_source_support={SOURCE_SUPPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
