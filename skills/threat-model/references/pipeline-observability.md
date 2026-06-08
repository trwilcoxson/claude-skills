# Pipeline Observability

Make the multi-agent run transparent: which persona is doing what, at which stage, uncluttered. The
agents do the work and report it; the stream fixes the shape and the renderer fixes the presentation.
No analysis lives in this layer.

## The event stream — `tm.run-event/1`

One append-only file, `events.ndjson`, one JSON object per line:

```json
{"schema":"tm.run-event/1","ts":"2026-06-07T12:04:17Z","run_id":"...","seq":1,"side":"skill",
 "stage":"recon","persona":"security-architect","action":"nodegoat","status":"done",
 "metrics":{"elapsed_ms":257000},"note":"components=23 stores=5 entry=18"}
```

- `status`: `start` when a persona begins, `done` when its output file lands, `error` on failure.
- `done.metrics`/`note` are a **projection of that persona's `## Execution Log`** (counts, skips,
  assumptions) — nothing new is computed here.
- `seq` is assigned centrally (the orchestrator stamps it) so parallel specialists don't race; the
  renderer also falls back to ordering by `(seq, ts)`.

## Who emits

- **Skill pipeline** — the parent/orchestrator emits a `start` before each Task spawn and a `done`
  after that agent's output file lands (so even a sub-agent that dies has a visible `start`), for
  `security-architect`, `diagram-specialist`, `validation-specialist`, `privacy-agent`, `grc-agent`,
  `code-review`, `report-analyst`, plus the verify stage. Use `evals/reliability/events.py` `emit()`.
- **Eval** — `run.py` emits as it drives stages; for runs executed via the Workflow tool,
  `events.py from_transcripts(<transcript-dir>, <run-id>)` derives the stream from the agent
  transcripts (real timestamps), so observability works over the runs the harness actually performs.

Any pass/fail gate (e.g. an HTML-output check) is a deterministic function in the
`checks.py`/`diagram_checks.py` family and is surfaced as an event `status` — the renderer never judges.

## Viewing — `tm_observe.py`

A pure read-only renderer (`python3 tm_observe.py events.ndjson [--tail|--tree|--once]`). Same file
in → byte-identical out.

```
12:00:00  skill  recon        security-architect  ▶ start nodegoat
12:04:17  skill  recon        security-architect  ✔ done  nodegoat   elapsed=4m17s
12:05:00  eval   judge        quality-judge       ▶ start run1
```

- `--tail` (default): one fixed-column line per event — scannable while a run streams.
- `--tree`: grouped stage → persona with durations.
- `--once`: final per-persona summary.

Convenience: `python3 run.py observe --transcripts <dir> --run <id>` derives + renders in one step.
