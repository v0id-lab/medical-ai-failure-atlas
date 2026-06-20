#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_OUTSIDE_REVIEWER_MICRO_BRIEF_20260620.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_public_action_audit_20260620.md"
SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_manual_source_support_20260620.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_release_notes_20260620.md"
RELEASE_AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_release_audit_20260620.md"
RELEASE_REFS = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_release_refs_20260620.json"
RELEASE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_outside_reviewer_micro_brief_release_source_support_20260620.md"

REQUIRED_FILES = [DOC, AUDIT, SUPPORT, RELEASE_NOTES, RELEASE_AUDIT, RELEASE_REFS, RELEASE_SUPPORT]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Outside Reviewer Micro Brief",
    "Leave one small objection on issue 154.",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/154",
    "One useful sentence is enough",
    "not maintaining this repository",
    "not posting through a project account",
    "controlled seed can test comment routing, but it is not outside review and is not external validation",
    "Use synthetic or public examples only.",
    "Done means issue 154 has one true outside comment",
]

FORBIDDEN = [
    "patient data used",
    "real patient evidence confirmed",
    "clinically validated",
    "clinical deployment ready",
    "safe for clinical use",
    "diagnosis advice provided",
    "treatment advice provided",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "TBYS submitted",
    "PRODIS submitted",
    "official guidance",
    "compliance certified",
    "outside style public objection",
    "independent validation",
    "external validation achieved",
]


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def check_text(label: str, text: str, errors: list[str]) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing file: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""
    support_text = SUPPORT.read_text(encoding="utf-8") if SUPPORT.exists() else ""
    release_text = RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else ""
    release_audit_text = RELEASE_AUDIT.read_text(encoding="utf-8") if RELEASE_AUDIT.exists() else ""
    release_support_text = RELEASE_SUPPORT.read_text(encoding="utf-8") if RELEASE_SUPPORT.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")

    if "Allowed action: public GitHub commit after validation." not in audit_text:
        errors.append("Audit missing allowed action boundary")
    if "navigation claims only" not in support_text:
        errors.append("Source support missing navigation claim boundary")
    if "Issue 154 state and comment count." not in support_text:
        errors.append("Source support missing issue readback check")
    if "This release adds a short public brief for one true outside reviewer comment." not in release_text:
        errors.append("Release notes missing release purpose")
    if "medical-ai-safety-field-kit-outside-reviewer-micro-brief-20260620" not in release_audit_text:
        errors.append("Release audit missing release target")
    if "Allowed action: public GitHub release after validation." not in release_audit_text:
        errors.append("Release audit missing allowed action boundary")
    if "navigation claims only" not in release_support_text:
        errors.append("Release source support missing navigation claim boundary")
    if "No formal references are used in the release notes." not in release_support_text:
        errors.append("Release source support missing reference boundary")
    if "Release readback after action" not in release_audit_text:
        errors.append("Release audit missing release readback")
    if "Release is not draft." not in release_support_text:
        errors.append("Release source support missing draft readback")
    if "Release is not prerelease." not in release_support_text:
        errors.append("Release source support missing prerelease readback")

    if RELEASE_REFS.exists():
        import json

        payload = json.loads(RELEASE_REFS.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_outside_reviewer_micro_brief_release":
            errors.append("Unexpected release refs artifact")
        if payload.get("formal_references") != []:
            errors.append("Release refs should have zero formal references")
        if payload.get("primary_issue") != 154:
            errors.append("Release refs expected primary issue 154")
        for flag in [
            "contains_patient_data",
            "claims_clinical_validation",
            "claims_clinical_deployment",
            "claims_benchmark_ranking",
            "claims_score_certification",
            "claims_source_truth_certification",
            "claims_partner",
            "claims_institutional_approval",
            "claims_endorsement",
            "claims_formal_application",
            "claims_payment",
            "claims_terms_acceptance",
            "requires_tbys_action",
            "requires_prodis_action",
        ]:
            if payload.get(flag) is not False:
                errors.append(f"Expected false release flag: {flag}")

    check_text("Doc", doc_text, errors)
    check_text("Audit", audit_text, errors)
    check_text("Source support", support_text, errors)
    check_text("Release notes", release_text, errors)
    check_text("Release audit", release_audit_text, errors)
    check_text("Release source support", release_support_text, errors)

    if errors:
        print("FAIL Outside Reviewer Micro Brief validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Outside Reviewer Micro Brief validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
