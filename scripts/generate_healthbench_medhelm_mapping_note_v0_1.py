#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HEALTHBENCH_MEDHELM_MAPPING_NOTE_V0_1.md"
DATA = ROOT / "docs" / "healthbench_medhelm_mapping_note_v0_1.json"


SOURCE_ANCHORS = [
    {
        "source_id": "openai_healthbench",
        "source_name": "OpenAI HealthBench public page",
        "source_url": "https://openai.com/index/healthbench/",
        "source_basis": "realistic health scenarios and physician expert rubric emphasis",
        "mapping_use": "rubric discipline and clinically relevant response review",
    },
    {
        "source_id": "healthbench_professional",
        "source_name": "HealthBench Professional public abstract",
        "source_url": "https://arxiv.org/abs/2604.27470",
        "source_basis": "real clinician tasks, care consult, writing and documentation, medical research, physician authored conversations, and adjudicated rubrics",
        "mapping_use": "clinician workflow surface and rubric adjudication boundaries",
    },
    {
        "source_id": "medhelm_site",
        "source_name": "MedHELM public site",
        "source_url": "https://medhelm.org/",
        "source_basis": "121 clinical tasks, 22 subcategories, 31 datasets, 5 categories, and measures across accuracy, calibration, robustness, and writing style",
        "mapping_use": "task taxonomy and metric family orientation",
    },
    {
        "source_id": "medhelm_leaderboard",
        "source_name": "Stanford HELM MedHELM latest page",
        "source_url": "https://crfm.stanford.edu/helm/medhelm/latest/",
        "source_basis": "structured taxonomy, clinical task coverage, and benchmark surface reporting",
        "mapping_use": "public taxonomy mapping without performance claims",
    },
]


MAPPING_ROWS = [
    {
        "row_id": "HHM001",
        "local_surface": "SourceCheckup Medical",
        "healthbench_lens": "physician rubric discipline for answer support and uncertainty wording",
        "medhelm_lens": "medical research assistance and writing style review",
        "track_a_value": "Turkish source support review before any sandbox or workflow discussion",
        "track_b_value": "global source verification contributor surface",
        "blocked_claim": "benchmark compatibility",
        "next_action": "keep source claim rows synthetic and add reviewer questions",
    },
    {
        "row_id": "HHM002",
        "local_surface": "Medical AI Failure Atlas",
        "healthbench_lens": "realistic health scenario failure pattern review",
        "medhelm_lens": "clinical decision support and patient communication task orientation",
        "track_a_value": "Turkish clinical risk education without deployment claim",
        "track_b_value": "open failure pattern taxonomy for public review",
        "blocked_claim": "model ranking",
        "next_action": "map failure modes to task families without scoring",
    },
    {
        "row_id": "HHM003",
        "local_surface": "TR MedLLM SafetyBench",
        "healthbench_lens": "clinician rubric wording for missing context and escalation",
        "medhelm_lens": "multilingual clinical task readiness discussion",
        "track_a_value": "Turkish medical language model safety cases",
        "track_b_value": "multilingual safety case contribution surface",
        "blocked_claim": "clinical validation",
        "next_action": "add task family labels without claiming benchmark status",
    },
    {
        "row_id": "HHM004",
        "local_surface": "Turkish Clinical AI Assurance Lab",
        "healthbench_lens": "rubric gate and adjudication trail",
        "medhelm_lens": "calibration, robustness, and writing style boundary review",
        "track_a_value": "assurance card language for Turkish health AI review",
        "track_b_value": "release gate pattern for public medical AI infrastructure",
        "blocked_claim": "official endorsement",
        "next_action": "connect assurance cards to benchmark style evidence fields",
    },
    {
        "row_id": "HHM005",
        "local_surface": "Health Data Quality and Label Audit Commons",
        "healthbench_lens": "rubric item provenance and adjudication quality",
        "medhelm_lens": "dataset and task surface quality review",
        "track_a_value": "synthetic data quality gate for Turkish benchmark work",
        "track_b_value": "open label audit pattern for medical AI eval datasets",
        "blocked_claim": "dataset quality proof",
        "next_action": "add label audit fields for source, rubric, and reviewer state",
    },
    {
        "row_id": "HHM006",
        "local_surface": "Clinician AI Literacy Academy Turkiye",
        "healthbench_lens": "clinician rubric literacy and adversarial scenario reading",
        "medhelm_lens": "clinician task taxonomy literacy",
        "track_a_value": "clinician education on benchmark limits and review gates",
        "track_b_value": "public teaching surface for benchmark literacy",
        "blocked_claim": "safety proof",
        "next_action": "turn mapping rows into short clinician review lessons",
    },
]


BOUNDARIES = [
    "No compatibility claim.",
    "No benchmark equivalence claim.",
    "No model ranking.",
    "No model safety proof.",
    "No clinical validation.",
    "No clinical deployment.",
    "No official endorsement.",
    "No patient data.",
    "No endpoint call.",
    "No score report.",
]


def write_json() -> None:
    payload = {
        "artifact": "healthbench_medhelm_mapping_note_v0_1",
        "date": "2026 06 17",
        "status": "public preview",
        "contains_patient_data": False,
        "not_for_clinical_use": True,
        "no_model_calls": True,
        "no_endpoint_calls": True,
        "no_ranking": True,
        "no_compatibility_claim": True,
        "source_anchors": SOURCE_ANCHORS,
        "mapping_rows": MAPPING_ROWS,
        "boundaries": BOUNDARIES,
    }
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_doc() -> None:
    lines: list[str] = [
        "# HealthBench and MedHELM mapping note v0.1",
        "",
        "Date: 2026 06 17",
        "",
        "Status: public preview.",
        "",
        "This note maps local synthetic medical AI safety surfaces toward HealthBench and MedHELM style review without claiming compatibility, equivalence, acceptance, ranking, validation, deployment, safety proof, source truth certification, or endorsement.",
        "",
        "It is a bounded orientation artifact for public infrastructure review.",
        "",
        "## Source anchors checked",
        "",
        "Checked on 2026 06 17:",
        "",
    ]
    for index, source in enumerate(SOURCE_ANCHORS, start=1):
        lines.append(f"{index}. {source['source_name']}: {source['source_url']}")
    lines.extend(
        [
            "",
            "Current source summary:",
            "",
        ]
    )
    for index, source in enumerate(SOURCE_ANCHORS, start=1):
        lines.append(f"{index}. {source['source_basis']}.")
    lines.extend(
        [
            "",
            "## Mapping boundary",
            "",
            "Allowed wording:",
            "",
            "`HealthBench and MedHELM oriented mapping note`",
            "",
            "`mapping toward benchmark style review surfaces`",
            "",
            "`synthetic local infrastructure readiness note`",
            "",
            "Not allowed wording:",
            "",
            "`HealthBench compatible`",
            "",
            "`MedHELM compatible`",
            "",
            "`benchmark validated`",
            "",
            "`accepted benchmark extension`",
            "",
            "`model ranking report`",
            "",
            "`clinical validation`",
            "",
            "## Mapping rows",
            "",
        ]
    )
    for row in MAPPING_ROWS:
        lines.extend(
            [
                f"### {row['row_id']}: {row['local_surface']}",
                "",
                f"HealthBench lens: {row['healthbench_lens']}.",
                "",
                f"MedHELM lens: {row['medhelm_lens']}.",
                "",
                f"Track A value: {row['track_a_value']}.",
                "",
                f"Track B value: {row['track_b_value']}.",
                "",
                f"Blocked claim: {row['blocked_claim']}.",
                "",
                f"Next action: {row['next_action']}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Release boundaries",
            "",
        ]
    )
    for index, boundary in enumerate(BOUNDARIES, start=1):
        lines.append(f"{index}. {boundary}")
    lines.extend(
        [
            "",
            "## Track A value",
            "",
            "For Turkiye health AI safety infrastructure, this note gives a clinician led way to connect local Turkish medical language model safety, source review, assurance lab, literacy, and label audit surfaces to international evaluation vocabulary while blocking official route, sandbox, deployment, validation, ranking, and endorsement claims.",
            "",
            "## Track B value",
            "",
            "For global open source medical AI evaluation, this note makes the repository easier for benchmark maintainers and contributors to inspect without making a compatibility claim.",
            "",
            "## Next safe public action",
            "",
            "Keep the mapping note public, add reviewer questions to SourceCheckup and Failure Atlas rows, and open external maintainer discussion only after exact text review and owner clearance.",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    write_json()
    write_doc()
    print(f"wrote {DOC.relative_to(ROOT)}")
    print(f"wrote {DATA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
