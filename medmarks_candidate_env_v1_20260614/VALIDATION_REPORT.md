# Medmarks candidate environment v1 validation report

Status: public sync candidate. Not a pull request and not an accepted Medmarks environment.

Date: 2026 06 14.

## Scope

This report validates the local proof pack:

`medmarks_candidate_env_v1_20260614/`

The proof pack is not a Medmarks issue, pull request, or accepted environment.

## Live upstream checks used

Medmarks repository readback:

1. repository: Medmarks upstream repository
2. license: MIT
3. issues enabled: true
4. discussions enabled: false
5. environment folder includes `healthbench`

Medmarks developer guide readback:

1. new environment packages live under `environments`
2. environments expose `load_environment`
3. `pyproject.toml` may include `[tool.prime.environment]`
4. smoke testing should happen before contribution

HealthBench environment readback:

1. exports `load_environment`
2. uses single turn environment pattern
3. uses judge criteria and point lists

## Files checked

1. `environments/failure_atlas_safety_wording/failure_atlas_safety_wording.py`
2. `environments/failure_atlas_safety_wording/judge_prompts.py`
3. `environments/failure_atlas_safety_wording/pyproject.toml`
4. `environments/failure_atlas_safety_wording/README.md`
5. `configs/failure_atlas_safety_wording_smoke.toml`
6. `configs/failure_atlas_safety_wording_30case_smoke.toml`
7. `../data/failure_atlas_external_sample_v0_1.jsonl`
8. `../data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl`
9. `../docs/MEDMARKS_HEALTHBENCH_EVIDENCE_RELIABILITY_CROSSWALK_V0_1.md`
10. `../docs/MEDMARKS_V1_DEPENDENCY_AWARE_DRY_RUN_NOTE_20260614.md`
11. `../docs/MEDMARKS_V1_30_CASE_EXPANSION_PLAN_20260614.md`
12. `../schemas/medmarks_failure_probe_seed_v0_1.schema.json`
13. `../docs/MEDMARKS_FAILURE_PROBE_SET_DATASHEET_V0_1.md`
14. `../docs/MEDMARKS_FAILURE_PROBE_TAXONOMY_V0_1.md`

## Checks run

The local validation used Python syntax checks, local smoke loading for the three case sample and thirty case seed, seed builder and validator checks, strict public sanitation checks, forbidden visible process label scanning, and repository validation.

## Result

Syntax validation:

PASS

Smoke run:

```json
{
  "status": "smoke_pass",
  "cases": 3,
  "first_case_id": "FA_SAMPLE_001",
  "points_per_case": [
    8,
    8,
    8
  ],
  "review_status": "physician authored synthetic draft pending final clinician review",
  "contains_patient_data": false,
  "not_for_clinical_use": true
}
```

Thirty case seed smoke run:

PASS

1. 30 synthetic cases loaded.
2. first case ID: `FA_MEDMARKS_001`
3. every case has eight rubric points.
4. every case is marked no patient data and not for clinical use.
5. review status is `single physician authored synthetic draft pending additional clinician review`.

Thirty case seed validation:

PASS

1. expected stratum counts passed.
2. duplicate source scenario check passed.
3. raw model output key scan passed.
4. clinical domain count: 15.
5. schema version and exploratory probe role passed.
6. language, source license, provenance, selection method, and review status passed.
7. controlled tag and simple PII pattern checks passed.

Dependency probe:

PASS with dependency gap.

Output file:

`medmarks_candidate_env_v1_20260614/dependency_probe_v0_1.json`

Probe result:

1. status: `probe_pass_with_dependency_gap`
2. no endpoint or model call: true
3. hard checks ok: true
4. package metadata ok: true
5. config shape ok: true
6. thirty case smoke shape ok: true
7. optional dependencies missing in this workspace: `datasets`, `medarc_verifiers`, `openai`, `verifiers`

Claim boundary from this probe:

1. It is acceptable to claim local dependency probe readiness without endpoint calls.
2. It is acceptable to claim the environment metadata and local smoke shape are ready for a Medmarks checkout test.
3. It is not acceptable to claim a full Medmarks dependency run, accepted Medmarks environment, judge or model evaluation, clinical validation, model ranking, or safety performance.

Medmarks PR staging package:

PASS.

Build command:

```bash
python3 scripts/build_medmarks_pr_staging_v0_1.py
```

Validation command:

```bash
python3 scripts/validate_medmarks_pr_staging_v0_1.py
```

Staging directory:

`medmarks_candidate_env_v1_20260614/medmarks_pr_staging_v0_1/`

Validation output:

`medmarks_candidate_env_v1_20260614/medmarks_pr_staging_validation_v0_1.json`

Staging result:

1. status: `staging_pass`
2. no endpoint or model call: true
3. files staged: 11
4. pyproject metadata: pass
5. Medmarks style config path: pass
6. JSONL rows: 30
7. first case ID: `FA_MEDMARKS_001`
8. contains patient data: false
9. not for clinical use: true
10. thirty case smoke: pass
11. points per case: 8

Staging boundary:

1. This is a local package only.
2. No pull request was opened.
3. Initial local staging did not install dependencies.
4. A later scratch checkout dependency smoke run was completed without endpoint calls.
5. No model endpoint or judge endpoint was called.
6. No Medmarks acceptance, clinical validation, or model ranking claim is supported by this staging pass.

Scratch checkout dependency smoke:

PASS.

Date:

2026 06 14.

Scratch checkout:

`outputs/external_checkouts/medmarks_dependency_dry_run_20260614/`

Upstream repository:

`https://github.com/MedARC-AI/medmarks`

Checked upstream HEAD:

`154710b74e01fb203b5ccf47312dc73d27cd04b4`

What passed:

1. Fresh Medmarks checkout matched the recorded HEAD.
2. The staging package copied into the checkout.
3. Python 3.12 isolated environment was created.
4. Medmarks dependencies installed in that isolated environment.
5. `datasets`, `medarc_verifiers`, `openai`, and `verifiers` imported successfully.
6. The package build metadata was fixed from an invalid build requirement to `hatchling`.
7. The environment package installed editable in the scratch checkout.
8. Thirty synthetic cases loaded.
9. A two row dataset smoke built successfully.
10. `load_environment` created a `SingleTurnEnv` with a dummy key used only to satisfy client construction.
11. `medarc-eval bench --dry-run` produced a one eval plan for thirty examples.

Endpoint boundary:

1. No model endpoint call was made.
2. No judge endpoint call was made.
3. No real API key was entered or exported.
4. No benchmark run beyond `--dry-run` was executed.
5. No pull request, issue, public post, package publish, payment, login, or terms acceptance occurred in this dependency smoke.

Claim boundary after scratch dependency smoke:

1. It is acceptable to say the Medmarks style staging package passed a scratch checkout dependency smoke and Medmarks bench dry run planning without endpoint calls.
2. It is not acceptable to claim a model evaluation, judge evaluation, accepted Medmarks environment, pull request readiness, clinical validation, benchmark performance, model ranking, or deployment safety.

Claude critic follow up:

PASS

Claude flagged that the thirty case set must not be framed as representative, validated, or a benchmark. Fixes applied:

1. each row now has `schema_version`
2. each row now has `artifact_role` set to `exploratory_failure_probe_set`
3. each row now has language, source license, derivation, source data status, selection method, and review status
4. a machine readable schema file was added
5. a datasheet and taxonomy note were added
6. the validator checks controlled tags, simple PII patterns, length bounds, source uniqueness, strata counts, and absence of raw model output keys

Metadata validation:

PASS

1. Prime loader is `failure_atlas_safety_wording:load_environment`.
2. visibility is `PUBLIC`.
3. source sample has 3 synthetic cases.
4. every case is marked no patient data and not for clinical use.

Package import validation:

PASS

The package imports from `medmarks_candidate_env_v1_20260614/environments` without requiring Verifiers dependencies. End to end `load_environment()` still requires an environment with Medmarks dependencies installed.

Hardening note validation:

PASS

1. Dependency aware dry run boundary note added.
2. Thirty case expansion plan added.
3. Thirty case seed builder and validator added.
4. Forbidden visible process label scan returned no hits.
5. No external issue, pull request, discussion, model run, or endpoint call was made.

Repository validation:

PASS

`make validate` passed after the Medmarks v1 hardening notes were added.

## Improvement over v0

V0 was a standalone script.

V1 now adds:

1. `load_environment`
2. Prime environment metadata
3. case level rubric loading rather than hardcoded shared criteria
4. local smoke path that does not call a model or judge endpoint
5. explicit not for clinical use and clinician review boundary
6. package import path with relative import support
7. safer judge JSON extraction and local averaging rather than private helper access
8. thirty case exploratory probe seed with schema, datasheet, taxonomy, and stricter validator

## Remaining blockers

1. Medmarks Verifiers dependencies were not installed in this local workspace, so `load_environment()` was not executed end to end.
2. The thirty case seed is not an accepted Medmarks environment.
3. The seed is not clinically validated.
4. External issue, pull request, or publication requires separate audit and user approval.
5. A real judge or model evaluation still requires endpoint, provider terms, cost cap, and explicit user approval.
