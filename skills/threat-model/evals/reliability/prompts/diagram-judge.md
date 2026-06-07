# Diagram judge — is the threat-model diagram correct? (semantic)

The deterministic layer (`diagram_checks.py`) confirms the diagram *has* the required taxonomy
(layers, typed/annotated edges, trust-boundary subgraphs, ownership markers, an L4 risk layer that
references findings). You judge whether those elements are **correct** for the real system —
placement and accuracy, not presence.

## Inputs
- `{repo}` — the target.
- `{run_dir}/report.md` (the Mermaid diagrams) + `recon.json` + `findings.json`.

## Judge against the real architecture
1. **Trust boundaries placed correctly** — do the L2 subgraph zones enclose the right components
   (e.g. internet edge vs internal subnet vs data tier), and does every flow that actually crosses a
   boundary cross one in the diagram? Flag misplaced or missing boundaries.
2. **Flow annotations accurate** — are edge protocol / sensitivity / encryption labels right for the
   real traffic (e.g. a plaintext internal hop labeled `[PLAIN]`, cardholder data `[RESTRICTED]`)?
   Flag wrong or generic labels.
3. **Component metadata accurate** — do ownership/tech markers match reality (managed vs self-managed,
   the right vendor/stack)?
4. **Risk layer faithful** — does the L4 overlay risk-color the components that actually carry the
   HIGH+ findings, and do its threat annotations (STRIDE-LM, L×I, TM-NNN) match the findings table?
   Flag findings missing from the overlay and overlay risks with no backing finding.
5. **Taxonomy fit** — are the symbol shapes used per their meaning (process vs data store vs external
   vs control vs secrets)?

## Output (JSON)
```json
{ "diagram_soundness": 0.0, "verdict": "robust|adequate|weak",
  "issues": [ {"area":"trust-boundaries|flows|metadata|risk-layer|taxonomy", "detail":"...", "severity":"high|med|low"} ],
  "notes":"..." }
```
`diagram_soundness` = fraction of the five dimensions that are correct. Cite the diagram line or repo
file when you flag something. A diagram that is present but inaccurate is `weak`, not `robust`.
