# Source claim review queue v0.1

Date: 2026 06 16

Status: public preview.

This queue turns SourceCheckup Medical from a local parser into a public review surface. It tells maintainers which source claim needs review, which evidence checks are required, and whether the row must be rewritten or held before reuse.

This is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, and not an institutional or national program endorsement.

## Public files

1. Queue rows: `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`
2. Validator: `scripts/validate_source_claim_review_queue_v0_1.py`
3. Runnable target: `make source_claim_queue`

## Queue fields

Each row records:

1. `queue_id`
2. `source_surface`
3. `connected_project`
4. `synthetic_answer_excerpt`
5. `exact_claim_text`
6. `claim_centrality`
7. `locator_or_source_text`
8. `declared_source_status`
9. `required_checks`
10. `triage_priority`
11. `assigned_review_lane`
12. `public_action`
13. `release_gate`
14. `patient_data`
15. `external_action_ready`
16. `outward_use_allowed`
17. `review_state`

## What the queue blocks

The queue blocks public reuse when a row makes a central source claim and still needs one or more of these checks:

1. Source existence.
2. Metadata match.
3. Exact claim support.
4. Guideline scope.
5. Policy jurisdiction.
6. Rewrite without source claim.

`pass_local_sourcecheckup` only means the row has no local source claim risk in this queue. It does not mean a medical claim is true, safe, verified, validated, or ready for clinical use.

## Track A value

For Türkiye health AI safety infrastructure, this queue creates a repeatable review gate for Turkish medical language model evaluation, clinician AI literacy exercises, source claim discipline, and sandbox readiness discussion.

The queue does not claim official status, official acceptance, sandbox access, regulatory approval, or institutional endorsement.

## Track B value

For global open source medical AI evaluation, this queue gives contributors a concrete way to add source claim review rows without turning citations into proof.

It supports Failure Atlas, SourceCheckup Medical, no ranking reports, clinician review protocol work, and future benchmark compatibility notes.

## Run

```bash
make source_claim_queue
```

The validator checks row count, source surface coverage, required evidence checks, review states, release gates, patient data boundary, and outward use boundary.

## Maintainer rule

No row in this queue is cleared for outward use until a maintainer has checked the exact source, metadata, and claim support or rewritten the row so it no longer makes the source claim.
