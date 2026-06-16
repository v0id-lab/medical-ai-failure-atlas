# No ranking leaderboard design v0.1

Status: public design preview.

Date: 2026 06 16

This document defines a public report design for future medical AI safety evaluation runs. It is called a leaderboard because readers expect a single place to inspect model run results, but v0.1 is deliberately a no ranking design.

It does not claim that any model is safe, clinically useful, validated for clinical use, superior, compatible with another benchmark, or ready for clinical deployment.

All current rows are synthetic placeholders.

## Why no ranking first

A simple rank table can hide the exact failure pattern that matters in medicine. A model can look strong overall while still failing on red flag escalation, medication safety, source support, privacy, or patient communication.

The first public design therefore reports gates and failure patterns before any aggregate score.

## Public report fields

Each future report row should include:

1. `run_id`
2. `model_label`
3. `scenario_set`
4. `synthetic_only`
5. `patient_data_used`
6. `clinical_use_allowed`
7. `sourcecheckup_gate`
8. `failure_atlas_pattern`
9. `clinician_review_state`
10. `release_gate`
11. `public_summary`

## Required public gates

1. Patient data must be false.
2. Clinical use must be false.
3. Clinical validation claim must be false.
4. Model safety claim must be false.
5. Institutional endorsement claim must be false.
6. Compatibility claims must be false unless independently verified and clearly scoped.
7. SourceCheckup gate must be visible for every source dependent answer set.
8. Clinician review state must be visible for every report.

## Report states

1. `synthetic_preview_only`: safe to inspect as a synthetic public example.
2. `needs_source_review`: source support is incomplete.
3. `needs_clinician_review`: clinical risk interpretation is incomplete.
4. `not_for_public_summary`: raw output, terms, privacy, or claim risk prevents public summary.

## What this enables

1. A public view of safety gates before scores.
2. A way to connect SourceCheckup Medical to Failure Atlas categories.
3. A future path for model run reports without claiming clinical safety.
4. A structure for contributors to propose synthetic report rows.

## Current preview files

1. `leaderboard/synthetic_report_template_v0_1.tsv`
2. `leaderboard/README.md`
3. `scripts/validate_leaderboard_template_v0_1.py`

## Next build

1. Add public contributor guidance for synthetic report rows.
2. Add a machine readable schema for report rows.
3. Add a generated Markdown report from the TSV template.
4. Connect issue labels to SourceCheckup v0.2 and leaderboard preview work.
