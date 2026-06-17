#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_closeout_digest_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_index_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_INDEX_V0_1.md"

ARCHIVE_INDEX_ROWS = [
    {
        "archive_index_id": "RQPX001",
        "source_closeout_digest_id": "RQPD001",
        "archive_index_name": "Boundary archive index row",
        "archive_index_note": "archive only when synthetic only and not for clinical use wording remains visible",
    },
    {
        "archive_index_id": "RQPX002",
        "source_closeout_digest_id": "RQPD002",
        "archive_index_name": "Reviewer question archive index row",
        "archive_index_note": "archive only when reviewer question proposal fields are complete and bounded",
    },
    {
        "archive_index_id": "RQPX003",
        "source_closeout_digest_id": "RQPD003",
        "archive_index_name": "Blocked wording archive index row",
        "archive_index_note": "archive only when blocked wording stays separated from publishable wording",
    },
    {
        "archive_index_id": "RQPX004",
        "source_closeout_digest_id": "RQPD004",
        "archive_index_name": "Public surface archive index row",
        "archive_index_note": "archive only when public surface references avoid access and endorsement claims",
    },
    {
        "archive_index_id": "RQPX005",
        "source_closeout_digest_id": "RQPD005",
        "archive_index_name": "Validation archive index row",
        "archive_index_note": "archive only when generated artifact checks are recorded before public maintainer review",
    },
    {
        "archive_index_id": "RQPX006",
        "source_closeout_digest_id": "RQPD006",
        "archive_index_name": "Next build archive index row",
        "archive_index_note": "archive only when next maintainer material stays inside the same public preview boundary",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    closeout_digest_ids = {row["closeout_digest_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in ARCHIVE_INDEX_ROWS:
        if row["source_closeout_digest_id"] not in closeout_digest_ids:
            raise ValueError(f"missing source closeout digest id: {row['source_closeout_digest_id']}")
        rows.append(
            {
                **row,
                "archive_index_state": "ready_for_public_preview_acceptance_archive_index",
                "archive_boundary": "synthetic only and not for clinical use",
                "archive_decision": "publish acceptance archive index only",
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
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_index_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_closeout_digest_v0_1.json",
        "acceptance_archive_index_row_count": len(rows),
        "acceptance_closeout_digest_rows_represented": source["acceptance_closeout_digest_row_count"],
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
        "previous_public_issue_number": 72,
        "public_preview_acceptance_archive_index": "ready_for_public_preview_acceptance_archive_index",
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
        "# Reviewer question maintainer public preview acceptance archive index v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive index gives a compact public archive path for reviewer question maintainer acceptance checks.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive index rows: {len(rows)}",
        "",
        f"Acceptance closeout digest rows represented: {data['acceptance_closeout_digest_rows_represented']}",
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
        "Public preview acceptance archive index: `ready_for_public_preview_acceptance_archive_index`",
        "",
        "## Acceptance archive index rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['archive_index_id']}",
                "",
                f"Archive index name: {row['archive_index_name']}",
                "",
                f"Source closeout digest row: `{row['source_closeout_digest_id']}`",
                "",
                f"Archive index note: {row['archive_index_note']}",
                "",
                f"Archive index state: `{row['archive_index_state']}`",
                "",
                f"Archive decision: {row['archive_decision']}",
                "",
                f"Archive boundary: {row['archive_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_index",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive release note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_index_rows={len(rows)}")


if __name__ == "__main__":
    main()
