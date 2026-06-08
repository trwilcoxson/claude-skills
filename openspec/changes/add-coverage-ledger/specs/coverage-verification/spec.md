## ADDED Requirements

### Requirement: Structural completeness, not prescribed presence
The eval SHALL verify that every applicable taxonomy item has a terminal state (no `pending`/blank —
the agent attempted it). It SHALL NOT require any specific item to be `present`, because availability
varies by source material; there is no answer key.

#### Scenario: Item left unresolved
- **WHEN** an applicable taxonomy item has no terminal state in the ledger
- **THEN** the check records a defect (the agent did not attempt it)

#### Scenario: Item honestly unknown
- **WHEN** an applicable item is `unknown` with a note
- **THEN** the check passes for that item (honest gap, not a failure)

### Requirement: Grounding of present claims and noted unknowns
The eval SHALL verify that every `present`/`partial` item cites a source reference that resolves in
the materials, every `unknown` carries a note, and every `absent`/`not-applicable` carries a reason.

#### Scenario: Ungrounded present
- **WHEN** an item is `present` but its source reference does not resolve in the materials
- **THEN** the check records a defect

### Requirement: Applicability consistency
The eval SHALL verify the ledger's applicability is consistent with the declared facts (recon/findings):
a Tier-2 item marked applicable when its precondition is false, or marked not-applicable when its
precondition is true, is a defect.

#### Scenario: Inconsistent applicability
- **WHEN** the recon declares multi-tenancy but the multi-tenancy items are marked not-applicable
- **THEN** the check records a defect

### Requirement: Coverage profile
The eval SHALL compute and report a coverage profile — counts/fraction by state over the applicable
items (the "best/most detail it can be" measure) — without turning `unknown` into a failure.

#### Scenario: Profile reported
- **WHEN** the ledger is scored
- **THEN** the report shows applicable item counts by state and the present-with-evidence fraction

### Requirement: Judge assesses state correctness
A judge SHALL assess whether the ledger states are correct against the real system — whether a
`not-applicable` truly does not apply, an `absent` is genuinely absent (a missed-finding check), and a
`present` detail is accurate — separately from the deterministic structural checks.

#### Scenario: Judging a not-applicable
- **WHEN** the judge reviews an item marked not-applicable
- **THEN** it confirms the item genuinely does not apply or flags it as a missed gap
