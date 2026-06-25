#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "clinical_intelligence_stack_20260625.json"
BUILDER = ROOT / "scripts" / "build_clinical_intelligence_stack_20260625.py"
SCHEMA = ROOT / "data" / "clinical_state_language_v0_1_20260625.schema.json"
TRAJECTORIES = ROOT / "data" / "clinical_trajectory_seed_set_v0_1_20260625.jsonl"
DOCS = [
    ROOT / "docs" / "CLINICAL_INTELLIGENCE_STACK_MANIFESTO_20260625.md",
    ROOT / "docs" / "CLINICAL_STATE_LANGUAGE_V0_1_20260625.md",
    ROOT / "docs" / "CLINICAL_TRAJECTORY_ENGINE_V0_1_20260625.md",
    ROOT / "docs" / "MEDICAL_REASONING_VERIFIER_V0_1_20260625.md",
    ROOT / "docs" / "AGENTIC_MEDICINE_SANDBOX_V0_1_20260625.md",
]

REQUIRED_DOC_PHRASES = [
    "Clinical Intelligence Stack Manifesto",
    "Medical AI needs a clinical intelligence stack, not another chatbot benchmark.",
    "Clinical State Language",
    "Clinical Trajectory Engine",
    "Medical Reasoning Verifier",
    "Agentic Medicine Sandbox",
    "Multilingual Medical Intelligence",
    "Medical Intelligence Atlas",
    "make clinical_intelligence_stack",
]

FORBIDDEN_PHRASES = [
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used true",
    "model superiority proven",
    "medical advice provided",
    "diagnosis provided",
    "treatment recommendation provided",
    "regulatory clearance secured",
    "institutional approval granted",
    "partner confirmed",
    "endorsement confirmed",
    "publication accepted",
]


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"{path.relative_to(ROOT)} line {line_number}: {error}") from error
    return rows


def main() -> int:
    errors: list[str] = []

    if not CONFIG.exists():
        errors.append(f"Missing config: {CONFIG.relative_to(ROOT)}")
        config = {}
    else:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    if not SCHEMA.exists():
        errors.append(f"Missing schema: {SCHEMA.relative_to(ROOT)}")
        schema = {}
    else:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    try:
        rows = load_jsonl(TRAJECTORIES)
    except Exception as error:  # noqa: BLE001
        rows = []
        errors.append(str(error))

    if len(config.get("source_anchors", [])) != 8:
        errors.append("Expected eight source anchors")
    if len(config.get("stack_layers", [])) != 6:
        errors.append("Expected six stack layers")
    if len(config.get("clinical_state_fields", [])) != 12:
        errors.append("Expected twelve clinical state fields")
    if len(config.get("verifier_dimensions", [])) != 10:
        errors.append("Expected ten verifier dimensions")
    if len(config.get("agent_roles", [])) != 6:
        errors.append("Expected six agent roles")
    if len(rows) != 20:
        errors.append("Expected twenty clinical trajectory rows")

    required_schema = set(schema.get("required", []))
    for field in [
        "state_id",
        "trajectory_id",
        "timepoint",
        "patient_voice",
        "problem_list",
        "timeline",
        "missing_data",
        "hypotheses",
        "evidence_for",
        "evidence_against",
        "risk_state",
        "action_boundary",
        "follow_up_triggers",
        "source_support_needed",
        "language_context",
        "synthetic_only",
        "patient_data_used",
        "clinical_use_allowed",
    ]:
        if field not in required_schema:
            errors.append(f"Schema missing required field: {field}")

    seen_ids: set[str] = set()
    for row in rows:
        trajectory_id = row.get("trajectory_id")
        if trajectory_id in seen_ids:
            errors.append(f"Duplicate trajectory id: {trajectory_id}")
        seen_ids.add(str(trajectory_id))
        if row.get("synthetic_only") is not True:
            errors.append(f"{trajectory_id}: synthetic_only must be true")
        if row.get("patient_data_used") is not False:
            errors.append(f"{trajectory_id}: patient_data_used must be false")
        if row.get("clinical_use_allowed") is not False:
            errors.append(f"{trajectory_id}: clinical_use_allowed must be false")
        states = row.get("states", [])
        if len(states) != 2:
            errors.append(f"{trajectory_id}: expected two states")
        for state in states:
            if state.get("patient_data_used") is not False:
                errors.append(f"{state.get('state_id')}: patient_data_used must be false")
            if state.get("clinical_use_allowed") is not False:
                errors.append(f"{state.get('state_id')}: clinical_use_allowed must be false")
            if not state.get("missing_data"):
                errors.append(f"{state.get('state_id')}: missing_data cannot be empty")
            if not state.get("source_support_needed"):
                errors.append(f"{state.get('state_id')}: source_support_needed cannot be empty")

    combined = ""
    for doc in DOCS:
        if not doc.exists():
            errors.append(f"Missing generated doc: {doc.relative_to(ROOT)}")
            continue
        combined += "\n" + doc.read_text(encoding="utf-8")

    lower = combined.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"Forbidden phrase: {phrase}")

    if errors:
        print("FAIL Clinical Intelligence Stack validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Clinical Intelligence Stack validation")
    print(f"config={CONFIG.relative_to(ROOT)}")
    print(f"schema={SCHEMA.relative_to(ROOT)}")
    print(f"trajectories={TRAJECTORIES.relative_to(ROOT)}")
    print(f"docs={len(DOCS)}")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
