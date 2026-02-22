# Compliance Standards and Regulatory Reference for Agentic AI Systems

> Reference document for the Agentic AI Requirements skill. Provides standards, regulations,
> and compliance requirements applicable to production agentic AI systems as of February 2026.

---

## NIST AI Risk Management Framework (AI RMF 1.0)

The NIST AI RMF provides the most comprehensive risk management structure for AI systems.
AI-600-1 (GenAI Profile) extends it specifically to generative AI and agentic systems.

### Four Core Functions Applied to Agentic Systems

#### 1. GOVERN -- Policies, Roles, and Accountability

Establishes organizational governance for AI systems. For agentic systems, this means:

- **Board-level oversight**: Who is accountable for the agent system's behavior?
- **Risk appetite definition**: What level of autonomous action is acceptable?
- **Policy framework**: Written policies for agent development, deployment, and operation
- **Role assignment**: Who owns prompts, evaluations, incident response, and compliance?
- **Third-party management**: Governance of LLM providers, tool services, and data processors

Maps to framework requirements: G-1 (audit logging), G-2 (regulatory mapping), G-4 (access controls), G-5 (incident response), G-6 (formal risk assessment), G-7 (runtime policy enforcement).

#### 2. MAP -- Context and Risk Identification

Identifies the system's context, stakeholders, and potential harms:

- **Use case documentation**: What the system does, for whom, and in what context
- **Stakeholder identification**: Users, affected parties, operators, regulators
- **Potential harms analysis**: What can go wrong? Who is harmed? How severely?
- **Data lineage tracking**: What data enters the system, where it goes, how it is processed
- **Threat modeling**: Attack surface analysis specific to agentic systems

Maps to: ET-1 (decision scope documentation), ET-2 (transparency), ET-5 (societal impact), DOC-1 (README with purpose and architecture).

#### 3. MEASURE -- Testing, Evaluation, and Monitoring

Quantitative and qualitative assessment of AI system performance:

- **Bias metrics**: Statistical measures of disparate impact across user groups
- **Accuracy metrics**: Task completion rates, trajectory quality, reasoning quality
- **Safety metrics**: Input/output validation failure rates, guardrail trigger rates
- **Robustness metrics**: Performance under adversarial inputs, edge cases, distribution shift
- **Continuous monitoring**: Drift detection, quality degradation alerting

Maps to: E-1 through E-8 (evaluation requirements), O-1 through O-7 (observability requirements).

#### 4. MANAGE -- Risk Treatment, Monitoring, and Improvement

Active management of identified risks throughout the system lifecycle:

- **Risk treatment**: Accept, mitigate, transfer, or avoid each identified risk
- **Incident response**: Detection, classification, response, recovery, post-mortem
- **Model lifecycle management**: Version control, A/B testing, rollback capability
- **Continuous improvement**: Feedback loops from production to development
- **Regulatory compliance**: Ongoing demonstration of compliance

Maps to: D-1 through D-7 (deployment requirements), S-1 through S-8 (safety requirements), G-5 (incident response).

---

## EU AI Act -- Timeline and Obligations

The EU AI Act is the world's first comprehensive AI regulation. Its phased enforcement
timeline directly affects agentic AI system development.

### Enforcement Timeline

| Date | Milestone | Impact on Agent Systems |
|------|-----------|------------------------|
| **Feb 2025** | AI literacy + banned practices provisions | Organizations must ensure AI literacy for staff. Banned: social scoring, real-time biometric ID, subliminal manipulation. |
| **Aug 2025** | Governance rules, GPAI model obligations | General-purpose AI models must meet transparency requirements. Governance bodies operational. |
| **Aug 2026** | Full enforcement | Transparency requirements, conformity assessments, penalties for non-compliance. High-risk system obligations fully enforceable. |
| **Aug 2027** | Full obligations for high-risk AI in regulated products | AI embedded in regulated products (medical devices, vehicles, financial systems) must meet all requirements. |

### Agent-Specific Obligations

**Transparency (Article 50):**
- Users must know they are interacting with an AI system
- AI-generated content must be labeled as such
- Deepfakes must be disclosed
- For agents: every user-facing interaction must clearly indicate AI involvement

**Technical Documentation (Article 11, Annex IV):**
- Description of the AI system and its intended purpose
- Data governance and data management practices
- Design specifications and development methodology
- Risk management system and risk assessment results
- Monitoring, functioning, and control of the AI system

**Human Oversight (Article 14):**
- High-risk AI systems must include human oversight mechanisms
- Humans must be able to understand, interpret, and override AI decisions
- For agents: HITL checkpoints, approval gates, kill switches

**Data Governance (Article 10):**
- Training data must be documented
- Bias mitigation measures must be implemented
- Data quality criteria must be defined and monitored
- For agents: document what data enters prompts, what reaches LLM providers

**Registration (Article 49):**
- High-risk AI systems must be registered in the EU database
- Registration before placing on market or putting into service

**Penalties (Article 99):**
- Up to 35 million EUR or 7% of total worldwide annual turnover
- Graduated by infringement severity
- Banned practices: up to 35M EUR / 7%
- Non-compliance with other provisions: up to 15M EUR / 3%
- Incorrect information to authorities: up to 7.5M EUR / 1.5%

### Risk Classification for Agent Systems

| Risk Level | Description | Agent Examples |
|------------|-------------|----------------|
| **Unacceptable** | Banned practices | Social scoring agents, subliminal manipulation |
| **High-risk** | Significant impact on health, safety, fundamental rights | Hiring agents, credit scoring, medical triage, law enforcement |
| **Limited risk** | Transparency obligations | Customer service chatbots, content generators |
| **Minimal risk** | No specific obligations | Internal tooling agents, development assistants |

---

## Audit Logging Requirements

Drawn from HIPAA, SOX, GDPR, PCI-DSS, and general compliance best practices.

### What to Log for Agent Systems

Every log entry should capture:

| Field | Description | Example |
|-------|-------------|---------|
| `timestamp` | ISO 8601 with timezone | `2026-02-22T14:30:00Z` |
| `trace_id` | End-to-end request correlation | `a1b2c3d4-e5f6-7890` |
| `span_id` | Individual operation within trace | `x1y2z3` |
| `agent_name` | Which agent performed the action | `security_agent` |
| `action` | What was done | `analyze_feature`, `call_tool`, `create_issue` |
| `input_summary` | Truncated/redacted input | `Feature: OAuth integration (523 chars)` |
| `output_summary` | Truncated/redacted output | `3 concerns, risk=HIGH, review=yes` |
| `model` | LLM model used | `gpt-4o-mini` |
| `tokens_in` | Input token count | `1,240` |
| `tokens_out` | Output token count | `890` |
| `latency_ms` | Operation duration | `2,340` |
| `status` | Success/failure | `success`, `error`, `timeout` |
| `error_type` | If failed, classification | `rate_limit`, `validation_error` |
| `user_id` | Who triggered the request | `github:user123` (if applicable) |
| `tool_calls` | Tools invoked during this step | `[create_github_issue]` |

### Log Events Specific to Agent Systems

- All agent decisions (which path taken, which tools selected)
- All tool calls with parameters (redacted if sensitive)
- All state changes (memory writes, session updates)
- All errors, retries, and fallback activations
- All human interventions (approvals, overrides, escalations)
- All data access (what data was read, from where)
- All external API calls (provider, endpoint, response code)
- Guardrail activations (what was blocked and why)

### Retention Requirements by Regulation

| Regulation | Minimum Retention | Scope |
|------------|------------------|-------|
| **HIPAA** | 6 years | Health-related agent decisions |
| **SOX** | 7 years | Financial reporting, audit trails |
| **GDPR** | Only as long as necessary | Must justify retention period; right to erasure applies |
| **PCI-DSS** | 1 year (readily available) | Payment card data processing |
| **EU AI Act** | Duration of system lifecycle + 10 years for high-risk | Technical documentation, conformity records |
| **SOC 2** | Per trust service criteria | Security, availability, processing integrity |

### Log Integrity Requirements

- **Immutability**: Append-only storage; logs cannot be modified or deleted by operators
- **Cryptographic verification**: Hash chains or Merkle trees to detect tampering
- **Access control**: Separation of duties -- system operators should not be able to modify audit logs
- **Backup**: Logs stored in geographically separate locations
- **Encryption**: Logs encrypted at rest and in transit

### Log Format Standard

Use structured JSON logging with consistent field names:

```json
{
  "timestamp": "2026-02-22T14:30:00.123Z",
  "level": "INFO",
  "trace_id": "a1b2c3d4-e5f6-7890",
  "span_id": "x1y2z3",
  "agent": "security_agent",
  "action": "analyze_feature",
  "input_chars": 523,
  "output": {"concerns": 3, "risk": "HIGH", "review": true},
  "model": "gpt-4o-mini",
  "tokens": {"input": 1240, "output": 890},
  "latency_ms": 2340,
  "status": "success"
}
```

---

## Protocol Standards for Agent Interoperability

### MCP (Model Context Protocol)

- **Origin**: Anthropic (November 2024). Donated to Agentic AI Foundation (AAIF) under Linux Foundation (December 2025).
- **Specification**: 2025-11-25 revision (one-year anniversary release)
- **Architecture**: Client-server, JSON-RPC 2.0
- **Ecosystem**: 5,800+ servers, 300+ clients, 8M+ downloads
- **Adoption**: OpenAI (March 2025), Google DeepMind, GitHub, Microsoft (Build 2025)
- **Purpose**: Secure tool invocation, typed data exchange between agents and external services
- **Compliance relevance**: Standardized tool interface simplifies audit logging, access control, and security review. All tool calls through MCP have consistent schema, making compliance monitoring tractable.

### A2A (Agent-to-Agent Protocol)

- **Origin**: Google (April 2025). Donated to Linux Foundation (June 2025).
- **Specification**: v0.3 (July 2025) added gRPC support, signed security cards
- **Architecture**: Peer-to-peer, Agent Cards for capability discovery
- **Ecosystem**: 150+ supporting organizations (Atlassian, Salesforce, SAP, PayPal)
- **Status**: Pre-1.0 as of February 2026; development pace has slowed relative to MCP
- **Purpose**: Cross-system agent communication, task outsourcing between organizational boundaries
- **Compliance relevance**: Agent Cards provide machine-readable capability declarations, supporting transparency and accountability requirements.

### ACP (Agent Communication Protocol)

- **Origin**: BeeAI (IBM)
- **Architecture**: REST-native, multi-part messages, async streaming
- **Status**: Emerging; less adoption than MCP or A2A
- **Purpose**: Asynchronous agent messaging with rich media support

### ANP (Agent Network Protocol)

- **Architecture**: W3C-style, decentralized identifiers, JSON-LD semantic graphs
- **Status**: Very early stage
- **Purpose**: Open-network agent discovery and communication with verifiable identities

### Protocol Selection Guidance

| Use Case | Recommended Protocol |
|----------|---------------------|
| Tool/service integration | MCP |
| Cross-organization agent communication | A2A |
| Async messaging with streaming | ACP |
| Decentralized agent networks | ANP |
| Internal same-framework agents | Framework-native (LangGraph state, CrewAI Flows) |

---

## Data Privacy Controls for Agent Systems

### PII Detection and Masking

- Scan all agent inputs for PII before passing to LLM providers
- Scan all agent outputs for PII before returning to users or logging
- Categories: names, emails, phone numbers, SSNs, credit cards, addresses, health data
- Tools: Guardrails AI PII validator, Presidio (Microsoft), custom regex + NER models
- Implementation: Pre-processing pipeline before LLM call, post-processing before storage/output

### Data Minimization

- Agents should access only the data they need for the current task
- Do not pass entire databases, full conversation histories, or unfiltered search results
- Implement context windowing: summarize or truncate older data
- Document what data each agent requires and enforce access boundaries

### Right to Erasure (GDPR Article 17)

- Ability to delete all data associated with a specific user from:
  - Agent memory stores (Mem0, vector databases, session storage)
  - Conversation logs and audit trails (with regulatory retention exceptions)
  - Cached responses and embeddings
- Implementation: User ID tagging on all stored data, deletion API endpoint

### Cross-Border Data Transfer

- Know where your LLM provider processes data (OpenAI: US; Anthropic: US/UK; Google: varies)
- EU data processed by US providers requires Standard Contractual Clauses (SCCs) or adequacy decisions
- Consider: self-hosted models (Ollama, vLLM) for data sovereignty requirements
- Document data flows including which external services receive user data

### Consent Management

- If processing personal data, obtain and record consent
- Consent must be: freely given, specific, informed, unambiguous
- Provide mechanism to withdraw consent
- For agents: clearly state that user input will be processed by AI and may be sent to third-party providers

---

## Incident Response for AI Agent Systems

### Detection

| Signal | Description | Action |
|--------|-------------|--------|
| Anomalous output | Agent producing unexpected output patterns | Alert + quality check |
| Safety violation | Guardrail triggered, blocked content | Alert + log + review |
| Performance degradation | Latency spike, accuracy drop, cost spike | Alert + investigate |
| Error rate spike | Sudden increase in agent failures | Alert + circuit breaker |
| Adversarial activity | Repeated injection attempts, unusual input patterns | Alert + rate limit + block |

### Classification

| Severity | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **Critical (P0)** | Data breach, safety bypass, regulatory violation | 15 minutes | Agent leaking PII, bypassed guardrails |
| **High (P1)** | System unavailable, significant quality degradation | 1 hour | All agents failing, model provider down |
| **Medium (P2)** | Partial degradation, non-critical feature failure | 4 hours | One agent type failing with fallback active |
| **Low (P3)** | Minor quality issue, cosmetic defect | Next business day | Output formatting regression |

### Response

1. **Automated circuit breakers**: Disable agent or reduce to safe mode after N consecutive failures
2. **Kill switch activation**: Environment variable or feature flag to immediately disable the system
3. **Human escalation**: Notify on-call engineer via PagerDuty/Opsgenie/equivalent
4. **Scope assessment**: Determine how many users/requests were affected
5. **Communication**: Notify affected users if impact is significant

### Recovery

1. **Rollback**: Revert to last known-good agent version (code, prompts, configuration)
2. **Model fallback**: Switch to alternative model provider if primary is the issue
3. **Degraded mode**: Operate with reduced functionality until root cause is resolved
4. **Verification**: Run evaluation suite against restored system to confirm fix

### Post-Mortem

1. **Timeline**: Reconstruct the incident from audit logs and traces
2. **Root cause**: Identify the underlying cause (prompt change, model update, tool failure, attack)
3. **Impact assessment**: Quantify affected users, incorrect outputs, data exposure
4. **Remediation**: Document what was fixed and what preventive measures were implemented
5. **Follow-up**: Track remediation items to completion

### Regulatory Notification

- **EU AI Act**: Serious incidents involving high-risk AI must be reported to market surveillance authorities
- **GDPR**: Data breaches must be reported to supervisory authority within 72 hours
- **HIPAA**: Breaches affecting 500+ individuals must be reported to HHS within 60 days
- **SOX**: Material weaknesses in financial reporting AI must be disclosed

---

## OWASP Top 10 for LLM Applications (2025)

Directly applicable to agentic AI systems:

| Rank | Risk | Agent Relevance |
|------|------|-----------------|
| 1 | **Prompt Injection** | Direct and indirect injection via tool outputs, memory, user input |
| 2 | **Sensitive Information Disclosure** | Agents leaking training data, system prompts, PII |
| 3 | **Supply Chain Vulnerabilities** | Compromised MCP servers, malicious tool packages |
| 4 | **Data and Model Poisoning** | Corrupted memory stores, poisoned RAG documents |
| 5 | **Improper Output Handling** | Agent output used unsanitized in SQL, HTML, shell commands |
| 6 | **Excessive Agency** | Agents with more permissions than needed |
| 7 | **System Prompt Leakage** | System prompts exposed through clever querying (new in 2025) |
| 8 | **Vector and Embedding Weaknesses** | Adversarial embeddings in vector stores |
| 9 | **Misinformation** | Agents producing confident but incorrect information |
| 10 | **Unbounded Consumption** | Runaway agent loops consuming unlimited tokens/compute |

---

## Key Statistics for Compliance Planning (February 2026)

- 77% of enterprises faced GenAI-related security breaches (IBM 2025)
- 39% of companies reported agents accessing unintended systems
- 32% saw agents allowing inappropriate data downloads
- 57.3% of surveyed organizations have agents in production (LangChain report)
- Only 52% have implemented evaluations (vs 89% with observability)
- 23% of enterprises are actually scaling AI agents; 39% stuck in experimentation
- 40% of agentic AI projects fail before reaching production (hidden costs)
