#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ISSUE_TEMPLATE_ROUTE_NOTE_V0_1.md"

REQUIRED_TEMPLATE_ROUTE_IDS = {"RQPI001", "RQPI002", "RQPI003", "RQPI004", "RQPI005", "RQPI006"}
REQUIRED_CONTRIBUTOR_ROUTE_IDS = {"RQPC001", "RQPC002", "RQPC003", "RQPC004", "RQPC005", "RQPC006"}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ISSUE_TEMPLATE_ROUTE_NOTE_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_CONTRIBUTOR_ROUTE_NOTE_V0_1.md",
    "docs/reviewer_question_maintainer_public_preview_contributor_route_note_v0_1.json",
    "docs/REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_RELEASE_CARD_V0_1.md",
    "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Reviewer question maintainer public preview issue template route note v0.1",
    "Issue template route note rows: 6",
    "Contributor route note rows represented: 6",
    "Release card rows represented: 6",
    "Navigation rows represented: 6",
    "Rollup rows represented: 6",
    "Archive rows represented: 5",
    "Closure rows represented: 5",
    "Handoff rows represented: 5",
    "Decision rows represented: 5",
    "Candidate summary rows represented: 5",
    "Audit trail rows represented: 5",
    "Evidence rows represented: 5",
    "Readiness rows represented: 5",
    "Closeout rows represented: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "Issue history rows represented: 11",
    "Previous public issue represented: 69",
    "current public preview route only",
    "ready_for_public_preview_issue_template_route_note",
    "Boundary issue template route row",
    "Reviewer question issue template route row",
    "Blocked wording issue template route row",
    "Public surface issue template route row",
    "Validation issue template route row",
    "Next build issue template route row",
    "benchmark scoring",
    "benchmark compatibility",
    "benchmark equivalence",
    "endpoint result",
    "patient data",
    "clinical validation",
    "clinical deployment",
    "model ranking",
    "official endorsement",
    "route access",
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
    "not route access",
    "not an official endorsement",
    "make reviewer_question_maintainer_public_preview_issue_template_route_note",
    "Add a reviewer question maintainer public preview maintainer acceptance checklist without scoring",
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
    expected_counts = {
        "issue_template_route_note_row_count": 6,
        "contributor_route_note_rows_represented": 6,
        "release_card_rows_represented": 6,
        "navigation_rows_represented": 6,
        "rollup_rows_represented": 6,
        "archive_rows_represented": 5,
        "closure_rows_represented": 5,
        "handoff_rows_represented": 5,
        "decision_rows_represented": 5,
        "candidate_summary_rows_represented": 5,
        "audit_trail_rows_represented": 5,
        "evidence_rows_represented": 5,
        "readiness_rows_represented": 5,
        "closeout_rows_represented": 5,
        "contributor_digest_rows_represented": 5,
        "release_index_surface_rows_represented": 9,
        "issue_history_rows_represented": 11,
        "previous_public_issue_number": 69,
    }
    for key, value in expected_counts.items():
        if data.get(key) != value:
            errors.append(f"{key} must be {value}")
    if data.get("public_preview_issue_template_route_note") != "ready_for_public_preview_issue_template_route_note":
        errors.append("public_preview_issue_template_route_note must be ready_for_public_preview_issue_template_route_note")
    if data.get("maintainer_review_scope") != "current public preview route only":
        errors.append("maintainer_review_scope must be current public preview route only")
    if len(rows) != 6:
        errors.append(f"Expected 6 issue template route note rows, found {len(rows)}")

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
        "no_route_access_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    template_route_ids = {str(row.get("template_route_id")) for row in rows}
    if template_route_ids != REQUIRED_TEMPLATE_ROUTE_IDS:
        errors.append("template route id set must match required ids")
    contributor_route_ids = {str(row.get("source_contributor_route_id")) for row in rows}
    if contributor_route_ids != REQUIRED_CONTRIBUTOR_ROUTE_IDS:
        errors.append("source contributor route id set must match required ids")
    if {str(row.get("template_route_state")) for row in rows} != {"ready_for_public_preview_issue_template_route_note"}:
        errors.append("all template route states must be ready_for_public_preview_issue_template_route_note")

    for row in rows:
        template_route_id = str(row.get("template_route_id", ""))
        for key in [
            "template_route_name",
            "source_contributor_route_id",
            "template_route_note",
            "template_route_state",
            "template_route_boundary",
            "template_route_decision",
            "blocked_claims",
        ]:
            if key not in row:
                errors.append(f"{template_route_id}: missing {key}")

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
        errors.append("Generated outward facing issue template route note must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question maintainer public preview issue template route note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question maintainer public preview issue template route note validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"issue_template_route_note_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
