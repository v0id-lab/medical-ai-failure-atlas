#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_target_distribution_index_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_issue149_comment_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_public_post_seed_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_public_action_audit_20260619.md"
SOURCE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_manual_source_support_20260619.md"


REQUIRED_FILES = [DOC, DATA, ISSUE_COMMENT, RELEASE_NOTES, PUBLIC_POST_SEED, AUDIT, SOURCE_SUPPORT]

REQUIRED_DOC_PHRASES = [
    "Medical AI Safety Field Kit Target Distribution Index",
    "public distribution layer for issue 149",
    "Use issue 149 as the single public link",
    "Target one: TUSEB and TUYZE route owner",
    "Target two: SBSGM Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı",
    "Target three: TEKNOFEST Sağlıkta Yapay Zeka ecosystem",
    "Target four: Hacettepe health informatics",
    "Target five: Open medical AI maintainer and reviewer community",
    "Seventy two hour push",
    "Public post seed one",
    "Sources checked",
    "No mail was sent",
    "make medical_ai_safety_field_kit_target_distribution_index",
]

REQUIRED_COMMENT_PHRASES = [
    "Maintainer note for issue 149",
    "single public intake point",
    "target distribution index",
    "One missing failure mode",
    "One Turkish medical wording risk",
    "One source support gap",
    "One field readiness gate",
    "benchmark or score could be misused",
    "Please keep examples synthetic and free of patient data",
]

FORBIDDEN_PHRASES = [
    "patient data used",
    "real patient",
    "clinically validated",
    "clinical deployment ready",
    "diagnosis advice",
    "treatment advice",
    "benchmark ranking confirmed",
    "score certified",
    "source truth certified",
    "partner confirmed",
    "institution approved",
    "endorsed by",
    "formal application submitted",
    "payment completed",
    "terms accepted",
    "official guidance",
    "compliance certified",
]

FORBIDDEN_INTERNAL_LABELS = [
    "de" + "AI",
    "human" + "ized",
    "AI " + "detector",
    "submit" + "_audit",
]

REQUIRED_THREADS = {
    "19edcafe5c2dfa60",
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
}

REQUIRED_FLAGS = {
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "contains_patient_data": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_diagnosis_or_treatment_advice": False,
    "claims_benchmark_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_endorsement": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "issue_comment_safe_after_audit": True,
}


def text_without_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)


def add_text_checks(errors: list[str], label: str, text: str) -> None:
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains forbidden phrase: {phrase}")
    for phrase in FORBIDDEN_INTERNAL_LABELS:
        if phrase.lower() in lower_text:
            errors.append(f"{label} contains internal process label: {phrase}")
    if "-" in text_without_urls(text):
        errors.append(f"{label} contains non URL hyphen character")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing artifact: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    comment_text = ISSUE_COMMENT.read_text(encoding="utf-8") if ISSUE_COMMENT.exists() else ""
    release_text = RELEASE_NOTES.read_text(encoding="utf-8") if RELEASE_NOTES.exists() else ""
    post_text = PUBLIC_POST_SEED.read_text(encoding="utf-8") if PUBLIC_POST_SEED.exists() else ""
    audit_text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""
    source_support_text = SOURCE_SUPPORT.read_text(encoding="utf-8") if SOURCE_SUPPORT.exists() else ""

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase.lower() not in doc_text.lower():
            errors.append(f"Doc missing required phrase: {phrase}")
    for phrase in REQUIRED_COMMENT_PHRASES:
        if phrase.lower() not in comment_text.lower():
            errors.append(f"Issue comment missing required phrase: {phrase}")

    for label, text in [
        ("Doc", doc_text),
        ("Issue comment", comment_text),
        ("Release notes", release_text),
        ("Public post seed", post_text),
        ("Audit", audit_text),
        ("Manual source support", source_support_text),
    ]:
        add_text_checks(errors, label, text)

    for phrase in [
        "SBSGM has a Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı page",
        "TUSEB announced the 2026 A4 UM Uzman call",
        "TEKNOFEST Health AI competition pages show",
        "Hacettepe Bilişim Enstitüsü pages show",
        "Support limit",
    ]:
        if phrase.lower() not in source_support_text.lower():
            errors.append(f"Manual source support missing phrase: {phrase}")

    payload = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for key, expected in REQUIRED_FLAGS.items():
        if payload.get(key) is not expected:
            errors.append(f"JSON flag {key} expected {expected}")

    if payload.get("source_issue_number") != 149:
        errors.append("source issue must be 149")
    if payload.get("target_count") != 5 or len(payload.get("targets", [])) != 5:
        errors.append("Expected five target routes")
    if set(payload.get("active_thread_ids_checked", [])) != REQUIRED_THREADS:
        errors.append("Active thread ids checked do not match required set")
    if payload.get("targeted_search_count") != 5:
        errors.append("Expected five targeted Gmail searches")
    if "No new substantive route owner reply" not in payload.get("gmail_reply_state", ""):
        errors.append("Gmail reply state must state no new substantive route owner reply")

    required_target_fields = {
        "target_id",
        "name",
        "route_type",
        "status",
        "why_this_target",
        "source_basis",
        "source_urls",
        "issue149_use",
        "safe_ask",
        "do_not_claim",
        "send_state",
        "clearance_needed",
    }
    target_ids = set()
    for target in payload.get("targets", []):
        missing = required_target_fields - set(target)
        if missing:
            errors.append(f"Target missing fields: {sorted(missing)}")
        target_ids.add(target.get("target_id"))
        if not target.get("do_not_claim"):
            errors.append(f"Target {target.get('target_id')} lacks blocked claim list")
        if not target.get("source_urls"):
            errors.append(f"Target {target.get('target_id')} lacks source urls")
    if target_ids != {"TD001", "TD002", "TD003", "TD004", "TD005"}:
        errors.append("Target ids mismatch")

    if "public repository commit" not in payload.get("permitted_public_actions", []):
        errors.append("Public repository commit must be permitted")
    if "issue 149 maintainer comment" not in payload.get("permitted_public_actions", []):
        errors.append("Issue 149 maintainer comment must be permitted")

    if errors:
        print("FAIL Medical AI Safety Field Kit target distribution index validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS Medical AI Safety Field Kit target distribution index validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"issue_comment={ISSUE_COMMENT.relative_to(ROOT)}")
    print(f"release_notes={RELEASE_NOTES.relative_to(ROOT)}")
    print(f"public_post_seed={PUBLIC_POST_SEED.relative_to(ROOT)}")
    print(f"audit={AUDIT.relative_to(ROOT)}")
    print(f"manual_source_support={SOURCE_SUPPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
