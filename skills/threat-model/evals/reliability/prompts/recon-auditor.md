# Recon auditor — is the coverage denominator trustworthy?

Coverage is measured against the surface the system itself discovered (`recon.json`). That is
gameable: if recon misses a whole subsystem, coverage looks complete while the model is blind to
it. You guard against that by comparing recon to the **actual repo**.

## Inputs
- `{repo}` — the target repository (read the tree and the code).
- `{run_dir}/recon.json` — the surface the system claims to have discovered.

## Procedure
1. Independently inventory the repo's real surface: every route/handler/entry point, every data
   store and external service, every trust boundary (process/network/privilege), every IaC or
   container exposure.
2. Compare to `recon.json`. Flag **major** subsystems or surface present in the repo but absent
   from recon (ignore trivial omissions; focus on things whose absence would hide real risk).

## Output (JSON)
```json
{ "missed_subsystems": [ "human-readable description + repo path" ],
  "recon_surface_count": 0, "independent_surface_count": 0, "notes": "..." }
```
If recon is complete, return an empty `missed_subsystems` — that means the coverage denominator is
trustworthy for this run.
