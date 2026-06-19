#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MEDICAL_AI_SAFETY_FIELD_KIT_SEND_APPROVAL_PACKET_20260619.md"
DATA = ROOT / "docs" / "medical_ai_safety_field_kit_send_approval_packet_20260619.json"
ISSUE_COMMENT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_issue149_comment_20260619.md"
RELEASE_NOTES = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_release_notes_20260619.md"
PUBLIC_POST_SEED = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_public_post_seed_20260619.md"
AUDIT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_public_action_audit_20260619.md"
SOURCE_SUPPORT = ROOT / "outputs" / "medical_ai_safety_field_kit_send_approval_packet_manual_source_support_20260619.md"


ISSUE_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149"
INDEX_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_TARGET_DISTRIBUTION_INDEX_20260619.md"
PACKET_URL = "https://github.com/v0id-lab/medical-ai-failure-atlas/blob/main/docs/MEDICAL_AI_SAFETY_FIELD_KIT_SEND_APPROVAL_PACKET_20260619.md"


THREADS = [
    "19edcafe5c2dfa60",
    "19eda863ce89f083",
    "19edaa3a3868fd0f",
    "19edac07e13052fa",
    "19edb2e645ca1f6d",
    "19edb491af3d687b",
    "19edb64c4ae9fec6",
    "19edb8289b165cc0",
    "19edb9dc297ad804",
]


message_drafts = [
    {
        "draft_id": "SEND001",
        "target": "TUSEB and TUYZE route owner",
        "recipient_state": "prior messages sent to info at tuseb.gov.tr, no new reply found",
        "send_state": "not sent",
        "requires_goktug_clearance": True,
        "subject": "Medical AI Safety Field Kit route owner question",
        "body": """Sayin TUSEB ve TUYZE ekibi,

Ben Dr. Goktug Ozkan. Hasta verisi kullanmayan, klinik kullanim ya da klinik dogrulama iddiasi tasimayan bir Medical AI Safety Field Kit calismasini acik kaynak olarak gelistiriyorum.

Public inceleme yuzeyi burada:

https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149

Tek ricam sudur: Bu tur bir non patient data saglik yapay zekasi guvenlik hazirlik yuzeyi icin dogru ilk rota TUSEB, TUYZE ya da baska bir birim midir?

Bu mesaj basvuru, TBYS islemi, teklif, ortaklik, butce, resmi rol, hasta verisi, klinik kullanim ya da klinik dogrulama talebi degildir. Sadece dogru route owner bilgisini ogrenmek istiyorum.

Uygun kisi ya da ekip siz degilseniz, dogru yonlendirme yapabilirseniz memnun olurum.

Saygilarimla,

Dr. Goktug Ozkan""",
        "blocked_claims": [
            "application",
            "TBYS action",
            "proposal",
            "partnership",
            "budget",
            "official role",
            "patient data",
            "clinical use",
            "clinical validation",
        ],
    },
    {
        "draft_id": "SEND002",
        "target": "Hacettepe health informatics warm follow up",
        "recipient_state": "prior acknowledgement from Gozdem Dural, no substantive reply yet",
        "send_state": "not sent",
        "requires_goktug_clearance": True,
        "subject": "Kisa takip: Medical AI Safety Field Kit public review yuzeyi",
        "body": """Sayin Dr. Ogretim Uyesi Gozdem Dural,

Nazik yanitiniz icin tesekkur ederim.

Onceki mesajdaki acik kaynak calismayi tek bir public review yuzeyinde topladim:

https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149

Eger uygun gorurseniz, saglik bilisimi acisindan tek bir public itiraz ya da eksik guvenlik kapisi birakmaniz bile cok degerli olur.

Bu calisma Hacettepe destegi, kurumsal iliski, klinik kullanim, klinik dogrulama ya da hasta verisi iddiasi tasimamaktadir. Amac, saglik yapay zekasi projelerinde kaynak destegi, veri uygunlugu, insan degerlendirmesi ve kamuya acik iddia dili icin eksik riskleri erken yakalamaktir.

Saygilarimla,

Dr. Goktug Ozkan""",
        "blocked_claims": [
            "Hacettepe support",
            "institutional relationship",
            "clinical use",
            "clinical validation",
            "patient data",
            "endorsement",
        ],
    },
]


public_post_seed = """I am turning the Medical AI Safety Field Kit into a public review surface.

Need one concrete objection from clinicians, health informatics reviewers, hospital quality teams, Turkish medical language reviewers, source support reviewers, and open model maintainers.

Useful comments:

1. One missing failure mode.
2. One Turkish medical wording risk.
3. One source support gap.
4. One field readiness gate.
5. One way a benchmark or score could be misused.

No patient data. No clinical validation claim. No clinical deployment claim. No ranking.

Public call:

https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149
"""


payload = {
    "artifact_id": "medical_ai_safety_field_kit_send_approval_packet_20260619",
    "created_at_trt": "2026 06 19 19:50 TRT",
    "source_issue_number": 149,
    "source_issue_url": ISSUE_URL,
    "target_distribution_index_url": INDEX_URL,
    "checked_after_reading_baglam2": True,
    "checked_after_reading_trackers": True,
    "checked_gmail_before_build": True,
    "gmail_reply_state": "Prior Hacettepe health informatics acknowledgement only. No new substantive route owner reply.",
    "active_thread_ids_checked": THREADS,
    "targeted_search_count": 6,
    "message_drafts": message_drafts,
    "public_post_seed": public_post_seed,
    "emails_sent": False,
    "social_posted": False,
    "issue_comment_prepared_not_posted": True,
    "release_notes_prepared_not_published": True,
    "requires_goktug_clearance_before_send": True,
    "contains_patient_data": False,
    "claims_clinical_validation": False,
    "claims_clinical_deployment": False,
    "claims_diagnosis_or_treatment_advice": False,
    "claims_benchmark_ranking": False,
    "claims_score_certification": False,
    "claims_source_truth_certification": False,
    "claims_partner": False,
    "claims_institutional_approval": False,
    "claims_official_role": False,
    "claims_endorsement": False,
    "claims_formal_application": False,
    "claims_payment": False,
    "claims_terms_acceptance": False,
    "next_action": "Goktug may approve one exact draft for sending, or keep all drafts parked while issue 149 gathers public comments.",
}


doc = f"""# Medical AI Safety Field Kit Send Approval Packet

Date: 2026 06 19

Status: public approval packet. No message has been sent from this packet.

Purpose: move from passive public documentation to a concrete outreach decision surface while preserving safety boundaries.

Public front door:

1. {ISSUE_URL}
2. {INDEX_URL}

## Current reply state

Active medical AI outreach threads and targeted Gmail searches were checked before this build. The only inbound item remains the earlier Hacettepe health informatics acknowledgement. No new substantive route owner reply was found.

## Decision rule

Use this packet only after Goktug approves an exact draft. Do not send, post, tag, apply, submit, accept terms, claim partner status, claim institution status, claim public authority guidance, use patient data, or make clinical validation or deployment claims.

## Draft one: TUSEB and TUYZE route owner

Recipient state: prior messages went to the TUSEB address. No new reply was found.

Subject:

{message_drafts[0]["subject"]}

Body:

{message_drafts[0]["body"]}

Send state: not sent.

Clearance needed: Goktug must approve exact text and target before sending.

## Draft two: Hacettepe health informatics warm follow up

Recipient state: Gozdem Dural sent an acknowledgement. No substantive route owner reply has arrived.

Subject:

{message_drafts[1]["subject"]}

Body:

{message_drafts[1]["body"]}

Send state: not sent.

Clearance needed: Goktug must approve exact text and timing before sending.

## Public post seed

Status: prepared only. Not posted.

{public_post_seed}

## Use order

1. If Goktug wants institutional route clarity first, approve draft one.
2. If Goktug wants warm academic review first, approve draft two.
3. If Goktug wants public visibility without direct mail, approve the public post seed.
4. If no approval is given, keep all drafts parked and use issue 149 as the only live public surface.

## Source support

The source support note records official public pages checked for TUSEB, SBSGM, TEKNOFEST, Hacettepe, and the public repository issue.

## Boundary

No mail was sent. No social post was made. No application was submitted. No TBYS or PRODIS action was taken. No partner, institution, endorsement, official role, clinical validation, clinical deployment, patient data, diagnosis, treatment, ranking, score, payment, terms, or public authority guidance claim is made.

## Maintainer command

Run:

```bash
make medical_ai_safety_field_kit_send_approval_packet
```
"""


issue_comment = f"""Maintainer note for issue 149:

The target distribution work now has a send approval packet:

{PACKET_URL}

It contains two exact drafts and one public post seed.

Nothing in the packet has been sent or posted.

Useful review now:

1. Which draft is too broad.
2. Which safety boundary is missing.
3. Which route should not be contacted yet.
4. Which public reviewer role should be asked first.

Please keep examples synthetic and free of patient data.

Boundary: no clinical validation, deployment, ranking, endorsement, partner, institution, application, payment, terms, or public authority guidance claim.
"""


release_notes = f"""# Medical AI Safety Field Kit Send Approval Packet

Date: 2026 06 19

This release adds a public approval packet for the Medical AI Safety Field Kit outreach sprint.

It includes:

1. TUSEB and TUYZE route owner draft.
2. Hacettepe health informatics warm follow up draft.
3. Public post seed.
4. Source support note.
5. Public action audit.

No mail was sent. No social post was made. No application was submitted. No patient data, clinical validation, clinical deployment, ranking, partner, institution, endorsement, payment, or terms claim is made.

Public issue:

{ISSUE_URL}
"""


audit = """# Public Action Audit

Artifact: Medical AI Safety Field Kit Send Approval Packet

Date: 2026 06 19

Gmail state: active medical AI outreach threads and targeted searches were checked before build. The only inbound item remains the prior Hacettepe health informatics acknowledgement. No new substantive route owner reply was found.

External material state: two message drafts and one public post seed were prepared. None were sent or posted.

Source state: official TUSEB, SBSGM, TEKNOFEST, and Hacettepe pages were checked for route context. The public repository issue was checked as the intake surface.

Public action cleared after validation: repository commit only. Issue comment text and release note text are prepared but not posted or published from this packet.

External actions not performed: no mail, no social post, no application, no TBYS, no PRODIS, no payment, no terms acceptance, no partner claim, no institution claim, no official role claim, no endorsement, no patient data, no clinical validation, no clinical deployment, no clinical advice, no ranking, and no score certification.

Open decision: Goktug must approve exact target and text before any draft is sent or posted.
"""


source_support = """# Manual Source Support

Artifact: Medical AI Safety Field Kit Send Approval Packet

Date: 2026 06 19

Checked source claims:

1. TUSEB announced the 2026 A4 UM Uzman call for specialists continuing compulsory public service.

Source: https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616

2. TUSEB A group project support page routes active call details through TBYS.

Source: https://proje-destek.tuseb.gov.tr/a-grubu-proje-destekleri

3. SBSGM has a Yapay Zeka ve Yenilikci Teknolojiler Daire Baskanligi page. The page lists duties including identifying AI improvable processes, following AI developments, stakeholder collaboration, interoperability, and training material preparation.

Source: https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html

4. TEKNOFEST Health AI competition pages show the health AI competition surface and related public result links.

Source: https://www.teknofest.org/tr/yarismalar/saglikta-yapay-zeka-yarismasi/

5. Hacettepe Bilisim Enstitusu pages show a public health informatics program surface.

Source: https://bilisim.hacettepe.edu.tr/tr/saglik_bilisimi_tezli_yl_programi-277

6. Issue 149 is the public intake surface for the Medical AI Safety Field Kit.

Source: https://github.com/v0id-lab/medical-ai-failure-atlas/issues/149

Support limit: source existence and visible page claims were checked. This does not create public authority guidance, endorsement, review, partnership, route access, application status, clinical validation, or deployment readiness.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    write(DOC, doc)
    write(DATA, json.dumps(payload, ensure_ascii=False, indent=2))
    write(ISSUE_COMMENT, issue_comment)
    write(RELEASE_NOTES, release_notes)
    write(PUBLIC_POST_SEED, public_post_seed)
    write(AUDIT, audit)
    write(SOURCE_SUPPORT, source_support)


if __name__ == "__main__":
    main()
