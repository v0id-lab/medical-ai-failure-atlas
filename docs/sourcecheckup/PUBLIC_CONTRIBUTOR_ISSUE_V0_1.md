# SourceCheckup public contributor issue guide v0.1

Status: public preview.

Date: 2026 06 16

This guide defines how contributors can open a public SourceCheckup issue for synthetic source claim review examples.

It is not clinical advice, not patient data, not clinical deployment, not clinical validation, not a source truth certificate, not a model safety claim, and not an institutional or national program endorsement.

## Purpose

The public issue route helps contributors submit synthetic examples where a medical AI answer uses one of these source surfaces:

1. DOI style locator.
2. PMID style locator.
3. URL style locator.
4. Guideline language.
5. Policy language.
6. Broad source language.
7. No source despite a source dependent claim.

The issue route does not verify the claim by itself. It creates a maintainer review queue.

## Public issue template

Use:

`.github/ISSUE_TEMPLATE/sourcecheckup_review.yml`

The template requires:

1. Source surface.
2. Synthetic answer excerpt.
3. Exact claim to review.
4. Whether the claim is central to the answer.
5. Declared source locator or source text.
6. Required evidence checks.
7. Proposed public action.
8. Boundaries.

## Required contributor boundaries

Every issue must state:

1. The example is synthetic and contains no patient data.
2. No external action has been executed.
3. Outward use is not allowed without maintainer review.
4. SourceCheckup output is a review queue, not proof that a medical claim is true.
5. The issue is not clinical advice and not a clinical validation claim.

## Maintainer triage

Maintainers should route accepted issues into one of:

1. `sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl`
2. `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`
3. `docs/sourcecheckup/SOURCE_CLAIM_REVIEW_QUEUE_V0_1.md`
4. `sourcecheckup/schemas/sourcecheckup_contribution_schema_v0_2.json`
5. A closed issue comment explaining why the row is not suitable.

## Required evidence checks

Use one or more of:

1. `locator_format`
2. `source_exists`
3. `metadata_match`
4. `exact_claim_support`
5. `guideline_scope`
6. `policy_jurisdiction`
7. `rewrite_without_source_claim`

## Example public issue body

Source surface:

`guideline`

Synthetic answer excerpt:

`Guidelines recommend routine use for this condition.`

Exact claim to review:

`Guidelines recommend routine use for this condition.`

Required evidence:

1. Guideline exists.
2. Guideline date and owner match.
3. Population and setting match.
4. The exact routine use claim is supported.
5. If not supported, rewrite without the guideline claim.

Boundary:

Synthetic only. No patient data. No external action. No clinical advice. No clinical validation claim.

## Track A value

For Turkiye health AI safety infrastructure, this issue route creates a public source discipline intake surface for Turkish medical LLM review, clinician AI literacy, and assurance lab release gates without claiming official status or sandbox access.

## Track B value

For global open source medical AI evaluation, this issue route gives SourceCheckup Medical a public contributor path that can grow source quality examples without publishing patient data, model rankings, clinical validation claims, or unsupported guideline claims.
