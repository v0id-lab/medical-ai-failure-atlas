#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_SFC005_SYNTHETIC_EVIDENCE_STARTER_20260620.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_sfc005_synthetic_evidence_starter_20260620.json"
ISSUE_BODY = ROOT / "outputs" / "medical_ai_safety_field_kit_sfc005_issue_body_20260620.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_sfc005_public_action_audit_20260620.md"

REQUIRED_FILES = [DOC, DATA, ISSUE_BODY, AUDIT]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit SFC005 Synthetic Evidence Starter",
    "synthetic failure card is cited as if it proves real world harm frequency",
    "Pattern seed check",
    "Frequency check",
    "Outcome check",
    "Model check",
    "Generalization check",
    "Source support check",
    "This synthetic card describes a plausible failure pattern for review",
    "It does not measure incidence, model performance, patient harm, or clinical outcome",
    "make medical_ai_safety_field_kit_sfc005_synthetic_evidence_starter",
]

REQUIRED_BODY_PHRASES = [
    "SFC005 synthetic evidence boundary starter",
    "Evidence claim that goes too far",
    "Done condition",
    "Boundary",
    "Main public intake",
]

REQUIRED_URLS = [
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/PUBLIC_SAFE_FAILURE_CARDS_20260619.md",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_GLOBAL_SAFETY_CLAIM_REVIEW_WORKBOOK_20260620.md",
    "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149",
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
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_FALSE_FLAGS = [
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
    body_text = ISSUE_BODY.read_text(encoding="utf-8") if ISSUE_BODY.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_BODY_PHRASES:
        if phrase.lower() not in body_text.lower():
            errors.append(f"Issue body missing required phrase: {phrase}")
    if "Allowed action: public GitHub commit and one new public GitHub issue only after validation." not in audit_text:
        errors.append("Audit missing allowed action boundary")
    for url in REQUIRED_URLS:
        if url not in doc_text:
            errors.append(f"Doc missing required URL: {url}")

    check_text("Doc", doc_text, errors)
    check_text("Issue body", body_text, errors)
    check_text("Audit", audit_text, errors)

    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        if payload.get("artifact") != "medical_ai_safety_field_kit_sfc005_synthetic_evidence_starter":
            errors.append("Unexpected artifact id")
        if payload.get("card_id") != "SFC005":
            errors.append("Unexpected card id")
        if payload.get("primary_goal") != "get one public objection that blocks synthetic evidence overclaim wording":
            errors.append("Unexpected primary goal")
        if len(payload.get("evidence_boundary_checks", [])) != 6:
            errors.append("Expected six evidence boundary checks")
        if len(payload.get("stop_rules", [])) != 7:
            errors.append("Expected seven stop rules")
        for flag in REQUIRED_FALSE_FLAGS:
            if payload.get(flag) is not False:
                errors.append(f"Expected false flag: {flag}")

    if errors:
        print("FAIL SFC005 synthetic evidence starter validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS SFC005 synthetic evidence starter validation")
    print(f"doc={DOC.relative_to(ROOT)}")
    print(f"issue_body={ISSUE_BODY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
