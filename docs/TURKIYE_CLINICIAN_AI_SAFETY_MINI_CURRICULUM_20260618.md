# Türkiye Clinician AI Safety Mini Curriculum

Date: 2026 06 18

Status: public 30 minute clinician AI safety mini curriculum, not an official course, not a clinical validation, and not a deployment package.

Purpose: turn the Türkiye field readiness dashboard into a concrete education artifact that a medical faculty, simulation center, health informatics unit, or health AI education route owner can review without patient data, clinical deployment, formal application, or partner claim.

This artifact is designed for route owner review only. It does not claim TÜBİTAK, TÜSEB, TÜYZE, university, hospital, or company approval.

## Live opportunity fit checked on 2026 06 18

TÜBİTAK source:
https://tubitak.gov.tr/tr/duyuru/1711-yapay-zeka-ekosistem-2026-yili-cagrisi-acildi

Observed fit: TÜBİTAK states that the 1711 Yapay Zekâ Ekosistem 2026 call opened on 15 June 2026. The official page lists five priority areas and includes Akıllı Eğitim Teknolojileri. The same page states that applications are received through PRODİS from 15 June 2026 to 18 September 2026 at 25:59 UTC+3, with pre registration due by 14 September 2026 at 17:30.

Constraint: the official TÜBİTAK page does not list a direct health AI priority area. Therefore this curriculum can only support a smart education route discussion unless a real provider, demand side owner, and eligible consortium route appear.

TÜSEB source:
https://www.tuseb.gov.tr/haberler/2026-yili-tuseb-proje-desteklerine-iliskin-cagri-ayrintilari-yayimlandi-20260127

Observed fit: TÜSEB published 2026 project support call details and says applications are received through TBYS according to the call calendar. The page lists academic and producing health support groups.

Constraint: this artifact is not a TÜSEB proposal. It can support a later proposal readiness discussion only after role, eligibility, scope, and institutional route are verified.

TÜYZE source:
https://tuyze.tuseb.gov.tr/

Observed fit: TÜYZE publicly lists health AI seminars with Marmara University Faculty of Medicine and TÜSEB TÜYZE between 08 April and 20 May 2026. TÜYZE also visibly maintains health AI education and activity surfaces.

Constraint: this artifact does not claim TÜYZE review, support, or partnership.

## Learning goal

By the end of 30 minutes, a clinician or medical education reviewer should be able to separate four things:

1. A medical AI answer that needs source support review.
2. A medical AI answer that needs clinician review before any use.
3. A medical AI safety claim that is only public build language.
4. A medical AI claim that would require real clinical validation before external use.

## Audience

Primary audience: physicians, health professions educators, health informatics students, simulation educators, medical ethics reviewers, and project teams preparing early health AI education work.

Not intended audience: patients, autonomous diagnosis tools, live clinical decision systems, billing workflows, or production hospital deployments.

## Required materials

1. One synthetic medical AI answer with no patient data.
2. One short source support worksheet.
3. One failure mode checklist.
4. One public claim hygiene checklist.
5. One facilitator note that repeats the truth boundary.

## 30 minute flow

### Minute 0 to 3: boundary opening

Facilitator says:

This is a safety literacy exercise. It is not clinical advice, not clinical validation, not model approval, and not deployment readiness. We use only synthetic examples and public wording.

Participant action:

Mark any claim that sounds like validation, approval, deployment, or institutional endorsement.

### Minute 3 to 8: source support review

Facilitator task:

Show a synthetic AI answer that cites a plausible source but gives an unsupported recommendation.

Participant action:

Answer three questions:

1. Does the source exist?
2. Does the source support the exact claim?
3. Is the answer safe to reuse without clinician review?

Expected answer:

The answer is not safe to reuse if source support has not been checked and clinician review has not happened.

### Minute 8 to 14: failure mode capture

Facilitator task:

Show three failure mode labels:

1. unsupported source claim
2. missing uncertainty
3. inappropriate escalation language

Participant action:

Assign one label to the synthetic answer and write a one sentence reason.

Expected answer:

At least one failure mode must be written as a review note, not as a model score or leaderboard rank.

### Minute 14 to 20: no ranking safety review

Facilitator task:

Explain that this workflow does not rank models. It records whether a specific answer can be reviewed, whether its source support is traceable, and whether public claims are safe.

Participant action:

Rewrite one unsafe sentence into a bounded sentence.

Unsafe sentence:

This model is ready for Turkish hospitals.

Bounded sentence:

This public example has no clinical validation and should be treated as a source support review exercise only.

### Minute 20 to 26: route owner decision

Facilitator task:

Ask which route would be needed before any larger action:

1. medical faculty education route
2. hospital quality or digital medicine route
3. ethics route
4. data stewardship route
5. TÜBİTAK smart education route
6. TÜSEB or TÜYZE health AI education route

Participant action:

Select one route and state what evidence is missing.

Expected answer:

The missing evidence must be route owner review, partner commitment, eligible scope, or clinical validation evidence. It must not be replaced by public GitHub activity.

### Minute 26 to 30: closeout

Facilitator task:

Ask the participant to complete this sentence:

Before this can be used outside a classroom or review exercise, the next required gate is ...

Expected safe gates:

1. route owner review
2. ethics review if human subjects or institutional activity appears
3. data governance review if real data appears
4. clinical validation if any clinical performance claim appears
5. legal or administrative review if a formal application or partnership appears

## Facilitator scoring

This is not a model score. It is a readiness screen.

Pass condition:

1. Participant identifies that no patient data is present.
2. Participant does not treat source presence as source support.
3. Participant separates public build language from clinical validation.
4. Participant names the missing route owner gate.
5. Participant avoids ranking the model.

Fail condition:

1. Participant says the example has clinical validation.
2. Participant treats a citation as enough evidence without checking claim support.
3. Participant recommends clinical use.
4. Participant claims institutional approval.
5. Participant asks for patient data during the exercise.

## Reuse rule

This curriculum can be reused as a public education review artifact. It cannot be described as an approved course, accredited course, official module, clinical training, hospital protocol, model evaluation certificate, partner deliverable, or clinical validation package.

## Public action rule

Use this artifact when no route owner reply exists and a visible education artifact is more useful than repeating the same e mail. If a route owner replies, send a reply specific fit note before using this curriculum.

## Truth boundary

No application has been submitted. No proposal has been submitted. No congress submission has been made. No partner commitment exists. No budget exists. No payment was made. No terms were accepted. No official role exists. No endorsement exists. No patient data was used. No clinical deployment exists. No clinical validation exists.

## Runnable check

```bash
make turkiye_clinician_ai_safety_mini_curriculum
```
