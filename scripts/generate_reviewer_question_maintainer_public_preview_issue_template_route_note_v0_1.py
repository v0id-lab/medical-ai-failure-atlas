#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_maintainer_public_preview_contributor_route_note_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_ISSUE_TEMPLATE_ROUTE_NOTE_V0_1.md"

ISSUE_TEMPLATE_ROWS = [
    {
        "template_route_id": "RQPI001",
        "source_contributor_route_id": "RQPC001",
        "template_route_name": "Boundary issue template route row",
        "template_route_note": "route issue template wording toward synthetic only and not for clinical use examples",
    },
    {
        "template_route_id": "RQPI002",
        "source_contributor_route_id": "RQPC002",
        "template_route_name": "Reviewer question issue template route row",
        "template_route_note": "route contributor reviewer question proposals into public issue template fields",
    },
    {
        "template_route_id": "RQPI003",
        "source_contributor_route_id": "RQPC003",
        "template_route_name": "Blocked wording issue template route row",
        "template_route_note": "route blocked wording into issue template warnings before maintainer review",
    },
    {
        "template_route_id": "RQPI004",
        "source_contributor_route_id": "RQPC004",
        "template_route_name": "Public surface issue template route row",
        "template_route_note": "route public surface references into trace fields without access claims",
    },
    {
        "template_route_id": "RQPI005",
        "source_contributor_route_id": "RQPC005",
        "template_route_name": "Validation issue template route row",
        "template_route_note": "route local checks into issue template readiness fields before public maintainer review",
    },
    {
        "template_route_id": "RQPI006",
        "source_contributor_route_id": "RQPC006",
        "template_route_name": "Next build issue template route row",
        "template_route_note": "route next maintainer acceptance checklist material inside the same public preview boundary",
    },
]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    route_ids = {row["route_id"] for row in source["rows"]}
    rows: list[dict[str, Any]] = []
    for row in ISSUE_TEMPLATE_ROWS:
        if row["source_contributor_route_id"] not in route_ids:
            raise ValueError(f"missing source contributor route id: {row['source_contributor_route_id']}")
        rows.append(
            {
                **row,
                "template_route_state": "ready_for_public_preview_issue_template_route_note",
                "template_route_boundary": "synthetic only and not for clinical use",
                "template_route_decision": "publish issue template route note only",
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
        "version": "reviewer_question_maintainer_public_preview_issue_template_route_note_v0_1",
        "status": "public_preview",
        "date": "2026 06 18",
        "source": "docs/reviewer_question_maintainer_public_preview_contributor_route_note_v0_1.json",
        "issue_template_route_note_row_count": len(rows),
        "contributor_route_note_rows_represented": source["contributor_route_note_row_count"],
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
        "previous_public_issue_number": 69,
        "public_preview_issue_template_route_note": "ready_for_public_preview_issue_template_route_note",
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
        "# Reviewer question maintainer public preview issue template route note v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 18",
        "",
        "This issue template route note gives a compact public path for reviewer question proposal fields after the contributor route note.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Issue template route note rows: {len(rows)}",
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
        "Public preview issue template route note: `ready_for_public_preview_issue_template_route_note`",
        "",
        "## Issue template route note rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['template_route_id']}",
                "",
                f"Template route name: {row['template_route_name']}",
                "",
                f"Source contributor route row: `{row['source_contributor_route_id']}`",
                "",
                f"Template route note: {row['template_route_note']}",
                "",
                f"Template route state: `{row['template_route_state']}`",
                "",
                f"Template route decision: {row['template_route_decision']}",
                "",
                f"Template route boundary: {row['template_route_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_issue_template_route_note",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview maintainer acceptance checklist without scoring, compatibility, endpoint, patient data, clinical validation, route access, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"issue_template_route_note_rows={len(rows)}")


if __name__ == "__main__":
    main()
