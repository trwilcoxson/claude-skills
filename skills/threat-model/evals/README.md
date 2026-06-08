# threat-model evals

A **reference-free reliability harness**: it checks that the threat-model skill is reliable on
*whatever real system you point it at*, with no per-target answer key. See
[`reliability/`](reliability/) for the harness, and
[`reliability/sample-runs/`](reliability/sample-runs/) for real runs against OWASP NodeGoat (a web
app, with a measured skill-improvement loop) and TerraGoat (Terraform IaC).

## Why not a fixed test suite

An earlier iteration used hand-authored cases with golden "must-find" lists and exact-severity
gates. That is a conformance test, not a reliability test: it forces answers (it recorded a
correctly reasoned MEDIUM-9 finding as a "miss" because the key demanded HIGH), it can't credit a
valid finding nobody pre-listed, and it doesn't scale to arbitrary targets. It was removed in favor
of grading *properties that hold for any good threat model* — structure, internal consistency
(`severity == band(L×I)`), grounding against the real repo, coverage of the system's own discovered
surface, plus judged reasoning quality, adversarial recall, recon completeness, and cross-run
stability. None of those need ground truth per target, so the harness applies to anything you point
it at. The full rationale is in [`reliability/README.md`](reliability/README.md).
