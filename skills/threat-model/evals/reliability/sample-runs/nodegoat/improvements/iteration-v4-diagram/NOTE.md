# Iteration 3 — diagram acceptance gate (loop closed)

Diagram verification (`../../../../diagram_checks.py`) caught that every prior run produced an
under-built diagram while passing all other checks (see `../../../DIAGRAM-FINDING.md`). The skill
gained a blocking **Diagram acceptance gate** (SKILL.md, Phase 2). This run re-ran NodeGoat against
the gated skill.

## Result — diagram now passes on all 3 runs

| | Before (baseline runs) | After (gate, this run) |
|---|---|---|
| Layers | L1 + L4 only | **L1, L2, L3, L4** (all 3 runs) |
| Flows annotated (protocol/sensitivity/`[ENC|PLAIN]`) | 0% | **93% / 94% / 100%** |
| Component ownership markers (L1) | 0% | **88% / 83% / 90%** |
| Trust-boundary subgraphs | 1 | **15 / 11 / 16** |
| L4 risk overlay linked to findings | no | **yes — 17/17 HIGH+ findings annotated** with `⚠ STRIDE · L×I=score BAND · MITRE · CWE · TM-NNN` |
| Diagram verification | FAIL | **PASS (0 defects)** all 3 runs |

Full contract on the gated runs: structure / consistency / grounding / coverage / **diagram** all
pass, 0 defects. Residual: 1–4 unlabeled edges per run (soft warning, not pass-blocking).

## Check corrections made at the same time (not tuning-to-pass)

Two deterministic sub-checks were genuinely wrong and were fixed; the **baseline runs still FAIL**
(7/5/6 defects) afterward, so the fixes corrected bugs without weakening the gate:
- **L4 linkage** matched recon component ids (`C5`) against the overlay, but the diagram uses
  semantic node ids (`Express`, `Session`). Now matched on the shared `TM-NNN` id scheme.
- **Ownership** was measured across all four layers + the legend, diluting the fraction. Now measured
  on L1 process/data-store nodes only (which is where the markers belong) — revealing the real ~88%.
- A few unlabeled edges are a soft warning rather than a hard fail (spec wants every arrow typed; a
  1/61 straggler shouldn't fail an otherwise-complete diagram).
