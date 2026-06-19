#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_target_distribution_index_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_issue149_comment_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_public_post_seed_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_public_action_audit_20260619.md"
SOURCE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_target_distribution_index_manual_source_support_20260619.md"


ISSUE_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149"
DOC_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"


TARGETS = [
    {
        "target_id": "TD001",
        "name": "TUSEB and TUYZE route owner",
        "route_type": "route owner clarification",
        "status": "reply pending from prior TUSEB address outreach",
        "why_this_target": "TUSEB A4 UM call is live and TUYZE is the natural health AI education and data surface, but no application or eligibility claim is safe.",
        "source_basis": [
            "TUSEB announced the 2026 A4 UM call on 16 June 2026.",
            "TUSEB A group page says active calls and details are accessed through TBYS.",
        ],
        "source_urls": [
            "https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616",
            "https://proje-destek.tuseb.gov.tr/a-grubu-proje-destekleri",
        ],
        "issue149_use": "Use issue 149 as the single public review link for a non patient data safety field kit.",
        "safe_ask": "Who is the right route owner for a non patient data medical AI safety field kit review surface.",
        "do_not_claim": [
            "application",
            "eligibility",
            "TUSEB support",
            "TUYZE support",
            "partner status",
            "clinical validation",
        ],
        "send_state": "draft only until Goktug approves exact follow up text",
        "clearance_needed": True,
    },
    {
        "target_id": "TD002",
        "name": "SBSGM Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı",
        "route_type": "public sector route clarification",
        "status": "live official unit verified",
        "why_this_target": "The official unit lists AI problem identification, solution work, AI developments, stakeholder collaboration, interoperability, and training material duties.",
        "source_basis": [
            "SBSGM page lists Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı among directorates.",
            "The unit duties include identifying AI improvable processes, following AI developments, stakeholder collaboration, interoperability, and training material preparation.",
        ],
        "source_urls": [
            "https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html",
            "https://sbsgm.saglik.gov.tr/TR-104215/mert-ozcan.html",
        ],
        "issue149_use": "Use issue 149 as a public field review surface, not as a ministry proposal.",
        "safe_ask": "Is there a generic public route where a non patient data health AI safety checklist can be reviewed or pointed to the right unit.",
        "do_not_claim": [
            "ministry collaboration",
            "public authority guidance",
            "approval",
            "route access",
            "deployment readiness",
        ],
        "send_state": "draft only until channel and text are approved",
        "clearance_needed": True,
    },
    {
        "target_id": "TD003",
        "name": "TEKNOFEST Sağlıkta Yapay Zeka ecosystem",
        "route_type": "public team safety awareness",
        "status": "application closed, visibility still useful",
        "why_this_target": "Official pages show the health AI competition and its aim, while the competition list marks Health AI application complete.",
        "source_basis": [
            "TEKNOFEST says the Health AI competition aims to support health problem solving and build knowledge and trained human capacity.",
            "The official competition list marks Sağlıkta Yapay Zeka Yarışması application complete.",
            "The February announcement listed 20 February 2026 as the application deadline.",
        ],
        "source_urls": [
            "https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/",
            "https://www.teknofest.org/tr/yarismalar/",
            "https://www.teknofest.org/tr/duyurular/saglikta-dijital-donusum-saglikta-yapay-zeka-yarismasi/",
        ],
        "issue149_use": "Use issue 149 as a public safety checklist for teams and mentors, not as a competition submission.",
        "safe_ask": "Teams can use the field kit to catch source support gaps, failure modes, wording risk, and no ranking misuse before public trust language.",
        "do_not_claim": [
            "competition participation",
            "late submission",
            "mentor relationship",
            "award relevance",
            "organizer approval",
        ],
        "send_state": "generic public post seed only, no tagged outreach without approval",
        "clearance_needed": False,
    },
    {
        "target_id": "TD004",
        "name": "Hacettepe health informatics",
        "route_type": "warm academic reviewer route",
        "status": "prior acknowledgement only",
        "why_this_target": "Hacettepe has a visible health informatics surface and an existing acknowledgement from the health informatics route.",
        "source_basis": [
            "Hacettepe Bilişim Enstitüsü lists Sağlık Bilişimi among its academic units.",
            "Hacettepe academic personnel page lists the Health Informatics department and public contact context.",
            "Gmail shows an acknowledgement that the prior note will be reviewed, but no substantive route owner reply yet.",
        ],
        "source_urls": [
            "https://bilisim.hacettepe.edu.tr/tr/akademik_personel-8",
            "https://bilisim.hacettepe.edu.tr/tr/saglik_bilisimi_tezli_yl_programi-277",
        ],
        "issue149_use": "Use issue 149 as the single public link if a short warm follow up is approved.",
        "safe_ask": "Would a health informatics reviewer be willing to leave one public objection or missing safety gate.",
        "do_not_claim": [
            "Hacettepe review",
            "Hacettepe support",
            "institutional relationship",
            "endorsement",
        ],
        "send_state": "warm follow up draft only until Goktug approves exact text",
        "clearance_needed": True,
    },
    {
        "target_id": "TD005",
        "name": "Open medical AI maintainer and reviewer community",
        "route_type": "global open source reviewer intake",
        "status": "safe public distribution lane",
        "why_this_target": "This lane needs no institutional claim and can ask maintainers to find benchmark misuse, source support gaps, and failure mode blind spots.",
        "source_basis": [
            "Public repository issue 149 is already the reviewer front door.",
            "No private route owner or institutional claim is needed for generic open source calls.",
        ],
        "source_urls": [
            ISSUE_URL,
        ],
        "issue149_use": "Use issue 149 as the only public intake point.",
        "safe_ask": "Leave one concrete failure mode, source support gap, Turkish wording risk, field readiness gate, or benchmark misuse concern.",
        "do_not_claim": [
            "maintainer endorsement",
            "ranking",
            "score certification",
            "clinical proof",
        ],
        "send_state": "safe as generic public post seed, no tags without approval",
        "clearance_needed": False,
    },
]


payload = {
    "artifact_id": "medical_ai_safety_field_kit_target_distribution_index_20260619",
    "created_at_trt": "2026 06 19 19:15 TRT",
    "source_issue_number": 149,
    "source_issue_url": ISSUE_URL,
    "public_call_doc": "docs/MEDICAL_AI_SAFETY_FIELD_KIT_PUBLIC_CALL_20260619.md",
    "distribution_mode": "targeted public distribution index",
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "gmail_reply_state": "Earlier Hacettepe health informatics acknowledgement only. No new substantive route owner reply.",
    "active_thread_ids_checked": [
        "19edcafe5c2dfa60",
        "19eda863ce89f083",
        "19edaa3a3868fd0f",
        "19edac07e13052fa",
        "19edb2e645ca1f6d",
        "19edb491af3d687b",
        "19edb64c4ae9fec6",
        "19edb8289b165cc0",
        "19edb9dc297ad804",
    ],
    "targeted_search_count": 5,
    "target_count": len(TARGETS),
    "targets": TARGETS,
    "reviewer_lanes": [
        "clinician reviewer",
        "health informatics reviewer",
        "hospital quality reviewer",
        "Turkish medical language reviewer",
        "source support reviewer",
        "open model maintainer",
    ],
    "permitted_public_actions": [
        "public repository commit",
        "issue 149 maintainer comment",
        "release note",
        "generic public post seed prepared but not posted",
    ],
    "blocked_claims": [
        "patient data",
        "clinical validation",
        "clinical deployment",
        "diagnosis or treatment advice",
        "benchmark ranking",
        "score certification",
        "source truth certification",
        "partner claim",
        "institution claim",
        "endorsement",
        "formal application",
        "payment",
        "terms acceptance",
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
    "issue_comment_safe_after_audit": True,
    "email_or_dm_requires_goktug_clearance": True,
    "social_post_requires_goktug_clearance": True,
    "next_action": "Use issue 149 comment as the public intake push, then prepare exact Goktug approved drafts for TUSEB TUYZE and Hacettepe.",
}


doc = f"""# Medical AI Safety Field Kit Target Distribution Index

Date: 2026 06 19

Status: public distribution layer for issue 149.

This index turns the Medical AI Safety Field Kit public call into a target aware distribution plan. The goal is not more internal polish. The goal is to route real reviewers toward one public intake point while blocking false trust language.

Primary public intake:

1. {ISSUE_URL}

## Distribution rule

Use issue 149 as the single public link. Each target gets one safe ask and one explicit boundary. Do not imply that a target has reviewed, approved, partnered, endorsed, funded, validated, deployed, or accepted anything.

## Target one: TUSEB and TUYZE route owner

Why now: TUSEB announced the 2026 A4 UM call on 16 June 2026, and TUSEB project support pages route active call details through TBYS. This is a live signal, but it is not an application clearance.

Safe ask: Who is the right route owner for a non patient data medical AI safety field kit review surface.

Use issue 149 as the public review link, not as an application, TBYS action, eligibility claim, budget request, or partnership request.

Do not claim TUSEB support, TUYZE support, eligibility, application status, official route access, clinical validation, or partner status.

Send state: draft only until Goktug approves exact follow up text.

## Target two: SBSGM Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı

Why now: The official SBSGM page lists this unit and describes duties that include identifying AI improvable processes, following AI developments, stakeholder collaboration, interoperability, and training material preparation.

Safe ask: Is there a generic public route where a non patient data health AI safety checklist can be reviewed or pointed to the right unit.

Use issue 149 as a public field review surface, not as a ministry proposal.

Do not claim ministry collaboration, public authority guidance, approval, route access, deployment readiness, or policy compliance.

Send state: draft only until channel and text are approved.

## Target three: TEKNOFEST Sağlıkta Yapay Zeka ecosystem

Why now: TEKNOFEST pages show the health AI competition and its aim, while the competition list marks Sağlıkta Yapay Zeka application complete. The opportunity is not a submission. The opportunity is safety awareness for teams and mentors.

Safe ask: Teams can use issue 149 to catch source support gaps, failure modes, wording risk, and no ranking misuse before public trust language.

Use issue 149 as a safety checklist link, not as a competition entry, late submission, organizer relationship, award claim, or mentor claim.

Send state: generic public post seed only, no tagged outreach without approval.

## Target four: Hacettepe health informatics

Why now: Hacettepe has a visible health informatics surface and an existing acknowledgement from the health informatics route. That acknowledgement is not a review or endorsement.

Safe ask: Would a health informatics reviewer be willing to leave one public objection or missing safety gate.

Use issue 149 as the single public link if a warm follow up is approved.

Do not claim Hacettepe review, Hacettepe support, institutional relationship, endorsement, or collaboration.

Send state: warm follow up draft only until Goktug approves exact text.

## Target five: Open medical AI maintainer and reviewer community

Why now: This lane needs no institutional claim and can ask maintainers to find benchmark misuse, source support gaps, Turkish wording risks, and failure mode blind spots.

Safe ask: Leave one concrete failure mode, source support gap, Turkish wording risk, field readiness gate, or benchmark misuse concern.

Use issue 149 as the only public intake point.

Do not claim maintainer endorsement, ranking, score certification, clinical proof, or source truth certification.

Send state: safe as generic public post seed, no tags without approval.

## Seventy two hour push

First six hours: publish this distribution index and add one maintainer comment to issue 149.

Hours six to twenty four: keep three public post seeds ready for manual social sharing by Goktug.

Hours twenty four to forty eight: if comments arrive, route each comment to one reviewer lane and one platform lane.

Hours forty eight to seventy two: if no comments arrive, add a second public call for one concrete objection and prepare exact follow up drafts for TUSEB TUYZE and Hacettepe.

## Public post seed one

I am opening the Medical AI Safety Field Kit for public attack.

Need reviewers from clinical practice, health informatics, hospital quality, Turkish medical language, source support, and open model maintenance.

Bring one concrete objection: a missing safety gate, a weak source support claim, a Turkish wording risk, or a failure mode.

No patient data. No clinical deployment claim. No model ranking.

Public call: {ISSUE_URL}

## Public post seed two

Türkiye needs health AI safety readiness work before trust language gets cheap.

I am using the Medical AI Safety Field Kit as a public review surface for Turkish medical wording risk, source support, data fitness, human review boundaries, and failure reporting.

If you can break one assumption, that is useful.

No patient data. No clinical validation claim. No institution claim.

Public call: {ISSUE_URL}

## Public post seed three

Open medical model evaluation needs more than scores.

I am building a Failure Atlas layer for unsafe precision, missing context, weak source support, patient facing wording risk, and review gate failures.

Looking for maintainers and reviewers who can point to one failure mode or one misuse risk.

No ranking. No score certification. No deployment claim.

Public call: {ISSUE_URL}

## Sources checked

1. SBSGM Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı page.
2. SBSGM Mert Özcan page.
3. TUSEB 2026 A4 UM call announcement.
4. TUSEB A group project support page.
5. TEKNOFEST Sağlıkta Yapay Zeka competition page.
6. TEKNOFEST competition list.
7. TEKNOFEST Health AI announcement with the 20 February 2026 application deadline.
8. Hacettepe Bilişim Enstitüsü health informatics public pages.

## Boundary

No mail was sent. No social post was made. No application was submitted. No TBYS or PRODİS action was taken. No partner, institution, endorsement, clinical validation, clinical deployment, patient data, diagnosis, treatment, ranking, score, payment, terms, or public authority guidance claim is made.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_target_distribution_index
```
"""


issue_comment = f"""Maintainer note for issue 149:

I am turning this issue into the single public intake point for the next distribution sprint.

The target distribution index is here:

{DOC_URL}

Useful comments now:

1. One missing failure mode.
2. One Turkish medical wording risk.
3. One source support gap.
4. One field readiness gate that should block public trust language.
5. One way a benchmark or score could be misused.

Please keep examples synthetic and free of patient data.

Boundary: this is not a clinical validation, deployment, ranking, endorsement, partner, institution, application, payment, or public authority guidance claim.
"""


release_notes = f"""# Medical AI Safety Field Kit Target Distribution Index

This release turns issue 149 from a broad public call into a target aware distribution sprint.

What changed:

1. Five target routes are mapped to one safe ask each.
2. TUSEB TUYZE, SBSGM AI unit, TEKNOFEST Health AI, Hacettepe health informatics, and open medical AI maintainers are separated by route risk.
3. Three public post seeds are prepared for Goktug review.
4. The issue 149 maintainer comment is prepared as the public intake push.
5. Every route blocks patient data, clinical validation, clinical deployment, ranking, score, partner, institution, endorsement, application, payment, and terms claims.

Primary public intake: {ISSUE_URL}
"""


post_seed = f"""Direct reviewer call:

I am opening the Medical AI Safety Field Kit for public attack.

Need reviewers from clinical practice, health informatics, hospital quality, Turkish medical language, source support, and open model maintenance.

Bring one concrete objection: a missing safety gate, a weak source support claim, a Turkish wording risk, or a failure mode.

No patient data. No clinical deployment claim. No model ranking.

Public call: {ISSUE_URL}

Türkiye readiness:

Türkiye needs health AI safety readiness work before trust language gets cheap.

I am using the Medical AI Safety Field Kit as a public review surface for Turkish medical wording risk, source support, data fitness, human review boundaries, and failure reporting.

If you can break one assumption, that is useful.

No patient data. No clinical validation claim. No institution claim.

Public call: {ISSUE_URL}

Open model angle:

Open medical model evaluation needs more than scores.

I am building a Failure Atlas layer for unsafe precision, missing context, weak source support, patient facing wording risk, and review gate failures.

Looking for maintainers and reviewers who can point to one failure mode or one misuse risk.

No ranking. No score certification. No deployment claim.

Public call: {ISSUE_URL}
"""


audit = """# Public Action Audit

Artifact: Medical AI Safety Field Kit Target Distribution Index

Date: 2026 06 19

Gmail state: active medical AI outreach threads and targeted searches were checked before build. The only inbound item remains the earlier Hacettepe health informatics acknowledgement. No new substantive route owner reply was found.

Source state: official SBSGM, TUSEB, TEKNOFEST, and Hacettepe pages were checked for target route basis.

Public action cleared after validation: repository commit, release, and issue 149 maintainer comment.

External actions not performed: no mail, no social post, no application, no TBYS, no PRODİS, no payment, no terms acceptance, no partner claim, no institution claim, no endorsement, no patient data, no clinical validation, no clinical deployment, no clinical advice, no ranking, and no score certification.

Open decisions: exact e mail or social sharing requires Goktug approval.
"""


source_support = """# Manual Source Support

Artifact: Medical AI Safety Field Kit Target Distribution Index

Date: 2026 06 19

Checked source claims:

1. SBSGM has a Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı page. The page lists duties including AI process identification, AI solution work, following AI developments, stakeholder collaboration, interoperability, and training material preparation.

Source: https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html

2. SBSGM Mert Özcan page states that as of February 2026 he also continues the Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı duty.

Source: https://sbsgm.saglik.gov.tr/TR-104215/mert-ozcan.html

3. TUSEB announced the 2026 A4 UM Uzman call on 16 June 2026 for specialists continuing compulsory public service.

Source: https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616

4. TUSEB A group project support page says active calls and call details are available through TBYS.

Source: https://proje-destek.tuseb.gov.tr/a-grubu-proje-destekleri

5. TEKNOFEST Health AI competition pages show the health AI competition surface. The competition list marks Sağlıkta Yapay Zeka as application complete. The announcement page listed 20 February 2026 as the application deadline.

Sources:

https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

https://www.teknofest.org/tr/yarismalar/

https://www.teknofest.org/tr/duyurular/saglikta-dijital-donusum-saglikta-yapay-zeka-yarismasi/

6. Hacettepe Bilişim Enstitüsü pages show a public health informatics surface and academic personnel context.

Sources:

https://bilisim.hacettepe.edu.tr/tr/akademik_personel-8

https://bilisim.hacettepe.edu.tr/tr/saglik_bilisimi_tezli_yl_programi-277

Support limit: source existence and visible page claims were checked. This does not create public authority guidance, endorsement, review, partnership, route access, application status, clinical validation, or deployment readiness.
"""


def main() -> None:
    DOC.write_text(doc, encoding="utf-8")
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ISSUE_COMMENT.write_text(issue_comment, encoding="utf-8")
    RELEASE_NOTES.write_text(release_notes, encoding="utf-8")
    PUBLIC_POST_SEED.write_text(post_seed, encoding="utf-8")
    AUDIT.write_text(audit, encoding="utf-8")
    SOURCE_SUPPORT.write_text(source_support, encoding="utf-8")
    print(f"wrote {DOC.relative_to(ROOT)}")
    print(f"wrote {DATA.relative_to(ROOT)}")
    print(f"wrote {ISSUE_COMMENT.relative_to(ROOT)}")
    print(f"wrote {RELEASE_NOTES.relative_to(ROOT)}")
    print(f"wrote {PUBLIC_POST_SEED.relative_to(ROOT)}")
    print(f"wrote {AUDIT.relative_to(ROOT)}")
    print(f"wrote {SOURCE_SUPPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
