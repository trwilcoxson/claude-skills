# threat-model evals &amp; benchmarks

A self-testing harness for the `threat-model` skill, built around the Skills 2.0 model
(Create → **Eval** → **Improve** → **Benchmark**, repeated after every model update). It answers
three questions the skill could not answer about itself before:

1. **Does the skill still work?** Run it against a fixed set of cases with known-good expectations.
2. **Does the skill still earn its keep?** Benchmark it against a no-skill baseline on the same prompts.
3. **Did a model change break or obsolete it?** Compare against a blessed baseline (regression),
   and watch whether the bare model starts passing without the skill (outgrowth).

## Not the same thing as the runtime validation layer

The skill already has strong **in-run quality control** — Phase 5 false-negative hunting, Phase 6
false-positive/confidence validation, the `validation-specialist` agent, the completeness
checklists. That machinery checks *one assessment of one target system while a run is happening*.

This directory is a different layer: **meta-level evaluation of the skill itself** across many
inputs and across model versions. Don't conflate them. Validation makes a single run trustworthy;
evals tell you whether the skill, as a whole, is good and still pulling its weight.

## Design: deterministic harness, agent-driven execution

The skill is LLM-driven, so "run the skill and judge it" needs Claude. But the *scoring* must not.
Following the same philosophy as the `python-quality` skill ("deterministic tools first, then hand
results to the LLM for reasoning"), the split is:

- **Deterministic (this harness):** load and validate cases, recompute every score from rubric
  verdicts, aggregate pass-rate / time / tokens, render the report, flag regression and outgrowth.
  The pass/fail signal never depends on a model doing arithmetic.
- **Agent-driven (prompt templates in `harness/prompts/`):** four roles in fresh contexts —
  **Executor** (runs the skill on a prompt), **Grader** (verdict per rubric item), **Comparator**
  (blind A/B of two outputs), **Analyzer** (patterns across the result set → concrete skill edits).

## Layout

```
evals/
  cases/                 8 YAML cases (6 positive, 1 trigger-negative, 1 injection-resilience)
  schema/                JSON Schema for a case and for a grader result
  harness/
    eval_runner.py       CLI: validate | plan | ingest | report | compare | bless
    metrics.py           scoring + regression/outgrowth (deterministic)
    report.py            self-contained HTML report
    prompts/             executor / grader / comparator / analyzer templates
    requirements.txt     PyYAML
  baselines/             blessed skill-arm scores for regression (current/ is git-ignored)
  trigger-tuning/        labeled queries + trigger_tune.py (feature: trigger tuning)
  runs/                  generated per-run artifacts (git-ignored)
```

## A case

Each `cases/*.yaml` pairs a realistic prompt with machine-checkable expectations and a weighted
rubric (see `schema/case.schema.json`):

- `expected.must_find_threats` — threats a correct model must surface, each with the right STRIDE-LM
  letter and a minimum OWASP severity. A missed `CRITICAL` fails the case outright.
- `expected.dfd_layers` / `stride_categories` / `required_report_sections` — structural coverage.
- `rubric` — 5–8 weighted, objectively checkable criteria the Grader applies.
- `pass_threshold` — fraction of rubric weight needed to pass.

The set deliberately spans the trigger surface and the failure modes that matter: payment/PCI,
microservices mesh, agentic+RAG, **simple-crud** (proves the skill scales *down* without
over-generating), serverless, multi-tenant Kubernetes, a **trigger-negative** near-miss that must
*not* activate, and an **injection-resilience** case where the pasted architecture hides a prompt
injection the skill must refuse to follow and instead report as a finding.

## Run a benchmark

```bash
cd skills/threat-model/evals
pip install -r harness/requirements.txt

python3 harness/eval_runner.py validate                 # schema-check the cases
python3 harness/eval_runner.py plan   --run 2026-06-06  # writes runs/2026-06-06/ + INSTRUCTIONS.md
# follow INSTRUCTIONS.md: Executor produces outputs (skill arm + baseline arm),
# Grader writes one results/<case>.<arm>.json per task
python3 harness/eval_runner.py ingest --run 2026-06-06  # validate the grader output
python3 harness/eval_runner.py report --run 2026-06-06 --with-compare   # -> runs/2026-06-06/report.html
```

The report puts **skill-active vs baseline** side by side: pass rate, mean elapsed time, mean token
usage, and a per-case rubric breakdown with missed must-finds.

## Regression and outgrowth

```bash
python3 harness/eval_runner.py bless   --run 2026-06-06   # promote this skill arm to the baseline
# ... after a model update, run a fresh benchmark, then:
python3 harness/eval_runner.py compare --run 2026-07-xx
```

- **Regression** — the skill arm lost ground on a case it used to pass → the model changed; improve
  the skill.
- **Outgrowth** — the *no-skill* arm now passes the positive cases → the model may have outgrown the
  skill; consider retiring it.

## Trigger tuning

The frontmatter `description` decides whether the skill ever fires. `trigger-tuning/` measures that
instead of assuming it:

```bash
cd trigger-tuning
python3 trigger_tune.py split                              # 60/40 train / held-out
python3 trigger_tune.py template --out observations.json   # fill in trigger counts (3 runs/query/candidate)
python3 trigger_tune.py report --observations observations.json
```

Each candidate description is scored on the held-out set by trigger rate on positives vs
false-activation on near-miss negatives; iterate the wording (~5 candidates) and keep the winner.

## Lifecycle &amp; skill typing

`threat-model` is a **Capacity Uplift** skill: it does work the base model can't yet do well on its
own, so it has an expiry and must be **re-benchmarked after every model update** and watched for
outgrowth. (Contrast: an *Encoded Preferences* skill — a fixed workflow/house style — keeps its
value as models improve.) The standing cadence is Create → Eval → Improve → Benchmark, re-run on
each model bump; bless only when a run holds or beats the baseline.
