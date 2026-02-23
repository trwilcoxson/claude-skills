# Quality Attributes for Software Architecture

## What are Quality Attributes?

Quality attributes are the non-functional requirements that define **how** a system works, as opposed to **what** it does. Functional requirements describe behavior (the system shall process payments), while quality attributes describe properties of that behavior (the system shall process payments in under 200ms with 99.99% availability).

Architecture is primarily about satisfying quality attributes. Here is the critical insight: almost any functional requirement can be achieved with almost any architecture. You can build a payment system as a monolith, as microservices, as a serverless function, or as a mainframe batch job. All of them can process payments. The architecture decision is driven by the quality attributes: how fast, how reliable, how secure, how easy to change, how cheap to operate.

Quality attributes are sometimes called "-ilities" because many of them end with that suffix: scalability, reliability, maintainability, availability, testability, observability. But not all do: performance, security, and cost efficiency are equally important quality attributes that break the naming convention.

The most dangerous architectural failures come not from missing features but from neglected quality attributes. A system that does everything the user asked for but falls over at 100 concurrent users, takes 30 seconds to respond, or requires a full rewrite to add a new payment provider has failed architecturally, even though it is functionally complete.

Quality attributes interact with each other in complex ways. Improving one often degrades another. These tradeoffs are the essence of architecture work: there is no single "best" architecture, only architectures that make the right tradeoffs for a given context.

---

## ISO 25010 Product Quality Model (2023 Revision)

The ISO/IEC 25010:2023 standard provides a standardized taxonomy of software product quality. The 2023 revision updated the original 2011 model. Below is the full taxonomy with architecture relevance assessed for each category.

| Category | Sub-characteristics | Architecture Relevance |
|----------|-------------------|----------------------|
| **Functional Suitability** | Completeness, Correctness, Appropriateness | Low -- mostly functional design |
| **Performance Efficiency** | Time behavior, Resource utilization, Capacity | **HIGH** -- drives scaling, caching, data architecture |
| **Compatibility** | Co-existence, Interoperability | Medium -- affects integration design |
| **Usability** | Learnability, Operability, Error protection, Accessibility | Low -- mostly UI/UX |
| **Reliability** | Availability, Fault tolerance, Recoverability | **HIGH** -- drives redundancy, failover, data replication |
| **Security** | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity | **HIGH** -- drives trust boundaries, encryption, audit |
| **Maintainability** | Modularity, Reusability, Analysability, Modifiability, Testability | **HIGH** -- drives decomposition, coupling, cohesion |
| **Portability** | Adaptability, Installability, Replaceability | Medium -- drives abstraction layers |

The HIGH-relevance categories (Performance Efficiency, Reliability, Security, Maintainability) are the primary drivers of architectural decisions. An architect who addresses these four well has handled the majority of structural risk. The Medium-relevance categories (Compatibility, Portability) influence integration and abstraction decisions. The Low-relevance categories (Functional Suitability, Usability) are addressed primarily through design and implementation rather than architecture.

---

## Architecture-Relevant Quality Attributes Deep Dive

### 1. Availability

**Definition:** The proportion of time a system is operational and accessible when required for use. Availability encompasses both planned uptime and the system's ability to withstand and recover from failures.

**Why architects care:** Availability directly impacts business revenue and user trust. For many systems, every minute of downtime has a quantifiable cost. Achieving high availability requires deliberate architectural decisions about redundancy, failure detection, and recovery mechanisms. You cannot bolt availability onto a single-server architecture after the fact.

**Architectural tactics:**
- **Redundancy:** Deploy multiple instances of each component so that failure of one does not cause system failure. Applies to compute, storage, networking, and entire availability zones.
- **Failover:** Automatically detect failed components and redirect traffic to healthy ones. Includes active-passive, active-active, and leader election patterns.
- **Health checks:** Implement liveness and readiness probes so load balancers and orchestrators can detect and remove unhealthy instances before users are affected.
- **Graceful degradation:** Design the system to shed non-critical functionality under stress rather than failing completely. Serve cached data when the database is down. Disable recommendations but keep search working.
- **Bulkhead isolation:** Partition resources so that a failure in one area does not cascade to others. Separate thread pools, separate databases, separate circuits.

**Measurement:**
- Uptime percentage: 99.9% (three nines) = 8.77 hours downtime/year; 99.99% (four nines) = 52.6 minutes/year; 99.999% (five nines) = 5.26 minutes/year
- Mean Time Between Failures (MTBF)
- Mean Time To Recovery (MTTR)
- Recovery Point Objective (RPO) and Recovery Time Objective (RTO)

**Common tradeoffs:** Cost increases (redundant infrastructure is not free). Complexity increases (failover logic, consensus protocols, split-brain scenarios). Consistency may decrease (CAP theorem -- in a partition, choose availability or consistency, not both).

---

### 2. Scalability

**Definition:** The ability of a system to handle increased load (users, data volume, transaction rate) by adding resources, without requiring architectural changes.

**Why architects care:** Systems that cannot scale hit a wall. Rearchitecting under growth pressure is expensive and risky. Scalability must be designed in from the start through appropriate decomposition, data partitioning strategies, and statelessness.

**Architectural tactics:**
- **Horizontal scaling (scale-out):** Add more instances of a component rather than making one instance bigger. Requires stateless design or externalized state.
- **Partitioning/sharding:** Distribute data across multiple stores based on a partition key. Reduces per-node load and enables parallel processing.
- **Caching:** Store frequently accessed data in fast-access stores (Redis, Memcached, CDN, browser cache) to reduce load on origin systems.
- **Asynchronous processing:** Decouple request acceptance from request processing using message queues. Absorb traffic spikes without dropping requests.
- **Read replicas:** Scale read-heavy workloads by replicating data to read-only copies. Write to primary, read from replicas.

**Measurement:**
- Throughput at target load (requests/second at 10x current traffic)
- Scale-out time (how quickly new capacity comes online)
- Linear vs. sub-linear scaling curve
- Cost per unit of throughput at various scale levels

**Common tradeoffs:** Complexity increases significantly (distributed systems are harder to reason about, debug, and operate). Consistency may decrease (eventual consistency in distributed caches and replicas). Cost increases (more infrastructure, more operational overhead). Maintainability may decrease (sharding logic spreads across the codebase).

---

### 3. Performance

**Definition:** The responsiveness of a system in terms of latency (time to respond to a single request) and throughput (number of requests processed per unit of time).

**Why architects care:** Performance problems are often architectural, not implementational. No amount of code optimization can fix a chatty microservice architecture that makes 50 synchronous calls per request. Performance-sensitive paths need architectural attention: data locality, caching strategy, async boundaries, and protocol choices.

**Architectural tactics:**
- **Caching at multiple levels:** Application cache, distributed cache, CDN, database query cache, materialized views. Each level trades freshness for speed.
- **Connection pooling:** Reuse expensive connections (database, HTTP) rather than creating and destroying them per request.
- **Asynchronous I/O:** Use non-blocking I/O to handle many concurrent connections with fewer threads. Critical for I/O-bound workloads.
- **Query optimization and denormalization:** Structure data for read patterns. Use materialized views, pre-computed aggregations, and read-optimized schemas.
- **Content delivery networks (CDN):** Serve static and cacheable content from edge locations geographically close to users.

**Measurement:**
- P50 latency (median), P95 latency, P99 latency. The tail matters: P99 often reveals architectural bottlenecks that P50 hides.
- Throughput: requests per second, transactions per second
- Apdex score (Application Performance Index)
- Resource utilization under load (CPU, memory, network, disk I/O)

**Common tradeoffs:** Maintainability may decrease (caching adds invalidation complexity, denormalization violates DRY). Cost increases (CDNs, caching infrastructure, more compute for async processing). Data freshness decreases (cached data is stale data). Code complexity increases (async code is harder to reason about and debug).

---

### 4. Security

**Definition:** The degree to which a system protects information and data so that persons, other products, or systems have the degree of access appropriate to their types and levels of authorization.

**Why architects care:** Security is not a feature you add; it is a property of the architecture. Trust boundaries, encryption decisions, authentication flows, and authorization models are structural. A fundamentally insecure architecture cannot be patched to security; it must be redesigned.

**Architectural tactics:**
- **Authentication and authorization:** Centralized identity provider (IdP), OAuth 2.0 / OIDC flows, role-based or attribute-based access control (RBAC/ABAC), API key management.
- **Encryption:** TLS for data in transit, AES-256 or equivalent for data at rest, key management via HSM or cloud KMS. End-to-end encryption where appropriate.
- **Input validation and output encoding:** Validate all inputs at trust boundaries. Encode outputs to prevent injection attacks. Use parameterized queries for database access.
- **Audit logging:** Record who did what, when, and from where. Immutable audit logs for compliance. Log access to sensitive data separately.
- **Defense in depth:** Multiple layers of security so that a breach of one layer does not compromise the system. Network segmentation, WAF, intrusion detection, principle of least privilege.

**Measurement:**
- Vulnerability count (from SAST/DAST scans), categorized by severity
- Time-to-detect (mean time to identify a breach or intrusion)
- Compliance score against relevant standards (SOC 2, HIPAA, PCI-DSS, OWASP Top 10)
- Percentage of endpoints with proper authentication and authorization

**Common tradeoffs:** Usability may decrease (MFA adds friction, strict password policies frustrate users). Performance may decrease (encryption, token validation, and audit logging add latency). Development velocity may decrease (security reviews, penetration testing, compliance audits take time). Cost increases (security tooling, HSMs, WAFs, security team).

---

### 5. Maintainability

**Definition:** The degree of effectiveness and efficiency with which a system can be modified to improve it, correct it, or adapt it to changes in environment and requirements.

**Why architects care:** Most software cost is in maintenance, not initial development. The architecture determines whether changes are localized (change one module) or systemic (change everything). High maintainability directly translates to faster feature delivery, lower bug rates, and easier onboarding.

**Architectural tactics:**
- **Modularity:** Decompose the system into cohesive, loosely coupled modules with well-defined interfaces. Each module should have a single reason to change.
- **Loose coupling:** Minimize dependencies between modules. Use interfaces, events, and message passing rather than direct calls and shared state.
- **High cohesion:** Group related functionality together. A module should do one thing well, not a little bit of everything.
- **Clear interface contracts:** Define explicit APIs (REST, gRPC, function signatures) with versioning, documentation, and backward compatibility rules.
- **Automated testing:** Comprehensive test suites (unit, integration, contract, end-to-end) that catch regressions early and enable confident refactoring.

**Measurement:**
- Change lead time (time from code commit to production)
- Coupling metrics (afferent/efferent coupling, instability index)
- Test coverage (line, branch, mutation testing)
- Cyclomatic complexity trends
- Onboarding time for new developers

**Common tradeoffs:** Initial development time increases (designing clean interfaces and writing tests takes more effort upfront). Performance may decrease slightly (indirection through interfaces adds minor overhead). Over-engineering risk (excessive abstraction in the name of maintainability can itself become a maintenance burden).

---

### 6. Modifiability

**Definition:** The degree to which a system can be effectively and efficiently modified without introducing defects or degrading existing quality.

**Why architects care:** Modifiability is the architectural response to the certainty that requirements will change. An architecture that is easy to modify lets the business respond quickly to market changes. An architecture that resists modification becomes a competitive liability.

**Architectural tactics:**
- **Information hiding:** Encapsulate implementation details behind stable interfaces. Internal changes should not ripple to consumers.
- **Interface contracts:** Define explicit contracts between modules. Use API versioning to evolve without breaking consumers.
- **Dependency injection:** Inject dependencies rather than hard-coding them. Enables swapping implementations without changing consumers.
- **Feature flags:** Decouple deployment from release. Deploy new code behind flags and enable it gradually, with the ability to disable instantly.
- **Plugin architecture:** Design extension points where new functionality can be added without modifying existing code (Open/Closed Principle at the architecture level).

**Measurement:**
- Files changed per feature (fewer is better; a well-modularized system localizes changes)
- Regression rate (percentage of changes that introduce bugs elsewhere)
- Time to implement a standard-sized feature
- Blast radius analysis (how many components are affected by a single change)

**Common tradeoffs:** Abstraction overhead (every interface and injection point is code that must be maintained). Performance overhead (indirection has a cost, though usually negligible). Complexity (too many extension points make the system harder to understand).

---

### 7. Testability

**Definition:** The degree of effectiveness and efficiency with which tests can be established for a system and those tests can be used to determine whether specified criteria have been met.

**Why architects care:** Testability is an architectural property, not a testing-team problem. If the architecture makes testing hard (tight coupling, hidden dependencies, global state), no amount of testing effort can achieve adequate coverage. Testable architectures enable fast, reliable feedback loops.

**Architectural tactics:**
- **Dependency injection:** Pass dependencies as parameters or through a DI container. Enables replacement with test doubles (mocks, stubs, fakes).
- **Pure functions:** Isolate business logic into pure functions with no side effects. Pure functions are trivially testable: given input X, assert output Y.
- **Ports and adapters (Hexagonal Architecture):** Separate core logic from infrastructure concerns. Test the core without databases, networks, or file systems.
- **Test doubles:** Design interfaces that allow substitution of real implementations with controlled test implementations.
- **Contract testing:** Define and verify contracts between services independently. Each service tests that it conforms to and consumes the agreed contract.

**Measurement:**
- Test coverage (line, branch, path) -- but recognize coverage as a necessary-not-sufficient metric
- Test execution time (fast tests get run more often)
- Flaky test rate (percentage of tests that pass/fail non-deterministically)
- Mutation testing score (percentage of injected mutations caught by tests)

**Common tradeoffs:** Complexity of DI setup (dependency injection frameworks add configuration overhead). Abstraction proliferation (interfaces created solely for testability add indirection). Test maintenance cost (more tests means more code to maintain when interfaces change).

---

### 8. Observability

**Definition:** The ability to understand the internal state of a system by examining its external outputs. A system is observable when you can determine what happened, why, and where, without deploying new code or adding new instrumentation.

**Why architects care:** In distributed systems, failures are inevitable and often subtle. Without observability, debugging production issues becomes guesswork. Observability must be architected in: it affects logging infrastructure, tracing propagation, metrics collection, and data retention.

**Architectural tactics:**
- **Structured logging:** Emit logs as structured data (JSON) with correlation IDs, timestamps, severity levels, and contextual fields. Enable machine parsing and querying.
- **Distributed tracing:** Propagate trace context (trace ID, span ID) across service boundaries. Reconstruct the full path of a request through the system using tools like Jaeger or Zipkin.
- **Metrics collection:** Emit RED metrics (Rate, Errors, Duration) and USE metrics (Utilization, Saturation, Errors) from every component. Aggregate in a time-series database (Prometheus, CloudWatch).
- **Health endpoints:** Expose standardized health check endpoints that report component status, dependency health, and readiness to serve traffic.
- **Alerting:** Define alert thresholds on key metrics with escalation policies. Distinguish between pages (wake someone up) and notifications (look at this tomorrow).

**Measurement:**
- Mean Time to Detect (MTTD) incidents
- Trace completeness (percentage of requests with full end-to-end traces)
- Log coverage (percentage of error paths with contextual logging)
- Dashboard coverage (percentage of services with operational dashboards)

**Common tradeoffs:** Storage cost increases (logs, traces, and metrics generate significant data volume). Performance overhead (instrumentation adds latency, though typically small). Noise (too many alerts cause alert fatigue; too many metrics make dashboards unreadable).

---

### 9. Deployability

**Definition:** The ease, speed, and safety with which a system can be deployed to production environments. A highly deployable system can be released frequently with low risk and fast recovery.

**Why architects care:** Deployment is where architecture meets operations. A monolithic architecture that requires a 4-hour deployment window with 15 manual steps is architecturally constrained. A well-decomposed system with independent deployability enables high-frequency releases and rapid iteration.

**Architectural tactics:**
- **CI/CD pipelines:** Automate build, test, and deployment. Every commit is a release candidate. Pipeline failures block deployment.
- **Feature flags:** Decouple deployment from release. Ship code to production behind flags, enable gradually, and disable instantly if problems arise.
- **Canary deployments:** Route a small percentage of traffic to the new version. Monitor for errors and latency regression before proceeding to full rollout.
- **Blue-green deployments:** Maintain two production environments. Deploy to the inactive one, verify, then switch traffic. Instant rollback by switching back.
- **Rollback automation:** Automate the ability to revert to the previous version. One-click or automatic rollback on error threshold breach.

**Measurement:**
- Deployment frequency (daily, weekly, monthly)
- Change failure rate (percentage of deployments causing incidents)
- Mean Time to Recovery (MTTR) from a failed deployment
- Deployment duration (time from push to fully live)

**Common tradeoffs:** Infrastructure complexity increases (canary routing, blue-green environments, flag management systems). Cost increases (maintaining multiple environments). Operational knowledge required (teams need to understand deployment strategies and tooling).

---

### 10. Cost Efficiency

**Definition:** The total resource cost required to deliver and operate a unit of business value. Encompasses infrastructure cost, operational cost, development cost, and opportunity cost.

**Why architects care:** Every architectural decision has cost implications. Choosing microservices over a monolith increases infrastructure and operational cost but may reduce the cost of change. Over-provisioning wastes money; under-provisioning loses customers. Architects must make cost-aware tradeoffs.

**Architectural tactics:**
- **Right-sizing:** Match resource allocation (CPU, memory, storage) to actual usage. Avoid over-provisioning "just in case." Use monitoring data to size appropriately.
- **Autoscaling:** Scale resources up and down based on demand. Pay for peak capacity only when you need it, not 24/7.
- **Serverless:** Use function-as-a-service (Lambda, Cloud Functions) for sporadic or unpredictable workloads. Pay per invocation rather than per hour.
- **Spot/preemptible instances:** Use discounted compute for fault-tolerant workloads (batch processing, CI/CD, stateless workers). Accept the risk of interruption for 60-90% cost savings.
- **Caching:** Reduce expensive operations (database queries, API calls, computation) by caching results. A well-placed cache can reduce origin load by 90%+.

**Measurement:**
- Cost per request or cost per transaction
- Cost per user (monthly or annual)
- Infrastructure cost trend (month-over-month)
- Cost efficiency ratio (revenue per dollar of infrastructure cost)
- Waste metrics (idle resources, over-provisioned instances)

**Common tradeoffs:** May constrain other quality attributes. Cost-optimized architectures may sacrifice availability (fewer replicas), performance (smaller instances), or security (cheaper tiers with fewer features). The key is intentional tradeoff, not accidental.

---

## N x N Tradeoff Matrix

This matrix shows how optimizing for the row quality attribute typically affects the column quality attribute. These are tendencies, not absolutes -- specific architectural decisions may defy these patterns.

|  | Perf | Avail | Secur | Maint | Scala | Testa | Observ | Deploy | Cost |
|--|------|-------|-------|-------|-------|-------|--------|--------|------|
| **Performance** | -- | ○ | ↓ | ↓ | ○ | ↓ | ↓ | ○ | ↓ |
| **Availability** | ○ | -- | ○ | ↓ | ↑ | ○ | ↑ | ↓ | ↓ |
| **Security** | ↓ | ○ | -- | ↓ | ○ | ↓ | ↑ | ↓ | ↓ |
| **Maintainability** | ↓ | ○ | ○ | -- | ↑ | ↑ | ↑ | ↑ | ↑ |
| **Scalability** | ○ | ↑ | ○ | ↓ | -- | ↓ | ○ | ↓ | ↓ |
| **Testability** | ○ | ○ | ○ | ↑ | ○ | -- | ○ | ↑ | ○ |
| **Observability** | ↓ | ↑ | ↑ | ○ | ○ | ○ | -- | ○ | ↓ |
| **Deployability** | ○ | ↑ | ○ | ↑ | ○ | ↑ | ○ | -- | ↓ |
| **Cost** | ↓ | ↓ | ↓ | ○ | ↓ | ○ | ↓ | ○ | -- |

**Legend:** ↑ = tends to improve, ↓ = tends to hurt, ○ = neutral/independent

**How to read this matrix:** Row = "if I optimize for this." Column = "the effect on this." For example, row "Performance," column "Security" shows ↓, meaning that aggressive performance optimization tends to hurt security (bypassing validation, skipping encryption, reducing logging).

**Key insight from the matrix:** Maintainability is the most synergistic quality attribute -- improving it tends to improve scalability, testability, observability, deployability, and cost. This is why many architects prioritize maintainability as a foundation that enables other qualities.

---

## Quality Attribute Scenario Template

The standard six-part format for specifying quality attribute requirements precisely and testably. Vague statements like "the system should be fast" are useless. QA scenarios make requirements concrete and measurable.

| Part | Description | Example |
|------|-------------|---------|
| **Source** | Who or what generates the stimulus | End user, external system, attacker, timer, DevOps engineer |
| **Stimulus** | The event or condition | 1000 concurrent requests, security probe, code change request, server crash |
| **Artifact** | What part of the system is affected | API gateway, database, authentication module, payment service |
| **Environment** | System state when stimulus arrives | Normal operation, peak load, degraded mode, startup, maintenance window |
| **Response** | How the system should respond | Process request, reject gracefully, alert operations team, failover to backup |
| **Measure** | How to verify the response | P99 < 200ms, zero data loss, alert within 5 minutes, RTO < 30 seconds |

### Example Scenarios

**Scenario 1: Performance under Load**

| Part | Value |
|------|-------|
| Source | 5,000 concurrent end users |
| Stimulus | Submit search queries during peak hours |
| Artifact | Search API service |
| Environment | Normal operation at peak load (Monday 9 AM) |
| Response | Return search results successfully |
| Measure | P95 latency < 500ms, P99 < 1s, zero errors |

**Scenario 2: Availability during Failure**

| Part | Value |
|------|-------|
| Source | AWS availability zone |
| Stimulus | Complete AZ failure (network partition) |
| Artifact | Entire application stack |
| Environment | Normal operation |
| Response | Failover to remaining AZs, continue serving traffic with no user-visible interruption |
| Measure | RTO < 30 seconds, RPO = 0 (zero data loss), availability stays above 99.95% |

**Scenario 3: Security Breach Attempt**

| Part | Value |
|------|-------|
| Source | External attacker |
| Stimulus | SQL injection attempt via public API endpoint |
| Artifact | API gateway and database layer |
| Environment | Normal operation |
| Response | Block the malicious input, log the attempt with full context, alert security team |
| Measure | Zero successful injections, alert within 60 seconds, full audit trail preserved |

**Scenario 4: Modifiability for New Feature**

| Part | Value |
|------|-------|
| Source | Product team |
| Stimulus | Request to add a new payment provider (Stripe to supplement existing PayPal) |
| Artifact | Payment service module |
| Environment | Normal development cycle |
| Response | Implement, test, and deploy new provider without modifying existing payment flows |
| Measure | Change requires fewer than 5 files modified, no regressions in existing payment tests, delivered in 1 sprint |

**Scenario 5: Deployability for Hotfix**

| Part | Value |
|------|-------|
| Source | On-call engineer |
| Stimulus | Critical bug discovered in production (data corruption on edge case) |
| Artifact | Order processing service |
| Environment | Production, business hours, active traffic |
| Response | Deploy hotfix to production with zero downtime |
| Measure | Time from fix committed to live in production < 30 minutes, zero failed requests during deployment, automatic rollback if error rate exceeds 1% |

---

## Pairwise Comparison Method

When multiple quality attributes compete, architects need a systematic way to prioritize. The pairwise comparison method forces explicit tradeoff decisions rather than treating everything as "important."

### Process

1. **List all relevant quality attributes** for the system (typically 5-8).
2. **Compare each pair:** For every combination of two QAs, ask the stakeholders: "If we had to choose between these two, which is more important for THIS system?" Record the winner.
3. **Count wins** for each quality attribute.
4. **Rank by win count.** Ties indicate equally important attributes.
5. **Top 3 drive architecture decisions.** These are the primary drivers that shape structural choices. The remaining attributes are constraints -- they must be satisfied to an acceptable degree but do not drive the architecture.

### Sample Pairwise Comparison Matrix

Context: E-commerce platform handling financial transactions.

| vs. | Avail | Perf | Secur | Maint | Scala | Deploy | **Wins** |
|-----|-------|------|-------|-------|-------|--------|----------|
| **Availability** | -- | Avail | Secur | Avail | Avail | Avail | **4** |
| **Performance** | Avail | -- | Secur | Perf | Scala | Perf | **2** |
| **Security** | Secur | Secur | -- | Secur | Secur | Secur | **5** |
| **Maintainability** | Avail | Perf | Secur | -- | Maint | Maint | **2** |
| **Scalability** | Avail | Scala | Secur | Maint | -- | Scala | **2** |
| **Deployability** | Avail | Perf | Secur | Maint | Scala | -- | **0** |

**Result ranking:**

| Rank | Quality Attribute | Wins | Role |
|------|-------------------|------|------|
| 1 | Security | 5 | **Primary driver** -- shapes trust boundaries, auth architecture, encryption strategy |
| 2 | Availability | 4 | **Primary driver** -- shapes redundancy, failover, data replication |
| 3 | Performance | 2 (tie) | **Secondary driver** -- shapes caching, data architecture |
| 3 | Maintainability | 2 (tie) | **Constraint** -- must meet acceptable threshold |
| 3 | Scalability | 2 (tie) | **Constraint** -- must meet acceptable threshold |
| 6 | Deployability | 0 | **Constraint** -- must meet acceptable threshold |

In this example, Security and Availability are the clear primary drivers. Architecture decisions should optimize for these two first. Performance, Maintainability, and Scalability are tied as secondary concerns. Deployability is a constraint -- it must not be terrible, but it does not drive major structural decisions.

### Tips for Effective Pairwise Comparison

- **Include the right stakeholders.** Business leaders care about availability and security. Developers care about maintainability and testability. Both perspectives matter.
- **Be specific about context.** "Security is more important than performance" is not universally true. It is true for a banking application. It may not be true for a real-time gaming server.
- **Revisit periodically.** Priorities change as the system matures. A startup may prioritize deployability and time-to-market. The same company at scale may prioritize availability and performance.
- **Document the rationale.** Record not just the ranking but why each decision was made. This context is invaluable when revisiting decisions later.
- **Accept that tradeoffs are permanent.** Architecture is the art of making the right tradeoffs. There is no architecture that optimizes all quality attributes simultaneously. Attempting to do so leads to analysis paralysis or mediocrity across the board.
