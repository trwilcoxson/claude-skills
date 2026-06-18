# Reliability mode — make the doc describe how this system behaves under failure, load, and recovery, well enough to run it

**Consumer:** The SRE / production-engineering lead who carries the pager for this system and owns its SLOs.
**Done means:** A pager-carrying engineer who has never seen the code can, from this doc alone, deploy it, roll it back, predict what breaks when any dependency dies, drive it through a degraded mode, fail it over, restore it from backup, and know which alert wakes whom — without guessing.

See also: `data.md` for deep data-correctness and consistency grilling; this mode covers data only where it threatens availability and recovery.

## Required in the doc
- Deployment topology diagram — every tier/zone/region, instance counts, what's stateful vs stateless.
- Release & rollback procedure — including the schema-change rollback rule.
- Dependency inventory — every upstream and downstream, tiered hard vs soft.
- Failure-modes & degraded-modes table — per dependency: timeout, retry, breaker, what the user sees when it's down.
- SLO table with error budget, plus SPOF list.
- Replication & failover topology with a tested-failover record (game-day evidence).
- Backup & DR section with RPO/RTO and a tested-restore record.
- Observability section — the signals, dashboards, and the alerts that page.
- Runbook index and on-call surface.
- Capacity/quota table including external rate limits.
- Cost-of-downtime figure tied to the SLO/DR investment.

## Rubric

### Deployment topology & release
- **Topology is drawn, not described** — demand a diagram showing every tier, AZ/region, load balancer, and the instance/replica count per tier. Prose like "runs on Kubernetes" hides whether a single node loss takes the service down. Mark each box stateful or stateless.
- **Single vs multi-AZ vs multi-region** — state the actual spread. "Multi-AZ" with all replicas pinned to one AZ by an anti-affinity gap is a lie the diagram exposes. If single-region, say so and own the regional-outage exposure.
- **Release mechanism** — name it: rolling, blue/green, canary, all-at-once. State batch size / surge / max-unavailable. All-at-once on a stateful tier is a self-inflicted outage waiting to happen.
- **Canary criteria & bake time** — if canary, what metric gates promotion and how long it bakes. A canary with no automatic abort metric is just a slower full deploy.
- **Rollback mechanism & time** — exact command/pipeline to roll back, and the measured time from "decide to roll back" to "old version serving." Untimed rollback is untested rollback.
- **Rollback safety under schema change** — THE question: after a migration runs, can the previous code version still run against the new schema? Demand the expand/contract (parallel-change) discipline — additive deploy, backfill, switch reads, contract later — or an explicit statement of the point of no return. Name the irreversible migrations (column drop, type narrow, NOT NULL add, table rename) and the procedure when rollback is no longer code-only (forward-fix, restore-from-backup, dual-write). A doc that says "we can always roll back" without this is wrong by default.
- **Migration/code ordering & gating** — does the migration run before, during, or after the code deploy? Is the new code dark-launched behind a flag until the migration completes? Get the sequence; out-of-order is where the 3am outage lives.
- **Long-running / locking migrations** — flag any migration that takes a table lock or rewrites a large table. State whether it runs online (e.g. gh-ost/pt-osc style) and the lock/duration budget. A blocking ALTER on a hot table is an outage disguised as a deploy.
- **Config/artifact immutability** — is the deployed artifact pinned by digest, or by a mutable tag like `:latest`? Mutable tags make "what's running" and "rollback target" undefined.
- **Stateful-tier deploy & restart story** — how do datastores, brokers, caches get upgraded/restarted without data loss or split-brain? Stateless tiers are easy; this is where it actually hurts.

### Scaling & bottlenecks
- **Scaling model per tier** — horizontal/vertical, auto or manual, the trigger metric and thresholds, min/max bounds. "It autoscales" without the trigger and ceiling is not a model.
- **First bottleneck to give out** — under sustained load growth, what saturates first — connection pool, DB write IOPS, a single-threaded leader, an external rate limit, a queue? Name it. If the team can't, they've never load-tested.
- **Scaling that doesn't help** — call out tiers where adding instances makes it worse (more app pods exhausting the same DB connection pool). This is the classic scale-the-wrong-thing incident.
- **Cold-start / warm-up** — does a new instance need cache warm-up, JIT, or pool fill before it can take full load? Autoscaling that adds cold instances during a spike can deepen the spike.
- **Load-test evidence** — the measured throughput ceiling and latency curve, not a guess. "We think it handles 10k rps" vs "tested to 8k rps, p99 cliff at 8.5k" are different documents.

### Dependencies & blast radius
- **Complete dependency inventory** — every upstream (callers) and downstream (DBs, caches, queues, third-party APIs, auth, DNS, secrets store, config service). The one left off the list is the one that takes you down.
- **Hard vs soft per dependency** — for each: is it required for the core request path (hard) or can the system function without it (soft)? This is the single most important reliability classification; everything downstream depends on it.
- **Blast radius per dependency** — concrete: "when X dies, the system does Y." Not "degrades gracefully." Hard dep down = which requests fail with what error; soft dep down = which feature is lost.
- **Transitive / shared dependencies** — does a soft dependency secretly call a hard one? Do two "independent" dependencies share a datastore or auth provider so they fail together? Correlated failure breaks the hard/soft model.
- **Synchronous coupling depth** — how many synchronous hops does one user request fan out into? Each sync hop multiplies failure probability and latency. Deep sync chains are fragile by construction.
- **Dependency version/compatibility failure** — separate from a dependency dying: a downstream ships a breaking API/schema/protocol change while still up. Demand contract versioning, consumer-driven contract tests or schema-registry compatibility gates, and what the system does on an unexpected response shape (reject vs corrupt). A dependency that's "up" but incompatible is a blast-radius gap that health checks miss entirely.

### Streaming, batch & stateful processing (if applicable)
Skip this block only if the system is purely request/response. If any tier is event-driven, a stream processor, or a batch/ETL pipeline, the sync-HTTP rubric is not enough.
- **Delivery & processing guarantees** — at-least-once vs at-most-once vs effectively-exactly-once per stream, and how it's achieved (idempotent sinks, dedupe keys, transactional writes). "Exactly-once" asserted without the mechanism is marketing; the wrong guarantee silently drops or double-counts data.
- **Consumer lag as data loss** — is consumer/replication lag monitored and alerted, and what's the retention vs worst-case lag? If lag exceeds broker retention, unconsumed records are gone — silent data loss that no error surfaces. Name the retention-vs-lag headroom.
- **Checkpoint / offset recovery** — where processing state and offsets are committed, and whether a restart resumes from the last checkpoint without reprocessing or skipping. Offset committed before the side effect = data loss on crash; after = duplicates. Get the ordering.
- **Watermarks & late/out-of-order data** — for windowed/stateful processing, the watermark/allowed-lateness policy and what happens to data arriving after the window closes (dropped, side-output, reprocessed). Silent drop of late events is a correctness bug disguised as reliability.
- **Backfill & reprocessing** — can a pipeline replay from a point in time after a bug or outage, and is reprocessing idempotent so a replay doesn't double-apply? A pipeline you can't safely re-run leaves you with permanently wrong data after any incident.
- **Batch/ETL failure & partial-run recovery** — for batch jobs: what happens on mid-run failure — resume, full rerun, or corrupt partial output? State idempotency and whether downstream sees partial results. A non-idempotent batch with no checkpoint corrupts the warehouse on every retry.

### Failure modes & recovery
- **Per-dependency timeout** — every outbound call has an explicit connect and read timeout, documented. A missing timeout is an unbounded hang that exhausts your thread/connection pool and turns one slow dependency into a full outage.
- **Retry policy & budget** — which calls retry, how many times, with what backoff and jitter, and the total retry budget so retries can't amplify a downstream brownout into a retry storm. Retries without a budget are a DDoS you aim at yourself.
- **Idempotency of retried operations** — any retried write must be idempotent (idempotency key, dedupe, conditional write). Retrying a non-idempotent payment/charge/email is a double-charge incident.
- **Circuit breakers** — which dependencies sit behind a breaker, the open/half-open thresholds, and behavior while open (fail fast, fallback, shed). Without breakers, a dead dependency keeps consuming timeout budget on every request.
- **Timeout budget alignment** — do caller timeouts exceed the sum of downstream timeouts plus retries? Misaligned budgets mean the caller gives up while work continues, or hangs longer than the user-facing SLA.
- **Partial-failure / poison handling** — what happens to a message/job that always fails — DLQ, max-attempts, alert? Unbounded reprocessing of a poison message stalls the whole queue.
- **Thundering herd / cache stampede** — on cache expiry or cold start, do N requests all hit the origin at once? Demand request coalescing / single-flight / staggered TTL, or own the stampede risk.
- **Network-layer failure modes** — name them explicitly, not just "the dependency is down": DNS resolver failure and stale/short TTL behavior (does a stale record point at a dead endpoint, does resolution failure fail open or hard?), load-balancer connection limits and what happens when they're hit, and partial network partitions / packet loss where a dependency is reachable-but-slow rather than cleanly dead. Partial partitions are nastier than clean failures because breakers and health checks flap instead of tripping. State the connect-vs-read timeout split and whether DNS resolution itself is timed.

### Clock & time
- **Clock-skew tolerance** — where the system assumes synchronized clocks (token/JWT expiry, certificate validity, distributed locks/leases, ordering, cache TTLs) and how much NTP skew it tolerates before things break. Skew silently rejects valid tokens or expires leases early; name the NTP source and the failure if it drifts.
- **Time-based expiry as a failure source** — short-lived tokens, signed-URL expiry, lease/lock TTLs: what happens at the boundary, and whether clock drift or a slow renewal path turns a valid request into a 401/403. Time-based auth failures look like outages and get misdiagnosed for hours.
- **Leap second / DST / monotonic-vs-wall-clock** — does any timer, scheduler, or duration measurement use wall-clock time where it should use a monotonic clock? Leap seconds and DST jumps have taken down schedulers and caused negative durations; call out the assumption or own the risk.

### Degraded modes (named, not generic)
- **A defined degraded state per soft dependency** — for each non-critical dependency, the specific reduced-functionality state: feature flag off, serve stale cache, read-only mode, queue-and-replay, default value. "Graceful degradation" with no named state is a wish, not a design.
- **How degraded mode is entered and exited** — automatic on breaker-open, or a manual flag flip? Who decides, and how does the system recover to full function when the dependency returns? Modes you can enter but not cleanly exit are traps.
- **User-visible contract in each mode** — what the user actually sees and what's silently dropped. "Stale up to 5 min" vs "writes rejected" are different promises to make explicit.
- **Stale-data bounds** — if a mode serves stale cache, the maximum staleness and whether that's acceptable for the data (stale price/balance/permission can be a correctness or compliance problem, not just UX).
- **Degraded-mode tested (with evidence)** — has each degraded path actually been exercised by killing the dependency in a real environment, with a date and the observed user-visible behavior recorded — or is it dead code asserted to work? Untested fallbacks fail when first invoked; a "tested" claim with no record of what was observed is the same as untested.

### Backpressure & load-shedding
- **Queue-depth limits** — bounded queues with a max depth and defined behavior at the limit (block, reject, shed). Unbounded queues convert a load spike into an OOM and hide latency until collapse.
- **Load-shedding policy** — when overloaded, what gets shed and in what priority order? Health checks and critical paths protected, lower-priority traffic dropped first. No shed policy means everything degrades together until total failure.
- **Admission control / rate limiting** — inbound limits per client/tenant/endpoint so one caller can't starve the rest. Plus the response on limit (429 with Retry-After). Noisy-neighbor protection.
- **Buffer / pool saturation behavior** — when the connection pool, thread pool, or memory buffer saturates, does it fail fast or queue unboundedly? Fail-fast-when-full beats silent latency growth into collapse.
- **Backpressure propagation** — does pressure at the bottom propagate up so upstreams slow down, or do they keep pushing until something breaks? Flow control end to end vs local-only.

### Availability, SLOs & redundancy
- **SLOs defined and measured** — availability and latency targets (p50/p95/p99) per critical path, with the actual SLI definition (what counts as a good request, measured where). A target with no SLI is unmeasurable.
- **Error budget & policy** — the budget derived from the SLO and what happens when it's burned (freeze releases, focus on reliability). A burn alert and a burn policy, not just a number.
- **SPOF inventory** — every single point of failure: single DB primary, single NAT gateway, single leader, single region, single third-party with no alternative, one person who knows the runbook. Each SPOF either gets redundancy or an explicit accepted-risk sign-off.
- **Redundancy model** — N+1 / N+2 / active-active per tier, and whether you can lose an instance/AZ/region and stay within SLO. State the headroom; running at N with no spare means any single failure is an incident.
- **Health checks** — liveness vs readiness distinction, what each probes, and that readiness actually pulls a sick instance from the LB. A liveness check that passes while the instance can't serve is worse than none.
- **Graceful shutdown / connection draining** — on deploy or scale-down, are in-flight requests drained and the instance deregistered before kill? Hard kills drop live requests on every deploy.

### Replication & failover (distinct from backup/restore)
- **Replication topology** — primary/replica layout per datastore, sync vs async, and the replication lag under normal and peak load. Async replication has a data-loss window; name it.
- **Data-loss window (RPO at failover)** — with async replication, how much committed data can be lost on an unplanned failover? This is separate from backup RPO and is often worse.
- **Failover trigger & mechanism** — automatic (with what detector and quorum) or manual; the promotion procedure and who runs it. Automatic failover with no fencing invites split-brain.
- **Split-brain prevention** — fencing / quorum / STONITH so two primaries can't accept writes simultaneously. The most expensive data-corruption incidents come from undefended dual-primary.
- **Multi-region data consistency under failover** — for active-active or any topology that accepts writes in more than one place during a partition or failover, name the conflict-resolution rule for application data: last-write-wins (and on whose clock — see clock-skew), CRDTs, vector clocks, or a single-writer-per-key partition. LWW across regions silently discards a real user write whenever two regions update the same record; "active-active" with no stated conflict policy is undefined data behavior, not redundancy.
- **Measured failover time** — actual time to detect + promote + reconverge, from a real or game-day test, not the vendor brochure number.
- **Game-day evidence (artifact, not a checkbox)** — not just a date: demand the actual evidence of a real drill — the runbook/ticket link, the measured detect-and-promote numbers, what broke and the follow-up fixes. A bare "tested Q3" with no measured time, no incident notes, and no artifact is a claim, not a test; treat it as untested until the evidence shows a real failover happened.
- **Failback procedure** — how you return to the original primary after it recovers, and whether failback is as safe as failover. Teams test failover and forget failback.

### Backup & disaster recovery
- **RPO / RTO stated and justified** — recovery point and recovery time objectives per datastore, tied to the cost-of-downtime, not pulled from the air.
- **Backup scope, schedule, retention** — what's backed up, how often, kept how long, and whether it covers everything needed to rebuild (data + schema + config + secrets). A backup missing the config can't restore the system.
- **Backup isolation / immutability** — backups in a separate account/region and immutable (ransomware/operator-error resistant). A backup deletable by the same creds that run prod is not a backup.
- **Tested restore (with the evidence artifact)** — not just a date: the measured restore time vs the RTO, the data-integrity check that confirmed the restored copy was actually usable (row counts, checksum, app-level validation), and the ticket/log link proving a restore actually ran. "We test restores quarterly" with no measured number and no artifact is a hope wearing a checkbox; an untested backup is no backup, and an unverified restore is the same thing.
- **DR scenario coverage** — region loss, datastore corruption, accidental mass delete, ransomware. Each with a defined recovery path, not just "we have backups."
- **Encryption & key availability in DR** — if data is encrypted at rest, are the keys recoverable in the DR scenario, or are they in the region you just lost? Lost-key restore is a permanent outage.

### Certificates, secrets & expiry
- **Cert/secret expiry inventory** — every TLS cert, signing key, API token, mTLS cert, and service-account credential with its expiry and rotation owner. Expiry is a scheduled outage you can prevent.
- **Rotation procedure & zero-downtime overlap** — rotation done with overlapping validity (new credential accepted before old is revoked), not a hard cutover. Hard cutover rotation is a self-inflicted outage.
- **Expiry alerting** — alerts fire well before expiry (e.g. 30/14/7 days), to a human who can act. Cert-expiry outages are pure unforced errors.
- **Auto-renewal failure handling** — if certs auto-renew (ACME etc.), what happens and who's paged when renewal fails? Silent renewal failure surfaces as an outage at expiry.

### Observability
- **The four signals** — logs, metrics, traces present for every critical path, and what each captures; specifically, can you trace one request end to end across services? Missing any one signal means a class of incident you can see happening but can't localize, which is MTTR spent guessing.
- **Golden-signal dashboards** — latency, traffic, errors, saturation per service, on a dashboard a responder opens during an incident, with the link in the runbook. No pre-built incident dashboard means the responder is authoring queries at 3am while the outage runs.
- **Alerts that page vs alerts that inform** — which conditions page a human (symptom-based: SLO burn, error rate, latency, saturation), and which are FYI. Cause-based alert spam without symptom alerts means you page on noise and miss the real outage.
- **Alert quality** — each paging alert has a threshold, a clear owner, and a linked runbook; no alert without an action. Alerts nobody can act on get muted, then the real one gets muted too.
- **Correlation IDs / structured logs** — request/trace IDs propagated so logs across services can be stitched. Grepping unstructured logs across N services during an incident is how MTTR explodes.
- **Saturation & leading indicators** — metrics that predict trouble before users feel it (queue depth, pool utilization, replication lag, disk fill rate, GC pressure). Lagging-only signals mean you find out from customers.
- **Synthetic / black-box monitoring** — an external prober hitting the real user path, so you detect outages independent of internal metrics that may also be down. Without it, a failure that also takes down your telemetry is invisible until customers report it.

### Runbooks & on-call
- **Runbook per paging alert** — every alert that pages has a runbook: symptoms, diagnosis steps, mitigation, escalation. A page with no runbook is a 3am research project.
- **On-call surface defined** — who's on call, rotation, escalation chain, and the auth/access a responder needs at 3am (is break-glass access pre-provisioned or blocked behind a daytime approval?). Access friction during an incident is pure added MTTR.
- **Top failure-scenario playbooks** — explicit playbooks for the likely big ones: dependency down, DB failover, rollback-a-bad-deploy, drain-a-region, restore-from-backup, enter/exit degraded mode. The first time you write the steps for one of these should not be while it's happening; absent playbooks turn the highest-stakes incidents into improvisation.
- **Escalation & comms** — when to escalate, to whom, and the incident-comms channel (status page, stakeholders). Reliability includes telling people it's broken.
- **Maintenance / freeze windows** — defined change windows, and the deploy-freeze policy during high-traffic events. Deploying into Black-Friday peak is a choice the doc should force.

### Capacity & quotas
- **Capacity headroom** — current peak utilization vs provisioned, per tier, and the headroom before the next scaling action is forced. Running hot with no headroom means the next spike is an incident.
- **External rate limits & quotas** — every third-party API limit, cloud service quota (instances, IPs, connections), and DB connection cap, with current usage vs limit. Hitting an undocumented cloud quota mid-incident blocks your own recovery.
- **Quota-exhaustion behavior** — what the system does when it hits a quota (queue, shed, fail) and whether quota-approach is alerted. Silent quota walls cause confusing partial outages.
- **Growth runway** — at current growth, when does each capacity/quota dimension run out? Forces the provisioning conversation before it's urgent.

### Configuration & feature flags
- **Config source & change safety** — where runtime config lives, how it's changed, and whether a bad config change can be rolled back as fast as code. Config changes cause as many outages as code; treat them with the same rigor.
- **Feature-flag inventory & kill switches** — flags that gate risky features and the kill switches for degraded modes, with who can flip them and how fast they propagate. Flags are your fastest mitigation; document them or you won't find them mid-incident.
- **Flag-propagation latency & failure** — how long a flag flip takes to reach all instances, and the default if the flag service is unreachable. A flag that fails open to "on" during a flag-service outage is a hidden hard dependency.
- **Dynamic config blast radius** — can one config push hit all instances/regions at once with no canary? Global instant config push is a global instant outage vector.

### Cost of downtime
- **Quantified cost of downtime** — revenue/SLA-penalty/reputational cost per hour (or per the relevant unit), even rough. This is what justifies the SLO target, the DR spend, and the redundancy headroom. Without it, every reliability investment is an unwinnable argument and the doc can't defend its own targets.

## Grill order
1. **Hard/soft dependency classification + blast radius** — without this, no failure analysis is possible; it gates everything below.
2. **Rollback safety under schema change** — the single most common way "safe" deploys cause unrecoverable outages; pin expand/contract and the point of no return.
3. **Per-dependency timeout / retry-budget / idempotency / breaker** — the mechanics that stop one slow dependency becoming a full outage. For any event-driven, streaming, or batch tier, take the streaming block here too: delivery guarantee, consumer-lag-vs-retention, checkpoint/offset recovery.
4. **Named degraded mode per soft dependency** — turn "graceful degradation" into specific, exitable, tested states.
5. **SLOs, SPOFs, redundancy headroom** — the availability targets and whether the topology can actually meet them.
6. **Replication topology, data-loss window, tested failover** — and split-brain defense; separate from backup.
7. **Backup/DR with RPO/RTO and a tested restore** — prove recovery, don't assume it.
8. **Backpressure & load-shedding + first bottleneck** — behavior at and beyond capacity.
9. **Deployment topology, release/rollback mechanics, scaling model** — the operate-it basics.
10. **Cert/secret expiry & rotation** — cheap to fix, common to forget.
11. **Observability — paging alerts, dashboards, traces** — can you see it break.
12. **Runbooks, on-call surface, capacity/quota, config/flags** — the operational layer.
13. **Cost of downtime** — last, but it's what makes the rest of the doc fundable; capture the figure even if rough.

## Deliverable
Leave these artifacts in the architecture doc:

- **Dependency & blast-radius table** — columns: Dependency | Direction (up/down) | Tier (hard/soft) | Timeout | Retry policy & budget | Idempotent (Y/N) | Circuit breaker (Y/N) | Behavior when it dies (degraded state) | Shared with.
- **Streaming/pipeline reliability table** (if any event-driven, streaming, or batch tier exists) — columns: Stream/job | Delivery guarantee | Dedupe/idempotency mechanism | Retention | Worst-case lag | Lag alert | Checkpoint/offset store | Late-data policy | Backfill/replay (safe Y/N).
- **Failure-modes / degraded-modes table** — columns: Failure scenario | Detection | Automatic response | Degraded state entered | User-visible contract | Max staleness | Exit/recovery condition | Tested (date + evidence link).
- **SLO & error-budget table** — columns: Critical path | SLI definition | SLO target | Window | Error budget | Burn-alert threshold | Burn policy.
- **SPOF register** — columns: SPOF | Tier | Mitigation / redundancy | Accepted-risk owner & date (if no mitigation).
- **Replication & failover record** — topology diagram + table: Datastore | Replication (sync/async) | Lag (normal/peak) | RPO at failover | Failover trigger | Split-brain defense | Multi-region write-conflict rule | Measured failover time | Last game-day (date + evidence link) | Failback procedure.
- **Backup & DR table** — columns: Asset | Backup schedule | Retention | Isolation/immutability | RPO | RTO | Last tested restore (date + evidence link) | Measured restore time | Integrity check used.
- **Cert/secret rotation register** — columns: Credential | Type | Expiry | Rotation owner | Zero-downtime overlap (Y/N) | Expiry alert lead time.
- **Capacity & quota table** — columns: Resource | Limit/quota | Current peak usage | Headroom | Behavior at limit | Alert threshold | Growth runway.
- **Deployment topology diagram** — tiers, zones/regions, instance counts, stateful/stateless markers, LBs.
- **Release & rollback procedure** — including the schema-change expand/contract rule and the named point-of-no-return migrations.
- **Alert-to-runbook index** — columns: Paging alert | Trigger condition | Owner | Runbook link.
- **Cost-of-downtime figure** — stated per hour (or relevant unit), with the SLO/DR investments it justifies.
