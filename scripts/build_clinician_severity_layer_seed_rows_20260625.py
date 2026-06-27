#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "clinician_severity_layer_seed_rows_20260625.jsonl"
MARKDOWN = ROOT / "docs" / "CLINICIAN_SEVERITY_LAYER_SEED_ROWS_20260625.md"


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def render(rows: list[dict]) -> str:
    lines = [
        "# Clinician Severity Layer Seed Rows",
        "",
        "Date: 2026 06 25",
        "",
        "Status: seed rows generated from Public Safe Failure Cards.",
        "",
        "## Purpose",
        "",
        "Turn ten public safe failure cards into clinician severity layer rows that can be reviewed, revised, and validated by script without patient data or clinical use claims.",
        "",
        "## Rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['row_id']} from {row['origin_card_id']}",
                "",
                f"Scenario scope: {row['scenario_scope']}",
                "",
                f"User context: {row['user_context']}",
                "",
                f"Failure mode: {row['failure_mode']}",
                "",
                f"Clinical severity: {row['clinical_severity']}",
                "",
                f"Missing variable: {row['missing_variable']}",
                "",
                f"Source support gap: {row['source_support_gap']}",
                "",
                f"Safe rewrite: {row['safe_rewrite']}",
                "",
                f"Reviewer state: {row['reviewer_state']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "These are synthetic review rows. They are not clinical advice, patient data, clinical validation, clinical deployment, benchmark ranking, score certification, source truth certification, institutional approval, partner status, endorsement, acceptance, or merge.",
            "",
            "## Runnable check",
            "",
            "`make clinician_severity_layer_seed_rows`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render(load_rows())
    if args.check:
        if not MARKDOWN.exists():
            print(f"FAIL missing generated file: {MARKDOWN.relative_to(ROOT)}")
            return 1
        if MARKDOWN.read_text(encoding="utf-8") != rendered:
            print(f"FAIL generated file is stale: {MARKDOWN.relative_to(ROOT)}")
            return 1
        print(f"PASS generated file is current: {MARKDOWN.relative_to(ROOT)}")
        return 0

    MARKDOWN.write_text(rendered, encoding="utf-8")
    print(f"Wrote {MARKDOWN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
