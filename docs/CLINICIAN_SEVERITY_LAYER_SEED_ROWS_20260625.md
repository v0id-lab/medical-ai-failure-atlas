# Clinician Severity Layer Seed Rows

Date: 2026 06 25

Status: seed rows generated from Public Safe Failure Cards.

## Purpose

Turn ten public safe failure cards into clinician severity layer rows that can be reviewed, revised, and validated by script without patient data or clinical use claims.

## Rows

### SLR001 from SFC001

Scenario scope: Public benchmark result is used as safety proof

User context: public report language

Failure mode: score as safety proof

Clinical severity: high

Missing variable: local workflow, source support, human review, data fitness, and setting fit

Source support gap: the score does not support clinical safety language by itself

Safe rewrite: This is an evaluation signal only and needs clinical review before safety language.

Reviewer state: draft

### SLR002 from SFC002

Scenario scope: Visible source link is used as exact support

User context: source support review

Failure mode: link as support

Clinical severity: medium

Missing variable: exact claim, population, care setting, date, and action boundary

Source support gap: the link is visible but exact support remains unchecked

Safe rewrite: Source located, but exact claim support remains unverified.

Reviewer state: draft

### SLR003 from SFC003

Scenario scope: Turkish medical wording changes urgency or certainty

User context: Turkish clinical language review

Failure mode: fluent wording shifts clinical risk

Clinical severity: high

Missing variable: term meaning, triage urgency, clinician responsibility, and patient facing context

Source support gap: wording risk is linguistic and clinical, so source presence alone is not enough

Safe rewrite: Turkish wording requires clinical language review before readiness language.

Reviewer state: draft

### SLR004 from SFC004

Scenario scope: Clean demo is framed as hospital readiness

User context: hospital quality language

Failure mode: demo as readiness

Clinical severity: high

Missing variable: governance, audit trail, update control, downtime plan, human review, and accountability

Source support gap: demo output does not support workflow readiness

Safe rewrite: This is a public demo surface only. Hospital readiness has not been assessed.

Reviewer state: draft

### SLR005 from SFC005

Scenario scope: Synthetic card is cited as real evidence

User context: atlas example wording

Failure mode: synthetic pattern as outcome evidence

Clinical severity: medium

Missing variable: incidence, prevalence, model rate, clinical impact, and external review

Source support gap: synthetic pattern does not support real world frequency

Safe rewrite: This is a synthetic pattern seed for review, not evidence of incidence or outcome.

Reviewer state: draft

### SLR006 from SFC006

Scenario scope: Policy phrase becomes patient instruction

User context: clinician literacy material

Failure mode: policy text as direct instruction

Clinical severity: high

Missing variable: setting, patient group, contraindications, local practice, and clinician judgment

Source support gap: broad policy language does not support direct patient action

Safe rewrite: This policy reference needs clinician interpretation before patient facing instruction.

Reviewer state: draft

### SLR007 from SFC007

Scenario scope: Public dataset is treated as medically fit

User context: data quality review

Failure mode: access as data fitness

Clinical severity: medium

Missing variable: label quality, provenance, population fit, leakage control, consent boundary, and task suitability

Source support gap: dataset access does not support data fitness claims

Safe rewrite: Dataset access is not data fitness. Label quality and task suitability remain unreviewed.

Reviewer state: draft

### SLR008 from SFC008

Scenario scope: Human review is named but undefined

User context: workflow review language

Failure mode: ceremonial human review

Clinical severity: high

Missing variable: reviewer role, trigger, authority, record, and escalation path

Source support gap: a phrase about human review does not prove a working review process

Safe rewrite: Human review is not defined until role, trigger, authority, and record are explicit.

Reviewer state: draft

### SLR009 from SFC009

Scenario scope: Vendor statement becomes medical assurance

User context: model capability wording

Failure mode: vendor language as assurance

Clinical severity: medium

Missing variable: independent review, clinical context, source support, local workflow, and data fitness

Source support gap: vendor capability language does not support medical assurance

Safe rewrite: Vendor language is background context only. Medical assurance requires independent review gates.

Reviewer state: draft

### SLR010 from SFC010

Scenario scope: Sandbox route is described as deployment readiness

User context: route exploration language

Failure mode: route exploration as readiness

Clinical severity: high

Missing variable: formal process, institutional decision, clinical governance, procurement route, and patient facing use clearance

Source support gap: a sandbox or route question does not support deployment readiness

Safe rewrite: This is route exploration only and does not imply clinical deployment or institutional adoption.

Reviewer state: draft

## Boundary

These are synthetic review rows. They are not clinical advice, patient data, clinical validation, clinical deployment, benchmark ranking, score certification, source truth certification, institutional approval, partner status, endorsement, acceptance, or merge.

## Runnable check

`make clinician_severity_layer_seed_rows`
