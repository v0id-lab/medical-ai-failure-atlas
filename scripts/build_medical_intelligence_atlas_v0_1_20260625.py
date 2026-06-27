#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "medical_intelligence_atlas_v0_1_20260625.json"
MARKDOWN = ROOT / "docs" / "MEDICAL_INTELLIGENCE_ATLAS_V0_1_20260625.md"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(data: dict) -> str:
    lines = [
        "# Medical Intelligence Atlas v0.1",
        "",
        f"Date: {data['date']}",
        "",
        f"Status: {data['status']}",
        "",
        "## Purpose",
        "",
        data["purpose"],
        "",
        "## Global Boundaries",
        "",
        *numbered(data["global_boundaries"]),
        "",
        "## Build Nodes",
        "",
    ]
    for node in data["nodes"]:
        lines.extend(
            [
                f"### {node['id']} {node['layer']}",
                "",
                f"Artifact: {node['artifact']}",
                "",
                f"Input: {node['input']}",
                "",
                f"Output: {node['output']}",
                "",
                f"Validator: {node['validator']}",
                "",
                f"Risk gate: {node['risk_gate']}",
                "",
                f"Next build: {node['next_build']}",
                "",
            ]
        )
    lines.extend(["## Relationships", ""])
    for relation in data["relationships"]:
        lines.extend(
            [
                f"### {relation['from']} to {relation['to']}",
                "",
                relation["contract"],
                "",
            ]
        )
    lines.extend(["## Release States", ""])
    for state in data["release_states"]:
        lines.extend(
            [
                f"### {state['state']}",
                "",
                state["meaning"],
                "",
            ]
        )
    lines.extend(
        [
            "## Validation Command",
            "",
            "`make medical_intelligence_atlas`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = load_config()
    expected = render_markdown(data)

    if args.check:
        if not MARKDOWN.exists():
            print(f"FAIL missing generated file: {MARKDOWN.relative_to(ROOT)}")
            return 1
        if MARKDOWN.read_text(encoding="utf-8") != expected:
            print(f"FAIL generated file is stale: {MARKDOWN.relative_to(ROOT)}")
            return 1
        print("PASS Medical Intelligence Atlas generated file is current")
        print(f"file={MARKDOWN.relative_to(ROOT)}")
        return 0

    MARKDOWN.write_text(expected, encoding="utf-8")
    print(f"Wrote {MARKDOWN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
