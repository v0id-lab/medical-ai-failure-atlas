#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCECHECKUP_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "sourcecheckup_review.yml"
FAILURE_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "synthetic_failure_case.yml"
GUIDE = ROOT / "docs" / "CONTRIBUTOR_ISSUE_TEMPLATE_REVIEWER_QUESTIONS_V0_1.md"

REQUIRED_FILES = [
    SOURCECHECKUP_TEMPLATE,
    FAILURE_TEMPLATE,
    GUIDE,
    ROOT / "docs" / "BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md",
    ROOT / "docs" / "benchmark_style_reviewer_questions_v0_1.json",
]

REQUIRED_TEMPLATE_PHRASES = [
    "benchmark_reviewer_question_id",
    "benchmark_lens",
    "reviewer_question",
    "blocked_claim_type",
    "This does not add scoring, ranking, benchmark compatibility, endpoint, patient data, clinical validation, or endorsement claims.",
]

REQUIRED_SOURCECHECKUP_PHRASES = [
    "SourceCheckup source review",
    "HealthBench rubric discipline",
    "MedHELM policy and workflow task orientation",
    "source truth certification",
    "official policy proof",
    "benchmark compatibility",
]

REQUIRED_FAILURE_PHRASES = [
    "Synthetic medical AI failure case",
    "HealthBench realistic scenario review",
    "MedHELM clinical decision support orientation",
    "false reassurance safety proof",
    "unsafe precision",
    "communication safety proof",
]

REQUIRED_GUIDE_PHRASES = [
    "Contributor issue template reviewer questions v0.1",
    ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
    ".github/ISSUE_TEMPLATE/synthetic_failure_case.yml",
    "benchmark_reviewer_question_id",
    "benchmark_lens",
    "reviewer_question",
    "blocked_claim_type",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a benchmark compatibility claim",
    "not a benchmark equivalence claim",
    "not a score report",
    "not a model ranking",
    "not an endpoint result",
    "not an official endorsement",
    "SourceCheckup reviewer question rows should focus on source support",
    "Failure Atlas reviewer question rows should focus on escalation",
    "without claiming sandbox access",
    "no score, no ranking, no compatibility, and no endorsement boundaries",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "patient data used",
    "model is safe",
    "best model",
]


def read(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_phrases(path: Path, text: str, phrases: list[str], errors: list[str]) -> None:
    lower = text.lower()
    for phrase in phrases:
        if phrase.lower() not in lower:
            errors.append(f"{path.relative_to(ROOT)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            errors.append(f"{path.relative_to(ROOT)} forbidden phrase present: {phrase}")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    sourcecheckup = read(SOURCECHECKUP_TEMPLATE, errors)
    failure = read(FAILURE_TEMPLATE, errors)
    guide = read(GUIDE, errors)

    require_phrases(SOURCECHECKUP_TEMPLATE, sourcecheckup, REQUIRED_TEMPLATE_PHRASES + REQUIRED_SOURCECHECKUP_PHRASES, errors)
    require_phrases(FAILURE_TEMPLATE, failure, REQUIRED_TEMPLATE_PHRASES + REQUIRED_FAILURE_PHRASES, errors)
    require_phrases(GUIDE, guide, REQUIRED_GUIDE_PHRASES, errors)

    if "-" in guide:
        errors.append(f"{GUIDE.relative_to(ROOT)} contains hyphen character")

    if "BSRQ" not in sourcecheckup or "BSRQ" not in failure:
        errors.append("Issue templates should mention local BSRQ ids")

    if errors:
        print("FAIL benchmark reviewer question issue template validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS benchmark reviewer question issue template validation")
    print(f"sourcecheckup_template={SOURCECHECKUP_TEMPLATE.relative_to(ROOT)}")
    print(f"failure_template={FAILURE_TEMPLATE.relative_to(ROOT)}")
    print(f"guide={GUIDE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
