# Agentic Medicine Sandbox v0.1

Date: 2026 06 25

## Purpose

The sandbox frames medical AI as a process. The model must listen, maintain state, request data, check sources, hand off, and update when the trajectory changes.

## Agent Roles

### 1. patient simulator

Provides synthetic patient messages and changes over time.

### 2. clinician reasoner

Maintains problem representation and next safe action boundary.

### 3. test result emitter

Releases structured labs, vitals, imaging summaries, or missing result notices.

### 4. source support checker

Flags claims that need guideline, paper, policy, or official source support.

### 5. consultant simulator

Adds specialty constraints without giving real patient advice.

### 6. follow up monitor

Checks whether the plan updates when the state changes.

## First Loop

1. Patient simulator emits a synthetic state.
2. Clinician reasoner builds a Clinical State Language row.
3. Test result emitter changes one state variable.
4. Medical Reasoning Verifier checks the model response.
5. Follow up monitor checks whether the next step changed.

## Boundary

This sandbox is for research, representation, and evaluation design. It is not clinical deployment, medical advice, diagnosis, treatment, or triage.
