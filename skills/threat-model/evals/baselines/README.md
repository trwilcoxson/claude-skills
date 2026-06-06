# Baselines

`bless` writes the skill arm of a known-good run here as `current/skill.json` (per-case scores)
plus `current/meta.json` (which run, when). `compare` reads it to detect:

- **Regression** — a later run where the skill arm lost ground on a case it used to pass. The
  Skills 2.0 signal for "the model changed; improve the skill."
- **Outgrowth** — uses the baseline (no-skill) arm of the *current* run, not this file: if the
  bare model starts passing the positive cases without the skill, the skill may have outlived its
  usefulness.

Re-bless after a deliberate skill improvement so the bar moves up. Do **not** bless a run that
regressed. `current/` is git-ignored — it is local state, not a committed artifact.
