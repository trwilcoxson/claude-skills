## Why

When the multi-agent threat-model pipeline (and the eval) runs, there is no clean way to see which
persona/agent is doing what, at which stage. Progress only surfaces after the fact in per-agent
Execution Logs and `pipeline-summary.md`. Someone (or something) running the CLI should be able to
follow the run, uncluttered.

## What Changes

- Personas/stages SHALL emit a structured `start`/`done` run event as they run (a machine-readable
  projection of what already goes into the Execution Log) to one append-only stream.
- A deterministic renderer SHALL present an uncluttered "what agent is doing what" view over that
  stream (live tail, tree, and final summary).
- The boundary holds: agents do the work and emit events reporting it; the schema fixes the shape and
  the renderer fixes the presentation — it performs no analysis, scheduling, or agent spawning.

## Capabilities

### New Capabilities
- `pipeline-observability`: the run-event stream (schema + emission points) and the deterministic
  renderer that makes stage/persona progress transparent.

### Modified Capabilities
<!-- none -->

## Impact

- New: `evals/reliability/tm_observe.py` (renderer), `evals/reliability/events.py` (schema + helpers
  incl. deriving events from a workflow run's transcripts), `references/pipeline-observability.md`.
- Modified: `SKILL.md` (orchestration emits events around each Task spawn), `evals/reliability/run.py`
  (emit/derive events).
- No change to what any agent analyzes; events are a projection of existing Execution Log data.
