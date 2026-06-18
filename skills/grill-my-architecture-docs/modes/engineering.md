# Engineering mode — make the doc let an implementer build against this system correctly without reading the source

**Consumer:** A staff/senior engineer on a neighboring team integrating with or extending this system. They hold sign-off when they can implement a correct client (or a correct change) from the doc alone.
**Done means:** A competent engineer who has never seen the source can write a caller that hits the right endpoints/events with the right payloads, sets correct timeout/retry/idempotency budgets, handles every documented error and degradation, paginates and bulk-loads safely, and knows which fields/endpoints they are allowed to depend on — without reading the code, without asking the owning team, and without being surprised in production.

## Required in the doc
- **Component / context map** — the services in scope, what each owns, who calls whom.
- **Interface catalog** — every public API, event, and schema a consumer touches, with versions; and for code-level integration, the published library/SDK package, its semver policy, and compatibility surface.
- **Data model + ownership** — core entities, their store, the single owning service.
- **Consistency & transaction model** — consistency level per read path, transaction boundaries, cross-service consistency mechanism.
- **Delivery & ordering guarantees** — per channel/topic/queue.
- **Error & idempotency contract** — error taxonomy, idempotency-key semantics, retry rules, DLQ.
- **Stability contract** — what is public/supported vs private/internal; deprecation policy; extension points.
- **Tech stack + rationale** — languages, frameworks, datastores, brokers, and why.
- **Key sequence flows** — happy path plus at least one failure/contended path, end to end.
- **Migration & rollout plan** — for the change this doc proposes, if any.
- **Build / test / CI-CD** — how a change ships, with the gates it must pass.

If the interface catalog, data ownership, or error/idempotency contract is missing, stop and demand it before grilling anything else — the doc is not reviewable for this lens without them.

## Rubric

### Component contracts — interfaces & schemas
- **Endpoint/operation inventory** — demand a complete list of every operation a consumer can call (HTTP method+path, RPC method, GraphQL field, CLI). A partial list means consumers reverse-engineer from the source, which is the exact failure this lens exists to prevent.
- **Request schema, field by field** — for each operation: every field, type, required/optional, default, allowed values/enum, format (e.g. RFC3339, UUID v4), units, and constraints (length, range, regex). Vague types ("a date", "an ID") cause silent serialization bugs at the boundary.
- **Response schema, field by field** — same rigor, including which fields are always present vs conditional, nullable vs absent, and the meaning of empty vs null vs missing.
- **Auth & authz on the contract** — what credential the call carries (token type, scope/claim required), and what authorization the callee enforces. Without it the integrator can't even make a successful first call.
- **Content types & encoding** — JSON/protobuf/avro, charset, compression, numeric precision (int64 vs float, money as minor units vs decimal string). "Just JSON" hides the int64-in-JavaScript precision trap.
- **Schema source of truth** — OpenAPI/proto/Avro/JSON-Schema file location and how it's generated/validated, so the consumer codegens rather than hand-types DTOs. The machine-readable artifact is the contract; prose schemas in the doc rot the moment the code changes, so the doc must point at the generated file and a compat check, not restate fields it will fail to keep in sync.
- **Field semantics, not just types** — what each non-obvious field *means* and who sets it. A `status` enum is useless without the state it represents and who transitions it.

### Versioning & compatibility
- **Versioning scheme** — URI version, header, media-type, or schema-registry compat mode. Where the version lives and how a consumer pins it; if a consumer can't pin, every provider release can silently change its contract underneath them.
- **Backward compatibility promise** — what the provider guarantees won't break within a version (no field removal, no type narrowing, no enum-value removal, additive-only). State it explicitly; "we try not to break things" is not a contract.
- **Forward compatibility expectation** — what consumers must tolerate (unknown fields, new enum values, new event types). If consumers must ignore-unknown, say so — strict parsers will break on the next additive change.
- **Breaking-change & deprecation policy** — how breaking changes are introduced (new version side-by-side), notice period, deprecation signaling (Sunset header, changelog, registry), and how long old versions run.
- **Enum/lookup evolution** — can new enum values appear without a new version? What must a consumer do on an unrecognized value (fail, drop, route-to-unknown)?

### Library / SDK consumers — integration as linked code, not over-the-wire
- **Published-package contract** — if consumers integrate by depending on a shared library/SDK as code (not an API), demand the package coordinates (registry, group/artifact or npm/PyPI name) and the semver policy: what a major/minor/patch bump is allowed to change. Without a stated semver contract a consumer can't safely set a version range and a routine "minor" bump breaks their build.
- **Binary / ABI / source compatibility** — for compiled or typed languages: whether the package promises source compat, binary/ABI compat, or neither across a given range, and which surface is public API vs incidentally-exported internals. A consumer that links against an internal symbol breaks on an upgrade with no warning.
- **Transitive dependency footprint** — the library's own runtime dependencies and their version ranges, plus any that are likely to collide with a consumer's tree (logging, serialization, an HTTP client, a gRPC runtime). Undocumented transitive pins produce diamond-dependency conflicts the consumer can't resolve without reading the source.
- **Supported runtimes & toolchain** — language/runtime versions, compiler/SDK floor, and platform/arch matrix the package supports. A consumer on an unlisted runtime hits undefined behavior, not a clean error.
- **Release & deprecation cadence for the package** — how releases are cut, how long a major line gets fixes, and how deprecations are signaled in-code (annotations, compiler warnings). This is the package-world analogue of the API deprecation policy and governs how a consumer plans upgrades.

### Inter-service SLAs — what a caller may rely on
- **Published consumer SLA per operation** — the latency (p50/p95/p99), availability, and throughput a caller is entitled to assume. This is the *consumer-facing* promise, distinct from the provider's internal SLO; it's what sets the caller's timeout and retry budget. Missing this and every integrator guesses, then either times out too early or hangs.
- **Timeout guidance** — the recommended client timeout per operation, derived from the p99 + margin. Tell the caller the number so independent teams don't pick conflicting ones.
- **Rate limits & quotas** — per-consumer limits, the algorithm (token bucket/fixed window), burst allowance, the response when exceeded (429 + `Retry-After`), and how quota is requested/raised.
- **Documented degradation modes** — what a caller sees when the service is degraded (e.g. stale reads served, a feature disabled, a field omitted, a fallback value). Callers must code for the degraded shape, not just the happy shape.
- **Backpressure & load-shedding signals** — how the service tells a caller to slow down (429, 503, queue-depth header) and the expected client reaction.
- **Capacity / concurrency limits** — max in-flight requests per consumer, max connections, payload-size-driven limits. Blocks the consumer from designing fan-out that the provider can't absorb.
- **SLO vs SLA delineation** — if internal SLOs are documented, mark clearly which numbers are promises to callers vs internal targets. (See also reliability mode for the provider-side error budget.)

### Data model & ownership
- **Core entity catalog** — each entity, its identity (key), lifecycle/states, and the relationships between entities. Without the nouns and how they connect, a consumer models the domain wrong and builds joins/state machines that don't match the source of truth.
- **Owning service per entity** — exactly one service owns the write path for each entity; name it. Ambiguous ownership produces dual writers and split-brain data.
- **Datastore per entity** — what store backs it (Postgres, Dynamo, Kafka topic, S3) and whether the consumer may read it directly or only via API. Direct DB reads against another team's tables are the most common stability violation; the doc must say yes/no.
- **Read models / projections** — any denormalized or cached read views, their freshness, and whether they're a supported access path. A consumer that reads a projection assuming it's authoritative and current gets stale data and files a false bug.
- **Identifiers consumers store** — which IDs are stable and safe to persist as foreign keys vs which are ephemeral/internal and will change. Persisting an internal ID that gets reassigned is a silent data-corruption bug.
- **PII / data-classification flags on fields** — which fields are sensitive, so the consumer handles/stores them correctly. (Security and compliance modes go deeper; engineering needs at least the flag.)

### Consistency & transactions
- **Consistency model per read path** — strong, read-your-writes, eventual (with bound), or monotonic. Specify per endpoint, not globally — different reads often differ. Without it, a caller reads-after-write and gets stale data, then files a false bug.
- **Replication / propagation lag** — for eventual paths, the expected and worst-case lag, so callers know how long to wait or whether to poll.
- **Transaction boundaries** — what is atomic within a single call and what is not. If two fields in one request can be partially applied, say so loudly.
- **Cross-service consistency mechanism** — saga, outbox, 2PC, or "none, eventually reconciled." Name the pattern, the compensating actions, and the window during which the system is inconsistent. This determines whether a caller can trust a success response means the whole effect happened.
- **Read-after-write contract** — explicitly: if I write then immediately read, do I see my write? On which endpoint? This is the single most common integration surprise.
- **Isolation / concurrent-write behavior** — optimistic concurrency (version/ETag), last-write-wins, or locking. How a consumer detects and handles a conflict (409 + how to retry).

### Delivery & ordering guarantees (per channel)
- **Per-channel delivery semantics** — for every queue/topic/webhook: at-least-once, at-most-once, or exactly-once. State it per channel; mixing assumptions across channels causes either dropped or duplicated effects.
- **Ordering guarantee** — global, per-key/partition, or none. If per-key, name the key. Consumers that assume ordering where there is none will process events out of sequence.
- **Dedup key & window** — for at-least-once channels: the exact field a consumer dedups on and the window over which duplicates can arrive. Without the key and window, the consumer can't build idempotent handling and will double-process.
- **Event schema & versioning** — same field-by-field rigor as APIs; event-type field, schema version, registry. Plus: are events fat (full state) or thin (id + fetch)?
- **Redelivery / replay** — can events be replayed (recovery, backfill)? Will a consumer see old events again, and must it tolerate that?
- **Poison-message / DLQ behavior on the producer side** — what the producer does with events it can't deliver, and whether/how a consumer can recover them.
- **Webhook specifics, if any** — signing/verification, retry schedule, expected consumer response (2xx semantics), timeout, and ordering across retries.

### Error handling & idempotency
- **Error taxonomy** — the full set of error codes/types a consumer can receive, each with: HTTP/gRPC status, stable error code (not just message), meaning, whether it's retryable, and the expected consumer action. A consumer cannot write correct error handling against prose.
- **Retryable vs terminal classification** — explicit per error. 4xx-but-retryable (429, 409-on-conflict) and 5xx-but-not-retryable cases must be called out — they violate the naive "retry 5xx, fail 4xx" rule.
- **Idempotency-key contract** — the exact field/header name, who generates it, its scope (per-operation, per-consumer), the dedup window, and what a retry with the same key returns (the original result vs a conflict). This is what makes safe retries possible; without it every retry risks a duplicate side effect.
- **Retry semantics & budget** — recommended retry count, backoff (exponential + jitter), and total budget so retries don't amplify into a cascade. Tie to the timeout guidance above.
- **Partial-failure shape** — for any operation that can partially succeed (bulk, fan-out), the response shape that reports per-item success/failure, and how the consumer retries only the failed subset.
- **Dead-letter handling** — where failed messages/requests land, retention, and the consumer's path to inspect/replay them.
- **Error response body schema** — the structured error envelope (code, message, details, correlation/trace id) so consumers parse rather than regex the message.
- **Correlation/trace propagation** — the header(s) a consumer must propagate (trace-id, request-id) so failures are debuggable across the boundary.

### Pagination, bulk & large payloads
- **Pagination model** — cursor vs offset, the page-size default and max, how the cursor is passed, and cursor opacity/expiry. Offset pagination over a mutating dataset skips/duplicates rows — if that's the model, document the hazard.
- **Ordering under concurrent writes** — what ordering pagination guarantees while the underlying data changes, and whether a consumer can miss or double-see rows mid-scan.
- **Total count** — is a total returned, is it exact or estimated, and is it expensive (should the consumer avoid requesting it)?
- **Bulk operations** — batch endpoints, max batch size, whether the batch is atomic or partial-success, and the per-item result shape.
- **Max request/response size** — hard limits in bytes/items, the error when exceeded, and the sanctioned pattern for exceeding them (chunking, async job, presigned upload).
- **Streaming / async large jobs** — for big exports/imports: the submit-poll-result pattern, job-status states, result retention, and how to resume.
- **Compression & payload shaping** — supported encodings and field-selection/sparse-fieldset support. Without them a consumer is forced to pull full objects in tight loops, blowing latency and bandwidth budgets the provider then has to absorb.

### Stability contract — what NOT to depend on
- **Public vs internal surface** — an explicit table marking every endpoint, event, field, and table as supported/public or internal/private. The whole lens hinges on this: consumers will depend on whatever they can reach unless told not to.
- **Internal fields exposed but unsupported** — fields that leak through the API but may change without notice; flag them so no one builds on a debug field.
- **Direct datastore access policy** — whether reading the owner's DB/topic directly is ever sanctioned, and if not, what the supported alternative is.
- **Deprecation policy & notice period** — concrete notice (e.g. 2 versions / 90 days), the signal channel, and migration guidance commitment.
- **Sanctioned extension points** — the supported ways to extend behavior: webhooks, plugins, hooks, custom-field/metadata bags, feature flags. If extension is expected, this is part of the contract, not an afterthought.
- **Unsupported-usage consequences** — what happens to consumers who depend on internal surface (no notice, will break). Stated plainly so the trade-off is owned by the consumer.

### Tech stack & rationale
- **Stack inventory** — languages, runtimes/versions, frameworks, datastores, brokers, cache, and infra primitives the consumer's integration touches or must match.
- **Rationale & constraints** — why these choices, and any that constrain the consumer (e.g. a broker that caps message size, a store that forbids cross-partition transactions). The constraint matters more than the brand name.
- **Client libraries / SDKs** — official SDKs, supported languages, and whether hand-rolled clients are supported. Avoids every team writing a fragile bespoke client.

### Critical sequence flows
- **Happy-path end-to-end** — at least one full sequence diagram across services for the primary use case, showing calls, events, and state transitions. Prose can't convey ordering and fan-out.
- **The gnarly path** — at least one failure/contended/compensating flow: a saga rollback, a retry-after-timeout, a concurrent-write conflict, or a partial failure. This is where integrations actually break and where the doc earns its keep.
- **Idempotency/retry shown in a flow** — a sequence that shows what a retried call does given the idempotency contract, so the contract is concrete, not abstract.

### Migration & rollout (if the doc proposes a change)
- **Compatibility of the change** — is it backward compatible for existing consumers; if not, the dual-version plan and the consumer migration ask.
- **Dual-write / backfill plan** — for data/schema changes: the dual-write window, backfill strategy, and how reads are kept correct during it.
- **Cutover sequence** — ordered steps, the point of no return, and how consumers are coordinated.
- **Rollback / undo** — concretely how to reverse each step, including data already migrated. "We'll roll back" without a data-undo plan is not a rollback.
- **Feature-flag / phased exposure** — how the change is gated and ramped, and how a consumer opts in/out.

### Build, test & CI-CD
- **Build & local-run** — how to build and run the service/component locally or against a sandbox, so an extender can iterate.
- **Test strategy & contract tests** — unit/integration/e2e layers, and specifically whether consumer-driven contract tests (Pact-style) exist so a consumer can verify compatibility in their own pipeline.
- **Failure-mode fixtures & fault injection** — how a consumer reproduces the provider's degraded and failure paths locally: contract-test fixtures for each error code, partial-success/bulk-failure responses, timeouts, 429/503 backpressure, and stale/degraded reads — plus any sandbox toggle or fault-injection hook to force them. Happy-path fixtures only let a consumer test the path that rarely breaks; most integration bugs live in the error and partial-success handling, and there's no way to exercise that handling without a way to provoke the failure.
- **CI-CD pipeline & quality gates** — the gates a change must pass (lint, tests, coverage threshold, schema-compat check, security scan) before merge/deploy. The schema-compat gate is the one that protects every downstream consumer.
- **Sandbox / staging environment** — a non-prod environment integrators can test against, with how to get access and how its data differs from prod.
- **Observability handles for consumers** — the trace/metric/log identifiers a consumer can use to debug their own integration against this system.

## Grill order
1. Interface catalog completeness — every operation/event listed, with field-by-field request/response schemas and a schema source of truth. If this is thin, nothing else matters.
2. Error & idempotency contract — error taxonomy with retryable flags, idempotency-key field/scope/window, retry budget. This is what makes a caller safe in production.
3. Inter-service consumer SLAs — latency/availability/throughput a caller may rely on, with timeout and rate-limit guidance.
4. Consistency & transactions — read-after-write per path, transaction boundaries, cross-service mechanism and its inconsistency window.
5. Delivery & ordering — per-channel semantics, ordering, dedup key + window.
6. Data model & ownership — entities, single owner, datastore, direct-access policy, stable vs ephemeral IDs.
7. Stability contract — public vs internal surface table, deprecation policy, extension points.
8. Pagination, bulk & large payloads — cursors, limits, partial success, max sizes.
9. Versioning & compatibility — scheme, backward/forward promises, enum evolution; for SDK/library consumers, semver policy, ABI/source compat, and transitive-dependency footprint.
10. Critical sequence flows — happy path plus one gnarly path.
11. Migration & rollout — only if the doc proposes a change.
12. Tech stack, build/test/CI-CD gates, sandbox — polish that makes integration smooth.

## Deliverable
Leave these artifacts in the architecture doc:

- **Interface catalog table** — one row per operation/event. Columns: Name | Type (HTTP/RPC/event) | Address (method+path / topic) | Public or Internal | Version | Auth/scope | Request schema ref | Response schema ref | Idempotent (Y/N + key) | Consumer SLA (p99 / avail) | Recommended timeout.
- **Error register** — Error code | Status | Meaning | Retryable (Y/N) | Consumer action | Appears on (operations).
- **Delivery & ordering matrix** — Channel | Delivery (at-least/at-most/exactly-once) | Ordering (global/per-key/none) | Ordering key | Dedup key | Dedup window | Replay possible (Y/N).
- **Data ownership table** — Entity | Owning service | Datastore | Direct read allowed (Y/N) | Consistency on read | Stable ID for FKs (Y/N).
- **Stability/support matrix** — Surface (endpoint/field/event/table) | Public or Internal | Deprecation notice | Sanctioned extension point (if any).
- **Idempotency & retry contract block** — key field name, scope, dedup window, retried-call return behavior, recommended retry count + backoff + total budget.
- **Two sequence diagrams** — happy path and one failure/compensation path, both spanning services and showing events and idempotent retries.
- **Migration register (if applicable)** — Step | Backward compatible (Y/N) | Dual-write/backfill | Rollback action | Consumer ask.
