# Sample reliability runs

Real runs of the reference-free harness on different kinds of targets. No answer key was used for
any of them; adding a target is a `targets/<id>.yaml` + a clone.

- **[`nodegoat/`](nodegoat/RELIABILITY.md)** — OWASP NodeGoat (Express + MongoDB web app). The
  baseline run, including the gaps it surfaced. [`nodegoat/v2-evidence/LOOP-CLOSURE.md`](nodegoat/v2-evidence/LOOP-CLOSURE.md)
  records the Improve step: the gaps drove two skill edits, and re-running verified them (two
  intermittent CRITICALs became stable; the stored-XSS→admin recall gap closed).
- **[`terragoat/`](terragoat/RELIABILITY.md)** — TerraGoat AWS (Terraform IaC). A deliberately
  different system type, run through the same harness with zero code changes — the generality proof.

Across both: the deterministic contract (structure / consistency `severity==band(L×I)` / grounding /
coverage) held on every run, the high-severity core is stable, and the judged layers (quality,
adversarial recall, recon completeness) produced real, target-specific signal without ground truth.
