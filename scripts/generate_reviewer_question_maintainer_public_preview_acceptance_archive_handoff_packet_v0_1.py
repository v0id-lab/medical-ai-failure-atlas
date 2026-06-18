#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_final_index_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_handoff_packet_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_HANDOFF_PACKET_V0_1.md"

HANDOFF_PACKET_ROWS = [
    {
        "handoff_packet_id": "RQPH001",
        "source_final_index_id": "RQPF001",
        "handoff_packet_name": "Boundary handoff packet row",
        "handoff_packet_note": "handoff only when synthetic only and not for clinical use wording remains visible",
    },
    {
        "handoff_packet_id": "RQPH002",
        "source_final_index_id": "RQPF002",
        "handoff_packet_name": "Reviewer question handoff packet row",
        "handoff_packet_note": "handoff only when reviewer question proposal fields are complete and bounded",
    },
    {
        "handoff_packet_id": "RQPH003",
        "source_final_index_id": "RQPF003",
        "handoff_packet_name": "Blocked wording handoff packet row",
        "handoff_packet_note": "handoff only when blocked wording stays separated from publishable wording",
    },
    {
        "handoff_packet_id": "RQPH004",
        "source_final_index_id": "RQPF004",
        "handoff_packet_name": "Public surface handoff packet row",
        "handoff_packet_note": "handoff only when public surface references avoid access and endorsement claims",
    },
    {
        "handoff_packet_id": "RQPH005",
        "source_final_index_id": "RQPF005",
        "handoff_packet_name": "Validation handoff packet row",
        "handoff_packet_note": "handoff only when generated artifact checks are recorded before public maintainer review",
    },
    {
        "handoff_packet_id": "RQPH006",
        "source_final_index_id": "RQPF006",
        "handoff_packet_name": "Next build handoff packet row",
        "handoff_packet_note": "handoff only when next maintainer material stays inside the same public preview boundary",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    final_index_ids = {row["final_index_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in HANDOFF_PACKET_ROWS:
        if row["source_final_index_id"] not in final_index_ids:
            raise ValueError(f"missing source final index id: {row['source_final_index_id']}")
        rows.append(
            {
                **row,
                "handoff_packet_state": "ready_for_public_preview_acceptance_archive_handoff_packet",
                "handoff_packet_boundary": "synthetic only and not for clinical use",
                "handoff_packet_decision": "publish acceptance archive handoff packet only",
                "blocked_claims": [
                    "benchmark scoring",
                    "benchmark compatibility",
                    "benchmark equivalence",
                    "endpoint result",
                    "patient data",
                    "clinical validation",
                    "clinical deployment",
                    "model ranking",
                    "official endorsement",
                    "route access",
                ],
            }
        )

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_handoff_packet_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_archive_final_index_v0_1.json",
        "acceptance_archive_handoff_packet_row_count": len(rows),
        "acceptance_archive_final_index_rows_represented": source["acceptance_archive_final_index_row_count"],
        "issue_template_route_note_rows_represented": source["issue_template_route_note_rows_represented"],
        "contributor_route_note_rows_represented": source["contributor_route_note_rows_represented"],
        "release_card_rows_represented": source["release_card_rows_represented"],
        "navigation_rows_represented": source["navigation_rows_represented"],
        "rollup_rows_represented": source["rollup_rows_represented"],
        "archive_rows_represented": source["archive_rows_represented"],
        "closure_rows_represented": source["closure_rows_represented"],
        "handoff_rows_represented": source["handoff_rows_represented"],
        "decision_rows_represented": source["decision_rows_represented"],
        "candidate_summary_rows_represented": source["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": source["audit_trail_rows_represented"],
        "evidence_rows_represented": source["evidence_rows_represented"],
        "readiness_rows_represented": source["readiness_rows_represented"],
        "closeout_rows_represented": source["closeout_rows_represented"],
        "contributor_digest_rows_represented": source["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": source["release_index_surface_rows_represented"],
        "issue_history_rows_represented": source["issue_history_rows_represented"],
        "previous_public_issue_number": 76,
        "public_preview_acceptance_archive_handoff_packet": "ready_for_public_preview_acceptance_archive_handoff_packet",
        "maintainer_review_scope": "current public preview route only",
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_endpoint_result": True,
        "no_score_report": True,
        "no_model_ranking": True,
        "no_benchmark_compatibility_claim": True,
        "no_benchmark_equivalence_claim": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_official_endorsement_claim": True,
        "no_route_access_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question maintainer public preview acceptance archive handoff packet v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive handoff packet gives a compact public archive handoff path for reviewer question maintainer acceptance checks.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive handoff packet rows: {len(rows)}",
        "",
        f"Acceptance archive final index rows represented: {data['acceptance_archive_final_index_rows_represented']}",
        "",
        f"Issue template route note rows represented: {data['issue_template_route_note_rows_represented']}",
        "",
        f"Contributor route note rows represented: {data['contributor_route_note_rows_represented']}",
        "",
        f"Release card rows represented: {data['release_card_rows_represented']}",
        "",
        f"Navigation rows represented: {data['navigation_rows_represented']}",
        "",
        f"Rollup rows represented: {data['rollup_rows_represented']}",
        "",
        f"Archive rows represented: {data['archive_rows_represented']}",
        "",
        f"Closure rows represented: {data['closure_rows_represented']}",
        "",
        f"Handoff rows represented: {data['handoff_rows_represented']}",
        "",
        f"Decision rows represented: {data['decision_rows_represented']}",
        "",
        f"Candidate summary rows represented: {data['candidate_summary_rows_represented']}",
        "",
        f"Audit trail rows represented: {data['audit_trail_rows_represented']}",
        "",
        f"Evidence rows represented: {data['evidence_rows_represented']}",
        "",
        f"Readiness rows represented: {data['readiness_rows_represented']}",
        "",
        f"Closeout rows represented: {data['closeout_rows_represented']}",
        "",
        f"Contributor digest rows represented: {data['contributor_digest_rows_represented']}",
        "",
        f"Release index surface rows represented: {data['release_index_surface_rows_represented']}",
        "",
        f"Issue history rows represented: {data['issue_history_rows_represented']}",
        "",
        f"Previous public issue represented: {data['previous_public_issue_number']}",
        "",
        "Maintainer review scope: current public preview route only",
        "",
        "Public preview acceptance archive handoff packet: `ready_for_public_preview_acceptance_archive_handoff_packet`",
        "",
        "## Acceptance archive handoff packet rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['handoff_packet_id']}",
                "",
                f"Handoff packet name: {row['handoff_packet_name']}",
                "",
                f"Source acceptance archive final index row: `{row['source_final_index_id']}`",
                "",
                f"Handoff packet note: {row['handoff_packet_note']}",
                "",
                f"Handoff packet state: `{row['handoff_packet_state']}`",
                "",
                f"Handoff packet decision: {row['handoff_packet_decision']}",
                "",
                f"Handoff packet boundary: {row['handoff_packet_boundary']}",
                "",
                "Blocked claims: benchmark scoring, benchmark compatibility, benchmark equivalence, endpoint result, patient data, clinical validation, clinical deployment, model ranking, official endorsement, route access",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_handoff_packet",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive steward note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_handoff_packet_rows={len(rows)}")


if __name__ == "__main__":
    main()
