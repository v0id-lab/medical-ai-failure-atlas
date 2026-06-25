#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "docs" / "clinical_intelligence_stack_global_target_map_20260625.json"
BUILDER = ROOT / "scripts" / "build_clinical_intelligence_stack_global_target_map_20260625.py"
MARKDOWN = ROOT / "docs" / "CLINICAL_INTELLIGENCE_STACK_GLOBAL_TARGET_MAP_20260625.md"

REQUIRED_PHRASES = [
    "Clinical Intelligence Stack Global Target Map",
    "Medical AI needs a clinical intelligence stack, not another chatbot benchmark.",
    "Do not cold pitch a partnership",
    "reasoning model teams",
    "health benchmark builders",
    "health foundation model developers",
    "Turkiye health AI decision ecosystem",
    "AI hardware and national technology circles",
    "English X launch thread",
    "Turkish LinkedIn national frame post",
    "make clinical_intelligence_stack_global_target_map",
]

FORBIDDEN_PHRASES = [
    "partner confirmed",
    "endorsement confirmed",
    "will repost",
    "will approve",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "model superiority proven",
    "official role granted",
    "terms accepted",
    "payment completed",
]


def main() -> int:
    errors: list[str] = []

    if not CONFIG.exists():
        errors.append(f"Missing config: {CONFIG.relative_to(ROOT)}")
        data = {}
    else:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))

    check = subprocess.run(
        [sys.executable, str(BUILDER), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if check.returncode != 0:
        errors.append(check.stdout.strip())

    if len(data.get("source_anchors", [])) != 8:
        errors.append("Expected eight source anchors")
    if len(data.get("audience_routes", [])) != 5:
        errors.append("Expected five audience routes")
    if len(data.get("launch_sequence", [])) != 4:
        errors.append("Expected four launch sequence rows")
    if len(data.get("blocked_moves", [])) != 8:
        errors.append("Expected eight blocked moves")
    if len(data.get("next_artifacts", [])) != 5:
        errors.append("Expected five next artifacts")

    text = ""
    if not MARKDOWN.exists():
        errors.append(f"Missing markdown: {MARKDOWN.relative_to(ROOT)}")
    else:
        text = MARKDOWN.read_text(encoding="utf-8")

    lower = text.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"Missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"Forbidden phrase: {phrase}")

    if errors:
        print("FAIL Clinical Intelligence Stack global target map validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Clinical Intelligence Stack global target map validation")
    print(f"config={CONFIG.relative_to(ROOT)}")
    print(f"markdown={MARKDOWN.relative_to(ROOT)}")
    print(f"source_anchors={len(data['source_anchors'])}")
    print(f"audience_routes={len(data['audience_routes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
