#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "clinical_intelligence_stack_20260625.json"
SCHEMA = ROOT / "data" / "clinical_state_language_v0_1_20260625.schema.json"
TRAJECTORIES = ROOT / "data" / "clinical_trajectory_seed_set_v0_1_20260625.jsonl"
MANIFESTO = ROOT / "docs" / "CLINICAL_INTELLIGENCE_STACK_MANIFESTO_20260625.md"
STATE_DOC = ROOT / "docs" / "CLINICAL_STATE_LANGUAGE_V0_1_20260625.md"
TRAJECTORY_DOC = ROOT / "docs" / "CLINICAL_TRAJECTORY_ENGINE_V0_1_20260625.md"
VERIFIER_DOC = ROOT / "docs" / "MEDICAL_REASONING_VERIFIER_V0_1_20260625.md"
SANDBOX_DOC = ROOT / "docs" / "AGENTIC_MEDICINE_SANDBOX_V0_1_20260625.md"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def numbered(items: list[str]) -> list[str]:
    return [f"{index}. {item}" for index, item in enumerate(items, 1)]


def build_schema(data: dict) -> dict:
    properties = {
        "state_id": {"type": "string"},
        "trajectory_id": {"type": "string"},
        "timepoint": {"type": "string"},
        "patient_voice": {"type": "string"},
        "problem_list": {"type": "array", "items": {"type": "string"}},
        "timeline": {"type": "array", "items": {"type": "string"}},
        "missing_data": {"type": "array", "items": {"type": "string"}},
        "hypotheses": {"type": "array", "items": {"type": "string"}},
        "evidence_for": {"type": "array", "items": {"type": "string"}},
        "evidence_against": {"type": "array", "items": {"type": "string"}},
        "risk_state": {"type": "string"},
        "action_boundary": {"type": "string"},
        "follow_up_triggers": {"type": "array", "items": {"type": "string"}},
        "source_support_needed": {"type": "array", "items": {"type": "string"}},
        "language_context": {"type": "string"},
        "synthetic_only": {"type": "boolean"},
        "patient_data_used": {"type": "boolean"},
        "clinical_use_allowed": {"type": "boolean"},
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/goktugozkanmd/medical-ai-failure-atlas/clinical-state-language/v0.1",
        "title": "Clinical State Language v0.1",
        "description": data["position"],
        "type": "object",
        "required": list(properties),
        "additionalProperties": False,
        "properties": properties,
    }


def build_trajectory_rows(data: dict) -> list[dict]:
    rows: list[dict] = []
    for index, seed in enumerate(data["trajectory_seeds"], 1):
        trajectory_id = seed["id"]
        row = {
            "trajectory_id": trajectory_id,
            "version": "v0.1",
            "domain": seed["domain"],
            "arc": seed["arc"],
            "synthetic_only": True,
            "patient_data_used": False,
            "clinical_use_allowed": False,
            "ranking_allowed": False,
            "states": [
                {
                    "state_id": f"{trajectory_id}-S1",
                    "trajectory_id": trajectory_id,
                    "timepoint": "initial",
                    "patient_voice": seed["initial_voice"],
                    "problem_list": [seed["arc"]],
                    "timeline": ["initial synthetic prompt"],
                    "missing_data": ["role context", "vital signs or severity marker", "current medication or relevant history"],
                    "hypotheses": ["high risk path remains possible", "lower risk path remains possible"],
                    "evidence_for": ["synthetic prompt contains a possible risk signal"],
                    "evidence_against": ["insufficient data for a settled conclusion"],
                    "risk_state": "uncertain",
                    "action_boundary": "Name missing variables and route boundaries without diagnosis or treatment instruction.",
                    "follow_up_triggers": ["worsening symptom", "new danger sign", "missing result becomes available"],
                    "source_support_needed": ["source needed before public clinical claim"],
                    "language_context": "plain clinical English with room for Turkish localization",
                    "synthetic_only": True,
                    "patient_data_used": False,
                    "clinical_use_allowed": False,
                },
                {
                    "state_id": f"{trajectory_id}-S2",
                    "trajectory_id": trajectory_id,
                    "timepoint": "turning point",
                    "patient_voice": seed["turning_point"],
                    "problem_list": [seed["arc"], "state changed over time"],
                    "timeline": ["initial synthetic prompt", "new state variable appears"],
                    "missing_data": ["exact timing", "objective severity marker", "responsible clinician or setting"],
                    "hypotheses": ["trajectory risk increased", "initial reassurance may be unsafe"],
                    "evidence_for": ["state changed after the first message"],
                    "evidence_against": ["no complete evaluation record is present"],
                    "risk_state": "changed",
                    "action_boundary": seed["expected_intelligence"],
                    "follow_up_triggers": ["persistent symptom", "objective worsening", "unreviewed result"],
                    "source_support_needed": ["source needed before guideline or performance claim"],
                    "language_context": "plain clinical English with room for Turkish localization",
                    "synthetic_only": True,
                    "patient_data_used": False,
                    "clinical_use_allowed": False,
                },
            ],
            "expected_intelligence": seed["expected_intelligence"],
        }
        rows.append(row)
    return rows


def dump_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(rows: list[dict]) -> str:
    return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n"


def source_lines(data: dict) -> list[str]:
    lines: list[str] = []
    for source in data["source_anchors"]:
        lines.extend(
            [
                f"### {source['id']} {source['name']}",
                "",
                f"URL: {source['url']}",
                "",
                f"Claim support: {source['claim_support']}",
                "",
                f"Use in stack: {source['use_in_stack']}",
                "",
            ]
        )
    return lines


def render_manifesto(data: dict, rows: list[dict]) -> str:
    lines = [
        "# Clinical Intelligence Stack Manifesto",
        "",
        f"Date: {data['date']}",
        "",
        "## Thesis",
        "",
        data["public_thesis"],
        "",
        "Medical AI teams already know how to make a model answer. The next hard problem is to make a system represent a patient state, track change, choose what it still does not know, and hand work to the right tool or human.",
        "",
        "## Position",
        "",
        data["position"],
        "",
        "## Why Now",
        "",
        *numbered(data["why_now"]),
        "",
        "## First Build",
        "",
        f"Clinical state schema: `{SCHEMA.relative_to(ROOT)}`",
        "",
        f"Synthetic trajectory seed rows: `{TRAJECTORIES.relative_to(ROOT)}`",
        "",
        f"Trajectory count: {len(rows)}",
        "",
        "## Stack Layers",
        "",
    ]
    for layer in data["stack_layers"]:
        lines.extend(
            [
                f"### {layer['layer']}",
                "",
                f"Job: {layer['job']}",
                "",
                f"First artifact: `{layer['first_artifact']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Source Anchors",
            "",
            *source_lines(data),
            "## Boundaries",
            "",
            *numbered([f"No {claim} claim." for claim in data["blocked_claims"]]),
            "",
            "## Build Command",
            "",
            "`make clinical_intelligence_stack`",
            "",
        ]
    )
    return "\n".join(lines)


def render_state_doc(data: dict) -> str:
    lines = [
        "# Clinical State Language v0.1",
        "",
        f"Date: {data['date']}",
        "",
        "## Purpose",
        "",
        "Clinical State Language gives medical AI systems a compact way to represent the state of a synthetic patient over time. It keeps the model from treating a message as a complete clinical world.",
        "",
        "## Fields",
        "",
    ]
    for index, field in enumerate(data["clinical_state_fields"], 1):
        lines.extend([f"### {index}. {field['field']}", "", field["definition"], ""])
    lines.extend(
        [
            "## Required Guardrails",
            "",
            "1. Every state must be synthetic.",
            "2. Every state must mark patient data use as false.",
            "3. Every state must mark clinical use as false.",
            "4. Every state must name missing data.",
            "5. Every state must state what source support would be needed before a public clinical claim.",
            "",
        ]
    )
    return "\n".join(lines)


def render_trajectory_doc(data: dict, rows: list[dict]) -> str:
    domain_counts: dict[str, int] = {}
    for row in rows:
        domain_counts[row["domain"]] = domain_counts.get(row["domain"], 0) + 1
    lines = [
        "# Clinical Trajectory Engine v0.1",
        "",
        f"Date: {data['date']}",
        "",
        "## Purpose",
        "",
        "The trajectory engine turns one message into a short clinical journey. It tests whether a model can keep state across time instead of answering each turn in isolation.",
        "",
        "## Seed Set",
        "",
        f"Rows: {len(rows)}",
        "",
        "Synthetic only: true",
        "",
        "Patient data used: false",
        "",
        "Clinical use allowed: false",
        "",
        "## Domains",
        "",
    ]
    for domain, count in sorted(domain_counts.items()):
        lines.append(f"{domain}: {count}")
    lines.extend(["", "## Example Rows", ""])
    for row in rows[:5]:
        lines.extend(
            [
                f"### {row['trajectory_id']} {row['domain']}",
                "",
                f"Arc: {row['arc']}",
                "",
                f"Expected intelligence: {row['expected_intelligence']}",
                "",
            ]
        )
    lines.extend(["## Data File", "", f"`{TRAJECTORIES.relative_to(ROOT)}`", ""])
    return "\n".join(lines)


def render_verifier_doc(data: dict) -> str:
    lines = [
        "# Medical Reasoning Verifier v0.1",
        "",
        f"Date: {data['date']}",
        "",
        "## Purpose",
        "",
        "The verifier scores the shape of clinical reasoning, not model prestige. It asks whether the answer maintained state, handled missing data, sequenced action, and avoided claims the local evidence cannot support.",
        "",
        "## Dimensions",
        "",
        *numbered(data["verifier_dimensions"]),
        "",
        "## Output Shape",
        "",
        "Each verifier row should produce a pass, caution, or fail state with one sentence of evidence and one repair instruction.",
        "",
        "## Model Team Value",
        "",
        "Math and code have clear verifiers. Clinical AI needs verifier rows that represent incomplete state, time, action, and source support. This package starts that layer without patient data or clinical deployment claims.",
        "",
    ]
    return "\n".join(lines)


def render_sandbox_doc(data: dict) -> str:
    lines = [
        "# Agentic Medicine Sandbox v0.1",
        "",
        f"Date: {data['date']}",
        "",
        "## Purpose",
        "",
        "The sandbox frames medical AI as a process. The model must listen, maintain state, request data, check sources, hand off, and update when the trajectory changes.",
        "",
        "## Agent Roles",
        "",
    ]
    for index, role in enumerate(data["agent_roles"], 1):
        lines.extend([f"### {index}. {role['role']}", "", role["job"], ""])
    lines.extend(
        [
            "## First Loop",
            "",
            "1. Patient simulator emits a synthetic state.",
            "2. Clinician reasoner builds a Clinical State Language row.",
            "3. Test result emitter changes one state variable.",
            "4. Medical Reasoning Verifier checks the model response.",
            "5. Follow up monitor checks whether the next step changed.",
            "",
            "## Boundary",
            "",
            "This sandbox is for research, representation, and evaluation design. It is not clinical deployment, medical advice, diagnosis, treatment, or triage.",
            "",
        ]
    )
    return "\n".join(lines)


def build_outputs(data: dict) -> dict[Path, str]:
    rows = build_trajectory_rows(data)
    return {
        SCHEMA: dump_json(build_schema(data)),
        TRAJECTORIES: dump_jsonl(rows),
        MANIFESTO: render_manifesto(data, rows),
        STATE_DOC: render_state_doc(data),
        TRAJECTORY_DOC: render_trajectory_doc(data, rows),
        VERIFIER_DOC: render_verifier_doc(data),
        SANDBOX_DOC: render_sandbox_doc(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = load_config()
    outputs = build_outputs(data)

    if args.check:
        errors: list[str] = []
        for path, expected in outputs.items():
            if not path.exists():
                errors.append(f"Missing generated file: {path.relative_to(ROOT)}")
                continue
            if path.read_text(encoding="utf-8") != expected:
                errors.append(f"Generated file is stale: {path.relative_to(ROOT)}")
        if errors:
            for error in errors:
                print(f"FAIL {error}")
            return 1
        print("PASS Clinical Intelligence Stack generated files are current")
        for path in outputs:
            print(f"file={path.relative_to(ROOT)}")
        return 0

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
