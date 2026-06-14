# Medmarks PR staging package v0.1

Status: local staging package only. Not submitted.

Purpose: mirror the files that would be needed for a future Medmarks style environment review, without opening a pull request, installing dependencies, or calling a model endpoint.

Contents:

1. `environments/failure_atlas_safety_wording/`
2. `environments/failure_atlas_safety_wording/data/failure_atlas_medmarks_30_case_seed_v0_1.jsonl`
3. `environments/failure_atlas_safety_wording/docs/`
4. `configs/failure_atlas_safety_wording_30case_smoke.toml`

Boundary:

1. Synthetic cases only.
2. No patient data.
3. Not for clinical use.
4. No raw model output included.
5. No endpoint call made by the staging builder.
6. Not a validated benchmark.
7. Not an accepted Medmarks environment.

Next safe validation:

```bash
python3 scripts/validate_medmarks_pr_staging_v0_1.py
```

Full dependency or endpoint tests require separate approval.
