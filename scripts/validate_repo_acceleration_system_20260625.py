#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "docs" / "repo_acceleration_system_20260625.json"
BUILDER = ROOT / "scripts" / "build_repo_acceleration_system_20260625.py"
OUTPUTS = [
    ROOT / "docs" / "REPO_ACCELERATION_NORTH_STAR_20260625.md",
    ROOT / "docs" / "SIX_MONTH_COMPRESSED_BUILD_MAP_20260625.md",
    ROOT / "docs" / "NEXT_72_HOUR_EXECUTION_QUEUE_20260625.md",
    ROOT / "docs" / "CLINICIAN_SEVERITY_LAYER_PRODUCT_SPEC_20260625.md",
    ROOT / "docs" / "EXTERNAL_PROOF_OF_WORK_LEDGER_20260625.md",
]

REQUIRED_PHRASES = [
    "Repo Acceleration North Star",
    "clinician led medical AI failure intelligence layer",
    "The repo is not another leaderboard",
    "Clinician severity layer",
    "Source support layer",
    "Claim hygiene layer",
    "Turkish clinical context layer",
    "Open source eval bridge",
    "Six Month Compressed Build Map",
    "Next 72 Hour Execution Queue",
    "Clinician Severity Layer Product Spec",
    "External Proof Of Work Ledger",
    "make repo_acceleration_system",
]

FORBIDDEN_PHRASES = [
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "model superiority proven",
    "score certified",
    "source truth certified",
    "regulatory clearance secured",
    "institutional approval granted",
    "partner confirmed",
    "endorsement confirmed",
    "accepted contribution",
    "merged contribution",
    "terms accepted",
    "payment completed",
]


def main() -> int:
    errors: list[str] = []

    if not JSON_PATH.exists():
        errors.append(f"Missing json: {JSON_PATH.relative_to(ROOT)}")
        data = {}
    else:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    combined = ""
    for path in OUTPUTS:
        if not path.exists():
            errors.append(f"Missing generated markdown: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text
        if "-" in text:
            errors.append(f"Generated markdown contains a hyphen character: {path.relative_to(ROOT)}")

    lower_combined = combined.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower_combined:
            errors.append(f"Missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_combined:
            errors.append(f"Forbidden phrase in generated docs: {phrase}")

    expected_lengths = {
        "positioning": 4,
        "product_stack": 5,
        "strategic_bets": 5,
        "six_month_outcomes": 6,
        "compressed_build_waves": 4,
        "severity_layer_fields": 8,
        "next_72_hour_queue": 12,
        "external_proof_routes": 5,
        "blocked_claims": 12,
        "proof_metrics": 10,
        "validator_commands": 3,
    }
    for key, expected in expected_lengths.items():
        if len(data.get(key, [])) != expected:
            errors.append(f"JSON {key} must contain {expected} rows")

    if errors:
        print("FAIL repo acceleration system validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS repo acceleration system validation")
    print(f"json={JSON_PATH.relative_to(ROOT)}")
    print(f"generated_docs={len(OUTPUTS)}")
    print(f"queue_items={len(data['next_72_hour_queue'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
