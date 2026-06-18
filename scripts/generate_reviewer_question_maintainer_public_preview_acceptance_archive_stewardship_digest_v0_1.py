#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_closeout_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_digest_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ACCEPTANCE_ARCHIVE_STEWARDSHIP_DIGEST_V0_1.md"

DIGEST_ROWS = [
    {
        "stewardship_digest_id": "RQPSD001",
        "source_stewardship_closeout_id": "RQPSC001",
        "digest_name": "Boundary digest row",
        "digest_note": "preserve synthetic only and not for clinical use wording as the first reader check",
        "reader_action": "read the boundary sentence before any archive reuse",
    },
    {
        "stewardship_digest_id": "RQPSD002",
        "source_stewardship_closeout_id": "RQPSC002",
        "digest_name": "Reviewer question digest row",
        "digest_note": "summarize reviewer question completeness without scoring or endpoint results",
        "reader_action": "review completeness fields before proposing a public wording change",
    },
    {
        "stewardship_digest_id": "RQPSD003",
        "source_stewardship_closeout_id": "RQPSC003",
        "digest_name": "Blocked wording digest row",
        "digest_note": "keep blocked wording visible when a maintainer prepares an archive update",
        "reader_action": "compare proposed text against blocked claim types",
    },
    {
        "stewardship_digest_id": "RQPSD004",
        "source_stewardship_closeout_id": "RQPSC004",
        "digest_name": "Public surface digest row",
        "digest_note": "point readers to public surfaces without implying route access or endorsement",
        "reader_action": "use linked public files only as preview documentation",
    },
    {
        "stewardship_digest_id": "RQPSD005",
        "source_stewardship_closeout_id": "RQPSC005",
        "digest_name": "Validation digest row",
        "digest_note": "summarize runnable validation before public archive reuse",
        "reader_action": "run the digest check before opening a public issue",
    },
    {
        "stewardship_digest_id": "RQPSD006",
        "source_stewardship_closeout_id": "RQPSC006",
        "digest_name": "Next action digest row",
        "digest_note": "carry only the next safe public build inside the same bounded archive route",
        "reader_action": "keep any external maintainer contact behind owner clearance",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    closeout_ids = {row["stewardship_closeout_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in DIGEST_ROWS:
        if row["source_stewardship_closeout_id"] not in closeout_ids:
            raise ValueError(f"missing source stewardship closeout id: {row['source_stewardship_closeout_id']}")
        rows.append(
            {
                **row,
                "digest_state": "ready_for_public_preview_acceptance_archive_stewardship_digest",
                "digest_boundary": "synthetic only and not for clinical use",
                "digest_decision": "publish acceptance archive stewardship digest only",
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
        "version": "reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_digest_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_closeout_v0_1.json",
        "acceptance_archive_stewardship_digest_row_count": len(rows),
        "acceptance_archive_stewardship_closeout_rows_represented": source["acceptance_archive_stewardship_closeout_row_count"],
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
        "previous_public_issue_number": 80,
        "public_preview_acceptance_archive_stewardship_digest": "ready_for_public_preview_acceptance_archive_stewardship_digest",
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
        "# Reviewer question maintainer public preview acceptance archive stewardship digest v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This acceptance archive stewardship digest gives maintainers and contributors one compact reading path for the current reviewer question public preview archive.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Acceptance archive stewardship digest rows: {len(rows)}",
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
        "Public preview acceptance archive stewardship digest: `ready_for_public_preview_acceptance_archive_stewardship_digest`",
        "",
        "## Digest rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['stewardship_digest_id']}",
                "",
                f"Digest name: {row['digest_name']}",
                "",
                f"Source acceptance archive stewardship closeout row: `{row['source_stewardship_closeout_id']}`",
                "",
                f"Digest note: {row['digest_note']}",
                "",
                f"Reader action: {row['reader_action']}",
                "",
                f"Digest state: `{row['digest_state']}`",
                "",
                f"Digest decision: {row['digest_decision']}",
                "",
                f"Digest boundary: {row['digest_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_acceptance_archive_stewardship_digest",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview acceptance archive public handoff note without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"acceptance_archive_stewardship_digest_rows={len(rows)}")


if __name__ == "__main__":
    main()
