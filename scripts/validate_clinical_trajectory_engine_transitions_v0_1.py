#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURES = (
    ROOT
    / "data"
    / "clinical_trajectory_engine_transition_fixtures_v0_1_20260625.jsonl"
)

TOP_REQUIRED = {
    "trajectory_id",
    "version",
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
    "ranking_allowed",
    "domain",
    "arc",
    "purpose",
    "states",
    "transitions",
}

STATE_REQUIRED = {
    "state_id",
    "timepoint",
    "synthetic_only",
    "patient_data_used",
    "clinical_use_allowed",
    "patient_voice",
    "risk_state",
    "missing_variables",
    "red_flags",
    "action_boundary",
    "allowed_actions",
    "blocked_actions",
    "transition_note",
}

TRANSITION_REQUIRED = {
    "from_state",
    "to_state",
    "trigger",
    "missing_variables_added",
    "red_flags_added",
    "boundary_change",
    "action_boundary",
    "allowed_actions",
    "blocked_actions",
}

FORBIDDEN_CLAIMS = [
    "clinical deployment ready",
    "validated for clinical use",
    "safe for patient use",
    "diagnosis provided",
    "treatment recommendation provided",
    "medical advice provided",
    "real patient data",
    "ranking allowed true",
]

BOUNDARY_TERMS = [
    "boundary",
    "do not",
    "only",
]

BLOCKED_ACTION_TERMS = [
    "diagnos",
    "treatment",
    "dose",
    "advice",
    "reassurance",
    "care plan",
    "protocol",
]


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{relative(path)} line {line_number}: {error}") from error
        if not isinstance(item, dict):
            raise ValueError(f"{relative(path)} line {line_number}: expected JSON object")
        rows.append((line_number, item))
    return rows


def require_fields(
    errors: list[str],
    label: str,
    item: dict[str, Any],
    required: set[str],
) -> None:
    missing = sorted(required.difference(item))
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(missing)}")


def has_text_list(item: dict[str, Any], field: str) -> bool:
    value = item.get(field)
    return isinstance(value, list) and all(isinstance(entry, str) and entry.strip() for entry in value)


def validate_boundary(errors: list[str], label: str, text: Any) -> None:
    if not isinstance(text, str) or not text.strip():
        errors.append(f"{label}: action_boundary must be non empty text")
        return
    lowered = text.lower()
    if not any(term in lowered for term in BOUNDARY_TERMS):
        errors.append(f"{label}: action_boundary must name a clear boundary")


def validate_blocked_actions(errors: list[str], label: str, item: dict[str, Any]) -> None:
    if not has_text_list(item, "blocked_actions"):
        errors.append(f"{label}: blocked_actions must be a non empty text list")
        return
    joined = " ".join(item["blocked_actions"]).lower()
    if not any(term in joined for term in BLOCKED_ACTION_TERMS):
        errors.append(f"{label}: blocked_actions should cover diagnosis, treatment, dosing, advice, or reassurance")


def validate_fixture_rows(rows: list[tuple[int, dict[str, Any]]]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    trajectory_ids: set[str] = set()
    domains: Counter[str] = Counter()
    missing_variables: Counter[str] = Counter()
    red_flags: Counter[str] = Counter()
    state_count = 0
    transition_count = 0
    state_boundary_count = 0
    transition_boundary_count = 0

    if not rows:
        errors.append("fixture file contains no rows")

    for line_number, row in rows:
        label = f"line {line_number}"
        require_fields(errors, label, row, TOP_REQUIRED)

        trajectory_id = row.get("trajectory_id")
        row_label = str(trajectory_id or label)
        if not isinstance(trajectory_id, str) or not trajectory_id.startswith("CTEF"):
            errors.append(f"{row_label}: trajectory_id must start with CTEF")
        elif trajectory_id in trajectory_ids:
            errors.append(f"{row_label}: duplicate trajectory_id")
        else:
            trajectory_ids.add(trajectory_id)

        for field, expected in [
            ("synthetic_only", True),
            ("patient_data_used", False),
            ("clinical_use_allowed", False),
            ("ranking_allowed", False),
        ]:
            if row.get(field) is not expected:
                errors.append(f"{row_label}: {field} must be {str(expected).lower()}")

        text_blob = json.dumps(row, ensure_ascii=False).lower()
        for phrase in FORBIDDEN_CLAIMS:
            if phrase in text_blob:
                errors.append(f"{row_label}: forbidden clinical use claim: {phrase}")

        domain = row.get("domain")
        if isinstance(domain, str) and domain.strip():
            domains[domain] += 1
        else:
            errors.append(f"{row_label}: domain must be non empty text")

        states = row.get("states")
        if not isinstance(states, list) or len(states) < 3:
            errors.append(f"{row_label}: expected at least three states")
            states = []

        transitions = row.get("transitions")
        if not isinstance(transitions, list) or not transitions:
            errors.append(f"{row_label}: expected non empty transitions")
            transitions = []

        state_ids: list[str] = []
        state_by_id: dict[str, dict[str, Any]] = {}
        row_has_red_flag = False

        for index, state in enumerate(states):
            state_count += 1
            if not isinstance(state, dict):
                errors.append(f"{row_label}: state {index + 1} must be an object")
                continue
            state_id = state.get("state_id")
            state_label = str(state_id or f"{row_label} state {index + 1}")
            require_fields(errors, state_label, state, STATE_REQUIRED)
            if not isinstance(state_id, str) or not state_id.startswith(f"{trajectory_id}-S"):
                errors.append(f"{state_label}: state_id must use the trajectory prefix")
            elif state_id in state_by_id:
                errors.append(f"{state_label}: duplicate state_id")
            else:
                state_ids.append(state_id)
                state_by_id[state_id] = state

            for field, expected in [
                ("synthetic_only", True),
                ("patient_data_used", False),
                ("clinical_use_allowed", False),
            ]:
                if state.get(field) is not expected:
                    errors.append(f"{state_label}: {field} must be {str(expected).lower()}")

            for field in ["missing_variables", "allowed_actions"]:
                if not has_text_list(state, field):
                    errors.append(f"{state_label}: {field} must be a non empty text list")
            validate_blocked_actions(errors, state_label, state)
            validate_boundary(errors, state_label, state.get("action_boundary"))
            state_boundary_count += 1

            if has_text_list(state, "missing_variables"):
                missing_variables.update(entry.lower() for entry in state["missing_variables"])
            red_flag_list = state.get("red_flags")
            if isinstance(red_flag_list, list):
                for entry in red_flag_list:
                    if isinstance(entry, str) and entry.strip():
                        red_flags[entry.lower()] += 1
                        row_has_red_flag = True
                    else:
                        errors.append(f"{state_label}: red_flags entries must be text")
            else:
                errors.append(f"{state_label}: red_flags must be a list")

            if index > 0 and not red_flag_list:
                errors.append(f"{state_label}: non initial states should name red flags")

        if states and transitions and len(transitions) != len(states) - 1:
            errors.append(f"{row_label}: transitions must connect each adjacent state")
        if not row_has_red_flag:
            errors.append(f"{row_label}: at least one state must contain red flags")

        for index, transition in enumerate(transitions):
            transition_count += 1
            if not isinstance(transition, dict):
                errors.append(f"{row_label}: transition {index + 1} must be an object")
                continue
            transition_label = (
                f"{row_label} transition {transition.get('from_state')} to {transition.get('to_state')}"
            )
            require_fields(errors, transition_label, transition, TRANSITION_REQUIRED)
            validate_blocked_actions(errors, transition_label, transition)
            validate_boundary(errors, transition_label, transition.get("action_boundary"))
            transition_boundary_count += 1

            from_state = transition.get("from_state")
            to_state = transition.get("to_state")
            if from_state not in state_by_id:
                errors.append(f"{transition_label}: from_state not found")
            if to_state not in state_by_id:
                errors.append(f"{transition_label}: to_state not found")
            if from_state in state_by_id and to_state in state_by_id:
                expected_to = state_ids[state_ids.index(from_state) + 1] if state_ids.index(from_state) + 1 < len(state_ids) else None
                if to_state != expected_to:
                    errors.append(f"{transition_label}: transition must move to the next listed state")

            for field in ["missing_variables_added", "red_flags_added", "allowed_actions"]:
                if not has_text_list(transition, field):
                    errors.append(f"{transition_label}: {field} must be a non empty text list")

            if isinstance(to_state, str) and to_state in state_by_id:
                to_missing = {
                    entry.lower()
                    for entry in state_by_id[to_state].get("missing_variables", [])
                    if isinstance(entry, str)
                }
                for entry in transition.get("missing_variables_added", []):
                    if isinstance(entry, str) and entry.lower() not in to_missing:
                        errors.append(f"{transition_label}: missing variable not present in target state: {entry}")

                to_red_flags = {
                    entry.lower()
                    for entry in state_by_id[to_state].get("red_flags", [])
                    if isinstance(entry, str)
                }
                for entry in transition.get("red_flags_added", []):
                    if isinstance(entry, str) and entry.lower() not in to_red_flags:
                        errors.append(f"{transition_label}: red flag not present in target state: {entry}")

            boundary_change = transition.get("boundary_change")
            if not isinstance(boundary_change, str) or " to " not in boundary_change.lower():
                errors.append(f"{transition_label}: boundary_change must describe a before and after boundary")

    summary = {
        "rows": len(rows),
        "states": state_count,
        "transitions": transition_count,
        "domains": domains,
        "missing_variables": missing_variables,
        "red_flags": red_flags,
        "state_boundaries": state_boundary_count,
        "transition_boundaries": transition_boundary_count,
    }
    return errors, summary


def print_summary(path: Path, summary: dict[str, Any]) -> None:
    domains: Counter[str] = summary["domains"]
    missing_variables: Counter[str] = summary["missing_variables"]
    red_flags: Counter[str] = summary["red_flags"]
    print("PASS Clinical Trajectory Engine transition fixture validation")
    print(f"fixtures={relative(path)}")
    print(f"rows={summary['rows']}")
    print(f"states={summary['states']}")
    print(f"transitions={summary['transitions']}")
    print(f"domains={', '.join(sorted(domains))}")
    print(f"missing_variable_mentions={sum(missing_variables.values())}")
    print(f"unique_missing_variables={len(missing_variables)}")
    print(f"red_flag_mentions={sum(red_flags.values())}")
    print(f"unique_red_flags={len(red_flags)}")
    print(f"state_action_boundaries={summary['state_boundaries']}")
    print(f"transition_action_boundaries={summary['transition_boundaries']}")
    print("top_missing_variables=" + ", ".join(name for name, _ in missing_variables.most_common(5)))
    print("top_red_flags=" + ", ".join(name for name, _ in red_flags.most_common(5)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and summarize synthetic Clinical Trajectory Engine transition fixtures."
    )
    parser.add_argument(
        "fixtures",
        nargs="?",
        default=DEFAULT_FIXTURES,
        type=Path,
        help="Path to the trajectory fixture JSONL file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = args.fixtures if args.fixtures.is_absolute() else ROOT / args.fixtures
    if not path.exists():
        print(f"FAIL Clinical Trajectory Engine transition fixture validation")
        print(f"- Missing fixture file: {relative(path)}")
        return 1

    try:
        rows = load_jsonl(path)
    except Exception as error:  # noqa: BLE001
        print("FAIL Clinical Trajectory Engine transition fixture validation")
        print(f"- {error}")
        return 1

    errors, summary = validate_fixture_rows(rows)
    if errors:
        print("FAIL Clinical Trajectory Engine transition fixture validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print_summary(path, summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
