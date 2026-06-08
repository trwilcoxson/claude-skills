## Why

The threat-model skill produces a strong DFD set but its visual suite is not product-grade: a gap
analysis found spec-required visuals that don't render (attack tree, auth sequence) and several
expected visuals missing entirely (STRIDE-per-element matrix, Likelihood×Impact risk heat map, MITRE
ATT&CK technique layer, attack-flow/kill-chain graph, RBAC matrix, SBOM/dependency graph). The
reliability eval never checked these, so the central artifact drifted while every other check passed.

## What Changes

- The skill SHALL render eight additional analytical/communication visuals, each gated by a
  precondition derived from the assessment so it is produced only when applicable.
- The skill SHALL emit a few neutral structured facts (declared kill-chains, trust-boundary kind,
  dependency manifest reference) so the eval can gate and verify on facts the LLM produced rather than
  inferring content in deterministic code.
- The reliability eval SHALL deterministically verify the presence, shape, and internal consistency
  of each visual (never its content correctness), and the diagram judge SHALL assess correctness.
- The skill's Diagram acceptance gate SHALL require the applicable visuals before a model is finalized.

The boundary is firm: the LLM generates every visual; deterministic eval code only enforces structure
and consistency (the same kind of result each run).

## Capabilities

### New Capabilities
- `threat-model-visuals`: the visuals the skill produces (the eight additions + their preconditions
  and the neutral facts it emits to make verification possible).
- `diagram-verification`: the deterministic structure/consistency checks the eval enforces for each
  visual, plus the semantic correctness the diagram judge assesses.

### Modified Capabilities
<!-- none: the reliability harness has no committed OpenSpec baseline; these are new capabilities. -->

## Impact

- Skill: `SKILL.md` (Phase 5/7, Diagram acceptance gate), `references/mermaid-diagrams.md`,
  new `references/analytical-visuals.md`, `references/report-template.md`.
- Eval: `evals/reliability/diagram_checks.py`, `schema/findings.schema.json`, `schema/recon.schema.json`,
  `prompts/diagram-judge.md`, `prompts/executor.md`.
- No change to the structure/consistency/grounding/coverage layers already enforced.
