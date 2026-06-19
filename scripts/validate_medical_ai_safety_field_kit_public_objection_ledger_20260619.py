#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_LEDGER_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_objection_ledger_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_ledger_issue149_comment_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_ledger_public_action_audit_20260619.md"


REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, AUDIT]
REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Public Objection Ledger",
    "public objection ledger for issue 149",
    "Issue state checked at build: open",
    "Issue comment count at build: 1",
    "No external reviewer objection has been recorded yet",
    "No fake reviewer row is allowed",
    "No release is required for this ledger",
    "make medical_ai_safety_field_kit_public_objection_ledger",
]
REQUIRED_COMMENT_PHRASES = [
    "Maintainer note for issue 149",
    "public objection ledger",
    "Use it to leave one concrete objection in one lane",
    "Failure mode",
    "Turkish wording risk",
    "Source support gap",
    "Field readiness gate",
    "Benchmark misuse risk",
    "Reviewer route suggestion",
]
FORBIDDEN_PHRASES = [
    "patient data used",
    "real patient case",
    "clinically validated",
    "clinical deployment ready",
    "diagnosis advice provided",
    "treatment advice provided",
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
    "compliance certified",
]
FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]
REQUIRED_FALSE_FLAGS = [
    "fake_reviewer_rows_allowed",
    "contains_patient_data",
    "claims_clinical_validation",
    "claims_clinical_deployment",
    "claims_diagnosis_or_treatment_advice",
    "claims_benchmark_ranking",
    "claims_score_certification",
    "claims_source_truth_certification",
    "claims_partner",
    "claims_institutional_approval",
    "claims_endorsement",
    "claims_formal_application",
    "claims_payment",
    "claims_terms_acceptance",
    "release_published",
    "email_sent",
    "social_posted",
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
        "Audit": AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else "",
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

    if payload.get("source_issue_number") != 149:
        errors.append("source issue must be 149")
    if payload.get("issue_state_checked") != "OPEN":
        errors.append("issue state must be OPEN")
    if payload.get("issue_comment_count_at_build") != 1:
        errors.append("issue comment count at build must be one")
    if payload.get("public_comments_from_external_reviewers") != 0:
        errors.append("external reviewer comment count must be zero")
    if "No new substantive route owner reply" not in payload.get("gmail_reply_state", ""):
        errors.append("Gmail reply state must state no new substantive route owner reply")

    rows = payload.get("ledger_rows", [])
    if len(rows) != 6:
        errors.append("Expected six ledger rows")
    expected_lanes = {
        "failure mode",
        "Turkish wording risk",
        "source support gap",
        "field readiness gate",
        "benchmark misuse risk",
        "reviewer route suggestion",
    }
    found_lanes = {row.get("lane") for row in rows}
    if found_lanes != expected_lanes:
        errors.append("Ledger lanes mismatch")
    for row in rows:
        for field in ["lane", "current_public_objections", "accepted_comment_shape", "blocked_content"]:
            if field not in row:
                errors.append(f"Ledger row missing field: {field}")
        if row.get("current_public_objections") != 0:
            errors.append(f"Ledger row {row.get('lane')} must start with zero public objections")
        if not row.get("blocked_content"):
            errors.append(f"Ledger row {row.get('lane')} lacks blocked content")

    if errors:
        print("FAIL Medical AI Safety Field Kit public objection ledger validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical AI Safety Field Kit public objection ledger validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    print(f"audit={AUDIT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
