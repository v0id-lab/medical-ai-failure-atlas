#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRAIL = ROOT / "docs" / "reviewer_question_maintainer_audit_trail_packet_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "reviewer_question_maintainer_release_candidate_summary_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "REVIEWER_QUESTION_MAINTAINER_RELEASE_CANDIDATE_SUMMARY_V0_1.md"

SUMMARY_ROWS = [
    {
        "summary_id": "RQMC001",
        "summary_name": "Synthetic boundary candidate",
        "source_trail_id": "RQMT001",
        "candidate_surface": "docs/REVIEWER_QUESTION_MAINTAINER_AUDIT_TRAIL_PACKET_V0_1.md",
        "maintainer_decision": "candidate remains synthetic only",
    },
    {
        "summary_id": "RQMC002",
        "summary_name": "Reviewer question lane candidate",
        "source_trail_id": "RQMT002",
        "candidate_surface": "docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
        "maintainer_decision": "candidate keeps reviewer question lanes source facing and bounded",
    },
    {
        "summary_id": "RQMC003",
        "summary_name": "Public wording candidate",
        "source_trail_id": "RQMT003",
        "candidate_surface": "docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md",
        "maintainer_decision": "candidate keeps blocked score, endpoint, compatibility, validation, and endorsement wording out",
    },
    {
        "summary_id": "RQMC004",
        "summary_name": "Release surface candidate",
        "source_trail_id": "RQMT004",
        "candidate_surface": "docs/PUBLIC_RELEASE_NOTE_V0_1_20260616.md",
        "maintainer_decision": "candidate surfaces remain linked from public release notes",
    },
    {
        "summary_id": "RQMC005",
        "summary_name": "Validation candidate",
        "source_trail_id": "RQMT005",
        "candidate_surface": "Makefile",
        "maintainer_decision": "candidate keeps runnable validation before issue closeout",
    },
]


def main() -> int:
    trail = json.loads(TRAIL.read_text(encoding="utf-8"))
    trail_ids = {row["trail_id"] for row in trail["rows"]}
    rows: list[dict[str, Any]] = []
    for row in SUMMARY_ROWS:
        if row["source_trail_id"] not in trail_ids:
            raise ValueError(f"missing source trail id: {row['source_trail_id']}")
        rows.append(
            {
                **row,
                "candidate_status": "public_preview_release_candidate_summary",
                "candidate_state": "current_preview_candidate",
                "boundary": "synthetic only and not for clinical use",
            }
        )

    data: dict[str, Any] = {
        "version": "reviewer_question_maintainer_release_candidate_summary_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/reviewer_question_maintainer_audit_trail_packet_v0_1.json",
        "candidate_summary_row_count": len(rows),
        "audit_trail_rows_represented": trail["audit_trail_row_count"],
        "evidence_rows_represented": trail["evidence_rows_represented"],
        "readiness_rows_represented": trail["readiness_rows_represented"],
        "closeout_rows_represented": trail["closeout_rows_represented"],
        "handoff_rows_represented": trail["handoff_rows_represented"],
        "contributor_digest_rows_represented": trail["contributor_digest_rows_represented"],
        "release_index_surface_rows_represented": trail["release_index_surface_rows_represented"],
        "issue_history_rows_represented": trail["issue_history_rows_represented"],
        "previous_public_issue_number": 60,
        "release_candidate_decision": "public_preview_candidate_only",
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
        "# Reviewer question maintainer release candidate summary v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This release candidate summary gives maintainers a compact public preview candidate view after reviewer question audit trail packet review.",
        "",
        "It is not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Candidate summary rows: {len(rows)}",
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
        "Release candidate decision: `public_preview_candidate_only`",
        "",
        "## Maintainer candidate rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['summary_id']}",
                "",
                f"Summary name: {row['summary_name']}",
                "",
                f"Source trail row: `{row['source_trail_id']}`",
                "",
                f"Candidate surface: `{row['candidate_surface']}`",
                "",
                f"Maintainer decision: {row['maintainer_decision']}",
                "",
                f"Candidate status: `{row['candidate_status']}`",
                "",
                f"Candidate state: `{row['candidate_state']}`",
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
            "make reviewer_question_maintainer_release_candidate_summary",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a reviewer question maintainer public preview decision log without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"candidate_summary_rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
