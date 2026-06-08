## 1. Manifest facts (skill-emitted, neutral)

- [x] 1.1 Add `kill_chains: [{id, goal, steps}]` to `evals/reliability/schema/findings.schema.json`
- [x] 1.2 Add trust_boundary `kind` enum + external_dep `manifest`/`risk` to `evals/reliability/schema/recon.schema.json`
- [x] 1.3 Update `prompts/executor.md` to emit these fields and to render the new visuals

## 2. Skill rendering

- [x] 2.1 Add attack-tree, auth-sequence, attack-flow render templates to `references/mermaid-diagrams.md`
- [x] 2.2 Add new `references/analytical-visuals.md` (STRIDE matrix, L×I heat map, ATT&CK layer, RBAC matrix, SBOM graph)
- [x] 2.3 Add report-template sections in `references/report-template.md`
- [x] 2.4 Extend `SKILL.md` Phase 5/7 and the Diagram acceptance gate to require the applicable visuals by precondition
- [x] 2.5 Add matching items to `references/analysis-checklists.md`

## 3. Eval verification (structure/consistency only)

- [x] 3.1 Extend `evals/reliability/diagram_checks.py` with per-visual checks, each gated by its precondition over declared facts
- [x] 3.2 Reuse `band()` for the heat map; add per-visual results to the defect list + `diagram` stats
- [x] 3.3 Extend `prompts/diagram-judge.md` with the per-visual semantic checks

## 4. Verify

- [x] 4.1 Smoke `diagram_checks.py` on hand-made manifests: each check fires (missing→defect, present+consistent→pass, precondition false→skip)
- [x] 4.2 Confirm the old committed runs still FAIL the new checks (no rubber-stamping)
- [x] 4.3 Live: re-run the skill on NodeGoat via the eval workflow; confirm the new visuals render and `run.py report` shows the diagram contract green including them; judge confirms correctness
- [ ] 4.4 `openspec validate add-product-grade-diagrams --strict`; commit; archive after merge
