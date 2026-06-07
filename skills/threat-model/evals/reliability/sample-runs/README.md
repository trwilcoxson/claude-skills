# Sample reliability runs

Real runs of the reference-free harness on three different kinds of targets. No answer key was used
for any of them; adding a target is a `targets/<id>.yaml` + a clone.

> **Note:** diagram verification was added after these runs and re-scored against them — **all nine
> runs fail the diagram spec** (missing layers, unannotated flows, no ownership markers, L4 not linked
> to findings) even though they pass every other check. The per-target writeups' "contract 3/3" refers
> to the structure/consistency/grounding/coverage layers that predate diagram verification. See
> [`DIAGRAM-FINDING.md`](DIAGRAM-FINDING.md). The `reliability.html` files have been regenerated and now
> show the `Diagram` column (FAIL).

- **[`nodegoat/`](nodegoat/RELIABILITY.md)** — OWASP NodeGoat (Express + MongoDB web app). The
  baseline run plus a two-iteration improvement loop:
  [`nodegoat/improvements/LOOP-CLOSURE.md`](nodegoat/improvements/LOOP-CLOSURE.md) records which
  skill edits reliably landed (secret sweep → two CRITICALs now stable; CI/CD recon; stored-XSS→admin
  gap closed) and which did **not** (injection-sink tracing stayed run-dependent) — with run-level
  evidence either way.
- **[`terragoat/`](terragoat/RELIABILITY.md)** — TerraGoat AWS (Terraform IaC). A declarative
  cloud-infra target; all six CRITICAL misconfigs stable across runs.
- **[`crapi/`](crapi/RELIABILITY.md)** — OWASP crAPI (~900-file polyglot microservices: Java, Go,
  Python, React, plus an LLM agent + MCP server). The scale test — contract held 3/3, recon complete,
  and the skill found both classic API vulns (BOLA/BFLA/JWT/injection) and the agentic threats
  (excessive agency, indirect prompt injection, MCP auth bypass).

Across all three: the deterministic contract (structure / consistency `severity==band(L×I)` /
grounding / coverage) held on every run, the high-severity core was stable, and the judged layers
(quality, adversarial recall, recon completeness) produced real, target-specific signal without
ground truth. Same harness, no per-target tuning.
