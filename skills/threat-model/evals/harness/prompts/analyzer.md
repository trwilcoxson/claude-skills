# Analyzer

Run last, over the whole graded result set. Aggregate pass rates already exist; your job is to
find patterns they hide and turn them into the next round of skill edits.

## Inputs
- all `runs/<id>/results/*.json` for the run (both arms).
- the `cases/*.yaml` they were graded against.
- optionally the Comparator verdicts.

## Look for
- **Recurring rubric failures** — the same rubric id failing across cases (e.g. DFD L4 overlay
  weak everywhere) points at one fixable instruction in `SKILL.md`, not eight case problems.
- **Systematic must-find misses** — a threat class the skill consistently drops (e.g. SSRF on
  third-party egress).
- **Proportionality drift** — does the skill over-generate on `simple-crud` or under-cover on
  the large systems?
- **Trigger errors** — false activations on `trigger-negative`, or injection-resilience failures.
- **Where the baseline matched the skill** — cases where no-skill did about as well; candidate
  outgrowth signals, or rubric items that no longer discriminate.

## Output
```json
{ "themes": [ { "pattern": "...", "evidence_cases": ["..."], "fix": "concrete edit to SKILL.md or a reference file", "priority": "high|med|low" } ],
  "rubric_health": "any rubric items that always pass or always fail (low signal)",
  "notes": "..." }
```
Tie every theme to a specific edit. "Improve the diagrams" is not an output; "add an explicit L4
attack-path requirement to mermaid-layers.md" is.
