# Clinician Severity Layer Product Spec

Date: 2026 06 25

## Purpose

Turn each medical AI failure example into a compact clinician review row that can be judged, revised, and shared without patient data or clinical use claims.

## Required fields

### 1. scenario_scope

What synthetic or public situation is being reviewed.

### 2. user_context

Whether the answer is for patient facing text, clinician support, report language, or maintainer review.

### 3. failure_mode

The smallest named way the answer could mislead, omit context, overstate evidence, or create unsafe action.

### 4. clinical_severity

A bounded grade for potential harm if the failure were trusted.

### 5. missing_variable

The patient, workflow, source, date, guideline, local protocol, or supervision fact that is missing.

### 6. source_support_gap

What source evidence is absent or too weak for the claim being made.

### 7. safe_rewrite

A shorter safer version that reduces the risk without pretending to validate the model.

### 8. reviewer_state

Draft, needs clinician review, needs source support, ready for public example, or blocked.

## Review states

1. Draft
2. Needs clinician review
3. Needs source support
4. Ready for public example
5. Blocked

## Product rule

A row is not ready until it names the failure mode, missing variable, source support gap, safe rewrite, and reviewer state.
