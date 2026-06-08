## ADDED Requirements

### Requirement: Structured run-event stream
The pipeline SHALL record run events to a single append-only stream (`events.ndjson`, schema
`tm.run-event/1`): a `start` event when a persona/stage begins and a `done` event when its output
lands, each carrying `ts, run_id, seq, stage, persona, action, status, metrics, note`. The `done`
payload SHALL be a projection of the data already written to that persona's Execution Log — no new
analysis is introduced.

#### Scenario: A persona runs
- **WHEN** a persona/stage begins and later completes its output
- **THEN** the stream contains a `start` event and a `done` event for it, with stage, persona, and status set

#### Scenario: Done mirrors the execution log
- **WHEN** a `done` event is emitted
- **THEN** its metrics and note are a projection of that persona's Execution Log, introducing no new analysis

### Requirement: Ordering is stable
Event ordering SHALL be stable and not depend on the race between parallel agents: sequence numbers
are assigned centrally (or the renderer derives a total order from timestamps with a stable tiebreak).

#### Scenario: Parallel specialists
- **WHEN** several specialists run in parallel and emit events
- **THEN** the rendered order is deterministic for the same `events.ndjson`

### Requirement: Deterministic presentation only
The renderer SHALL be a pure function of `events.ndjson` to a terminal view, performing no analysis,
scheduling, or agent spawning. The same input SHALL always produce the same output.

#### Scenario: Re-render is identical
- **WHEN** the renderer is run twice on the same `events.ndjson`
- **THEN** it prints byte-identical output

### Requirement: Uncluttered stage/persona view
The renderer SHALL present an uncluttered view of which persona is doing what at each stage, in fixed
columns, with at least a one-line-per-event tail and a by-stage tree.

#### Scenario: Following a run
- **WHEN** a user runs the renderer over a run's events
- **THEN** they see, per event, the stage, the persona, and the action/status in aligned columns, with no extraneous output

### Requirement: Works over the actual multi-agent runs
The system SHALL be able to produce the event stream for the runs the harness actually performs,
including deriving events from a completed workflow run's agent transcripts.

#### Scenario: Deriving from a workflow run
- **WHEN** a workflow run has completed and its agent transcripts exist
- **THEN** an `events.ndjson` can be derived from them and rendered
