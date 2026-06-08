# Stability matcher — group equivalent findings across runs (semantic)

Cross-run finding identity is a semantic judgment, not string overlap, so it lives here rather than
in a deterministic heuristic. You receive the HIGH+ findings from N runs of the same skill on the
same target and cluster the ones that are **the same underlying issue**, however differently worded.

## Input
A JSON list of findings, each `{run, id, title, severity, cwe, assets}`.

## Cluster
Two findings are the same issue if they describe the same weakness on the same asset/surface — e.g.
"Passwords stored and compared in cleartext" and "Cleartext password storage and plaintext
credential comparison" are one cluster; "committed TLS private key" and "hardcoded session secrets"
are **different** clusters (different secrets, different assets) even though both touch secrets.
Do not over-merge on a shared generic CWE; do not under-merge on wording.

## Output (JSON)
```json
{ "clusters": [ { "label": "short canonical name", "severity": "HIGH|CRITICAL",
                  "runs": [1,2,3] } ] }
```
`runs` = the distinct run numbers this issue appears in. A cluster present in every run is part of
the stable core; one present in a subset is variable. Use each finding exactly once. Pick the
severity the issue carries in most runs.
