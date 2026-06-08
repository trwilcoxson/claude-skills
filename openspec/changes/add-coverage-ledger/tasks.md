## 1. Taxonomy

- [ ] 1.1 Author `references/coverage-taxonomy.md` from the 54-section reference: items at section→key-field granularity, each with id, tier (1/2), and Tier-2 precondition
- [ ] 1.2 Encode a machine list the eval/agents key off (ids + tier + precondition)

## 2. Ledger

- [ ] 2.1 Add `evals/reliability/schema/coverage.schema.json` (items: id, state, detail, source[], note)
- [ ] 2.2 `prompts/executor.md` (+ SKILL.md): initialize the ledger from the taxonomy, resolve items to terminal states with evidence/notes across the pipeline, emit `coverage.json`
- [ ] 2.3 SKILL.md final coverage pass (validation-specialist): no `pending`; lift unknown/partial/absent-gap into Open Questions / Known Limitations; write coverage profile
- [ ] 2.4 `references/report-template.md`: Open Questions / Known Limitations / Coverage Profile sourced from the ledger

## 3. Verification

- [ ] 3.1 `evals/reliability/coverage_checks.py`: terminal-state-per-applicable, grounded present (reuse `_resolves_in_repo`), noted unknown, applicability-vs-facts consistency; emit coverage profile. Structure-only, no required-presence.
- [ ] 3.2 Coverage judge prompt: assess state correctness (n/a, absent, present accuracy)
- [ ] 3.3 Surface coverage profile in `report.py`; wire into `run.py`/contract

## 4. Verify

- [ ] 4.1 Smoke `coverage_checks.py`: pending item → defect; ungrounded present → defect; honest unknown → pass; inconsistent applicability → defect
- [ ] 4.2 Live: re-run a target; confirm a populated ledger, coverage profile, open-questions surfaced; judge confirms states
- [ ] 4.3 `openspec validate add-coverage-ledger --strict`; commit; archive after merge
