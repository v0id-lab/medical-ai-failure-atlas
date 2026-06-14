# Medmarks exploratory failure probe set datasheet v0.1

Status: internal draft only. Not externally posted.

Date: 2026 06 14.

## What this is

This is a thirty case synthetic exploratory probe set for testing whether a Medmarks style open ended environment can load and score medical AI safety wording cases.

It is designed to exercise failure mechanisms such as unsafe remote dosing, false reassurance, missing variable awareness, evidence reliability, protocol over precision, delayed care, communication risk, and conservative care negative controls.

## What this is not

This is not a validated benchmark.

This is not a representative sample of medical AI failures.

This is not clinical decision support evidence.

This is not a model ranking dataset.

This is not an accepted Medmarks environment.

## Composition

Rows: 30.

Source: existing synthetic scenario banks in this repository.

Selection method: purposive, non random, single author seed selection.

Clinical domains: 15.

Strata:

1. urgent triage and false reassurance: 6
2. unsafe remote dosing or medication safety: 5
3. evidence reliability: 5
4. protocol over precision: 5
5. omission or delayed care: 4
6. communication risk: 3
7. conservative care negative controls: 2

## Collection process

Cases were derived from synthetic scenario bank rows using a deterministic builder script.

No patient record, chart, e mail, message, or real clinical vignette was used.

No raw model answer is included in the seed file.

## Preprocessing

The builder converts each source scenario into:

1. a prompt
2. safety focus
3. failure mechanism tags
4. clinician review question
5. four rubric criteria

The validator checks fixed safety flags, schema version, stratum counts, source uniqueness, rubric shape, absence of raw model output keys, simple PII patterns, and clinical domain breadth.

## Uses

Appropriate internal uses:

1. local Medmarks environment loading test
2. rubric and validator development
3. clinician review worksheet preparation
4. future audited issue or pull request draft after user approval

Inappropriate uses:

1. clinical care
2. model ranking
3. prevalence estimation
4. publication claims of validated safety performance
5. training data without leakage review

## Known limitations

1. single physician authored draft
2. additional clinician review not complete
3. non random selection
4. English only
5. text only
6. no pediatric, surgical, dermatology, imaging, or procedure heavy coverage beyond limited seed examples
7. no demographic fairness evaluation
8. no real model judge run yet

## Maintenance

Schema version:

`medmarks_failure_probe_seed_v0_1`

Current file:

`data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl`

Builder:

`scripts/build_medmarks_30_case_seed_v0_1.py`

Validator:

`scripts/validate_medmarks_30_case_seed_v0_1.py`

Any external use requires audit and explicit user approval.
