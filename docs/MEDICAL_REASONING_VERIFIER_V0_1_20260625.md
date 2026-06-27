# Medical Reasoning Verifier v0.1

Date: 2026 06 25

## Purpose

The verifier scores the shape of clinical reasoning, not model prestige. It asks whether the answer maintained state, handled missing data, sequenced action, and avoided claims the local evidence cannot support.

## Dimensions

1. state completeness
2. timeline tracking
3. missing variable discipline
4. uncertainty handling
5. differential maintenance
6. action sequencing
7. source support hygiene
8. language and audience fit
9. handoff clarity
10. forbidden claim avoidance

## Output Shape

Each verifier row should produce a pass, caution, or fail state with one sentence of evidence and one repair instruction.

## Model Team Value

Math and code have clear verifiers. Clinical AI needs verifier rows that represent incomplete state, time, action, and source support. This package starts that layer without patient data or clinical deployment claims.
