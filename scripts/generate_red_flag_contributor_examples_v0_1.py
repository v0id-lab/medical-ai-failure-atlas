#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTIONS = ROOT / "sourcecheckup" / "examples" / "sourcecheckup_contribution_examples_v0_2.jsonl"
CHECKLIST = ROOT / "docs" / "red_flag_warning_checklist_v0_1.json"
OUTPUT = ROOT / "docs" / "sourcecheckup" / "RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md"
RED_FLAG_IDS = {"SCV2_009", "SCV2_010", "SCV2_011"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def joined(values: list[str]) -> str:
    return ", ".join(values)


def main() -> None:
    rows = load_jsonl(CONTRIBUTIONS)
    red_flag_rows = [row for row in rows if str(row["contribution_id"]) in RED_FLAG_IDS]
    checklist = json.loads(CHECKLIST.read_text(encoding="utf-8"))
    surfaces = Counter(str(row["source_surface"]) for row in red_flag_rows)
    checks = Counter(
        str(check)
        for row in red_flag_rows
        for check in row["required_evidence_checks"]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Red flag source locator contributor examples v0.1",
        "",
        "Status: generated public preview.",
        "",
        "Date: 2026 06 16",
        "",
        "These examples turn the red flag warning checklist into concrete SourceCheckup contributor rows.",
        "",
        "They use synthetic examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.",
        "",
        "## Summary",
        "",
        f"Red flag contributor examples: {len(red_flag_rows)}",
        "",
        f"Total SourceCheckup contributor examples: {len(rows)}",
        "",
        f"Linked red flag checklists: {checklist['checklist_count']}",
        "",
        "Linked route: `STM003`",
        "",
        "Linked SourceCheckup row: `SCQ_003`",
        "",
        "Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`",
        "",
        "Linked assurance example: `ARG001`",
        "",
        "Linked public checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`",
        "",
        "## Source surface coverage",
        "",
    ]
    for surface, count in sorted(surfaces.items()):
        lines.extend([f"{surface}: {count}", ""])

    lines.extend(["## Required evidence check coverage", ""])
    for check, count in sorted(checks.items()):
        lines.extend([f"{check}: {count}", ""])

    lines.extend(["## Contributor examples", ""])
    for row in red_flag_rows:
        sources = row.get("declared_sources", [])
        source_summary = "none"
        if sources:
            source_summary = joined(
                [f"{source.get('type')} {source.get('value')}" for source in sources]
            )
        lines.extend(
            [
                f"### {row['contribution_id']}: {row['source_surface']}",
                "",
                f"Synthetic answer excerpt: {row['synthetic_answer_excerpt']}",
                "",
                f"Exact claim to review: {row['exact_claim_text']}",
                "",
                f"Declared sources: {source_summary}",
                "",
                f"Required evidence checks: {joined(row['required_evidence_checks'])}",
                "",
                f"Proposed public action: {row['proposed_public_action']}",
                "",
                f"Maintainer review status: {row['maintainer_review_status']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Review use",
            "",
            "1. Use these examples to test whether a contributor row separates locator format from source support.",
            "2. Use these examples to test whether warning signs remain visible before comfort language.",
            "3. Use these examples to test whether symptom fluctuation is blocked as a shortcut to reassurance.",
            "4. Use these examples to route unresolved red flag wording to clinician review.",
            "",
            "## Boundary checks",
            "",
            "1. Every example is synthetic.",
            "2. Patient data is not used.",
            "3. External action readiness is false for every row.",
            "4. Outward use is not allowed until maintainer review and exact source support checks are complete.",
            "5. SourceCheckup rows do not certify a source, guideline, policy, benchmark, or medical claim.",
            "",
            "## Public files",
            "",
            "1. Source examples: `sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl`",
            "2. Generated red flag contributor examples: `docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md`",
            "3. Validator: `scripts/validate_red_flag_contributor_examples_v0_1.py`",
            "4. Runnable target: `make red_flag_contributor_examples`",
            "5. Red flag checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`",
            "",
        ]
    )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated={OUTPUT.relative_to(ROOT)}")
    print(f"red_flag_examples={len(red_flag_rows)}")
    print(f"total_contributor_examples={len(rows)}")
    print(f"source_surfaces={len(surfaces)}")
    print(f"evidence_checks={len(checks)}")


if __name__ == "__main__":
    main()
