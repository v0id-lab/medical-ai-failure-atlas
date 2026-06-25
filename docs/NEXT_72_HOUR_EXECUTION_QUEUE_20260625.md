# Next 72 Hour Execution Queue

Date: 2026 06 25

## Queue

### Q1. Severity

Action: Convert ten existing safe failure cards into severity layer rows.

Deliverable: Severity row pack

Gate: No patient data and no clinical use claim.

### Q2. Severity

Action: Add a validator that requires every severity row to include missing variable and safe rewrite fields.

Deliverable: Severity row validator

Gate: Fail if any row claims clinical validation.

### Q3. Source

Action: Map SourceCheckup rows to the severity fields where source support changes the risk.

Deliverable: Source support crosswalk

Gate: Do not certify source truth.

### Q4. Turkish context

Action: Pick twelve Turkish clinical wording risks from existing TR MedLLM surfaces.

Deliverable: Turkish wording risk queue

Gate: Use synthetic examples only.

### Q5. Turkish context

Action: Create a one page path for TEKNOFEST teams from model result to claim hygiene gate.

Deliverable: Report wording path

Gate: No finalist, official role, or competition claim.

### Q6. Public review

Action: Add issue 154 routing language that sends comments to severity, source, wording, or claim hygiene.

Deliverable: Issue route note

Gate: No comment is called validation.

### Q7. Open source eval

Action: Keep lighteval and inspect ai route states fresh with public preflight before public language.

Deliverable: Route refresh

Gate: No acceptance or merge claim.

### Q8. Open source eval

Action: Write the next lm eval scope card only after the current PR states are checked.

Deliverable: Eval scope card

Gate: No new upstream comment without fresh reason.

### Q9. README

Action: Make the first screen point to the new north star and the public objection route.

Deliverable: README navigation patch

Gate: Keep boundaries visible.

### Q10. Validation

Action: Add one Makefile target per new public system and require it in validate.

Deliverable: Makefile guard

Gate: Generated docs must not be stale.

### Q11. Proof

Action: Track PR 156 as the public acceleration proof path.

Deliverable: Proof ledger update

Gate: Draft PR is not merge or acceptance.

### Q12. BAGLAM2

Action: Record only commit, PR, checks, blocker, and next action.

Deliverable: BAGLAM2 result note

Gate: Do not add routine no event logs.
