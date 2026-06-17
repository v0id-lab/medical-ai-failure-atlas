#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "label_audit" / "label_audit_release_note_packet_v0_1.json"
CHANGELOG = ROOT / "docs" / "label_audit" / "label_audit_public_changelog_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_public_release_index_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md"

INDEX_SURFACES = [
    {
        "surface_id": "LARI001",
        "surface_name": "Public contributor route",
        "public_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "role": "opens the synthetic label audit issue route",
    },
    {
        "surface_id": "LARI002",
        "surface_name": "Example intake rows",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "role": "shows synthetic provenance and label review rows",
    },
    {
        "surface_id": "LARI003",
        "surface_name": "Example dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_DASHBOARD_V0_1.md",
        "role": "summarizes role, audit row, review state, and blocked claim type",
    },
    {
        "surface_id": "LARI004",
        "surface_name": "Maintainer triage board",
        "public_file": "docs/label_audit/LABEL_AUDIT_MAINTAINER_TRIAGE_BOARD_V0_1.md",
        "role": "maps dashboard rows to maintainer actions",
    },
    {
        "surface_id": "LARI005",
        "surface_name": "Public wording decision log",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "role": "records blocked wording and safer public wording",
    },
    {
        "surface_id": "LARI006",
        "surface_name": "Release gate checklist",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md",
        "role": "turns wording decisions into release checks",
    },
    {
        "surface_id": "LARI007",
        "surface_name": "Release gate outcome dashboard",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md",
        "role": "summarizes current pass and block outcomes",
    },
    {
        "surface_id": "LARI008",
        "surface_name": "Release note packet",
        "public_file": "docs/label_audit/LABEL_AUDIT_RELEASE_NOTE_PACKET_V0_1.md",
        "role": "packages the label audit route into one release note surface",
    },
    {
        "surface_id": "LARI009",
        "surface_name": "Public changelog",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_CHANGELOG_V0_1.md",
        "role": "records the chronological maintainer sequence",
    },
]

ISSUE_HISTORY = [
    (19, "Roadmap: Label audit reviewer role table", "label audit reviewer roles", "reviewer role table added"),
    (20, "Roadmap: Label audit public contributor issue route", "label audit issue route", "public contributor route added"),
    (21, "Roadmap: Label audit example intake rows", "label audit examples", "example intake rows added"),
    (22, "Roadmap: Label audit example dashboard", "label audit dashboard", "example dashboard added"),
    (23, "Roadmap: Label audit maintainer triage board", "label audit triage", "maintainer triage board added"),
    (24, "Roadmap: Label audit public wording decisions", "label audit wording", "public wording decision log added"),
    (25, "Roadmap: Label audit release gate checklist", "label audit release gates", "release gate checklist added"),
    (26, "Roadmap: Label audit release gate outcome dashboard", "label audit outcomes", "release gate outcome dashboard added"),
    (27, "Roadmap: Label audit release note packet", "label audit release packet", "release note packet added"),
    (28, "Roadmap: Label audit public changelog", "label audit changelog", "public changelog added"),
]


def main() -> None:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    changelog = json.loads(CHANGELOG.read_text(encoding="utf-8"))
    surfaces: list[dict[str, Any]] = [
        {
            **surface,
            "index_status": "included_in_public_release_index",
            "next_action": "keep linked surface current during public preview",
        }
        for surface in INDEX_SURFACES
    ]
    issues: list[dict[str, Any]] = [
        {
            "issue_number": number,
            "issue_title": title,
            "issue_state": "closed",
            "public_label": label,
            "public_value": value,
        }
        for number, title, label, value in ISSUE_HISTORY
    ]

    data: dict[str, Any] = {
        "version": "label_audit_public_release_index_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "sources": [
            "docs/label_audit/label_audit_release_note_packet_v0_1.json",
            "docs/label_audit/label_audit_public_changelog_v0_1.json",
        ],
        "index_surface_count": len(surfaces),
        "issue_history_count": len(issues),
        "release_note_packet_rows_represented": packet["packet_surface_count"],
        "changelog_rows_represented": changelog["change_row_count"],
        "index_decision": "ready_for_public_preview",
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_model_safety_claim": True,
        "no_model_ranking": True,
        "no_dataset_quality_proof": True,
        "no_official_endorsement_claim": True,
        "surfaces": surfaces,
        "issue_history": issues,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit public release index v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This index is the durable public entry point for the label audit contributor route, release packet, changelog, validation commands, and public issue history.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Index surface rows: {len(surfaces)}",
        "",
        f"Issue history rows: {len(issues)}",
        "",
        f"Release note packet rows represented: {data['release_note_packet_rows_represented']}",
        "",
        f"Changelog rows represented: {data['changelog_rows_represented']}",
        "",
        "Index decision: `ready_for_public_preview`",
        "",
        "## Public surfaces",
        "",
    ]

    for surface in surfaces:
        lines.extend(
            [
                f"### {surface['surface_id']}",
                "",
                f"Surface name: {surface['surface_name']}",
                "",
                f"Public file: `{surface['public_file']}`",
                "",
                f"Role: {surface['role']}",
                "",
                f"Index status: `{surface['index_status']}`",
                "",
                f"Next action: {surface['next_action']}",
                "",
            ]
        )

    lines.extend(["## Public issue history", ""])
    for issue in issues:
        lines.extend(
            [
                f"### Issue {issue['issue_number']}",
                "",
                f"Title: {issue['issue_title']}",
                "",
                f"State: {issue['issue_state']}",
                "",
                f"Public label: {issue['public_label']}",
                "",
                f"Public value: {issue['public_value']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_release_index",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"index_surface_rows={len(surfaces)}")
    print(f"issue_history_rows={len(issues)}")


if __name__ == "__main__":
    main()
