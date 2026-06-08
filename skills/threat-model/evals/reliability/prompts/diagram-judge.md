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

## Judge the analytical & communication visuals (only those present)
6. **Attack tree** — is the root the true highest-value objective; are AND vs OR gates logically right
   (parent genuinely requires all vs any children); are leaf techniques the real exploitable steps?
7. **Attack flow** — is the step ordering a realistic kill chain (initial access → … → objective); are
   the lateral hops actually reachable in this system?
8. **Auth sequence** — is the protocol modeled correctly (handshake order, token exchange/lifetimes),
   and are the failure paths the real ones (lockout / generic error / rate-limit)?
9. **STRIDE-per-element matrix** — are the cells marked `n/a` genuinely inapplicable (not a missed
   threat), and do the `clean` cells really have no threat? (Recall, not just population.)
10. **Risk heat map** — are the underlying L and I scores reasonable for the system?
11. **ATT&CK layer** — is each technique the correct mapping for the described behavior; tactic right?
12. **RBAC matrix** — are the role→resource permissions correct against the real access control; are
    the `GAP` cells real authorization defects?
13. **SBOM graph** — is the dependency tree accurate and are the `risk`-flagged deps genuinely
    EOL/CVE-bearing?

## Output (JSON)
```json
{ "diagram_soundness": 0.0, "verdict": "robust|adequate|weak",
  "issues": [ {"area":"trust-boundaries|flows|metadata|risk-layer|taxonomy|attack-tree|attack-flow|auth-sequence|stride-matrix|heat-map|attack-layer|rbac|sbom", "detail":"...", "severity":"high|med|low"} ],
  "notes":"..." }
```
`diagram_soundness` = fraction of the present dimensions that are correct. Cite the diagram line or
repo file when you flag something. A visual that is present but inaccurate is `weak`, not `robust`.
