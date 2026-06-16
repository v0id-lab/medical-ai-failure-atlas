# SourceCheckup Medical

SourceCheckup Medical is a small source discipline tool for medical AI answers.

It checks whether an answer uses DOI, PMID, URL, guideline, policy, or broad source support language, then creates a review queue.

## What It Does

1. Extracts DOI, PMID, and URL locators from model answers.
2. Checks declared source format.
3. Flags broad source language such as "studies show" or "guidelines recommend".
4. Flags guideline and policy claims that need exact source support.
5. Writes a JSON and Markdown report for human review.

## What It Does Not Do

1. It does not prove a medical claim is true.
2. It does not verify that a DOI, PMID, URL, guideline, or policy is current.
3. It does not provide clinical advice.
4. It does not use patient data.
5. It does not claim model safety or clinical validation.

## Run

```bash
make sourcecheckup
```

Run the larger v0.2 public example set:

```bash
make sourcecheckup_v02
```

Validate v0.2 contribution examples:

```bash
make sourcecheckup_contrib_v02
```

Validate the public contributor issue route:

```bash
make sourcecheckup_public_issue
```

Validate the public source claim review queue:

```bash
make source_claim_queue
```

Generate the SourceCheckup expansion dashboard:

```bash
make sourcecheckup_expansion_dashboard
```

Current public example sets:

1. `sourcecheckup/examples/sourcecheckup_seed_answers.jsonl`
2. `sourcecheckup/examples/source_surface_examples_v0_2.jsonl`
3. `sourcecheckup/examples/sourcecheckup_contribution_examples_v0_2.jsonl`
4. `sourcecheckup/review_queue/source_claim_review_queue_v0_1.jsonl`
5. `docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`
6. `.github/ISSUE_TEMPLATE/sourcecheckup_review.yml`
7. `sourcecheckup/build/source_claim_example_expansion_v0_2.md`

## Input Format

Schema:

`sourcecheckup/schemas/sourcecheckup_input_schema_v0_1.json`

Required fields:

1. `answer_id`
2. `prompt`
3. `answer`

Optional fields:

1. `declared_sources`
2. `declared_claims`

## Output

The report includes:

1. Gate counts.
2. Flag counts.
3. Extracted locators.
4. Verification queue.
5. Per answer review notes.

This is built for synthetic medical AI evaluation workflows before any clinical use is considered.

## Public Review Queue

The source claim review queue adds maintainer triage fields for exact claim text, source surface, required evidence checks, release gate, assigned review lane, and public action.

Current public expansion counts:

1. 10 SourceCheckup v0.2 answer examples.
2. 8 SourceCheckup contributor examples.
3. 12 source claim review queue rows.
4. 8 review queue source surfaces.
5. 3 review queue release gates.

Queue guide:

`docs/sourcecheckup/SOURCE_CLAIM_REVIEW_QUEUE_V0_1.md`

Expansion dashboard:

`sourcecheckup/build/source_claim_example_expansion_v0_2.md`

Public contributor issue guide:

`docs/sourcecheckup/PUBLIC_CONTRIBUTOR_ISSUE_V0_1.md`

Current boundary:

`pass_local_sourcecheckup` means only that no local source claim risk was triggered. It does not mean a medical claim is true, externally verified, clinically validated, or safe for clinical use.
