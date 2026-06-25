#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "clinical_intelligence_stack_global_target_map_20260625.json"
MARKDOWN = ROOT / "docs" / "CLINICAL_INTELLIGENCE_STACK_GLOBAL_TARGET_MAP_20260625.md"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def render_markdown(data: dict) -> str:
    lines = [
        "# Clinical Intelligence Stack Global Target Map",
        "",
        f"Date: {data['date']}",
        "",
        "## Public Hook",
        "",
        data["public_hook"],
        "",
        "## Distribution Rule",
        "",
        data["distribution_rule"],
        "",
        "## Source Anchors",
        "",
    ]
    for source in data["source_anchors"]:
        lines.extend(
            [
                f"### {source['id']} {source['name']}",
                "",
                f"URL: {source['url']}",
                "",
                f"Supported signal: {source['supported_signal']}",
                "",
                f"Target angle: {source['target_angle']}",
                "",
            ]
        )
    lines.extend(["## Audience Routes", ""])
    for route in data["audience_routes"]:
        lines.extend(
            [
                f"### {route['priority']}. {route['audience']}",
                "",
                f"Examples: {', '.join(route['examples'])}",
                "",
                f"Why they care: {route['why_they_care']}",
                "",
                f"Artifact to show: {route['artifact_to_show']}",
                "",
                f"Public line: {route['public_line']}",
                "",
                f"First channel: {route['first_channel']}",
                "",
            ]
        )
    lines.extend(["## Launch Sequence", ""])
    for step in data["launch_sequence"]:
        lines.extend(
            [
                f"### {step['step']}. {step['name']}",
                "",
                f"Goal: {step['goal']}",
                "",
                f"Surface: {step['surface']}",
                "",
                f"Gate: {step['gate']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Blocked Moves",
            "",
            *numbered(data["blocked_moves"]),
            "",
            "## Next Artifacts",
            "",
            *numbered(data["next_artifacts"]),
            "",
            "## Validation Command",
            "",
            "`make clinical_intelligence_stack_global_target_map`",
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
        print("PASS Clinical Intelligence Stack global target map generated file is current")
        print(f"file={MARKDOWN.relative_to(ROOT)}")
        return 0

    MARKDOWN.write_text(expected, encoding="utf-8")
    print(f"Wrote {MARKDOWN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
