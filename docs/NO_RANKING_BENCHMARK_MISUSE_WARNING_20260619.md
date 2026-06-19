# No Ranking Benchmark Misuse Warning

Date: 2026 06 19

Status: public benchmark misuse warning.

Purpose: convert the MedHELM HealthBench BRIDGE Compatibility Note and the Hospital AI Governance Intake Worksheet into a public warning against using benchmark scores as safety proof.

This warning is not a benchmark result, not model comparison, not ranking, not leaderboard, not score certification, not procurement evidence, not clinical validation, not clinical deployment, not patient data, not an official MedHELM, HealthBench, BRIDGE, OpenAI, CHAI, Joint Commission, hospital, university, regulator, vendor, or partner statement, not payment, and not terms acceptance.

## Source anchors

1. MedHELM

Source: https://medhelm.org/

Use in this warning: benchmark reports need task context, clinical workflow context, calibration, robustness, writing style, and reviewer role before public safety language is used.

2. OpenAI HealthBench

Source: https://openai.com/index/healthbench/

Use in this warning: rubric based health evaluations can improve model assessment, but public reporting still needs leakage control, source support, uncertainty, and careful wording.

3. BRIDGE

Source: https://github.com/YLab-Open/BRIDGE

Use in this warning: multilingual clinical text evaluation needs language, specialty, document type, care stage, access, and data boundary context before broad safety claims are made.

4. CHAI AI Governance

Source: https://www.chai.org/workgroup/cross-cutting/ai-governance

Use in this warning: public benchmark language should sit inside governance lanes such as policy, structure, lifecycle, risk, data, third party review, education, and feedback.

5. CHAI draft responsible health AI framework release

Source: https://www.chai.org/blog/chai-releases-draft-responsible-health-ai-framework-for-public-comment

Use in this warning: public reporting should focus on risk, evidence, lifecycle, and uncertainty rather than score certification or deployment claims.

## Misuse patterns

### 1. Score becomes safety proof

Public warning: a high benchmark score does not prove safe use in a clinical workflow.

Reviewer question: what exact task, user, care setting, failure mode, and human review route were checked.

Required evidence: task map, risk note, reviewer role, failure mode row, release boundary.

Blocked claim: safety proof.

### 2. Leaderboard becomes procurement evidence

Public warning: a leaderboard position is not procurement evidence for a hospital, clinic, payer, university, or public program.

Reviewer question: what local governance, data, cost, vendor, monitoring, and accountability records exist.

Required evidence: governance intake row, third party review, data boundary note, maintenance owner.

Blocked claim: procurement readiness.

### 3. Benchmark pass becomes clinical validation

Public warning: passing a benchmark is not clinical validation and does not show patient outcome benefit.

Reviewer question: what prospective or retrospective clinical validation was actually performed and by whom.

Required evidence: validation protocol, reviewer credentials, study setting, outcome definition, audit record.

Blocked claim: clinical validation.

### 4. Public demo becomes deployment readiness

Public warning: a public demo can show behavior, but it does not show operational readiness.

Reviewer question: who owns monitoring, correction, escalation, and retirement after release.

Required evidence: lifecycle route, monitoring plan, correction route, escalation owner, stop condition.

Blocked claim: deployment readiness.

### 5. Single language score hides Turkish readiness

Public warning: a score in one language does not prove Turkish medical readiness.

Reviewer question: what Turkish terminology, specialty, setting, abbreviation, and patient communication cases were reviewed.

Required evidence: Turkish language scope, terminology review, specialty spread, clinician review question.

Blocked claim: Turkish representativeness.

### 6. Specialty average hides care stage risk

Public warning: an average score can hide failures in emergency, chronic care, discharge, triage, or medication stages.

Reviewer question: which specialty, document type, and care stage produced the risk.

Required evidence: specialty label, document type label, care stage label, stratified risk note.

Blocked claim: broad medical coverage.

### 7. Source support is missing

Public warning: a medically fluent answer is not safe if the source claim cannot be checked.

Reviewer question: which claim needs a source and what level of support exists.

Required evidence: SourceCheckup row, source URL, support state, uncertainty state, blocked wording.

Blocked claim: source truth certification.

### 8. Health data quality is unreviewed

Public warning: benchmark reporting without label provenance, missingness, leakage, and access context can hide data risk.

Reviewer question: what is known about data origin, label source, missing fields, leakage risk, and regulated access limits.

Required evidence: data quality card, label audit row, leakage statement, access boundary.

Blocked claim: patient data clearance.

### 9. Human review role is absent

Public warning: automated scoring without a visible clinical reviewer role is not a safety conclusion.

Reviewer question: who can interpret the result, challenge it, and stop public safety language.

Required evidence: reviewer role table, disagreement route, adjudication question, release gate.

Blocked claim: clinician endorsed safety.

### 10. Example leakage or benchmark contamination is unclear

Public warning: public examples, prompts, answers, or hidden test content can contaminate future evaluation.

Reviewer question: has the artifact avoided protected examples, answer keys, hidden prompts, and copied test rows.

Required evidence: example protection statement, public safe summary, contamination check, release note.

Blocked claim: clean benchmark evidence.

## Minimum pass condition

Do not publish benchmark based safety language unless each score or result is paired with task context, source support, data boundary, clinical reviewer role, uncertainty, and an explicit no ranking boundary.

## Stop conditions

Stop the public claim if any of these are true:

1. A score is described as safety proof.
2. A leaderboard is described as procurement evidence.
3. A benchmark pass is described as clinical validation.
4. A demo is described as deployment readiness.
5. Turkish readiness is implied without Turkish review.
6. Specialty or care stage risk is hidden behind an average.
7. A medical claim has no source support state.
8. Data quality and leakage are not reviewed.
9. Human review role is absent.
10. Benchmark examples or answers are copied into public text.

## Public next use

1. Pair with the Hospital AI Governance Intake Worksheet.
2. Pair with the MedHELM HealthBench BRIDGE Compatibility Note.
3. Use before public release, proposal, outreach, benchmark note, score language, or safety report.
4. Use as a reviewer handoff card when a team wants to cite benchmark performance without overclaiming.

## Runnable check

```bash
make no_ranking_benchmark_misuse_warning
```
