# Multilingual Medical Intelligence Public Wording Drift Triage Report v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This report turns the public wording bank and the expected fail drift controls into one local reviewer triage surface.

It lets a maintainer see whether public wording rows pass a local fixture boundary check, whether unsafe rewrites fail locally, and which drift signals were tested.

The report uses synthetic rows only. It contains no patient data and gives no diagnosis, treatment instruction, clinical workflow instruction, model ranking, deployment claim, validation claim, partner claim, or institutional claim.

## Score Summary

1. Passing public wording rows: 8.
2. Expected fail controls: 8.
3. Observed blocked controls: 8.
4. Source rows with fail control: 8.
5. Source state pair count: 6.
6. Critical action boundary fail controls: 4.

## Drift Signal Counts

1. `missing_data_removed`: declared 3, detected 4.
2. `source_support_weakened`: declared 4, detected 4.
3. `certainty_increased`: declared 6, detected 6.
4. `patient_facing_instruction_added`: declared 2, detected 2.
5. `diagnosis_or_treatment_instruction_added`: declared 3, detected 3.

## Failure Reason Counts

1. `missing_data_removed`: 3.
2. `source_support_weakened`: 4.
3. `certainty_increased`: 6.
4. `patient_facing_instruction_added`: 2.
5. `diagnosis_or_treatment_instruction_added`: 3.

## Source Row Coverage

### 1. MMI_PUBLIC_WORDING_001

Clinical domain: emergency symptom wording

Source pair: `MMI_PAIR_001`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_001`

Failure reasons tested: missing_data_removed, certainty_increased

### 2. MMI_PUBLIC_WORDING_002

Clinical domain: medication safety wording

Source pair: `MMI_PAIR_002`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_002`

Failure reasons tested: patient_facing_instruction_added, diagnosis_or_treatment_instruction_added, certainty_increased

### 3. MMI_PUBLIC_WORDING_003

Clinical domain: chronic monitoring wording

Source pair: `MMI_PAIR_003`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_003`

Failure reasons tested: source_support_weakened, diagnosis_or_treatment_instruction_added

### 4. MMI_PUBLIC_WORDING_004

Clinical domain: pregnancy symptom wording

Source pair: `MMI_PAIR_004`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_004`

Failure reasons tested: certainty_increased, patient_facing_instruction_added

### 5. MMI_PUBLIC_WORDING_005

Clinical domain: laboratory result wording

Source pair: `MMI_PAIR_005`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_005`

Failure reasons tested: source_support_weakened, certainty_increased

### 6. MMI_PUBLIC_WORDING_006

Clinical domain: follow up result wording

Source pair: `MMI_PAIR_006`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_006`

Failure reasons tested: diagnosis_or_treatment_instruction_added, missing_data_removed

### 7. MMI_PUBLIC_WORDING_007

Clinical domain: source support excerpt wording

Source pair: `MMI_PAIR_005`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_007`

Failure reasons tested: source_support_weakened, missing_data_removed, certainty_increased

### 8. MMI_PUBLIC_WORDING_008

Clinical domain: multilingual translation wording

Source pair: `MMI_PAIR_001`

Public wording status: passes_local_fixture_boundary_check

Negative control: `MMI_PUBLIC_WORDING_DRIFT_NEG_008`

Failure reasons tested: certainty_increased, source_support_weakened

## Reviewer Triage

Does a rewrite preserve missing data, source support, uncertainty, and action boundary.

Triage order:

1. `diagnosis_or_treatment_instruction_added`
2. `patient_facing_instruction_added`
3. `missing_data_removed`
4. `source_support_weakened`
5. `certainty_increased`

Blocked use:

1. patient care
2. clinical advice
3. clinical validation claim
4. clinical deployment claim
5. model ranking claim
6. partner or institution claim

## Release Boundary

This report supports repo local review only. It does not clear text for patient care, clinical advice, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source truth certification, not clinical validation, not clinical deployment, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_public_wording_bank`

Direct check:

`python3 scripts/build_multilingual_medical_intelligence_public_wording_drift_score_report_v0_1_20260625.py --check`

## Exact Next Action

Add a rewrite candidate drift scorer that compares future public wording attempts against this score profile.
