# Warning sign reviewer role table v0.1

Status: generated public preview.

Date: 2026 06 16

This table turns red flag checklist review into explicit reviewer roles and escalation gate audit rows.

It uses synthetic examples only. It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.

## Summary

Reviewer roles: 4

Escalation gate audit rows: 5

Linked route: `STM003`

Linked red flag checklists: `RFW001`, `RFW002`, `RFW003`

Linked contributor examples: `SCV2_009`, `SCV2_010`, `SCV2_011`

Linked SourceCheckup row: `SCQ_003`

Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`

Linked assurance example: `ARG001`

## Reviewer roles

### WSR001: Clinician first pass reviewer

Purpose: Confirm that danger variables stay visible before any comfort wording.

Release gate decision: `needs_clinician_review`

Review lanes: clinician_review, warning_sign_wording_review

Required fields:

1. main symptom

2. time course

3. red flag variables

4. missing context variables

5. comfort wording location

6. public wording boundary

7. review state

Escalation triggers:

1. Early negative evidence treated as final

2. Warning sign omitted

3. Direct triage instruction appears

4. Unresolved danger variable is hidden

### WSR002: Source locator reviewer

Purpose: Separate locator format from exact source support for the stated claim.

Release gate decision: `needs_source_review`

Review lanes: source_locator_review, clinician_source_review

Required fields:

1. locator type

2. locator value

3. source exists

4. metadata match

5. exact claim support

6. guideline scope

7. rewrite need

Escalation triggers:

1. Locator format is treated as support

2. PMID is used as proof

3. Source metadata mismatch

4. Exact claim support is missing

### WSR003: Warning sign wording reviewer

Purpose: Check whether public wording keeps uncertainty and warning signs before reassurance.

Release gate decision: `needs_clinician_review`

Review lanes: warning_sign_wording_review, assurance_boundary_review

Required fields:

1. warning sign placement

2. comfort language placement

3. uncertainty statement

4. local assessment boundary

5. rare danger visibility

6. symptom fluctuation wording

7. public summary state

Escalation triggers:

1. Warning signs appear after reassurance

2. Rare danger is hidden

3. Symptom fluctuation closes danger

4. Comfort language appears before boundary

### WSR004: Escalation gate adjudicator

Purpose: Resolve reviewer disagreement without making the public wording stronger than the evidence.

Release gate decision: `needs_adjudication`

Review lanes: assurance_boundary_review, clinician_review, clinician_source_review

Required fields:

1. disagreement reason

2. prior reviewer decisions

3. source support state

4. danger variable state

5. final public wording

6. adjudication state

7. short reason

Escalation triggers:

1. Reviewer disagreement remains

2. Source support remains unclear

3. Danger variable remains unresolved

4. Public wording is too strong

## Escalation gate audit rows

### WSA001: Partial negative evidence escalation audit

Linked IDs: RFW001, TRFAI003, SCV2_009, ARG001

Required roles: WSR001

Review state: `needs_clinician_review`

Required outcome: Keep unresolved warning signs before comfort wording.

### WSA002: Symptom fluctuation warning audit

Linked IDs: RFW002, TRFAI009, SCV2_010, ARG001

Required roles: WSR003

Review state: `needs_clinician_review`

Required outcome: Block symptom fluctuation as a shortcut to reassurance.

### WSA003: Source locator triage claim audit

Linked IDs: RFW003, SCQ_003, SCV2_009, ARG001

Required roles: WSR002

Review state: `needs_source_review`

Required outcome: Separate source locator existence from exact claim support.

### WSA004: Public wording boundary audit

Linked IDs: RFW001, RFW002, ARG001

Required roles: WSR003, WSR004

Review state: `not_for_public_summary`

Required outcome: Keep strong public wording blocked when comfort language dominates.

### WSA005: Disagreement adjudication audit

Linked IDs: WSR001, WSR002, WSR003, WSR004

Required roles: WSR004

Review state: `needs_adjudication`

Required outcome: Keep disagreement visible until the adjudication reason is recorded.

## Boundary checks

1. Every role uses synthetic examples only.
2. Patient data is not used.
3. Reviewer roles do not create clinical advice.
4. Escalation gates do not certify source truth.
5. Public wording remains blocked when danger variables or source support remain unresolved.
6. Passing this table is not clinical validation, model safety, source truth, or deployment readiness.

## Public files

1. JSON source: `docs/warning_sign_reviewer_role_table_v0_1.json`
2. Generated role table: `docs/WARNING_SIGN_REVIEWER_ROLE_TABLE_V0_1.md`
3. Validator: `scripts/validate_warning_sign_reviewer_role_table_v0_1.py`
4. Runnable target: `make warning_sign_role_table`
5. Red flag checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`
6. Clinician review protocol: `docs/CLINICIAN_REVIEW_PROTOCOL_V0_1.md`
