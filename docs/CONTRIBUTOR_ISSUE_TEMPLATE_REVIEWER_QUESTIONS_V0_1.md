# Contributor issue template reviewer questions v0.1

Date: 2026 06 17

Status: public preview.

This note records how public issue templates accept benchmark style reviewer question rows.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a benchmark compatibility claim, not a benchmark equivalence claim, not a score report, not a model ranking, not an endpoint result, and not an official endorsement.

## Updated public issue templates

1. `.github/ISSUE_TEMPLATE/sourcecheckup_review.yml`
2. `.github/ISSUE_TEMPLATE/synthetic_failure_case.yml`

## New reviewer question fields

1. `benchmark_reviewer_question_id`
2. `benchmark_lens`
3. `reviewer_question`
4. `blocked_claim_type`

## Allowed use

Contributors may use these fields to explain which review question a synthetic SourceCheckup or Failure Atlas row should answer.

The fields are orientation fields only. They do not make a row compatible with HealthBench, MedHELM, Medmarks, or any other benchmark.

## Required boundaries

Every reviewer question issue must preserve these boundaries:

1. Synthetic only.
2. No patient data.
3. No raw model output.
4. No private benchmark content.
5. No endpoint call.
6. No score report.
7. No model ranking.
8. No benchmark compatibility claim.
9. No benchmark equivalence claim.
10. No clinical deployment.
11. No clinical validation.
12. No official endorsement.

## SourceCheckup route

SourceCheckup reviewer question rows should focus on source support, policy wording, locator format, exact claim support, guideline scope, and rewrite routing.

Accepted rows may later move into:

1. `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`
2. `docs/sourcecheckup/SOURCE_CLAIM_REVIEW_QUEUE_V0_1.md`
3. `docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md`

## Failure Atlas route

Failure Atlas reviewer question rows should focus on escalation, medication safety, missing context, warning sign visibility, communication risk, and unsafe precision.

Accepted rows may later move into:

1. `failure_atlas/public/case_intake_examples_v0_1.jsonl`
2. `failure_atlas/public/build/clinician_review_queue_v0_1.md`
3. `docs/BENCHMARK_STYLE_REVIEWER_QUESTIONS_V0_1.md`

## Maintainer triage

Maintainers should close or rewrite any issue that claims:

1. A benchmark score.
2. Benchmark compatibility.
3. Benchmark equivalence.
4. Model superiority.
5. Clinical safety.
6. Clinical validation.
7. Endpoint results.
8. Patient data use.
9. Official endorsement.

## Track A value

For Turkiye health AI safety infrastructure, this gives Turkish medical LLM source review and Failure Atlas intake a public contributor route for reviewer questions without claiming sandbox access, official route access, deployment, validation, or endorsement.

## Track B value

For global open source medical AI evaluation, this turns benchmark style reviewer questions into an inspectable issue intake path while preserving no score, no ranking, no compatibility, and no endorsement boundaries.

## Example intake rows

See `docs/REVIEWER_QUESTION_INTAKE_EXAMPLES_V0_1.md` for synthetic examples that fill the reviewer question fields without scoring, ranking, compatibility, endpoint, patient data, clinical validation, or endorsement claims.
