#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "label_audit" / "label_audit_release_gate_checklist_v0_1.json"
JSON_OUTPUT = ROOT / "docs" / "label_audit" / "label_audit_release_gate_outcome_dashboard_v0_1.json"
MD_OUTPUT = ROOT / "docs" / "label_audit" / "LABEL_AUDIT_RELEASE_GATE_OUTCOME_DASHBOARD_V0_1.md"


def main() -> None:
    checklist = json.loads(CHECKLIST.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(checklist["rows"], start=1):
        current_state = str(item["current_state"])
        release_decision = str(item["release_decision"])
        rows.append(
            {
                "outcome_id": f"LAGO{index:03d}",
                "release_gate_id": item["release_gate_id"],
                "gate_name": item["gate_name"],
                "current_state": current_state,
                "release_decision": release_decision,
                "required_public_wording": item["required_public_wording"],
                "blocked_wording": item["blocked_wording"],
                "evidence_surface": item["evidence_surface"],
                "next_action": "keep public preview wording",
            }
        )

    state_counts = Counter(row["current_state"] for row in rows)
    decision_counts = Counter(row["release_decision"] for row in rows)
    data: dict[str, Any] = {
        "version": "label_audit_release_gate_outcome_dashboard_v0_1",
        "status": "public_preview",
        "date": "2026 06 17",
        "source": "docs/label_audit/label_audit_release_gate_checklist_v0_1.json",
        "outcome_row_count": len(rows),
        "pass_state_count": state_counts.get("pass", 0),
        "block_state_count": state_counts.get("block", 0),
        "release_decision_count": len(decision_counts),
        "contains_patient_data": False,
        "synthetic_examples_only": True,
        "not_for_clinical_use": True,
        "no_raw_model_output_release": True,
        "no_clinical_deployment_claim": True,
        "no_clinical_validation_claim": True,
        "no_model_safety_claim": True,
        "no_model_ranking": True,
        "no_dataset_quality_proof": True,
        "no_official_endorsement_claim": True,
        "rows": rows,
    }
    JSON_OUTPUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Label audit release gate outcome dashboard v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 17",
        "",
        "This dashboard summarizes pass and block outcomes across label audit release gate rows.",
        "",
        "It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Outcome rows: {len(rows)}",
        "",
        f"Pass state rows: {data['pass_state_count']}",
        "",
        f"Block state rows: {data['block_state_count']}",
        "",
        f"Release decision values represented: {data['release_decision_count']}",
        "",
        "Release decision: `allowed_for_public_preview`",
        "",
        "## Outcome rows",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"### {row['outcome_id']}",
                "",
                f"Release gate id: `{row['release_gate_id']}`",
                "",
                f"Gate name: {row['gate_name']}",
                "",
                f"Current state: `{row['current_state']}`",
                "",
                f"Release decision: `{row['release_decision']}`",
                "",
                f"Required public wording: {row['required_public_wording']}",
                "",
                f"Blocked wording: {row['blocked_wording']}",
                "",
                f"Evidence surface: {row['evidence_surface']}",
                "",
                f"Next action: {row['next_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Public files",
            "",
            "1. Outcome dashboard JSON: `docs/label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json`",
            "2. Release gate checklist: `docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md`",
            "3. Public wording decision log: `docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md`",
            "4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`",
            "",
            "## Runnable check",
            "",
            "Run:",
            "",
            "```bash",
            "make label_audit_outcome_dashboard",
            "```",
            "",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={JSON_OUTPUT.relative_to(ROOT)}")
    print(f"generated={MD_OUTPUT.relative_to(ROOT)}")
    print(f"outcome_rows={len(rows)}")


if __name__ == "__main__":
    main()
