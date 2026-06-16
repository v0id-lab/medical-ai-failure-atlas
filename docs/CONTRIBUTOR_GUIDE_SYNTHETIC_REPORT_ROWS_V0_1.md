# Contributor guide for synthetic report rows v0.1

Status: public contributor guide.

Date: 2026 06 16

This guide explains how to propose synthetic report rows for the no ranking leaderboard preview.

The goal is to make medical AI safety reporting more inspectable without claiming model safety, clinical validation, clinical deployment, institutional endorsement, or benchmark superiority.

## What contributors can propose

1. A synthetic scenario set label.
2. A placeholder model label.
3. A SourceCheckup gate.
4. A Failure Atlas pattern.
5. A clinician review state.
6. A release gate.
7. A short public summary.

## Required boundaries

Every proposed row must keep:

1. `synthetic_only` as `true`.
2. `patient_data_used` as `false`.
3. `clinical_use_allowed` as `false`.

Do not include patient data, private model output, real clinical advice, identifiable details, private benchmark material, institutional claims, or model superiority claims.

## Good row shape

A useful row tells reviewers what failed or what still needs review. It does not try to crown a winner.

Example purpose:

1. Show that source review is incomplete.
2. Show that a medication wording pattern needs clinician review.
3. Show that privacy review is required.
4. Show that a row is safe only as a synthetic preview.

## Current template

Use:

`leaderboard/synthetic_report_template_v0_1.tsv`

Run:

```bash
make leaderboard_report
```

The generated report is:

`leaderboard/build/synthetic_report_v0_1.md`

## Review path

1. Open an issue using the synthetic failure case or SourceCheckup review template.
2. State that the row is synthetic.
3. State which safety gate the row is meant to test.
4. Do not submit real patient details.
5. Do not claim a model is safe or superior.
