#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "leaderboard" / "synthetic_report_template_v0_1.tsv"

REQUIRED_COLUMNS = [
    "run_id",
    "model_label",
    "scenario_set",
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
    "sourcecheckup_gate",
    "failure_atlas_pattern",
    "clinician_review_state",
    "release_gate",
    "public_summary",
]

ALLOWED_BOOL = {"true", "false"}
ALLOWED_SOURCECHECKUP_GATES = {
    "local_pass",
    "needs_source_review",
    "needs_clinician_review",
}
ALLOWED_REVIEW_STATES = {
    "needs_source_review",
    "needs_clinician_review",
    "reviewed_synthetic_only",
}
ALLOWED_RELEASE_GATES = {
    "synthetic_preview_only",
    "needs_source_review",
    "needs_clinician_review",
    "not_for_public_summary",
}

FORBIDDEN_PHRASES = [
    "clinically validated",
    "safe for clinical use",
    "approved for clinical use",
    "regulatory approved",
    "best model",
    "model ranking",
    "patient data used",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not TEMPLATE.exists():
        fail(errors, f"Missing template: {TEMPLATE}")
    else:
        with TEMPLATE.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames != REQUIRED_COLUMNS:
                fail(errors, f"Unexpected columns: {reader.fieldnames}")
                rows = []
            else:
                rows = list(reader)

        if len(rows) < 4:
            fail(errors, "Expected at least 4 synthetic preview rows")

        seen_ids: set[str] = set()
        for line_number, row in enumerate(rows, start=2):
            run_id = row.get("run_id", "")
            if not run_id:
                fail(errors, f"Line {line_number}: missing run_id")
            if run_id in seen_ids:
                fail(errors, f"Line {line_number}: duplicate run_id {run_id}")
            seen_ids.add(run_id)

            if row.get("synthetic_only") != "true":
                fail(errors, f"Line {line_number}: synthetic_only must be true")
            if row.get("patient_data_used") != "false":
                fail(errors, f"Line {line_number}: patient_data_used must be false")
            if row.get("clinical_use_allowed") != "false":
                fail(errors, f"Line {line_number}: clinical_use_allowed must be false")
            if row.get("sourcecheckup_gate") not in ALLOWED_SOURCECHECKUP_GATES:
                fail(errors, f"Line {line_number}: invalid sourcecheckup_gate")
            if row.get("clinician_review_state") not in ALLOWED_REVIEW_STATES:
                fail(errors, f"Line {line_number}: invalid clinician_review_state")
            if row.get("release_gate") not in ALLOWED_RELEASE_GATES:
                fail(errors, f"Line {line_number}: invalid release_gate")

            row_text = " ".join(str(value).lower() for value in row.values())
            for phrase in FORBIDDEN_PHRASES:
                if phrase in row_text:
                    fail(errors, f"Line {line_number}: forbidden phrase {phrase!r}")

    if errors:
        print("FAIL leaderboard template validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS leaderboard template validation")
    print(f"rows={len(rows)}")
    print(f"template={TEMPLATE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
