# Architecture Review Framework (ATAM-Lite)

## Overview

### What is ATAM?

The Architecture Tradeoff Analysis Method (ATAM) is a structured technique developed by the Software Engineering Institute (SEI) at Carnegie Mellon University for evaluating software architectures against quality attribute requirements. ATAM's core insight is that architectural decisions are fundamentally about tradeoffs: improving one quality attribute (e.g., performance) often comes at the cost of another (e.g., modifiability). By making these tradeoffs explicit and analyzing them against concrete scenarios, teams can identify risks before they become costly defects in production.

A traditional ATAM evaluation involves 15-20 participants over 3-4 days, with a formal presentation structure, external evaluators, and extensive documentation. This level of ceremony is appropriate for safety-critical systems, large government contracts, or organizations with dedicated architecture review boards. For most modern software teams, it is impractical.

### Why "Lite"?

This ATAM-Lite adaptation preserves the core analytical rigor of ATAM -- scenario-based evaluation, sensitivity and tradeoff identification, and risk classification -- while reducing the ceremony, participant count, and time investment to fit the cadence of modern development teams. The full process fits within a single 2-4 hour session with 2-5 participants.

Key adaptations from traditional ATAM:

- **Smaller group**: 2-5 reviewers instead of 15-20. Everyone is a direct contributor to the system.
- **Shorter time-box**: 2-4 hours instead of 3-4 days. Can be split across two sessions if needed.
- **Informal presentation**: Architecture is presented from existing artifacts (diagrams, ADRs, dashboards), not a formal slide deck.
- **Integrated follow-up**: Risks feed directly into the backlog as prioritized action items, not a separate report that lives on a shelf.
- **Repeatable cadence**: Designed to be run quarterly, not as a one-time evaluation event.

### When to Use

Run an ATAM-Lite review in these situations:

- **Before a major release**: Validate that the architecture supports the new capabilities and expected load.
- **Quarterly cadence**: Regular health checks catch architectural drift before it becomes technical debt.
- **After a significant incident**: Post-mortems reveal operational risks. An architecture review identifies whether the root cause points to structural issues.
- **Before a major migration**: Moving to a new cloud provider, database, or framework. Evaluate the target architecture before committing.
- **When the team has grown significantly**: New team members bring different assumptions. A review re-establishes shared understanding.
- **When performance or reliability has degraded**: Symptoms in production may point to architectural problems that cannot be fixed with code-level optimizations.

---

## Phase 1: Preparation (Before the Session)

Preparation determines whether the review session will be productive or an unfocused conversation. Invest 1-2 hours in preparation before the session.

### Identify Reviewers (2-5 People)

Select reviewers who bring diverse perspectives on the system:

| Role | Perspective | Why Included |
|------|------------|--------------|
| **Architect / Tech Lead** | Structural vision, decision history | Knows why decisions were made; can explain tradeoffs |
| **Senior Developer** | Implementation reality, code-level constraints | Knows where the architecture diagram diverges from the code |
| **Operations / SRE** | Deployment, monitoring, incident response | Knows where the system breaks and what is painful to operate |
| **Security Engineer** | Threat landscape, compliance requirements | Identifies attack surfaces and regulatory constraints |
| **Product Owner / PM** | Business drivers, upcoming roadmap | Ensures the review is grounded in actual business needs |

Not every review needs all five roles. At minimum, include the architect and one person from a different discipline (ops or security). The key is that no single perspective dominates.

### Gather Artifacts

Collect these artifacts before the session so reviewers can prepare:

- **Architecture diagrams**: C4 model Level 1 (Context) and Level 2 (Container) at minimum. Level 3 (Component) for the subsystem under review if applicable.
- **ADR log**: All accepted ADRs, especially those related to the review scope.
- **Deployment configuration**: Infrastructure-as-code files (Terraform, Helm charts, docker-compose), CI/CD pipeline definitions.
- **Monitoring dashboards**: Current SLO/SLI dashboards, error rate trends, latency distributions, resource utilization.
- **Dependency inventory**: List of external dependencies (APIs, databases, third-party services) with their SLAs.
- **Recent incident reports**: Post-mortems from the last quarter.
- **Roadmap summary**: Upcoming features or changes that may stress the architecture.

### Define Review Scope

A review can cover the full system or focus on a specific subsystem. Scoping is critical for time-boxing. Examples of well-scoped reviews:

- "Review the order processing pipeline from API ingestion through payment completion."
- "Evaluate the authentication and authorization architecture across all services."
- "Assess the data pipeline from ingestion through the analytics dashboard."
- "Full system review with emphasis on scalability for the upcoming product launch."

Write the scope statement in a single sentence and share it with reviewers in advance.

### Time-Box

The full ATAM-Lite session should take 2-4 hours:

| Phase | Duration | Notes |
|-------|----------|-------|
| Architecture Presentation | 30 min | Presenter + Q&A |
| Scenario Generation | 30 min | Individual writing + group consolidation |
| Scenario Prioritization | 15 min | Dot voting |
| Architecture Analysis | 60-90 min | Trace scenarios through architecture |
| Risk Assessment | 20 min | Classify and prioritize |
| Report Drafting | 15-30 min | Capture findings while fresh |
| **Total** | **2.5-4 hours** | |

For teams that struggle with a single long session, split into two sessions: Phases 1-3 in the first session, Phases 4-6 in the second.

---

## Phase 2: Architecture Presentation (30 Minutes)

The architect or tech lead presents the system to establish a shared mental model. Even if all reviewers work on the system daily, this step is important because it forces alignment on how the architecture is described and understood.

### Presentation Structure

**1. Business Context and Drivers (5 min)**

What does this system do? Who are the users? What are the key business metrics? What is changing in the business that motivates this review?

Example: "We are a B2B SaaS platform for inventory management. Our largest customer just signed a contract for 500 warehouse locations, up from our current maximum of 50. We need to evaluate whether our architecture can support this 10x growth."

**2. Quality Attribute Requirements (10 min)**

List the top 5-7 quality attributes that matter most, with measurable targets:

| Quality Attribute | Requirement | Current State |
|-------------------|------------|---------------|
| Performance | P99 API latency < 200ms | P99 = 180ms (close to limit) |
| Availability | 99.9% uptime (8.7h downtime/year) | 99.85% last quarter |
| Scalability | Support 10K concurrent users | Currently tested to 2K |
| Security | SOC 2 Type II compliance | Audit scheduled Q3 |
| Modifiability | New integration in < 2 weeks | Last integration took 6 weeks |
| Observability | MTTD < 5 min, MTTR < 30 min | MTTD ~15 min currently |
| Cost efficiency | Infrastructure < 15% of revenue | Currently 12% |

**3. Architecture Overview (10 min)**

Walk through the C4 Level 1 (Context) and Level 2 (Container) diagrams. Identify:

- Major components and their responsibilities
- Communication paths (synchronous, asynchronous, batch)
- Data stores and their roles
- External dependencies and integration points
- Deployment topology (regions, availability zones, clusters)

**4. Key Technology Decisions (5 min)**

Summarize the most significant ADRs and any decisions that are currently under debate. Highlight any decisions that reviewers should probe during analysis.

---

## Phase 3: Quality Attribute Scenario Generation

Scenarios are the core analytical tool of ATAM. A scenario describes a concrete situation that the system must handle, expressed in a way that can be traced through the architecture.

### Scenario Format

Each scenario follows a six-part structure:

| Element | Description | Example |
|---------|------------|---------|
| **Source** | Who or what triggers the stimulus | External user, internal service, attacker, time-based scheduler |
| **Stimulus** | The event or condition | 5,000 simultaneous API requests, database failover, security scan, new feature request |
| **Artifact** | The part of the system being stimulated | API gateway, order service, payment database, CI/CD pipeline |
| **Environment** | The conditions under which it occurs | Normal operation, peak load, partial outage, during deployment |
| **Response** | What the system should do | Process requests, failover transparently, reject unauthorized access, deploy without downtime |
| **Measure** | How success is quantified | P99 < 200ms, failover in < 30s, zero data exposure, zero-downtime deployment |

### Example Scenarios by Quality Attribute

**Performance**
"During a Black Friday peak (Source: 10K concurrent users), when the product catalog API receives 50K requests/minute (Stimulus) against the catalog service and its PostgreSQL database (Artifact) under peak load conditions (Environment), the system responds with complete product data (Response) with P99 latency under 300ms and zero dropped requests (Measure)."

**Availability**
"When the primary database instance crashes unexpectedly (Source: infrastructure failure, Stimulus: primary node loss) affecting the order processing service (Artifact) during normal business hours (Environment), the system fails over to the read replica (Response) within 30 seconds with zero data loss and no user-visible errors (Measure)."

**Security**
"When an attacker submits a crafted JWT token with a manipulated role claim (Source: malicious actor, Stimulus: forged credential) against the API gateway (Artifact) during normal operation (Environment), the system rejects the request and logs the attempt with full request metadata (Response) with zero unauthorized data access and alert generated within 60 seconds (Measure)."

**Modifiability**
"When the product team requests integration with a new third-party shipping provider (Source: product requirement, Stimulus: new integration) affecting the shipping service (Artifact) during normal development (Environment), the team implements and deploys the integration (Response) within 10 developer-days without modifying any other service (Measure)."

**Scalability**
"When the customer base grows from 1K to 10K active tenants over 6 months (Source: business growth, Stimulus: 10x tenant increase) affecting the entire platform (Artifact) during normal operation (Environment), the system scales horizontally without architectural changes (Response) with per-tenant cost increasing by no more than 10% and no degradation in P99 latency (Measure)."

### Scenario Generation Process

1. Each reviewer independently writes 3-5 scenarios (10 minutes of silent writing).
2. Each reviewer reads their scenarios aloud. The facilitator captures them on a shared list, merging duplicates (15 minutes).
3. Clarify any ambiguous scenarios. Ensure each has all six elements (5 minutes).

### Prioritization via Dot Voting

Each reviewer receives 5 votes (dots). They distribute votes across the scenarios they consider most important to analyze. Votes can be concentrated (all 5 on one scenario) or distributed. Tally the votes and select the top 8-10 scenarios for analysis.

Record the prioritized list:

| Rank | Scenario | Votes | Quality Attribute |
|------|----------|-------|-------------------|
| 1 | 10x tenant scaling | 12 | Scalability |
| 2 | Primary DB failover | 10 | Availability |
| 3 | Black Friday peak load | 8 | Performance |
| ... | ... | ... | ... |

---

## Phase 4: Architecture Analysis

This is the core of the review. For each prioritized scenario, the group traces the stimulus through the architecture and identifies sensitivity points, tradeoff points, risks, and non-risks.

### Analysis Process (Per Scenario)

**Step 1: Trace Through the Architecture (5 min)**

Starting from the stimulus source, walk through every component, communication path, and data store involved in handling the scenario. Draw the path on the architecture diagram. Identify:

- Which components are on the critical path?
- Where does data flow? What transformations occur?
- What are the failure modes at each step?
- Where are the synchronous bottlenecks?

**Step 2: Identify Sensitivity Points (3 min)**

A sensitivity point is a property of a component or connection where a small change has a disproportionately large effect on a quality attribute.

Examples:
- "The database connection pool size is a sensitivity point for performance. Changing it from 20 to 50 connections could double throughput, but setting it to 200 could overwhelm the database."
- "The retry count on the payment gateway call is a sensitivity point for both availability and cost. Too few retries cause failed orders; too many retries cause duplicate charges."

**Step 3: Identify Tradeoff Points (3 min)**

A tradeoff point is an architectural decision where improving one quality attribute necessarily degrades another.

Examples:
- "Adding a caching layer in front of the product catalog improves performance but reduces consistency (stale data) and increases modifiability cost (cache invalidation logic)."
- "Encrypting all inter-service communication improves security but increases latency by 5-10ms per hop and complicates debugging."

**Step 4: Identify Risks (3 min)**

A risk is an architectural decision or property that may prevent the system from achieving a quality attribute goal under the given scenario.

Examples:
- "RISK: The system uses a single PostgreSQL instance with no read replicas. Under the 10x scaling scenario, the database will become the bottleneck and there is no horizontal scaling path without re-architecture."
- "RISK: Session state is stored in-memory on application servers. Under the failover scenario, all active sessions will be lost when a server goes down."

**Step 5: Identify Non-Risks (2 min)**

A non-risk is an architectural decision that is well-supported and does not pose a concern for the given scenario. Documenting non-risks is important because it prevents re-analysis of the same areas in future reviews and acknowledges good decisions.

Examples:
- "NON-RISK: The API gateway handles TLS termination and rate limiting. This is well-configured with automated certificate rotation and per-tenant rate limits."
- "NON-RISK: The CI/CD pipeline includes automated rollback on health check failure. Deployment risk is well-mitigated."

### Analysis Recording Template

Use this table to capture findings for each scenario:

| Scenario | Components Involved | Sensitivity Points | Tradeoff Points | Risks | Non-Risks | Rating |
|----------|--------------------|--------------------|-----------------|-------|-----------|--------|
| 10x tenant scaling | API GW, Auth, All services, PostgreSQL, Redis | DB connection pool size; cache TTL | Caching (perf vs. consistency); shared vs. per-tenant DB (cost vs. isolation) | Single DB instance, no sharding strategy; no load testing beyond 2K users | Rate limiting is per-tenant and well-configured; stateless services scale horizontally | HIGH |
| Primary DB failover | PostgreSQL, Order Service, Payment Service | Replication lag threshold; health check interval | Sync vs. async replication (consistency vs. failover speed) | No automated failover configured; application does not retry on connection loss | Backups run hourly with verified restores | CRITICAL |

---

## Phase 5: Risk Assessment

After analyzing all prioritized scenarios, consolidate the risks into a single list and classify each by severity.

### Risk Severity Levels

| Severity | Criteria | Response Timeline |
|----------|---------|-------------------|
| **CRITICAL** | Architectural flaw that could cause system failure, data loss, or security breach under expected operating conditions. The system cannot reliably serve its core function. | Immediate action required. Block the next release if applicable. Begin remediation within 48 hours. |
| **HIGH** | Significant issue that will cause problems under expected load, growth, or usage patterns within the next 6 months. The system functions today but is on a path toward failure. | Action within 1 sprint. Prioritize above feature work. |
| **MEDIUM** | Issue that limits the system's ability to evolve, increases maintenance cost, or creates operational burden. The system functions and will continue to function, but at increasing cost. | Address within the next quarter. Include in planning. |
| **LOW** | Minor concern or improvement opportunity. The system is not at risk, but could be better. | Add to backlog. Address opportunistically or during refactoring efforts. |

### Risk Consolidation

Merge related risks from different scenarios. A risk identified in multiple scenarios is likely more severe than one found in a single scenario.

| Risk ID | Description | Scenarios Affected | Severity | Mitigation Recommendation |
|---------|------------|-------------------|----------|--------------------------|
| R1 | Single PostgreSQL instance with no failover or horizontal scaling | Scaling, Failover, Peak Load | CRITICAL | Implement read replicas, configure automated failover (Patroni or RDS Multi-AZ), evaluate sharding strategy |
| R2 | No load testing beyond 2K concurrent users | Scaling, Peak Load | HIGH | Establish load testing pipeline, run monthly with production-like data volume |
| R3 | In-memory session state on application servers | Failover | HIGH | Migrate session state to Redis with TTL-based expiration |
| R4 | Cache invalidation is manual/ad-hoc | Modifiability, Consistency | MEDIUM | Implement event-driven cache invalidation tied to data change events |

---

## Phase 6: Report Generation

Capture the review findings in a structured report while the discussion is fresh. The report serves as a reference for the team, input for sprint planning, and a baseline for the next review.

### Architecture Review Report Template

```markdown
# Architecture Review Report

## 1. Executive Summary

**Review Date**: YYYY-MM-DD
**Review Scope**: [scope statement]
**Participants**: [names and roles]
**Overall Health Rating**: [CRITICAL | CONCERNING | FAIR | GOOD | EXCELLENT]

### Key Findings
1. [Most important finding — 1 sentence]
2. [Second finding]
3. [Third finding]
4. [Fourth finding, if applicable]
5. [Fifth finding, if applicable]

### Immediate Actions Required
- [Action 1, if any CRITICAL risks exist]
- [Action 2]

---

## 2. System Overview

[2-3 paragraph description of the system architecture as presented
during the review. Include or reference the C4 diagrams.]

---

## 3. Quality Attribute Scenarios

### Prioritized Scenarios

| Rank | Scenario | Quality Attribute | Rating |
|------|----------|-------------------|--------|
| 1 | [scenario summary] | [QA] | [CRITICAL/HIGH/MEDIUM/LOW] |
| 2 | ... | ... | ... |

### Scenario Details

#### Scenario 1: [Title]
- **Full Description**: [six-part scenario]
- **Analysis**: [summary of trace-through findings]
- **Rating**: [rating with justification]

[Repeat for each scenario]

---

## 4. Sensitivity Points

| ID | Description | Affected QAs | Current Setting | Recommendation |
|----|------------|-------------|-----------------|----------------|
| S1 | DB connection pool size | Performance, Scalability | 20 connections | Load test to find optimal; consider dynamic sizing |
| S2 | ... | ... | ... | ... |

---

## 5. Tradeoff Points

| ID | Description | QA Improved | QA Degraded | Current Balance | Notes |
|----|------------|------------|------------|-----------------|-------|
| T1 | Caching layer | Performance | Consistency | 60s TTL | Consider event-driven invalidation |
| T2 | ... | ... | ... | ... | ... |

---

## 6. Risks

### Critical
| ID | Description | Scenarios | Mitigation | Owner | Target Date |
|----|------------|-----------|------------|-------|-------------|
| R1 | [description] | [list] | [recommendation] | [name] | [date] |

### High
| ID | Description | Scenarios | Mitigation | Owner | Target Date |
|----|------------|-----------|------------|-------|-------------|

### Medium
| ID | Description | Scenarios | Mitigation | Owner | Target Date |
|----|------------|-----------|------------|-------|-------------|

### Low
| ID | Description | Scenarios | Mitigation | Owner | Target Date |
|----|------------|-----------|------------|-------|-------------|

---

## 7. Non-Risks

[List architectural decisions that are well-supported. This section
is important for acknowledging good work and preventing unnecessary
re-evaluation in future reviews.]

| ID | Description | Scenarios | Why It Works |
|----|------------|-----------|-------------|
| NR1 | Rate limiting per tenant | Scaling, Security | Well-configured, tested, monitored |
| NR2 | ... | ... | ... |

---

## 8. Recommendations

### Immediate (This Sprint)
1. [Action item tied to CRITICAL risk]
2. [Action item tied to CRITICAL risk]

### Short-Term (This Quarter)
1. [Action item tied to HIGH risk]
2. [Action item tied to HIGH risk]

### Medium-Term (Next Quarter)
1. [Action item tied to MEDIUM risk]

### Long-Term (6+ Months)
1. [Action item tied to LOW risk or strategic improvement]

---

## Appendix
- [Link to architecture diagrams]
- [Link to ADR log]
- [Link to monitoring dashboards]
- [Link to previous review report for comparison]
```

---

## Health Scoring Rubric

The overall health rating provides a single-glance summary of the architecture's condition. It is derived from the risk assessment, not from subjective impression.

| Rating | Criteria | Typical Action |
|--------|---------|----------------|
| **CRITICAL** | One or more CRITICAL risks identified. The system is at risk of failure, data loss, or security breach under expected operating conditions. | Stop feature work. Remediate immediately. Escalate to leadership. |
| **CONCERNING** | No CRITICAL risks, but two or more HIGH risks identified. The system functions today but is on a trajectory toward significant problems. | Dedicate the next sprint primarily to risk mitigation. Defer non-essential feature work. |
| **FAIR** | At most one HIGH risk and/or multiple MEDIUM risks. The system is functional and stable but has known limitations that constrain its evolution. | Address risks as part of normal quarterly planning. No emergency action needed. |
| **GOOD** | No HIGH risks. A small number of MEDIUM or LOW risks. The architecture is sound and supports current needs with minor improvement opportunities. | Continue normal development. Address LOW risks opportunistically. |
| **EXCELLENT** | No risks above LOW severity. The architecture supports current requirements and has clear headroom for anticipated growth. Non-risks significantly outnumber risks. | Maintain current practices. Focus the next review on emerging requirements. |

### Scoring Formula

Apply these rules in order. The first matching rule determines the rating:

1. If **any** risk is rated CRITICAL, the overall health is **CRITICAL**.
2. If **2 or more** risks are rated HIGH, the overall health is **CONCERNING**.
3. If **1** risk is rated HIGH, or **3 or more** risks are rated MEDIUM, the overall health is **FAIR**.
4. If **1-2** risks are rated MEDIUM and no HIGH risks, the overall health is **GOOD**.
5. If **all** risks are LOW or no risks are identified, the overall health is **EXCELLENT**.

This formula intentionally skews conservative. A single CRITICAL risk makes the entire system CRITICAL regardless of how many things are working well. This reflects the reality that one architectural flaw can bring down an otherwise excellent system.

---

## Lightweight Review Alternatives

Not every review needs the full ATAM-Lite process. The following lightweight formats are useful for smaller teams, focused concerns, or higher-frequency cadences.

### Architecture Kata (1 Hour)

An architecture kata is a time-boxed design exercise adapted for review purposes.

**Format:**
1. **Present** (15 min): The architect presents the current design for a specific subsystem or upcoming feature.
2. **Challenge** (20 min): Reviewers ask questions, probe assumptions, and suggest alternatives. Focus on "what could go wrong?" and "what are we not considering?"
3. **Iterate** (15 min): The architect revises the design based on feedback, explaining which suggestions they accept and why.
4. **Capture** (10 min): Record the key decisions and any risks identified. Write ADRs for any significant decisions.

**Best for:** Pre-implementation design review, onboarding new architects, evaluating design alternatives before committing.

### Threat Modeling Session (2 Hours)

A focused security review using the STRIDE framework.

**Format:**
1. **Diagram** (20 min): Draw data flow diagrams for the system or subsystem under review. Identify trust boundaries.
2. **STRIDE Analysis** (60 min): For each component and data flow crossing a trust boundary, systematically evaluate:
   - **S**poofing: Can an attacker impersonate a legitimate entity?
   - **T**ampering: Can data be modified in transit or at rest?
   - **R**epudiation: Can actions be performed without accountability?
   - **I**nformation Disclosure: Can sensitive data leak?
   - **D**enial of Service: Can the system be made unavailable?
   - **E**levation of Privilege: Can an attacker gain unauthorized access?
3. **Prioritize** (20 min): Rank threats by likelihood and impact.
4. **Mitigate** (20 min): Identify mitigations for the top threats. Record as risks in the architecture risk log.

**Best for:** Pre-launch security review, compliance preparation, after a security incident.

### Dependency Review (30 Minutes)

A focused review of external and internal dependencies.

**Format:**
1. **Inventory** (10 min): List all external dependencies (third-party APIs, managed services, open-source libraries) and internal service dependencies.
2. **Health Check** (10 min): For each dependency, evaluate:
   - Is the dependency actively maintained?
   - Are there known vulnerabilities (check CVE databases, Dependabot/Snyk alerts)?
   - Is the dependency pinned to a specific version?
   - What is the blast radius if this dependency fails or is compromised?
   - Is there a fallback or alternative?
3. **Action Items** (10 min): Create tickets for any dependencies that need updating, replacing, or isolation.

**Best for:** Weekly automated checks (with manual review of flagged items), supply chain security, pre-upgrade planning.

### SLO Review (1 Hour)

A focused review of Service Level Objectives and their alignment with business needs.

**Format:**
1. **Current SLOs** (10 min): Review existing SLOs and their current achievement levels. Pull data from monitoring dashboards.
2. **SLO Fitness** (20 min): For each SLO, ask:
   - Does this SLO measure what users actually care about?
   - Is the target achievable and meaningful? (An SLO that is always met trivially is not useful.)
   - Is the error budget being consumed at a sustainable rate?
   - Are there user-facing quality attributes that have no SLO coverage?
3. **Gap Analysis** (15 min): Identify missing SLOs, overly lax SLOs, and SLOs that are consistently breached.
4. **Adjustments** (15 min): Propose SLO changes and new SLOs. Ensure each SLO has a clear owner and escalation path when the error budget is exhausted.

**Best for:** Bi-weekly operational review, post-incident follow-up, before capacity planning.

---

## Review Cadence Recommendations

Establish a regular rhythm of reviews at different levels of depth. Consistency matters more than perfection; a mediocre review done quarterly is far more valuable than a perfect review done never.

| Review Type | Frequency | Duration | Participants | Output |
|-------------|-----------|----------|-------------|--------|
| **Full ATAM-Lite** | Quarterly, or before major releases | 2-4 hours | 3-5 (cross-functional) | Full Architecture Review Report |
| **Architecture Kata** | Monthly, or before major features | 1 hour | 2-3 (architect + senior devs) | ADRs + risk notes |
| **Threat Modeling** | Quarterly, or before security-sensitive changes | 2 hours | 2-4 (including security) | Threat register + mitigation plan |
| **Dependency Review** | Weekly (automated) + monthly (manual) | 30 min manual | 1-2 (dev + ops) | Dependency health report |
| **SLO Review** | Bi-weekly | 1 hour | 2-3 (dev + ops + product) | SLO adjustments + action items |

### Scheduling Tips

- **Anchor to existing ceremonies**: Schedule the quarterly ATAM-Lite at the start of each quarter's planning cycle so findings feed directly into prioritization.
- **Rotate the facilitator**: Avoid making architecture review the sole responsibility of one person. Rotating the facilitator builds architectural thinking across the team.
- **Keep a review log**: Track when reviews were conducted, what was covered, and what risks were identified. This log becomes valuable evidence for compliance audits and for tracking whether identified risks were actually addressed.
- **Timebox strictly**: Reviews expand to fill available time. A 2-hour review that stays focused produces better results than a 4-hour review that loses energy.
- **Make it safe**: The review should be a collaborative analysis, not a critique of the architect's work. Frame findings as "the architecture has this risk" not "you made a bad decision." Psychological safety is essential for honest risk identification.

### Tracking Review Outcomes

After each review, track risk mitigation progress:

| Risk ID | Identified | Severity | Owner | Status | Resolved | Notes |
|---------|-----------|----------|-------|--------|----------|-------|
| R1 | 2025-Q1 | CRITICAL | Alice | In Progress | - | Read replicas deployed; failover testing scheduled |
| R2 | 2025-Q1 | HIGH | Bob | Done | 2025-04-15 | Load testing pipeline running monthly |
| R3 | 2025-Q1 | HIGH | Carol | Not Started | - | Blocked by Redis cluster provisioning |

Review this tracking table at the start of each subsequent review to assess progress and re-evaluate risk severity based on new information.
