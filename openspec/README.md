# OpenSpec — design & specification

This directory is the **spec-first design** of the threat-model skill and its evaluation harness,
using [OpenSpec](https://github.com/Fission-AI/OpenSpec). Each capability is specified as
`Requirement`s with `Scenario`s (WHEN/THEN) before it is built, so the design is auditable and the
intent is explicit.

## The principle (every capability obeys it)

> The LLM/agents do **all reasoning and generation** — every threat, every visual, every event
> payload. **Determinism lives only in the templates and evals**, to enforce that the structure is
> present and internally consistent (the same *kind* of result each run). Deterministic code never
> scripts or judges the answer.

A recurring corollary: when the eval needs to gate on something, the **skill emits the fact** as a
neutral structured field (declared kill chains, trust-boundary kind, dependency manifest, coverage
state) and the eval checks structure over that fact — it never infers content in code.

## Changes

| Change | Capabilities | Status |
|---|---|---|
| [`add-product-grade-diagrams`](changes/add-product-grade-diagrams/) | `threat-model-visuals`, `diagram-verification` | implemented + verified |
| [`add-pipeline-observability`](changes/add-pipeline-observability/) | `pipeline-observability` | implemented + verified |
| [`add-coverage-ledger`](changes/add-coverage-ledger/) | `completeness-coverage`, `coverage-verification` | proposed |

Each change folder has `proposal.md` (why/what), `specs/<capability>/spec.md` (the
ADDED/MODIFIED requirement deltas), `design.md` (technical approach + the determinism boundary), and
`tasks.md` (implementation checklist with status).

## Capability map

- **threat-model-visuals** — the visuals the skill renders (the 8 product-grade additions + the DFD
  layers), each gated by a precondition, plus the neutral facts the skill emits for verification.
- **diagram-verification** — the deterministic, structure-only checks per visual (presence / shape /
  consistency against the manifests) and the diagram judge's correctness assessment.
- **pipeline-observability** — the `tm.run-event/1` stream (a projection of each persona's Execution
  Log) and the pure `tm-observe` renderer ("what agent is doing what").
- **completeness-coverage** — the coverage taxonomy + ledger: agents attempt every applicable
  production-grade item and record `present(+source)` / `partial` / `absent` / `not-applicable` /
  `unknown(+note)`; unknowns surface as open questions.
- **coverage-verification** — structure-only checks that every applicable item reached a terminal
  state (the agent tried), `present` is grounded, `unknown` is noted; never requires a specific item
  present.

## Working with it

```bash
openspec list                              # active changes + task progress
openspec view                              # interactive dashboard
openspec show add-product-grade-diagrams   # a proposal + its spec deltas
openspec validate <change> --strict        # validate a change
openspec archive <change>                  # after merge: fold deltas into specs/
```

Implementation lives in `../skills/threat-model/` (the skill: `SKILL.md` + `references/`) and
`../skills/threat-model/evals/reliability/` (the harness: `diagram_checks.py`, `events.py`,
`tm_observe.py`, `coverage_checks.py`, schemas, prompts, `sample-runs/`).
