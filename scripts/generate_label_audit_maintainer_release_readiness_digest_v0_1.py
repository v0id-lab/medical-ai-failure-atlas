#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_closeout_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_release_readiness_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_RELEASE_READINESS_DIGEST_V0_1.md"

READINESS_ROWS = [
    {
        "readiness_id": "LAMR001",
        "readiness_name": "Synthetic boundary readiness",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
        "readiness_action": "confirm closeout keeps public examples synthetic only",
    },
    {
        "readiness_id": "LAMR002",
        "readiness_name": "Intake pattern readiness",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "readiness_action": "confirm intake rows remain mapped to synthetic patterns",
    },
    {
        "readiness_id": "LAMR003",
        "readiness_name": "Public wording readiness",
        "evidence_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "readiness_action": "confirm blocked wording stays out of public surfaces",
    },
    {
        "readiness_id": "LAMR004",
        "readiness_name": "Release surface readiness",
        "evidence_file": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "readiness_action": "confirm release surfaces mention boundaries and runnable checks",
    },
    {
        "readiness_id": "LAMR005",
        "readiness_name": "Validation readiness",
        "evidence_file": "Makefile",
        "readiness_action": "run make label_audit_maintainer_release_readiness_digest before issue closure",
    },
]


def main() -> None:
    closeout = json.loads(CLOSEOUT.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "readiness_status": "included_in_public_maintainer_release_readiness_digest",
            "readiness_state": "current_preview_ready",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in READINESS_ROWS
    ]

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_release_readiness_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_closeout_digest_v0_1.json",
        "readiness_row_count": len(rows),
        "closeout_rows_represented": closeout["closeout_row_count"],
        "handoff_rows_represented": closeout["handoff_rows_represented"],
        "contributor_digest_rows_represented": closeout["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": closeout["release_index_surface_rows_represented"],
        "previous_public_issue_number": 32,
        "readiness_decision": "ready_for_public_preview",
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
        "# Label audit maintainer release readiness digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives maintainers a compact public preview readiness trail after label audit closeout review.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Readiness rows: {len(rows)}",
        "",
        f"Closeout rows represented: {data['closeout_rows_represented']}",
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
        "Readiness decision: `ready_for_public_preview`",
        "",
        "## Maintainer readiness rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['readiness_id']}",
                "",
                f"Readiness name: {row['readiness_name']}",
                "",
                f"Evidence file: `{row['evidence_file']}`",
                "",
                f"Readiness action: {row['readiness_action']}",
                "",
                f"Readiness status: `{row['readiness_status']}`",
                "",
                f"Readiness state: `{row['readiness_state']}`",
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
            "make label_audit_maintainer_release_readiness_digest",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"readiness_rows={len(rows)}")


if __name__ == "__main__":
    main()
