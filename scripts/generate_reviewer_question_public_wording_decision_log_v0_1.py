#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_intake_triage_board_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md"
OUT_JSON = ROOT / "docs" / "reviewer_question_public_wording_decision_log_v0_1.json"


BLOCKED_WORDING = {
    "RQINT001": "the locator proves the claim",
    "RQINT002": "the policy requirement is established",
    "RQINT003": "the answer proves safe escalation",
    "RQINT004": "the answer gives safe individualized medication advice",
}

PROPOSED_WORDING = {
    "RQINT001": "locator format still needs source support",
    "RQINT002": "policy source and clause are required",
    "RQINT003": "escalation boundary remains under review",
    "RQINT004": "individualized medication advice is blocked",
}


def build_rows(triage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in triage_rows:
        intake_id = str(row["intake_id"])
        rows.append(
            {
                "intake_id": intake_id,
                "template": row["template"],
                "benchmark_reviewer_question_id": row["benchmark_reviewer_question_id"],
                "reviewer_role_id": row["owner_role_id"],
                "reviewer_role_name": row["owner_role_name"],
                "blocked_public_claim_type": row["blocked_public_claim_type"],
                "blocked_wording": BLOCKED_WORDING[intake_id],
                "proposed_public_wording": PROPOSED_WORDING[intake_id],
                "decision_status": "safe_public_wording_ready",
                "maintainer_action": row["maintainer_action"],
                "next_public_surface": row["next_public_surface"],
                "track_a_value": row["track_a_value"],
                "track_b_value": row["track_b_value"],
            }
        )
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    rows = payload["rows"]
    lines = [
        "# Reviewer question public wording decision log v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This log records blocked wording, proposed public wording, reviewer role, decision status, maintainer action, and next public surface for each synthetic reviewer question triage row.",
        "",
        "It is not clinical advice, not patient data, not raw model output, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Public wording decision rows: {payload['decision_row_count']}",
        "",
        f"Blocked wording examples: {payload['blocked_wording_count']}",
        "",
        f"Proposed public wording examples: {payload['proposed_public_wording_count']}",
        "",
        f"Decision status values represented: {payload['decision_status_count']}",
        "",
        "Decision status: `safe_public_wording_ready`",
        "",
        "## Decision rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['intake_id']}",
                "",
                f"Reviewer question id: `{row['benchmark_reviewer_question_id']}`",
                "",
                f"Reviewer role: `{row['reviewer_role_id']}` {row['reviewer_role_name']}",
                "",
                f"Blocked public claim type: {row['blocked_public_claim_type']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Proposed public wording: {row['proposed_public_wording']}",
                "",
                f"Decision status: `{row['decision_status']}`",
                "",
                f"Maintainer action: {row['maintainer_action']}",
                "",
                f"Next public surface: {row['next_public_surface']}",
                "",
                f"Track A value: {row['track_a_value']}",
                "",
                f"Track B value: {row['track_b_value']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Public files",
            "",
            "1. Decision log JSON: `docs/reviewer_question_public_wording_decision_log_v0_1.json`",
            "2. Maintainer triage board: `docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md`",
            "3. Intake examples: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`",
            "4. SourceCheckup contributor guide: `docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`",
            "5. Failure Atlas checklist: `failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make reviewer_question_wording_log",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a release gate checklist for reviewer question public wording decisions without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = build_rows(source["rows"])
    payload = {
        "artifact": "reviewer_question_public_wording_decision_log_v0_1",
        "date": "2026 06 17",
        "status": "generated public preview",
        "source_artifact": "reviewer_question_intake_triage_board_v0_1",
        "decision_row_count": len(rows),
        "blocked_wording_count": len({row["blocked_wording"] for row in rows}),
        "proposed_public_wording_count": len({row["proposed_public_wording"] for row in rows}),
        "decision_status_count": len({row["decision_status"] for row in rows}),
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
    MARKDOWN.write_text(render_markdown(payload), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MARKDOWN.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
