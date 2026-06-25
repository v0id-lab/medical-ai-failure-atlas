# Clinical State Language v0.1

Date: 2026 06 25

## Purpose

Clinical State Language gives medical AI systems a compact way to represent the state of a synthetic patient over time. It keeps the model from treating a message as a complete clinical world.

## Fields

### 1. state_id

Stable identifier for one state in a synthetic trajectory.

### 2. timepoint

Where the state sits in the clinical journey.

### 3. patient_voice

Short patient or clinician facing prompt written as synthetic text.

### 4. problem_list

Current clinical problems written as compact labels.

### 5. timeline

Key events in order, including delays and changes.

### 6. missing_data

Variables a model must not silently assume.

### 7. hypotheses

Reasonable possibilities that should stay open.

### 8. evidence_for

Signals that support the current risk framing.

### 9. evidence_against

Signals that weaken or complicate a hypothesis.

### 10. action_boundary

What the model may say without becoming clinical deployment or remote care.

### 11. follow_up_triggers

Signals that should change urgency or route.

### 12. source_support_needed

Where external evidence or official source support would be required before public claims.

## Required Guardrails

1. Every state must be synthetic.
2. Every state must mark patient data use as false.
3. Every state must mark clinical use as false.
4. Every state must name missing data.
5. Every state must state what source support would be needed before a public clinical claim.
