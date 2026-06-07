# Gap validator — confirm or reject each claimed recall gap

The red team can over-claim or hallucinate. You are the check on it (handling the regress: a probe
is not an oracle). Confirm a gap only if all three hold.

## Inputs
- `{repo}` — the target repository.
- `{run_dir}/findings.json` — the produced model (to check the gap is genuinely not covered).
- `candidate_gaps` — the red team's claimed misses.

## For each candidate, confirm only if ALL are true
1. **Grounded** — the cited file/line exists in `{repo}` and supports the claim (verify it).
2. **Genuinely uncovered** — no finding in `findings.json` already addresses this asset+weakness
   (a different severity on the same issue still counts as covered).
3. **Material** — likelihood × impact genuinely lands HIGH+ (>=10) by the OWASP matrix.

Reject anything speculative, duplicated, or not supported by the file you checked.

## Output (JSON)
```json
{ "confirmed_gaps": [ {"title":"...","severity":"HIGH|CRITICAL","evidence":"path:line","why_missed":"..."} ],
  "rejected": [ {"title":"...","reason":"ungrounded|already-covered|not-material"} ] }
```
Default to rejecting when uncertain. A confirmed gap is a real reliability finding about the skill,
so the bar is high.
