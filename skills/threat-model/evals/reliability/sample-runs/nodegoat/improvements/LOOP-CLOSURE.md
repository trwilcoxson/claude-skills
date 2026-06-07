# NodeGoat — improvement loop (two iterations, honest)

The baseline run (`../`) surfaced reliability gaps with no answer key. Each iteration turned a gap
into a skill edit and **re-ran the harness to check whether it actually landed**. Not every edit
did — recorded here as measured, including the one that didn't.

Deterministic contract (structure / consistency / grounding / coverage) held **3/3 with 0 defects in
every iteration**; the edits change *what* is found and how reliably, not output validity.

## Stability of the high-severity core across iterations

| | Stable core | Committed TLS key (CRIT) | Seed/default creds (CRIT) | Login operator-injection |
|---|---|---|---|---|
| Baseline | 12/19 | 1/3 | 2/3 | 2/3 |
| Iteration 1 (`iteration-v2/`) | 13/19 | 2/3 | **3/3** | 0/3 |
| Iteration 2 (`iteration-v3/`) | 16/24 | **3/3** | **3/3** | 1/3 |

## Iteration 1 — untrusted input, secret sweep, cross-context tracing

Edits (commit `59ed40d`, plus the earlier injection-handling `d564d50`): §1.2 untrusted-input
handling, §1.3 mandatory secret/artifact sweep, §3 persisted/cross-context input tracing.

- **Worked:** seed/default credentials went 2/3 → **3/3 (stable)**; committed TLS key 1/3 → 2/3; and
  the CRITICAL **stored-XSS-via-name → admin-takeover recall gap closed** (it became a stable finding
  and the red team no longer flags it).

## Iteration 2 — CI/CD recon + injection sink tracing

Edits (commit `9b55d2e`): §1.3 enumerate the CI/CD + deployment surface; §3 injection sink tracing
with operator/object injection.

- **CI/CD recon edit — landed.** CI/CD is now in recon in **all 3 runs** (the recon-auditor previously
  flagged it absent). Residual: the Heroku `app.json`/`Procfile` PaaS deploy path is still missed —
  narrower than before, the next thing to close.
- **Secret sweep matured** — committed TLS key reached **3/3 (stable)** this iteration.
- **Injection-sink edit — did NOT reliably land.** Login operator-injection (`{"$gt":""}` object into
  the `findOne` selector) stays run-dependent: 2/3 at baseline, 0/3 in iteration 1, 1/3 here. The edit
  did not produce reliable detection, and the red team (grading run 1, which missed it) re-confirmed
  it as a HIGH gap. A real negative result — the fix needs a more directive form (name the auth/login
  query selector explicitly) or, given the variance, a deterministic lint rather than a prose
  instruction.

## Takeaway

The harness does what it should: it credited the edits that reliably improved behavior (secret sweep,
CI/CD recon, the stored-XSS chain) and refused to credit the one that didn't (injection sink tracing),
with run-level evidence either way. The loop continues — open items are the Heroku deploy recon gap
and a reliable fix for login operator-injection.
