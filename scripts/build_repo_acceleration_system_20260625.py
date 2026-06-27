#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "repo_acceleration_system_20260625.json"

OUTPUTS = {
    "north_star": ROOT / "docs" / "REPO_ACCELERATION_NORTH_STAR_20260625.md",
    "six_month": ROOT / "docs" / "SIX_MONTH_COMPRESSED_BUILD_MAP_20260625.md",
    "queue": ROOT / "docs" / "NEXT_72_HOUR_EXECUTION_QUEUE_20260625.md",
    "severity_spec": ROOT / "docs" / "CLINICIAN_SEVERITY_LAYER_PRODUCT_SPEC_20260625.md",
    "proof_ledger": ROOT / "docs" / "EXTERNAL_PROOF_OF_WORK_LEDGER_20260625.md",
}


def numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def rows(items: list[dict], fields: list[str]) -> list[str]:
    lines: list[str] = []
    for index, item in enumerate(items, 1):
        title = item.get("name") or item.get("layer") or item.get("outcome") or item.get("id") or item.get("route") or f"Item {index}"
        lines.extend([f"### {index}. {title}", ""])
        for field in fields:
            if field in item:
                label = field.replace("_", " ").title()
                lines.extend([f"{label}: {item[field]}", ""])
    return lines


def render_north_star(data: dict) -> str:
    lines = [
        "# Repo Acceleration North Star",
        "",
        f"Date: {data['date']}",
        "",
        f"Status: {data['status']}.",
        "",
        "## North star",
        "",
        data["north_star"],
        "",
        "## Positioning",
        "",
        *numbered(data["positioning"]),
        "",
        "## Product stack",
        "",
        *rows(data["product_stack"], ["job", "current_assets", "next_build", "proof"]),
        "## Strategic bets",
        "",
        *rows(data["strategic_bets"], ["why", "six_month_result", "hours_version"]),
        "## Blocked claims",
        "",
        *numbered(data["blocked_claims"]),
        "",
    ]
    return "\n".join(lines)


def render_six_month(data: dict) -> str:
    lines = [
        "# Six Month Compressed Build Map",
        "",
        f"Date: {data['date']}",
        "",
        "## Six month outcomes",
        "",
        *rows(data["six_month_outcomes"], ["evidence", "risk"]),
        "## Compressed build waves",
        "",
    ]
    for index, wave in enumerate(data["compressed_build_waves"], 1):
        lines.extend(
            [
                f"### {index}. {wave['wave']}",
                "",
                f"Goal: {wave['goal']}",
                "",
                "Outputs:",
                "",
                *numbered(wave["outputs"]),
                "",
            ]
        )
    lines.extend(["## Validator commands", "", *numbered([f"`{command}`" for command in data["validator_commands"]]), ""])
    return "\n".join(lines)


def render_queue(data: dict) -> str:
    lines = [
        "# Next 72 Hour Execution Queue",
        "",
        f"Date: {data['date']}",
        "",
        "## Queue",
        "",
    ]
    for item in data["next_72_hour_queue"]:
        lines.extend(
            [
                f"### {item['id']}. {item['lane']}",
                "",
                f"Action: {item['action']}",
                "",
                f"Deliverable: {item['deliverable']}",
                "",
                f"Gate: {item['gate']}",
                "",
            ]
        )
    return "\n".join(lines)


def render_severity_spec(data: dict) -> str:
    lines = [
        "# Clinician Severity Layer Product Spec",
        "",
        f"Date: {data['date']}",
        "",
        "## Purpose",
        "",
        "Turn each medical AI failure example into a compact clinician review row that can be judged, revised, and shared without patient data or clinical use claims.",
        "",
        "## Required fields",
        "",
    ]
    for index, field in enumerate(data["severity_layer_fields"], 1):
        lines.extend(
            [
                f"### {index}. {field['field']}",
                "",
                field["definition"],
                "",
            ]
        )
    lines.extend(
        [
            "## Review states",
            "",
            "1. Draft",
            "2. Needs clinician review",
            "3. Needs source support",
            "4. Ready for public example",
            "5. Blocked",
            "",
            "## Product rule",
            "",
            "A row is not ready until it names the failure mode, missing variable, source support gap, safe rewrite, and reviewer state.",
            "",
        ]
    )
    return "\n".join(lines)


def render_proof_ledger(data: dict) -> str:
    lines = [
        "# External Proof Of Work Ledger",
        "",
        f"Date: {data['date']}",
        "",
        "## Routes",
        "",
        *rows(data["external_proof_routes"], ["current_meaning", "proof_value", "blocked_read"]),
        "## Proof metrics",
        "",
        *numbered(data["proof_metrics"]),
        "",
        "## Boundary",
        "",
        "This ledger records reviewable public work. It does not record endorsement, validation, deployment, acceptance, merge, partner status, or institutional support.",
        "",
    ]
    return "\n".join(lines)


RENDERERS = {
    "north_star": render_north_star,
    "six_month": render_six_month,
    "queue": render_queue,
    "severity_spec": render_severity_spec,
    "proof_ledger": render_proof_ledger,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rendered = {key: RENDERERS[key](data) for key in OUTPUTS}

    if args.check:
        errors: list[str] = []
        for key, path in OUTPUTS.items():
            if not path.exists():
                errors.append(f"Missing generated file: {path.relative_to(ROOT)}")
                continue
            if path.read_text(encoding="utf-8") != rendered[key]:
                errors.append(f"Generated file is stale: {path.relative_to(ROOT)}")
        if errors:
            for error in errors:
                print(f"FAIL {error}")
            return 1
        print("PASS repo acceleration system generated files are current")
        for path in OUTPUTS.values():
            print(f"file={path.relative_to(ROOT)}")
        return 0

    for key, path in OUTPUTS.items():
        path.write_text(rendered[key], encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
