# Data mode — make the doc define the data this system exposes and the contract downstream consumers depend on

**Consumer:** data/analytics engineering lead who owns the warehouse, the event/CDC pipeline, and downstream data products (dashboards, models, reverse-ETL), and who also consumes this system when its data product is a queried analytics API or a shared read replica rather than an emitted feed.
**Done means:** I can integrate this system as a source — emitted feed, analytics API, or read replica — without reverse-engineering its database, predict the blast radius of any schema change before it ships, model the cost of the data path, and hold the producing team to a written data contract with owners, SLAs, and a breaking-change process.

## Required in the doc
- **Data-product catalog** — every event, table, API endpoint, or read replica this system exposes for downstream consumption, with schemas, field types, and semantics.
- **Access mode per product** — for each, whether consumers receive an emitted feed (event/CDC/batch/file), query an analytics API, or read a shared replica directly, since that decides who owns coupling and load.
- **Schema evolution policy** — compatibility rules, versioning scheme, and the breaking-change process.
- **Lineage / integration section** — how data leaves the operational store and reaches consumers (CDC vs batch vs streaming vs direct query), with the transformations applied.
- **Data contract** — named producer owner, freshness/completeness SLAs, and consumer obligations.
- **Identifier & key reference** — primary keys, surrogate vs natural keys, and how entities join across this system and others.
- **PII / regulated-data inventory** for the analytics path — which emitted/queryable fields are personal, financial, health, or otherwise regulated.
- **Downstream dependency map** — which dashboards, models, and reverse-ETL flows consume this data.
- **Time-semantics statement** — event-time vs processing-time, timezones, and ordering guarantees.

If the doc has none of these, demand the catalog first; nothing else is reviewable without it.

## Rubric

### Event taxonomy & schemas
- **Complete data-product inventory** — every event topic, outbox table, CDC stream, analytics API endpoint, shared read replica, and exported file the system exposes for downstream consumption, named explicitly. An undocumented source is an unmonitored source; consumers discover it by breaking.
- **Per-event schema** — for each event: field name, type, nullability, units, enum domains, and a one-line meaning per field. "userId: string" is not a schema; demand whether it's the app user, the billing account, or the auth subject.
- **Naming conventions** — event names, field names, casing (snake vs camel), and namespace/prefix rules. Inconsistent naming forces per-source special-casing in every downstream model.
- **Event semantics** — is each event a state-change fact (immutable), a snapshot, or a command? Mixing fact and snapshot semantics in one stream silently corrupts aggregations.
- **Required vs optional fields** — which fields are guaranteed present vs best-effort. Consumers build joins and filters on "guaranteed"; demand the line between the two.
- **Cardinality & volume** — events/sec and per-day row counts per source, peak vs steady. Drives warehouse partitioning, cost, and whether streaming is even viable.
- **Payload size & nesting** — typical and max payload size, nesting depth, arrays/maps. Deeply nested JSON blobs become flatten-tax and break columnar storage assumptions.
- **Envelope vs payload** — is there a standard envelope (event id, type, version, timestamp, source, trace id)? A missing event id kills dedup; a missing version kills evolution.

### Schema registry & evolution
- **Registry of record** — where schemas live (a schema registry, an IDL/proto repo, declared warehouse sources, or just a wiki). If the answer is "the code," there is no contract and consumers cannot pin to anything.
- **Compatibility mode** — backward, forward, or full compatibility declared per subject, and what's actually enforced at publish time vs aspirational. Consumers plan upgrades against this guarantee.
- **Versioning scheme** — how versions are expressed (topic suffix, envelope field, registry subject version) and how a consumer pins or negotiates a version.
- **Breaking-change definition** — what counts as breaking (drop/rename field, type narrow, enum value removal, semantic change to an existing field). Enum-value additions and silent semantic changes are the ones that bite; demand they be named.
- **Breaking-change process** — notice period, dual-publish/expand-contract path, consumer sign-off, and deprecation window. "We'll Slack you" is not a process; demand who must be notified and how far in advance.
- **Additive-change handling** — confirm new optional fields don't require consumer redeploys and default sensibly in existing pipelines. If an additive change can break a consumer, every release becomes a coordinated deploy and the producer loses the ability to ship independently.
- **Schema CI** — is compatibility checked in the producer's CI before merge? Without it, the policy is unenforced and every release is a roll of the dice.
- **Deprecation & sunset** — how a field/event is marked deprecated, how usage is measured before removal, and the actual sunset date. Fields never die without usage telemetry.

### Lineage & warehouse/lake integration
- **Extraction / access mechanism** — CDC (log-based vs trigger-based), batch extract, event stream, API poll, or direct replica query, named per source. Each has different latency, completeness, delete-handling, and coupling characteristics; a directly-queried replica couples consumers to the operational schema with no contract layer.
- **CDC specifics** — if CDC: log-based vs trigger-based, how hard deletes and soft deletes surface downstream, and whether before-images are available. Deletes invisible to CDC silently inflate every downstream count.
- **Landing target & format** — destination (warehouse schema, lake path), file/table format and whether it is columnar, and partitioning scheme. Drives query cost and what late data can be reprocessed.
- **Transformation boundary** — what's transformed in-flight vs raw-landed-then-transformed (ELT). Demand the line; in-flight transforms are invisible to downstream debugging.
- **Lineage map** — source table/event → landing → staging → mart → consumer, end to end. Without it, no one can answer "if this column changes, what breaks?"
- **Load pattern** — append, upsert/merge, truncate-reload, or snapshot. Determines whether reloads are idempotent and whether history is preserved.
- **Sync frequency & latency** — extract cadence and end-to-end source-to-warehouse latency, with the SLA. Dashboards promise freshness they can only keep if this is pinned.
- **Schema drift handling** — what the pipeline does when the source adds/changes a column unexpectedly (auto-evolve, fail, drop). Auto-evolve hides breaks; fail-closed surfaces them.

### Cost of the data path
- **Storage growth** — projected size and growth rate of raw, staging, and mart layers per source, and whether raw is kept forever or aged out. Append/CDC sources compound; "cheap storage" becomes the biggest line on the bill without a retention plan. (See also the finops mode for the full cost model.)
- **Per-query cost** — for warehouse and analytics-API paths, the cost shape of the heavy consumers (scanned bytes, slot/credit time) and whether wide nested payloads force full-row scans. A flatten-on-read mart over deeply nested JSON can cost more per dashboard load than the pipeline that built it.
- **Egress & movement cost** — cross-region or cross-cloud transfer for replication, replica reads, and reverse-ETL syncs. Egress on a chatty replica or a high-frequency reverse-ETL flow is invisible until the bill arrives.
- **Cost ownership** — who is charged for the warehouse/API spend this source drives, and whether it is showback or chargeback to consumers. Uncharged data is uncapped data; without an owner, no one rationalizes a runaway query or an over-retained raw zone.

### Data contract & quality
- **Producer ownership** — named team and on-call for each dataset, not "the platform team." Contracts need a counterparty who answers pages.
- **Freshness SLA** — max acceptable lag per dataset and what consumers should do when it's breached. Stale data presented as live is worse than a visible outage.
- **Completeness guarantee** — expected row counts/ranges, and detection for partial loads or dropped partitions. A 70%-loaded day looks like a real business dip.
- **Validation rules** — declared constraints (not-null, ranges, referential integrity, accepted enum values) and where they're enforced (producer, pipeline, or only discovered downstream). Enforcement only at the consumer means the producer ships bad data and the consumer eats the incident.
- **Test coverage bar** — a stated definition of "enough" quality coverage: which columns and which rule classes (nullability, uniqueness, referential, freshness, accepted-values) must carry an automated test, and the minimum coverage on key and critical columns, run as CI on the data path rather than ad hoc. Left to reviewer judgment, coverage drifts to whatever was easy; a named bar turns a gap into a defect instead of an opinion.
- **Quality monitoring & alerting** — what's checked (volume anomalies, null spikes, schema mismatch, freshness), who's paged, and the runbook. Quality without alerting is hope.
- **Delivery guarantee** — at-least-once, at-most-once, or exactly-once, and the dedup key consumers must use. At-least-once with no event id forces consumers to invent dedup.
- **Ordering guarantee** — per-key ordering, global ordering, or none. Out-of-order state-change events corrupt last-write-wins logic.
- **Contract artifact** — is the contract a versioned, machine-readable spec (a data-contract file or model contract checked into the repo) or just prose? Machine-readable contracts can be CI-enforced; prose rots.
- **Consumer obligations** — what consumers must do (pin versions, handle nulls, tolerate replays, not depend on undeclared fields). A contract is two-sided; demand the consumer side.

### Identifiers & joinability
- **Primary key per entity/event** — the key, its stability, and whether it's globally unique or scoped. Unstable keys make incremental loads and joins unreliable.
- **Surrogate vs natural keys** — which keys are system-internal surrogates vs business-natural, and which is safe to join on across systems. Surrogates don't travel; consumers must know.
- **Cross-system join keys** — how this system's entities join to other sources (customer, account, product). Missing a shared key means manual fuzzy-matching downstream.
- **ID format & namespacing** — UUID vs sequence vs composite, and whether ids can collide across environments/tenants. Reused ids across tenants silently merge unrelated records.
- **Foreign-key relationships** — declared references between this system's datasets, and whether referential integrity holds at landing time given async loads. Late-arriving parents break FK joins.
- **Slowly-changing dimensions** — for entities that change (customer plan, status), is history tracked (SCD type 2) or overwritten? Point-in-time correctness in reports depends on this.
- **Tenant / partition key** — multi-tenant discriminator and whether it's present on every row. Row-level tenant isolation downstream requires it on every record.

### PII & regulated data in the analytics path
- **PII/regulated inventory** — which fields reaching consumers (via warehouse, API, or replica) are personal, financial, health, or otherwise regulated, classified per field. You can't protect what isn't inventoried (see also compliance mode).
- **Masking/tokenization point** — where sensitive fields are masked, hashed, or tokenized, and whether raw values ever land in the lake. Raw PII in a "temporary" raw zone is still a breach surface.
- **Access controls in the warehouse** — who can query PII columns, via what role/policy (column-level security, row-level security, masking policies). "The warehouse is internal" is not an access control.
- **Join-key reidentification risk** — whether hashed/tokenized join keys can be reversed or correlated to reidentify subjects. Consistent hashing enables joins and reidentification at once.
- **Retention & deletion** — how long PII persists downstream and how a deletion/erasure request propagates to the warehouse, lake, and backups. DSAR/right-to-erasure obligations don't stop at the operational DB.
- **Derived-data leakage** — whether aggregates, models, or reverse-ETL outputs re-expose PII the raw layer protected. Masking source columns is moot if a mart unmasks them.
- **Audit of sensitive queries** — whether access to regulated columns is logged. Compliance reviews ask who queried what.

### Reporting & metrics dependencies
- **Downstream dependency inventory** — named dashboards, semantic-layer metrics, ML feature pipelines, and reverse-ETL flows that consume this data. The blast radius of a change is invisible without it.
- **Blast-radius per field** — for high-traffic fields, which consumers break if it changes. Lets the producer assess impact before, not after, shipping.
- **Critical metrics traceability** — which board-level / revenue / SLA metrics depend on these datasets. A schema change to a revenue source is a different conversation than a debug log.
- **Single metric definition** — for each metric this source feeds, whether one canonical definition exists (in a semantic layer or shared model) or each consumer rolls its own SQL. Two dashboards computing "active users" from the same table with different filters report different numbers and burn a quarter arguing which is right.
- **Metric ownership & certification** — who owns each metric's definition, whether definitions are certified/reviewed before they become "official," and how a change to a definition is versioned and announced. An uncertified metric on an exec dashboard is a number nobody is accountable for; demand the owner and the certification gate.
- **Reverse-ETL exposure** — whether this data is synced back into operational tools (CRM, ads, billing). Reverse-ETL turns a quiet schema change into a customer-facing one.
- **Consumer notification path** — how downstream owners learn of changes (registry subscribers, contract CI, a channel). Closes the loop on the breaking-change process.

### Historical, backfill & reprocessing
- **Replayability** — can the source be replayed/re-extracted to rebuild downstream from scratch, and over what window? Without replay, a pipeline bug is permanent data loss.
- **Idempotent loads** — re-running a load produces the same result (merge on key, not blind append). Non-idempotent loads make backfills double-count.
- **Backfill procedure** — documented process to reload a date range, including throttling and not corrupting incremental state. Ad-hoc backfills are how production marts get clobbered.
- **Late-arriving data** — how the pipeline handles events that arrive after their window closed (restate, drop, side-table) and the lateness bound. Late data silently understates closed periods.
- **Retention at source** — how long the source retains data available for re-extraction (CDC log/topic retention). Short retention caps how far back you can ever rebuild.
- **Reprocessing trigger** — what forces a reprocess (logic bug, schema fix, restated source) and who authorizes it. Reprocessing overwrites history; it needs an owner.

### Time semantics
- **Event-time vs processing-time** — every timestamp field labeled as when-it-happened vs when-we-saw-it. Aggregating on the wrong one shifts every time-series report.
- **Watermarks / completeness signal** — how a consumer knows a time window is complete enough to aggregate. Without it, dashboards report partial windows as final.
- **Timezone handling** — are timestamps UTC, local, or naive, and is the offset stored? Naive local timestamps across DST make duplicate or missing hours.
- **Timestamp precision & clock source** — precision (s/ms/us) and source (app clock, DB clock, ingest clock). Skewed clocks reorder events and break sessionization.
- **Effective-dating** — for dimension/state data, the valid-from/valid-to semantics enabling point-in-time joins. Reports that need "as of" state are wrong without it.
- **Ordering vs time** — whether timestamp order matches delivery order, and the max skew. Consumers doing last-write-wins on timestamp need the skew bound.

## Grill order
1. **Data-product inventory** — get the full list of events/datasets/APIs/replicas this system exposes and how each is accessed. Nothing downstream is reviewable until this exists.
2. **Per-event schemas + identifiers** — types, nullability, semantics, and the keys consumers join on.
3. **Data contract: ownership, freshness, completeness, delivery/ordering guarantees** — the obligations I hold the producer to.
4. **Schema evolution & breaking-change process** — versioning, compatibility, notice period, CI enforcement.
5. **Lineage & integration** — CDC vs batch vs streaming vs direct query, landing format, transformation boundary, load pattern, latency.
6. **Cost of the data path** — storage growth, per-query cost of the heavy consumers, egress, and who is charged.
7. **PII in the analytics path** — inventory, masking point, warehouse access, deletion propagation.
8. **Downstream dependency map & blast radius** — who breaks when this changes; metric definitions and ownership; reverse-ETL exposure.
9. **Time semantics** — event vs processing time, watermarks, timezones.
10. **Backfill / replay / late data** — replayability, idempotency, lateness handling.
11. **Polish** — naming conventions, machine-readable contract artifact, test coverage bar, deprecation telemetry.

## Deliverable
Leave these artifacts in the architecture doc:

- **Data-Product Catalog** — one row per source. Columns: `name` | `access mode (event/CDC/batch/file/API/replica)` | `schema/registry link` | `primary key` | `delivery guarantee` | `ordering` | `volume (peak/day)` | `producer owner` | `current version`.
- **Schema table per source** — columns: `field` | `type` | `nullable?` | `units/enum domain` | `meaning` | `PII class` | `required vs optional`.
- **Data Contract block per dataset** — fields: `owner team + on-call` | `freshness SLA` | `completeness rule` | `validation rules` | `test coverage bar` | `quality alerts + runbook` | `consumer obligations` | `deprecation policy`. Link a machine-readable spec where one exists.
- **Lineage diagram** — source → extraction (CDC/batch/stream) → landing/format → staging → mart → named consumers, with load pattern and latency annotated on each hop.
- **Identifier & join matrix** — columns: `entity` | `primary key` | `surrogate/natural` | `cross-system join key` | `SCD type` | `tenant key`.
- **PII-in-analytics register** — columns: `field` | `classification` | `masking/tokenization point` | `lands raw? (y/n)` | `who can query` | `deletion propagation path`.
- **Downstream dependency / blast-radius map** — columns: `consumer (dashboard/model/reverse-ETL)` | `datasets used` | `metric definition + owner` | `critical metric?` | `certified?` | `breaks-if-changed notes`.
- **Cost-of-path line** — per source: storage growth rate, raw retention, per-query cost shape of the heavy consumers, egress exposure, and who is charged (showback/chargeback).
- **Time-semantics note** — per timestamp field: event vs processing time, timezone, precision, and the watermark/completeness signal consumers use.
