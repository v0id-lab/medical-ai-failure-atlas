# Inter rater review subset plan v0.1

Status: internal plan. Not a validation claim.

Date: 2026 06 14.

## Purpose

This plan defines the first held out double review subset for the Medical AI Failure Atlas.

The goal is not to publish model rankings. The goal is to test whether the rubric can be applied consistently by more than one reviewer.

## Current review status

Use:

`single physician authored synthetic draft pending additional clinician review`

Do not use:

`clinically validated`

Do not use:

`validated benchmark`

## Subset file

`data/inter_rater_review_subset_v0_1.tsv`

## Review form files

Reviewer facing form:

`review_forms/inter_rater_review_form_v0_1.tsv`

Coordinator source key:

`review_forms/inter_rater_review_source_key_v0_1.tsv`

Adjudication log template:

`review_forms/adjudication_log_template_v0_1.tsv`

The reviewer facing form must not include source priority, possible failure tags, source triage file, or prior short reason fields.

## Subset size

Total rows:

24

Composition:

1. 6 high priority rows.
2. 12 medium priority boundary rows.
3. 6 low priority negative control rows.

This is a pilot subset for protocol testing.

It is not powered to estimate a stable Cohen kappa value.

Any agreement statistic from this subset must be described as exploratory.

## Selection logic

### High priority rows

Include all six high priority rows from the current hard30 and v3 scale30 runs.

Reason:

These rows define the highest risk safety boundary cases and must be reviewed before any stronger public wording is used.

### Medium priority rows

Select 12 rows that stress the boundary between useful clinical escalation and unsafe precision.

Selection targets:

1. over specific protocol detail;
2. false reassurance plus protocol detail;
3. under informative answers after correct danger recognition;
4. evidence overclaim.

Reason:

These rows test whether the safety gates are too strict, too loose, or too dependent on reviewer preference.

The medium rows are intentionally over sampled relative to their source distribution because the first goal is to stress test gate definitions, not estimate prevalence.

### Low priority rows

Select six low priority rows as negative controls.

Reason:

A useful rubric should not over label every detailed answer as unsafe. Low priority controls test false positive tendency.

The subset is not proportional to the full source corpus. It is a deliberately enriched pilot set.

## Reviewer workflow

Each reviewer should label the 24 rows independently.

The reviewer sees:

1. scenario id;
2. model answer;
3. model name;
4. prompt text;
5. gate definitions;
6. dimension anchors.

The reviewer should not see the other reviewer decision before completing their own first pass.

The reviewer should also not see the previous automated triage priority or possible failure tag while assigning first pass labels.

## Required fields

For each row:

1. all five safety gates marked present, absent, or unsure;
2. all eight dimensions scored from 0 to 2;
3. final label;
4. confidence;
5. short reason;
6. safer wording if a safety gate is present;
7. atlas candidate yes, no, or unsure.

## Agreement analysis

Minimum agreement outputs after two independent reviewers:

1. gate level agreement by each safety gate;
2. final label agreement;
3. count of major gate disagreements;
4. count of final label disagreements;
5. list of rows requiring adjudication.

Optional later metrics:

1. Cohen kappa for binary gate presence if two reviewers label all rows.
2. Weighted agreement for final labels.
3. Krippendorff alpha only if the design expands beyond two reviewers or has substantial missingness.

Do not report Cohen kappa as a stable validation statistic from this 24 row pilot alone.

Before formal agreement claims, prepare a larger pre specified subset with a sample size justification.

## Disagreement handling

Use:

`docs/CLINICIAN_REVIEW_DISAGREEMENT_PROTOCOL_V0_1.md`

No original reviewer field should be overwritten.

Adjudicated fields must be added separately.

## Readiness gates

Before this subset can support public wording:

1. label definition lock v0.1 remains unchanged during review;
2. both reviewers complete all 24 rows or missingness is explicitly recorded;
3. major disagreements are adjudicated or listed as unresolved;
4. raw model output redistribution is cleared or public examples are paraphrased safely;
5. final public text is audited.

## Public wording after completion

Allowed only if the steps above are true:

`a 24 row held out subset was independently reviewed by two reviewers with documented disagreement handling`

Still not allowed:

1. `clinically validated benchmark`
2. `safe for clinical use`
3. `model ranking`
4. `deployment ready`
