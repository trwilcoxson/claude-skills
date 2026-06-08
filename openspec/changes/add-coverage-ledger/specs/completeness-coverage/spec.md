## ADDED Requirements

### Requirement: Coverage taxonomy
The skill SHALL define a production-grade coverage taxonomy: a tiered, applicability-gated item set
(derived from the production-grade reference) where Tier-1 items always apply and Tier-2 items apply
only when their precondition holds (e.g. AI/ML, multi-tenancy, Kubernetes, mobile, hardware). The
taxonomy is structure — it states what production-grade work should address, not what any specific
system must contain.

#### Scenario: Conditional item
- **WHEN** a system has no AI/ML components
- **THEN** the AI/ML taxonomy items are marked not-applicable rather than expected

### Requirement: Coverage ledger with terminal states
The skill SHALL maintain a coverage ledger (`coverage.json`) that resolves every applicable taxonomy
item to exactly one terminal state: `present`, `partial`, `absent`, `not-applicable`, or `unknown`.
`present`/`partial` SHALL carry a source reference; `absent`/`not-applicable` SHALL carry a reason;
`unknown` SHALL carry a note describing what was searched and why it is undetermined. No applicable
item is left unresolved.

#### Scenario: Found in sources
- **WHEN** an agent finds an item's information in the source materials
- **THEN** it records the item `present` with the detail and a source reference that resolves in the materials

#### Scenario: Not determinable from sources
- **WHEN** an agent cannot determine an item from the available source materials
- **THEN** it records the item `unknown` with a note on what was searched, rather than omitting it

### Requirement: Agents attempt maximum supportable detail
Agents SHALL attempt every applicable item and record the most detailed state the source materials
support; depth is bounded by what is discoverable, not by attention. Each agent updates the ledger
for its domain as the pipeline runs (accumulating shared state).

#### Scenario: Pipeline accumulates coverage
- **WHEN** the reconnaissance and analysis agents run in sequence
- **THEN** each resolves the ledger items in its domain, and by the end every applicable item has a terminal state

### Requirement: Unknowns and partials surface in the report
The skill SHALL lift `unknown`, `partial`, and `absent`-by-gap items from the ledger into the report's
Open Questions / Known Limitations sections, so missing-because-unavailable is tracked, not hidden.

#### Scenario: Open questions populated
- **WHEN** the ledger contains `unknown` items at the end of a run
- **THEN** those items appear as open questions / known limitations in the report with their notes
