# threat-model — reliability run: OWASP NodeGoat

A real run of the reference-free harness. The skill was pointed at a real repository
([OWASP NodeGoat](https://github.com/OWASP/NodeGoat) — Express + MongoDB, intentional vulns), run
**3 times**, and judged entirely by properties derived from the target and the output. **No answer
key**: the only target-specific input is `targets/nodegoat.yaml` (id + repo). Model: Claude Opus 4.8.

## Verdict

**Structurally rock-solid; real recall and stability gaps.** The system reliably produces
well-formed, internally consistent, fully grounded threat models on every run — but it does not
reliably surface every high-severity issue run-to-run, and an independent red team found a CRITICAL
it missed. That is exactly the kind of reliability signal this harness exists to produce, and it
needed no per-target ground truth to produce it.

## 1. Deterministic contract (per run) — held on every run

| Run | Structure | Consistency | Grounding | Coverage | Findings | Defects |
|---|---|---|---|---|---|---|
| 1 | pass | pass | 1.00 | 1.00 | 25 | 0 |
| 2 | pass | pass | 1.00 | 1.00 | 20 | 0 |
| 3 | pass | pass | 1.00 | 1.00 | 21 | 0 |

- **Consistency** = `severity == band(likelihood × impact)` on *every* finding, counts match, refs
  resolve — held across all 66 findings with zero violations. (One run even logged a self-correction
  re-banding 20-point findings to CRITICAL — and it landed consistent.)
- **Grounding = 1.00**: every recon element's evidence resolved in the actual repo. Zero invented
  components across three runs.
- **Coverage = 1.00**: every entry point / data store / trust boundary the system discovered was
  addressed by a finding or explicitly marked no-issue.

This is the determinism that *should* hold for any target, and it did.

## 2. Stability across runs (semantic match) — the main reliability gap

**12 of 19 distinct high-severity issues appear in all 3 runs; mean pairwise overlap 0.74.**

- **Stable (every run):** eval() RCE, cleartext passwords, unencrypted PII, NoSQL `$where`
  injection (all CRITICAL), plus hardcoded secrets, IDOR, missing admin access control, SSRF,
  XSS-via-autoescape-off, plaintext HTTP, insecure session cookies, weak password policy (HIGH).
- **Not reliably surfaced:** **2 CRITICALs** — *default seed accounts* (2/3 runs) and *committed TLS
  private key* (1/3) — plus CSRF, NoSQL-in-login, outdated deps, open redirect, ReDoS (HIGH, 1–2/3).

So the app-logic crown jewels are stable, but repo-artifact CRITICALs (committed key, seed creds)
are hit-or-miss. A real finding to feed back into the skill (e.g. a deterministic secret/artifact
sweep in Phase 1 so those don't depend on the model's attention that run).

## 3. Reasoning quality (judged, reference-free)

Mean attack-path soundness **0.92** over 13 sampled findings; proportionality **proportionate**
(every finding traced to a real sink/file; no padding, no invented components). One weak finding:
`TM-013` — the wrong-context-encoding XSS is grounded (the code's own `@FIXME` confirms it) but the
specific source→sink path was conflated. Reference-free: the judge assessed soundness against the
repo, never against a target answer.

## 4. Adversarial recall (gaps generated per target, not pre-authored)

An independent red team threat-modeled the same repo; a second agent validated each claim. **2
confirmed gaps, 0 rejected:**

- **CRITICAL — stored XSS via `firstName`/`lastName` → admin account takeover.** Permissive
  `^.{1,100}$` validators store raw names that render unescaped in `benefits.html`/`layout.html`;
  the admin's post-login landing page is `/benefits`, so the payload fires in the admin's session.
  The skill's `TM-013` scoped name XSS to *self*-view and missed the cross-user privilege-escalation
  chain.
- **HIGH — pre-auth reflected XSS** in the login form `userName` field (autoescape off).

This is recall measured without a golden list — the misses come from the target itself.

## 5. Recon completeness (coverage-denominator guard)

Coverage = 1.00 is measured against the system's *own* recon, so it's gameable if recon skips a
subsystem. The auditor compared recon to the real repo (56 surface elements vs 60 independently
found) and flagged that recon **missed the CI/CD subsystem** (`.github/workflows`, `.travis.yml`,
`Gruntfile.js`) and the **PaaS deploy surface** (`app.json` declaring a publicly accessible
`MONGODB_URI` + postdeploy `db-reset`, `Procfile`). Coverage is trustworthy for the application
layer, blind to CI/CD. So the perfect coverage number carries an asterisk — and the harness says so.

## Method & honesty notes

- **Reference-free & dynamic.** Adding a target is adding a `targets/<id>.yaml` and cloning a repo.
  Nothing here is specific to NodeGoat beyond its path.
- **Determinism boundary.** Structure, consistency (`severity==band(L×I)`), grounding, and coverage
  are deterministic. Quality, adversarial recall, recon completeness, and *cross-run finding
  identity* are semantic → LLM-judged. Finding-identity was first attempted as a deterministic
  heuristic; token-overlap under-merged reworded duplicates and CWE-chaining over-merged via shared
  CWEs, so it moved to an LLM matcher (`prompts/stability-matcher.md`) — the same determinism-boundary
  lesson, applied to the harness itself. The heuristic remains as a conservative fallback.
- **Outputs not forced.** Executors *write* `report.md` + `recon.json` + `findings.json`; the harness
  validates them. Malformed output would be a measured structural defect — there were none.
- **Reproduce.** `run1..3/` hold each run's manifests + `scored.json`; `agents/` holds the judged
  layers (`quality.json`, `recall.json`, `recon-audit.json`, `stability-clusters.json`);
  `reliability.html` is the rendered report. Quality / recall / recon were judged on run 1.
