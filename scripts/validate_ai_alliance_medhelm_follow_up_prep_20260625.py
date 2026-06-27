#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AI_ALLIANCE_MEDHELM_FOLLOW_UP_PREP_20260625.md"
DATA = ROOT / "docs" / "ai_alliance_medhelm_follow_up_prep_20260625.json"

REQUIRED_DOC_PHRASES = [
    "AI Alliance MedHELM Follow Up Prep",
    "No public reply",
    "Purpose: keep the next public response small",
    "Live GitHub issue check confirmed The AI Alliance trust safety evals issue 50 is open.",
    "Dean Wampler replied on 2026 06 25",
    "No maintainer request for a pull request",
    "Decision: wait for the promised follow up.",
    "Do not post another public comment now.",
    "No public thanks comment only for visibility.",
    "A claim boundary checklist for MedHELM taxonomy or leaderboard wording.",
    "Public or synthetic examples only.",
    "Benchmark score becomes safety proof.",
    "Source link becomes source support.",
    "Workflow coverage becomes clinical readiness.",
    "Do not post unless the maintainer reply makes it useful.",
    "Recheck The AI Alliance trust safety evals issue 50 on 2026 06 26",
    "make ai_alliance_medhelm_follow_up_prep",
]

REQUIRED_URLS = {
    "https://github.com/The-AI-Alliance/trust-safety-evals/issues/50#issuecomment-4799636637",
}

FORBIDDEN_PHRASES = [
    "ai alliance is reviewing",
    "adoption confirmed",
    "endorsement confirmed",
    "partnership confirmed",
    "medhelm compatible",
    "benchmark result confirmed",
    "leaderboard effect confirmed",
    "model ranking confirmed",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "official role granted",
    "pull request requested",
    "payment completed",
    "terms accepted",
]

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_model_output": False,
    "contains_benchmark_items": False,
    "claims_ai_alliance_review": False,
    "claims_ai_alliance_adoption": False,
    "claims_ai_alliance_endorsement": False,
    "claims_ai_alliance_partnership": False,
    "claims_medhelm_compatibility": False,
    "claims_benchmark_result": False,
    "claims_leaderboard_effect": False,
    "claims_model_ranking": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_medical_advice": False,
    "claims_patient_data_use": False,
    "claims_official_role": False,
    "claims_formal_contribution_request": False,
    "claims_pull_request_requested": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "allows_visibility_only_public_reply": False,
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
    urls = set(re.findall(r"https?://\S+", text))
    if urls != REQUIRED_URLS:
        errors.append("Doc URL set mismatch")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key in [
        "checked_after_reading_baglam2",
        "checked_after_reading_linkedin_tracker",
        "checked_gmail_before_build",
        "checked_live_github_issue",
    ]:
        if payload.get(key) is not True:
            errors.append(f"Expected {key} to be true")
    if payload.get("gmail_message_id") != "19efeeb5cb896ae4":
        errors.append("Gmail message id mismatch")
    if payload.get("source_comment_url") not in REQUIRED_URLS:
        errors.append("Source comment URL mismatch")
    if payload.get("issue_state") != "open":
        errors.append("Expected issue state open")
    if payload.get("maintainer_login") != "deanwampler":
        errors.append("Maintainer login mismatch")
    if payload.get("current_decision") != "wait_for_promised_follow_up":
        errors.append("Current decision mismatch")
    if payload.get("posting_allowed_now") is not False:
        errors.append("Posting should not be allowed now")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")
    if len(payload.get("allowed_next_actions", [])) != 4:
        errors.append("Expected four allowed next actions")
    if len(payload.get("blocked_next_actions", [])) != 9:
        errors.append("Expected nine blocked next actions")
    if len(payload.get("if_maintainer_asks_for_smaller_contribution", [])) != 4:
        errors.append("Expected four smaller contribution actions")

    if errors:
        print("FAIL AI Alliance MedHELM follow up prep validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS AI Alliance MedHELM follow up prep validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"allowed_next_actions={len(payload.get('allowed_next_actions', []))}")
    print(f"blocked_next_actions={len(payload.get('blocked_next_actions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
