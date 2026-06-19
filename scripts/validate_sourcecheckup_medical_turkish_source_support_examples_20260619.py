#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SOURCECHECKUP_MEDICAL_TURKISH_SOURCE_SUPPORT_EXAMPLES_20260619.md"
DATA = ROOT / "docs" / "sourcecheckup_medical_turkish_source_support_examples_20260619.json"


REQUIRED_DOC_PHRASES = [
    "SourceCheckup Medical Turkish Source Support Examples",
    "public examples for Turkish source support review",
    "No new route owner reply was found.",
    "prior Hacettepe acknowledgement remains the only reply",
    "issue #134, issue #137, and issue #138",
    "Review fields",
    "claim id",
    "Turkish claim sentence under review",
    "English gloss",
    "source surface",
    "source support state",
    "Turkish wording risk",
    "clinical scope",
    "reviewer role",
    "evidence needed",
    "allowed public wording",
    "blocked public claim",
    "stop condition",
    "SCTR001",
    "SCTR002",
    "SCTR003",
    "SCTR004",
    "SCTR005",
    "SCTR006",
    "Maintainer use rules",
    "make sourcecheckup_medical_turkish_source_support_examples",
]

FORBIDDEN_PHRASES = [
    "this is a benchmark result",
    "leaderboard rank",
    "model standing confirmed",
    "this is model ranking",
    "score certified",
    "source truth certified",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data accessed",
    "regulated data accessed",
    "this is procurement evidence",
    "partner confirmed",
    "institution approved",
    "payment completed",
    "terms accepted",
    "endorsement secured",
    "clinical clearance confirmed",
]

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_benchmark_examples": False,
    "contains_answer_keys": False,
    "contains_hidden_prompts": False,
    "claims_benchmark_result": False,
    "claims_leaderboard_ranking": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_regulated_data_access": False,
    "claims_patient_data_clearance": False,
    "claims_procurement_evidence": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_endorsement": False,
}

REQUIRED_FIELDS = {
    "claim id",
    "Turkish claim sentence under review",
    "English gloss",
    "source surface",
    "source support state",
    "Turkish wording risk",
    "clinical scope",
    "reviewer role",
    "evidence needed",
    "allowed public wording",
    "blocked public claim",
    "stop condition",
}

REQUIRED_REVIEWER_ROUTES = {
    "source review",
    "language review",
    "clinician review",
    "data steward review",
    "governance review",
    "maintainer release decision",
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
    if payload.get("prior_acknowledgement_state") != "Hacettepe health informatics acknowledgement only":
        errors.append("Expected Hacettepe acknowledgement only state")
    if payload.get("linked_issues") != [134, 137, 138]:
        errors.append("Expected links to issues 134, 137, and 138")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    fields = set(payload.get("required_fields", []))
    if fields != REQUIRED_FIELDS:
        errors.append("Required fields do not match required field set")
    reviewer_routes = set(payload.get("reviewer_routes", []))
    if reviewer_routes != REQUIRED_REVIEWER_ROUTES:
        errors.append("Reviewer routes do not match required route set")
    example_ids = set(payload.get("example_ids", []))
    if example_ids != {f"SCTR{index:03d}" for index in range(1, 7)}:
        errors.append("Expected six example ids")
    if payload.get("next_public_action") != "Turkiye A4 UM private decision checklist":
        errors.append("Unexpected next public action")

    if errors:
        print("FAIL SourceCheckup Medical Turkish source support examples validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup Medical Turkish source support examples validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"example_ids={len(example_ids)}")
    print(f"reviewer_routes={len(reviewer_routes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
