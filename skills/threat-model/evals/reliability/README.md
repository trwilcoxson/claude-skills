# Reliability harness (reference-free, dynamic)

Validates that the threat-model flow is **reliable on whatever you point it at** — not that it
reproduces a fixed answer. There is no per-target ground truth. A target is just a real system
(`targets/<id>.yaml` = id + source + a local repo path supplied at runtime); adding one is adding
a file and cloning a repo. The system is run **N times** per target.

This supersedes the answer-key approach in `../cases/` + `../harness/` (fixed prompts with
hand-authored must-find lists). That approach forced answers — e.g. it recorded a correctly
reasoned MEDIUM(9) finding as a "miss" because the key demanded HIGH. Quality here is graded from
properties of `(target, output)` that hold for any good threat model, so it scales to any target.

## How quality is judged without an answer key

Five layers. The system emits, per run, `report.md` + two manifests (`recon.json`, `findings.json`,
see `schema/`). Everything below is derived from those plus the real repo.

**Deterministic (the reliability contract — should hold on every run, any target):**
1. **Structure** — manifests parse and carry required fields; `report.md` has the template sections.
2. **Consistency** — `severity == band(likelihood × impact)`; `summary_counts` match the findings;
   `TM-NNN` cross-refs and `report.md`↔manifest counts agree; CWE/MITRE ids are well-formed.
3. **Grounding** — every recon element's `evidence` resolves in the actual repo (path/glob/string);
   every finding ref points to a real recon id. Catches invented components.
4. **Coverage** — every entry point / data store / trust boundary the system *itself* discovered is
   addressed by a finding or explicitly marked `no_issue_surface`. The denominator is the system's
   own recon, not a golden list.

**Agent-judged (sampled, reference-free):**
5a. **Quality** (`quality-judge`) — is each attack path sound against the real repo, and is severity
    *defensible* (not equal to a target)? Is it proportionate (no padding, no invented components)?
5b. **Adversarial recall** (`red-team` → `gap-validator`) — an independent agent threat-models the
    same repo and surfaces HIGH+ risks the model missed; a second agent confirms each is grounded,
    uncovered, and material. This replaces hand-authored must-finds with gaps generated per target.
5c. **Recon completeness** (`recon-auditor`) — compares recon to the real repo so the coverage
    denominator can't be gamed by a recon that skipped a subsystem.

**Stability:** across the N runs, the HIGH+ "core" is matched semantically and we report how much of
it is present in *every* run. Reliability = the crown jewels appear every time; breadth may vary.

## Run it

```bash
cd skills/threat-model/evals/reliability
git clone --depth 1 https://github.com/OWASP/NodeGoat.git /tmp/nodegoat   # the target
# Run the skill N times on the repo (Executor prompt in prompts/executor.md), each emitting
# report.md + recon.json + findings.json into runs/<target>/run{1..N}/.
# Run the judged layers (quality-judge / red-team -> gap-validator / recon-auditor) into runs/<target>/agents/.
python3 run.py report --runs-root runs/nodegoat --repo /tmp/nodegoat \
    --target nodegoat --source https://github.com/OWASP/NodeGoat --out runs/nodegoat/reliability.html
```

`run.py check --run <dir> --repo <path>` runs just the deterministic layer on a single run.

A committed real run is under [`sample-target-run/`](sample-target-run/) — see its `RELIABILITY.md`.
