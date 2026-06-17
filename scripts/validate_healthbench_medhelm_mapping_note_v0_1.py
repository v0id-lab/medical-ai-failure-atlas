#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HEALTHBENCH_MEDHELM_MAPPING_NOTE_V0_1.md"
DATA = ROOT / "docs" / "healthbench_medhelm_mapping_note_v0_1.json"

REQUIRED_DOC_PHRASES = [
    "HealthBench and MedHELM mapping note v0.1",
    "HealthBench and MedHELM oriented mapping note",
    "mapping toward benchmark style review surfaces",
    "synthetic local infrastructure readiness note",
    "No compatibility claim.",
    "No benchmark equivalence claim.",
    "No model ranking.",
    "No clinical validation.",
    "No clinical deployment.",
    "No official endorsement.",
    "No patient data.",
    "No endpoint call.",
    "No score report.",
    "OpenAI HealthBench public page: https://openai.com/index/healthbench/",
    "HealthBench Professional public abstract: https://arxiv.org/abs/2604.27470",
    "MedHELM public site: https://medhelm.org/",
    "Stanford HELM MedHELM latest page: https://crfm.stanford.edu/helm/medhelm/latest/",
    "121 clinical tasks",
    "22 subcategories",
    "31 datasets",
    "5 categories",
    "accuracy, calibration, robustness, and writing style",
    "care consult, writing and documentation, medical research",
    "clinician led way",
    "external maintainer discussion only after exact text review and owner clearance",
]

REQUIRED_JSON_FLAGS = {
    "contains_patient_data": False,
    "not_for_clinical_use": True,
    "no_model_calls": True,
    "no_endpoint_calls": True,
    "no_ranking": True,
    "no_compatibility_claim": True,
}

FORBIDDEN_PHRASES = [
    "this repository is healthbench compatible",
    "this repository is medhelm compatible",
    "this artifact is benchmark validated",
    "this is an accepted benchmark extension",
    "this is a model ranking report",
    "clinical validation claim",
    "source truth certification claim",
    "official endorsement claim",
    "safety proof claim",
    "patient data used",
    "endpoint result",
]

REQUIRED_ROW_IDS = ["HHM001", "HHM002", "HHM003", "HHM004", "HHM005", "HHM006"]
REQUIRED_SURFACES = [
    "SourceCheckup Medical",
    "Medical AI Failure Atlas",
    "TR MedLLM SafetyBench",
    "Turkish Clinical AI Assurance Lab",
    "Health Data Quality and Label Audit Commons",
    "Clinician AI Literacy Academy Turkiye",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        fail(errors, f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        fail(errors, f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            fail(errors, f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            fail(errors, f"Doc contains forbidden phrase: {phrase}")
    if "-" in text:
        fail(errors, "Doc contains hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_JSON_FLAGS.items():
        if payload.get(key) is not expected:
            fail(errors, f"JSON flag {key} expected {expected}")
    source_anchors = payload.get("source_anchors", [])
    if len(source_anchors) != 4:
        fail(errors, "Expected 4 source anchors")
    mapping_rows = payload.get("mapping_rows", [])
    if len(mapping_rows) != 6:
        fail(errors, "Expected 6 mapping rows")
    row_ids = {row.get("row_id") for row in mapping_rows}
    for row_id in REQUIRED_ROW_IDS:
        if row_id not in row_ids:
            fail(errors, f"Missing mapping row id: {row_id}")
    surfaces = {row.get("local_surface") for row in mapping_rows}
    for surface in REQUIRED_SURFACES:
        if surface not in surfaces:
            fail(errors, f"Missing local surface: {surface}")
    for row in mapping_rows:
        blocked_claim = str(row.get("blocked_claim", "")).lower()
        if not blocked_claim:
            fail(errors, f"{row.get('row_id')}: missing blocked claim")
        if "compatibility" in str(row.get("next_action", "")).lower():
            fail(errors, f"{row.get('row_id')}: next action implies compatibility")

    if errors:
        print("FAIL HealthBench MedHELM mapping note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS HealthBench MedHELM mapping note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"mapping_rows={len(mapping_rows)}")
    print(f"source_anchors={len(source_anchors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
