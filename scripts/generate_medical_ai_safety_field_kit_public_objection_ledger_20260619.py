#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_LEDGER_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_public_objection_ledger_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_ledger_issue149_comment_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_public_objection_ledger_public_action_audit_20260619.md"


ISSUE_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149"
PUBLIC_CALL = "docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md"
TARGET_INDEX = "docs/MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"
LEDGER_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_OBJECTION_LEDGER_20260619.md"


ledger_rows = [
    {
        "lane": "failure mode",
        "current_public_objections": 0,
        "accepted_comment_shape": "one synthetic failure mode that could break public trust language",
        "blocked_content": ["patient data", "private clinical example", "diagnosis advice", "treatment advice"],
    },
    {
        "lane": "Turkish wording risk",
        "current_public_objections": 0,
        "accepted_comment_shape": "one Turkish medical wording risk that could mislead a clinician, patient, or reviewer",
        "blocked_content": ["institution claim", "endorsement claim", "clinical proof claim"],
    },
    {
        "lane": "source support gap",
        "current_public_objections": 0,
        "accepted_comment_shape": "one claim that needs stronger source support before public use",
        "blocked_content": ["source truth certification", "score certification", "benchmark ranking"],
    },
    {
        "lane": "field readiness gate",
        "current_public_objections": 0,
        "accepted_comment_shape": "one gate that should block deployment style wording",
        "blocked_content": ["clinical validation", "clinical deployment", "regulatory compliance claim"],
    },
    {
        "lane": "benchmark misuse risk",
        "current_public_objections": 0,
        "accepted_comment_shape": "one way a score, benchmark, or leaderboard could be misread",
        "blocked_content": ["ranking claim", "model safety proof", "score guarantee"],
    },
    {
        "lane": "reviewer route suggestion",
        "current_public_objections": 0,
        "accepted_comment_shape": "one reviewer role or route suggestion without naming unsupported partners",
        "blocked_content": ["partner status", "institution approval", "official route access"],
    },
]


payload = {
    "artifact_id": "medical_ai_safety_field_kit_public_objection_ledger_20260619",
    "created_at_trt": "2026 06 19 20:05 TRT",
    "source_issue_number": 149,
    "source_issue_url": ISSUE_URL,
    "issue_state_checked": "OPEN",
    "issue_comment_count_at_build": 1,
    "public_call_doc": PUBLIC_CALL,
    "target_distribution_index_doc": TARGET_INDEX,
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "gmail_reply_state": "Prior Hacettepe health informatics acknowledgement only. No new substantive route owner reply.",
    "public_comments_from_external_reviewers": 0,
    "fake_reviewer_rows_allowed": False,
    "ledger_rows": ledger_rows,
    "reviewer_lanes": [row["lane"] for row in ledger_rows],
    "blocked_claims": [
        "patient data",
        "clinical validation",
        "clinical deployment",
        "diagnosis or treatment advice",
        "benchmark ranking",
        "score certification",
        "source truth certification",
        "partner status",
        "institution approval",
        "formal application",
        "payment",
        "terms acceptance",
        "endorsement",
    ],
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
    "release_published": False,
    "email_sent": False,
    "social_posted": False,
    "next_non_sending_action": "Add one issue 149 maintainer comment linking the objection ledger and asking for one objection by lane.",
}


doc = f"""# Medical AI Safety Field Kit Public Objection Ledger

Date: 2026 06 19

Status: public objection ledger for issue 149.

Issue state checked at build: open.

Issue comment count at build: 1.

Public front door:

1. {ISSUE_URL}

Companion artifacts:

1. {PUBLIC_CALL}
2. {TARGET_INDEX}

## Purpose

This ledger turns issue 149 from a broad public call into a concrete objection collection surface. The goal is to attract useful criticism, not to claim validation or approval.

## Ledger rows
"""

for index, row in enumerate(ledger_rows, start=1):
    doc += f"""
{index}. Lane: {row['lane']}

Current public objections: {row['current_public_objections']}

Accepted comment shape: {row['accepted_comment_shape']}

Blocked content: {', '.join(row['blocked_content'])}
"""

doc += f"""

## Comment rule

Leave one concrete objection in one lane:

1. Failure mode.
2. Turkish wording risk.
3. Source support gap.
4. Field readiness gate.
5. Benchmark misuse risk.
6. Reviewer route suggestion.

Keep examples synthetic and free of patient data.

## Non claims

This ledger is not clinical validation, clinical deployment, diagnosis advice, treatment advice, patient data work, model ranking, score certification, source truth certification, partner status, institution approval, formal application, payment, terms acceptance, or endorsement.

## Current truth state

No external reviewer objection has been recorded yet. No fake reviewer row is allowed. If public comments arrive, each row must point to the visible issue comment before it is counted.

## Public action boundary

No release is required for this ledger. No mail is sent. No social post is made. No application, TBYS action, PRODIS action, payment, terms acceptance, partner claim, institution claim, patient data, clinical validation, clinical deployment, ranking, score certification, or endorsement is made.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_public_objection_ledger
```
"""


issue_comment = f"""Maintainer note for issue 149:

Next step after the public call and Target Distribution Index: I am keeping a public objection ledger for this issue.

Use it to leave one concrete objection in one lane:

1. Failure mode.
2. Turkish wording risk.
3. Source support gap.
4. Field readiness gate.
5. Benchmark misuse risk.
6. Reviewer route suggestion.

The ledger is only a routing surface. It is not clinical validation, clinical deployment, diagnosis or treatment advice, patient data work, model ranking, score certification, source truth certification, partner status, institutional approval, formal application, payment, terms acceptance, or endorsement.

Artifact:

{LEDGER_URL}
"""


audit = """# Public Action Audit

Artifact: Medical AI Safety Field Kit Public Objection Ledger

Date: 2026 06 19

Gmail state: active medical AI outreach threads and targeted searches were checked before build. The only inbound item remains the prior Hacettepe health informatics acknowledgement. No new substantive route owner reply was found.

Issue state: issue 149 was checked as open. The issue had one maintainer comment at build time and no external reviewer objection rows were visible.

External material state: one issue comment body was prepared for the public ledger. No email, social post, application, release, or external repository action was performed by this artifact before validation.

Public action allowed after validation: repository commit and one issue 149 maintainer comment.

External actions not performed: no mail, no social post, no application, no TBYS, no PRODIS, no payment, no terms acceptance, no partner claim, no institution claim, no endorsement, no patient data, no clinical validation, no clinical deployment, no clinical advice, no ranking, and no score certification.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    write(DOC, doc)
    write(DATA, json.dumps(payload, ensure_ascii=False, indent=2))
    write(ISSUE_COMMENT, issue_comment)
    write(AUDIT, audit)


if __name__ == "__main__":
    main()
