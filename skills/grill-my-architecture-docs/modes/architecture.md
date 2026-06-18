# Architecture-review mode — make the doc let the review board judge fit, longevity, and decisions, not just today's correctness

**Consumer:** Enterprise / domain architecture review board (chief architect, domain architects, integration and data architecture leads) holding go/no-go authority against the target-state estate.
**Done means:** The board can decide approve / approve-with-conditions / reject from the doc alone — they can see how this design moves the estate toward (or away from) published target architecture, every significant decision is recorded with its alternatives and consequences, reuse-vs-build is settled, exposed interfaces are governed and cataloged, lock-in and exit cost are quantified, the multi-year capacity/cost trajectory is forecast, and whatever this replaces has a funded sunset plan. A correct-but-undocumented design is a reject.

**See also:** reliability, finops, and security modes own the deep grilling of run-cost economics, SLO/capacity engineering, and identity/threat detail respectively; this mode checks only that those concerns conform to estate standards and are owned, and hands off the depth rather than re-grilling them.

**When reference artifacts are missing or stale:** target architecture, capability map, API catalog, and approved-tech lists are often partial or out of date. Do not treat their absence as an automatic blocker, and do not let it excuse the design. Establish which exist and how current they are, then grade against the best available expression of intent (a draft, a principles doc, the chief architect's stated direction), and record the artifact gap itself as a finding for the board. State explicitly in each affected rubric line whether the design is being judged against a published artifact or against inferred intent, so the board knows the confidence behind the call. A target artifact is itself open to challenge: if this design diverges because the target is wrong or stale, that is a candidate to amend the target, not a divergence to apologize for — say so and route it as a target-change proposal.

## Required in the doc
- **Diagram set** — context, container, component, sequence (key flows), deployment, and data-flow views, each consistent with the prose.
- **Target-state alignment statement** — where this sits on the published target architecture / capability map and the multi-year roadmap, with every deliberate divergence flagged.
- **Standards conformance section** — approved-technology list status plus interoperability standards (wire protocols, canonical data formats, eventing/integration standards).
- **Reuse assessment** — existing capabilities/services evaluated for reuse before any net-new build.
- **Decision record / ADR log** — every significant decision with context, alternatives considered, and consequences.
- **API governance register** — each exposed interface: contract, owner, catalog registration, standards conformance, deprecation/sunset policy.
- **Vendor lock-in / exit analysis** — switching cost, portability, contractual exit terms, fallback for strategic dependencies.
- **Multi-year capacity and run-cost forecast** — load growth, infra footprint, cost trajectory with stated assumptions.
- **Legacy sunset plan** — for whatever this replaces or overlaps: decommission timeline, cutover dependency, dual-run funding, who turns the old thing off.
- **Technical debt and decommission register** — shortcuts taken with payback plans, plus how this system itself is eventually retired.

## Rubric

Scale the demand to the change. The full register set is mandatory for a new platform, a strategic dependency, or a one-way door; for a small or fast-moving design, demand the substance (the decision was made deliberately, the divergence is owned, the interface is governed) without the ceremony of a 30-entry ADR log or a five-year forecast. The test for each artifact is whether its absence would let a real risk go unjudged, not whether the template has an empty cell. When you waive an artifact as disproportionate, say so explicitly so the board sees it was considered and skipped, not missed.

### Target-state alignment
- **Position on the target architecture** — demand a concrete mapping to the published target-state / capability model: which capability this realizes, which target building block it instantiates. Without it the board cannot judge fit, only correctness.
- **Roadmap placement** — where this falls on the multi-year roadmap (now / next / later, or the named wave/horizon). A design that is correct but off-roadmap timing is a conditional approval at best.
- **Direction of travel** — does this move the estate toward the target or entrench a state the target wants to retire? Demand an explicit "converges / neutral / diverges" call per major component, not a blanket claim.
- **Deliberate divergence register** — every place this knowingly departs from target architecture, each with: reason, blast radius, and either a dated convergence plan (how and when it rejoins the target) or an explicit case that the target itself is wrong and should move. Undocumented divergence is the single most common silent reject — flag it hard. But do not treat the target as automatically authoritative: a divergence that is the right long-term call against a stale or wrong target should be routed as a target-amendment proposal with the same rigor, not forced into a convergence plan that walks the estate back toward a worse state.
- **Convergence plan ownership** — who owns closing each divergence, and what triggers it (funding, a platform GA, a dependency retirement). A divergence with no owner and no trigger is permanent debt mislabeled as temporary.
- **Strategic intent fit** — alignment with stated architecture principles (e.g. buy-before-build, cloud-first, event-driven, API-first, data-as-product). Name the principle and show conformance or a justified exception; an unexamined principle violation is how a design quietly sets a precedent the board never agreed to.
- **Reference architecture conformance** — if a domain/solution reference architecture exists, show conformance or document the gap. Missing this lets a one-off pattern leak into the estate.
- **Capability overlap** — does this duplicate a capability the target already assigns to another platform/team? Overlap must be named and resolved, not discovered later by the board.

### Standards and interoperability
- **Approved-technology status** — every technology tagged against the approved list: approved / emerging / contained / retiring / prohibited. Anything off-list needs an exception reference. If no approved list exists or it is stale, say so and grade against stated direction rather than waving the check through — an unvetted technology choice becomes an estate-wide support, license, and skills liability the board absorbs.
- **Wire protocol standards** — conformance to corporate protocol standards (REST/HTTP semantics, gRPC, GraphQL, messaging transport). Demand the named standard, not "we use HTTP."
- **Canonical data format conformance** — payloads aligned to the enterprise canonical/common data model and shared schemas; deviations mapped. Divergent local formats are integration debt the board absorbs estate-wide.
- **Eventing / messaging standards** — event envelope, schema registry usage, topic/queue naming, ordering and delivery semantics against the org eventing standard. Missing this fractures the event backbone.
- **Identity and integration standards** — conformance to the enterprise service-to-service auth standard (OAuth2/OIDC/mTLS) and to the sanctioned integration patterns (sync vs async, orchestration vs choreography). Demand only the conformance statement here and defer the threat depth to the security mode; a bespoke auth or integration shape is estate-wide operability and security debt the board inherits. Note which standard, if any, actually exists to conform to.
- **Versioning standard** — interface and schema versioning scheme against corporate policy (semver, URI vs header versioning, backward-compat rules). Without a stated scheme, every consumer integrates against an implicit contract and the first breaking change becomes an estate-wide incident.
- **Observability/telemetry standards** — conformance to mandated logging, tracing, metrics formats and correlation-id propagation so the system is operable within the shared estate tooling. Scope this to format/standard conformance only; SLOs, alerting quality, and on-call design belong to the reliability mode, so do not re-grill them here. A system that emits off-standard telemetry is invisible in shared dashboards and unsupportable by central ops.
- **Localization / accessibility / regulatory standards** — where mandated, confirm conformance or scope an exception; cheaper to surface at review than at audit.

### Reuse vs duplication
- **Reuse inventory checked** — evidence that existing platforms, shared services, and capabilities were searched before deciding to build. "We didn't know it existed" is an avoidable board finding.
- **Build justification** — for each net-new component, why an existing service was not reused (fit gap, capacity, ownership, cost). The board needs the rejected-reuse reasoning, not just the build decision.
- **Shared-service consumption** — which enterprise shared services this consumes (auth, notifications, payments, document store, MDM). Reinventing a shared service is a default reject.
- **Component contribution-back** — anything built here that is reusable should be flagged for promotion to a shared asset, with ownership. Otherwise the estate accumulates near-duplicate private copies.
- **Data duplication** — any data this re-masters that an authoritative source already owns; demand system-of-record alignment, not a new local copy of golden data.

### Decision records (ADRs)
- **Coverage of significant decisions** — every architecturally significant decision has an ADR: technology selection, integration style, data ownership, build-vs-buy, divergence from target. Absence of an ADR for a load-bearing choice blocks sign-off.
- **Context per decision** — the forces and constraints at decision time (deadline, skills, existing contracts, regulatory). Future readers must understand why it was reasonable then.
- **Alternatives considered** — at least the credible options that were rejected, with why. An ADR with one option is a justification, not a decision record.
- **Consequences** — positive and negative, including debt incurred and doors closed. The board judges longevity from consequences, not from the chosen option alone.
- **Status and supersession** — proposed / accepted / superseded, with links when a later ADR overrides an earlier one. A stale ADR presented as current is a trap.
- **Reversibility classification** — one-way vs two-way door per decision. One-way doors deserve disproportionate board scrutiny; the doc should pre-sort them.
- **Decision owner and date** — who decided and when, so accountability and recency are legible.

### API governance and catalog
- **Interface inventory** — every exposed interface (sync API, async topic, batch/file, webhook) listed; shadow interfaces are how integration debt hides.
- **Contract artifact** — machine-readable contract per interface (OpenAPI, AsyncAPI, protobuf, schema). "Documented in the wiki" is not a contract.
- **Contract owner** — a named accountable owner per interface, not a team alias only. Ownerless interfaces rot.
- **Catalog registration** — each interface published to the org API/service catalog with its registration ID, or a dated plan to register. Unregistered interfaces are invisible to future reuse and impact analysis.
- **Corporate API standards conformance** — naming, error model, pagination, auth, rate limiting, idempotency against the corporate API standard; deviations justified.
- **Consumer model** — known/expected consumers, internal vs partner vs public exposure, and the SLA tier offered. Drives deprecation obligations.
- **Deprecation and sunset policy** — versioning lifecycle, notice period, and sunset commitment per interface, conforming to corporate policy. An interface with no sunset policy is a permanent commitment by default.
- **Backward-compatibility rules** — what counts as breaking, and the change process. Protects every downstream consumer the board is responsible for.

### Vendor lock-in and exit cost
- **Strategic dependency map** — each vendor/managed-service/proprietary dependency and how strategically locked-in it is (commodity / substitutable / proprietary / single-source). Without the classification the board cannot tell a swappable convenience from a bet-the-estate commitment, and prices the risk wrong.
- **Switching cost** — concrete cost and effort to move off each significant dependency (re-platform effort, retraining, data egress). "We could switch" without a number is not an answer.
- **Data and config portability** — can data and configuration be exported in open, re-importable formats? Proprietary-only export is a hidden one-way door.
- **Contractual exit terms** — notice periods, data-return obligations, egress fees, price-escalation caps, source-code escrow where relevant. The board owns these long after the project team disbands.
- **Fallback / continuity plan** — what happens if a strategic dependency is acquired, sunset, price-shocked, or fails. At minimum a stance (accept / mitigate / dual-source).
- **Concentration risk** — over-reliance on a single vendor across the estate; flag if this design deepens an existing concentration the board is trying to reduce.

### Multi-year capacity and cost
- **Scope boundary** — this mode checks that a multi-year trajectory exists, names its scaling cliffs, and is owned; the finops mode owns unit-economics and budget depth, the reliability mode owns capacity/SLO engineering. Demand the trajectory and the handoff, not a second full costing. Re-grilling the same numbers across modes wastes the board's time and double-counts the same gap.
- **Load growth model** — projected demand over a multi-year horizon (3–5y typical) with stated growth assumptions and their source. A point-in-time sizing tells the board nothing about longevity.
- **Capacity headroom and scaling limits** — where the architecture hits a ceiling (a hard partition limit, single-writer bottleneck, license tier cap) and at what load. The board needs to know the cliff before the estate hits it.
- **Run-cost trajectory** — projected run cost over the horizon, not just year-one, with the cost drivers and unit-economics assumptions (cost per transaction/tenant/GB).
- **Cost sensitivity** — which assumptions, if wrong, blow up the forecast (egress, per-call licensing, storage growth). Cheap insurance against a surprise renewal.
- **Footprint trajectory** — infra footprint growth (environments, regions, nodes) and its estate-wide implications (shared-platform pressure, license pool draw).
- **Decommission cost** — the cost and effort to eventually retire this system, so total lifecycle cost is visible, not just stand-up cost.

### Legacy sunset and dual-run
- **What this replaces or overlaps** — explicit list of existing systems/capabilities this supersedes or partially overlaps. Silent overlap is how the estate accumulates zombies.
- **Decommission timeline** — dated plan to retire the legacy, gated on this system reaching parity/cutover milestones. "Eventually" is not a plan the board can approve.
- **Cutover dependency** — what must be true before the old thing can be turned off (data migrated, consumers repointed, parallel-run validated). Surfaces hidden coupling.
- **Dual-run funding and ownership** — who pays for running both systems during overlap, for how long, and who owns the decision and the act of turning the old one off. Unfunded dual-run is the classic stranded-legacy failure.
- **Data migration and reconciliation** — how data moves from legacy and how parity is proven. Without reconciliation, "decommissioned" is a hope.
- **Stranded-capability check** — any legacy capability this does NOT replace, and where it goes. Half-replacements leave the estate worse than before.

### Technical debt and exit
- **Debt register** — shortcuts and known compromises taken to ship, each with impact and a payback plan (owner + trigger/date). Undeclared debt is the debt that never gets paid.
- **Debt vs divergence linkage** — debt that exists specifically because of a target-architecture divergence should tie back to the convergence plan, so it is not paid twice or forgotten.
- **System exit / decommission design** — how THIS system is retired when its day comes: data export, consumer notice, interface sunset, infra teardown. A system with no exit story is a future stranded asset.
- **Sustainability / supportability** — who supports this long-term, skills required, and whether those skills are scarce in the org. Longevity is a people problem too.

### Diagram completeness and consistency
- **Context view** — system in its environment with external actors and systems. Anchors scope; its absence makes every other view ambiguous.
- **Container view** — deployable/runnable units and their responsibilities and communication. Without it the board cannot tell what is independently deployable or where the trust and failure boundaries fall.
- **Component view** — internal structure of the significant containers, sufficient to judge cohesion and coupling. Missing this hides the modularity decisions that drive long-term maintainability.
- **Sequence views** — the critical and failure-path flows, not just the happy path. The board reads risk from the failure paths.
- **Deployment view** — runtime topology: environments, regions, zones, network boundaries, where each container actually runs. Absent this, capacity, blast radius, and data-residency claims cannot be checked against reality.
- **Data-flow view** — how data moves and is mastered across the system and its integrations, including direction and classification. Without it, system-of-record duplication and data-residency/classification breaches stay invisible until audit.
- **Prose/diagram consistency** — diagrams must match the text and the registers (every interface on the diagram appears in the API register, every external dependency in the lock-in analysis). Inconsistency between views is a reliable signal of an unreviewed design.

## Grill order
1. **Target-state alignment + divergence register** — if you cannot place this on the target architecture and roadmap with divergences flagged and convergence plans owned, nothing else matters. Lead here.
2. **Reuse vs duplication** — settle build-vs-reuse and capability/data overlap before debating the internals of something that maybe should not be built.
3. **ADR coverage** — pin down that every significant decision has context, alternatives, consequences, reversibility. This is what lets future boards trust the design.
4. **API governance and catalog registration** — interfaces inventoried, owned, contracted, registered, with sunset policy.
5. **Vendor lock-in and exit cost** — quantify switching cost, portability, contractual exit, fallback for strategic dependencies.
6. **Legacy sunset and dual-run funding** — decommission timeline, cutover dependency, who funds dual-run and turns the old thing off.
7. **Multi-year capacity and run-cost forecast** — growth model, scaling cliffs, cost trajectory and sensitivity.
8. **Standards and interoperability conformance** — protocols, canonical formats, eventing, versioning, observability.
9. **Technical debt and system-exit register** — declared debt with payback, and this system's own decommission design.
10. **Diagram completeness and prose consistency** — close last; verify the views exist, cover failure paths, and agree with the registers.

## Deliverable
Leave these artifacts in the architecture doc:

- **Target-state alignment table** — columns: Component/Decision | Target capability/building block | Roadmap horizon | Direction (converges/neutral/diverges) | Notes.
- **Divergence & convergence register** — columns: Divergence | Reason | Blast radius | Convergence plan | Trigger | Owner | Target date.
- **Reuse assessment table** — columns: Capability/Data | Existing asset evaluated | Decision (reuse/build/contribute-back) | Justification | System of record.
- **ADR log** — one entry per significant decision: ID | Title | Status | Context | Alternatives considered | Decision | Consequences | Reversibility (one-way/two-way) | Owner | Date.
- **API governance register** — columns: Interface | Type (sync/async/batch/webhook) | Contract artifact (link) | Owner | Catalog ID/status | Standards conformance | Consumers/exposure | SLA tier | Deprecation/sunset policy.
- **Vendor lock-in & exit matrix** — columns: Dependency | Lock-in class | Switching cost | Data/config portability | Contractual exit terms | Fallback plan.
- **Multi-year capacity & cost forecast** — table or chart over the horizon: Year | Projected load | Footprint | Run cost | Key assumptions | Scaling limit reached?
- **Legacy sunset plan** — columns: Legacy system/capability | Replaced/overlapped | Cutover dependency | Decommission date | Dual-run funder | Who turns it off | Migration/reconciliation approach.
- **Technical debt & decommission register** — columns: Item | Type (debt/divergence-linked) | Impact | Payback plan | Trigger/date | Owner; plus a system-exit subsection (data export, consumer notice, interface sunset, teardown).
- **Diagram set** — context, container, component, sequence (incl. failure paths), deployment, data-flow views, each captioned and cross-referenced to the registers above.
