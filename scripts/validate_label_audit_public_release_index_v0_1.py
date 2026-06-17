#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "label_audit" / "label_audit_public_release_index_v0_1.json"
MARKDOWN = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md"

REQUIRED_SURFACE_IDS = {
    "LARI001",
    "LARI002",
    "LARI003",
    "LARI004",
    "LARI005",
    "LARI006",
    "LARI007",
    "LARI008",
    "LARI009",
}
REQUIRED_ISSUES = set(range(19, 29))
REQUIRED_FILES = [
    "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
    "docs/label_audit/label_audit_public_release_index_v0_1.json",
    "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md",
    "docs/label_audit/LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md",
]
REQUIRED_PHRASES = [
    "Label audit public release index v0.1",
    "Index surface rows: 9",
    "Issue history rows: 10",
    "Release note packet rows represented: 7",
    "Changelog rows represented: 8",
    "ready_for_public_preview",
    "Public contributor route",
    "Example intake rows",
    "Example dashboard",
    "Maintainer triage board",
    "Public wording decision log",
    "Release gate checklist",
    "Release gate outcome dashboard",
    "Release note packet",
    "Public changelog",
    "included_in_public_release_index",
    "Roadmap: Label audit reviewer role table",
    "Roadmap: Label audit public contributor issue route",
    "Roadmap: Label audit example intake rows",
    "Roadmap: Label audit example dashboard",
    "Roadmap: Label audit maintainer triage board",
    "Roadmap: Label audit public wording decisions",
    "Roadmap: Label audit release gate checklist",
    "Roadmap: Label audit release gate outcome dashboard",
    "Roadmap: Label audit release note packet",
    "Roadmap: Label audit public changelog",
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
    "make label_audit_release_index",
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
        data: dict[str, Any] = {"surfaces": [], "issue_history": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    surfaces = data.get("surfaces", [])
    issues = data.get("issue_history", [])
    if not isinstance(surfaces, list):
        errors.append("surfaces must be a list")
        surfaces = []
    if not isinstance(issues, list):
        errors.append("issue_history must be a list")
        issues = []
    if data.get("index_surface_count") != 9:
        errors.append("index_surface_count must be 9")
    if data.get("issue_history_count") != 10:
        errors.append("issue_history_count must be 10")
    if data.get("release_note_packet_rows_represented") != 7:
        errors.append("release_note_packet_rows_represented must be 7")
    if data.get("changelog_rows_represented") != 8:
        errors.append("changelog_rows_represented must be 8")
    if data.get("index_decision") != "ready_for_public_preview":
        errors.append("index_decision must be ready_for_public_preview")
    if len(surfaces) != 9:
        errors.append(f"Expected 9 index surfaces, found {len(surfaces)}")
    if len(issues) != 10:
        errors.append(f"Expected 10 issue history rows, found {len(issues)}")

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

    surface_ids = {str(row.get("surface_id")) for row in surfaces}
    issue_numbers = {int(row.get("issue_number", -1)) for row in issues}
    if surface_ids != REQUIRED_SURFACE_IDS:
        errors.append("surface id set must match required ids")
    if issue_numbers != REQUIRED_ISSUES:
        errors.append("issue numbers must be 19 through 28")
    if {str(row.get("index_status")) for row in surfaces} != {"included_in_public_release_index"}:
        errors.append("all index statuses must be included_in_public_release_index")
    if {str(row.get("issue_state")) for row in issues} != {"closed"}:
        errors.append("all issue history states must be closed")

    for row in surfaces:
        surface_id = str(row.get("surface_id", ""))
        for key in ["surface_name", "public_file", "role", "index_status", "next_action"]:
            if key not in row:
                errors.append(f"{surface_id}: missing {key}")
    for row in issues:
        issue_number = str(row.get("issue_number", ""))
        for key in ["issue_title", "issue_state", "public_label", "public_value"]:
            if key not in row:
                errors.append(f"issue {issue_number}: missing {key}")

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
        errors.append("Generated outward facing release index must not contain hyphen characters")

    if errors:
        print("FAIL label audit public release index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS label audit public release index validation")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"index_surface_rows={len(surfaces)}")
    print(f"issue_history_rows={len(issues)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
