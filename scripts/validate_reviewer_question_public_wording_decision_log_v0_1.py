#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_wording_decision_log_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md"

REQUIRED_BLOCKED_WORDING = {
    "the locator proves the claim",
    "the policy requirement is established",
    "the answer proves safe escalation",
    "the answer gives safe individualized medication advice",
}
REQUIRED_PROPOSED_WORDING = {
    "locator format still needs source support",
    "policy source and clause are required",
    "escalation boundary remains under review",
    "individualized medication advice is blocked",
}
REQUIRED_FILES = [
    "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/reviewer_question_public_wording_decision_log_v0_1.json",
    "docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md",
    "docs/reviewer_question_intake_triage_board_v0_1.json",
    "docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md",
    "docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md",
    "failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md",
]
REQUIRED_PHRASES = [
    "Reviewer question public wording decision log v0.1",
    "Public wording decision rows: 4",
    "Blocked wording examples: 4",
    "Proposed public wording examples: 4",
    "Decision status values represented: 1",
    "safe_public_wording_ready",
    "the locator proves the claim",
    "the policy requirement is established",
    "the answer proves safe escalation",
    "the answer gives safe individualized medication advice",
    "locator format still needs source support",
    "policy source and clause are required",
    "escalation boundary remains under review",
    "individualized medication advice is blocked",
    "not clinical advice",
    "not patient data",
    "not raw model output",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "make reviewer_question_wording_log",
    "Add a release gate checklist for reviewer question public wording decisions without scoring",
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
    if data.get("decision_row_count") != 4:
        errors.append("decision_row_count must be 4")
    if len(rows) != 4:
        errors.append(f"Expected 4 decision rows, found {len(rows)}")
    if data.get("blocked_wording_count") != 4:
        errors.append("blocked_wording_count must be 4")
    if data.get("proposed_public_wording_count") != 4:
        errors.append("proposed_public_wording_count must be 4")
    if data.get("decision_status_count") != 1:
        errors.append("decision_status_count must be 1")

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

    blocked = {str(row.get("blocked_wording")) for row in rows}
    proposed = {str(row.get("proposed_public_wording")) for row in rows}
    statuses = {str(row.get("decision_status")) for row in rows}
    if blocked != REQUIRED_BLOCKED_WORDING:
        errors.append("blocked wording set must match required examples")
    if proposed != REQUIRED_PROPOSED_WORDING:
        errors.append("proposed wording set must match required examples")
    if statuses != {"safe_public_wording_ready"}:
        errors.append("decision status must be safe_public_wording_ready")

    for row in rows:
        row_id = str(row.get("intake_id", ""))
        for key in [
            "template",
            "benchmark_reviewer_question_id",
            "reviewer_role_id",
            "reviewer_role_name",
            "blocked_public_claim_type",
            "blocked_wording",
            "proposed_public_wording",
            "decision_status",
            "maintainer_action",
            "next_public_surface",
            "track_a_value",
            "track_b_value",
        ]:
            if key not in row:
                errors.append(f"{row_id}: missing {key}")

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
        errors.append("Generated outward facing wording decision log must not contain hyphen characters")

    if errors:
        print("FAIL reviewer question public wording decision log validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS reviewer question public wording decision log validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"decision_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
