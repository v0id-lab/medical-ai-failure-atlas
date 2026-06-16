#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "sourcecheckup" / "review_queue" / "source_claim_review_queue_v0_1.jsonl"

REQUIRED_FIELDS = [
    "queue_id",
    "source_surface",
    "connected_project",
    "synthetic_answer_excerpt",
    "exact_claim_text",
    "claim_centrality",
    "locator_or_source_text",
    "declared_source_status",
    "required_checks",
    "triage_priority",
    "assigned_review_lane",
    "public_action",
    "release_gate",
    "patient_data",
    "external_action_ready",
    "outward_use_allowed",
    "review_state",
]

ALLOWED_SURFACES = {
    "guideline",
    "doi",
    "pmid",
    "url",
    "policy",
    "broad_source_language",
    "evidence",
    "none",
}

REQUIRED_SURFACES = {
    "guideline",
    "doi",
    "pmid",
    "url",
    "policy",
    "broad_source_language",
    "none",
}

ALLOWED_CHECKS = {
    "locator_format",
    "source_exists",
    "metadata_match",
    "exact_claim_support",
    "guideline_scope",
    "policy_jurisdiction",
    "rewrite_without_source_claim",
}

ALLOWED_GATES = {
    "blocked_missing_source_support",
    "blocked_pending_source_verification",
    "pass_local_sourcecheckup",
}

ALLOWED_REVIEW_STATES = {
    "pending_maintainer_review",
    "maintainer_format_checked",
    "maintainer_rejected",
}

FORBIDDEN_PHRASES = [
    "patient name",
    "date of birth",
    "clinically validated",
    "safe for clinical use",
    "officially approved",
    "regulatory approved",
    "verified external truth",
    "source proves",
    "best model",
]


def load_rows(errors: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not QUEUE.exists():
        errors.append(f"Missing queue: {QUEUE}")
        return rows
    for line_number, line in enumerate(QUEUE.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"Line {line_number}: row must be an object")
            continue
        rows.append(row)
    return rows


def main() -> int:
    errors: list[str] = []
    rows = load_rows(errors)
    if len(rows) < 8:
        errors.append("Expected at least 8 queue rows")

    seen_ids: set[str] = set()
    surfaces: set[str] = set()
    checks_seen: set[str] = set()
    gates_seen: set[str] = set()

    for index, row in enumerate(rows, start=1):
        queue_id = str(row.get("queue_id", ""))
        if not queue_id.startswith("SCQ_"):
            errors.append(f"Row {index}: queue_id must start with SCQ_")
        if queue_id in seen_ids:
            errors.append(f"Row {index}: duplicate queue_id {queue_id}")
        seen_ids.add(queue_id)

        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"Row {index}: missing {field}")
            elif isinstance(row[field], str) and not str(row[field]).strip() and field != "locator_or_source_text":
                errors.append(f"Row {index}: empty {field}")

        surface = str(row.get("source_surface", ""))
        surfaces.add(surface)
        if surface not in ALLOWED_SURFACES:
            errors.append(f"Row {index}: invalid source_surface {surface}")

        checks = row.get("required_checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"Row {index}: required_checks must be a non empty list")
            checks = []
        for check in checks:
            check_text = str(check)
            checks_seen.add(check_text)
            if check_text not in ALLOWED_CHECKS:
                errors.append(f"Row {index}: invalid required check {check_text}")

        gate = str(row.get("release_gate", ""))
        gates_seen.add(gate)
        if gate not in ALLOWED_GATES:
            errors.append(f"Row {index}: invalid release_gate {gate}")

        review_state = str(row.get("review_state", ""))
        if review_state not in ALLOWED_REVIEW_STATES:
            errors.append(f"Row {index}: invalid review_state {review_state}")

        if row.get("patient_data") is not False:
            errors.append(f"Row {index}: patient_data must be false")
        if row.get("external_action_ready") is not False:
            errors.append(f"Row {index}: external_action_ready must be false")
        if row.get("outward_use_allowed") is not False:
            errors.append(f"Row {index}: outward_use_allowed must be false")

        if surface in {"doi", "pmid", "url"}:
            if "locator_format" not in checks:
                errors.append(f"Row {index}: locator surface must include locator_format")
            if not str(row.get("locator_or_source_text", "")).strip():
                errors.append(f"Row {index}: locator surface must include locator_or_source_text")
        if surface == "guideline" and "guideline_scope" not in checks:
            errors.append(f"Row {index}: guideline surface must include guideline_scope")
        if surface == "policy" and "policy_jurisdiction" not in checks:
            errors.append(f"Row {index}: policy surface must include policy_jurisdiction")
        if surface != "none" and "exact_claim_support" not in checks:
            errors.append(f"Row {index}: source claim row must include exact_claim_support")
        if surface == "none" and gate != "pass_local_sourcecheckup":
            errors.append(f"Row {index}: none surface should be a positive local pass control")

        row_text = " ".join(str(value).lower() for value in row.values())
        for phrase in FORBIDDEN_PHRASES:
            if phrase in row_text:
                errors.append(f"Row {index}: forbidden phrase {phrase!r}")

    missing_surfaces = sorted(REQUIRED_SURFACES - surfaces)
    if missing_surfaces:
        errors.append(f"Missing required source surfaces: {', '.join(missing_surfaces)}")
    for needed_check in {"source_exists", "metadata_match", "exact_claim_support", "rewrite_without_source_claim"}:
        if needed_check not in checks_seen:
            errors.append(f"Missing required evidence check coverage: {needed_check}")
    for needed_gate in {"blocked_missing_source_support", "blocked_pending_source_verification", "pass_local_sourcecheckup"}:
        if needed_gate not in gates_seen:
            errors.append(f"Missing release gate coverage: {needed_gate}")

    if errors:
        print("FAIL source claim review queue validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS source claim review queue validation")
    print(f"rows={len(rows)}")
    print(f"source_surfaces={len(surfaces)}")
    print(f"input={QUEUE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
