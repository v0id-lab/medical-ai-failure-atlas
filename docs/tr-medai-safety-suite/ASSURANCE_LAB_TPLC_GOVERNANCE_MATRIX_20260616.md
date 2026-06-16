# Türkiye Health AI Assurance Lab TPLC Governance Matrix - 2026-06-16

Local Track A product surface. Not sent. Not a public release. Not a regulatory claim.

Owner: Dr. Goktug Ozkan, Internal Medicine Specialist.

## Purpose

Türkiye's health AI entry route needs more than model enthusiasm. It needs a practical clinician led assurance layer that can organize evidence, risk, data quality, source support, human review, audit trail, and release boundaries before any clinical use or sandbox discussion.

This matrix turns the Turkish Clinical AI Assurance Lab into a concrete governance product.

## Source Direction

This matrix is informed by public signals from:

1. Türkiye 2026 to 2030 AI Action Plan public announcement and health sector relevance.
2. TÜYZE and TÜSEB health AI ecosystem signals.
3. TÜBİTAK BİLGEM YZE sectoral AI infrastructure route.
4. FDA AI enabled medical software lifecycle and transparency direction.
5. EU AI Act AI literacy and high risk governance direction.
6. CHAI health AI governance playbooks.
7. WHO large multimodal model and AI health policy governance language.

It does not claim compliance, certification, official acceptance, sandbox access, or institutional endorsement.

## Assurance Lab Control Domains

| Control domain | Assurance question | Required local evidence | Gate state now |
| --- | --- | --- | --- |
| Intended use boundary | What is the artifact meant to do and not do? | Local intended use statement and no clinical use statement. | OPEN LOCAL, CLOSED EXTERNAL |
| Patient data boundary | Does the artifact use patient data or identifiers? | Synthetic data statement, provenance, privacy review note. | OPEN LOCAL if false, CLOSED if unclear |
| Model execution boundary | Which model was run, where, and under what permission? | Model route, endpoint approval, raw output path, terms state. | CLOSED until exact run is cleared |
| Clinical risk card | What harm could happen if the model answer is wrong? | Risk category, severity, likelihood, mitigation, reviewer concern. | OPEN LOCAL |
| Source support card | Are DOI, PMID, URL, guideline, policy, and evidence claims supported? | SourceCheckup matrix, unsupported claim list, rewrite or removal decision. | PARTIAL LOCAL |
| Human review gate | Has clinician review happened and are disagreements tracked? | Clinician review queue, reviewer status, unresolved disagreements. | PARTIAL LOCAL |
| Data quality card | Is the dataset or case set fit for evaluation? | Data card, label audit, provenance, bias and coverage notes. | OPEN LOCAL |
| Lifecycle and change control | How are changes tracked before release? | Version, changelog, audit trail, release gate, regression checks. | OPEN LOCAL |
| Public wording gate | Can claims be safely made outside? | Public claim audit matrix, no endorsement language, no safety claim. | CLOSED EXTERNAL |
| Sandbox readiness | Could this be shown as a sandbox readiness packet? | All previous gates, no patient data, no deployment claim, review summary. | Separate targeted action |

## Card Set

### 1. Model Card

Minimum fields:

1. Model name.
2. Provider.
3. Version or local identifier.
4. Execution mode.
5. Endpoint or local run state.
6. Terms or account state.
7. Known limitations.
8. Evaluation context.
9. No clinical use boundary.

### 2. Risk Card

Minimum fields:

1. Clinical domain.
2. Primary risk theme.
3. Red flag omission risk.
4. False reassurance risk.
5. Medication safety risk.
6. Source hallucination risk.
7. Privacy risk.
8. Severity.
9. Likelihood.
10. Mitigation.
11. Residual risk.

### 3. Data Card

Minimum fields:

1. Synthetic or real data status.
2. Patient data present.
3. Identifier status.
4. Data source.
5. Provenance.
6. License or use rights.
7. Label method.
8. Reviewer status.
9. Bias or coverage limitations.
10. Data quality blockers.

### 4. Source Support Card

Minimum fields:

1. Claim text.
2. Claim type: DOI, PMID, URL, guideline, policy, source, model, route, or benchmark.
3. Source locator.
4. Support status: verified, unsupported, insufficient, stale, or not checked.
5. Required action: keep, rewrite, remove, verify later, or exclude from outward use.
6. Public wording decision.

### 5. Human Review Card

Minimum fields:

1. Reviewer role.
2. Review date.
3. Case count reviewed.
4. High risk rows reviewed.
5. Disagreements.
6. Required second review.
7. Final release recommendation.
8. Remaining blocker.

### 6. Audit Trail

Minimum fields:

1. Artifact id.
2. Version.
3. Build command or creation route.
4. Validation command.
5. Validator result.
6. Source files.
7. Reviewer status.
8. External action status.
9. Release decision.
10. Next action.

## Release Gate Levels

| Level | Meaning | External use |
| --- | --- | --- |
| L0 concept | Idea or outline only. | Not allowed |
| L1 local build | Local artifact exists and validates. | Not allowed |
| L2 clinician reviewed | At least one clinician review pass recorded. | Still not allowed unless public wording cleared |
| L3 public candidate | License, citation, privacy, source, wording, and second review gates addressed. | Requires Goktug clearance |
| L4 external pilot | Exact external target and use case cleared. | Requires explicit Goktug clearance |
| L5 clinical deployment | Clinical deployment evaluation. | Blocked in this automation |

Current assurance lab state: L1 local build for many artifacts, partial L2 for selected clinician authored items, not L3 public candidate, not L4 pilot, not L5 deployment.

## Sandbox Readiness Packet Structure

If later cleared, a sandbox readiness packet should contain:

1. One page intended use boundary.
2. No patient data statement.
3. Synthetic case generation method.
4. Failure taxonomy.
5. Model and run card.
6. Risk card summary.
7. Source support summary.
8. Clinician review summary.
9. Data quality card.
10. Audit trail.
11. Release gate decision.
12. Explicit statement that it is not clinical deployment.

## Türkiye Route Fit

| Türkiye route | Assurance Lab contribution | Current status |
| --- | --- | --- |
| TÜYZE or TÜSEB | Clinician led health AI safety and evaluation evidence package. | sent only, no acceptance claim |
| TÜBİTAK BİLGEM YZE | Turkish medical LLM evaluation and source support infrastructure. | sent only, no acceptance claim |
| SBSGM or Ministry health route | Risk, source, data quality, and release gate structure for sandbox readiness discussion. | local mapping only |
| TEKNOFEST health AI ecosystem | Data quality and label audit templates. | no affiliation claim |
| TRAI or TOBB ecosystem | Working group style contribution packet. | local target only |

## Claims To Avoid

Do not claim:

1. FDA compliance.
2. EU AI Act compliance.
3. CHAI compliance.
4. WHO endorsement.
5. Ministry approval.
6. TÜYZE, TÜSEB, or BİLGEM acceptance.
7. Regulatory sandbox access.
8. Clinical validation.
9. Patient data use.
10. Model safety.
11. Clinical or institutional release.

## Immediate Next Build

Convert this matrix into:

1. `outputs/tr_medai_safety_suite_v1_20260615/assurance_lab/tplc_governance_matrix_v0_1.md`
2. `outputs/tr_medai_safety_suite_v1_20260615/assurance_lab/tplc_governance_matrix_v0_1.json`
3. A validator that checks card domains, release levels, route fit, and false external gates.

Codex readiness today: public preview file READY and published in this repository. Institutional packet use, clinical deployment, or national route claims are separate targeted actions and are not claimed here.
