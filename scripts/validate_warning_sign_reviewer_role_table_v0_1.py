#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "warning_sign_reviewer_role_table_v0_1.json"
TABLE = ROOT / "docs" / "WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md"

REQUIRED_ROLES = {"WSR001", "WSR002", "WSR003", "WSR004"}
REQUIRED_AUDITS = {"WSA001", "WSA002", "WSA003", "WSA004", "WSA005"}
REQUIRED_CHECKLISTS = {"RFW001", "RFW002", "RFW003"}
REQUIRED_CONTRIBUTOR_EXAMPLES = {"SCV2_009", "SCV2_010", "SCV2_011"}
REQUIRED_ROUTE_IDS = {"STM003"}
REQUIRED_SOURCECHECKUP_ROWS = {"SCQ_003"}
REQUIRED_TR_CASES = {"TRFAI003", "TRFAI009"}
REQUIRED_ASSURANCE_EXAMPLES = {"ARG001"}
REQUIRED_REVIEW_STATES = {
    "needs_clinician_review",
    "needs_source_review",
    "needs_adjudication",
    "not_for_public_summary",
}
REQUIRED_RELEASE_GATE_DECISIONS = {
    "needs_clinician_review",
    "needs_source_review",
    "needs_adjudication",
}
REQUIRED_REVIEW_LANES = {
    "clinician_review",
    "warning_sign_wording_review",
    "source_locator_review",
    "assurance_boundary_review",
    "clinician_source_review",
}

REQUIRED_PHRASES = [
    "Warning sign reviewer role table v0.1",
    "Status: generated public preview.",
    "Reviewer roles: 4",
    "Escalation gate audit rows: 5",
    "Linked route: `STM003`",
    "Linked red flag checklists: `RFW001`, `RFW002`, `RFW003`",
    "Linked contributor examples: `SCV2_009`, `SCV2_010`, `SCV2_011`",
    "Linked SourceCheckup row: `SCQ_003`",
    "Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`",
    "Linked assurance example: `ARG001`",
    "Clinician first pass reviewer",
    "Source locator reviewer",
    "Warning sign wording reviewer",
    "Escalation gate adjudicator",
    "Partial negative evidence escalation audit",
    "Symptom fluctuation warning audit",
    "Source locator triage claim audit",
    "Public wording boundary audit",
    "Disagreement adjudication audit",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "Passing this table is not clinical validation",
    "make warning_sign_role_table",
    "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md",
    "docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def flatten(items: list[dict[str, Any]], key: str) -> set[str]:
    values: set[str] = set()
    for item in items:
        values.update(str(value) for value in item.get(key, []))
    return values


def main() -> int:
    errors: list[str] = []
    if not SOURCE.exists():
        errors.append(f"Missing source JSON: {SOURCE.relative_to(ROOT)}")
        data: dict[str, Any] = {"roles": [], "audit_rows": []}
    else:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))

    roles = data.get("roles", [])
    audit_rows = data.get("audit_rows", [])
    if not isinstance(roles, list):
        errors.append("roles must be a list")
        roles = []
    if not isinstance(audit_rows, list):
        errors.append("audit_rows must be a list")
        audit_rows = []
    if data.get("role_count") != 4:
        errors.append("role_count must be 4")
    if data.get("audit_row_count") != 5:
        errors.append("audit_row_count must be 5")
    if len(roles) != 4:
        errors.append(f"Expected 4 roles, found {len(roles)}")
    if len(audit_rows) != 5:
        errors.append(f"Expected 5 audit rows, found {len(audit_rows)}")

    for field in [
        "contains_patient_data",
        "synthetic_examples_only",
        "not_for_clinical_use",
        "no_clinical_deployment_claim",
        "no_clinical_validation_claim",
        "no_model_safety_claim",
        "no_model_ranking",
        "no_source_truth_certification",
        "no_official_endorsement_claim",
    ]:
        expected = False if field == "contains_patient_data" else True
        if data.get(field) is not expected:
            errors.append(f"{field} must be {expected}")

    checks = [
        ("route IDs", REQUIRED_ROUTE_IDS, set(map(str, data.get("linked_route_ids", [])))),
        ("checklists", REQUIRED_CHECKLISTS, set(map(str, data.get("linked_checklist_ids", [])))),
        (
            "contributor examples",
            REQUIRED_CONTRIBUTOR_EXAMPLES,
            set(map(str, data.get("linked_contributor_example_ids", []))),
        ),
        (
            "SourceCheckup rows",
            REQUIRED_SOURCECHECKUP_ROWS,
            set(map(str, data.get("linked_sourcecheckup_queue_ids", []))),
        ),
        ("TR MedLLM cases", REQUIRED_TR_CASES, set(map(str, data.get("linked_tr_medllm_case_ids", [])))),
        (
            "assurance examples",
            REQUIRED_ASSURANCE_EXAMPLES,
            set(map(str, data.get("linked_assurance_example_ids", []))),
        ),
        ("review states", REQUIRED_REVIEW_STATES, set(map(str, data.get("linked_review_states", [])))),
    ]
    for label, required, found in checks:
        missing = sorted(required - found)
        if missing:
            errors.append(f"Missing {label}: {', '.join(missing)}")

    found_roles = {str(role.get("role_id")) for role in roles}
    missing_roles = sorted(REQUIRED_ROLES - found_roles)
    if missing_roles:
        errors.append(f"Missing roles: {', '.join(missing_roles)}")
    found_audits = {str(row.get("audit_id")) for row in audit_rows}
    missing_audits = sorted(REQUIRED_AUDITS - found_audits)
    if missing_audits:
        errors.append(f"Missing audit rows: {', '.join(missing_audits)}")

    for role in roles:
        role_id = str(role.get("role_id", ""))
        for key in [
            "role_name",
            "purpose",
            "required_fields",
            "escalation_triggers",
            "release_gate_decision",
            "review_lanes",
        ]:
            if key not in role:
                errors.append(f"{role_id}: missing {key}")
        if len(role.get("required_fields", [])) < 6:
            errors.append(f"{role_id}: must include at least 6 required fields")
        if len(role.get("escalation_triggers", [])) < 4:
            errors.append(f"{role_id}: must include at least 4 escalation triggers")
        if str(role.get("release_gate_decision")) not in REQUIRED_RELEASE_GATE_DECISIONS:
            errors.append(f"{role_id}: unsupported release gate decision")

    found_lanes = flatten(roles, "review_lanes")
    missing_lanes = sorted(REQUIRED_REVIEW_LANES - found_lanes)
    if missing_lanes:
        errors.append(f"Missing review lanes: {', '.join(missing_lanes)}")

    for row in audit_rows:
        audit_id = str(row.get("audit_id", ""))
        for key in ["title", "linked_ids", "required_role_ids", "review_state", "required_outcome"]:
            if key not in row:
                errors.append(f"{audit_id}: missing {key}")
        if str(row.get("review_state")) not in REQUIRED_REVIEW_STATES:
            errors.append(f"{audit_id}: unsupported review state")
        for role_id in row.get("required_role_ids", []):
            if str(role_id) not in REQUIRED_ROLES:
                errors.append(f"{audit_id}: unknown required role {role_id}")

    if not TABLE.exists():
        errors.append(f"Missing generated table: {TABLE.relative_to(ROOT)}")
        text = ""
    else:
        text = TABLE.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated table missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing role table must not contain hyphen characters")

    if errors:
        print("FAIL warning sign reviewer role table validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS warning sign reviewer role table validation")
    print(f"table={TABLE.relative_to(ROOT)}")
    print(f"roles={len(roles)}")
    print(f"audit_rows={len(audit_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
