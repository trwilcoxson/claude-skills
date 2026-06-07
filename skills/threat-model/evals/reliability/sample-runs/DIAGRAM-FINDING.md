# Diagram verification — the drift it caught

The first version of this harness verified findings, recon grounding, coverage, and reasoning, but
**not the diagram**. Adding deterministic diagram verification (`../diagram_checks.py`) and re-scoring
every committed run exposed a real regression the green checks had hidden: **all nine runs across all
three targets fail the diagram spec**, even though they scored structure / consistency / grounding /
coverage 3/3 and quality up to 1.0.

| Target | Diagram defects per run | Typical failures |
|---|---|---|
| NodeGoat | 8 / 6 / 6 | only L1+L4 layers (L2/L3 missing for a 6-20 component system); 0% of flows annotated; 0% ownership markers; L4 not linked to any TM-NNN |
| TerraGoat | 5 / 5 / 6 | layers not stamped; no flow sensitivity annotations; no ownership markers; no legend/version stamp |
| crAPI | 6 / 1 / 9 | same shape — missing/annotation-light layers, L4 risk overlay not linked to findings |

The skill's *spec* already requires all of this (mermaid-spec §3–§8, mermaid-layers §2–§6,
the 26-category visual-completeness checklist). The skill simply under-delivered the diagram, and
nothing checked it — so "a full security review with a robust threat-model diagram" was not actually
being produced despite passing runs. This is exactly the drift the diagram dimension exists to stop.

## What the verification checks (mapped to the diagram requirements)

- **Taxonomy** — required layers present per scaling (L1-L4), legend + version stamp, classDefs.
- **Fully annotated flows** — every edge typed and carrying protocol/sensitivity/`[ENC|PLAIN]` (spec §4).
- **Trust boundaries** — L2 subgraph zones vs the recon trust boundaries.
- **Component metadata** — ownership markers (`[team:]`/`[vendor:]`/`[managed]`) on nodes (spec §7).
- **Risk layering linked to findings** — L4 risk classes + threat annotations (spec §5) whose `TM-NNN`
  ids match the findings; every HIGH+ finding's components present and risk-colored in L4.

Semantic correctness (are boundaries placed right, are annotations accurate) is the
`prompts/diagram-judge.md` layer.

## Response

The skill gained a blocking **Diagram acceptance gate** (SKILL.md, Phase 2) restating these as
must-haves before a diagram is finalized, and the eval executor now requires it. The next run is the
loop closure: diagrams should pass verification. Until a run does, these committed runs stand as the
honest baseline — strong on analysis, weak on the diagram artifact.
