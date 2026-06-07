# NodeGoat — loop closure (baseline → improved skill)

The baseline run (`../`) surfaced reliability gaps with no answer key. Those gaps drove two skill
edits (commit `59ed40d`); re-running the harness on the **improved** skill verified the gaps closed.
This is the Improve step, measured — not asserted.

## Skill edits

- **Phase 1.3 — mandatory secret/artifact sweep** (committed keys/certs, seed/default credentials,
  hardcoded tokens across the whole tree, each recorded as a finding).
- **Phase 3 — Persisted & Cross-Context Input Tracing** (trace stored user input to all sinks
  including other users' and admin/privileged views; model stored→privilege-escalation chains).

## Verified deltas — same target, 3 runs, improved skill (evidence in this folder)

| Signal | Baseline | Improved |
|---|---|---|
| Deterministic contract (structure / consistency / grounding / coverage) | 3/3 pass, 0 defects | 3/3 pass, 0 defects |
| Stability (LLM-matched, HIGH+ core) | 12/19 (overlap 0.74) | **13/19 (overlap 0.78)** |
| Default/seed credentials (CRITICAL) | 2/3 runs | **3/3 — now stable** |
| Committed TLS private key (CRITICAL) | 1/3 runs | **all 3 runs** (reads 2/3 as a standalone cluster because run 2 bundled it into the "hardcoded secrets" finding) |
| Stored-XSS-via-name → admin takeover | **confirmed recall GAP (CRITICAL)** — the headline baseline miss | **now a stable finding (3/3); no longer a recall gap** |

The two edits did exactly what the eval predicted: the attention-dependent secret CRITICALs became
reliable, and the cross-user stored-XSS chain is now caught by the skill itself.

## What the improved run's red team found instead

The red team runs fresh each time and explores differently, so it surfaces different real issues per
run. On the improved run it confirmed one new HIGH gap — **NoSQL operator injection on the login
query** (`req.body` objects flowing unvalidated into `findOne`). That is the *next* iteration's
input, not a regression: the gap the edits targeted is closed, and the loop keeps producing the next
thing to fix.

## Honesty notes

- "All 3 runs" for the committed key vs the "2/3" cluster number: `grep` confirms the key is flagged
  in every run; the semantic matcher counts a standalone cluster at 2/3 because run 2 phrased it as
  one combined "hardcoded secrets + committed key" finding. Reported both ways rather than rounding up.
- Deterministic contract held perfectly in both baseline and improved runs (the edits changed
  *what* gets found, not output validity).
- `run{1,2,3}/` here hold the improved-skill manifests + scores (report.md omitted to save space;
  the baseline `../run*/report.md` already shows the full output shape). `reliability.html` is the
  improved-run report.
