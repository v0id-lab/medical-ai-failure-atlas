#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "clinician_severity_layer_seed_rows_20260625.jsonl"
MARKDOWN = ROOT / "docs" / "CLINICIAN_SEVERITY_LAYER_SEED_ROWS_20260625.md"
BUILDER = ROOT / "scripts" / "build_clinician_severity_layer_seed_rows_20260625.py"

REQUIRED_FIELDS = {
    "row_id",
    "origin_card_id",
    "scenario_scope",
    "user_context",
    "failure_mode",
    "clinical_severity",
    "missing_variable",
    "source_support_gap",
    "safe_rewrite",
    "reviewer_state",
}

REQUIRED_PHRASES = [
    "Clinician Severity Layer Seed Rows",
    "Public Safe Failure Cards",
    "clinician severity layer rows",
    "Missing variable",
    "Source support gap",
    "Safe rewrite",
    "make clinician_severity_layer_seed_rows",
]

FORBIDDEN_PHRASES = [
    "real patient",
    "patient data used",
    "clinical advice provided",
    "clinical validation complete",
    "clinical deployment ready",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "institutional approval granted",
    "partner confirmed",
    "endorsement confirmed",
    "accepted contribution",
    "merged contribution",
]


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(DATA.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"Line {line_number} is not valid JSON: {error}") from error
    return rows


def main() -> int:
    errors: list[str] = []

    if not DATA.exists():
        errors.append(f"Missing data file: {DATA.relative_to(ROOT)}")
        rows: list[dict] = []
    else:
        try:
            rows = load_rows()
        except ValueError as error:
            errors.append(str(error))
            rows = []

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    if len(rows) != 10:
        errors.append("Expected ten severity seed rows")

    expected_row_ids = {f"SLR{index:03d}" for index in range(1, 11)}
    expected_card_ids = {f"SFC{index:03d}" for index in range(1, 11)}
    if {row.get("row_id") for row in rows} != expected_row_ids:
        errors.append("Severity row ids do not match SLR001 to SLR010")
    if {row.get("origin_card_id") for row in rows} != expected_card_ids:
        errors.append("Origin card ids do not match SFC001 to SFC010")

    for row in rows:
        missing = REQUIRED_FIELDS - set(row)
        if missing:
            errors.append(f"{row.get('row_id', 'unknown')}: missing fields {sorted(missing)}")
        if row.get("reviewer_state") != "draft":
            errors.append(f"{row.get('row_id', 'unknown')}: reviewer_state must be draft")
        for field in REQUIRED_FIELDS:
            if not str(row.get(field, "")).strip():
                errors.append(f"{row.get('row_id', 'unknown')}: empty field {field}")

    text = MARKDOWN.read_text(encoding="utf-8") if MARKDOWN.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Markdown missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase in markdown: {phrase}")
    if "-" in text:
        errors.append("Markdown contains a hyphen character")

    if errors:
        print("FAIL clinician severity layer seed rows validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS clinician severity layer seed rows validation")
    print(f"data={DATA.relative_to(ROOT)}")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
