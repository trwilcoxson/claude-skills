# Elite Design Review Scorecard

A comprehensive 9-section design review checklist for evaluating software architecture readiness. Each item includes pass criteria, required evidence, and red flags. This scorecard is intended for use during formal architecture reviews, pre-production readiness gates, and ongoing design health assessments.

**Scoring:** Each item is rated PASS, PARTIAL, or FAIL. STOP-SHIP items that receive FAIL block deployment regardless of overall score.

---

## Section A: Purpose & Scope

Purpose and scope failures are the most expensive defects in software. A system built to solve the wrong problem cannot be rescued by good engineering. This section validates that the team knows exactly what they are building, for whom, and where the edges are.

### A1: Mission Statement Clarity

The system has a single-sentence purpose statement that any engineer can recite from memory.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A one-sentence mission statement exists in the project's top-level README or architecture document. It names the primary user, the core action, and the value delivered. Every team member can paraphrase it without consulting documentation. |
| **Evidence Required** | The mission statement in the repository root. Interview two engineers at random; both articulate the system's purpose consistently without contradicting each other or the written statement. |
| **Red Flags** | The mission statement is a paragraph or longer. It uses hedging language ("also," "and additionally," "as well as"). Different team members describe fundamentally different purposes. No written statement exists and the purpose lives only in someone's head. |

### A2: Non-Functional Requirements Documented

Explicit NFRs exist with measurable targets, not vague aspirations.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A dedicated NFR document or section specifies at minimum: availability target (e.g., 99.9%), latency targets (p50, p95, p99), throughput capacity, data retention period, and maximum acceptable data loss window (RPO). Each target includes a number and a unit. |
| **Evidence Required** | The NFR document with quantified targets. Traceability from each NFR to at least one architectural decision that supports it. Evidence that NFRs were reviewed with stakeholders (sign-off, meeting notes, or ticket approval). |
| **Red Flags** | NFRs say "fast" or "highly available" without numbers. Targets are copy-pasted from a template and do not reflect the actual system's constraints. No NFR document exists. Latency targets exist but nobody has measured current latency. |

### A3: Stakeholder Concerns Mapped

Every identified stakeholder's primary concern is explicitly addressed in the architecture.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A stakeholder map exists listing each stakeholder role (product owner, security team, operations, compliance, end users), their primary concern, and a specific architectural element that addresses it. Concerns are not generic; they reflect actual conversations with those stakeholders. |
| **Evidence Required** | Stakeholder concern matrix with at minimum four distinct stakeholder roles. For each concern, a pointer to the relevant ADR, design section, or implementation artifact. Meeting notes or communication records showing the concern was gathered from the stakeholder directly, not assumed. |
| **Red Flags** | Stakeholder list contains only "the business" as a single entry. Concerns are fabricated by the engineering team without stakeholder input. Security and compliance stakeholders are absent from the map. A stakeholder's concern is listed but no architectural response exists for it. |

### A4: Scope Boundaries Defined

The architecture document explicitly states what is out of scope, not just what is in scope.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | An explicit "Out of Scope" section lists at least five things the system will not do. Each exclusion includes a brief rationale. Adjacent systems that handle excluded responsibilities are named. The boundary between this system and those adjacent systems is described at the interface level. |
| **Evidence Required** | The out-of-scope section in the architecture document. Evidence that scope was discussed and agreed upon (ADR, meeting notes, or ticket). No active feature work that contradicts the stated scope boundaries. |
| **Red Flags** | No out-of-scope section exists. The system description uses unbounded language ("handles all," "supports any"). Feature requests that violate scope are being accepted without updating the scope document. The system is slowly absorbing responsibilities from adjacent systems with no explicit decision to do so. |

---

## Section B: Boundaries & Domain Model

Domain modeling errors propagate through every layer of the system. A misdrawn boundary creates coupling that no amount of refactoring at the code level can fully repair. This section ensures the domain is modeled with precision and that boundaries are enforced, not merely documented.

### B1: Bounded Contexts Identified

Clear domain boundaries exist with ubiquitous language defined per context.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Each bounded context has a name, a glossary of terms (ubiquitous language), and a clear boundary description. The same real-world concept that appears in multiple contexts has distinct names or explicit mapping between contexts. Engineers working in one context do not need to understand the internals of another. |
| **Evidence Required** | Context boundary diagram showing each bounded context, its owned entities, and its public interface. A glossary per context with at least five domain terms defined. Code organization that reflects context boundaries (separate modules, packages, or services). |
| **Red Flags** | The same database table is written to by multiple bounded contexts. Domain terms are used inconsistently across the codebase ("user" means different things in different modules). No explicit boundaries exist and the codebase is organized by technical layer (controllers, services, repositories) rather than by domain. |

### B2: Invariants Enforced in Code

Business rules are validated at the domain layer, not scattered across controllers and scripts.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Domain invariants (e.g., "an order must have at least one line item," "account balance cannot go negative") are enforced in domain entities or value objects. Invariant violations raise domain-specific exceptions. No business rule enforcement exists only in the UI or API validation layer. |
| **Evidence Required** | Code samples showing invariant checks in domain objects. Unit tests that verify invariant violations produce the expected errors. Absence of business rule checks in controller or handler code that do not also exist in the domain layer. |
| **Red Flags** | Business rules are enforced only by database constraints with no domain-layer validation. Invariants are checked in API middleware but not in the domain. Test suite has no tests for invariant violations. A bug report exists where an invalid state was persisted because a code path bypassed validation. |

### B3: Trust Boundaries Defined

Explicit security zones exist with documented policies for crossing them.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A trust boundary diagram identifies at least three zones (e.g., public internet, DMZ, internal network, data stores). Every crossing between zones has a documented policy specifying authentication method, encryption requirement, and data sanitization rule. No implicit trust exists between zones. |
| **Evidence Required** | Trust boundary diagram with zone labels and crossing policies. Network configuration or infrastructure-as-code that enforces zone separation. Evidence that cross-zone calls use the documented authentication and encryption mechanisms. |
| **Red Flags** | Internal services communicate without authentication because they are "inside the firewall." No trust boundary diagram exists. A service in the DMZ has direct database access. Trust decisions are made based on IP address alone. |

### B4: Context Map Documented

Relationships between bounded contexts are explicitly categorized and managed.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A context map diagram shows every bounded context and the relationship type between each pair: Anti-Corruption Layer (ACL), Conformist, Shared Kernel, Open Host Service, Published Language, Customer-Supplier, or Partnership. Each relationship type has an associated integration strategy (API calls, events, shared library). The team that owns each context is identified. |
| **Evidence Required** | Context map diagram with relationship type labels. For each ACL, code showing the translation layer. For each Shared Kernel, documentation of the change coordination process. Team ownership assignments for every context. |
| **Red Flags** | All context relationships are unlabeled arrows on a diagram. An ACL relationship has no translation code and directly exposes another context's data model. A Shared Kernel exists but has no process for coordinating changes. The context map has not been updated in more than six months. |

### B5: Module Coupling Metrics

Afferent and efferent coupling are measured and within acceptable limits.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Coupling metrics are computed for each module or package. Efferent coupling (Ce) and afferent coupling (Ca) are tracked. The instability metric (I = Ce / (Ca + Ce)) is reviewed. Stable abstractions have high Ca and low Ce. Volatile implementations have high Ce and low Ca. No module sits in the "zone of pain" (highly stable and highly concrete) or the "zone of uselessness" (highly abstract and highly unstable). |
| **Evidence Required** | Coupling analysis output from a static analysis tool (jdepend, NDepend, Python dependency analyzers, or equivalent). A review of any module with instability metric outside the 0.3-0.7 range for concrete modules. CI integration that tracks coupling trends over time. |
| **Red Flags** | No coupling analysis has ever been run. A single module depends on more than ten other modules. Circular dependencies exist between modules. Coupling metrics are measured but never reviewed or acted upon. |

---

## Section C: Contracts & Interfaces

Interfaces are the load-bearing walls of a distributed system. A poorly designed contract creates invisible dependencies that surface as production incidents. This section validates that every interface is versioned, tested, consistent, and safe to retry.

### C1: API Versioning Strategy

All endpoints are versioned with a documented deprecation policy.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every public API endpoint includes a version identifier (URL path, header, or query parameter). A deprecation policy exists stating minimum notice period (e.g., 90 days), communication channel, and migration support offered. At least one prior deprecation has been executed following the policy, or a dry-run has been conducted. |
| **Evidence Required** | API documentation showing version identifiers on all endpoints. The written deprecation policy. Deprecation notices or sunset headers in API responses for any deprecated endpoints. Client migration guides for version transitions. |
| **Red Flags** | Endpoints have no version identifier. Breaking changes are deployed without notice. The deprecation policy exists but has never been followed. Multiple incompatible versions are maintained indefinitely with no sunset plan. |

### C2: Error Model Consistency

Standardized error responses exist across all APIs.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A single error response schema is used across all API endpoints. The schema includes at minimum: error code (machine-readable), message (human-readable), correlation ID, and timestamp. HTTP status codes are used correctly (4xx for client errors, 5xx for server errors). Error codes are documented in a central registry. |
| **Evidence Required** | The error response schema definition. Samples from at least three different endpoints showing consistent error formatting. The error code registry. Automated tests verifying error response structure. |
| **Red Flags** | Different endpoints return errors in different formats. Stack traces are exposed in production error responses. HTTP 200 is returned with an error payload in the body. Error messages contain internal implementation details or database column names. |

### C3: Event Schema Registry

All events have schemas, versions, and compatibility rules.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every event published to a message bus or event stream has a registered schema (Avro, Protobuf, JSON Schema, or equivalent). Schemas are versioned. Compatibility rules are enforced (backward, forward, or full compatibility). Schema validation occurs at both publish and consume time. |
| **Evidence Required** | The schema registry with registered event schemas. Schema compatibility configuration. CI pipeline step that validates schema changes against compatibility rules. Evidence that a schema change was rejected or modified due to compatibility check failure. |
| **Red Flags** | Events are published as untyped JSON with no schema. Schema changes are deployed without compatibility checks. Consumers parse events with try-catch blocks and best-effort field extraction. The schema registry exists but is not enforced at runtime. |

### C4: Contract Testing in Place

Consumer-driven contract tests verify interface compatibility.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Consumer-driven contract tests (Pact, Spring Cloud Contract, or equivalent) exist for all critical service-to-service interfaces. Contracts are generated by consumers and verified by providers. Contract tests run in CI for both consumer and provider pipelines. Breaking contract changes block provider deployment. |
| **Evidence Required** | Contract test files in the repository. CI pipeline configuration showing contract verification steps. A Pact broker or equivalent contract sharing mechanism. Evidence that a provider build was blocked by a contract test failure. |
| **Red Flags** | No contract tests exist and integration is verified only by end-to-end tests. Contract tests exist but are not run in CI. Contracts are written by the provider team rather than consumers. Contract test failures are ignored or tests are skipped. |

### C5: Idempotency Keys

All mutating operations support safe retries via idempotency keys.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every mutating API endpoint (POST, PUT, PATCH, DELETE) accepts an idempotency key. Duplicate requests with the same key return the original response without re-executing the operation. Idempotency keys have a documented TTL. The idempotency implementation handles concurrent duplicate requests (not just sequential ones). |
| **Evidence Required** | API documentation showing idempotency key parameter on all mutating endpoints. Integration tests demonstrating that duplicate requests produce identical responses and single side effects. Implementation code showing idempotency key storage and lookup. Load test results showing correct behavior under concurrent duplicate requests. |
| **Red Flags** | Mutating endpoints have no idempotency support. Idempotency is implemented only for payment endpoints but not for other state-changing operations. The idempotency key TTL is not documented. Concurrent duplicate requests cause race conditions or duplicate side effects. |

---

## Section D: Data Architecture

Data outlives code. A service can be rewritten in a weekend; a data migration takes months and carries risk at every step. This section validates that data ownership, access patterns, consistency models, and recovery procedures are deliberate choices, not accidents.

### D1: Query Patterns Supported

Read models match access patterns with no N+1 queries in critical paths.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every primary query pattern has been identified and documented. Read models (views, materialized views, denormalized tables, or search indices) exist for the top access patterns. Query execution plans for critical paths show index usage and no full table scans. No N+1 query patterns exist in any code path that serves user requests. |
| **Evidence Required** | Documented query patterns with expected volume. Query execution plans (EXPLAIN output) for the top five queries by volume. ORM query logs or application profiler output showing no N+1 patterns. Read model definitions for high-volume access patterns. |
| **Red Flags** | The database schema was designed entity-first without considering query patterns. No query profiling has been done. ORM lazy loading is enabled globally with no explicit eager loading for critical paths. A single query pattern requires joining more than five tables. |

### D2: Consistency Model Explicit

CAP/PACELC choices are documented per data store.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Each data store has a documented consistency model. For distributed data stores, the CAP or PACELC trade-off is stated. Eventual consistency windows are quantified where applicable (e.g., "replication lag under 500ms at p99"). Application code handles stale reads appropriately where eventual consistency is chosen. |
| **Evidence Required** | Consistency model documentation per data store. For eventually consistent stores, measured replication lag metrics. Application code that handles stale reads (retry logic, read-your-writes patterns, or UI indicators). ADR explaining why each consistency model was chosen. |
| **Red Flags** | The team cannot articulate the consistency model of their primary data store. Strong consistency is assumed but the data store is configured for eventual consistency. No measurement of replication lag exists. Application code treats all reads as strongly consistent regardless of the underlying store. |

### D3: Schema Migration Safety

All database migrations are backward-compatible using expand-contract patterns.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Database migrations follow the expand-contract pattern: new columns/tables are added first (expand), application code is updated to use both old and new schemas, then old columns/tables are removed (contract). No migration deletes or renames a column in a single step. Migrations are tested against a copy of production-scale data. Migration rollback scripts exist for every forward migration. |
| **Evidence Required** | Migration files showing expand-contract pattern. Evidence that migrations have been tested against production-scale data (test environment with realistic volume). Rollback scripts for recent migrations. CI pipeline step that runs migrations forward and backward. |
| **Red Flags** | Migrations rename or delete columns in a single deployment. No rollback scripts exist. Migrations are tested only against an empty database. A migration has caused a production outage in the past six months. Migrations run without a transaction or with a table lock on a high-traffic table. |

### D4: Data Ownership Clear

Each entity has exactly one authoritative source.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A data ownership map exists showing every major entity, its authoritative source (the system of record), and which other systems hold copies. Copies are explicitly labeled as caches, projections, or replicas. Write access to an entity is restricted to its owning service. Other services read via API, event subscription, or read replica and never write directly. |
| **Evidence Required** | Data ownership map or diagram. Database access controls showing write permissions limited to the owning service. No direct cross-service database queries (verified by network policy or code review). Event-driven synchronization for data copies with documented staleness guarantees. |
| **Red Flags** | Multiple services write to the same database table. No ownership map exists and ownership is determined by "whoever wrote the code." A "shared database" pattern is used intentionally but without access controls. Data conflicts are resolved by "last write wins" with no conflict detection. |

### D5: Backup and Recovery Tested

RPO/RTO are defined, and recovery procedures are tested in practice, not just documented.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | RPO (Recovery Point Objective) and RTO (Recovery Time Objective) are defined per data store. Backups are automated and monitored. A full recovery drill has been executed within the last quarter. Recovery time during the drill met the RTO target. Backup integrity is verified automatically (checksums, test restores). |
| **Evidence Required** | RPO/RTO targets in the NFR document. Backup schedule and monitoring dashboard. Recovery drill report from the last quarter including actual recovery time. Automated backup verification logs. Documented recovery procedure (runbook) that was followed during the drill. |
| **Red Flags** | Backups exist but have never been restored. RPO/RTO targets are not defined. Backup monitoring has no alerts for failure. The last recovery drill was more than six months ago. Recovery procedure exists only as tribal knowledge. Backup retention period is shorter than the compliance requirement. |

---

## Section E: Reliability & Resilience

Production systems fail. The question is not whether a dependency will become unavailable, but whether the system will handle it without waking someone up at 3 AM. This section validates that failure is treated as a first-class design concern.

### E1: Dependency Failure Policies

Every external call has a timeout, retry policy, and fallback behavior.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every outbound HTTP call, database query, message publish, and cache operation has an explicit timeout. Retry policies specify max retries, backoff strategy (exponential with jitter), and retry conditions (which errors are retryable). Fallback behavior is defined (cached response, default value, degraded response, or fast failure with clear error). |
| **Evidence Required** | Configuration or code showing timeouts on all external calls. Retry policy configuration with backoff parameters. Fallback implementation code. Integration tests that simulate dependency failure and verify fallback behavior. Dependency failure runbook entries. |
| **Red Flags** | Default HTTP client timeouts (often 30-60 seconds or infinite) are used. Retries use fixed intervals with no jitter, creating thundering herd risk. No fallback behavior is defined and dependency failure causes the entire request to fail with a 500 error. Timeout values have never been tuned based on actual dependency latency. |

### E2: Idempotency Guaranteed

All side-effecting operations are safe to retry without duplication.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every operation that produces a side effect (database write, external API call, message publish, email send) is idempotent. Idempotency is implemented at the application level (not relying on infrastructure alone). Deduplication mechanisms handle both sequential and concurrent duplicate executions. Message consumers are idempotent and handle redelivery gracefully. |
| **Evidence Required** | Idempotency implementation for each side-effecting operation. Tests demonstrating duplicate execution safety. Message consumer code showing deduplication logic. Documentation of the idempotency strategy (idempotency keys, natural idempotency, or deduplication tables). |
| **Red Flags** | The team says "we just don't retry" instead of implementing idempotency. Idempotency relies on "at-most-once" delivery guarantees from the message broker. Database upserts are used without considering all columns that might change. A duplicate message caused a production issue (double charge, double notification) in the past year. |

### E3: Backpressure Handling

The system degrades gracefully under load via rate limiting, load shedding, or queue-based buffering.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Rate limiting is implemented at the API gateway or application level with documented limits per client or endpoint. Load shedding drops low-priority requests when the system approaches capacity. Queue-based workloads have bounded queue sizes with dead-letter handling. Backpressure signals propagate upstream (HTTP 429 with Retry-After header, or equivalent). |
| **Evidence Required** | Rate limiting configuration with documented limits. Load test results showing graceful degradation under 2x expected peak load. Queue configuration showing max sizes and dead-letter policies. HTTP 429 responses with Retry-After headers in API documentation. Monitoring dashboards showing rate limiting and load shedding metrics. |
| **Red Flags** | No rate limiting exists. The system accepts all requests regardless of load and relies on infrastructure autoscaling alone. Unbounded queues exist that can grow until memory is exhausted. Load testing has never been performed at above expected peak volume. The system returns 500 errors under load instead of 429. |

### E4: Circuit Breakers Configured

Cascading failure prevention exists for all external dependencies.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Circuit breakers are configured for every external dependency (other services, databases, caches, third-party APIs). Breaker thresholds are tuned based on observed error rates, not defaults. The half-open state probes the dependency with limited traffic before fully closing. Circuit breaker state transitions are logged and alerted on. |
| **Evidence Required** | Circuit breaker configuration for each external dependency. Threshold tuning documentation referencing observed error rates. Circuit breaker state transition logs or dashboard. Integration tests that verify circuit breaker behavior (open on failure, close on recovery). Alert configuration for circuit breaker open events. |
| **Red Flags** | No circuit breakers exist and a single dependency failure cascades to the entire system. Circuit breaker thresholds are left at library defaults. Circuit breaker state changes are not logged or monitored. The circuit breaker library is imported but not configured for most dependencies. |

### E5: Graceful Shutdown

In-flight requests are completed and connections are drained during shutdown.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | The application handles SIGTERM by stopping acceptance of new requests, completing in-flight requests (with a bounded timeout), closing database connections and message consumers, and then exiting. Kubernetes readiness probes (or equivalent) are removed before shutdown begins to prevent new traffic routing. The graceful shutdown timeout is shorter than the infrastructure kill timeout (e.g., 25 seconds vs. 30 seconds SIGKILL). |
| **Evidence Required** | Shutdown handler code showing the drain sequence. Configuration showing readiness probe removal timing. Infrastructure configuration showing SIGKILL timeout. Load test during rolling deployment showing zero dropped requests. |
| **Red Flags** | The application exits immediately on SIGTERM. No readiness probe exists or it is not removed during shutdown. In-flight requests receive connection reset errors during deployment. The graceful shutdown timeout exceeds the infrastructure kill timeout, causing forced termination. Long-running requests (file uploads, report generation) have no special handling during shutdown. |

### E6: Chaos Testing Planned

Failure injection experiments are defined and scheduled.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A chaos testing plan exists with at least five experiments covering: dependency failure, network partition, resource exhaustion (CPU, memory, disk), clock skew, and zone/region failure. Experiments have hypotheses, blast radius limits, and rollback procedures. At least one chaos experiment has been executed in a production or production-like environment. Results are documented and linked to remediation work. |
| **Evidence Required** | Chaos testing plan document with experiment definitions. Results from at least one executed experiment. Remediation tickets created from experiment findings. Tooling setup (Chaos Monkey, Litmus, Gremlin, or custom). Schedule for recurring experiments. |
| **Red Flags** | No chaos testing has been considered. The team says "we'll do it after launch." Chaos experiments are defined but have never been executed. Experiments were run once but findings were not acted upon. Chaos testing is done only in development environments that do not reflect production topology. |

---

## Section F: Security & Privacy

Security is not a feature; it is a constraint that applies to every feature. Items marked **STOP-SHIP** represent vulnerabilities so severe that they block deployment to production regardless of all other scores.

### F1: Authentication Enforced -- STOP-SHIP

All endpoints require valid identity verification.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every API endpoint (except explicit public endpoints like health checks) requires authentication. Authentication uses industry-standard protocols (OAuth 2.0, OIDC, mutual TLS). Token validation occurs on every request, not cached indefinitely. Service-to-service calls use machine identity (service accounts, mTLS), not shared secrets. |
| **Evidence Required** | API gateway or middleware configuration showing authentication enforcement. List of explicitly unauthenticated endpoints with justification. Security scan results showing no unauthenticated endpoints. Authentication integration tests. |
| **Red Flags** | Any non-public endpoint is accessible without authentication. Authentication is enforced by convention ("all developers add the auth middleware") rather than by default. JWTs are not validated for expiration. A shared API key is used across multiple services with no rotation. **Any unauthenticated mutating endpoint is an automatic STOP-SHIP.** |

### F2: Authorization Granular

RBAC or ABAC enforces principle of least privilege.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Authorization is enforced at the API layer and at the data layer. Roles are defined with minimum necessary permissions. Resource-level authorization prevents users from accessing other users' data (no IDOR vulnerabilities). Admin operations require elevated authentication (step-up auth or separate admin credentials). |
| **Evidence Required** | Role definitions with permission matrices. Authorization middleware or policy engine configuration. Tests for horizontal privilege escalation (user A cannot access user B's resources). Tests for vertical privilege escalation (regular user cannot perform admin operations). |
| **Red Flags** | Authorization checks exist only in the UI. A single "admin" role exists with no granularity. User ID is taken from the URL path without verifying it matches the authenticated identity. Authorization decisions are cached without TTL, allowing stale permissions. |

### F3: Secrets Management -- STOP-SHIP

No hardcoded secrets exist in code, and rotation policies are in place.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All secrets (API keys, database passwords, signing keys, certificates) are stored in a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager, or equivalent). No secrets exist in source code, environment files committed to git, or CI/CD configuration. Secrets have a defined rotation schedule. Rotation can be performed without downtime. |
| **Evidence Required** | Secrets manager configuration. Git history scan showing no committed secrets (truffleHog, git-secrets, or equivalent scan results). Rotation schedule documentation. Evidence of at least one successful rotation performed without downtime. Pre-commit hook or CI step that blocks secret commits. |
| **Red Flags** | Secrets found in source code or git history. Secrets are passed as environment variables in CI/CD configuration visible in logs. No rotation has ever been performed. Rotation requires system downtime. A `.env` file exists in the repository (even if gitignored, verify it was never committed). **Any secret in source code or git history is an automatic STOP-SHIP.** |

### F4: Input Validation -- STOP-SHIP

All external input is validated and sanitized.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every external input (API parameters, headers, file uploads, webhook payloads) is validated against a strict schema. SQL queries use parameterized statements exclusively. HTML output is escaped to prevent XSS. File uploads are validated for type, size, and content (not just extension). Input validation occurs at the application boundary before any processing. |
| **Evidence Required** | Input validation schemas or middleware configuration. Code review or static analysis confirming parameterized queries (no string concatenation in SQL). XSS prevention configuration (Content-Security-Policy headers, output encoding). SAST tool results showing no injection vulnerabilities. Penetration test results or OWASP ZAP scan. |
| **Red Flags** | String concatenation used in SQL queries. User input reflected in HTML responses without encoding. File uploads accepted without content validation. Input validation exists only on the client side. Error messages reveal database structure or internal paths. **Any SQL injection or command injection vulnerability is an automatic STOP-SHIP.** |

### F5: Audit Trail Complete

An immutable log records who did what, when, and from where.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All state-changing operations are logged with: actor identity, action performed, resource affected, timestamp, source IP or client identifier, and result (success or failure). Audit logs are stored separately from application logs. Audit logs are immutable (append-only storage, write-once bucket, or equivalent). Retention period meets compliance requirements. |
| **Evidence Required** | Audit log schema showing required fields. Sample audit log entries for create, update, and delete operations. Storage configuration showing immutability (S3 Object Lock, Cloud Storage retention policy, or equivalent). Retention policy documentation. Evidence that audit logs are not modifiable by application service accounts. |
| **Red Flags** | Audit logging covers only authentication events, not data modifications. Audit logs are stored in the same database as application data and modifiable by the application. No retention policy exists. Failed operations are not logged. Audit log entries lack actor identity or source information. |

### F6: Data Encryption

Data is encrypted at rest (AES-256) and in transit (TLS 1.3).

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All data stores use encryption at rest with AES-256 or equivalent. All network communication uses TLS 1.2 minimum, TLS 1.3 preferred. Certificate management is automated (auto-renewal). Internal service-to-service communication is encrypted. Encryption keys are managed by a KMS, not application code. |
| **Evidence Required** | Data store encryption configuration. TLS configuration showing minimum version and cipher suites. Certificate management automation (cert-manager, ACM, or equivalent). Network policy or service mesh configuration showing encrypted internal traffic. KMS key policy documentation. |
| **Red Flags** | Any data store has encryption at rest disabled. TLS 1.0 or 1.1 is still supported. Self-signed certificates are used in production without a private CA. Encryption keys are stored alongside the encrypted data. Internal communication uses plaintext HTTP. |

### F7: Dependency Security

No known critical CVEs exist in dependencies, and an SBOM is generated.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Dependency scanning runs in CI on every build (Snyk, Dependabot, Trivy, or equivalent). No critical or high-severity CVEs exist in production dependencies. An SBOM (Software Bill of Materials) is generated for each release. Dependency update process is documented and followed. Base container images are scanned and updated regularly. |
| **Evidence Required** | CI pipeline configuration showing dependency scanning step. Most recent scan results showing zero critical CVEs. SBOM artifact for the latest release. Dependency update tickets or PRs from the last 30 days. Container image scan results. |
| **Red Flags** | No dependency scanning is configured. Critical CVEs exist in production dependencies with no remediation timeline. Dependencies have not been updated in more than 90 days. The SBOM has never been generated. Base container images are pinned to old versions with known vulnerabilities. |

### F8: PII Handling

Data classification, retention policies, and right-to-deletion mechanisms exist.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All data fields are classified by sensitivity (public, internal, confidential, PII). PII fields are identified in the data model. Retention policies are defined per data classification. A deletion mechanism exists that removes a user's PII across all data stores within the required timeframe. PII is not logged, cached indefinitely, or replicated to analytics systems without anonymization. |
| **Evidence Required** | Data classification matrix. PII field inventory. Retention policy documentation. Deletion mechanism code or procedure. Evidence of a successful deletion execution (test or actual). Log and cache configuration showing PII exclusion or masking. |
| **Red Flags** | No data classification exists. PII appears in application logs. No deletion mechanism exists. Deletion removes data from the primary store but leaves copies in backups, caches, or analytics systems. Retention policies are documented but not enforced. Marketing or analytics systems receive raw PII without anonymization. |

---

## Section G: Observability & Operability

A system that cannot be observed cannot be operated. Observability is not logging more; it is asking arbitrary questions of the system without deploying new code. This section validates that the system is ready to be run by humans who did not build it.

### G1: SLOs Defined

Availability, latency, and error rate targets exist with error budgets.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | At least three SLOs are defined covering availability, latency (p99), and error rate. Each SLO has a measurement window (rolling 30 days). Error budgets are calculated and tracked. Error budget consumption rate drives development priorities (when budget is depleted, reliability work takes precedence over features). |
| **Evidence Required** | SLO definitions with targets and measurement windows. Error budget dashboard showing current budget consumption. Evidence that error budget depletion has influenced prioritization decisions. SLO measurement implementation (SLI definitions, data sources, calculation method). |
| **Red Flags** | No SLOs are defined. SLOs exist but are not measured. SLOs are set at 100% (unrealistic and not useful for error budgets). Error budgets are calculated but never referenced in planning. SLOs were copied from a template without consideration of actual system requirements. |

### G2: Structured Logging

JSON logs include correlation IDs, appropriate log levels, and PII scrubbing.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All logs are structured (JSON). Every log entry includes: timestamp, log level, service name, correlation ID (trace ID), and message. Log levels are used correctly (ERROR for failures requiring attention, WARN for degraded behavior, INFO for significant events, DEBUG for troubleshooting). PII is excluded or masked in all log entries. Log volume is manageable (not logging entire request/response bodies at INFO level). |
| **Evidence Required** | Log output samples showing JSON structure with required fields. Logging configuration showing level settings. PII scrubbing configuration or middleware. Log volume metrics showing daily ingestion rate. Evidence that correlation IDs propagate across service boundaries. |
| **Red Flags** | Logs are unstructured text. No correlation ID is present, making cross-service tracing impossible via logs. PII (emails, names, addresses) appears in logs. Every request/response body is logged at INFO level, creating excessive volume and cost. Log levels are inconsistent (INFO used for errors, DEBUG left on in production). |

### G3: Distributed Tracing

OpenTelemetry spans with context propagation exist across all services.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | OpenTelemetry (or equivalent) is instrumented across all services. Trace context propagates through HTTP headers, message headers, and async job metadata. Critical business operations have custom spans with relevant attributes. Traces are exported to a trace backend (Jaeger, Zipkin, Tempo, or cloud provider). Sampling strategy is documented and appropriate for traffic volume. |
| **Evidence Required** | OpenTelemetry SDK configuration in each service. Trace output showing spans across multiple services for a single request. Custom span definitions for critical operations. Trace backend dashboard. Sampling configuration documentation. |
| **Red Flags** | No distributed tracing exists. Tracing is configured but context propagation is broken between services. All traces are sampled (100%), creating excessive storage costs. Traces exist but nobody knows how to query them. Async operations (queue consumers, scheduled jobs) are not traced. |

### G4: Metrics Dashboards

RED metrics for services and USE metrics for infrastructure are visualized.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Every service has a dashboard showing RED metrics: Rate (requests per second), Errors (error rate), and Duration (latency histogram). Infrastructure dashboards show USE metrics: Utilization, Saturation, and Errors for CPU, memory, disk, and network. Business metrics are tracked (conversion rate, transaction volume, or domain-specific KPIs). Dashboards load in under 5 seconds and cover at least 30 days of history. |
| **Evidence Required** | Service dashboard screenshots or links showing RED metrics. Infrastructure dashboard showing USE metrics. Business metrics dashboard. Dashboard load time evidence. Documentation of dashboard ownership (who updates them). |
| **Red Flags** | No dashboards exist. Dashboards exist but show only infrastructure metrics, not application metrics. Dashboards are outdated and show metrics for deprecated services. Nobody on the team can explain what the dashboards show. Business metrics are not tracked in the monitoring system. |

### G5: Alerting Configured

Burn-rate alerts on SLO violations replace threshold-based alerting.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Alerts are based on SLO error budget burn rate, not static thresholds. Multi-window burn-rate alerts catch both fast burns (5-minute window) and slow burns (1-hour window). Each alert has a severity, notification channel, and link to a runbook. Alert fatigue is managed: fewer than 5 actionable alerts per on-call shift on average. |
| **Evidence Required** | Alert definitions showing burn-rate calculations. Alert routing configuration (PagerDuty, OpsGenie, or equivalent). Alert-to-runbook mapping. Alert frequency metrics from the last 30 days showing actionable alert count per shift. Evidence that noisy alerts have been tuned or removed. |
| **Red Flags** | Alerts are based on static thresholds (CPU > 80%) rather than error budget impact. More than 20 alerts fire per on-call shift. Alerts have no runbook links. Alert fatigue has caused the team to ignore alerts. Critical alerts go to a Slack channel that nobody monitors outside business hours. |

### G6: Runbooks Exist

Documented procedures cover the top 10 operational scenarios.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Runbooks exist for at least the top 10 operational scenarios: deployment, rollback, dependency failure, database failure, certificate renewal, secret rotation, scaling, data recovery, incident response, and security breach. Each runbook includes: symptoms, diagnosis steps, remediation steps, escalation path, and verification steps. Runbooks are reviewed and updated quarterly. |
| **Evidence Required** | Runbook documents or wiki pages covering the top 10 scenarios. Evidence of runbook usage during a real incident (incident report referencing the runbook). Last-reviewed date on each runbook within the last quarter. Runbook testing results (tabletop exercise or dry-run). |
| **Red Flags** | No runbooks exist. Runbooks exist but were written at launch and never updated. Runbooks contain outdated commands or reference deprecated tools. Operational procedures live only in one engineer's head. Runbooks were not consulted during recent incidents. |

### G7: On-Call Readiness

Escalation paths, contact information, and severity definitions are documented and tested.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | An on-call rotation exists with at least two engineers per rotation. Escalation paths are documented: primary on-call, secondary on-call, engineering manager, VP of Engineering. Severity levels are defined (SEV1 through SEV4) with response time expectations for each. On-call engineers have access to all production systems, runbooks, and communication channels. A shadow on-call program exists for onboarding new on-call engineers. |
| **Evidence Required** | On-call rotation schedule. Escalation path documentation. Severity level definitions with response time SLAs. Evidence that on-call engineers have verified production access. Shadow on-call program documentation or records. |
| **Red Flags** | No on-call rotation exists. A single engineer handles all production issues. Escalation path is unclear or undocumented. On-call engineers lack production access and must request it during an incident. No severity definitions exist, so every issue is treated as an emergency. On-call handoff includes no context about ongoing issues. |

---

## Section H: Testing & Delivery

Shipping is not the end of the engineering process; it is the beginning of the feedback loop. A system that cannot be deployed safely and frequently cannot be improved. This section validates that the delivery pipeline is a reliable machine, not a manual ceremony.

### H1: Test Pyramid Balanced -- STOP-SHIP

Unit tests outnumber integration tests, which outnumber end-to-end tests.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | The test suite follows the test pyramid: the majority of tests are unit tests, a smaller number are integration tests, and the fewest are end-to-end tests. Unit test coverage exceeds 70% on business logic. Integration tests cover all external boundaries (database, APIs, message queues). End-to-end tests cover critical user journeys only. Test execution time for the full suite is under 15 minutes. |
| **Evidence Required** | Test count by category (unit, integration, e2e). Code coverage report for business logic modules. CI pipeline showing test execution times. Evidence that the test suite catches real bugs (recent PRs where tests failed on real defects). |
| **Red Flags** | No automated tests exist. The test pyramid is inverted (more e2e tests than unit tests). Test coverage is below 30%. Tests take more than 30 minutes to run, causing developers to skip them. Tests are flaky and frequently ignored. The test suite has not caught a real bug in the last month. **No automated tests at all is an automatic STOP-SHIP.** |

### H2: CI Pipeline Green

All checks pass and no tests are skipped.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | The CI pipeline runs on every PR and includes: compilation/build, linting, unit tests, integration tests, security scanning, and contract tests. All checks pass on the main branch. No tests are skipped or marked as expected failures without a linked tracking ticket. Pipeline execution time is under 15 minutes. Flaky test rate is below 1%. |
| **Evidence Required** | CI pipeline configuration showing all steps. Main branch build status (green). List of any skipped tests with linked tickets for re-enablement. Pipeline execution time metrics. Flaky test tracking dashboard or report. |
| **Red Flags** | The CI pipeline is red on the main branch. Tests are skipped without tracking tickets. The pipeline takes more than 30 minutes. More than 5% of test runs fail due to flakiness. Security scanning is not part of the pipeline. Developers routinely merge with failing checks by using admin override. |

### H3: Deployment Automated

One-command deployment exists with rollback capability.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Deployment to any environment requires a single command or a single button click. Deployment includes automated smoke tests that run post-deploy. Rollback to the previous version requires a single command and completes in under 5 minutes. Deployment does not require SSH access to production servers. The deployment process is documented and any engineer on the team can perform it. |
| **Evidence Required** | Deployment pipeline configuration. Deployment execution logs showing a recent successful deployment. Rollback procedure documentation and evidence of a recent rollback (drill or real). Post-deployment smoke test configuration. Deployment frequency metrics (at least weekly for active services). |
| **Red Flags** | Deployment requires manual steps (SSH, file copying, manual configuration changes). Rollback requires restoring a database backup. Only one or two engineers know how to deploy. Deployments happen less than monthly for an actively developed service. Post-deployment verification is manual ("click around and see if it works"). |

### H4: Feature Flags Operational

Progressive rollout capability exists for risky changes.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A feature flag system is in place (LaunchDarkly, Unleash, Flipt, or custom). All risky changes are deployed behind feature flags. Flags support percentage-based rollout and user segment targeting. Flag state changes are audited. Stale flags are cleaned up on a defined schedule (no flags older than 90 days without review). |
| **Evidence Required** | Feature flag system configuration. Examples of recent features deployed behind flags. Percentage-based rollout evidence. Flag audit log. Flag cleanup process documentation and evidence of recent cleanup. |
| **Red Flags** | No feature flag system exists. Feature flags exist but are never used for progressive rollout. Hundreds of stale flags exist with no cleanup process. Flag evaluation adds significant latency. Flag state is stored in application configuration files rather than a dynamic system. |

### H5: Database Migration Tested

Migrations run forward and backward successfully in a production-like environment.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All database migrations are tested in a staging environment with production-like data volume. Forward and backward migrations are both tested. Migration execution time is measured and acceptable for production (no table locks exceeding the maintenance window). Migrations are run as a separate deployment step, not embedded in application startup. |
| **Evidence Required** | Staging environment with production-scale data. Migration test results showing forward and backward execution. Migration execution time measurements. Deployment pipeline showing migration as a separate step. Evidence that a migration rollback has been successfully tested within the last quarter. |
| **Red Flags** | Migrations are tested only against an empty database. Backward migrations do not exist ("we'll just fix it forward"). Migrations run during application startup and block health checks. No staging environment exists with realistic data volume. A migration has caused downtime in the last six months. |

### H6: Performance Baseline

Load tests establish normal operating parameters.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Load tests simulate expected peak traffic (at minimum 2x normal peak). Performance baselines are established for latency (p50, p95, p99), throughput, and error rate. Load tests run in CI or on a regular schedule (at least monthly). Performance regression detection compares current results to baselines. |
| **Evidence Required** | Load test scripts and configuration. Baseline performance metrics document. Recent load test results with comparison to baselines. CI integration or scheduling configuration. Evidence that a performance regression was detected and addressed. |
| **Red Flags** | No load testing has been performed. Load tests were run once before launch and never again. Load test environment does not match production topology. Performance baselines do not exist, so there is no way to detect regression. Load tests use unrealistic traffic patterns (uniform distribution instead of realistic bursts). |

---

## Section I: AI/Agent-Specific (Conditional)

**This section applies only if the system includes AI, LLM, or agent components.** If no AI components exist, mark this section as N/A and exclude it from scoring.

AI systems introduce a category of risk that traditional software does not face: non-deterministic behavior, unbounded cost, data leakage through model APIs, and actions taken without human oversight. This section validates that these risks are managed.

### I1: Tool Safety Boundaries

Agent actions are bounded with no unrestricted system access.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Agent tools (functions the LLM can call) have explicitly defined permissions. No tool grants unrestricted filesystem, network, or database access. Tool execution is sandboxed (containers, restricted IAM roles, or allowlisted operations). Tool call rate limiting prevents runaway execution. All tool calls are logged with input parameters and results. |
| **Evidence Required** | Tool permission definitions. Sandbox configuration or IAM role policies. Rate limiting configuration. Tool call audit logs. Tests demonstrating that out-of-bounds tool calls are rejected. |
| **Red Flags** | An agent has root/admin access to production systems. Tools accept arbitrary SQL or shell commands. No rate limiting exists on tool calls. Tool calls are not logged. A tool can send emails, create accounts, or delete data without human approval. |

### I2: Eval Harness in Place

Automated evaluation of LLM outputs against benchmarks runs regularly.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | An evaluation harness tests LLM outputs against a curated dataset of expected behaviors. Evaluations run in CI on every prompt or model change. Metrics include accuracy, relevance, safety (harmful content detection), and format compliance. Evaluation results are tracked over time to detect regression. Minimum quality thresholds gate deployment. |
| **Evidence Required** | Evaluation dataset with at least 50 test cases. Evaluation script and CI configuration. Historical evaluation results showing trends. Quality threshold configuration that blocks deployment on regression. Evidence that an evaluation failure blocked a deployment. |
| **Red Flags** | No evaluation harness exists. Evaluation is manual ("we read a few outputs and they looked good"). Evaluation dataset has fewer than 10 cases. Evaluations run but results do not block deployment. The evaluation dataset has not been updated since the system launched. |

### I3: Prompt Versioning

Prompts are versioned, tested, and reviewed like code.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | All prompts are stored in version control, not hardcoded as string literals scattered through the codebase. Prompt changes go through code review. Prompt versions are tied to evaluation results (each version has eval scores). Prompt rollback is possible by reverting to a previous version. A/B testing capability exists for comparing prompt versions in production. |
| **Evidence Required** | Prompt files in version control with git history showing reviews. Evaluation results linked to specific prompt versions. Prompt rollback procedure. A/B testing configuration or evidence of a recent prompt comparison experiment. |
| **Red Flags** | Prompts are hardcoded strings in application code with no version tracking. Prompt changes are deployed without review. No evaluation is run when prompts change. Prompts cannot be rolled back independently of application code. Multiple versions of the same prompt exist in different code paths with no clear ownership. |

### I4: Data Leakage Prevention

PII is not sent to external LLM APIs, or a documented exception exists.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A data classification review has been performed for all data sent to LLM APIs. PII is stripped or anonymized before sending to external APIs. If PII must be sent, a documented exception exists with: business justification, DPA (Data Processing Agreement) with the LLM provider, and user consent mechanism. Data loss prevention (DLP) scanning runs on LLM API payloads. |
| **Evidence Required** | Data classification of LLM inputs. PII stripping or anonymization code. DPA with LLM provider if PII is sent. DLP configuration. User consent mechanism if required. Audit log of data sent to LLM APIs (with PII masked in the log itself). |
| **Red Flags** | User data is sent to external LLM APIs without classification. No DPA exists with the LLM provider. PII stripping does not cover all PII types (addresses, phone numbers, SSNs). The team assumes the LLM provider "does not store data" without contractual verification. Prompt injection could cause the LLM to exfiltrate data in its response. |

### I5: Cost Controls

Token usage budgets and rate limiting on LLM calls prevent runaway costs.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | Per-user and per-request token budgets are defined and enforced. LLM API calls have rate limiting independent of application rate limiting. Cost monitoring dashboards show daily and monthly spend with trend analysis. Alerts fire when spend exceeds budget thresholds (50%, 75%, 90%). Kill switches exist to disable LLM features without full system outage. |
| **Evidence Required** | Token budget configuration. Rate limiting configuration for LLM calls. Cost monitoring dashboard. Alert configuration for budget thresholds. Kill switch implementation. Monthly cost reports for the last three months. |
| **Red Flags** | No token budgets exist. A single user or request can consume unlimited tokens. Cost monitoring is checked manually rather than automated. No alerts exist for cost overruns. A cost spike has occurred with no detection until the monthly bill arrived. The kill switch does not exist or has not been tested. |

### I6: Human-in-the-Loop

Critical actions require human approval with defined escalation paths.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | A classification of actions by risk level exists (low, medium, high, critical). High and critical actions require human approval before execution. Approval workflows have timeouts (auto-deny after N minutes). Escalation paths exist for when approvers are unavailable. Approval decisions are logged as part of the audit trail. Approval UI is separate from the AI output to prevent manipulation. |
| **Evidence Required** | Action risk classification document. Approval workflow configuration. Timeout and escalation configuration. Approval audit logs. UI/UX showing clear separation of AI recommendation from approval action. Evidence that a critical action was successfully blocked pending approval. |
| **Red Flags** | All agent actions execute without human approval. The approval UI presents the AI recommendation in a way that biases the approver toward approval. No timeout exists, causing pending actions to queue indefinitely. Approval is a rubber stamp with no context provided to the approver. Critical actions can bypass the approval workflow through API calls. |

### I7: Hallucination Mitigation

Grounding, RAG, or citation requirements reduce fabricated outputs.

| Dimension | Detail |
|---|---|
| **Pass Criteria** | LLM outputs that present facts are grounded in retrieved documents (RAG), structured data, or verified knowledge bases. Citations or source references are included in outputs. Confidence scores or uncertainty indicators are surfaced to users. Outputs are validated against source material when possible (automated fact-checking). Users are informed when the system is uncertain or when no grounding data was found. |
| **Evidence Required** | RAG pipeline or grounding implementation. Citation inclusion in LLM outputs. Confidence scoring mechanism. Automated validation logic. User-facing uncertainty indicators. Evaluation results showing hallucination rate on the test dataset. |
| **Red Flags** | LLM outputs are presented as authoritative with no source attribution. No RAG or grounding mechanism exists for factual queries. The system does not distinguish between grounded and ungrounded responses. Hallucination rate has not been measured. Users cannot distinguish AI-generated content from verified information. |

---

## Scoring Summary

### Per-Section Scoring

For each section, count the items rated PASS, PARTIAL, and FAIL.

| Section | Items | PASS | PARTIAL | FAIL | Section Score |
|---|---|---|---|---|---|
| A: Purpose & Scope | 4 | | | | |
| B: Boundaries & Domain Model | 5 | | | | |
| C: Contracts & Interfaces | 5 | | | | |
| D: Data Architecture | 5 | | | | |
| E: Reliability & Resilience | 6 | | | | |
| F: Security & Privacy | 8 | | | | |
| G: Observability & Operability | 7 | | | | |
| H: Testing & Delivery | 6 | | | | |
| I: AI/Agent-Specific (if applicable) | 7 | | | | |
| **TOTAL** | **46 (or 53 with Section I)** | | | | |

### Score Calculation

- **PASS** = 1 point
- **PARTIAL** = 0.5 points
- **FAIL** = 0 points
- **Section Score** = (Total Points / Item Count) x 100%
- **Overall Score** = (Total Points across all applicable sections / Total applicable items) x 100%

### Overall Grade

| Grade | Score Range | Meaning |
|---|---|---|
| **A** | 90% - 100% | Production-ready. Minor improvements identified. Ship with confidence. |
| **B** | 75% - 89% | Conditionally ready. Specific items require remediation with defined timelines. Ship with caution and a remediation plan. |
| **C** | 60% - 74% | Not ready. Significant gaps exist. Address critical items before considering production deployment. |
| **D** | Below 60% | Fundamental redesign required. Major architectural concerns must be resolved. |

### STOP-SHIP Override Rule

**Any STOP-SHIP item rated FAIL results in an automatic grade of D, regardless of all other scores.**

The STOP-SHIP items are:

| Item | Section | Condition |
|---|---|---|
| **F1: Authentication Enforced** | Security | Any unauthenticated mutating endpoint |
| **F3: Secrets Management** | Security | Any secret in source code or git history |
| **F4: Input Validation** | Security | Any SQL injection or command injection vulnerability |
| **H1: Test Pyramid Balanced** | Testing | No automated tests exist |

These represent vulnerabilities and risks so severe that no amount of excellence in other areas compensates. A system with SQL injection is not "mostly good" -- it is compromised.

### Evidence Requirements Summary

The review board requires the following evidence per section:

| Section | Minimum Evidence |
|---|---|
| A: Purpose & Scope | Mission statement, NFR document, stakeholder matrix, scope boundaries document |
| B: Boundaries & Domain Model | Context boundary diagram, glossary, coupling analysis, context map |
| C: Contracts & Interfaces | API docs with versions, error schema, schema registry, contract tests, idempotency tests |
| D: Data Architecture | Query plans, consistency model docs, migration files with rollback, ownership map, recovery drill report |
| E: Reliability & Resilience | Timeout/retry config, idempotency implementation, rate limiting config, circuit breaker config, shutdown handler, chaos plan |
| F: Security & Privacy | Auth config, role matrix, secrets scan, SAST results, audit logs, encryption config, dependency scan, PII inventory |
| G: Observability & Operability | SLO definitions, log samples, trace output, dashboards, alert config, runbooks, on-call schedule |
| H: Testing & Delivery | Test counts and coverage, CI config, deployment pipeline, feature flag config, migration tests, load test results |
| I: AI/Agent-Specific | Tool permissions, eval dataset and results, prompt version history, DLP config, cost dashboards, approval workflows, RAG pipeline |

---

## Elite Outcome Criteria

A system that achieves Grade A on this scorecard exhibits four defining properties. These are not aspirational qualities posted on a wall -- they are observable, testable, and measurable behaviors of the running system.

**Scale without brittleness.** The system handles 10x current load by adding resources, not by rewriting code. Coupling metrics remain stable as the team grows. New bounded contexts are added without modifying existing ones. The module dependency graph has no cycles, and adding a new feature does not require coordinated deployments across multiple services.

**Evolve without fear.** Engineers deploy multiple times per day with confidence. Feature flags enable progressive rollout. Contract tests catch breaking changes before they reach production. Schema migrations run forward and backward without data loss. The test suite runs in under 15 minutes and catches real bugs. A new team member can deploy to production within their first week.

**Fail gracefully and recover automatically.** Every external dependency has a circuit breaker, timeout, and fallback. The system sheds load before it collapses. Graceful shutdown drains connections without dropping requests. Chaos experiments have verified the failure modes. Recovery from a zone failure happens without human intervention. RTO has been tested, not just documented.

**Everything measurable, auditable, and governable.** SLOs are defined and tracked with error budgets that drive prioritization. Every state change is recorded in an immutable audit trail. Every LLM call is logged with cost attribution. Every secret has a rotation date. Every alert links to a runbook. Every deployment is traceable to a commit, a review, and a test result. Nothing is invisible.

These four properties are the difference between a system that survives production and one that thrives in it. The scorecard above is the map. The evidence is the territory. Review both.
