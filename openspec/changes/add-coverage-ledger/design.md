## Approach

Generalize the existing `visual-completeness-checklist.md` (26 diagram categories, each
APPLICABLE/NOT-APPLICABLE + evidence) to the whole production-grade taxonomy, made machine-readable.

### Taxonomy (`references/coverage-taxonomy.md` + machine list)

The 54-section reference encoded as items at a reviewer-meaningful granularity (~150–250 items, not
every leaf bullet), each with: `id`, `section`, `tier` (1 always / 2 conditional), `precondition`
(for Tier-2: the recon/findings fact that makes it applicable, e.g. `ai_ml`, `multi_tenant`, `k8s`,
`mobile_client`, `hardware`, `third_party`), and the sub-fields it expects. Tier-1 covers the core
checklist (system context, assets, data classification, actors, trust boundaries, entry/exit points,
auth/authz, logging/detection, threats, controls, risk, invariants, evidence, residual risk).

### Ledger (`coverage.json`, schema in `evals/reliability/schema/coverage.schema.json`)

```json
{ "items": [
  { "id": "data-classification.payment-data", "state": "present",
    "detail": "PAN stored in vault, KMS at rest", "source": ["app/data/card-dao.js"], "note": "" },
  { "id": "multi-tenancy.isolation-model", "state": "unknown",
    "detail": "", "source": [], "note": "no tenancy code found; single-tenant assumed but unconfirmed" }
] }
```
- `state` ∈ `present|partial|absent|not-applicable|unknown`.
- `present`/`partial` → `source[]` (paths/strings that resolve in the materials, reusing the grounding
  resolver in `checks.py`); `unknown` → `note`; `absent`/`not-applicable` → `note` (reason).
- Initialized from the taxonomy (all `pending`); agents resolve items in their domain; the
  validation-specialist confirms none remain `pending` and writes the coverage profile.

### Verification (`evals/reliability/coverage_checks.py`, same family as `diagram_checks.py`)

Structure/consistency only: every applicable item has a terminal state (defect on `pending`);
`present`/`partial` source resolves (reuse `_resolves_in_repo`); `unknown` has a note; applicability
matches declared facts; never requires a specific item present. Emits a coverage profile (counts by
state, present-with-evidence fraction). A coverage judge prompt assesses state correctness (n/a really
n/a, absent really absent, present accurate).

### Agentic flow

- Phase 1: recon agent seeds the ledger and resolves context/assets/data/actors/trust/network/entry-
  exit items.
- Phases 3–6: analysis agents resolve threats/controls/risk/invariants/attack-paths/evidence items.
- Final coverage pass (validation-specialist): no `pending`; lift `unknown`/`partial`/`absent`-gap into
  the report's Open Questions / Known Limitations; write the coverage profile to `pipeline-summary.md`.

## Determinism boundary

Deterministic: the item set, the allowed states, "every applicable item terminal," "`present` cites a
resolving source," "`unknown` has a note," applicability-vs-facts consistency, the profile. The eval
enforces *effort + honesty + grounding*, not the presence of any particular content. Non-deterministic:
the state, detail, evidence, analysis. Judge: correctness of the states.

## Notes / risks

- `unknown` is first-class and never a failure — that is the mechanism for "they won't always have
  access to it." Penalize only `pending` (didn't try) and ungrounded `present`.
- Granularity is the main tuning knob; start at section→key-items, tighten with use. Keep the taxonomy
  versioned so coverage is comparable across runs.
- Composes with diagrams: visual items reference the diagram checks rather than duplicating them.
