# Elite Software Architecture: Operational Playbook

> A comprehensive reference for producing production-grade architecture decisions, designs, and reviews. Every section is actionable: principles include enforcement mechanisms, patterns include concrete configurations, and strategies include measurable quality gates.

---

## 1. The Ten Operating Principles

These principles are ordered by priority. When two principles conflict, the higher-numbered principle yields to the lower-numbered one.

### 1.1 Boundaries First

**Principle:** Domain boundaries and trust boundaries are explicit, documented, and enforced in code and infrastructure.

**Rationale:** The single most expensive architectural mistake is an unclear boundary. When module A reaches into module B's internals, every change to B becomes a change to A. Trust boundaries that exist only in documentation get violated the moment a deadline arrives.

**Enforcement examples:**
- Each bounded context owns its own database schema; no cross-schema joins.
- Internal module APIs are exposed through explicit public interfaces (Python: `__init__.py` re-exports; Go: exported types; Java: module-info.java).
- Network policies enforce east-west traffic rules: service A cannot call service C directly if the architecture says it must go through service B.

**Violation signal:** A pull request introduces a direct import from another module's internal package, or a database migration adds a foreign key referencing another module's table.

---

### 1.2 Change Is the Constant

**Principle:** Design every component for safe evolution, not just initial delivery.

**Rationale:** The first version of any system is the cheapest version. The cost of software is dominated by the second through hundredth change. Architectures that optimize for day-one simplicity at the expense of changeability accumulate compound interest in technical debt.

**Enforcement examples:**
- Every API endpoint is versioned from day one (`/v1/orders`).
- Database schemas use expand-contract migrations; columns are never renamed or removed in a single step.
- Feature flags gate all user-visible changes, enabling instant rollback without deployment.

**Violation signal:** A schema migration drops a column that downstream consumers still reference. A "quick" API change breaks existing clients without a deprecation period.

---

### 1.3 Reliability Is a Feature

**Principle:** Ship both the happy-path behavior and the failure behavior. If a failure mode has not been designed, it has been designed poorly.

**Rationale:** Distributed systems do not fail cleanly. Network partitions, clock skew, partial failures, and retry storms are not edge cases; they are operating conditions. Reliability that is bolted on after launch is always more expensive and less effective than reliability built in.

**Enforcement examples:**
- Every outbound HTTP call has an explicit timeout, retry policy, and circuit breaker.
- Every async consumer defines a dead-letter queue and a retry strategy.
- Every critical path has a defined graceful degradation mode documented in its runbook.

**Violation signal:** An HTTP client is instantiated with default (infinite) timeouts. A message consumer silently drops failed messages. A service has no health check endpoint.

---

### 1.4 Observability Is Part of the Product

**Principle:** If a behavior cannot be measured and alerted on, it does not exist in production.

**Rationale:** You cannot improve what you cannot see. Observability is not a debugging luxury; it is the mechanism by which you know your system is meeting its promises. SLOs without instrumentation are fiction.

**Enforcement examples:**
- Every request handler emits structured logs with a correlation ID, duration, and status code.
- Every service publishes RED metrics (Rate, Errors, Duration) to a metrics backend.
- Every deployment pipeline includes a step that verifies new instrumentation is present.

**Violation signal:** A new endpoint is deployed without corresponding metrics or log statements. An alert fires but the on-call engineer cannot find correlated traces.

---

### 1.5 Security Is an Invariant

**Principle:** Least privilege and auditable actions are the default, not an opt-in layer.

**Rationale:** Security bolted on after the fact creates seams that attackers exploit. When security is an invariant -- a property that holds at every state transition -- it becomes dramatically harder to violate and cheaper to maintain.

**Enforcement examples:**
- Service accounts use short-lived tokens with minimal scopes; no long-lived API keys.
- Every state-changing operation writes an immutable audit log entry before returning success.
- CI pipelines fail on any dependency with a known CVE rated HIGH or CRITICAL.

**Violation signal:** A service account has admin privileges. An API endpoint modifies data without writing an audit record. A `requirements.txt` pins to `*` instead of exact versions.

---

### 1.6 Constraints Are Automated

**Principle:** Architectural constraints live in CI pipelines as fitness functions, not in wiki pages or team memory.

**Rationale:** Documentation that says "module X must not depend on module Y" is a suggestion. A CI check that fails the build when that dependency appears is a constraint. Tribal knowledge leaves when people leave; automated checks persist.

**Enforcement examples:**
- ArchUnit or pytest-archon tests verify module dependency rules on every commit.
- A pre-commit hook rejects files containing hardcoded secrets (detect-secrets, gitleaks).
- Schema compatibility is checked against the registry before merge.

**Violation signal:** An architect explains a constraint verbally in a meeting but does not add a corresponding CI check. A "known rule" is violated in a PR that passes all automated checks.

---

### 1.7 Fast Feedback Loops

**Principle:** Reduce the time between a change and knowledge of its impact to the minimum achievable.

**Rationale:** A bug found in code review costs 10x less than one found in staging and 100x less than one found in production. Fast feedback loops are not just about testing; they encompass canary deployments, feature flags, and safe rollback mechanisms that let you learn from production safely.

**Enforcement examples:**
- Unit tests run in under 10 seconds; the full CI pipeline completes in under 10 minutes.
- Canary deployments automatically roll back if error rate exceeds baseline by 2x.
- Feature flags allow instant kill-switch for any new behavior without a deploy.

**Violation signal:** The CI pipeline takes over 30 minutes. A deployment requires a full rollback (redeploy previous version) rather than a flag toggle. Tests are skipped because they are "too slow."

---

### 1.8 Simple Defaults

**Principle:** Start with a modular monolith and hexagonal architecture. Introduce distributed complexity only when a concrete, measurable constraint demands it.

**Rationale:** Microservices are an optimization for organizational scaling, not a starting architecture. A well-structured monolith is easier to develop, test, deploy, and debug. Premature distribution multiplies operational complexity without delivering proportional value.

**Enforcement examples:**
- New projects start from the modular monolith template (Section 2).
- A service extraction requires a written ADR documenting the specific constraint that justifies it.
- Shared libraries are preferred over shared services for cross-cutting concerns.

**Violation signal:** A team proposes a new microservice without documenting why the functionality cannot live in an existing module. A system with three developers has twelve services.

---

### 1.9 Explicit Contracts

**Principle:** Every inter-component interface -- API, event, schema, file format -- is versioned, documented, and enforced.

**Rationale:** Implicit contracts are the primary source of integration failures. When two teams disagree about the shape of a payload, the one with the most recent deployment "wins" and the other breaks. Explicit contracts make these agreements visible and testable.

**Enforcement examples:**
- OpenAPI specs are the source of truth for HTTP APIs; code is generated from specs.
- Event schemas are registered in a schema registry with backward compatibility checks.
- Database schemas include version metadata and migration scripts in version control.

**Violation signal:** An API response includes fields not present in the OpenAPI spec. A consumer breaks because a producer added a required field to an event without a schema version bump.

---

### 1.10 Everything Has an Owner

**Principle:** Every service, module, dataset, runbook, dashboard, and cost center has a named owner recorded in a machine-readable format.

**Rationale:** Unowned components decay. When no one is responsible for a service's SLO, its reliability degrades. When no one owns a dashboard, its queries become stale. Ownership is the mechanism by which accountability and continuous improvement are sustained.

**Enforcement examples:**
- Every repository contains an `OWNERS` or `CODEOWNERS` file mapping paths to teams.
- Every service is tagged with `owner`, `team`, and `cost-center` in infrastructure-as-code.
- Quarterly ownership audits flag unowned or orphaned resources.

**Violation signal:** A production alert fires and no one knows who to page. A cloud bill includes significant spend from resources with no owner tag. A runbook references a team that no longer exists.

---

## 2. Default Architecture Template

### Modular Monolith + Hexagonal Architecture

This is the starting point for every new system. Deviate only with a documented ADR.

```
project-root/
|-- src/
|   |-- modules/
|   |   |-- orders/
|   |   |   |-- domain/           # Entities, value objects, domain events, invariants
|   |   |   |   |-- models.py
|   |   |   |   |-- events.py
|   |   |   |   |-- exceptions.py
|   |   |   |   |-- services.py   # Domain services (pure logic, no I/O)
|   |   |   |-- application/      # Use cases, command/query handlers
|   |   |   |   |-- commands.py
|   |   |   |   |-- queries.py
|   |   |   |   |-- policies.py   # Authorization, validation orchestration
|   |   |   |-- ports/            # Interfaces (ABCs / protocols)
|   |   |   |   |-- repositories.py
|   |   |   |   |-- event_publisher.py
|   |   |   |   |-- payment_gateway.py
|   |   |   |-- adapters/         # Implementations of ports
|   |   |   |   |-- postgres_repo.py
|   |   |   |   |-- kafka_publisher.py
|   |   |   |   |-- stripe_gateway.py
|   |   |   |-- __init__.py       # Public API -- only export what other modules may use
|   |   |-- inventory/
|   |   |   |-- ...               # Same structure
|   |   |-- shipping/
|   |       |-- ...
|   |-- shared/                   # Truly shared kernel (keep minimal)
|   |   |-- types.py              # Money, Address, UserId
|   |   |-- events.py             # Cross-module event base classes
|   |-- entrypoints/
|   |   |-- api/                  # HTTP handlers (FastAPI, Flask)
|   |   |-- cli/                  # CLI commands
|   |   |-- workers/              # Async consumers, background jobs
|   |   |-- schedulers/           # Cron-like periodic tasks
|   |-- infrastructure/
|       |-- config.py             # Environment-based configuration
|       |-- observability.py      # Logging, metrics, tracing setup
|       |-- middleware.py         # Auth, correlation ID, error handling
|-- tests/
|   |-- unit/                     # Domain + application layer tests (no I/O)
|   |-- integration/              # Adapter tests with real dependencies
|   |-- contract/                 # API contract tests
|   |-- system/                   # End-to-end tests
|-- migrations/                   # Database migrations (Alembic, Flyway)
|-- docs/
|   |-- adrs/                     # Architecture Decision Records
|   |-- runbooks/
|-- fitness/                      # Architectural fitness functions
|   |-- test_boundaries.py
|   |-- test_dependencies.py
|-- pyproject.toml / Makefile / docker-compose.yml
```

### Layer Rules

| Layer | May Depend On | Must Not Depend On |
|-------|--------------|-------------------|
| Domain | Standard library, shared kernel types | Application, Ports, Adapters, Entrypoints, any I/O library |
| Application | Domain, Ports (interfaces only) | Adapters, Entrypoints |
| Ports | Domain (for type references) | Adapters, Entrypoints, Application |
| Adapters | Domain, Ports, external libraries | Entrypoints, Application (except via DI) |
| Entrypoints | Application (via dependency injection) | Domain internals, Adapters directly |

### When to Extract a Service (All Four Criteria Must Be Met)

1. **Independent scaling requirement:** The module needs to scale at a fundamentally different rate or on different hardware (e.g., CPU-bound ML inference vs. I/O-bound CRUD).
2. **Independent deployment cadence:** The module changes 10x more frequently than adjacent modules and the coupling tax of shared deployment is measurable.
3. **Distinct failure domain:** A failure in this module must not cascade to the rest of the system, and in-process isolation (bulkheads, thread pools) is insufficient.
4. **Organizational boundary:** A separate team owns this module and the coordination cost of shared code exceeds the cost of a network boundary.

If fewer than four criteria are met, the module stays in the monolith.

---

## 3. Boundary & Invariant Definition Guide

### Bounded Context Identification

A bounded context is identified by asking three questions:

1. **Language divergence:** Do the same words mean different things? ("Account" in billing vs. identity is two bounded contexts.)
2. **Lifecycle independence:** Can this concept change without requiring changes to its neighbors?
3. **Data ownership:** Does this concept have a single authoritative source of truth?

### Context Mapping Patterns

| Pattern | When to Use | Example |
|---------|------------|---------|
| **Conformist** | Downstream accepts upstream's model as-is; low divergence | Internal service consuming a well-designed domain event |
| **Anti-Corruption Layer (ACL)** | Upstream model is messy, legacy, or external; protect your domain | Wrapping a third-party payment API in your own gateway port |
| **Shared Kernel** | Two contexts co-evolve tightly and are owned by the same team | Shared value objects (Money, Address) in a monolith |
| **Open Host Service** | Upstream publishes a clean, documented API for many consumers | A public API gateway with OpenAPI specs |
| **Published Language** | Both sides agree on a canonical schema (e.g., CloudEvents, Protocol Buffers) | Event-driven integration between two bounded contexts |

### Trust Boundaries

- **Internal (same trust zone):** Calls between modules in the same process or between services behind the same network perimeter. AuthN is service-identity-based (mTLS, workload identity). AuthZ is enforced at the application layer.
- **External (zero-trust zone):** Calls from user-facing clients, third-party integrations, or across organizational boundaries. All input is untrusted. AuthN requires user identity tokens (JWT, OAuth2). Rate limiting, input validation, and WAF rules apply.
- **Privileged (admin zone):** Calls that modify system configuration, access secrets, or perform break-glass operations. Require MFA, short-lived elevated tokens, and enhanced audit logging.

### Data Classification

| Level | Description | Storage | Access | Example |
|-------|------------|---------|--------|---------|
| **Public** | Intentionally published | Any | Any | Marketing site content, public API docs |
| **Internal** | Business operational data | Encrypted at rest | Authenticated employees/services | Internal dashboards, aggregate metrics |
| **Confidential** | Business-sensitive or customer data | Encrypted at rest + field-level for PII | Role-based, audit-logged | Customer records, financial transactions |
| **Restricted** | Regulatory or legally protected | Encrypted at rest + in transit + field-level, key rotation every 90 days | Named individuals, MFA required, full audit trail | Payment card data (PCI), health records (HIPAA), credentials |

### Tenancy Models

| Model | Isolation | Cost | Complexity | Use When |
|-------|-----------|------|-----------|----------|
| **Shared DB, shared schema** (row-level tenant ID) | Low | Low | Low | SaaS MVP, homogeneous tenants, <100 tenants |
| **Shared DB, schema-per-tenant** | Medium | Medium | Medium | Moderate regulatory needs, tenant-specific migrations |
| **DB-per-tenant** | High | High | High | Strict regulatory isolation, large enterprise tenants |

For row-level tenancy, enforce tenant isolation at the ORM/query layer:

```python
class TenantAwareRepository:
    def __init__(self, session: Session, tenant_id: str):
        self._session = session
        self._tenant_id = tenant_id

    def query(self, model: type[T]) -> Query[T]:
        return self._session.query(model).filter(
            model.tenant_id == self._tenant_id
        )
```

---

## 4. Contract Discipline

### API-First Design

The design sequence is: **Spec -> Review -> Codegen -> Implement -> Contract Test**.

1. Write the OpenAPI 3.1 spec before writing any handler code.
2. Review the spec in a PR -- this is an architecture review, not a code review.
3. Generate server stubs and client SDKs from the spec.
4. Implement the handler logic behind the generated interfaces.
5. Contract tests validate that the implementation matches the spec.

```yaml
# openapi.yaml excerpt
openapi: "3.1.0"
info:
  title: Orders API
  version: "1.2.0"
paths:
  /v1/orders:
    post:
      operationId: createOrder
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateOrderRequest"
      responses:
        "201":
          description: Order created
          headers:
            Idempotency-Key:
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
        "409":
          description: Duplicate idempotency key
```

### Event-First Design

Events use the CloudEvents envelope with a schema registry:

```json
{
  "specversion": "1.0",
  "id": "evt_abc123",
  "source": "/orders-module",
  "type": "com.example.order.created.v1",
  "datacontenttype": "application/json",
  "time": "2026-02-22T10:30:00Z",
  "data": {
    "order_id": "ord_xyz",
    "customer_id": "cust_456",
    "total_cents": 4999,
    "currency": "USD"
  }
}
```

**Schema versioning rules:**
- Adding an optional field: compatible, same major version.
- Removing a field or changing a type: breaking, new major version.
- Renaming a field: breaking, new major version. Add the new field alongside the old one during the transition.

### Breaking Change Protocol

1. **Announce:** Add deprecation notice to the spec and changelog. Set `Sunset` header on deprecated endpoints.
2. **Support period:** Maintain the old version for a minimum of 2 release cycles or 90 days, whichever is longer.
3. **Migrate:** Provide migration guide and, where possible, automated migration tooling.
4. **Remove:** Delete the old version only after confirming zero traffic (via metrics) or after the sunset date.

### Idempotency

All state-changing operations must support idempotency:

```python
@app.post("/v1/orders")
async def create_order(
    request: CreateOrderRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    existing = await idempotency_store.get(idempotency_key)
    if existing:
        return existing  # Return cached response, same status code

    result = await order_service.create(request)
    await idempotency_store.set(idempotency_key, result, ttl=86400)
    return result
```

---

## 5. Minimum Reliability Kit

### Timeouts

| Timeout Type | Default | Max | Notes |
|-------------|---------|-----|-------|
| TCP connect | 2s | 5s | Fail fast if host is unreachable |
| Read/response | 10s | 30s | Adjust per endpoint; batch endpoints get longer |
| Total request | 15s | 60s | Includes retries; the outer budget |
| Database query | 5s | 30s | Statement timeout at DB level, not just client |
| Queue consumer ack | 30s | 300s | Must ack or nack before visibility timeout |

### Retries

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=10, jitter=2),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
async def call_payment_gateway(request: PaymentRequest) -> PaymentResult:
    return await gateway.charge(request)
```

**Rules:**
- Never retry non-idempotent operations without an idempotency key.
- Never retry 4xx errors (except 429 Too Many Requests).
- Always add jitter to prevent thundering herd.
- Set a total timeout budget that encompasses all retry attempts.

### Circuit Breakers

```python
# Using pybreaker or equivalent
breaker = CircuitBreaker(
    fail_max=5,                # Open after 5 consecutive failures
    reset_timeout=30,          # Try half-open after 30 seconds
    exclude=[ValidationError], # Don't count client errors as failures
)

@breaker
async def call_inventory_service(sku: str) -> StockLevel:
    return await inventory_client.check_stock(sku)
```

**States:**
- **Closed:** Normal operation. Track failure rate over a rolling window.
- **Open:** All calls fail immediately with a fallback. Duration: 30 seconds.
- **Half-Open:** Allow 1-3 probe requests. If they succeed, close. If they fail, re-open.

### Bulkheads

Isolate failure domains with dedicated resource pools:

```python
# Separate connection pools per downstream dependency
payment_pool = httpx.AsyncClient(
    limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
    timeout=httpx.Timeout(connect=2.0, read=10.0, pool=5.0),
)

inventory_pool = httpx.AsyncClient(
    limits=httpx.Limits(max_connections=50, max_keepalive_connections=25),
    timeout=httpx.Timeout(connect=2.0, read=5.0, pool=5.0),
)
```

### Rate Limiting

```python
# Token bucket configuration
rate_limits = {
    "default": {"rate": 100, "period": 60},      # 100 req/min general
    "per_tenant": {"rate": 1000, "period": 60},   # 1000 req/min per tenant
    "expensive_ops": {"rate": 10, "period": 60},  # 10 req/min for heavy endpoints
}
```

### Load Shedding & Graceful Degradation

Define degradation tiers:

| Tier | Trigger | Behavior |
|------|---------|----------|
| **Nominal** | Normal load | Full functionality |
| **Degraded** | P99 latency > 2x SLO, error rate > 1% | Disable non-critical features (recommendations, analytics), serve cached results |
| **Critical** | Error rate > 10%, circuit breakers open | Return static fallback responses, reject non-essential traffic, page on-call |
| **Emergency** | System at risk of total failure | Shed all non-authenticated traffic, serve minimal health check, activate break-glass procedures |

```python
class DegradationManager:
    def current_tier(self) -> Tier:
        error_rate = metrics.get_error_rate(window="5m")
        p99 = metrics.get_latency_p99(window="5m")
        if error_rate > 0.10:
            return Tier.CRITICAL
        if error_rate > 0.01 or p99 > self.slo_p99 * 2:
            return Tier.DEGRADED
        return Tier.NOMINAL

    async def maybe_serve_cached(self, key: str, fresh_fn):
        if self.current_tier() >= Tier.DEGRADED:
            cached = await cache.get(key)
            if cached:
                return cached  # Serve stale data with header indicating staleness
        return await fresh_fn()
```

---

## 6. Security & Privacy as Architecture

### Identity & Authorization

| Concern | External (User-facing) | Internal (Service-to-service) |
|---------|----------------------|------------------------------|
| **AuthN** | OAuth2 + OIDC, JWT access tokens (short-lived: 15 min) | mTLS with workload identity (SPIFFE/SPIRE) |
| **AuthZ** | RBAC for coarse access, ABAC for fine-grained policies | Service-level ACLs, scope-based token validation |
| **Token format** | Opaque reference tokens at the edge, JWT internally | X.509 certificates with SANs |
| **Session** | Refresh tokens (24h), secure/httponly/samesite cookies | No sessions; stateless mTLS per-request |

### Data Protection

```yaml
# Encryption configuration reference
encryption:
  at_rest:
    algorithm: AES-256-GCM
    key_management: AWS KMS / GCP KMS / HashiCorp Vault
    key_rotation: every 90 days
    envelope_encryption: true  # Data key encrypted by master key
  in_transit:
    minimum_tls: "1.3"
    cipher_suites:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
  field_level:
    pii_fields: [email, phone, ssn, date_of_birth]
    algorithm: AES-256-GCM with per-field data keys
    searchable: false  # Use blind index for searchable encrypted fields
```

### Audit Log

Every state-changing action produces an immutable audit record:

```json
{
  "event_id": "audit_789",
  "timestamp": "2026-02-22T10:31:00.000Z",
  "actor": {"type": "user", "id": "usr_123", "ip": "10.0.1.5"},
  "action": "order.created",
  "resource": {"type": "order", "id": "ord_xyz"},
  "context": {"tenant_id": "t_456", "correlation_id": "req_abc"},
  "outcome": "success",
  "metadata": {"idempotency_key": "idk_001"}
}
```

**Requirements:** Append-only storage (no updates or deletes), integrity verification (hash chain or Merkle tree), retention per data classification policy (minimum 1 year for confidential, 7 years for restricted/financial).

### Supply Chain Security

- **SBOM:** Generate Software Bill of Materials on every build (Syft, CycloneDX).
- **Dependency scanning:** Run on every PR and nightly (Dependabot, Snyk, Trivy).
- **Signed artifacts:** Container images signed with Sigstore/cosign; verify signatures before deployment.
- **Reproducible builds:** Pin all dependencies to exact versions with hashes. Lock files are committed.
- **Base image policy:** Only approved base images from a curated registry. No `latest` tags.

---

## 7. SLO-Driven Observability

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Every log entry automatically includes:
# - timestamp (ISO 8601)
# - level
# - correlation_id (from request context)
# - service, version, environment

logger.info(
    "order_created",
    order_id="ord_xyz",
    customer_id="cust_456",
    total_cents=4999,
    duration_ms=42,
)
# Output: {"timestamp":"2026-02-22T10:31:00Z","level":"info","event":"order_created",
#          "order_id":"ord_xyz","correlation_id":"req_abc","service":"orders","duration_ms":42}
```

**Rules:**
- JSON format in production, human-readable in development.
- PII is never logged. Use tokenized references (`customer_id`) not raw data (`customer_email`).
- Log at boundaries: request received, external call made, response sent, error caught.
- Log levels: DEBUG (development only), INFO (business events), WARNING (recoverable issues), ERROR (failures requiring attention), CRITICAL (system-level failures).

### Metrics

**RED for services (request-driven):**

| Metric | Instrument | Example |
|--------|-----------|---------|
| **Rate** | Counter | `http_requests_total{method, path, status}` |
| **Errors** | Counter | `http_requests_total{status=~"5.."}` or dedicated `errors_total{type}` |
| **Duration** | Histogram | `http_request_duration_seconds{method, path}` with buckets: 0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10 |

**USE for resources (infrastructure):**

| Metric | Instrument | Example |
|--------|-----------|---------|
| **Utilization** | Gauge | `db_connection_pool_used / db_connection_pool_max` |
| **Saturation** | Gauge | `queue_depth`, `thread_pool_pending_tasks` |
| **Errors** | Counter | `db_connection_errors_total`, `disk_io_errors_total` |

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({
    "service.name": "orders-service",
    "service.version": "1.2.0",
    "deployment.environment": "production",
}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

async def create_order(request):
    with tracer.start_as_current_span(
        "create_order",
        attributes={"order.customer_id": request.customer_id},
    ) as span:
        # Trace context propagates automatically via W3C Trace Context headers
        inventory = await check_inventory(request.items)
        payment = await charge_payment(request.payment)
        span.set_attribute("order.id", order.id)
        return order
```

**Span naming conventions:** `{operation}` for internal, `{service}/{operation}` for external calls. Examples: `create_order`, `payment-gateway/charge`, `postgres/query`.

### SLO Definitions

```yaml
slos:
  - name: "Order API Availability"
    sli: "successful requests / total requests"  # 2xx and 4xx are success; 5xx is failure
    target: 99.9%                                 # 43.8 min/month error budget
    window: 30 days (rolling)
    burn_rate_alerts:
      - severity: warning
        burn_rate: 6x     # Exhausts budget in 5 days
        short_window: 5m
        long_window: 1h
      - severity: critical
        burn_rate: 14x    # Exhausts budget in 2.14 days
        short_window: 2m
        long_window: 15m

  - name: "Order API Latency"
    sli: "requests < 500ms / total requests"
    target: 99.0%
    window: 30 days (rolling)
```

### Runbook Template

```markdown
# Runbook: [Service] - [Symptom]

## Symptoms
- Alert name and threshold
- What the operator will see in dashboards/logs

## Impact
- User-facing impact (degraded feature, full outage)
- Affected SLOs

## Diagnosis
1. Check [dashboard link] for [metric]
2. Query logs: `{service="orders"} |= "error" | json | status >= 500`
3. Check dependent services: [list with status pages]

## Remediation
- **If [condition A]:** [action, command, or procedure]
- **If [condition B]:** [action, command, or procedure]
- **If unknown:** Escalate to [team] via [channel]

## Escalation
- L1: On-call engineer (PagerDuty)
- L2: Service owner ([name/team])
- L3: Platform team ([name/team])

## Post-Incident
- File incident report within 24 hours
- Schedule blameless post-mortem within 72 hours
```

---

## 8. Testing Strategy

### The Test Pyramid

```
        /  System Tests  \          ~5%    Slow, expensive, high confidence
       / Contract Tests    \        ~10%   Medium speed, integration confidence
      / Integration Tests    \      ~20%   Adapter + real dependency
     /   Unit Tests            \    ~65%   Fast, isolated, domain logic
    /____________________________\
```

### Unit Tests

Target: Domain layer and application layer. Zero I/O. Sub-second execution.

```python
def test_order_rejects_negative_quantity():
    with pytest.raises(InvalidQuantityError):
        Order.create(
            customer_id="cust_1",
            items=[OrderItem(sku="ABC", quantity=-1, price_cents=1000)],
        )

def test_order_calculates_total():
    order = Order.create(
        customer_id="cust_1",
        items=[
            OrderItem(sku="A", quantity=2, price_cents=1000),
            OrderItem(sku="B", quantity=1, price_cents=500),
        ],
    )
    assert order.total_cents == 2500
```

### Integration Tests

Target: Adapter implementations against real dependencies using testcontainers.

```python
@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine

def test_postgres_repo_persists_order(postgres):
    repo = PostgresOrderRepository(Session(postgres))
    order = Order.create(customer_id="cust_1", items=[...])
    repo.save(order)
    retrieved = repo.get_by_id(order.id)
    assert retrieved == order
```

### Contract Tests

Validate API compatibility between producer and consumer using Pact or Schemathesis:

```python
# Consumer side: define expectations
@pact.upon_receiving("a request to create an order")
@pact.with_request("POST", "/v1/orders", body={"customer_id": "cust_1", "items": [...]})
@pact.will_respond_with(201, body=Like({"id": "ord_1", "status": "pending"}))
def test_create_order_contract(pact_server):
    client = OrderClient(base_url=pact_server.url)
    result = client.create_order(customer_id="cust_1", items=[...])
    assert result.status == "pending"
```

### Non-Functional Tests

| Type | Tool | Trigger | Threshold |
|------|------|---------|-----------|
| Load testing | k6 | Pre-release, weekly | P99 < 500ms at 2x expected peak |
| Chaos testing | Chaos Monkey, Litmus | Monthly game day | System recovers within SLO budget |
| Security scanning | OWASP ZAP, Semgrep | Every PR, nightly | Zero HIGH/CRITICAL findings |
| Mutation testing | mutmut, Stryker | Weekly | Mutation score > 80% for domain layer |

### AI / Agent Testing

```python
# Eval harness for LLM-backed components
@pytest.mark.parametrize("case", load_eval_cases("evals/classification.yaml"))
async def test_intent_classification(agent, case):
    result = await agent.classify(case.input)
    assert result.intent == case.expected_intent
    assert result.confidence >= case.min_confidence

# Tool call validation
async def test_agent_calls_correct_tools():
    result = await agent.run("Check inventory for SKU-123")
    tool_calls = [step.tool_name for step in result.steps if step.is_tool_call]
    assert "check_inventory" in tool_calls
    assert "charge_payment" not in tool_calls  # Must not call unrelated tools

# Prompt regression test
async def test_prompt_stability():
    baseline = load_baseline("baselines/v1.json")
    results = await run_eval_suite(agent, eval_cases)
    assert results.accuracy >= baseline.accuracy - 0.02  # Max 2% regression
```

### Quality Gates

```yaml
# CI quality gate configuration
quality_gates:
  coverage:
    line: 80%
    branch: 70%
    domain_layer: 95%    # Highest bar for business logic
  architecture:
    - "no cross-module internal imports"
    - "domain layer has zero I/O imports"
    - "all ports are abstract (Protocol or ABC)"
  security:
    - "no secrets in source (detect-secrets)"
    - "no CVEs above MEDIUM (trivy, safety)"
  performance:
    - "unit tests complete in < 10s"
    - "full pipeline completes in < 10m"
```

---

## 9. Delivery & Change Management

### Progressive Delivery

```
Code Merge -> Build -> Deploy Canary (1%) -> Monitor (15 min)
  -> If healthy: Expand (10%) -> Monitor (15 min)
  -> If healthy: Expand (50%) -> Monitor (30 min)
  -> If healthy: Promote (100%)
  -> At any stage, if error rate > baseline * 2: Auto-rollback
```

**Feature flags are mandatory for all user-visible changes:**

```python
async def get_recommendations(user_id: str):
    if feature_flags.is_enabled("new-recommendation-engine", user_id=user_id):
        return await new_engine.recommend(user_id)
    return await legacy_engine.recommend(user_id)
```

Flag lifecycle: `created -> testing -> canary -> GA -> permanent | removed`. Flags older than 90 days without a status update are flagged for cleanup.

### Migration Discipline: Expand-Contract

**Phase 1 -- Expand:** Add the new column/field/endpoint alongside the old one. Both work. Deploy. Verify.

**Phase 2 -- Migrate:** Backfill data, update consumers to use the new path. Monitor until old path traffic reaches zero.

**Phase 3 -- Contract:** Remove the old column/field/endpoint. Deploy. Verify.

```sql
-- Phase 1: Expand
ALTER TABLE orders ADD COLUMN customer_email_v2 VARCHAR(255);
-- Application writes to both columns

-- Phase 2: Migrate
UPDATE orders SET customer_email_v2 = customer_email WHERE customer_email_v2 IS NULL;
-- Application reads from v2, writes to both

-- Phase 3: Contract (after all consumers migrated)
ALTER TABLE orders DROP COLUMN customer_email;
ALTER TABLE orders RENAME COLUMN customer_email_v2 TO customer_email;
```

### ADR Practice

**When to write an ADR:**
- Choosing between two or more viable approaches.
- Deviating from the default architecture template.
- Adopting or replacing a technology, framework, or service.
- Changing a boundary, contract, or data model in a non-backward-compatible way.

**ADR template:**

```markdown
# ADR-NNN: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
What is the issue? What constraints apply? What forces are at play?

## Decision
What is the change we are making? Be specific.

## Consequences
What are the positive, negative, and neutral outcomes of this decision?

## Alternatives Considered
What other options were evaluated and why were they rejected?
```

**Lifecycle:** ADRs are immutable once accepted. If a decision is reversed, write a new ADR that supersedes the original. Never edit an accepted ADR.

---

## 10. Operability & Excellence Loops

### Incident Response

| Severity | Criteria | Response Time | Escalation |
|----------|----------|--------------|------------|
| **SEV1** | Complete outage, data loss, security breach | 15 minutes | Page on-call, incident commander, engineering lead |
| **SEV2** | Major feature degraded, SLO burn rate critical | 30 minutes | Page on-call, notify service owner |
| **SEV3** | Minor feature degraded, error rate elevated | 4 hours | Notify on-call via Slack, no page |
| **SEV4** | Cosmetic, non-impacting, workaround available | Next business day | Ticket, normal prioritization |

**Blameless post-mortem template:**
1. **Timeline:** Minute-by-minute reconstruction from detection to resolution.
2. **Impact:** Users affected, duration, SLO budget consumed.
3. **Root cause:** The systemic condition that allowed the failure, not the individual action.
4. **Contributing factors:** What made detection or resolution slower?
5. **Action items:** Each item has an owner, priority, and due date.

### Game Days

Schedule quarterly chaos experiments:

```yaml
game_day:
  frequency: quarterly
  scope: production (with safeguards) or staging
  scenarios:
    - name: "Database failover"
      action: Kill primary DB instance
      expected: Automatic failover within 30s, zero data loss
    - name: "Dependency outage"
      action: Block traffic to payment gateway
      expected: Circuit breaker opens, orders queued for retry, users see graceful error
    - name: "Region failure"
      action: Drain traffic from one availability zone
      expected: Load balancer redirects, latency increase < 50%
  safeguards:
    - Feature flag to abort experiment instantly
    - Experiment runs only during business hours with full team available
    - Blast radius limited to 5% of traffic
```

### Capacity Planning

- **Forecasting:** Use trailing 90-day traffic data to project next-quarter peak. Apply 2x headroom multiplier for growth and burst tolerance.
- **Auto-scaling triggers:** Scale out at 70% CPU or 80% memory sustained for 3 minutes. Scale in at 30% CPU sustained for 10 minutes. Minimum 2 instances always.
- **Resource right-sizing:** Review actual vs. provisioned resources monthly. Flag resources consistently using less than 20% of allocation.

### Cost Observability

```yaml
# Infrastructure tagging requirements
required_tags:
  - service: "orders-api"        # Maps cost to service
  - team: "commerce"             # Maps cost to team
  - environment: "production"    # Separates prod from dev/staging spend
  - cost_center: "CC-1234"       # Maps to finance tracking

cost_alerts:
  - type: anomaly
    threshold: 20%     # Alert if daily spend deviates > 20% from 7-day average
  - type: budget
    threshold: 80%     # Alert when 80% of monthly budget consumed
  - type: waste
    criteria: "unused resources (0 traffic for 7 days)"
```

---

## 11. Evolutionary Architecture Automation

Fitness functions are automated tests that verify architectural properties. They run in CI on every commit and fail the build on violation.

### Module Boundary Checks

```python
# fitness/test_boundaries.py
import pytest
from archon import ArchitectureRule

def test_domain_has_no_io_imports():
    """Domain layer must not import I/O libraries."""
    rule = (
        ArchitectureRule()
        .modules_matching("src.modules.*.domain.*")
        .should_not_import("sqlalchemy", "httpx", "redis", "kafka", "boto3", "requests")
    )
    rule.check()

def test_no_cross_module_internal_imports():
    """Modules must not reach into another module's internals."""
    rule = (
        ArchitectureRule()
        .modules_matching("src.modules.orders.*")
        .should_not_import("src.modules.inventory.domain.*")
        .should_not_import("src.modules.inventory.adapters.*")
        # Allowed: src.modules.inventory (public API via __init__.py)
    )
    rule.check()

def test_adapters_implement_ports():
    """Every port interface must have at least one adapter implementation."""
    for module in discover_modules("src/modules"):
        ports = get_abstract_classes(f"{module}/ports/")
        adapters = get_concrete_classes(f"{module}/adapters/")
        for port in ports:
            assert any(
                issubclass(adapter, port) for adapter in adapters
            ), f"Port {port.__name__} in {module} has no adapter implementation"
```

### Security Lint

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

# CI step
- name: Security scan
  run: |
    # No SQL string concatenation
    ! grep -rn "f\".*SELECT.*{" src/ --include="*.py"
    # No hardcoded credentials
    detect-secrets scan --baseline .secrets.baseline
    # Dependency vulnerabilities
    trivy fs --severity HIGH,CRITICAL --exit-code 1 .
```

### Dependency Rules

```python
# fitness/test_dependencies.py
import json
import subprocess
from datetime import datetime, timedelta

def test_no_critical_cves():
    """No dependencies with CRITICAL CVEs."""
    result = subprocess.run(
        ["trivy", "fs", "--format", "json", "--severity", "CRITICAL", "."],
        capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    vulnerabilities = [v for r in report.get("Results", []) for v in r.get("Vulnerabilities", [])]
    assert len(vulnerabilities) == 0, (
        f"Found {len(vulnerabilities)} CRITICAL CVEs: "
        + ", ".join(v["VulnerabilityID"] for v in vulnerabilities)
    )

def test_max_dependency_age():
    """No dependency older than 18 months without an exception."""
    max_age = timedelta(days=548)
    exceptions = load_exceptions("fitness/dependency_age_exceptions.yaml")
    for dep in get_locked_dependencies():
        if dep.name in exceptions:
            continue
        assert dep.release_date > datetime.now() - max_age, (
            f"{dep.name}=={dep.version} released {dep.release_date}, exceeds {max_age.days}-day limit"
        )
```

### Schema Compatibility

```yaml
# CI step: check schema backward compatibility
- name: Schema compatibility check
  run: |
    # For Avro/Protobuf schemas
    schema-registry-cli compatibility \
      --subject orders-value \
      --schema schemas/orders/v2.avsc \
      --compatibility BACKWARD

    # For OpenAPI specs
    oasdiff breaking \
      --base main:openapi.yaml \
      --revision HEAD:openapi.yaml \
      --fail-on ERR
```

### Performance Budgets

```python
# fitness/test_performance.py
import subprocess
import json

def test_p99_latency_under_budget():
    """P99 latency must stay under 500ms for critical endpoints."""
    result = subprocess.run(
        ["k6", "run", "--out", "json=results.json", "load_tests/critical_paths.js"],
        capture_output=True, text=True,
    )
    with open("results.json") as f:
        metrics = json.load(f)

    p99 = metrics["metrics"]["http_req_duration"]["values"]["p(99)"]
    assert p99 < 500, f"P99 latency {p99}ms exceeds 500ms budget"

def test_unit_test_execution_time():
    """Unit tests must complete in under 10 seconds."""
    result = subprocess.run(
        ["pytest", "tests/unit/", "--timeout=10", "-q"],
        capture_output=True, text=True, timeout=15,
    )
    assert result.returncode == 0, "Unit tests exceeded 10-second budget"
```

### Putting It All Together: CI Pipeline

```yaml
# .github/workflows/quality.yml
name: Quality Gates
on: [pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Unit tests + coverage
        run: |
          pytest tests/unit/ --cov=src --cov-report=xml
          coverage report --fail-under=80

      - name: Architecture fitness functions
        run: pytest fitness/ -v

      - name: Security checks
        run: |
          detect-secrets scan --baseline .secrets.baseline
          trivy fs --severity HIGH,CRITICAL --exit-code 1 .

      - name: Schema compatibility
        run: oasdiff breaking --base origin/main:openapi.yaml --revision HEAD:openapi.yaml --fail-on ERR

      - name: Contract tests
        run: pytest tests/contract/ -v

      - name: Integration tests
        run: pytest tests/integration/ -v
        services:
          postgres:
            image: postgres:16
          redis:
            image: redis:7
```

---

## Quick Reference Card

| Decision | Default | Deviate When |
|----------|---------|-------------|
| Architecture | Modular monolith + hexagonal | All 4 extraction criteria met |
| Communication | Sync (HTTP/gRPC) | Event ordering or decoupling needed -> async |
| Database | Single shared DB, schema-per-module | Regulatory isolation or independent scaling needed |
| API style | REST + OpenAPI | High-throughput internal -> gRPC; real-time -> WebSocket/SSE |
| Auth | OAuth2/OIDC + JWT | Machine-to-machine -> mTLS |
| Observability | OpenTelemetry + structured logs | Never deviate |
| Testing | Pyramid (unit-heavy) | Never deviate |
| Deployment | Canary with auto-rollback | Simple internal tools -> blue-green |
| IaC | Terraform/Pulumi | Never deviate from IaC; tool choice is flexible |
| Secrets | Vault / cloud KMS | Never store in code, env vars as last resort |

---

*This playbook is a living document. When a principle, pattern, or threshold proves wrong in practice, write an ADR, update this reference, and add a fitness function to enforce the change.*
