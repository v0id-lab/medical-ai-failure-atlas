#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "label_audit" / "label_audit_maintainer_evidence_map_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_maintainer_audit_trail_packet_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md"

TRAIL_ROWS = [
    {
        "trail_id": "LAMT001",
        "trail_name": "Synthetic boundary trail",
        "source_evidence_id": "LAME001",
        "audit_surface": "docs/label_audit/LABEL_AUDIT_MAINTAINER_CLOSEOUT_DIGEST_V0_1.md",
        "maintainer_check": "record that public examples remain synthetic only",
    },
    {
        "trail_id": "LAMT002",
        "trail_name": "Intake pattern trail",
        "source_evidence_id": "LAME002",
        "audit_surface": "docs/label_audit/LABEL_AUDIT_EXAMPLE_INTAKE_V0_1.md",
        "maintainer_check": "record that intake rows stay mapped to label audit review patterns",
    },
    {
        "trail_id": "LAMT003",
        "trail_name": "Public wording trail",
        "source_evidence_id": "LAME003",
        "audit_surface": "docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_check": "record that blocked claims stay out of public wording",
    },
    {
        "trail_id": "LAMT004",
        "trail_name": "Release surface trail",
        "source_evidence_id": "LAME004",
        "audit_surface": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "maintainer_check": "record that public surfaces expose boundaries and runnable checks",
    },
    {
        "trail_id": "LAMT005",
        "trail_name": "Validation trail",
        "source_evidence_id": "LAME005",
        "audit_surface": "Makefile",
        "maintainer_check": "record that audit trail packet generation and validation ran before issue closeout",
    },
]


def main() -> None:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    evidence_ids = {row["evidence_id"] for row in evidence["rows"]}
    rows: list[dict[str, Any]] = []
    for row in TRAIL_ROWS:
        if row["source_evidence_id"] not in evidence_ids:
            raise ValueError(f"missing source evidence id: {row['source_evidence_id']}")
        rows.append(
            {
                **row,
                "trail_status": "ready_for_public_maintainer_audit_trail",
                "trail_state": "current_preview_trail",
                "boundary": "synthetic only and not for clinical use",
            }
        )

    data: dict[str, Any] = {
        "version": "label_audit_maintainer_audit_trail_packet_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_maintainer_evidence_map_v0_1.json",
        "audit_trail_row_count": len(rows),
        "evidence_rows_represented": evidence["evidence_row_count"],
        "readiness_rows_represented": evidence["readiness_rows_represented"],
        "closeout_rows_represented": evidence["closeout_rows_represented"],
        "handoff_rows_represented": evidence["handoff_rows_represented"],
        "contributor_digest_rows_represented": evidence["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": evidence["release_index_surface_rows_represented"],
        "previous_public_issue_number": 34,
        "audit_trail_decision": "ready_for_public_preview_audit_trail",
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
        "# Label audit maintainer audit trail packet v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This audit trail packet gives maintainers a compact public preview trail from evidence map rows to the audit surface each row depends on.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Audit trail rows: {len(rows)}",
        "",
        f"Evidence rows represented: {data['evidence_rows_represented']}",
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
        "Audit trail decision: `ready_for_public_preview_audit_trail`",
        "",
        "## Maintainer audit trail rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['trail_id']}",
                "",
                f"Trail name: {row['trail_name']}",
                "",
                f"Source evidence row: `{row['source_evidence_id']}`",
                "",
                f"Audit surface: `{row['audit_surface']}`",
                "",
                f"Maintainer check: {row['maintainer_check']}",
                "",
                f"Trail status: `{row['trail_status']}`",
                "",
                f"Trail state: `{row['trail_state']}`",
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
            "make label_audit_maintainer_audit_trail_packet",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"audit_trail_rows={len(rows)}")


if __name__ == "__main__":
    main()
