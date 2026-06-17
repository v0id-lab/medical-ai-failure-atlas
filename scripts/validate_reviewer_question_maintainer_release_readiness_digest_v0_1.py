#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_release_readiness_digest_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md"

REQUIRED_READINESS_IDS = {"RQMR001", "RQMR002", "RQMR003", "RQMR004", "RQMR005"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_release_readiness_digest_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
    "docs/reviewer_question_maintainer_closeout_digest_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question maintainer release readiness digest v0.1",
    "Readiness rows: 5",
    "Closeout rows represented: 5",
    "Handoff rows represented: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "Issue history rows represented: 11",
    "Previous public issue represented: 57",
    "current public preview route only",
    "ready_for_public_preview",
    "Synthetic boundary readiness",
    "Reviewer question lane readiness",
    "Public wording readiness",
    "Release surface readiness",
    "Validation readiness",
    "included_in_public_maintainer_release_readiness_digest",
    "current_preview_ready",
    "synthetic only and not for clinical use",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "make reviewer_question_maintainer_release_readiness_digest",
    "Add a reviewer question maintainer evidence map without scoring",
]
FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
    "benchmark compatible",
    "score improved",
]


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"rows": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    rows = data.get("rows", [])
    if not isinstance(rows, list):
        errors.append("rows must be a list")
        rows = []
    if data.get("readiness_row_count") != 5:
        errors.append("readiness_row_count must be 5")
    if data.get("closeout_rows_represented") != 5:
        errors.append("closeout_rows_represented must be 5")
    if data.get("handoff_rows_represented") != 5:
        errors.append("handoff_rows_represented must be 5")
    if data.get("contributor_digest_rows_represented") != 5:
        errors.append("contributor_digest_rows_represented must be 5")
    if data.get("release_index_surface_rows_represented") != 9:
        errors.append("release_index_surface_rows_represented must be 9")
    if data.get("issue_history_rows_represented") != 11:
        errors.append("issue_history_rows_represented must be 11")
    if data.get("previous_public_issue_number") != 57:
        errors.append("previous_public_issue_number must be 57")
    if data.get("readiness_decision") != "ready_for_public_preview":
        errors.append("readiness_decision must be ready_for_public_preview")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 5:
        errors.append(f"Expected 5 readiness rows, found {len(rows)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_raw_model_output_release",
        "no_endpoint_result",
        "no_score_report",
        "no_model_ranking",
        "no_benchmark_compatibility_claim",
        "no_benchmark_equivalence_claim",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    readiness_ids = {str(row.get("readiness_id")) for row in rows}
    if readiness_ids != REQUIRED_READINESS_IDS:
        errors.append("readiness id set must match required ids")
    if {str(row.get("readiness_status")) for row in rows} != {"included_in_public_maintainer_release_readiness_digest"}:
        errors.append("all readiness statuses must be included_in_public_maintainer_release_readiness_digest")
    if {str(row.get("readiness_state")) for row in rows} != {"current_preview_ready"}:
        errors.append("all readiness states must be current_preview_ready")

    for row in rows:
        readiness_id = str(row.get("readiness_id", ""))
        for key in ["readiness_name", "evidence_file", "readiness_action", "readiness_status", "readiness_state", "boundary"]:
            if key not in row:
                errors.append(f"{readiness_id}: missing {key}")

    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")

    if not MARKDOWN.exists():
        errors.append(f"Missing generated Markdown: {MARKDOWN.relative_to(ROOT)}")
        text = ""
    else:
        text = MARKDOWN.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated Markdown missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing maintainer release readiness digest must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question maintainer release readiness digest validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question maintainer release readiness digest validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"readiness_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
