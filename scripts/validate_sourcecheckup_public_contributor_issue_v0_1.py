#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "sourcecheckup" / "PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md"
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "sourcecheckup_review.yml"

REQUIRED_GUIDE_PHRASES = [
    "SourceCheckup public contributor issue guide",
    "synthetic source claim review examples",
    "not clinical advice",
    "not patient data",
    "not clinical deployment",
    "not clinical validation",
    "not a source truth certificate",
    "not a model safety claim",
    "SourceCheckup output is a review queue",
    ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
    "sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl",
    "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
    "locator_format",
    "source_exists",
    "metadata_match",
    "exact_claim_support",
    "guideline_scope",
    "policy_jurisdiction",
    "rewrite_without_source_claim",
]

REQUIRED_TEMPLATE_PHRASES = [
    "SourceCheckup source review",
    "labels: [\"sourcecheckup\", \"source review\"]",
    "synthetic examples only",
    "does not verify clinical truth",
    "source_surface",
    "synthetic_answer_excerpt",
    "exact_claim",
    "central_claim",
    "declared_sources",
    "required_evidence",
    "proposed_public_action",
    "This is synthetic and contains no patient data.",
    "No external action has been executed.",
    "Outward use is not allowed without maintainer review.",
    "SourceCheckup output is a review queue, not proof that a medical claim is true.",
]

FORBIDDEN_PHRASES = [
    "clinically validated",
    "validated for clinical use",
    "safe for clinical use",
    "official approval",
    "official acceptance",
    "sandbox access granted",
    "institutional endorsement",
    "real patient data used",
    "source proves",
    "model is safe",
    "best model",
]


def check_text(path: Path, required_phrases: list[str], errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()
    for phrase in required_phrases:
        if phrase.lower() not in lower_text:
            errors.append(f"{path.relative_to(ROOT)} missing required phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"{path.relative_to(ROOT)} forbidden phrase present: {phrase}")
    return text


def main() -> int:
    errors: list[str] = []
    guide_text = check_text(GUIDE, REQUIRED_GUIDE_PHRASES, errors)
    template_text = check_text(TEMPLATE, REQUIRED_TEMPLATE_PHRASES, errors)

    for relative_path in [
        ".github/ISSUE_TEMPLATE/sourcecheckup_review.yml",
        "sourcecheckup/schemas/sourcecheckup_contribution_schema_v0_2.json",
        "sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl",
        "sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl",
    ]:
        if relative_path not in guide_text and relative_path not in template_text:
            errors.append(f"Missing public route reference: {relative_path}")
        if not (ROOT / relative_path).exists():
            errors.append(f"Referenced file does not exist: {relative_path}")

    if errors:
        print("FAIL SourceCheckup public contributor issue validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SourceCheckup public contributor issue validation")
    print(f"guide={GUIDE.relative_to(ROOT)}")
    print(f"template={TEMPLATE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
