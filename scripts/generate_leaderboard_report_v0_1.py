#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "leaderboard" / "synthetic_report_template_v0_1.tsv"
OUTPUT = ROOT / "leaderboard" / "build" / "synthetic_report_v0_1.md"


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_report(rows: list[dict[str, str]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Synthetic no ranking report v0.1",
        "",
        "Status: generated public preview.",
        "",
        "This report is generated from `leaderboard/synthetic_report_template_v0_1.tsv`.",
        "",
        "It is not clinical advice, not patient data, not a clinical deployment artifact, not a clinical validation table, not a model safety claim, and not a superiority claim.",
        "",
        "## Summary",
        "",
        f"Rows: {len(rows)}",
        "",
        "All rows are synthetic placeholders.",
        "",
        "## Rows",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"### Row {index}: {row['run_id']}",
                "",
                f"Model label: `{row['model_label']}`",
                "",
                f"Scenario set: `{row['scenario_set']}`",
                "",
                f"SourceCheckup gate: `{row['sourcecheckup_gate']}`",
                "",
                f"Failure pattern: `{row['failure_atlas_pattern']}`",
                "",
                f"Clinician review: `{row['clinician_review_state']}`",
                "",
                f"Release gate: `{row['release_gate']}`",
                "",
            ]
        )
    lines.extend(
        [
            "",
            "## Public summaries",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### {row['run_id']}",
                "",
                row["public_summary"],
                "",
            ]
        )
    lines.extend(
        [
            "## Required boundary checks",
            "",
            "1. `synthetic_only` must be `true`.",
            "2. `patient_data_used` must be `false`.",
            "3. `clinical_use_allowed` must be `false`.",
            "4. No model should be described as safe or superior.",
            "5. No row should be used for clinical decisions.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = load_rows()
    write_report(rows)
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
