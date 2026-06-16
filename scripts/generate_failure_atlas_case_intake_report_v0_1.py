#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl",
    ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl",
]
OUTPUT = ROOT / "failure_atlas" / "public" / "build" / "case_intake_report_v0_1.md"


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in INPUTS:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                row["_source_file"] = str(path.relative_to(ROOT))
                rows.append(row)
    return rows


def main() -> None:
    rows = load_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Failure Atlas case intake report v0.1",
        "",
        "Status: generated public preview.",
        "",
        "This report is generated from the public Failure Atlas intake rows and the TR MedLLM synthetic risk pack.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, and not an institutional endorsement.",
        "",
        "## Summary",
        "",
        f"Rows: {len(rows)}",
        "",
        "## Intake rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['case_id']}",
                "",
                f"Clinical domain: `{row['clinical_domain']}`",
                "",
                f"Setting: `{row['setting']}`",
                "",
                f"Risk axis: `{row['risk_axis']}`",
                "",
                f"Release gate: `{row['release_gate']}`",
                "",
                f"Failure pattern: {row['failure_pattern']}",
                "",
                f"Taxonomy pattern IDs: {', '.join(row['taxonomy_pattern_ids'])}",
                "",
                f"Safe answer expectation: {row['safe_answer_expectation']}",
                "",
                f"Track A relevance: {row['track_a_relevance']}",
                "",
                f"Track B relevance: {row['track_b_relevance']}",
                "",
                f"Source file: `{row['_source_file']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. Every row is synthetic.",
            "2. Patient data is not used.",
            "3. Clinical use is not allowed.",
            "4. Source review and clinician review states remain visible.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
