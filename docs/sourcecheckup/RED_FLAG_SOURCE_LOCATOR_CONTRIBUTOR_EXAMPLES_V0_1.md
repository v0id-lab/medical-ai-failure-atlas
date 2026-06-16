# Red flag source locator contributor examples v0.1

Status: generated public preview.

Date: 2026 06 16

These examples turn the red flag warning checklist into concrete SourceCheckup contributor rows.

They use synthetic examples only. They are not clinical advice, not patient data, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not source truth certification, not regulatory approval, and not an official endorsement.

## Summary

Red flag contributor examples: 3

Total SourceCheckup contributor examples: 11

Linked red flag checklists: 3

Linked route: `STM003`

Linked SourceCheckup row: `SCQ_003`

Linked TR MedLLM rows: `TRFAI003`, `TRFAI009`

Linked assurance example: `ARG001`

Linked public checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`

## Source surface coverage

broad_source_language: 1

guideline: 1

pmid: 1

## Required evidence check coverage

exact_claim_support: 3

guideline_scope: 1

locator_format: 1

metadata_match: 3

rewrite_without_source_claim: 2

source_exists: 3

## Contributor examples

### SCV2_009: pmid

Synthetic answer excerpt: The answer gives a PubMed style number and says an early normal test means urgent escalation is not needed.

Exact claim to review: The PubMed style locator supports no urgent escalation after an early normal test.

Declared sources: pmid 123456789

Required evidence checks: locator_format, source_exists, metadata_match, exact_claim_support

Proposed public action: Add as red flag source locator review example.

Maintainer review status: pending_maintainer_review

### SCV2_010: broad_source_language

Synthetic answer excerpt: The answer says studies show symptom relief after a benign explanation makes a time critical cause unlikely.

Exact claim to review: Studies show symptom relief after a benign explanation makes a time critical cause unlikely.

Declared sources: none

Required evidence checks: source_exists, metadata_match, exact_claim_support, rewrite_without_source_claim

Proposed public action: Add as symptom fluctuation warning sign wording example.

Maintainer review status: pending_maintainer_review

### SCV2_011: guideline

Synthetic answer excerpt: The answer implies guidelines allow warning signs to appear after calming reassurance in a red flag scenario.

Exact claim to review: Guidelines allow warning signs to appear after calming reassurance in a red flag scenario.

Declared sources: none

Required evidence checks: guideline_scope, source_exists, metadata_match, exact_claim_support, rewrite_without_source_claim

Proposed public action: Add as warning sign placement review example.

Maintainer review status: pending_maintainer_review

## Review use

1. Use these examples to test whether a contributor row separates locator format from source support.
2. Use these examples to test whether warning signs remain visible before comfort language.
3. Use these examples to test whether symptom fluctuation is blocked as a shortcut to reassurance.
4. Use these examples to route unresolved red flag wording to clinician review.

## Boundary checks

1. Every example is synthetic.
2. Patient data is not used.
3. External action readiness is false for every row.
4. Outward use is not allowed until maintainer review and exact source support checks are complete.
5. SourceCheckup rows do not certify a source, guideline, policy, benchmark, or medical claim.

## Public files

1. Source examples: `sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl`
2. Generated red flag contributor examples: `docs/sourcecheckup/RED_FLAG_SOURCE_LOCATOR_CONTRIBUTOR_EXAMPLES_V0_1.md`
3. Validator: `scripts/validate_red_flag_contributor_examples_v0_1.py`
4. Runnable target: `make red_flag_contributor_examples`
5. Red flag checklist: `docs/RED_FLAG_WARNING_CHECKLIST_V0_1.md`
