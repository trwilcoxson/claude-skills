# Red team — find what the model missed (reference-free completeness)

There is no answer key. Your job is to independently threat-model the **real target** and surface
significant risks the produced model did **not** cover. This is how we measure recall without a
golden list — the gaps are generated per target, from the target.

## Inputs
- `{repo}` — the target repository. Read it directly and reason about it yourself.
- `{run_dir}/report.md` + `{run_dir}/findings.json` — what the model already produced (so you can
  avoid duplicates).

## Procedure
1. Do your own focused review of `{repo}` — auth, access control, injection sinks, data exposure,
   secrets, dependencies/SCA, SSRF, deserialization, IaC/container config, multi-tenant or session
   handling — whatever the actual code warrants.
2. For each candidate risk, check it is **grounded** (point to the file/line) and **not already
   covered** by the produced model (different asset/path than any existing finding), and estimate
   likelihood × impact → only keep **HIGH+ (>=10)**.
3. Return the gaps. If the model was thorough and you find none, say so — that is a strong result.

## Output (JSON)
```json
{ "candidate_gaps": [
    {"title":"...","severity":"HIGH|CRITICAL","evidence":"path:line or file","attack_path":"...",
     "why_missed":"what the model overlooked or under-rated"} ],
  "notes":"..." }
```
Quality over quantity. A vague or ungrounded "gap" is worse than none — each must name a real
location in the repo.
