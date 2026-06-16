#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTIONS = ROOT / "sourcecheckup" / "examples" / "sourcecheckup_contribution_examples_v0_2.jsonl"
OUTPUT = ROOT / "docs" / "sourcecheckup" / "RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md"
RED_FLAG_IDS = {"SCV2_009", "SCV2_010", "SCV2_011"}
REQUIRED_SURFACES = {"pmid", "broad_source_language", "guideline"}
REQUIRED_CHECKS = {
    "locator_format",
    "source_exists",
    "metadata_match",
    "exact_claim_support",
    "guideline_scope",
    "rewrite_without_source_claim",
}

REQUIRED_PHRASES = [
    "Red flag source locator contributor examples v0.1",
    "Status: generated public preview.",
    "Red flag contributor examples: 3",
    "Total SourceCheckup contributor examples: 11",
    "Linked red flag checklists: 3",
    "Linked route: `STM003`",
    "Linked SourceCheckup row: `SCQ_003`",
    "Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`",
    "Linked assurance example: `ARG001`",
    "docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md",
    "SCV2_009",
    "SCV2_010",
    "SCV2_011",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a model safety claim",
    "not a model ranking",
    "not source truth certification",
    "not regulatory approval",
    "not an official endorsement",
    "locator format from source support",
    "warning signs remain visible",
    "symptom fluctuation is blocked",
    "make red_flag_contributor_examples",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "deployment ready",
    "officially endorsed",
    "regulatory approved",
    "sandbox access granted",
    "patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path.relative_to(ROOT)}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def main() -> int:
    errors: list[str] = []
    rows = load_jsonl(CONTRIBUTIONS)
    red_flag_rows = [row for row in rows if str(row.get("contribution_id")) in RED_FLAG_IDS]
    if len(rows) != 11:
        errors.append(f"Expected 11 SourceCheckup contributor examples, found {len(rows)}")
    if len(red_flag_rows) != 3:
        errors.append(f"Expected 3 red flag contributor examples, found {len(red_flag_rows)}")

    found_ids = {str(row.get("contribution_id")) for row in red_flag_rows}
    missing_ids = sorted(RED_FLAG_IDS - found_ids)
    if missing_ids:
        errors.append(f"Missing red flag contribution IDs: {', '.join(missing_ids)}")
    surfaces = {str(row.get("source_surface")) for row in red_flag_rows}
    missing_surfaces = sorted(REQUIRED_SURFACES - surfaces)
    if missing_surfaces:
        errors.append(f"Missing source surfaces: {', '.join(missing_surfaces)}")
    checks = {str(check) for row in red_flag_rows for check in row.get("required_evidence_checks", [])}
    missing_checks = sorted(REQUIRED_CHECKS - checks)
    if missing_checks:
        errors.append(f"Missing evidence checks: {', '.join(missing_checks)}")
    for row in red_flag_rows:
        row_id = str(row.get("contribution_id"))
        if row.get("contains_patient_data") is not False:
            errors.append(f"{row_id}: contains_patient_data must be false")
        if row.get("external_actions_executed") is not False:
            errors.append(f"{row_id}: external_actions_executed must be false")
        if row.get("outward_use_allowed") is not False:
            errors.append(f"{row_id}: outward_use_allowed must be false")
        if row.get("maintainer_review_status") != "pending_maintainer_review":
            errors.append(f"{row_id}: maintainer review must be pending")

    if not OUTPUT.exists():
        errors.append(f"Missing generated examples: {OUTPUT.relative_to(ROOT)}")
        text = ""
    else:
        text = OUTPUT.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Generated file missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Forbidden phrase present: {phrase}")
    if "-" in text:
        errors.append("Generated outward facing examples must not contain hyphen characters")

    if errors:
        print("FAIL red flag contributor examples validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS red flag contributor examples validation")
    print(f"examples={OUTPUT.relative_to(ROOT)}")
    print(f"red_flag_examples={len(red_flag_rows)}")
    print(f"total_contributor_examples={len(rows)}")
    print(f"source_surfaces={len(surfaces)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
