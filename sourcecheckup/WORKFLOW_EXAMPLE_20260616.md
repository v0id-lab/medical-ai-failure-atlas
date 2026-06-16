# SourceCheckup Workflow Example

Date: 2026 06 16

Status: public preview.

Not clinical advice. No patient data. No live source verification is performed by this local tool.

## Goal

This workflow shows how a medical AI answer moves from answer text to source support review.

The key rule:

A citation is not evidence until the source exists, metadata match, and the source text supports the exact claim.

## Step 1: Prepare A JSONL Answer Row

Each row needs:

1. `answer_id`
2. `prompt`
3. `answer`

Optional structured fields:

1. `declared_sources`
2. `declared_claims`

Example source types:

1. `doi`
2. `pmid`
3. `url`
4. `guideline`
5. `policy`
6. `other`

## Step 2: Run SourceCheckup

```bash
make sourcecheckup
```

The command runs a self test and then creates:

1. `sourcecheckup/build/sourcecheckup_seed_report.json`
2. `sourcecheckup/build/sourcecheckup_seed_report.md`

## Step 3: Read The Gate

The current local gates are:

1. `blocked_missing_source_support`
2. `blocked_pending_source_verification`
3. `pass_local_sourcecheckup`

These gates are for source support review only. They do not mean clinical truth, clinical safety, model safety, guideline concordance, or clinical validation.

## Step 4: Review The Queue

The verification queue tells the reviewer what needs attention:

1. A DOI to verify.
2. A PMID to verify.
3. A URL to open and inspect.
4. A guideline claim needing exact source support.
5. A policy claim needing written official evidence.
6. Broad source language that should be rewritten or sourced.

## Step 5: Rewrite Or Verify

The reviewer can then:

1. Remove unsupported source language.
2. Replace broad phrases with narrow wording.
3. Add exact source metadata after live verification.
4. Mark the answer as unsuitable for outward use.
5. Keep a clean answer that makes no source claim.

## Example Interpretation

If an answer says:

`Studies show this model is safe for clinical deployment.`

SourceCheckup should flag it because:

1. `studies show` is broad source language.
2. `safe for clinical deployment` is a high risk claim.
3. No exact evaluated system, setting, outcome, or source text is provided.

A safer public rewrite is:

`This synthetic example is used to test whether a model answer makes unsupported safety claims. It is not evidence that any model is safe for clinical use.`

## Boundary

SourceCheckup is a review queue generator. It is not a medical fact checker, not a guideline engine, not a clinical validation system, and not a deployment approval tool.
