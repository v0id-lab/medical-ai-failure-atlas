# TÜSEB A4 UM Private Decision Checklist

Date: 2026 06 19

Status: public private decision checklist for a possible TÜSEB A4 UM aligned medical AI safety route before the 30 June pre application cutoff, not an application.

Purpose: make the private go or no go decision concrete without exposing private answers. The public artifact lists the evidence locks that must be true before any TBYS action, formal application, institution naming, budget entry, patient data step, clinical validation claim, or partner language can be considered.

This checklist is not a TÜSEB application, not a TBYS submission, not a TÜYZE proposal, not a university application, not a ministry application, not a partner claim, not institutional approval, not budget approval, not payment, not terms acceptance, not patient data access, not ethics approval, not clinical validation, not clinical deployment, not model ranking, not score certification, and not endorsement.

## Live source signals checked on 2026 06 19

### PDC001: TÜSEB A4 UM official notice

Official source: https://www.tuseb.gov.tr/haberler/tuseb-2026-a4-um-uzman-mecburi-hizmet-grubuna-yonelik-proje-cagrisi-acildi-20260616

Checked fact: TÜSEB published the 2026 A4 UM expert compulsory service call notice on 16 June 2026. The notice states that the call supports short term projects led by medical branch specialists who are still fulfilling compulsory state service after specialty training.

Decision use: public source confirms why a private eligibility check matters. It does not confirm Goktug eligibility.

### PDC002: TÜSEB A group call document

Official source: https://files.tuseb.gov.tr/tuseb/files/dokumanlar/tuseb-2026projecagrilari-agrubu.pdf

Checked fact: the A group call document lists A4 UM pre application as 15 June to 30 June, pre application result notification as 10 July, full application as 13 July to 14 August, and result notification as 16 September.

Decision use: public source confirms the decision window. It does not authorize submission.

### PDC003: TÜSEB A group project support surface

Official source: https://proje-destek.tuseb.gov.tr/a-grubu-proje-destekleri

Checked fact: TÜSEB maintains a public A group project support surface, while the A4 UM notice points detailed action toward TBYS.

Decision use: public preparation can continue, but TBYS action requires verified private account and authority state.

## Private answer states

Use only these public neutral states:

1. Yes privately verified.
2. No.
3. Unknown.
4. Not needed.
5. Stop.

Unknown means no external action.

## Private checklist rows

### PDC101: personal eligibility

Private question: am I personally in the A4 UM target group today.

Evidence needed: private employment or service status evidence.

Public allowed wording: eligibility is not publicly claimed.

Stop condition: if not verified before 30 June, do not submit.

### PDC102: compulsory service status

Private question: am I still fulfilling compulsory state service after specialty training.

Evidence needed: private status evidence.

Public allowed wording: the public call is eligibility gated.

Stop condition: if false or unknown, do not submit.

### PDC103: current institution naming authority

Private question: can the current institution be named in a formal route.

Evidence needed: explicit institutional permission or route instruction.

Public allowed wording: no institution is named as applicant, partner, host, or supporter.

Stop condition: if authority is missing, do not name the institution.

### PDC104: TBYS account and role

Private question: do I have the correct TBYS account and role for this call.

Evidence needed: private TBYS access state and role state.

Public allowed wording: no TBYS action is claimed.

Stop condition: if role is wrong or unknown, do not submit.

### PDC105: route owner reply

Private question: has TÜSEB, TÜYZE, or an official route owner answered the route fit question.

Evidence needed: email or official written answer.

Public allowed wording: no route owner reply has been received unless it is actually present.

Stop condition: if no answer and route fit remains uncertain, do not imply official fit.

### PDC106: non patient data scope

Private question: can the concept remain fully non patient data.

Evidence needed: concept scope that uses public, synthetic, or non patient materials only.

Public allowed wording: no patient data is used or requested.

Stop condition: if patient data becomes necessary, stop until ethics, data, and authority routes are real.

### PDC107: clinical boundary

Private question: does the concept avoid clinical deployment and clinical validation claims.

Evidence needed: text that limits the work to readiness, evaluation, source support, literacy, and review protocol.

Public allowed wording: this is a readiness and review concept only.

Stop condition: if deployment or validation language appears, remove it before any public or formal action.

### PDC108: budget authority

Private question: can any budget entry be reviewed by an authorized route before formal action.

Evidence needed: private budget review route.

Public allowed wording: no budget is approved.

Stop condition: if budget authority is missing, do not enter or approve budget.

### PDC109: terms and submission authority

Private question: who can accept terms or submit in TBYS.

Evidence needed: explicit private authority.

Public allowed wording: no terms are accepted and no submission is made.

Stop condition: if authority is not explicit, do not accept terms or submit.

### PDC110: ethics route

Private question: is ethics approval not needed because no patient data and no clinical action are used, or is an ethics route needed.

Evidence needed: private ethics route decision.

Public allowed wording: no ethics approval is claimed.

Stop condition: if ethics status is unclear, do not imply ethics clearance.

### PDC111: minimum concept fit

Private question: can the work fit as medical AI safety readiness rather than a software deployment or procurement claim.

Evidence needed: concept text that stays in evaluation, source support, literacy, data quality, and human review.

Public allowed wording: this is a readiness checklist and open source safety package.

Stop condition: if the concept becomes procurement, deployment, or product certification, stop.

### PDC112: final private decision

Private question: is the answer go, conditional wait, or no go.

Evidence needed: every prior row has a private answer.

Public allowed wording: current state is private decision pending.

Stop condition: if any required row is unknown or no, do not submit.

## Decision rule

Outcome go requires yes privately verified for PDC101, PDC102, PDC103, PDC104, PDC106, PDC107, PDC108, PDC109, PDC110, and PDC111. PDC105 may be yes or conditional wait only if official call logic and private authority are strong enough.

Outcome no go applies if any required private row is no or unknown before 30 June.

Outcome conditional wait applies only if private eligibility, institution authority, TBYS role, non patient data scope, clinical boundary, budget authority, terms authority, ethics route, and concept fit are verified, but route owner reply is still pending.

## Current decision

Current state is private decision pending, not TBYS action.

Reason: the call is live and time sensitive, but Gmail has no TÜSEB route owner reply, personal eligibility is not publicly verified, institutional authority is not verified, and no formal TBYS decision exists.

## Runnable check

```bash
make tuseb_a4_um_private_decision_checklist
```
