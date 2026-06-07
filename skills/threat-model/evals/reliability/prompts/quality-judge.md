# Quality judge — is the reasoning sound? (reference-free)

You judge the *quality* of a produced threat model against the **real target**, not against any
answer key. You never say "it should have found X from my list" — you only assess whether what it
*did* produce is sound and proportionate.

## Inputs
- `{repo}` — the target repository.
- `{run_dir}/report.md` + `{run_dir}/findings.json` — the produced model.

## Judge
1. **Attack-path soundness (per finding, sample up to ~10 spanning severities):** does the stated
   attack path actually follow from the real architecture in `{repo}`? Is the asset real and
   reachable as described? Is the severity *defensible* given the likelihood × impact reasoning
   (you are NOT checking it against a target severity — only that L, I, and the path are coherent)?
   Mark each sampled finding `sound` / `weak` / `wrong`.
2. **Proportionality:** is the volume and depth matched to the system — no padding with speculative
   findings, no inventing components, no boilerplate not grounded in the repo? Return
   `proportionate` / `inflated` / `thin`.

## Output (JSON)
```json
{ "n_judged": 0, "mean_soundness": 0.0, "proportionality": "proportionate|inflated|thin",
  "weak_findings": [ {"id":"TM-0xx","reason":"path does not follow / severity indefensible / asset not in repo"} ],
  "notes": "..." }
```
`mean_soundness` = fraction of sampled findings rated `sound`. Be strict and concrete; cite the
repo file when you call a path unsound.
