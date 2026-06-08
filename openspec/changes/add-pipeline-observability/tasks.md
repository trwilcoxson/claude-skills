## 1. Event stream

- [x] 1.1 Add `evals/reliability/events.py`: `tm.run-event/1` schema constants, `emit()` writer, and `from_transcripts(dir)` to derive events from a completed workflow run
- [x] 1.2 Document the schema + emission convention in `references/pipeline-observability.md`
- [x] 1.3 `SKILL.md` orchestration: emit start/done events around each Task spawn (mirrors the Execution Log)
- [x] 1.4 `evals/reliability/run.py`: emit events as it drives stages (or expose `events`/`observe` helpers)

## 2. Renderer

- [x] 2.1 Add `evals/reliability/tm_observe.py`: pure renderer with `--tail` / `--tree` / `--once`, fixed columns, stable order
- [x] 2.2 Ensure same input → byte-identical output (no clocks, no analysis)

## 3. Verify

- [x] 3.1 Unit: fixture `events.ndjson` (incl. parallel agents) → clean tail/tree; re-render byte-identical
- [x] 3.2 Real: derive events from the NodeGoat verification run's transcripts and render a clean stage/persona timeline
- [ ] 3.3 `openspec validate add-pipeline-observability --strict`; commit; archive after merge
