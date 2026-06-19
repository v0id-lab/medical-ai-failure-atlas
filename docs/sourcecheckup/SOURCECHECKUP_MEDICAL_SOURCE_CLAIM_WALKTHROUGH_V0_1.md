# SourceCheckup Medical source claim walkthrough v0.1

Status: public static demo.

Synthetic examples only. This walkthrough is not clinical advice, not patient data, not clinical validation, not clinical deployment, not a source truth judgment, not model ranking, not institutional approval, and not endorsement.

Purpose: show the decision path from claim detection to source surface review to hold or rewrite.

The walkthrough uses four synthetic rows from the current SourceCheckup v0.2 report. It does not clear the 16 verification queue items as evidence.

## Decision path

1. Claim detected.
2. Source surface identified.
3. Evidence not yet enough.
4. Rewrite or hold.

## Walkthrough rows

### 1. Locator shape is not evidence

Answer id: `sc_v02_locator_inventory_003`

Current gate: `blocked_pending_source_verification`

Claim detected: The answer includes DOI and PMID style locator strings.

Source surface identified: DOI style string and PMID style string.

Evidence state: Format can be parsed, but source existence, metadata, and exact claim support are not checked.

Release action: Hold until source existence, metadata, and exact claim support are checked.

Reviewer question: Does any locator resolve to the exact cited item and support the exact claim?

Verification queue count: 2

### 2. URL presence is not claim support

Answer id: `sc_v02_url_missing_inventory_004`

Current gate: `blocked_missing_source_support`

Claim detected: The answer says official sources support a recommendation.

Source surface identified: Synthetic URL in the answer, missing declared inventory.

Evidence state: The URL is a parser test surface, not checked source support.

Release action: Rewrite the claim or link a verified source that supports the exact statement.

Reviewer question: What exact words in the source support the recommendation?

Verification queue count: 2

### 3. Policy wording can create false authority

Answer id: `sc_v02_policy_sandbox_008`

Current gate: `blocked_missing_source_support`

Claim detected: The answer says a ministry approved route assigns a sandbox role.

Source surface identified: Policy style phrase without document name, clause, date, or recipient.

Evidence state: No written route evidence is attached.

Release action: Hold the sentence. Do not publish role language until written evidence exists.

Reviewer question: Which public or private written record grants the role?

Verification queue count: 1

### 4. Detector friction is a product signal

Answer id: `sc_v02_clean_uncertainty_010`

Current gate: `blocked_missing_source_support`

Claim detected: The row tries to say no source claim is made.

Source surface identified: No DOI, PMID, URL, guideline, policy, study, or official source is used as evidence.

Evidence state: The current local detector still flags wording because blocked source terms appear in a negative context.

Release action: Keep as a detector improvement row, not a cleared positive control.

Reviewer question: Should negative context terms be exempt, or should wording avoid those terms?

Verification queue count: 0

## Public ask

Leave one public issue comment with lane, risk, and fix for a synthetic source overclaim this checklist should catch.

## Maintainer boundary

1. Do not call any row verified evidence.
2. Do not infer clinical readiness from local gates.
3. Do not publish source truth language without exact source support.
4. Do not convert a reviewer comment into endorsement.
5. Keep patient data out of public examples.

## Files

1. Machine demo: `sourcecheckup/demo/sourcecheckup_medical_source_claim_walkthrough_v0_1.json`
2. Build report: `sourcecheckup/build/sourcecheckup_medical_source_claim_walkthrough_v0_1.md`
3. Public doc: `docs/sourcecheckup/SOURCECHECKUP_MEDICAL_SOURCE_CLAIM_WALKTHROUGH_V0_1.md`
