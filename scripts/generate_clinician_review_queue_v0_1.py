#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl",
    ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl",
]
OUTPUT = ROOT / "failure_atlas" / "public" / "build" / "clinician_review_queue_v0_1.md"

PRIORITY = {
    "needs_clinician_review": 0,
    "needs_source_review": 1,
    "synthetic_preview_only": 2,
    "not_for_public_summary": 3,
}


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in INPUTS:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            row["_source_file"] = str(path.relative_to(ROOT))
            rows.append(row)
    return rows


def main() -> None:
    rows = [row for row in load_rows() if row.get("clinician_review_needed") is True]
    rows.sort(key=lambda row: (PRIORITY.get(str(row["release_gate"]), 9), str(row["case_id"])))

    source_review_rows = [row for row in rows if row.get("sourcecheckup_needed") is True]
    turkish_rows = [row for row in rows if str(row["case_id"]).startswith("TRFAI")]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Clinician review queue v0.1",
        "",
        "Status: generated public preview.",
        "",
        "This queue turns synthetic intake rows into reviewer work items.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, and not an institutional endorsement.",
        "",
        "## Summary",
        "",
        f"Review rows: {len(rows)}",
        "",
        f"Turkish synthetic review rows: {len(turkish_rows)}",
        "",
        f"Rows needing source review: {len(source_review_rows)}",
        "",
        "## Review queue",
        "",
    ]

    for position, row in enumerate(rows, start=1):
        prompt_seed = row.get("turkish_prompt_seed")
        lines.extend(
            [
                f"### Queue item {position}: {row['case_id']}",
                "",
                f"Release gate: `{row['release_gate']}`",
                "",
                f"Risk axis: `{row['risk_axis']}`",
                "",
                f"Taxonomy pattern IDs: {', '.join(row['taxonomy_pattern_ids'])}",
                "",
                f"Clinical domain: `{row['clinical_domain']}`",
                "",
                f"Setting: `{row['setting']}`",
                "",
                f"Synthetic summary: {row['synthetic_case_summary']}",
                "",
                f"Reviewer question: Does the expected safe answer preserve this boundary: {row['safe_answer_expectation']}",
                "",
                f"SourceCheckup needed: `{str(row['sourcecheckup_needed']).lower()}`",
                "",
                f"Source file: `{row['_source_file']}`",
                "",
            ]
        )
        if prompt_seed:
            lines.extend([f"Turkish prompt seed: {prompt_seed}", ""])

    lines.extend(
        [
            "## Boundary checks",
            "",
            "1. The queue is for synthetic reviewer workflow design only.",
            "2. It does not publish patient data or raw model outputs.",
            "3. It does not rank models.",
            "4. It does not state that any model or answer is clinically safe.",
            "5. A clinician review queue is not clinical validation.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"review_rows={len(rows)}")
    print(f"turkish_rows={len(turkish_rows)}")
    print(f"source_review_rows={len(source_review_rows)}")


if __name__ == "__main__":
    main()
