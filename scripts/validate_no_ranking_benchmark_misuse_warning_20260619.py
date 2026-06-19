#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "NO_RANKING_BENCHMARK_MISUSE_WARNING_20260619.md"
DATA = ROOT / "docs" / "no_ranking_benchmark_misuse_warning_20260619.json"

REQUIRED_DOC_PHRASES = [
    "No Ranking Benchmark Misuse Warning",
    "public benchmark misuse warning",
    "using benchmark scores as safety proof",
    "not a benchmark result",
    "not model comparison",
    "not ranking",
    "not leaderboard",
    "not score certification",
    "not procurement evidence",
    "not clinical validation",
    "not clinical deployment",
    "not patient data",
    "not an official MedHELM, HealthBench, BRIDGE, OpenAI, CHAI, Joint Commission, hospital, university, regulator, vendor, or partner statement",
    "Score becomes safety proof",
    "Leaderboard becomes procurement evidence",
    "Benchmark pass becomes clinical validation",
    "Public demo becomes deployment readiness",
    "Single language score hides Turkish readiness",
    "Specialty average hides care stage risk",
    "Source support is missing",
    "Health data quality is unreviewed",
    "Human review role is absent",
    "Example leakage or benchmark contamination is unclear",
    "Minimum pass condition",
    "Stop conditions",
    "make no_ranking_benchmark_misuse_warning",
]

REQUIRED_SOURCE_URLS = {
    "https://medhelm.org/",
    "https://openai.com/index/healthbench/",
    "https://github.com/YLab-Open/BRIDGE",
    "https://www.chai.org/workgroup/cross-cutting/ai-governance",
    "https://www.chai.org/blog/chai-releases-draft-responsible-health-ai-framework-for-public-comment",
}

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "contains_healthbench_examples": False,
    "claims_benchmark_result": False,
    "claims_model_comparison": False,
    "claims_model_ranking": False,
    "claims_leaderboard_status": False,
    "claims_score_certification": False,
    "claims_procurement_evidence": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_partner": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
}

REQUIRED_PATTERNS = {
    "Score becomes safety proof",
    "Leaderboard becomes procurement evidence",
    "Benchmark pass becomes clinical validation",
    "Public demo becomes deployment readiness",
    "Single language score hides Turkish readiness",
    "Specialty average hides care stage risk",
    "Source support is missing",
    "Health data quality is unreviewed",
    "Human review role is absent",
    "Example leakage or benchmark contamination is unclear",
}

FORBIDDEN_PHRASES = [
    "safety proof confirmed",
    "procurement readiness confirmed",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data cleared",
    "official compatibility confirmed",
    "leaderboard submission complete",
    "score certification complete",
    "partner confirmed",
    "official role confirmed",
    "endorsed by",
    "payment completed",
    "terms accepted",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"Missing doc: {DOC.relative_to(ROOT)}")
    if not DATA.exists():
        errors.append(f"Missing data: {DATA.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    lower_text = text.lower()
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in lower_text:
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"Doc contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append("Doc contains non URL hyphen character")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    if payload.get("checked_after_reading_baglam2") is not True:
        errors.append("Expected BAGLAM2 read flag")
    if payload.get("checked_after_reading_trackers") is not True:
        errors.append("Expected tracker read flag")
    if payload.get("checked_gmail_before_build") is not True:
        errors.append("Expected Gmail checked flag")
    if payload.get("gmail_reply_state") != "no new route owner reply":
        errors.append("Expected no new route owner reply state")
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    urls = {item.get("source_url") for item in payload.get("source_anchors", [])}
    if urls != REQUIRED_SOURCE_URLS:
        errors.append("Source URL set does not match required source set")

    patterns = payload.get("misuse_patterns", [])
    if len(patterns) != 10:
        errors.append("Expected ten misuse patterns")
    found_patterns = {row.get("pattern") for row in patterns}
    missing = sorted(REQUIRED_PATTERNS - found_patterns)
    if missing:
        errors.append(f"Missing misuse patterns: {', '.join(missing)}")
    for row in patterns:
        for field in ["public_warning", "reviewer_question", "required_evidence", "blocked_claim"]:
            if not row.get(field):
                errors.append(f"{row.get('pattern')}: missing {field}")
        if len(row.get("required_evidence", [])) < 4:
            errors.append(f"{row.get('pattern')}: expected at least four evidence fields")

    if errors:
        print("FAIL no ranking benchmark misuse warning validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS no ranking benchmark misuse warning validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"misuse_patterns={len(patterns)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
