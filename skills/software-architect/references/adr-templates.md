# Architecture Decision Records (ADRs)

## What is an ADR?

An Architecture Decision Record (ADR) is a short document that captures a single architectural decision along with its context, rationale, and consequences. ADRs provide a decision log that explains *why* a system is built the way it is, not just *what* was built.

### Why ADRs Matter

Decisions are the most important architectural artifact a team produces. Code changes over time, diagrams fall out of date, and wiki pages rot, but the reasoning behind structural choices remains critical for every future developer, operator, and stakeholder who inherits the system. Without ADRs, teams repeatedly revisit the same decisions, new members second-guess past choices without understanding the constraints that existed at the time, and institutional knowledge walks out the door every time someone leaves the organization. A well-maintained ADR log eliminates the "why did we do it this way?" conversation and replaces it with a pointer to a numbered document that contains the full context.

### When to Write an ADR

Write an ADR any time you face a decision that meets one or more of these criteria:

- **Hard to reverse**: Choosing a database, adopting a framework, selecting an API paradigm, or picking an authentication mechanism. Once code is built on top of these choices, changing course is expensive.
- **Affects multiple teams or services**: If the decision changes an interface that other teams depend on, it deserves a record so those teams understand the reasoning and can plan accordingly.
- **Involves significant tradeoffs**: When there is no obviously correct answer and you are trading one quality attribute for another (e.g., consistency vs. availability, simplicity vs. flexibility), document which tradeoff you chose and why.
- **Triggers debate**: If the team spent more than 30 minutes discussing a technical choice in a meeting, the outcome should be captured in an ADR so the debate does not repeat itself.
- **Sets a precedent**: If you expect future decisions to reference this one (e.g., "we use event-driven communication between services"), write it down so the precedent is explicit.

---

## MADR 3.0 Full Template

The Markdown Any Decision Record (MADR) 3.0.0 template provides a structured, consistent format that balances thoroughness with ease of authoring. Copy the template below and fill in each section.

```markdown
# [short title -- noun phrase describing the decision]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
YYYY-MM-DD

## Decision Makers
[list everyone involved in the decision]

## Context and Problem Statement
[2-4 sentences describing the problem and why a decision is needed.
Explain the forces at play: business requirements, technical constraints,
team capabilities, timeline pressure, or operational concerns.]

## Decision Drivers
- [driver 1: e.g., "Must support 10K concurrent users"]
- [driver 2: e.g., "Team has deep experience with Python"]
- [driver 3: e.g., "Budget limits us to open-source solutions"]
- ...

## Considered Options
1. [Option 1 title]
2. [Option 2 title]
3. [Option 3 title]

## Decision Outcome
Chosen option: "[Option X]", because [justification in 1-2 sentences
tying back to the decision drivers].

### Consequences
#### Good
- [positive consequence 1]
- [positive consequence 2]
- ...

#### Bad
- [negative consequence 1]
- [negative consequence 2]
- ...

#### Neutral
- [neutral observation that is worth recording]

## Pros and Cons of the Options

### [Option 1]
[Brief description of the option in 1-2 sentences.]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]
- Bad, because [argument d]
- Neutral, because [observation]

### [Option 2]
[Brief description of the option in 1-2 sentences.]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]
- Neutral, because [observation]

### [Option 3]
[Brief description of the option in 1-2 sentences.]

- Good, because [argument a]
- Bad, because [argument b]
- Bad, because [argument c]
- Neutral, because [observation]

## More Information
[Links to related ADRs, RFCs, design docs, meeting notes, benchmarks,
proof-of-concept results, or external references that informed the
decision. If this ADR supersedes a previous one, link to it here.]
```

### Template Usage Notes

- **Title**: Use a noun phrase that reads like a label, not a question. Good: "Use PostgreSQL for Transactional Data". Bad: "Which database should we use?"
- **Decision Makers**: Include names and roles. This creates accountability and gives future readers someone to ask for additional context.
- **Considered Options**: Always include at least three options. If you cannot think of three, you have not explored the solution space enough. One option should always be "Do nothing / keep the status quo" to force an explicit evaluation of the current state.
- **Consequences**: Be honest about the negatives. Every decision has downsides. Listing them upfront builds trust and helps the team plan mitigation strategies. If the "Bad" section is empty, the ADR is incomplete.

---

## Y-Statement Format

The Y-Statement is a condensed, single-sentence format for capturing architectural decisions when a full ADR is not warranted or when you need a quick summary. The format is:

> **"In the context of** [context], **facing** [concern], **we decided for** [option], **to achieve** [quality attribute], **accepting** [tradeoff].**"**

This format works well for lightweight decisions, ADR summaries, or decision tables where brevity matters.

### Example Y-Statements

**1. Database Selection**
"In the context of building a transactional e-commerce platform, facing the need for strong consistency and complex joins across order/inventory/payment data, we decided for PostgreSQL, to achieve data integrity and query flexibility, accepting the operational overhead of managing a relational database and the need to shard manually at scale."

**2. API Style**
"In the context of a mobile-first product with limited bandwidth and varied data needs per screen, facing high payload sizes from our REST API, we decided for GraphQL, to achieve efficient data fetching and reduced over-fetching, accepting the added complexity of schema management, the learning curve for backend engineers, and the loss of HTTP-level caching."

**3. Authentication Mechanism**
"In the context of a multi-tenant SaaS platform with enterprise customers requiring SSO, facing incompatible authentication flows across identity providers, we decided for OIDC with a managed identity provider (Auth0), to achieve standards-compliant SSO with minimal custom code, accepting vendor lock-in and a per-active-user cost that scales with our customer base."

**4. Service Communication**
"In the context of an order processing pipeline where steps must complete reliably even during partial outages, facing tight coupling and cascading failures in our synchronous REST calls between services, we decided for asynchronous messaging via Amazon SQS, to achieve resilience and decoupled deployments, accepting eventual consistency in order status visibility and increased debugging complexity for distributed traces."

**5. Deployment Strategy**
"In the context of a startup with a small ops team deploying twelve microservices, facing manual deployment toil and environment drift across staging and production, we decided for containerized deployment on AWS ECS Fargate, to achieve reproducible builds and zero-server management, accepting higher per-unit compute cost compared to EC2 and limited control over the underlying runtime environment."

---

## ADR Lifecycle Management

### Status Transitions

An ADR moves through a defined lifecycle. Each status indicates where the decision stands:

- **Proposed**: The ADR is under active discussion. It has been drafted but the team has not yet committed to the decision. Reviewers should provide feedback, challenge assumptions, and suggest alternatives. A Proposed ADR should have a clear owner and a target date for resolution.

- **Accepted**: The team has agreed on the decision and implementation is underway or complete. An Accepted ADR should not be edited to change the decision. If the context changes, write a new ADR that supersedes this one.

- **Deprecated**: The decision no longer applies because the feature was removed, the service was decommissioned, or the constraint that drove the decision no longer exists. Add a note explaining why it was deprecated and the date of deprecation.

- **Superseded**: The decision has been replaced by a newer ADR. Add a line reading `Superseded by [ADR-XXX](link)` in the Status section. The new ADR should reference the old one in its "More Information" section, explaining what changed and why.

### Numbering Convention

Use a zero-padded three-digit number followed by a kebab-case title:

```
001-use-postgresql-for-transactional-data.md
002-adopt-graphql-for-mobile-api.md
003-use-oidc-with-auth0.md
004-async-messaging-via-sqs.md
005-containerize-on-ecs-fargate.md
```

Numbers are sequential and never reused. If ADR 003 is superseded by ADR 012, both files remain in the repository. The numbering provides a chronological record of when decisions were made.

### Storage Location

Store ADRs in a dedicated directory within the repository:

```
docs/architecture/decisions/
```

For monorepos with multiple services, consider a per-service structure:

```
services/order-service/docs/adr/
services/payment-service/docs/adr/
docs/architecture/decisions/          # cross-cutting decisions
```

Keep ADRs in version control alongside the code they govern. This ensures that ADRs are reviewed in pull requests, versioned alongside the implementation, and discoverable by anyone working in the repository.

### Maintaining the ADR Log

Create an `index.md` or `README.md` in the decisions directory that lists all ADRs with their status:

```markdown
# Architecture Decision Log

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 001 | Use PostgreSQL for Transactional Data | Accepted | 2025-03-15 |
| 002 | Adopt GraphQL for Mobile API | Accepted | 2025-04-02 |
| 003 | Use OIDC with Auth0 | Superseded by 012 | 2025-04-10 |
```

Update this index whenever an ADR is added or its status changes. Some teams automate this with a script that scans the directory and generates the table.

---

## Common ADR Topics

The following is a non-exhaustive list of architectural decisions that commonly deserve an ADR. Use this as a prompt when onboarding a new project or auditing whether your decision log has gaps.

1. **Architecture style** -- Monolith, modular monolith, microservices, serverless, or event-driven. This is often the first and most consequential decision.
2. **Primary programming language(s)** -- Language choice affects hiring, library ecosystems, performance characteristics, and long-term maintenance.
3. **Database technology selection** -- Relational, document, key-value, graph, time-series, or a combination. Includes decisions about managed vs. self-hosted.
4. **API style** -- REST, GraphQL, gRPC, WebSockets, or a combination. Includes versioning strategy.
5. **Authentication and authorization mechanism** -- Session-based, JWT, OAuth2/OIDC, API keys, mTLS, or a combination. Includes identity provider selection.
6. **Message broker / event streaming platform** -- Kafka, RabbitMQ, SQS, Pub/Sub, NATS, or Redis Streams. Includes decisions about message format and delivery guarantees.
7. **Caching strategy** -- Client-side, CDN, application-level (Redis/Memcached), database query cache. Includes cache invalidation approach.
8. **CI/CD pipeline design** -- Tool selection (GitHub Actions, GitLab CI, Jenkins, CircleCI), branching strategy, deployment gates, and artifact management.
9. **Monitoring and observability stack** -- Metrics (Prometheus, Datadog), logging (ELK, Loki), tracing (Jaeger, Tempo), and alerting strategy.
10. **Error handling strategy** -- Error codes vs. exceptions, error response format, retry policies, circuit breaker configuration, and dead-letter queues.
11. **Testing strategy** -- Unit/integration/e2e test ratios, test frameworks, contract testing, load testing tools, and test data management.
12. **Data serialization format** -- JSON, Protocol Buffers, Avro, MessagePack, or Parquet. Affects API contracts, storage efficiency, and schema evolution.
13. **Service communication pattern** -- Synchronous (HTTP, gRPC) vs. asynchronous (message queues, event streams). Includes choreography vs. orchestration.
14. **Deployment strategy** -- Containers on Kubernetes, serverless functions, VMs, PaaS. Includes blue-green, canary, or rolling deployment patterns.
15. **AI/LLM integration approach** -- Direct API calls, agent framework (LangChain, ADK, Pydantic AI), RAG pipeline design, model selection, prompt management, and guardrails.
16. **Frontend framework** -- React, Vue, Svelte, HTMX, or server-rendered. Includes state management and build tooling.
17. **Data pipeline architecture** -- Batch (Airflow, dbt), streaming (Flink, Spark Streaming), or hybrid. Includes data lake/warehouse selection.
18. **Secret management** -- Vault, AWS Secrets Manager, environment variables, SOPS. Includes rotation strategy.
19. **Multi-tenancy model** -- Shared database, schema-per-tenant, database-per-tenant, or account-per-tenant. Affects isolation, cost, and complexity.
20. **Disaster recovery and backup strategy** -- RPO/RTO targets, backup frequency, failover mechanisms, and geographic redundancy.

---

## ADR Review Checklist

Use this checklist when reviewing a proposed ADR before it moves to Accepted status. Every item should be satisfied.

- [ ] **Context is clear**: A reader unfamiliar with the project can understand the problem from the Context section alone, without needing to ask follow-up questions.
- [ ] **At least 3 options considered**: Including "do nothing / status quo" as an explicit option to force comparison against the current state.
- [ ] **Decision drivers are measurable**: Each driver is specific enough to evaluate options against. "Must be fast" is insufficient; "P99 latency under 200ms for read operations" is measurable.
- [ ] **Consequences include negatives**: No decision is without downsides. If the Bad section is empty, the analysis is incomplete. Honest acknowledgment of tradeoffs builds confidence in the decision.
- [ ] **Pros/cons reference the drivers**: Each pro and con ties back to at least one decision driver, making the evaluation traceable.
- [ ] **Decision outcome links to drivers**: The justification in the Decision Outcome section explicitly references the most important drivers, not just a vague preference.
- [ ] **Related ADRs are linked**: If this decision depends on, refines, or supersedes another ADR, the relationship is documented in the More Information section.
- [ ] **Status is correct**: A new ADR should be Proposed until the team agrees, then moved to Accepted in a follow-up commit.
- [ ] **Date is set**: The date reflects when the decision was made (Accepted), not when the document was first drafted.
- [ ] **Decision makers are listed**: Names and roles are included so future readers know who to contact for additional context.
- [ ] **The title is a noun phrase**: Describes the decision as a label (e.g., "Use PostgreSQL for Transactional Data"), not a question or verb phrase.
- [ ] **The document is concise**: An ADR should be one to two pages. If it is longer, consider splitting it into multiple ADRs or moving detailed analysis into a linked RFC.
