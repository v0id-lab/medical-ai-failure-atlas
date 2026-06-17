#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "reviewer_question_maintainer_public_preview_handoff_summary_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_closure_checklist_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_CLOSURE_CHECKLIST_V0_1.md"

CLOSURE_ROWS = [
    {
        "closure_id": "RQPC001",
        "source_handoff_id": "RQPH001",
        "closure_name": "Synthetic boundary closure",
        "closure_check": "confirm public preview text says synthetic only and not for clinical use",
    },
    {
        "closure_id": "RQPC002",
        "source_handoff_id": "RQPH002",
        "closure_name": "Reviewer question lane closure",
        "closure_check": "confirm reviewer question links stay source facing and do not imply benchmark scoring",
    },
    {
        "closure_id": "RQPC003",
        "source_handoff_id": "RQPH003",
        "closure_name": "Public wording closure",
        "closure_check": "confirm public wording blocks clinical validation, compatibility, endpoint, and endorsement claims",
    },
    {
        "closure_id": "RQPC004",
        "source_handoff_id": "RQPH004",
        "closure_name": "Release surface closure",
        "closure_check": "confirm release surfaces do not imply official endorsement or route access",
    },
    {
        "closure_id": "RQPC005",
        "source_handoff_id": "RQPH005",
        "closure_name": "Validation closure",
        "closure_check": "confirm runnable checks fail when closure rows or safety boundaries are missing",
    },
]


def main() -> None:
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    handoff_ids = {row["handoff_id"] for row in handoff["rows"]}
    rows: list[dict[str, Any]] = []
    for row in CLOSURE_ROWS:
        if row["source_handoff_id"] not in handoff_ids:
            raise ValueError(f"missing source handoff id: {row['source_handoff_id']}")
        rows.append(
            {
                **row,
                "closure_state": "ready_to_close_public_preview_item",
                "closure_boundary": "synthetic only and not for clinical use",
                "closure_decision": "close public preview checklist item only",
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
        "version": "reviewer_question_maintainer_public_preview_closure_checklist_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_public_preview_handoff_summary_v0_1.json",
        "closure_row_count": len(rows),
        "handoff_rows_represented": handoff["handoff_row_count"],
        "decision_rows_represented": handoff["decision_rows_represented"],
        "candidate_summary_rows_represented": handoff["candidate_summary_rows_represented"],
        "audit_trail_rows_represented": handoff["audit_trail_rows_represented"],
        "evidence_rows_represented": handoff["evidence_rows_represented"],
        "readiness_rows_represented": handoff["readiness_rows_represented"],
        "closeout_rows_represented": handoff["closeout_rows_represented"],
        "contributor_digest_rows_represented": handoff["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": handoff["release_index_surface_rows_represented"],
        "issue_history_rows_represented": handoff["issue_history_rows_represented"],
        "previous_public_issue_number": 63,
        "public_preview_closure": "ready_to_close_public_preview_item",
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
        "# Reviewer question maintainer public preview closure checklist v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This closure checklist turns the maintainer public preview handoff summary into closeable reviewer checks for the current public preview route.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, not route access, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Closure rows: {len(rows)}",
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
        "Public preview closure: `ready_to_close_public_preview_item`",
        "",
        "## Maintainer closure rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['closure_id']}",
                "",
                f"Closure name: {row['closure_name']}",
                "",
                f"Source handoff row: `{row['source_handoff_id']}`",
                "",
                f"Closure check: {row['closure_check']}",
                "",
                f"Closure state: `{row['closure_state']}`",
                "",
                f"Closure decision: {row['closure_decision']}",
                "",
                f"Closure boundary: {row['closure_boundary']}",
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
            "make reviewer_question_maintainer_public_preview_closure_checklist",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview archive digest without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"closure_rows={len(rows)}")


if __name__ == "__main__":
    main()
