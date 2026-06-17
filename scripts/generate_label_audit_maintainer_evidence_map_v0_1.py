#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "docs" / "label_audit" / "label_audit_maintainer_release_readiness_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_evidence_map_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_EVIDENCE_MAP_V0_1.md"

EVIDENCE_ROWS = [
    {
        "evidence_id": "LAME001",
        "evidence_name": "Synthetic boundary evidence",
        "source_readiness_id": "LAMR001",
        "source_file": "docs/label_audit/LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
        "maintainer_use": "check that public examples remain synthetic only",
    },
    {
        "evidence_id": "LAME002",
        "evidence_name": "Intake pattern evidence",
        "source_readiness_id": "LAMR002",
        "source_file": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "maintainer_use": "check that intake rows map to label audit review patterns",
    },
    {
        "evidence_id": "LAME003",
        "evidence_name": "Public wording evidence",
        "source_readiness_id": "LAMR003",
        "source_file": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_use": "check that blocked claims stay out of public wording",
    },
    {
        "evidence_id": "LAME004",
        "evidence_name": "Release surface evidence",
        "source_readiness_id": "LAMR004",
        "source_file": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "maintainer_use": "check that public surfaces expose boundaries and runnable checks",
    },
    {
        "evidence_id": "LAME005",
        "evidence_name": "Validation evidence",
        "source_readiness_id": "LAMR005",
        "source_file": "Makefile",
        "maintainer_use": "check that the evidence map is generated and validated before issue closeout",
    },
]


def main() -> None:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    readiness_ids = {row["readiness_id"] for row in readiness["rows"]}
    rows: list[dict[str, Any]] = []
    for row in EVIDENCE_ROWS:
        if row["source_readiness_id"] not in readiness_ids:
            raise ValueError(f"missing source readiness id: {row['source_readiness_id']}")
        rows.append(
            {
                **row,
                "evidence_status": "mapped_for_public_maintainer_review",
                "evidence_state": "current_preview_evidence",
                "boundary": "synthetic only and not for clinical use",
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_evidence_map_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_release_readiness_digest_v0_1.json",
        "evidence_row_count": len(rows),
        "readiness_rows_represented": readiness["readiness_row_count"],
        "closeout_rows_represented": readiness["closeout_rows_represented"],
        "handoff_rows_represented": readiness["handoff_rows_represented"],
        "contributor_digest_rows_represented": readiness["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": readiness["release_index_surface_rows_represented"],
        "previous_public_issue_number": 33,
        "evidence_map_decision": "mapped_for_public_preview_review",
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
        "# Label audit maintainer evidence map v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This evidence map gives maintainers a compact way to trace each release readiness row to the public evidence surface it depends on.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Evidence rows: {len(rows)}",
        "",
        f"Readiness rows represented: {data['readiness_rows_represented']}",
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
        "Evidence map decision: `mapped_for_public_preview_review`",
        "",
        "## Maintainer evidence rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['evidence_id']}",
                "",
                f"Evidence name: {row['evidence_name']}",
                "",
                f"Source readiness row: `{row['source_readiness_id']}`",
                "",
                f"Source file: `{row['source_file']}`",
                "",
                f"Maintainer use: {row['maintainer_use']}",
                "",
                f"Evidence status: `{row['evidence_status']}`",
                "",
                f"Evidence state: `{row['evidence_state']}`",
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
            "make label_audit_maintainer_evidence_map",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"evidence_rows={len(rows)}")


if __name__ == "__main__":
    main()
