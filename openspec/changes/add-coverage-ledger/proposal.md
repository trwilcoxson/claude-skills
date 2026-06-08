## Why

A production-grade threat model must let a reviewer answer a long, known set of questions (what
exists, who can touch it, what data moves, where trust changes, what can go wrong, what controls
exist, how they're verified, what residual risk remains). Today the skill produces good analysis but
does not systematically (a) attempt every item that production-grade work expects, (b) record, per
item, whether it was found, is absent, is not applicable, or **could not be determined from the
available sources**, or (c) ground each "found" claim in a source. So gaps are silent and depth
depends on attention rather than on what the source materials actually support.

## What Changes

- Add a **coverage taxonomy**: the production-grade item set (built from the 54-section reference),
  tiered and applicability-gated, as machine-readable structure.
- Agents SHALL maintain a **coverage ledger** (`coverage.json`) resolving every applicable item to a
  terminal state — `present` (+ source evidence), `partial`, `absent` (+ reason), `not-applicable`
  (+ reason), or `unknown` (+ note on what was searched) — accumulated across the pipeline.
- `unknown`/`partial` items SHALL surface as Open Questions / Known Limitations in the report (not be
  omitted), so missing-because-unavailable is tracked, not hidden.
- The eval SHALL verify the ledger **structurally**: every applicable item has a terminal state (no
  blanks — the agent tried), every `present` cites a source that resolves, every `unknown` carries a
  note, applicability is consistent. It computes a coverage profile but never requires a specific
  item to be present (availability varies — no answer key).
- The diagram visuals and component/flow/trust metadata become items in the ledger; the existing
  `visual-completeness-checklist` is the prototype this generalizes.

The boundary holds: the taxonomy/ledger schema and completeness/grounding enforcement are
deterministic; the per-item state, detail, and evidence are the agents' reasoning; correctness of the
states is the judge's.

## Capabilities

### New Capabilities
- `completeness-coverage`: the coverage taxonomy + ledger the skill maintains (states, evidence,
  open-question surfacing), and how agents fill it across the flow.
- `coverage-verification`: the deterministic structural checks over the ledger (terminal state per
  applicable item, grounded `present`, noted `unknown`, applicability consistency) and the coverage
  profile; plus the judge's assessment of state correctness.

### Modified Capabilities
<!-- composes with threat-model-visuals / diagram-verification; no requirement changes to them -->

## Impact

- New: `references/coverage-taxonomy.md` (the item set), `evals/reliability/schema/coverage.schema.json`,
  coverage checks in `evals/reliability/` (a `coverage_checks.py` in the `diagram_checks.py` family),
  a coverage judge prompt.
- Modified: `SKILL.md` (agents initialize + fill the ledger; final coverage pass; Open-Questions/
  Limitations sourced from it), `prompts/executor.md` (emit `coverage.json`), `references/report-template.md`.
- Generalizes `visual-completeness-checklist.md`; reuses the grounding discipline already in
  `checks.py`/`diagram_checks.py`.
