# Clinical Intelligence Stack Manifesto

Date: 2026 06 25

## Thesis

Medical AI needs a clinical intelligence stack, not another chatbot benchmark.

Medical AI teams already know how to make a model answer. The next hard problem is to make a system represent a patient state, track change, choose what it still does not know, and hand work to the right tool or human.

## Position

A clinician built open system for representing patient state, patient trajectories, reasoning quality, tool use, source support, and multilingual clinical context.

## Why Now

1. Health AI evaluation is moving from exam style tasks toward realistic conversations, clinical workflows, and physician rubrics.
2. Reasoning model teams need verifiers and environments outside math and code.
3. Clinical AI agents need patient state, time, missing data, tests, source checks, and follow up loops rather than one answer.
4. Turkish medical AI has visible official and competition routes, but it still lacks a public clinical intelligence infrastructure layer.

## First Build

Clinical state schema: `data/clinical_state_language_v0_1_20260625.schema.json`

Synthetic trajectory seed rows: `data/clinical_trajectory_seed_set_v0_1_20260625.jsonl`

Trajectory count: 20

## Stack Layers

### Clinical State Language

Job: Represent a patient state as problems, timeline, missing data, hypotheses, evidence, risk, action boundary, follow up signal, and source support.

First artifact: `data/clinical_state_language_v0_1_20260625.schema.json`

### Clinical Trajectory Engine

Job: Generate synthetic patient journeys across timepoints so models handle change, delay, deterioration, response, and follow up.

First artifact: `data/clinical_trajectory_seed_set_v0_1_20260625.jsonl`

### Medical Reasoning Verifier

Job: Check whether a model saw missing variables, handled uncertainty, sequenced actions, kept source support clean, and avoided unsupported clinical claims.

First artifact: `docs/MEDICAL_REASONING_VERIFIER_V0_1_20260625.md`

### Agentic Medicine Sandbox

Job: Simulate a clinical process with patient, clinician, test, source check, consultant, and follow up agents.

First artifact: `docs/AGENTIC_MEDICINE_SANDBOX_V0_1_20260625.md`

### Multilingual Medical Intelligence

Job: Treat Turkish clinical language and health system context as a clinical reality layer rather than translation.

First artifact: `docs/CLINICAL_INTELLIGENCE_STACK_MANIFESTO_20260625.md`

### Medical Intelligence Atlas

Job: Publish field notes, diagrams, trajectory examples, and model behavior analysis in Turkish and English.

First artifact: `docs/CLINICAL_INTELLIGENCE_STACK_MANIFESTO_20260625.md`

## Source Anchors

### CIS001 OpenAI HealthBench

URL: https://openai.com/index/healthbench/

Claim support: HealthBench frames health AI evaluation around realistic health scenarios and physician expert judgement.

Use in stack: Supports physician judged realistic conversation and rubric driven evaluation.

### CIS002 Stanford MedHELM

URL: https://medhelm.org/

Claim support: MedHELM organizes medical model evaluation around 121 clinical tasks in a clinician validated taxonomy.

Use in stack: Supports a broader clinical task map instead of one leaderboard.

### CIS003 AgentClinic

URL: https://arxiv.org/abs/2405.07960

Claim support: AgentClinic evaluates models in simulated clinical environments with interaction, incomplete information, tools, and multiple specialties.

Use in stack: Supports the need for agentic clinical process simulation.

### CIS004 DeepSeek R1

URL: https://arxiv.org/abs/2501.12948

Claim support: DeepSeek R1 shows the centrality of reasoning, reinforcement learning, verification, self reflection, and dynamic strategy adaptation.

Use in stack: Supports medical reasoning verifiers as a valuable contribution for model teams.

### CIS005 Google MedGemma

URL: https://developers.google.com/health-ai-developer-foundations/medgemma

Claim support: MedGemma is presented as a developer model that requires validation on the intended use case and likely adaptation.

Use in stack: Supports use case specific validation and adaptation kits.

### CIS006 DT GPT digital twin trajectory work

URL: https://www.nature.com/articles/s41746-025-02004-3

Claim support: The paper frames longitudinal patient forecasting and digital twins as a next generation clinical AI direction.

Use in stack: Supports patient trajectory representation.

### CIS007 EHRWorld

URL: https://arxiv.org/html/2602.03569v1

Claim support: EHRWorld uses the medical world model frame for long horizon clinical trajectories.

Use in stack: Supports patient centric world model language.

### CIS008 Turkiye official health AI route

URL: https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html

Claim support: The official department page defines health AI and innovative technology duties including problem identification, solution production, collaboration, and education materials.

Use in stack: Supports the national route context without claiming partnership.

## Boundaries

1. No clinical validation claim.
2. No clinical deployment claim.
3. No patient data use claim.
4. No model superiority claim.
5. No medical advice claim.
6. No diagnosis claim.
7. No treatment recommendation claim.
8. No regulatory clearance claim.
9. No institutional approval claim.
10. No partner commitment claim.
11. No endorsement claim.
12. No publication acceptance claim.

## Build Command

`make clinical_intelligence_stack`
