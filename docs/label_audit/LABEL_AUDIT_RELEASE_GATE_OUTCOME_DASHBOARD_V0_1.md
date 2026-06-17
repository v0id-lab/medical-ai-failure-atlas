# Label audit release gate outcome dashboard v0.1

Status: generated public preview.

Date: 2026 06 17

This dashboard summarizes pass and block outcomes across label audit release gate rows.

It is not proof of dataset quality, not clinical advice, not patient data, not raw model output release, not clinical deployment, not clinical validation, not a model safety claim, not a model ranking, not regulatory approval, and not an official endorsement.

## Summary

Outcome rows: 5

Pass state rows: 5

Block state rows: 0

Release decision values represented: 1

Release decision: `allowed_for_public_preview`

## Outcome rows

### LAGO001

Release gate id: `LARG001`

Gate name: Synthetic provenance gate

Current state: `pass`

Release decision: `allowed_for_public_preview`

Required public wording: synthetic example only

Blocked wording: covers real care records

Evidence surface: Health data quality card

Next action: keep public preview wording

### LAGO002

Release gate id: `LARG002`

Gate name: Label definition review gate

Current state: `pass`

Release decision: `allowed_for_public_preview`

Required public wording: pending clinician review

Blocked wording: clinically validated labels

Evidence surface: Label definition lock

Next action: keep public preview wording

### LAGO003

Release gate id: `LARG003`

Gate name: Pilot subset scope gate

Current state: `pass`

Release decision: `allowed_for_public_preview`

Required public wording: protocol testing only

Blocked wording: representative of deployment performance

Evidence surface: Platform dashboard

Next action: keep public preview wording

### LAGO004

Release gate id: `LARG004`

Gate name: Raw output release gate

Current state: `pass`

Release decision: `allowed_for_public_preview`

Required public wording: raw outputs are withheld

Blocked wording: raw outputs are available in public

Evidence surface: Public release boundary

Next action: keep public preview wording

### LAGO005

Release gate id: `LARG005`

Gate name: Dataset quality proof gate

Current state: `pass`

Release decision: `allowed_for_public_preview`

Required public wording: dataset quality is not proven

Blocked wording: proves dataset quality

Evidence surface: Release note

Next action: keep public preview wording

## Public files

1. Outcome dashboard JSON: `docs/label_audit/label_audit_release_gate_outcome_dashboard_v0_1.json`
2. Release gate checklist: `docs/label_audit/LABEL_AUDIT_RELEASE_GATE_CHECKLIST_V0_1.md`
3. Public wording decision log: `docs/label_audit/LABEL_AUDIT_PUBLIC_WORDING_DECISION_LOG_V0_1.md`
4. Health data quality card: `docs/HEALTH_DATA_QUALITY_AND_LABEL_AUDIT_CARD_V0_1.md`

## Runnable check

Run:

```bash
make label_audit_outcome_dashboard
```
