#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIGEST = ROOT / "docs" / "label_audit" / "label_audit_public_contributor_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_handoff_notes_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_HANDOFF_NOTES_V0_1.md"

HANDOFF_ROWS = [
    {
        "handoff_id": "LAMH001",
        "handoff_name": "Confirm synthetic scope",
        "public_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "maintainer_action": "reject or redact any row that could describe a real patient",
    },
    {
        "handoff_id": "LAMH002",
        "handoff_name": "Check intake fit",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "maintainer_action": "map the proposal to an existing synthetic intake pattern",
    },
    {
        "handoff_id": "LAMH003",
        "handoff_name": "Check blocked wording",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_action": "block dataset quality proof, clinical validation, and model safety wording",
    },
    {
        "handoff_id": "LAMH004",
        "handoff_name": "Check release route",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
        "maintainer_action": "confirm the change belongs in the public preview route",
    },
    {
        "handoff_id": "LAMH005",
        "handoff_name": "Run maintainer checks",
        "public_file": "Makefile",
        "maintainer_action": "run make label_audit_maintainer_handoff before public closeout",
    },
]


def main() -> None:
    digest = json.loads(DIGEST.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "handoff_status": "included_in_public_maintainer_handoff",
            "boundary": "synthetic only and not for clinical use",
            "closeout_state": "maintainer_review_required",
        }
        for row in HANDOFF_ROWS
    ]

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_handoff_notes_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_public_contributor_digest_v0_1.json",
        "handoff_row_count": len(rows),
        "contributor_digest_rows_represented": digest["digest_step_count"],
        "release_index_surface_rows_represented": digest["release_index_surface_rows_represented"],
        "handoff_decision": "ready_for_public_preview",
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
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit maintainer handoff notes v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "These handoff notes give maintainers a short checklist for reviewing synthetic label audit contributor proposals before public closeout.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Handoff rows: {len(rows)}",
        "",
        f"Contributor digest rows represented: {data['contributor_digest_rows_represented']}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        "Handoff decision: `ready_for_public_preview`",
        "",
        "## Maintainer handoff rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['handoff_id']}",
                "",
                f"Handoff name: {row['handoff_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Handoff status: `{row['handoff_status']}`",
                "",
                f"Closeout state: `{row['closeout_state']}`",
                "",
                f"Boundary: {row['boundary']}",
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
            "make label_audit_maintainer_handoff",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"handoff_rows={len(rows)}")


if __name__ == "__main__":
    main()
