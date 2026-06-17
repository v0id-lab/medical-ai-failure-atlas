#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "label_audit" / "label_audit_maintainer_handoff_notes_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_closeout_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md"

CLOSEOUT_ROWS = [
    {
        "closeout_id": "LAMC001",
        "closeout_name": "Synthetic scope closeout",
        "evidence_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "closeout_action": "record that public examples stay synthetic only",
    },
    {
        "closeout_id": "LAMC002",
        "closeout_name": "Intake fit closeout",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "closeout_action": "record that proposed rows map to existing synthetic intake patterns",
    },
    {
        "closeout_id": "LAMC003",
        "closeout_name": "Blocked wording closeout",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "closeout_action": "record that blocked public wording remains excluded",
    },
    {
        "closeout_id": "LAMC004",
        "closeout_name": "Release route closeout",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
        "closeout_action": "record that the change stays inside public preview route",
    },
    {
        "closeout_id": "LAMC005",
        "closeout_name": "Validation closeout",
        "evidence_file": "Makefile",
        "closeout_action": "run make label_audit_maintainer_closeout_digest before issue closure",
    },
]


def main() -> None:
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "closeout_status": "included_in_public_maintainer_closeout_digest",
            "closeout_state": "current_preview_closed",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in CLOSEOUT_ROWS
    ]

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_closeout_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_handoff_notes_v0_1.json",
        "closeout_row_count": len(rows),
        "handoff_rows_represented": handoff["handoff_row_count"],
        "contributor_digest_rows_represented": handoff["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": handoff["release_index_surface_rows_represented"],
        "previous_public_issue_number": 31,
        "closeout_decision": "ready_for_public_preview",
        "maintainer_review_scope": "current public preview route only",
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
        "# Label audit maintainer closeout digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives maintainers a compact closeout trail for synthetic label audit public preview updates after handoff review.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Closeout rows: {len(rows)}",
        "",
        f"Handoff rows represented: {data['handoff_rows_represented']}",
        "",
        f"Contributor digest rows represented: {data['contributor_digest_rows_represented']}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Previous public issue represented: {data['previous_public_issue_number']}",
        "",
        "Maintainer review scope: current public preview route only",
        "",
        "Closeout decision: `ready_for_public_preview`",
        "",
        "## Maintainer closeout rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['closeout_id']}",
                "",
                f"Closeout name: {row['closeout_name']}",
                "",
                f"Evidence file: `{row['evidence_file']}`",
                "",
                f"Closeout action: {row['closeout_action']}",
                "",
                f"Closeout status: `{row['closeout_status']}`",
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
            "make label_audit_maintainer_closeout_digest",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"closeout_rows={len(rows)}")


if __name__ == "__main__":
    main()
