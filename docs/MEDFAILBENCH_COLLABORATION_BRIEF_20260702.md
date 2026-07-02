# MedFailBench collaboration brief — 2026-07-02

## One-line positioning

MedFailBench is a clinician-built open-source benchmark for inspecting medical AI failure modes before clinical-sounding model outputs become trusted language.

## Why this is different

Most medical AI benchmarks ask whether a model knows the right answer. MedFailBench asks a different question: what safety boundary failed?

Examples:

- missed urgent escalation
- unsafe remote dosing or protocol detail
- unsupported guideline certainty
- weak source support
- vague safety-net wording
- Turkish clinical wording risk

## Current public artifacts

- GitHub repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
- Hugging Face Space: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas
- Live app: https://goktugozkanmd-medical-ai-failure-atlas.hf.space
- Weekly real model response preview: `docs/MEDFAILBENCH_WEEKLY_MODEL_RESPONSE_EVAL_20260702.md`
- Taxonomy: `docs/SAFETY_GATE_TAXONOMY_V0_2.md`
- Clinical severity rubric: `docs/CLINICAL_SEVERITY_RUBRIC_V0_2.md`

## What is ready now

- Synthetic-only public case set.
- Clinician-authored safety gates.
- Hugging Face leaderboard preview.
- Model submission form.
- Contribution guide and issue templates.
- First real model response evaluation preview across 3 models and 5 hard prompts.

## What this is not

- Not clinical advice.
- Not clinical validation.
- Not a model ranking.
- Not patient data.
- Not an institutional endorsement.

## Collaboration ask

I am looking for narrow review, not broad endorsement.

Best first contribution:

1. Pick one synthetic case or one safety gate.
2. Say whether the failure boundary is clinically meaningful.
3. Suggest safer wording or a missing variable.
4. If useful, submit a synthetic case through GitHub issues.

## Fit for Ali / TR-MMLU style discussion

Use MedFailBench as a clinical safety layer, not as a replacement for general knowledge benchmarks.

Possible integration:

- TR-MMLU checks language and knowledge performance.
- MedFailBench checks clinical safety boundaries and wording risk.
- SourceCheckup checks whether claims are supported by real sources.

## Fit for Kyoto / academic meeting

Position as a clinician-led research artifact for medical AI evaluation, multilingual clinical risk, and safety taxonomy design.

Useful discussion question:

> How should clinical safety boundaries be represented in medical LLM evaluation beyond exam accuracy?

## Fit for Acıbadem CASE / hospital AI literacy

Position as a teaching and review tool for clinicians evaluating AI outputs.

Practical use:

- show one unsafe answer
- identify the failed boundary
- rewrite the answer safely
- discuss why a polished answer can still be unsafe

## Next artifact

A 2-page technical note should convert this into a preprint-style methods outline:

- benchmark design
- synthetic-only data boundary
- safety gate taxonomy
- severity scoring
- real model response preview
- limitations
