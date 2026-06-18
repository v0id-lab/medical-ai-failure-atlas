#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_index_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_PUBLIC_HANDOFF_RELEASE_INDEX_V0_1.md"

PUBLIC_HANDOFF_RELEASE_INDEX_ROWS = [
    {
        "public_handoff_release_index_id": "RQPHRI001",
        "source_public_handoff_digest_id": "RQPHD001",
        "release_index_name": "Boundary public handoff release index row",
        "release_index_note": "release index keeps synthetic only and not for clinical use boundary first",
        "release_index_action": "make the boundary row the first public reading step",
    },
    {
        "public_handoff_release_index_id": "RQPHRI002",
        "source_public_handoff_digest_id": "RQPHD002",
        "release_index_name": "Reviewer question public handoff release index row",
        "release_index_note": "release index keeps reviewer questions visible as documentation fields",
        "release_index_action": "route reviewer question reading through public preview artifacts",
    },
    {
        "public_handoff_release_index_id": "RQPHRI003",
        "source_public_handoff_digest_id": "RQPHD003",
        "release_index_name": "Blocked wording public handoff release index row",
        "release_index_note": "release index keeps blocked wording visible before public summaries",
        "release_index_action": "keep scoring and compatibility wording blocked",
    },
    {
        "public_handoff_release_index_id": "RQPHRI004",
        "source_public_handoff_digest_id": "RQPHD004",
        "release_index_name": "Public surface public handoff release index row",
        "release_index_note": "release index links public preview surfaces without route access claims",
        "release_index_action": "list public surfaces as preview documents only",
    },
    {
        "public_handoff_release_index_id": "RQPHRI005",
        "source_public_handoff_digest_id": "RQPHD005",
        "release_index_name": "Validation public handoff release index row",
        "release_index_note": "release index keeps validation commands beside the public artifact list",
        "release_index_action": "run the release index check before public closeout",
    },
    {
        "public_handoff_release_index_id": "RQPHRI006",
        "source_public_handoff_digest_id": "RQPHD006",
        "release_index_name": "Next action public handoff release index row",
        "release_index_note": "release index keeps the next build bounded to public handoff release notation",
        "release_index_action": "keep external maintainer contact behind owner clearance",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_ids = {row["public_handoff_digest_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in PUBLIC_HANDOFF_RELEASE_INDEX_ROWS:
        if row["source_public_handoff_digest_id"] not in source_ids:
            raise ValueError(f"missing source public handoff digest id: {row['source_public_handoff_digest_id']}")
        rows.append(
            {
                **row,
                "public_handoff_release_index_state": "ready_for_public_preview_acceptance_archive_public_handoff_release_index",
                "public_handoff_release_index_boundary": "synthetic only and not for clinical use",
                "public_handoff_release_index_decision": "publish acceptance archive public handoff release index only",
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
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_index_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_digest_v0_1.json",
        "acceptance_archive_public_handoff_release_index_row_count": len(rows),
        "acceptance_archive_public_handoff_digest_rows_represented": source["acceptance_archive_public_handoff_digest_row_count"],
        "acceptance_archive_public_handoff_note_rows_represented": source["acceptance_archive_public_handoff_note_rows_represented"],
        "acceptance_archive_stewardship_digest_rows_represented": source["acceptance_archive_stewardship_digest_rows_represented"],
        "acceptance_archive_stewardship_closeout_rows_represented": source["acceptance_archive_stewardship_closeout_rows_represented"],
        "acceptance_archive_steward_index_rows_represented": source["acceptance_archive_steward_index_rows_represented"],
        "acceptance_archive_steward_note_rows_represented": source["acceptance_archive_steward_note_rows_represented"],
        "acceptance_archive_handoff_packet_rows_represented": source["acceptance_archive_handoff_packet_rows_represented"],
        "acceptance_archive_final_index_rows_represented": source["acceptance_archive_final_index_rows_represented"],
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
        "issue_history_rows_represented": source["issue_history_rows_represented"] + 1,
        "previous_public_issue_number": 83,
        "public_preview_acceptance_archive_public_handoff_release_index": "ready_for_public_preview_acceptance_archive_public_handoff_release_index",
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
        "# Reviewer question maintainer public preview acceptance archive public handoff release index v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive public handoff release index gives maintainers one public entry point for the current reviewer question archive handoff trail.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive public handoff release index rows: {len(rows)}",
        "",
        f"Acceptance archive public handoff digest rows represented: {data['acceptance_archive_public_handoff_digest_rows_represented']}",
        "",
        f"Acceptance archive public handoff note rows represented: {data['acceptance_archive_public_handoff_note_rows_represented']}",
        "",
        f"Acceptance archive stewardship digest rows represented: {data['acceptance_archive_stewardship_digest_rows_represented']}",
        "",
        f"Acceptance archive stewardship closeout rows represented: {data['acceptance_archive_stewardship_closeout_rows_represented']}",
        "",
        f"Acceptance archive steward index rows represented: {data['acceptance_archive_steward_index_rows_represented']}",
        "",
        f"Acceptance archive steward note rows represented: {data['acceptance_archive_steward_note_rows_represented']}",
        "",
        f"Acceptance archive handoff packet rows represented: {data['acceptance_archive_handoff_packet_rows_represented']}",
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
        "Public preview acceptance archive public handoff release index: `ready_for_public_preview_acceptance_archive_public_handoff_release_index`",
        "",
        "## Public handoff release index rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['public_handoff_release_index_id']}",
                "",
                f"Release index name: {row['release_index_name']}",
                "",
                f"Source acceptance archive public handoff digest row: `{row['source_public_handoff_digest_id']}`",
                "",
                f"Release index note: {row['release_index_note']}",
                "",
                f"Release index action: {row['release_index_action']}",
                "",
                f"Public handoff release index state: `{row['public_handoff_release_index_state']}`",
                "",
                f"Public handoff release index decision: {row['public_handoff_release_index_decision']}",
                "",
                f"Public handoff release index boundary: {row['public_handoff_release_index_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_public_handoff_release_index",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive public handoff release note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_public_handoff_release_index_rows={len(rows)}")


if __name__ == "__main__":
    main()
