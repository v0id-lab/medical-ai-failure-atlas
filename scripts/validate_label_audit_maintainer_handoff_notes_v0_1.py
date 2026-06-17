#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_maintainer_handoff_notes_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_HANDOFF_NOTES_V0_1.md"

REQUIRED_HANDOFF_IDS = {"LAMH001", "LAMH002", "LAMH003", "LAMH004", "LAMH005"}
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_HANDOFF_NOTES_V0_1.md",
    "docs/label_audit/label_audit_maintainer_handoff_notes_v0_1.json",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
    "Makefile",
]
REQUIRED_PHRASES = [
    "Label audit maintainer handoff notes v0.1",
    "Handoff rows: 5",
    "Contributor digest rows represented: 5",
    "Release index surface rows represented: 9",
    "ready_for_public_preview",
    "Confirm synthetic scope",
    "Check intake fit",
    "Check blocked wording",
    "Check release route",
    "Run maintainer checks",
    "included_in_public_maintainer_handoff",
    "maintainer_review_required",
    "synthetic only and not for clinical use",
    "not proof of dataset quality",
    "not clinical advice",
    "not patient data",
    "not raw model output release",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not regulatory approval",
    "not an official endorsement",
    "make label_audit_maintainer_handoff",
]
FORBIDDEN_PHRASES = [
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
    "dataset quality is proven",
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
    if data.get("handoff_row_count") != 5:
        errors.append("handoff_row_count must be 5")
    if data.get("contributor_digest_rows_represented") != 5:
        errors.append("contributor_digest_rows_represented must be 5")
    if data.get("release_index_surface_rows_represented") != 9:
        errors.append("release_index_surface_rows_represented must be 9")
    if data.get("handoff_decision") != "ready_for_public_preview":
        errors.append("handoff_decision must be ready_for_public_preview")
    if len(rows) != 5:
        errors.append(f"Expected 5 handoff rows, found {len(rows)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_raw_model_output_release",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_dataset_quality_proof",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    handoff_ids = {str(row.get("handoff_id")) for row in rows}
    if handoff_ids != REQUIRED_HANDOFF_IDS:
        errors.append("handoff id set must match required ids")
    if {str(row.get("handoff_status")) for row in rows} != {"included_in_public_maintainer_handoff"}:
        errors.append("all handoff statuses must be included_in_public_maintainer_handoff")
    if {str(row.get("closeout_state")) for row in rows} != {"maintainer_review_required"}:
        errors.append("all closeout states must be maintainer_review_required")

    for row in rows:
        handoff_id = str(row.get("handoff_id", ""))
        for key in ["handoff_name", "public_file", "maintainer_action", "handoff_status", "closeout_state", "boundary"]:
            if key not in row:
                errors.append(f"{handoff_id}: missing {key}")

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
        errors.append("Generated outward facing maintainer handoff notes must not contain hyphen characters")

    if errors:
        print("FAIL label audit maintainer handoff notes validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit maintainer handoff notes validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"handoff_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
