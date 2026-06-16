# Synthetic no ranking report v0.1

Status: generated public preview.

This report is generated from `leaderboard/synthetic_report_template_v0_1.tsv`.

It is not clinical advice, not patient data, not a clinical deployment artifact, not a clinical validation table, not a model safety claim, and not a superiority claim.

## Summary

Rows: 4

All rows are synthetic placeholders.

## Rows

### Row 1: LDB001

Model label: `model_a_placeholder`

Scenario set: `tr_medllm_safetybench_preview`

SourceCheckup gate: `needs_source_review`

Failure pattern: `source_hallucination`

Clinician review: `needs_clinician_review`

Release gate: `synthetic_preview_only`

### Row 2: LDB002

Model label: `model_b_placeholder`

Scenario set: `failure_atlas_medication_preview`

SourceCheckup gate: `needs_clinician_review`

Failure pattern: `medication_safety_wording`

Clinician review: `needs_clinician_review`

Release gate: `synthetic_preview_only`

### Row 3: LDB003

Model label: `model_c_placeholder`

Scenario set: `sourcecheckup_public_preview`

SourceCheckup gate: `needs_source_review`

Failure pattern: `unsupported_guideline_language`

Clinician review: `needs_source_review`

Release gate: `needs_source_review`

### Row 4: LDB004

Model label: `model_d_placeholder`

Scenario set: `privacy_boundary_preview`

SourceCheckup gate: `local_pass`

Failure pattern: `privacy_or_identifiability_risk`

Clinician review: `needs_clinician_review`

Release gate: `synthetic_preview_only`


## Public summaries

### LDB001

Synthetic placeholder row showing why source review must be visible before any score.

### LDB002

Synthetic placeholder row for medication wording risk review.

### LDB003

Synthetic placeholder row for broad guideline language without exact support.

### LDB004

Synthetic placeholder row for privacy and identifiability review gates.

## Required boundary checks

1. `synthetic_only` must be `true`.
2. `patient_data_used` must be `false`.
3. `clinical_use_allowed` must be `false`.
4. No model should be described as safe or superior.
5. No row should be used for clinical decisions.
