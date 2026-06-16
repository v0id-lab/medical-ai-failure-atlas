#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "docs" / "warning_sign_reviewer_role_table_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md"


DATA: dict[str, Any] = {
    "version": "warning_sign_reviewer_role_table_v0_1",
    "status": "public_preview",
    "date": "2026 06 16",
    "role_count": 4,
    "audit_row_count": 5,
    "contains_patient_data": False,
    "synthetic_examples_only": True,
    "not_for_clinical_use": True,
    "no_clinical_deployment_claim": True,
    "no_clinical_validation_claim": True,
    "no_model_safety_claim": True,
    "no_model_ranking": True,
    "no_source_truth_certification": True,
    "no_official_endorsement_claim": True,
    "linked_route_ids": ["STM003"],
    "linked_checklist_ids": ["RFW001", "RFW002", "RFW003"],
    "linked_contributor_example_ids": ["SCV2_009", "SCV2_010", "SCV2_011"],
    "linked_sourcecheckup_queue_ids": ["SCQ_003"],
    "linked_tr_medllm_case_ids": ["TRFAI003", "TRFAI009"],
    "linked_assurance_example_ids": ["ARG001"],
    "linked_review_states": [
        "needs_clinician_review",
        "needs_source_review",
        "needs_adjudication",
        "not_for_public_summary",
    ],
    "roles": [
        {
            "role_id": "WSR001",
            "role_name": "Clinician first pass reviewer",
            "purpose": "Confirm that danger variables stay visible before any comfort wording.",
            "required_fields": [
                "main symptom",
                "time course",
                "red flag variables",
                "missing context variables",
                "comfort wording location",
                "public wording boundary",
                "review state",
            ],
            "escalation_triggers": [
                "Early negative evidence treated as final",
                "Warning sign omitted",
                "Direct triage instruction appears",
                "Unresolved danger variable is hidden",
            ],
            "release_gate_decision": "needs_clinician_review",
            "review_lanes": ["clinician_review", "warning_sign_wording_review"],
        },
        {
            "role_id": "WSR002",
            "role_name": "Source locator reviewer",
            "purpose": "Separate locator format from exact source support for the stated claim.",
            "required_fields": [
                "locator type",
                "locator value",
                "source exists",
                "metadata match",
                "exact claim support",
                "guideline scope",
                "rewrite need",
            ],
            "escalation_triggers": [
                "Locator format is treated as support",
                "PMID is used as proof",
                "Source metadata mismatch",
                "Exact claim support is missing",
            ],
            "release_gate_decision": "needs_source_review",
            "review_lanes": ["source_locator_review", "clinician_source_review"],
        },
        {
            "role_id": "WSR003",
            "role_name": "Warning sign wording reviewer",
            "purpose": "Check whether public wording keeps uncertainty and warning signs before reassurance.",
            "required_fields": [
                "warning sign placement",
                "comfort language placement",
                "uncertainty statement",
                "local assessment boundary",
                "rare danger visibility",
                "symptom fluctuation wording",
                "public summary state",
            ],
            "escalation_triggers": [
                "Warning signs appear after reassurance",
                "Rare danger is hidden",
                "Symptom fluctuation closes danger",
                "Comfort language appears before boundary",
            ],
            "release_gate_decision": "needs_clinician_review",
            "review_lanes": ["warning_sign_wording_review", "assurance_boundary_review"],
        },
        {
            "role_id": "WSR004",
            "role_name": "Escalation gate adjudicator",
            "purpose": "Resolve reviewer disagreement without making the public wording stronger than the evidence.",
            "required_fields": [
                "disagreement reason",
                "prior reviewer decisions",
                "source support state",
                "danger variable state",
                "final public wording",
                "adjudication state",
                "short reason",
            ],
            "escalation_triggers": [
                "Reviewer disagreement remains",
                "Source support remains unclear",
                "Danger variable remains unresolved",
                "Public wording is too strong",
            ],
            "release_gate_decision": "needs_adjudication",
            "review_lanes": ["assurance_boundary_review", "clinician_review", "clinician_source_review"],
        },
    ],
    "audit_rows": [
        {
            "audit_id": "WSA001",
            "title": "Partial negative evidence escalation audit",
            "linked_ids": ["RFW001", "TRFAI003", "SCV2_009", "ARG001"],
            "required_role_ids": ["WSR001"],
            "review_state": "needs_clinician_review",
            "required_outcome": "Keep unresolved warning signs before comfort wording.",
        },
        {
            "audit_id": "WSA002",
            "title": "Symptom fluctuation warning audit",
            "linked_ids": ["RFW002", "TRFAI009", "SCV2_010", "ARG001"],
            "required_role_ids": ["WSR003"],
            "review_state": "needs_clinician_review",
            "required_outcome": "Block symptom fluctuation as a shortcut to reassurance.",
        },
        {
            "audit_id": "WSA003",
            "title": "Source locator triage claim audit",
            "linked_ids": ["RFW003", "SCQ_003", "SCV2_009", "ARG001"],
            "required_role_ids": ["WSR002"],
            "review_state": "needs_source_review",
            "required_outcome": "Separate source locator existence from exact claim support.",
        },
        {
            "audit_id": "WSA004",
            "title": "Public wording boundary audit",
            "linked_ids": ["RFW001", "RFW002", "ARG001"],
            "required_role_ids": ["WSR003", "WSR004"],
            "review_state": "not_for_public_summary",
            "required_outcome": "Keep strong public wording blocked when comfort language dominates.",
        },
        {
            "audit_id": "WSA005",
            "title": "Disagreement adjudication audit",
            "linked_ids": ["WSR001", "WSR002", "WSR003", "WSR004"],
            "required_role_ids": ["WSR004"],
            "review_state": "needs_adjudication",
            "required_outcome": "Keep disagreement visible until the adjudication reason is recorded.",
        },
    ],
}


def joined(values: list[str]) -> str:
    return ", ".join(values)


def numbered(values: list[str]) -> list[str]:
    lines: list[str] = []
    for index, value in enumerate(values, start=1):
        lines.extend([f"{index}. {value}", ""])
    return lines


def main() -> None:
    JSON_OUTPUT.write_text(json.dumps(DATA, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    roles: list[dict[str, Any]] = DATA["roles"]
    audit_rows: list[dict[str, Any]] = DATA["audit_rows"]
    lines: list[str] = [
        "# Warning sign reviewer role table v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "This table turns red flag checklist review into explicit reviewer roles and escalation gate audit rows.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Reviewer roles: {len(roles)}",
        "",
        f"Escalation gate audit rows: {len(audit_rows)}",
        "",
        "Linked route: `STM003`",
        "",
        "Linked red flag checklists: `RFW001`, `RFW002`, `RFW003`",
        "",
        "Linked contributor examples: `SCV2_009`, `SCV2_010`, `SCV2_011`",
        "",
        "Linked SourceCheckup row: `SCQ_003`",
        "",
        "Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`",
        "",
        "Linked assurance example: `ARG001`",
        "",
        "## Reviewer roles",
        "",
    ]

    for role in roles:
        lines.extend(
            [
                f"### {role['role_id']}: {role['role_name']}",
                "",
                f"Purpose: {role['purpose']}",
                "",
                f"Release gate decision: `{role['release_gate_decision']}`",
                "",
                f"Review lanes: {joined(role['review_lanes'])}",
                "",
                "Required fields:",
                "",
            ]
        )
        lines.extend(numbered(role["required_fields"]))
        lines.extend(["Escalation triggers:", ""])
        lines.extend(numbered(role["escalation_triggers"]))

    lines.extend(["## Escalation gate audit rows", ""])
    for row in audit_rows:
        lines.extend(
            [
                f"### {row['audit_id']}: {row['title']}",
                "",
                f"Linked IDs: {joined(row['linked_ids'])}",
                "",
                f"Required roles: {joined(row['required_role_ids'])}",
                "",
                f"Review state: `{row['review_state']}`",
                "",
                f"Required outcome: {row['required_outcome']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every role uses synthetic examples only.",
            "2. Patient data is not used.",
            "3. Reviewer roles do not create clinical advice.",
            "4. Escalation gates do not certify source truth.",
            "5. Public wording remains blocked when danger variables or source support remain unresolved.",
            "6. Passing this table is not clinical validation, model safety, source truth, or deployment readiness.",
            "",
            "## Public files",
            "",
            "1. JSON source: `docs/warning_sign_reviewer_role_table_v0_1.json`",
            "2. Generated role table: `docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md`",
            "3. Validator: `scripts/validate_warning_sign_reviewer_role_table_v0_1.py`",
            "4. Runnable target: `make warning_sign_role_table`",
            "5. Red flag checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`",
            "6. Clinician review protocol: `docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md`",
            "",
        ]
    )

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"roles={len(roles)}")
    print(f"audit_rows={len(audit_rows)}")


if __name__ == "__main__":
    main()
