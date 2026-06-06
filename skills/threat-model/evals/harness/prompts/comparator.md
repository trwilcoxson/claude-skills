# Comparator

Blind A/B between two outputs for the **same case** — typically two skill versions, or skill
vs baseline. Use this to detect quality differences the rubric totals can hide (two outputs can
tie on points while one is clearly better).

## Inputs
- `case` — the `cases/*.yaml` file.
- `output_A`, `output_B` — two Executor outputs for that case, given to you **unlabeled**. You
  are not told which is which; the operator records the mapping separately.

## Procedure
1. Judge each output against the case `expected` and rubric independently first.
2. Then compare directly on: completeness of must-finds, correctness of severities and attack
   paths, DFD quality (layers, trust boundaries, encryption state), proportionality (no invented
   components, no padding), and absence of fabricated framework IDs.
3. Pick a winner: `A`, `B`, or `tie`. State the 2-4 concrete differences that decided it.
4. Keep it blind: do not speculate about which is "the new version."

## Output
```json
{ "case_id": "...", "winner": "A | B | tie", "margin": "clear | slight | tie",
  "reasons": ["...", "..."] }
```
