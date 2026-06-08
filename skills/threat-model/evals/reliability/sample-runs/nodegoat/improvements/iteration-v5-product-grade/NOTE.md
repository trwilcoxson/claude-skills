# Iteration 4 — product-grade visuals (Change A) + observability (Change B), verified

Re-ran NodeGoat against the skill with the 8 analytical/communication visuals required and the
neutral facts emitted (`kill_chains`, `roles`, boundary `kind`, dep `manifest`).

## Deterministic verification (`diagram_checks.py`)

- **run1: PASS — 0 defects, all 8 analytical visuals present** (attack tree, attack flow, auth
  sequence, STRIDE-per-element matrix, L×I heat map, ATT&CK layer, RBAC matrix, SBOM) plus the 4 DFD
  layers; 4 kill chains declared; flows 88% annotated; ownership 87%; L4 linked to findings. The full
  product-grade visual suite renders and passes the structure checks. (`run1/` is committed here.)
- **run3: FAIL — 4 defects** (missing attack-flow, 47% annotated flows, L4 not linked). A weaker run
  the eval correctly rejects → analytical-visual **stability** is the next iteration's finding (the
  skill *can* produce the full suite — run1 proves it — but not yet on every run).
- run2 died on an infrastructure socket error (not a skill/eval issue).

## Correctness (diagram judge) — `diagram-judge.json`

Verdict **robust (0.88)**. Diagrams verified against the real NodeGoat source; architecture, risk
content, flow labels, RBAC GAP cells, auth-sequence, and heat-map all accurate. Blemishes (the
next-iteration backlog, all analytical-layer): KC1 attack-tree mis-parents the eval/RCE step under
"obtain session" (the attack-flow orders it correctly); recurring single-child OR gates; one ATT&CK
mapping `T1530` (cloud storage) should be `T1213` (self-hosted Mongo); an incomplete stored-XSS
mechanics narrative (the SBOM correctly flags the marked-0.3.5 bypass); 3 L2 trust-boundary zones
drawn vs 4 declared in recon.

## Observability (Change B)

`run.py observe --transcripts <run> --tree` rendered the run's stage/persona timeline cleanly
(executors → diagram-judge, with durations) from the real transcripts — the uncluttered
"what agent is doing what" view, deterministic re-render.

## Boundary held

Templates/agents generated every visual and every event payload; `diagram_checks.py` enforced only
presence/shape/consistency; the judge assessed correctness. The eval distinguished a compliant run
(run1) from a weaker one (run3) with no answer key.
