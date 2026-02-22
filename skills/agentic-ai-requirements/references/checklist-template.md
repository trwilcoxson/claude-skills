# Agentic AI System Requirements Checklist v1.0

> Quick-reference scoring checklist for assessing agentic AI systems against the
> enterprise-grade requirements framework. Print this out or use it inline.

## Instructions

Score each requirement using the following scale:

| Symbol | Meaning | Points | Criteria |
|--------|---------|--------|----------|
| MET | Fully implemented and documented | 2 | Evidence exists in code, docs, or config |
| PARTIAL | Partially implemented or undocumented | 1 | Some evidence, but incomplete or informal |
| NOT MET | Not implemented | 0 | No evidence found |
| N/A | Not applicable to this system | -- | Excluded from scoring denominator |

**How to use:** Work through each requirement. Mark your score. Total each category.
Compare against the maturity tiers at the bottom to determine your system's maturity level.

---

## MUST Requirements (30 items, 60 points max)

### 1. Agent Architecture & Design (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| A-1 | Agents defined with explicit persona, instructions, capabilities, constraints | __ /2 |
| A-2 | Single vs multi-agent architecture justified with decision record | __ /2 |
| A-3 | Orchestration pattern selected and documented (supervisor, pipeline, swarm, hybrid) | __ /2 |

**Subtotal: __ /6**

### 2. Reasoning & Decision Logic (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| R-1 | Reasoning pattern selected and documented per agent (CoT, ReAct, Plan-and-Execute) | __ /2 |
| R-2 | Structured output schemas enforced for all agents feeding downstream logic | __ /2 |
| R-3 | Error handling with conservative fallbacks defined for every agent | __ /2 |

**Subtotal: __ /6**

### 3. Memory & State Management (2 items)

| ID | Requirement | Score |
|----|-------------|-------|
| M-1 | Memory architecture documented: what is stored, for how long, by whom | __ /2 |
| M-2 | Input validation and size limits on all stateful data | __ /2 |

**Subtotal: __ /4**

### 4. Tool Use & External Integration (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| T-1 | Every tool defined with typed input/output schemas and descriptions | __ /2 |
| T-2 | Least-privilege tool access enforced per agent (documented tool-agent mapping) | __ /2 |
| T-3 | Injection prevention in all tool calls that invoke external processes | __ /2 |

**Subtotal: __ /6**

### 5. Multi-Agent Coordination (2 items)

| ID | Requirement | Score |
|----|-------------|-------|
| C-1 | Communication topology defined and documented (direct, mediated, broadcast) | __ /2 |
| C-2 | Error isolation between agents (one agent failure does not crash the system) | __ /2 |

**Subtotal: __ /4**

### 6. Evaluation & Testing (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| E-1 | Automated evaluation with 5+ diverse test cases (positive, negative, edge, adversarial, degenerate) | __ /2 |
| E-2 | Task completion evaluated (not just output shape) with deterministic + LLM evaluators | __ /2 |
| E-3 | Pass/fail rates tracked and reported across runs | __ /2 |

**Subtotal: __ /6**

### 7. Observability & Monitoring (1 item)

| ID | Requirement | Score |
|----|-------------|-------|
| O-1 | Structured logging (JSON) for every agent invocation with name, I/O, latency, status | __ /2 |

**Subtotal: __ /2**

### 8. Safety, Security & Guardrails (4 items)

| ID | Requirement | Score |
|----|-------------|-------|
| S-1 | All inputs validated before reaching the LLM (size, format, content) | __ /2 |
| S-2 | All outputs validated before reaching users or external systems | __ /2 |
| S-3 | Least-privilege access for all agents and tools (scoped credentials) | __ /2 |
| S-4 | Secrets loaded from env vars or secret managers, never in code or logs | __ /2 |

**Subtotal: __ /8**

### 9. Ethical & Responsible AI (2 items)

| ID | Requirement | Score |
|----|-------------|-------|
| ET-1 | Decision scope and limitations documented (what the system does and does NOT decide) | __ /2 |
| ET-2 | Transparency for automated decisions (users can understand WHY a decision was made) | __ /2 |

**Subtotal: __ /4**

### 10. Deployment & Operations (2 items)

| ID | Requirement | Score |
|----|-------------|-------|
| D-1 | Deployment architecture documented (where, triggers, scaling, dependencies) | __ /2 |
| D-2 | Environment-based configuration (all env-varying config from env vars, not hardcoded) | __ /2 |

**Subtotal: __ /4**

### 11. Documentation & Reproducibility (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| DOC-1 | README with purpose, architecture, quick start, and CLI reference | __ /2 |
| DOC-2 | All prompts and instructions version-controlled (git) | __ /2 |
| DOC-3 | All dependencies tracked and pinned (requirements.txt, lock files) | __ /2 |

**Subtotal: __ /6**

### 12. Governance & Compliance (2 items)

| ID | Requirement | Score |
|----|-------------|-------|
| G-1 | Audit logging for all agent actions with timestamps and correlation IDs | __ /2 |
| G-2 | Applicable regulations mapped to system capabilities (GDPR, HIPAA, EU AI Act) | __ /2 |

**Subtotal: __ /4**

---

## SHOULD Requirements (36 items, 72 points max)

### 1. Agent Architecture & Design (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| A-4 | Orchestration logic separated from agent logic (deterministic where possible) | __ /2 |
| A-5 | Single Responsibility Principle applied to agent boundaries | __ /2 |
| A-6 | Component interaction documented with data flow diagram (Mermaid, PlantUML) | __ /2 |

**Subtotal: __ /6**

### 2. Reasoning & Decision Logic (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| R-4 | Deterministic vs LLM-driven decision boundaries documented for every decision point | __ /2 |
| R-5 | Output validation beyond schema (semantic reasonableness, cross-field consistency) | __ /2 |
| R-6 | Retry with exponential backoff for transient LLM API failures (max 3 retries) | __ /2 |

**Subtotal: __ /6**

### 3. Memory & State Management (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| M-3 | Memory types selected with justification (episodic, semantic, procedural) | __ /2 |
| M-4 | State recovery / checkpointing for workflows longer than 30 seconds | __ /2 |
| M-5 | Per-agent state isolation in multi-agent systems (no implicit shared state) | __ /2 |

**Subtotal: __ /6**

### 4. Tool Use & External Integration (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| T-4 | Dry-run mode for all tools with side effects (default in development) | __ /2 |
| T-5 | Integration protocols selected and documented (MCP, A2A, direct, custom) | __ /2 |
| T-6 | Tool call timeouts and circuit breakers implemented | __ /2 |

**Subtotal: __ /6**

### 5. Multi-Agent Coordination (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| C-3 | Per-agent timeouts (independent of pipeline timeout) | __ /2 |
| C-4 | Conflict resolution defined for contradictory agent outputs | __ /2 |
| C-5 | Inter-agent message size and frequency limits enforced | __ /2 |

**Subtotal: __ /6**

### 6. Evaluation & Testing (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| E-4 | Trajectory quality evaluated (not just final output) | __ /2 |
| E-5 | At least one adversarial test case (prompt injection, contradictory input) | __ /2 |
| E-6 | Evaluation suite integrated into CI/CD (runs on every code change) | __ /2 |

**Subtotal: __ /6**

### 7. Observability & Monitoring (4 items)

| ID | Requirement | Score |
|----|-------------|-------|
| O-2 | End-to-end request tracing with correlation IDs (OpenTelemetry preferred) | __ /2 |
| O-3 | Per-request and aggregate cost tracking (token usage, model costs) | __ /2 |
| O-4 | Latency monitoring per stage (per-agent, per-tool, total) with SLOs | __ /2 |
| O-5 | Output quality monitoring / drift detection in production | __ /2 |

**Subtotal: __ /8**

### 8. Safety, Security & Guardrails (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| S-5 | Human-in-the-loop checkpoints for high-consequence actions | __ /2 |
| S-6 | Multi-layer prompt injection defense (input + output + instruction hierarchy) | __ /2 |
| S-7 | Rate limiting and abuse prevention per user and globally | __ /2 |

**Subtotal: __ /6**

### 9. Ethical & Responsible AI (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| ET-3 | Bias assessment documented (potential biases, monitoring, mitigations) | __ /2 |
| ET-4 | Attribution and provenance tracking (sources cited, findings attributed to agents) | __ /2 |
| ET-5 | Societal impact documented for high-stakes domains | __ /2 |

**Subtotal: __ /6**

### 10. Deployment & Operations (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| D-3 | CI/CD pipeline with automated evals, vulnerability scanning, rollback | __ /2 |
| D-4 | Cost optimization implemented (model routing, caching, cascade, or batching) | __ /2 |
| D-5 | Graceful degradation defined for LLM API down, tool unavailable, overload | __ /2 |

**Subtotal: __ /6**

### 11. Documentation & Reproducibility (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| DOC-4 | All configuration options documented (name, type, default, description) | __ /2 |
| DOC-5 | Evaluation methodology documented (test cases, expected outcomes, pass criteria) | __ /2 |
| DOC-6 | Prompt versioning with changelog (what changed, why, eval results before/after) | __ /2 |

**Subtotal: __ /6**

### 12. Governance & Compliance (3 items)

| ID | Requirement | Score |
|----|-------------|-------|
| G-3 | Data privacy controls (PII handling, data minimization, right to erasure) | __ /2 |
| G-4 | Access controls and authentication for all system entry points | __ /2 |
| G-5 | Incident response procedures documented (detection, disable, investigate, notify) | __ /2 |

**Subtotal: __ /6**

---

## Scoring Summary

| # | Category | MUST Score | MUST Max | SHOULD Score | SHOULD Max |
|---|----------|-----------|----------|-------------|------------|
| 1 | Agent Architecture & Design | __ | /6 | __ | /6 |
| 2 | Reasoning & Decision Logic | __ | /6 | __ | /6 |
| 3 | Memory & State Management | __ | /4 | __ | /6 |
| 4 | Tool Use & External Integration | __ | /6 | __ | /6 |
| 5 | Multi-Agent Coordination | __ | /4 | __ | /6 |
| 6 | Evaluation & Testing | __ | /6 | __ | /6 |
| 7 | Observability & Monitoring | __ | /2 | __ | /8 |
| 8 | Safety, Security & Guardrails | __ | /8 | __ | /6 |
| 9 | Ethical & Responsible AI | __ | /4 | __ | /6 |
| 10 | Deployment & Operations | __ | /4 | __ | /6 |
| 11 | Documentation & Reproducibility | __ | /6 | __ | /6 |
| 12 | Governance & Compliance | __ | /4 | __ | /6 |
| | **TOTAL** | **__** | **/60** | **__** | **/72** |

**MUST Percentage:** __ / 60 = ___%
**SHOULD Percentage:** __ / 72 = ___%

---

## Maturity Tiers

| Tier | MUST % | SHOULD % | Description |
|------|--------|----------|-------------|
| **Foundational** | < 80% | -- | Below minimum viable. Not ready for any deployment. Address all MUST gaps before proceeding. |
| **Professional** | >= 80% | < 75% | Meets minimum requirements. Suitable for internal/limited deployment. SHOULD gaps are improvement opportunities. |
| **Enterprise** | >= 80% | >= 75% | Production-grade. Suitable for external/customer-facing deployment. Regulatory readiness possible. |
| **Research-Grade** | >= 95% | >= 90% | Exceeds standard requirements. Suitable for high-stakes, regulated, or frontier applications. |

### Tier Determination

```
IF MUST% < 80%  --> Foundational (action: address MUST gaps immediately)
IF MUST% >= 80% AND SHOULD% < 75%  --> Professional (action: prioritize SHOULD items)
IF MUST% >= 80% AND SHOULD% >= 75%  --> Enterprise (action: consider MAY items)
IF MUST% >= 95% AND SHOULD% >= 90%  --> Research-Grade (action: maintain and iterate)
```

---

## Critical Gaps Quick Check

Before doing the full assessment, check these 5 make-or-break items:

| # | Item | Status |
|---|------|--------|
| 1 | **Structured output enforced** (R-2) -- Agents return typed schemas, not freeform text | YES / NO |
| 2 | **Error isolation implemented** (C-2) -- One agent crash does not bring down the system | YES / NO |
| 3 | **Input validation present** (S-1) -- All user input validated before reaching the LLM | YES / NO |
| 4 | **Evaluation suite exists** (E-1) -- At least 5 automated test cases with expected outcomes | YES / NO |
| 5 | **Secrets managed properly** (S-4) -- No API keys in source code, logs, or agent prompts | YES / NO |

**If any answer is NO, address it before proceeding with the full assessment.**

---

## Top Anti-Patterns to Check

During assessment, watch for these high-impact anti-patterns (see anti-patterns.md for full list):

| AP # | Name | Quick Test |
|------|------|------------|
| AP-2 | God Agent | Does any agent have > 10 tools or > 2,000 words in its prompt? |
| AP-7 | Prompt-and-Pray | Is any agent output parsed with regex instead of structured schemas? |
| AP-17 | Unsafe Execution | Does any tool pass LLM output to shell commands via string interpolation? |
| AP-25 | Vibes-Based Testing | Is there a runnable evaluation suite with quantitative pass/fail criteria? |
| AP-30 | Black Box Agent | Can you trace a single request through every agent and tool call? |
| AP-36 | Maximum Privilege | Does any agent have admin/root access when read-only would suffice? |
| AP-37 | No Kill Switch | Can you disable the system in under 60 seconds? |
| AP-43 | YOLO Deployment | Does code go directly from dev to production with no staging? |

---

## Assessment Metadata

| Field | Value |
|-------|-------|
| System assessed | |
| Assessor | |
| Date | |
| Framework version | v1.0 (February 2026) |
| MUST score | __ / 60 (__%) |
| SHOULD score | __ / 72 (__%) |
| Maturity tier | |
| Top 3 gaps | 1. __ 2. __ 3. __ |
| Recommended next actions | |
