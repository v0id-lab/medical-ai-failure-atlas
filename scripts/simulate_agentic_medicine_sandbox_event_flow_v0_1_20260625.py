#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_agentic_medicine_sandbox_event_fixtures_v0_1_20260625 import (
    DEFAULT_FIXTURES,
    REQUIRED_AGENTS,
    group_events,
    load_events,
    path_label,
    validate_events,
)


def append_list(target: list[str], value: Any) -> None:
    if isinstance(value, list):
        target.extend(str(item) for item in value)
    elif value is not None:
        target.append(str(value))


def simulate_scenario(scenario_id: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    state = {
        "scenario_id": scenario_id,
        "agent_sequence": [],
        "event_count": 0,
        "patient_state_messages": [],
        "working_states": [],
        "missing_data": [],
        "changed_variables": [],
        "source_support_checks": [],
        "consultant_constraints": [],
        "follow_up_status": [],
        "open_loop": False,
        "clinical_use_allowed": False,
        "patient_data_used": False,
    }

    trace: list[dict[str, Any]] = []
    for event in events:
        payload = event["payload"]
        agent = event["agent"]
        state["event_count"] += 1
        state["agent_sequence"].append(agent)

        if agent == "patient_simulator":
            state["patient_state_messages"].append(payload["patient_voice"])
            append_list(state["missing_data"], payload["missing_data"])
        elif agent == "clinician_reasoner":
            state["working_states"].append(payload["working_state"])
            append_list(state["missing_data"], payload["uncertainties"])
        elif agent == "test_result_emitter":
            state["changed_variables"].append(payload["changed_variable"])
        elif agent == "source_support_checker":
            state["source_support_checks"].append(
                {
                    "claim_to_check": payload["claim_to_check"],
                    "support_status": payload["support_status"],
                    "release_gate": payload["release_gate"],
                }
            )
        elif agent == "consultant_simulator":
            state["consultant_constraints"].append(
                {
                    "consultant_role": payload["consultant_role"],
                    "constraint_added": payload["constraint_added"],
                }
            )
        elif agent == "follow_up_monitor":
            state["follow_up_status"].append(
                {
                    "follow_up_trigger": payload["follow_up_trigger"],
                    "state_update_required": payload["state_update_required"],
                    "close_loop_status": payload["close_loop_status"],
                }
            )
            state["open_loop"] = payload["close_loop_status"] == "open_loop"

        trace.append(
            {
                "turn_index": event["turn_index"],
                "agent": agent,
                "event_type": event["event_type"],
                "expected_next_agent": event["expected_next_agent"],
            }
        )

    state["missing_data"] = sorted(set(state["missing_data"]))
    state["trace"] = trace
    state["complete_agent_loop"] = state["agent_sequence"] == REQUIRED_AGENTS
    return state


def build_report(events: list[dict[str, Any]], scenario_id: str | None = None) -> dict[str, Any]:
    grouped = group_events(events)
    if scenario_id:
        if scenario_id not in grouped:
            available = ", ".join(sorted(grouped))
            raise ValueError(f"Unknown scenario_id {scenario_id!r}. Available: {available}")
        grouped = {scenario_id: grouped[scenario_id]}

    scenarios = [
        simulate_scenario(current_id, current_events)
        for current_id, current_events in sorted(grouped.items())
    ]
    return {
        "fixture": path_label(DEFAULT_FIXTURES),
        "scenario_count": len(scenarios),
        "event_count": sum(item["event_count"] for item in scenarios),
        "required_agents": REQUIRED_AGENTS,
        "scenarios": scenarios,
        "boundary": {
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
        },
    }


def print_text_report(report: dict[str, Any]) -> None:
    print("PASS agentic medicine sandbox event flow simulation")
    print(f"scenarios={report['scenario_count']}")
    print(f"events={report['event_count']}")
    for scenario in report["scenarios"]:
        source_checks = len(scenario["source_support_checks"])
        constraints = len(scenario["consultant_constraints"])
        changed_variables = "; ".join(scenario["changed_variables"])
        print(
            f"- {scenario['scenario_id']}: agents={len(scenario['agent_sequence'])} "
            f"source_checks={source_checks} consultant_constraints={constraints} "
            f"open_loop={scenario['open_loop']}"
        )
        print(f"  changed_variables={changed_variables}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simulate synthetic Agentic Medicine Sandbox event flow."
    )
    parser.add_argument("fixtures", nargs="?", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--scenario-id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = args.fixtures.resolve()
    if not path.exists():
        print(f"FAIL missing fixture file: {path_label(path)}")
        return 1

    try:
        events = load_events(path)
        errors = validate_events(events)
        if errors:
            print("FAIL cannot simulate invalid agentic medicine sandbox fixtures")
            for error in errors:
                print(f"- {error}")
            return 1
        report = build_report(events, args.scenario_id)
    except Exception as error:  # noqa: BLE001
        print(f"FAIL {error}")
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print_text_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
