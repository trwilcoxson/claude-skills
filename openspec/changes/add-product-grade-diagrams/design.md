## Approach

Three layers, same split the existing diagram verification already uses (`diagram_checks.py` +
`prompts/diagram-judge.md`): the **skill** renders, the **eval** checks structure, the **judge**
assesses correctness. Generation stays entirely in the LLM.

### Manifest additions (neutral, skill-emitted)

The eval must gate on facts, not infer them. Add to `evals/reliability/schema/`:
- `findings.schema.json`: `kill_chains: [{ id, goal, steps: [TM-id] }]` (optional array). A "kill
  chain" is the LLM's judgment; the eval only requires a tree/flow per declared chain.
- `recon.schema.json`: each trust_boundary gains `kind` (enum: process|network|trust|tenant|cicd|region);
  each external_dep gains optional `manifest` (path in evidence) and `risk` (free string the LLM sets).

These are additive and optional; existing manifests stay valid. The executor prompt is updated to
emit them.

### Precondition derivation (deterministic gates over declared facts)

- attack tree, attack-flow: `len(findings.kill_chains) >= 3`.
- auth sequence: any recon entry_point whose name/evidence matches an auth vocabulary OR any finding
  with `S`/`E` in `stride_lm`. Over-inclusive → may only SKIP, never FAIL on the name match alone.
- STRIDE matrix, heat map: always (any non-empty scored model).
- ATT&CK layer: any finding with a `mitre` id.
- RBAC matrix: ≥2 distinct roles, derived from recon actor metadata / findings, declared by the skill.
- SBOM: `recon.external_deps` non-empty AND a `manifest` present in evidence.

### Rendering (skill)

Canonical constructs, added to `references/`:
- `mermaid-diagrams.md`: attack tree (`flowchart TD`, root + `{AND}`/`{OR}` diamonds + technique
  leaves), auth `sequenceDiagram` (participants = DFD ids, success + `alt` failure, credential `rect`),
  attack-flow (`flowchart`, initial-access → objective).
- new `analytical-visuals.md`: STRIDE-per-element matrix (markdown table), L×I heat map (5×5 markdown
  grid banded by `frameworks.md` thresholds), ATT&CK markdown heatmap + Navigator JSON layer, RBAC
  matrix (roles × resources, anonymous row), SBOM dependency `flowchart`.
- `report-template.md`: sections for the matrices/heatmaps; `SKILL.md` Phase 5/7 + Diagram acceptance
  gate require the applicable visuals.

### Verification (eval)

Extend `diagram_checks.py` with one function per visual, each: (1) evaluate the precondition from the
manifests; (2) if false → skip; (3) if true → presence + shape + consistency checks only, using graph
topology, counts, regex, and set-membership/equality against manifest ids. Reuse the existing
`band()` for heat-map banding (matches `frameworks.md`). Add per-visual results to the same defect
list and the `diagram` stats block; `diagram_pass = no hard defects` unchanged. Extend
`prompts/diagram-judge.md` with the per-visual semantic checks; update `prompts/executor.md` to
require the visuals and emit the new manifest fields.

## Determinism boundary (enforced)

No check decides whether a threat/visual is *correct* — only whether it is present, well-shaped, and
internally consistent with what the LLM declared. Thresholds come from skill-declared facts
(`kill_chains`, `kind`, `manifest`), never from the eval clustering or classifying content. Wrong-but-
present content passes the deterministic layer and is caught only by the judge.

## Risks

- Mermaid parsing is regex-based and approximate; keep checks tolerant (fractions/“substantially”),
  and prefer SKIP over FAIL when a precondition is ambiguous — mirrors the soft-warning approach
  already used for stray untyped edges.
- Old committed runs will newly FAIL the added checks; that is correct (they predate the visuals) and
  is the guard that the checks aren't rubber-stamps.
