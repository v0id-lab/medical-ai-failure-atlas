#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "failure_atlas" / "public" / "taxonomy_map_v0_1.json"
INPUTS = [
    ROOT / "failure_atlas" / "public" / "case_intake_examples_v0_1.jsonl",
    ROOT / "tr_medllm_safetybench" / "synthetic_risk_pack_v0_1.jsonl",
]
OUTPUT = ROOT / "failure_atlas" / "public" / "build" / "taxonomy_dashboard_v0_1.md"


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            row["_source_file"] = str(path.relative_to(ROOT))
            rows.append(row)
    return rows


def main() -> None:
    taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    pattern_lookup = {item["id"]: item for item in taxonomy["patterns"]}
    rows: list[dict[str, object]] = []
    for path in INPUTS:
        rows.extend(load_jsonl(path))

    pattern_to_rows: dict[str, list[str]] = defaultdict(list)
    risk_counts: Counter[str] = Counter()
    gate_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    tr_rows: list[dict[str, object]] = []

    for row in rows:
        case_id = str(row["case_id"])
        risk_counts[str(row["risk_axis"])] += 1
        gate_counts[str(row["release_gate"])] += 1
        source_counts[str(row["_source_file"])] += 1
        if case_id.startswith("TRFAI"):
            tr_rows.append(row)
        for pattern_id in row["taxonomy_pattern_ids"]:
            pattern_to_rows[str(pattern_id)].append(case_id)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Failure Atlas taxonomy dashboard v0.1",
        "",
        "Status: generated public preview.",
        "",
        "This dashboard connects public synthetic case intake rows to taxonomy pattern IDs.",
        "",
        "It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, and not an institutional endorsement.",
        "",
        "## Summary",
        "",
        f"Total intake rows: {len(rows)}",
        "",
        f"Turkish synthetic risk rows: {len(tr_rows)}",
        "",
        f"Taxonomy patterns represented: {len(pattern_to_rows)}",
        "",
        "## Taxonomy pattern coverage",
        "",
    ]

    for pattern_id in sorted(pattern_lookup):
        item = pattern_lookup[pattern_id]
        mapped_rows = pattern_to_rows.get(pattern_id, [])
        row_text = ", ".join(mapped_rows) if mapped_rows else "No mapped row yet"
        lines.extend(
            [
                f"### {pattern_id}",
                "",
                f"Pattern: {item['name']}",
                "",
                f"Review question: {item['review_question']}",
                "",
                f"Mapped rows: {row_text}",
                "",
            ]
        )

    lines.extend(["## Risk axis coverage", ""])
    for risk_axis, count in sorted(risk_counts.items()):
        lines.extend([f"{risk_axis}: {count}", ""])

    lines.extend(["## Release gate coverage", ""])
    for gate, count in sorted(gate_counts.items()):
        lines.extend([f"{gate}: {count}", ""])

    lines.extend(["## Source files", ""])
    for source_file, count in sorted(source_counts.items()):
        lines.extend([f"`{source_file}`: {count}", ""])

    lines.extend(["## Turkish synthetic risk pack rows", ""])
    for row in tr_rows:
        lines.extend(
            [
                f"### {row['case_id']}",
                "",
                f"Risk axis: `{row['risk_axis']}`",
                "",
                f"Taxonomy pattern IDs: {', '.join(row['taxonomy_pattern_ids'])}",
                "",
                f"Release gate: `{row['release_gate']}`",
                "",
                f"Prompt seed: {row['turkish_prompt_seed']}",
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
            "4. Taxonomy IDs are review routing labels, not diagnosis or validation labels.",
            "5. Turkish rows are language risk seeds, not clinical advice.",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"taxonomy_patterns={len(pattern_to_rows)}")


if __name__ == "__main__":
    main()
