# Mermaid Diagram Review Checklist

Pre-submission quality gates for all Mermaid diagrams. Run this checklist before rendering to PNG and before including diagrams in the final report.

**References**: [mermaid-spec.md](mermaid-spec.md) for rules, [mermaid-layers.md](mermaid-layers.md) for layer requirements.

---

## 1. Structural Integrity

- [ ] Every component from Phase 1 reconnaissance appears as a node
- [ ] Every data flow from reconnaissance is represented as an edge
- [ ] No orphaned nodes (every node has at least one connection)
- [ ] Trust boundaries match security zones described in reconnaissance
- [ ] Edge directionality reflects actual data flow direction
- [ ] External entities visually distinguished from internal components
- [ ] Node IDs are consistent across all layers (same component = same ID)

## 2. Edge Typing Compliance

- [ ] **Every** edge has a typed label — no bare `-->` without label text
- [ ] Edge prefixes match the 8-type spec: (none), `[CTRL]`, `[AUTH]`, `[KEY]`, `[ADMIN]`, `[ASYNC]`, `[REPL]`, `[BUILD]`
- [ ] Edge line styles match their type (solid `-->`, dashed `-.->`, thick `==>`, circle `--o`)
- [ ] `linkStyle` colors applied for AUTH (blue), ADMIN (red), ASYNC (green), REPL (purple), BUILD (orange)
- [ ] Edge labels include protocol, data description, and sensitivity classification
- [ ] Encryption state (`[ENC]`/`[PLAIN]`) annotated where applicable (especially L3)

## 3. Symbol Compliance

- [ ] Shapes match the taxonomy: rectangles for externals, stadiums for processes, cylinders for data stores, diamonds for identity/decisions, hexagons for secrets, subroutines for controls, parallelograms for pipelines
- [ ] classDef classes correctly applied to each node type
- [ ] Tier 2 symbols (identity, secrets, control, pipeline, externalDep) used where applicable
- [ ] Tier 3 symbols (outOfScope, tenant/region boundaries) used only when relevant

## 4. Accessibility

- [ ] `flowchart TD` or `flowchart LR` — direction is consistent (no mixing without rationale)
- [ ] Legend subgraph present at the bottom with all symbols, edges, and risk classes used
- [ ] Version stamp comment present: `%% Version: {date} | Phase: {N} | System: {name}`
- [ ] Density within limits: ≤15 nodes per subgraph, ≤25 nodes total (split if exceeded)
- [ ] Node labels ≤4 lines, edge labels ≤1 line
- [ ] Risk colors work for deuteranopia (red-green colorblind) — verified by saturation difference

## 5. Layer Compliance

- [ ] Correct layer content separation (L1 = topology, L2 = trust/identity, L3 = data, L4 = threats)
- [ ] L1/L2/L3 use only neutral/structural styling — no risk colors
- [ ] L4 applies risk classes based on validated findings (highest severity per component)
- [ ] `:::noFindings` used for components with no validated threats (NOT `:::lowRisk`)
- [ ] `:::lowRisk` used only when analysis explicitly confirms low risk
- [ ] Attack path overlays (`==>` with red `linkStyle`) appear only in L4
- [ ] Filename convention followed: `{name}-L{N}-{layer}.mmd`
- [ ] For small systems (≤5 components): 2-layer approach acceptable (L1+L4)
- [ ] For large systems (>20 components): sub-diagrams created with cross-references

## 6. Annotation Format (L4 Only)

- [ ] Enriched node labels follow format: `Name\nTech\n⚠ STRIDE · LxI=Score BAND\nCWE IDs`
- [ ] STRIDE categories use single-letter abbreviations (S,T,R,I,D,E,LM)
- [ ] LxI calculation is correct (Likelihood × Impact = Score)
- [ ] BAND matches the score (CRITICAL 20-25, HIGH 12-19, MEDIUM 6-11, LOW 1-5)
- [ ] CWE IDs are verified against `references/frameworks.md`
- [ ] Ownership markers present where applicable (`[team:X]`, `[managed]`, `[vendor:X]`)
- [ ] No `note right of` syntax used (invalid in flowchart mode)

## 7. Post-Render Verification

After rendering to PNG with `npx -y @mermaid-js/mermaid-cli`:

- [ ] PNG file size >100 bytes (67 bytes = placeholder stub, not a real render)
- [ ] All nodes visible and readable at 100% zoom
- [ ] Edge labels not truncated or overlapping
- [ ] Subgraph labels visible and correctly positioned
- [ ] Legend renders cleanly without overlapping diagram content
- [ ] No rendering artifacts from deeply nested subgraphs

## 8. Common Fixes

If the checklist reveals issues, apply these fixes:

| Issue | Fix |
|-------|-----|
| `~~>` wavy arrows | Replace with `==>` + `linkStyle N stroke:#cc0000,stroke-width:3px` |
| `note` blocks | Remove; embed metadata in enriched node labels |
| classDef mid-diagram | Move ALL classDef to the end, after all nodes and edges |
| Unescaped specials in labels | Wrap in double quotes: `\|"label with (parens)"\|` |
| >25 nodes | Split into sub-diagrams by trust zone or functional domain |
| Missing version stamp | Add: `%% Version: {date} \| Phase: {N} \| System: {name}` |
| Bare untyped edges | Add label with prefix, protocol, and sensitivity |
