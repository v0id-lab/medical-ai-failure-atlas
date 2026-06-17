#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "docs" / "reviewer_question_maintainer_release_candidate_summary_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_public_preview_decision_log_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_PUBLIC_PREVIEW_DECISION_LOG_V0_1.md"

DECISION_ROWS = [
    {
        "decision_id": "RQMP001",
        "decision_name": "Synthetic boundary decision",
        "source_summary_id": "RQMC001",
        "decision_surface": "docs/REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md",
        "public_preview_decision": "allow synthetic boundary summary for public preview",
    },
    {
        "decision_id": "RQMP002",
        "decision_name": "Reviewer question lane decision",
        "source_summary_id": "RQMC002",
        "decision_surface": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "public_preview_decision": "allow source facing reviewer question lane summary for public preview",
    },
    {
        "decision_id": "RQMP003",
        "decision_name": "Public wording decision",
        "source_summary_id": "RQMC003",
        "decision_surface": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "public_preview_decision": "allow bounded public wording summary for public preview",
    },
    {
        "decision_id": "RQMP004",
        "decision_name": "Release surface decision",
        "source_summary_id": "RQMC004",
        "decision_surface": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "public_preview_decision": "allow linked release surface summary for public preview",
    },
    {
        "decision_id": "RQMP005",
        "decision_name": "Validation decision",
        "source_summary_id": "RQMC005",
        "decision_surface": "Makefile",
        "public_preview_decision": "allow runnable validation summary for public preview",
    },
]


def main() -> int:
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    summary_ids = {row["summary_id"] for row in candidate["rows"]}
    rows: list[dict[str, Any]] = []
    for row in DECISION_ROWS:
        if row["source_summary_id"] not in summary_ids:
            raise ValueError(f"missing source summary id: {row['source_summary_id']}")
        rows.append(
            {
                **row,
                "decision_status": "allowed_for_public_preview_only",
                "decision_state": "current_preview_decision",
                "boundary": "synthetic only and not for clinical use",
            }
        )

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_public_preview_decision_log_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_release_candidate_summary_v0_1.json",
        "decision_row_count": len(rows),
        "candidate_summary_rows_represented": candidate["candidate_summary_row_count"],
        "audit_trail_rows_represented": candidate["audit_trail_rows_represented"],
        "evidence_rows_represented": candidate["evidence_rows_represented"],
        "readiness_rows_represented": candidate["readiness_rows_represented"],
        "closeout_rows_represented": candidate["closeout_rows_represented"],
        "handoff_rows_represented": candidate["handoff_rows_represented"],
        "contributor_digest_rows_represented": candidate["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": candidate["release_index_surface_rows_represented"],
        "issue_history_rows_represented": candidate["issue_history_rows_represented"],
        "previous_public_issue_number": 61,
        "public_preview_decision": "allow_public_preview_only",
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
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Reviewer question maintainer public preview decision log v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This decision log records the maintainer public preview decision state after reviewer question release candidate summary review.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Decision rows: {len(rows)}",
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
        f"Handoff rows represented: {data['handoff_rows_represented']}",
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
        "Public preview decision: `allow_public_preview_only`",
        "",
        "## Maintainer decision rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['decision_id']}",
                "",
                f"Decision name: {row['decision_name']}",
                "",
                f"Source summary row: `{row['source_summary_id']}`",
                "",
                f"Decision surface: `{row['decision_surface']}`",
                "",
                f"Public preview decision: {row['public_preview_decision']}",
                "",
                f"Decision status: `{row['decision_status']}`",
                "",
                f"Decision state: `{row['decision_state']}`",
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
            "make reviewer_question_maintainer_public_preview_decision_log",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview handoff summary without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"decision_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
