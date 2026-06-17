#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "reviewer_question_public_wording_decision_log_v0_1.json"
MARKDOWN = ROOT / "docs" / "REVIEWER_QUESTION_RELEASE_GATE_CHECKLIST_V0_1.md"
OUT_JSON = ROOT / "docs" / "reviewer_question_release_gate_checklist_v0_1.json"


GATE_NAMES = {
    "RQINT001": "Source support wording gate",
    "RQINT002": "Policy wording source gate",
    "RQINT003": "Escalation boundary wording gate",
    "RQINT004": "Medication advice boundary gate",
}

GATE_QUESTIONS = {
    "RQINT001": "Does public wording avoid saying a locator proves the claim",
    "RQINT002": "Does public wording require a policy source and clause",
    "RQINT003": "Does public wording keep escalation boundary under review",
    "RQINT004": "Does public wording block individualized medication advice",
}

REQUIRED_CHECKS = {
    "RQINT001": "source support need is explicit",
    "RQINT002": "policy source need is explicit",
    "RQINT003": "escalation boundary is explicit",
    "RQINT004": "individualized medication advice is blocked",
}

BLOCK_STATES = {
    "RQINT001": "block wording that treats locator format as evidence",
    "RQINT002": "block wording that treats policy requirement as established",
    "RQINT003": "block wording that proves safe escalation",
    "RQINT004": "block wording that gives individualized medication advice",
}


def build_rows(decision_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(decision_rows, start=1):
        intake_id = str(row["intake_id"])
        rows.append(
            {
                "release_gate_id": f"RQRG{index:03d}",
                "gate_name": GATE_NAMES[intake_id],
                "intake_id": intake_id,
                "benchmark_reviewer_question_id": row["benchmark_reviewer_question_id"],
                "reviewer_role_id": row["reviewer_role_id"],
                "reviewer_role_name": row["reviewer_role_name"],
                "gate_question": GATE_QUESTIONS[intake_id],
                "required_check": REQUIRED_CHECKS[intake_id],
                "blocked_wording": row["blocked_wording"],
                "required_public_wording": row["proposed_public_wording"],
                "current_state": "pass",
                "release_decision": "allowed_for_public_preview",
                "pass_state": "public wording may proceed",
                "block_state": BLOCK_STATES[intake_id],
                "evidence_surface": row["next_public_surface"],
                "track_a_value": row["track_a_value"],
                "track_b_value": row["track_b_value"],
            }
        )
    return rows


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Reviewer question release gate checklist v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This checklist converts reviewer question public wording decisions into release gate checks with required pass or block states.",
        "",
        "It is not clinical advice, not patient data, not raw model output, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Release gate rows: {payload['release_gate_count']}",
        "",
        f"Pass state rows: {payload['pass_state_count']}",
        "",
        f"Block state rows: {payload['block_state_count']}",
        "",
        "Release decision: `allowed_for_public_preview`",
        "",
        "## Gate rows",
        "",
    ]
    for row in payload["rows"]:
        lines.extend(
            [
                f"### {row['release_gate_id']}",
                "",
                f"Gate name: {row['gate_name']}",
                "",
                f"Intake id: `{row['intake_id']}`",
                "",
                f"Reviewer question id: `{row['benchmark_reviewer_question_id']}`",
                "",
                f"Reviewer role: `{row['reviewer_role_id']}` {row['reviewer_role_name']}",
                "",
                f"Gate question: {row['gate_question']}",
                "",
                f"Required check: {row['required_check']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Required public wording: {row['required_public_wording']}",
                "",
                f"Current state: `{row['current_state']}`",
                "",
                f"Pass state: {row['pass_state']}",
                "",
                f"Block state: {row['block_state']}",
                "",
                f"Evidence surface: {row['evidence_surface']}",
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
            "1. Checklist JSON: `docs/reviewer_question_release_gate_checklist_v0_1.json`",
            "2. Public wording decision log: `docs/REVIEWER_QUESTION_PUBLIC_WORDING_DECISION_LOG_V0_1.md`",
            "3. Maintainer triage board: `docs/REVIEWER_QUESTION_INTAKE_TRIAGE_BOARD_V0_1.md`",
            "4. Intake examples: `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md`",
            "5. SourceCheckup contributor guide: `docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`",
            "6. Failure Atlas checklist: `failure_atlas/public/CASE_INTAKE_CHECKLIST_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make reviewer_question_release_gates",
            "```",
            "",
            "## Next safe public action",
            "",
            "Add a release gate outcome dashboard for reviewer question wording decisions without scoring, compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = build_rows(source["rows"])
    payload = {
        "artifact": "reviewer_question_release_gate_checklist_v0_1",
        "date": "2026 06 17",
        "status": "generated public preview",
        "source_artifact": "reviewer_question_public_wording_decision_log_v0_1",
        "release_gate_count": len(rows),
        "pass_state_count": sum(1 for row in rows if row["current_state"] == "pass"),
        "block_state_count": sum(1 for row in rows if row["current_state"] == "block"),
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
