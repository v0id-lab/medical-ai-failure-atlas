#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RELEASE_INDEX = ROOT / "docs" / "label_audit" / "label_audit_public_release_index_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_public_contributor_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_PUBLIC_CONTRIBUTOR_DIGEST_V0_1.md"

DIGEST_STEPS = [
    {
        "step_id": "LACD001",
        "step_name": "Read the release index",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_RELEASE_INDEX_V0_1.md",
        "contributor_action": "start from the durable route index",
    },
    {
        "step_id": "LACD002",
        "step_name": "Check the contributor route",
        "public_file": "docs/label_audit/PUBLIC_LABEL_AUDIT_CONTRIBUTOR_ISSUE_V0_1.md",
        "contributor_action": "confirm that the example is synthetic and allowed",
    },
    {
        "step_id": "LACD003",
        "step_name": "Compare example intake rows",
        "public_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "contributor_action": "match the proposed row to an existing intake pattern",
    },
    {
        "step_id": "LACD004",
        "step_name": "Review blocked wording",
        "public_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "contributor_action": "avoid dataset quality proof and clinical validation wording",
    },
    {
        "step_id": "LACD005",
        "step_name": "Run the release index check",
        "public_file": "Makefile",
        "contributor_action": "run make label_audit_release_index before opening or updating an issue",
    },
]


def main() -> None:
    release_index = json.loads(RELEASE_INDEX.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = [
        {
            **row,
            "digest_status": "included_in_public_contributor_digest",
            "boundary": "synthetic only and not for clinical use",
        }
        for row in DIGEST_STEPS
    ]

    data: dict[str, Any] = {
        "version": "label_audit_public_contributor_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_public_release_index_v0_1.json",
        "digest_step_count": len(rows),
        "release_index_surface_rows_represented": release_index["index_surface_count"],
        "issue_history_rows_represented": release_index["issue_history_count"],
        "digest_decision": "ready_for_public_preview",
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
        "# Label audit public contributor digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This digest gives contributors a short orientation path for using the label audit release index before opening or updating a synthetic label audit issue.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Digest step rows: {len(rows)}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Issue history rows represented: {data['issue_history_rows_represented']}",
        "",
        "Digest decision: `ready_for_public_preview`",
        "",
        "## Contributor steps",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['step_id']}",
                "",
                f"Step name: {row['step_name']}",
                "",
                f"Public file: `{row['public_file']}`",
                "",
                f"Contributor action: {row['contributor_action']}",
                "",
                f"Digest status: `{row['digest_status']}`",
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
            "make label_audit_contributor_digest",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"digest_step_rows={len(rows)}")


if __name__ == "__main__":
    main()
