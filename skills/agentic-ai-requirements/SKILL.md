---
name: agentic-ai-requirements
description: |
  Assess, design, and score agentic AI systems against a comprehensive enterprise-grade requirements framework.
  Triggers: "assess my agent system", "agentic AI requirements", "agent architecture review",
  "multi-agent design review", "evaluate my agent", "agentic system checklist",
  "design an agent system", "agent design guide", "agentic requirements", "agent assessment"
---

# Agentic AI Requirements Skill

Framework for assessing agentic AI systems against 12 categories, 88+ requirements, and MUST/SHOULD/MAY priority levels. Grounded in Feb 2026 state-of-the-art across LangGraph, CrewAI, Pydantic AI, Google ADK, OpenAI Agents SDK, Claude Agent SDK, DSPy, MCP/A2A protocols, NIST AI RMF, EU AI Act, and OWASP Top 10 for LLMs.

The 12 categories: Agent Architecture, Reasoning and Decision Logic, Memory and State, Tool Use and Integration, Multi-Agent Coordination, Evaluation and Testing, Observability and Monitoring, Safety and Security, Ethics and Responsible AI, Deployment and Operations, Documentation and Reproducibility, Governance and Compliance.

## Mode Detection

- **ASSESS** -- User says "assess", "evaluate", "review", "score", "audit", or "analyze" and references an existing codebase. Default when a codebase is present.
- **DESIGN** -- User says "design", "architect", "plan", "build", or "create" a new agent system. No existing codebase.
- **CHECKLIST** -- User says "checklist", "quick check", "scorecard", or "self-assessment". Lightweight mode.

If intent is ambiguous, ask the user which mode they want.

---

## Reference Files

Read these files as needed during assessment. Do NOT load all files at once.

| File | Contents |
|------|----------|
| `references/framework-requirements.md` | Full 12-category requirements (88 items) with IDs, priorities, rationale, anti-patterns |
| `references/framework-comparison.md` | Framework selection decision matrix |
| `references/pattern-catalog.md` | Orchestration and reasoning pattern catalog |
| `references/evaluation-guide.md` | Testing strategies, assessment frameworks, LLM judge patterns, benchmarks |
| `references/safety-security-guide.md` | OWASP Top 10 for LLMs, prompt injection defense, guardrails, sandboxing |
| `references/compliance-standards.md` | NIST AI RMF, EU AI Act, GDPR, SOC 2, audit logging requirements |
| `references/checklist-template.md` | Quick-reference scoring checklist (30 MUST + 36 SHOULD items) |
| `references/anti-patterns.md` | 48 anti-patterns organized by category with detection signals and remediation |

---

## ASSESS MODE

When the user asks to assess an existing agentic AI codebase, run these four phases in order.

### Phase 1: Reconnaissance

Explore the codebase systematically using Glob, Grep, and Read. Run searches in parallel where possible.

**Framework Detection** (run first -- determines subsequent patterns):
- Grep imports: pydantic_ai, langgraph, crewai, google.adk, google.genai, openai, anthropic, dspy, autogen
- Glob configs: pyproject.toml, requirements.txt, package.json, Pipfile, setup.cfg, uv.lock

**Agent Definitions** -- classes, system prompts, role definitions, persona configs:
- Grep: "Agent(", "system_prompt", "instructions", "role=", "persona"
- Grep: "output_type=", "response_model=", "structured_output", "json_schema"

**Tool Implementations** -- function decorators, schemas:
- Grep: "@tool", "tool(", "FunctionTool", "Tool(", "create_tool"

**Orchestration** -- control flow, state machines, graphs, async:
- Grep: "asyncio.gather", "StateGraph", "Flow(", "Pipeline", "supervisor", "router", "dispatch", "handoff"

**Memory and State** -- databases, caches, state stores, sessions:
- Grep: "memory", "state", "session", "checkpoint", "persist", "cache"
- Grep: "ChromaDB", "Pinecone", "Qdrant", "Redis", "sqlite", "vector"

**Testing** -- test files, benchmarks:
- Glob: test_*.py, *_test.py, tests/**, *benchmark*
- Grep: "def test_", "Case(", "assert", "LLMJudge", "rubric"

**Observability** -- logging, tracing, metrics:
- Grep: "logging", "logger", "opentelemetry", "trace", "span", "Logfire", "LangSmith", "Langfuse", "Phoenix"

**Safety** -- validation, filtering, rate limiting (look for both presence and absence):
- Grep: "validate", "sanitize", "rate_limit", "guardrail", "injection"
- Grep: "shell=True" (flag as anti-pattern T-3 if found)
- Grep: "os.getenv", "load_dotenv" (secret management)
- Grep: hardcoded patterns like "sk-", "api_key=", "password="

**Documentation** -- README, architecture docs, env templates:
- Glob: README*, ARCHITECTURE*, docs/**, .env.example

After reconnaissance, summarize: what the system does, framework used, agent count, orchestration pattern, external dependencies.

### Phase 2: Category-by-Category Assessment

Read `references/framework-requirements.md` for the full requirement list. Assess all 12 categories (A-1..A-8, R-1..R-8, M-1..M-7, T-1..T-8, C-1..C-7, E-1..E-8, O-1..O-7, S-1..S-8, ET-1..ET-6, D-1..D-7, DOC-1..DOC-7, G-1..G-7).

For each requirement, assign a score:
- **MET (2 pts)** -- Fully implemented with clear evidence (cite file:line)
- **PARTIAL (1 pt)** -- Partially implemented or lacking best practices
- **NOT MET (0 pts)** -- Not present or not detectable
- **N/A** -- Does not apply; exclude from scoring

### Phase 3: Gap Analysis and Scoring

Calculate scores:
- **MUST Score**: 30 items x 2 points = 60 max
- **SHOULD Score**: 37 items x 2 points = 74 max

Assign maturity tier:

| Tier | MUST % | SHOULD % | Description |
|------|--------|----------|-------------|
| Foundational | <80% | Any | Critical gaps. Not production-ready. |
| Professional | >=80% | <75% | Solid foundation. Needs SHOULD items for production. |
| Enterprise | >=80% | >=75% | Production-grade. Professional engineering standards. |
| Research-Grade | >=95% | >=90% | State-of-the-art. Exceeds industry norms. |

Identify: Top 5 Critical Gaps (unmet MUSTs), Top 5 Improvement Opportunities (unmet SHOULDs), Strengths (categories at 90%+).

### Phase 4: Report Generation

Output a structured markdown report:

```markdown
# Agentic AI Assessment Report

## Executive Summary
**System**: {name} | **Framework**: {framework} | **Architecture**: {N} agents, {pattern} | **Date**: {date}

### Maturity Tier: {tier}
| Metric | Score | Max | % |
|--------|-------|-----|---|
| MUST | {score} | 60 | {pct}% |
| SHOULD | {score} | 74 | {pct}% |

### Key Strengths
- {strength with evidence}

### Critical Gaps
- {gap with remediation}

## Category Breakdown
### {Category} ({MUST score}/{max} MUST, {SHOULD score}/{max} SHOULD)
| ID | Priority | Requirement | Score | Evidence |
|----|----------|-------------|-------|----------|
| {id} | {MUST/SHOULD} | {req} | {MET/PARTIAL/NOT MET} | {file:line} |

## Gap Analysis
### Critical Gaps (Unmet MUSTs)
{Ranked list with remediation steps}
### Improvement Opportunities (Unmet SHOULDs)
{Ranked list with recommendations}
### Anti-Patterns Detected
{List with file, name, fix -- reference references/anti-patterns.md}

## Recommendations
### Phase 1: Foundation (1-2 weeks) -- unmet MUSTs
### Phase 2: Professional Grade (1 month) -- unmet SHOULDs
### Phase 3: Enterprise Grade (as needed) -- selected MAYs
```

Offer to save the report to `{project_root}/agentic-assessment-report.md`.

---

## DESIGN MODE

Guide the user through a 10-step interactive walkthrough. At each step, ask questions, present options from reference files, and document decisions.

**Step 1: Task Definition** -- What problem? Inputs/outputs? Success criteria? Users?

**Step 2: Agent Count** -- Single vs multi-agent? Task decomposition? Document per A-2.

**Step 3: Orchestration Pattern** -- Reference `references/pattern-catalog.md`:
- Supervisor/Worker, Sequential Pipeline, Parallel Fan-out/Fan-in, Swarm, State Machine, Hybrid
- Ask which fits and why. Document per A-3.

**Step 4: Reasoning Strategy** -- Per agent, select:
- Direct Prompting, Chain-of-Thought, ReAct, Plan-and-Execute, Tree-of-Thought, Reflection
- Document per R-1.

**Step 5: Memory Architecture** -- Classify state as Ephemeral/Session/Persistent. Document stores and expiration per M-1.

**Step 6: Tool Design** -- For each tool: name, typed I/O, side effects, permission level, protocol (direct/MCP/A2A). Document per T-1..T-3.

**Step 7: Framework Selection** -- Reference `references/framework-comparison.md`. Match to steps 1-6. Key factors: structured output, orchestration, testing, memory, deployment, expertise.

**Step 8: Quality Assurance Plan** -- Reference `references/evaluation-guide.md`. Design: 5+ test cases (positive, negative, edge, adversarial, degenerate), assessors, pass threshold, CI/CD plan. Document per E-1..E-3.

**Step 9: Safety Posture** -- Reference `references/safety-security-guide.md`. Define: input/output validation, least-privilege matrix, HITL checkpoints, injection defense. Document per S-1..S-6.

**Step 10: Deployment** -- Runtime, trigger, config management, cost optimization. Document per D-1..D-2.

### Output: Architecture Decision Record

After all 10 steps, produce a structured ADR:

```markdown
# Architecture Decision Record: {System Name}
## Context
{Problem statement and requirements}
## Decisions
### Agent Architecture
- Count: {N} ({justification})
- Orchestration: {pattern} ({justification})
- Agents: {list with roles, tools, reasoning patterns}
### Technical Stack
- Framework: {name} ({justification})
- Language: {language}
- Memory: {types and stores}
- Tools: {list with protocols}
### Quality and Safety
- Testing: {approach}
- Safety: {guardrails}
- Observability: {plan}
### Deployment
- Environment: {runtime}
- Trigger: {mechanism}
- Scaling: {approach}
## Requirements Coverage
{Map decisions to MUST/SHOULD items addressed}
```

---

## CHECKLIST MODE

Output the full checklist for self-assessment or rapid scoring. Score: 0=Not Present, 1=Partial, 2=Complete. Also available in `references/checklist-template.md`.

### MUST Requirements (30 items, 60 points max)

**Agent Architecture and Design**
- [ ] A-1: Agent definitions with persona, instructions, constraints
- [ ] A-2: Single vs multi-agent justification documented
- [ ] A-3: Orchestration pattern selected and documented

**Reasoning and Decision Logic**
- [ ] R-1: Reasoning pattern selected per agent
- [ ] R-2: Structured output enforcement (typed schemas)
- [ ] R-3: Error handling with conservative fallbacks

**Memory and State Management**
- [ ] M-1: Memory architecture documented (ephemeral/session/persistent)
- [ ] M-2: Input validation with size limits on all stateful data

**Tool Use and Integration**
- [ ] T-1: Tool schemas with typed I/O and documentation
- [ ] T-2: Least-privilege tool access per agent
- [ ] T-3: Injection prevention in tool calls (parameterized inputs)

**Multi-Agent Coordination**
- [ ] C-1: Communication topology defined and documented
- [ ] C-2: Error isolation between agents (exception boundaries)

**Testing and Quality Assurance**
- [ ] E-1: Automated testing with 5+ diverse test cases
- [ ] E-2: Task completion testing (not just output shape)
- [ ] E-3: Pass/fail tracking across runs with persistence

**Observability and Monitoring**
- [ ] O-1: Structured logging for every agent invocation

**Safety, Security and Guardrails**
- [ ] S-1: Input validation before LLM processing
- [ ] S-2: Output validation before user/system delivery
- [ ] S-3: Least-privilege access for all agents and tools
- [ ] S-4: No secrets in code, logs, or agent output

**Ethics and Responsible AI**
- [ ] ET-1: Decision scope and limitations documented
- [ ] ET-2: Transparency for automated decisions (explainable outputs)

**Deployment and Operations**
- [ ] D-1: Deployment architecture documented
- [ ] D-2: Environment-based configuration (no hardcoded values)

**Documentation and Reproducibility**
- [ ] DOC-1: README with purpose, architecture, quick start, CLI reference
- [ ] DOC-2: Version-controlled prompts and instructions
- [ ] DOC-3: Pinned dependencies (lockfiles)

**Governance and Compliance**
- [ ] G-1: Audit logging for all agent actions with side effects
- [ ] G-2: Regulatory mapping (which regulations apply and how addressed)

**MUST Score: ___/60 (Threshold: >=80% for Professional tier)**

### SHOULD Requirements (37 items, 74 points max)

**Agent Architecture and Design**
- [ ] A-4: Orchestration logic separated from agent logic
- [ ] A-5: Single-responsibility agents
- [ ] A-6: Data flow diagram with trust boundaries

**Reasoning and Decision Logic**
- [ ] R-4: Deterministic vs LLM decision boundary documented
- [ ] R-5: Semantic output validation (beyond schema conformance)
- [ ] R-6: Retry with exponential backoff and jitter

**Memory and State Management**
- [ ] M-3: Memory type selection justified (episodic/semantic/procedural)
- [ ] M-4: State recovery for long-running workflows
- [ ] M-5: Isolated per-agent state (no implicit globals)

**Tool Use and Integration**
- [ ] T-4: Dry-run mode for tools with side effects
- [ ] T-5: Integration protocol documented (MCP/A2A/direct)
- [ ] T-6: Tool call timeouts and circuit breakers

**Multi-Agent Coordination**
- [ ] C-3: Per-agent timeouts (not just pipeline timeout)
- [ ] C-4: Conflict resolution for contradictory outputs
- [ ] C-5: Inter-agent message size and frequency limits

**Testing and Quality Assurance**
- [ ] E-4: Trajectory quality testing (not just final output)
- [ ] E-5: Adversarial test case included
- [ ] E-6: Test suite in CI/CD pipeline

**Observability and Monitoring**
- [ ] O-2: End-to-end request tracing (OpenTelemetry)
- [ ] O-3: Per-request and aggregate cost tracking
- [ ] O-4: Latency monitoring at each stage
- [ ] O-5: Output quality monitoring (drift detection)

**Safety, Security and Guardrails**
- [ ] S-5: Human-in-the-loop checkpoints for high-consequence actions
- [ ] S-6: Multi-layer prompt injection defense
- [ ] S-7: Rate limiting and abuse prevention

**Ethics and Responsible AI**
- [ ] ET-3: Bias assessment documented
- [ ] ET-4: Attribution and provenance tracking
- [ ] ET-5: Societal impact documentation (for high-stakes domains)

**Deployment and Operations**
- [ ] D-3: CI/CD pipeline for agent systems
- [ ] D-4: Cost optimization strategy implemented
- [ ] D-5: Graceful degradation defined

**Documentation and Reproducibility**
- [ ] DOC-4: Configuration options documented (table format)
- [ ] DOC-5: Testing methodology documented
- [ ] DOC-6: Prompt versioning with changelog

**Governance and Compliance**
- [ ] G-3: Data privacy controls (minimization, right-to-erasure)
- [ ] G-4: Access controls and authentication
- [ ] G-5: Incident response procedures documented

**SHOULD Score: ___/74 (Threshold: 56+ for Enterprise tier)**

### Maturity Tier Determination

| Tier | MUST % | SHOULD % | What It Means |
|------|--------|----------|---------------|
| Foundational | <80% | Any | Critical gaps. Not production-ready. |
| Professional | >=80% | <75% | Solid foundation. Ready for controlled production. |
| Enterprise | >=80% | >=75% | Production-grade. Professional engineering standards. |
| Research-Grade | >=95% | >=90% | State-of-the-art. Exceeds industry norms. |

---

## Scoring Instructions

1. **MET (2 pts)** -- Fully implemented with evidence. Best practices followed.
2. **PARTIAL (1 pt)** -- Partially addressed. Incomplete or non-ideal patterns.
3. **NOT MET (0 pts)** -- Absent or insufficient. "Not found in codebase" is valid evidence.
4. **N/A** -- Does not apply. Exclude from both numerator and denominator.

Always cite evidence: file path and relevant code/config for MET/PARTIAL.

---

## Anti-Pattern Detection

Actively scan for these during assessment. Full catalog: `references/anti-patterns.md` (48 items).

**Architecture**: God Agent (20+ tools or 5000+ word prompt), LLM as Router (simple if/else suffices), Invisible Architecture (no diagrams/docs)

**Safety**: shell=True in subprocess, hardcoded credentials, single-layer defense, fail-silent on security events

**Testing**: No test files, shape-only tests, LLM-only assessment without deterministic checks

**Operations**: No deployment docs, unpinned deps, no env-based config, prompts as string literals

Note each detected anti-pattern in the report with: file, anti-pattern name, recommended fix.

---

## Implementation Priority Matrix

Organize recommendations into phases:

**Phase 1: Foundation (Week 1-2)** -- Unmet MUSTs.
Priority: A-1/R-2 (agent defs), R-3/C-2 (error handling), S-1/S-2/M-2 (validation), O-1 (logging), E-1/E-2 (tests), DOC-1/DOC-3 (docs), S-4 (secrets), G-1 (audit).

**Phase 2: Professional (Week 3-4)** -- Unmet SHOULDs.
Priority: R-4 (decision boundaries), O-2 (tracing), O-3 (costs), S-5 (HITL), S-6 (injection defense), E-6 (CI/CD), DOC-4 (config docs), DOC-6 (prompt versioning).

**Phase 3: Enterprise (Month 2+)** -- Selected MAYs.
A-7 (dynamic composition), R-7 (reflection), M-6 (cross-session memory), T-7/S-8 (sandboxing), C-6 (consensus), D-4 (cost optimization), G-6 (NIST AI RMF).
