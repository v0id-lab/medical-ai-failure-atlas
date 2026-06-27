# Multilingual Medical Intelligence Cross Language Source Recency And Applicability Controls v0.1

Date: 2026 06 25

Status: ready for local repo review only

## Purpose

This report checks whether English and Turkish ASCII variants preserve the source recency applicability map, source date, population, setting, and applicability limits across the same record.

It blocks cross language source recency and applicability drift when one language shifts source date, inflates source recency status, broadens population or setting scope, or removes applicability limits.

It keeps source recency and applicability, source date identity, population and setting limits, and reviewer hold attached to the same synthetic source record.

The controls use synthetic rows only. They contain no patient data and make no diagnosis, treatment instruction, clinical validation, clinical deployment, model ranking, partner, or institutional claim.

## Score Summary

1. Control rows: 12.
2. Expected pass controls: 6.
3. Expected fail controls: 6.
4. Observed pass controls: 6.
5. Observed blocked controls: 6.
6. Source candidate coverage count: 6.
7. Source row coverage count: 6.

## Cross Language Signal Counts

1. `english_source_date_shifted`: declared 1, detected 1.
2. `turkish_source_date_shifted`: declared 1, detected 1.
3. `source_recency_status_inflated`: declared 1, detected 1.
4. `population_scope_broadened`: declared 1, detected 1.
5. `setting_scope_broadened`: declared 1, detected 1.
6. `applicability_limit_removed`: declared 1, detected 1.

## Reviewer Triage

Does either language shift source date, inflate source recency status, broaden population or setting scope, or remove applicability limits.

Triage order:

1. `english_source_date_shifted`
2. `turkish_source_date_shifted`
3. `source_recency_status_inflated`
4. `population_scope_broadened`
5. `setting_scope_broadened`
6. `applicability_limit_removed`

## Release Boundary

This report supports repo local review only. It does not clear text for patient care, clinical advice, translation clearance, source recency and applicability clearance, clinical validation, clinical deployment, model comparison, institutional use, or external publication.

Boundary note: not score certification, not source recency certification, not clinical validation, not clinical deployment, not translation clearance, not source recency and applicability clearance, and not external publication clearance.

## Validation Command

`make multilingual_medical_intelligence_cross_language_source_recency_applicability_controls`

Direct check:

`python3 scripts/score_multilingual_medical_intelligence_cross_language_source_recency_applicability_controls_v0_1_20260625.py --check`

## Exact Next Action

Add cross language source conflict and provenance controls so translated variants preserve source conflict status, source version, and provenance chain before public reuse.
