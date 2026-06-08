## Approach

One append-only NDJSON stream + one pure renderer. The agents already decide and write what happened
(Execution Logs, pipeline-summary); this makes it streaming and machine-readable, and presents it.

### Event record (`tm.run-event/1`)

`{ ts, run_id, seq, stage, persona, action, status, metrics, note }` — one JSON object per line in
`events.ndjson`. `status` ∈ `start|done|error`. `done` mirrors the Execution Log (counts, skips,
assumptions) — nothing new. `seq` is assigned by the emitter centrally so parallel agents don't race;
the renderer also falls back to a `(ts, seq)` total order.

### Emission points

- **Skill pipeline**: the parent/orchestrator emits `start` before each Task spawn and `done` after
  that agent's output file lands (so even a dead sub-agent has a visible `start`); it owns the verify
  stage and the pipeline-summary write. Documented in `references/pipeline-observability.md` and
  `SKILL.md` orchestration.
- **Eval**: `run.py` emits events as it drives stages; for runs executed via the Workflow tool,
  `events.py from_transcripts(dir)` derives the stream from the agent transcripts (which carry
  timestamps + labels), so observability works over the runs the harness actually performs.

### Renderer `tm_observe.py`

Pure read-only consumer of `events.ndjson`. Zero analysis, never spawns/blocks. Views:
- `--tail` (default): one fixed-column line per event — `HH:MM:SS  <side>  <stage>  <persona>  <status> <metrics>`.
- `--tree`: grouped stage → persona with start/done and duration.
- `--once`: final per-stage/persona summary table.
Same file in → byte-identical out (sort by `(seq if present else ts, ts)`; format is fixed-width).

### Determinism boundary

`events.py emit()` only serializes what a persona reports; `tm_observe.py` only formats. Any pass/fail
gate that today rides in prose (e.g. an HTML-output check) is a deterministic function in the
`checks.py`/`diagram_checks.py` family and is surfaced as an event `status` — the renderer never judges.

## Verification

- Unit: feed `tm_observe.py` a fixture `events.ndjson` (incl. parallel specialists) → assert clean
  tail/tree output and byte-identical re-render.
- Real: derive `events.ndjson` from the NodeGoat verification run's transcripts via
  `events.py from_transcripts` and render it → a clean per-stage/persona timeline of the actual run.
