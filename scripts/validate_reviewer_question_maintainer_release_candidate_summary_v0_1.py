#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_release_candidate_summary_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md"

REQUIRED_SUMMARY_IDS = {"RQMC001", "RQMC002", "RQMC003", "RQMC004", "RQMC005"}
REQUIRED_SOURCE_TRAIL_IDS = {"RQMT001", "RQMT002", "RQMT003", "RQMT004", "RQMT005"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md",
    "docs/reviewer_question_maintainer_release_candidate_summary_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md",
    "docs/reviewer_question_maintainer_audit_trail_packet_v0_1.json",
    "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question maintainer release candidate summary v0.1",
    "Candidate summary rows: 5",
    "Audit trail rows represented: 5",
    "Evidence rows represented: 5",
    "Readiness rows represented: 5",
    "Closeout rows represented: 5",
    "Handoff rows represented: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "Issue history rows represented: 11",
    "Previous public issue represented: 60",
    "current public preview route only",
    "public_preview_candidate_only",
    "Synthetic boundary candidate",
    "Reviewer question lane candidate",
    "Public wording candidate",
    "Release surface candidate",
    "Validation candidate",
    "public_preview_release_candidate_summary",
    "current_preview_candidate",
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
    "make reviewer_question_maintainer_release_candidate_summary",
    "Add a reviewer question maintainer public preview decision log without scoring",
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
    if data.get("candidate_summary_row_count") != 5:
        errors.append("candidate_summary_row_count must be 5")
    if data.get("audit_trail_rows_represented") != 5:
        errors.append("audit_trail_rows_represented must be 5")
    if data.get("evidence_rows_represented") != 5:
        errors.append("evidence_rows_represented must be 5")
    if data.get("readiness_rows_represented") != 5:
        errors.append("readiness_rows_represented must be 5")
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
    if data.get("previous_public_issue_number") != 60:
        errors.append("previous_public_issue_number must be 60")
    if data.get("release_candidate_decision") != "public_preview_candidate_only":
        errors.append("release_candidate_decision must be public_preview_candidate_only")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 5:
        errors.append(f"Expected 5 candidate summary rows, found {len(rows)}")

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

    summary_ids = {str(row.get("summary_id")) for row in rows}
    if summary_ids != REQUIRED_SUMMARY_IDS:
        errors.append("summary id set must match required ids")
    source_trail_ids = {str(row.get("source_trail_id")) for row in rows}
    if source_trail_ids != REQUIRED_SOURCE_TRAIL_IDS:
        errors.append("source trail id set must match required ids")
    if {str(row.get("candidate_status")) for row in rows} != {"public_preview_release_candidate_summary"}:
        errors.append("all candidate statuses must be public_preview_release_candidate_summary")
    if {str(row.get("candidate_state")) for row in rows} != {"current_preview_candidate"}:
        errors.append("all candidate states must be current_preview_candidate")

    for row in rows:
        summary_id = str(row.get("summary_id", ""))
        for key in ["summary_name", "source_trail_id", "candidate_surface", "maintainer_decision", "candidate_status", "candidate_state", "boundary"]:
            if key not in row:
                errors.append(f"{summary_id}: missing {key}")

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
        errors.append("Generated outward facing maintainer release candidate summary must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question maintainer release candidate summary validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question maintainer release candidate summary validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"candidate_summary_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
