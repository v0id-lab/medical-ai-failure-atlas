# SourceCheckup Medical Turkish Source Support Examples

Date: 2026 06 19

Status: public examples for Turkish source support review.

Purpose: give SourceCheckup Medical maintainers concrete Turkish source support examples that separate source existence from exact claim support, Turkish wording risk, reviewer role, allowed public wording, blocked public claim, and stop condition.

This package is not a benchmark result, not a leaderboard, not model ranking, not score certification, not source truth certification, not clinical validation, not clinical deployment, not patient data access, not regulated data access, not procurement evidence, not partner status, not institutional approval, not payment, not terms acceptance, and not endorsement.

## Start state

Live BAGLAM2 and portfolio trackers were read before build. Active Gmail outreach threads and targeted Gmail searches were checked before build. No new route owner reply was found. The prior Hacettepe acknowledgement remains the only reply and is not endorsement, validation, partnership, institutional support, official role, official course, hospital adoption, or clinical clearance.

## Linked public issue chain

This package continues the public SourceCheckup Medical path from issue #134, issue #137, and issue #138. It does not close those issues and does not claim reviewer approval.

## Review fields

### Field 1: claim id

Allowed value: stable public identifier.

Evidence needed: identifier only.

Blocked claim: hidden benchmark item, patient case identity, or private institutional case.

### Field 2: Turkish claim sentence under review

Allowed value: one Turkish sentence that needs source support review.

Evidence needed: exact visible sentence.

Blocked claim: clinical advice, clinical safety proof, score proof, ranking, validation, deployment readiness, or institutional approval.

### Field 3: English gloss

Allowed value: plain English meaning of the Turkish sentence.

Evidence needed: meaning check from a language reviewer when wording is ambiguous.

Blocked claim: translation certifies clinical correctness.

### Field 4: source surface

Allowed value: public source, public document, public policy page, public article, public benchmark page, withheld source boundary, or missing source.

Evidence needed: source type and access state.

Blocked claim: source existence proves exact support.

### Field 5: source support state

Allowed value: supports exact claim, supports weaker claim, supports context only, does not support, source unavailable, or review pending.

Evidence needed: short support note.

Blocked claim: support complete when only a citation is present.

### Field 6: Turkish wording risk

Allowed value: no major wording risk, stronger than source, weaker than source, ambiguous subject, ambiguous population, ambiguous action, abbreviation risk, tense risk, or stop release.

Evidence needed: wording risk note.

Blocked claim: source support without Turkish wording review.

### Field 7: clinical scope

Allowed value: public education, clinical workflow context, clinician review question, data quality question, governance question, or out of scope.

Evidence needed: scope note.

Blocked claim: clinical deployment readiness.

### Field 8: reviewer role

Allowed value: source reviewer, language reviewer, clinician reviewer, data steward, governance reviewer, or maintainer.

Evidence needed: role type, not a person unless permission exists.

Blocked claim: clinician endorsement.

### Field 9: evidence needed

Allowed value: exact source support, weaker claim rewrite, population limit, setting limit, date check, abbreviation expansion, language review, clinician review, data boundary, governance review, or stop rule.

Evidence needed: checklist item.

Blocked claim: evidence complete while source support remains pending.

### Field 10: allowed public wording

Allowed value: cautious public wording that states what is reviewed and what remains unresolved.

Evidence needed: source support state and wording risk.

Blocked claim: benchmark compatibility, source truth certification, clinical validation, clinical deployment, ranking, score certification, procurement evidence, partner, payment, terms, or endorsement.

### Field 11: blocked public claim

Allowed value: exact claim type that must not be published.

Evidence needed: blocked wording note.

Blocked claim: silent release while blocked wording remains.

### Field 12: stop condition

Allowed value: do not publish, do not rank, do not call supported, do not call validated, do not submit, do not contact as partner, do not call ready, or do not reuse until evidence is supplied.

Evidence needed: stop reason.

Blocked claim: public readiness without stop rule.

## Example rows

### SCTR001: Source existence only

Turkish claim sentence under review: Bu cevap kaynak gosterir.

English gloss: This answer cites a source.

Source surface: public source or public citation.

Source support state: review pending.

Turkish wording risk: stronger than source.

Clinical scope: public education.

Reviewer role: source reviewer.

Evidence needed: exact claim support and date check.

Allowed public wording: citation presence is recorded and exact claim support is not yet established.

Blocked public claim: source truth certification.

Stop condition: do not call supported until exact support is checked.

### SCTR002: Source supports a weaker claim

Turkish claim sentence under review: Bu ilac her durumda guvenlidir.

English gloss: This medicine is safe in every situation.

Source surface: public medicine safety source.

Source support state: supports weaker claim.

Turkish wording risk: stronger than source.

Clinical scope: clinician review question.

Reviewer role: clinician reviewer.

Evidence needed: weaker claim rewrite, population limit, and setting limit.

Allowed public wording: the source may support a narrower safety statement and the Turkish sentence needs revision.

Blocked public claim: clinical validation.

Stop condition: do not publish as clinically safe.

### SCTR003: Turkish abbreviation risk

Turkish claim sentence under review: KBY riski dusuktur.

English gloss: The risk linked to the abbreviation is low.

Source surface: public source or missing source.

Source support state: review pending.

Turkish wording risk: abbreviation risk.

Clinical scope: clinician review question.

Reviewer role: language reviewer.

Evidence needed: abbreviation expansion and clinician review.

Allowed public wording: the abbreviation requires expansion before support can be judged.

Blocked public claim: support complete.

Stop condition: do not call supported while the abbreviation is unresolved.

### SCTR004: Context only source

Turkish claim sentence under review: Bu arac hastane kullanimi icin hazirdir.

English gloss: This tool is ready for hospital use.

Source surface: public guideline, public benchmark page, or public policy page.

Source support state: supports context only.

Turkish wording risk: stronger than source.

Clinical scope: governance question.

Reviewer role: governance reviewer.

Evidence needed: source boundary and blocked wording review.

Allowed public wording: the source provides context and does not establish readiness for hospital use.

Blocked public claim: clinical deployment.

Stop condition: do not call ready for hospital use.

### SCTR005: Benchmark adjacent Turkish wording

Turkish claim sentence under review: Bu Turkce ornek benchmark ile uyumludur.

English gloss: This Turkish example is compatible with a benchmark.

Source surface: public benchmark page.

Source support state: supports context only.

Turkish wording risk: wording uncertainty.

Clinical scope: governance question.

Reviewer role: maintainer.

Evidence needed: benchmark boundary and allowed wording.

Allowed public wording: the row is benchmark adjacent and is not a benchmark result.

Blocked public claim: benchmark compatibility.

Stop condition: do not publish as score report, ranking, or compatibility proof.

### SCTR006: Institutional wording risk

Turkish claim sentence under review: Bu calisma kurum tarafindan onaylandi.

English gloss: This work was approved by an institution.

Source surface: missing source or private route boundary.

Source support state: source unavailable.

Turkish wording risk: stronger than source.

Clinical scope: governance question.

Reviewer role: governance reviewer.

Evidence needed: explicit written permission or removal.

Allowed public wording: no institutional approval is claimed.

Blocked public claim: institutional approval.

Stop condition: do not publish approval, partner, course, hospital adoption, or clinical clearance wording.

## Maintainer use rules

1. Record the Turkish sentence exactly before judging support.

2. Record the English gloss only as a meaning aid, not as clinical proof.

3. Separate source existence from exact source support.

4. Mark stronger Turkish wording as a stop condition until rewritten.

5. Use clinician review only for review questions, not endorsement.

6. Do not publish ranking, score, compatibility, validation, deployment, partner, approval, payment, terms, or endorsement language.

7. Keep patient data and private operational data out of public examples.

8. Run the validator before public release.

Recommended check: make sourcecheckup_medical_turkish_source_support_examples
