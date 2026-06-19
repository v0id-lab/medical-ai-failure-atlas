#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CHAI_GOVERNANCE_COMPANION_NOTE_20260619.md"
DATA = ROOT / "docs" / "chai_governance_companion_note_20260619.json"

REQUIRED_DOC_PHRASES = [
    "CHAI Governance Companion Note",
    "public governance companion for health AI safety infrastructure",
    "not a CHAI affiliation claim",
    "not a CHAI membership claim",
    "not a CHAI partner claim",
    "not CHAI endorsement",
    "not Joint Commission endorsement",
    "not certification",
    "not legal advice",
    "not regulatory evidence",
    "not clinical validation",
    "not clinical deployment",
    "not patient data use",
    "not payment",
    "not terms acceptance",
    "more than 150 health AI leaders",
    "eight elements of responsible AI use",
    "four core domains",
    "five subdomains under organizational processes",
    "ethics and quality assurance",
    "from use case identification and product development to deployment and monitoring",
    "AI policy",
    "Organizational structures",
    "Organizational resources",
    "Responsible AI lifecycle management and use",
    "Risk and impact assessment",
    "Responsible data management and use",
    "Third party management",
    "Education, training, and feedback",
    "Public transparency and no ranking reporting",
    "make chai_governance_companion_note",
]

REQUIRED_SOURCE_URLS = {
    "https://www.chai.org/",
    "https://www.chai.org/news/coalition-for-health-ai-chai-releases-comprehensive-governance-playbooks-to",
    "https://www.chai.org/workgroup/cross-cutting/ai-governance",
    "https://www.chai.org/workgroup/responsible-ai/responsible-ai-guide-raig-and-raig-executive-summary",
    "https://www.chai.org/blog/chai-releases-draft-responsible-health-ai-framework-for-public-comment",
}

REQUIRED_FLAGS = {
    "contains_patient_data": False,
    "contains_private_operational_data": False,
    "claims_chai_affiliation": False,
    "claims_chai_membership": False,
    "claims_chai_partner": False,
    "claims_chai_endorsement": False,
    "claims_joint_commission_endorsement": False,
    "claims_certification": False,
    "claims_legal_advice": False,
    "claims_regulatory_evidence": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_patient_data_use": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "claims_model_ranking": False,
    "claims_score_certification": False,
    "claims_procurement_evidence": False,
    "claims_institutional_adoption": False,
}

FORBIDDEN_PHRASES = [
    "chai affiliation confirmed",
    "chai membership confirmed",
    "chai partner confirmed",
    "endorsed by chai",
    "endorsed by joint commission",
    "certification complete",
    "legal advice provided",
    "regulatory evidence complete",
    "clinical validation complete",
    "clinical deployment ready",
    "patient data used",
    "payment completed",
    "terms accepted",
    "model ranking report",
    "score certification complete",
    "procurement evidence complete",
    "institutional adoption confirmed",
]

REQUIRED_LANES = {
    "AI policy",
    "Organizational structures",
    "Organizational resources",
    "Responsible AI lifecycle management and use",
    "Risk and impact assessment",
    "Responsible data management and use",
    "Third party management",
    "Education training and feedback",
    "Public transparency and no ranking reporting",
}


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
        errors.append("Source URL set does not match required CHAI source set")
    lanes = payload.get("governance_lanes", [])
    if len(lanes) != 9:
        errors.append("Expected nine governance lanes")
    found_lanes = {row.get("lane") for row in lanes}
    missing = sorted(REQUIRED_LANES - found_lanes)
    if missing:
        errors.append(f"Missing lanes: {', '.join(missing)}")
    for row in lanes:
        for field in ["public_artifact_question", "evidence_to_prepare", "blocked_claim"]:
            if not row.get(field):
                errors.append(f"{row.get('lane')}: missing {field}")

    if errors:
        print("FAIL CHAI governance companion note validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS CHAI governance companion note validation")
    print(f"markdown={DOC.relative_to(ROOT)}")
    print(f"json={DATA.relative_to(ROOT)}")
    print(f"governance_lanes={len(lanes)}")
    print(f"source_anchors={len(urls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
