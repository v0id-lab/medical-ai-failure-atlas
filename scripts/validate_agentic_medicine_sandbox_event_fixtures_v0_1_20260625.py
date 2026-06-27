#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURES = ROOT / "data" / "agentic_medicine_sandbox_event_fixtures_v0_1_20260625.jsonl"

REQUIRED_AGENTS = [
    "patient_simulator",
    "clinician_reasoner",
    "test_result_emitter",
    "source_support_checker",
    "consultant_simulator",
    "follow_up_monitor",
]

AGENT_EVENT_TYPES = {
    "patient_simulator": "synthetic_patient_state",
    "clinician_reasoner": "clinical_state_update",
    "test_result_emitter": "synthetic_test_event",
    "source_support_checker": "source_support_check",
    "consultant_simulator": "consultant_constraint",
    "follow_up_monitor": "follow_up_check",
}

AGENT_PAYLOAD_KEYS = {
    "patient_simulator": {"patient_voice", "state_delta", "missing_data", "requested_handoff"},
    "clinician_reasoner": {"working_state", "uncertainties", "requested_tests_or_context", "action_boundary"},
    "test_result_emitter": {"synthetic_result", "changed_variable", "interpretation_boundary", "test_event_status"},
    "source_support_checker": {"claim_to_check", "support_status", "needed_source_type", "release_gate", "source_assertion_made"},
    "consultant_simulator": {"consultant_role", "constraint_added", "handoff_note", "no_patient_specific_advice"},
    "follow_up_monitor": {"follow_up_trigger", "state_update_required", "close_loop_status", "next_safe_output_boundary"},
}

REQUIRED_EVENT_KEYS = {
    "event_id",
    "scenario_id",
    "turn_index",
    "agent",
    "event_type",
    "summary",
    "payload",
    "expected_next_agent",
    "safety",
}

REQUIRED_SAFETY_FLAGS = {
    "synthetic_only": True,
    "patient_data_used": False,
    "clinical_use_allowed": False,
    "contains_patient_identifier": False,
    "diagnosis_or_treatment_given": False,
    "patient_facing_instruction_given": False,
}

ALLOWED_SOURCE_SUPPORT_STATUS = {"needs_source", "blocked_until_sourced", "not_checked"}

FORBIDDEN_PHRASES = [
    "clinical validation complete",
    "clinical deployment ready",
    "safe for clinical use",
    "patient data used true",
    "model superiority proven",
    "regulatory clearance secured",
    "institutional approval granted",
    "partner confirmed",
    "endorsement confirmed",
    "real patient",
    "diagnosis provided",
    "treatment recommendation provided",
    "source verified",
    "guideline confirmed",
]

IDENTIFIER_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone": re.compile(r"\b(?:\+?\d[\d .()]{7,}\d)\b"),
    "medical_record_number": re.compile(r"\b(?:mrn|medical record number|record number)\b", re.IGNORECASE),
    "birthdate": re.compile(r"\b(?:date of birth|birthdate|dob)\b", re.IGNORECASE),
    "address": re.compile(r"\b(?:home address|street address|apartment number)\b", re.IGNORECASE),
}


def path_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_events(path: Path = DEFAULT_FIXTURES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path_label(path)} line {line_number}: invalid JSON: {error}") from error
        if not isinstance(row, dict):
            raise ValueError(f"{path_label(path)} line {line_number}: expected JSON object")
        rows.append(row)
    return rows


def group_events(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[str(event.get("scenario_id", ""))].append(event)
    return {
        scenario_id: sorted(rows, key=lambda item: item.get("turn_index", 0))
        for scenario_id, rows in grouped.items()
    }


def flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    if value is None:
        return ""
    return str(value)


def non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(non_empty(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None


def validate_event_shape(event: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    prefix = str(event.get("event_id") or f"row {index}")

    missing_keys = REQUIRED_EVENT_KEYS - set(event)
    if missing_keys:
        errors.append(f"{prefix}: missing event keys {sorted(missing_keys)}")
        return errors

    agent = event.get("agent")
    if agent not in REQUIRED_AGENTS:
        errors.append(f"{prefix}: unknown agent {agent!r}")
        return errors

    expected_type = AGENT_EVENT_TYPES[agent]
    if event.get("event_type") != expected_type:
        errors.append(f"{prefix}: expected event_type {expected_type!r}")

    if not isinstance(event.get("turn_index"), int) or event["turn_index"] < 1:
        errors.append(f"{prefix}: turn_index must be a positive integer")

    for string_key in ["event_id", "scenario_id", "summary"]:
        if not isinstance(event.get(string_key), str) or not event[string_key].strip():
            errors.append(f"{prefix}: {string_key} must be a non empty string")

    payload = event.get("payload")
    if not isinstance(payload, dict):
        errors.append(f"{prefix}: payload must be an object")
    else:
        missing_payload = AGENT_PAYLOAD_KEYS[agent] - set(payload)
        if missing_payload:
            errors.append(f"{prefix}: missing payload keys {sorted(missing_payload)}")
        for key in AGENT_PAYLOAD_KEYS[agent]:
            if key in payload and not non_empty(payload[key]):
                errors.append(f"{prefix}: payload.{key} cannot be empty")

    safety = event.get("safety")
    if not isinstance(safety, dict):
        errors.append(f"{prefix}: safety must be an object")
    else:
        for key, expected in REQUIRED_SAFETY_FLAGS.items():
            if safety.get(key) is not expected:
                errors.append(f"{prefix}: safety.{key} must be {expected!r}")

    if agent == "source_support_checker" and isinstance(payload, dict):
        if payload.get("support_status") not in ALLOWED_SOURCE_SUPPORT_STATUS:
            errors.append(f"{prefix}: source support status must remain unresolved")
        if payload.get("source_assertion_made") is not False:
            errors.append(f"{prefix}: source_assertion_made must be false")
        if payload.get("release_gate") != "blocked_until_sourced":
            errors.append(f"{prefix}: release_gate must be blocked_until_sourced")

    if agent == "consultant_simulator" and isinstance(payload, dict):
        if payload.get("no_patient_specific_advice") is not True:
            errors.append(f"{prefix}: consultant event must block patient specific advice")

    if agent == "follow_up_monitor" and isinstance(payload, dict):
        if payload.get("state_update_required") is not True:
            errors.append(f"{prefix}: follow up event must require state update")

    return errors


def validate_text_boundaries(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for event in events:
        event_id = str(event.get("event_id", "unknown"))
        text = flatten_text(event).lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                errors.append(f"{event_id}: forbidden phrase {phrase!r}")
        for label, pattern in IDENTIFIER_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{event_id}: possible identifier pattern detected: {label}")
    return errors


def validate_scenarios(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    grouped = group_events(events)
    if len(grouped) < 3:
        errors.append("Expected at least three synthetic scenarios")

    for scenario_id, scenario_events in grouped.items():
        if not scenario_id:
            errors.append("Scenario id cannot be empty")
            continue
        agents = [str(event.get("agent")) for event in scenario_events]
        if agents != REQUIRED_AGENTS:
            errors.append(f"{scenario_id}: expected agent sequence {REQUIRED_AGENTS}, found {agents}")

        turns = [event.get("turn_index") for event in scenario_events]
        expected_turns = list(range(1, len(scenario_events) + 1))
        if turns != expected_turns:
            errors.append(f"{scenario_id}: turn_index values must be continuous from 1")

        for index, event in enumerate(scenario_events):
            expected_next = scenario_events[index + 1]["agent"] if index + 1 < len(scenario_events) else None
            if event.get("expected_next_agent") != expected_next:
                errors.append(
                    f"{event.get('event_id')}: expected_next_agent must be {expected_next!r}"
                )

    return errors


def validate_events(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not events:
        return ["Fixture file contains no events"]

    seen_ids: set[str] = set()
    for index, event in enumerate(events, 1):
        event_id = str(event.get("event_id", ""))
        if event_id in seen_ids:
            errors.append(f"Duplicate event_id: {event_id}")
        seen_ids.add(event_id)
        errors.extend(validate_event_shape(event, index))

    all_agents = {str(event.get("agent")) for event in events}
    missing_agents = set(REQUIRED_AGENTS) - all_agents
    if missing_agents:
        errors.append(f"Missing required agents {sorted(missing_agents)}")

    errors.extend(validate_scenarios(events))
    errors.extend(validate_text_boundaries(events))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate synthetic Agentic Medicine Sandbox event fixtures."
    )
    parser.add_argument("fixtures", nargs="?", type=Path, default=DEFAULT_FIXTURES)
    args = parser.parse_args()

    path = args.fixtures.resolve()
    if not path.exists():
        print(f"FAIL missing fixture file: {path_label(path)}")
        return 1

    try:
        events = load_events(path)
    except Exception as error:  # noqa: BLE001
        print(f"FAIL {error}")
        return 1

    errors = validate_events(events)
    if errors:
        print("FAIL agentic medicine sandbox event fixture validation")
        for error in errors:
            print(f"- {error}")
        return 1

    grouped = group_events(events)
    print("PASS agentic medicine sandbox event fixture validation")
    print(f"fixtures={path_label(path)}")
    print(f"scenarios={len(grouped)}")
    print(f"events={len(events)}")
    print(f"agents={','.join(REQUIRED_AGENTS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
