# Agentic AI Framework Decision Matrix

> Last updated: February 2026. Data sourced from official releases, LangChain State of Agent
> Engineering report (1,340 respondents), and production adoption signals.

---

## Framework Profiles

### 1. LangGraph v1.0 (GA October 2025)

**Architecture:** Graph-based state machine with nodes, edges, and conditional routing. Immutable
state with reducer-driven schemas via `TypedDict` and `Annotated`. Durable checkpointing survives
server restarts.

**Key 2025-2026 capabilities:** Tools can update graph state directly. `Command` enables dynamic
edgeless flows. `interrupt()` for first-class HITL. Short-term and long-term memory with
time-travel/replay. React integration via single hook. Standard JSON Schema support (Zod 4,
Valibot, ArkType).

**Production signals:** Used by Uber, LinkedIn, Klarna. 57.3% of surveyed orgs have agents in
production. 89% have observability implemented.

**Languages:** Python, JavaScript, Go.

**Honest assessment:** Most mature for complex multi-agent orchestration. Steeper learning curve
than alternatives. Graph-based mental model is powerful but not intuitive for all developers.
Tighter coupling to LangChain ecosystem than some teams want.

### 2. CrewAI v1.9 (Stable January 2026)

**Architecture:** Role-based collaborative agents. Each agent has role, goal, backstory, and
toolset. Process models: sequential, hierarchical, consensual.

**Key 2025-2026 capabilities:** CrewAI Flows (v1.8.0, January 2026) for event-driven orchestration
with HITL. CrewAI AMP enterprise offering with unified control plane, real-time observability,
secure integrations, cloud and on-premise deployment.

**Production signals:** Fastest growing community for multi-agent prototyping. Enterprise AMP
offering maturing. Some report scalability concerns at very high agent counts.

**Languages:** Python.

**Honest assessment:** Fastest time-to-prototype. Intuitive role abstraction lowers barrier to
entry. Flows is relatively new (January 2026). Less granular control than LangGraph for complex
state machines. Strong choice for teams that need results fast.

### 3. Pydantic AI v1.62 (February 2026)

**Architecture:** Type-safe agents built on Pydantic validation. Structured inputs/outputs with
dependency injection and tool registration. 100% test coverage.

**Key 2025-2026 capabilities:** Durable execution (survives API failures, restarts, long-running
HITL). Pydantic Evals with span-based evaluation via OpenTelemetry traces. Pydantic Logfire for
tracing, debugging, cost monitoring (OpenTelemetry-compliant). Model-agnostic (OpenAI, Anthropic,
Gemini, Groq, Mistral, Ollama).

**Production signals:** Clean Pythonic API gaining rapid adoption. Strong eval story differentiates
from competitors.

**Languages:** Python.

**Honest assessment:** Best-in-class for structured output enforcement and type safety. Less
ergonomic for large-scale multi-agent orchestration compared to LangGraph or CrewAI. Smaller
community but growing. Excellent choice when correctness of output structure matters most.

### 4. Google ADK v1.0 (Python GA, April 2025)

**Architecture:** Code-first, model-agnostic (optimized for Gemini, supports Claude/OpenAI/Ollama
via LiteLLM). Agents-as-tools pattern lets you use other agents (including LangGraph, CrewAI) as
tools.

**Key 2025-2026 capabilities:** A2A protocol support for agent interoperability. Bidirectional
audio/video streaming for multimodal dialogue. Pre-built tools (Search, Code Exec), MCP support.
Built-in dev UI at localhost:4200. Deploy to Cloud Run, GKE, Vertex AI Agent Engine.

**Production signals:** TypeScript ADK available. Java ADK v0.1.0. Go ADK announced. 50+ A2A
technology partners (Atlassian, Salesforce, SAP).

**Languages:** Python, TypeScript, Java, Go.

**Honest assessment:** Most polyglot framework. Deep Google Cloud integration is a strength and a
constraint. Agent Engine pricing started late 2025. Relatively newer community compared to
LangChain. Strong choice for Google Cloud shops and multimodal applications.

### 5. OpenAI Agents SDK (March 2025)

**Architecture:** Production-ready successor to experimental Swarm. Agents with instructions,
built-in tools, handoffs, guardrails, and tracing. Provider-agnostic with documented non-OpenAI
model paths.

**Key capabilities:** Handoffs as first-class primitive for agent-to-agent transfer. Configurable
input/output guardrails. Built-in execution visualization and tracing.

**Languages:** Python, TypeScript.

**Honest assessment:** Clean abstraction. Built-in guardrails and tracing from launch. Relatively
thin orchestration compared to LangGraph. Less mature multi-agent patterns. Best for teams already
invested in the OpenAI ecosystem that need simple multi-agent workflows.

### 6. Claude Agent SDK v0.2 (Active Development)

**Architecture:** CLI-based agent framework. Built-in tools (Bash, Glob, file operations). Context
compaction for long-running tasks. Agent Skills system for document tasks (PowerPoint, Excel, Word,
PDF). 1M token context window (beta).

**Key capabilities:** MCP native. Effective harnesses for long-running agents. Context management
prevents context window exhaustion. Powers most of Anthropic's major agent loops.

**Languages:** TypeScript (primary), Python.

**Honest assessment:** Best-in-class context management. Exceptional for software engineering and
document automation tasks. Tied to Anthropic models. Not yet v1.0 (pre-release). TypeScript-first
may not suit all teams. Strong choice for code-heavy automation.

### 7. DSPy v2.6 (Stanford NLP)

**Architecture:** Declarative framework for programming (not prompting) language models. Typed
signatures compiled by optimizers into effective prompts/weights.

**Key capabilities:** MIPROv2 optimizer raises ReAct scores from 24% to 51%. BetterTogether and
LeReT optimizers. Composable modules for ReAct agents, RAG pipelines, customer service patterns.

**Languages:** Python.

**Honest assessment:** Unique optimizer-driven approach eliminates manual prompt engineering.
Steeper learning curve. Optimizer runs add latency to the development cycle. Academic rigor from
Stanford NLP but less intuitive for imperative programmers. Best for teams that want to
systematically optimize agent reasoning.

### 8. Emerging Frameworks (Late 2025 / Early 2026)

| Framework | Backer | Key Differentiator | Maturity |
|-----------|--------|-------------------|----------|
| **Strands Agents SDK** | AWS | Model-agnostic, first-class OTel tracing, deep AWS integrations | New (May 2025) |
| **Agno** (ex Phi-Data) | Independent | Full-stack with memory, knowledge, reasoning. 20+ ready tools. Web UI | Growing rapidly |
| **smolagents** | HuggingFace | Core logic in ~1,000 LOC. CodeAgent writes actions as code. Hub integration | Active |
| **BeeAI** | IBM | Apache 2.0. Python + TypeScript. Llama 3.3 / IBM Granite focus | Active |
| **Cloudflare Agents** | Cloudflare | Durable Objects, edge deployment, remote MCP hosting, free tier | Active |
| **Microsoft Agent Framework** | Microsoft | AutoGen + Semantic Kernel merger. Azure-native. GA target Q1 2026 | Preview |

---

## Decision Matrix

| Dimension | LangGraph | CrewAI | Pydantic AI | Google ADK | OpenAI SDK | Claude SDK | DSPy |
|-----------|-----------|--------|-------------|------------|------------|------------|------|
| **Production Maturity** | 5 | 4 | 4 | 4 | 4 | 3 | 3 |
| **Multi-Agent Quality** | 5 (graph states) | 5 (role-based) | 2 (manual) | 4 (A2A, agents-as-tools) | 3 (handoffs) | 2 (basic) | 2 (basic) |
| **Structured Output** | 4 | 3 | 5 (native Pydantic) | 4 | 4 | 3 | 4 (typed sigs) |
| **Tracing/Observability** | 5 (LangSmith) | 3 (external) | 5 (Logfire/OTel) | 4 (Cloud Trace) | 4 (built-in) | 3 (basic) | 2 (basic) |
| **Human-in-the-Loop** | 5 (interrupt API) | 4 (Flows HITL) | 3 (durable exec) | 3 (callbacks) | 3 (guardrails) | 2 (manual) | 1 (none) |
| **Memory: Short-term** | 5 (checkpoints) | 4 (built-in) | 3 (session) | 4 (sessions) | 3 (threads) | 5 (compaction) | 2 (basic) |
| **Memory: Long-term** | 4 (built-in) | 4 (entity mem) | 2 (custom) | 3 (Agent Engine) | 2 (custom) | 2 (custom) | 1 (none) |
| **Deployment Options** | 4 (LangServe, Cloud Run) | 4 (AMP, containers) | 3 (custom) | 5 (Cloud Run, Vertex, GKE) | 3 (custom) | 3 (CLI, custom) | 2 (custom) |
| **Learning Curve** | 4 (hard) | 2 (easy) | 2 (easy) | 3 (moderate) | 2 (easy) | 3 (moderate) | 5 (hard) |
| **Community Size** | 5 (largest) | 4 (large) | 3 (growing) | 3 (growing) | 4 (large) | 3 (growing) | 3 (academic) |
| **Lock-in Risk** | 3 (LangChain ecosystem) | 2 (low) | 1 (minimal) | 3 (Google Cloud) | 3 (OpenAI models) | 4 (Anthropic models) | 1 (minimal) |

**Scale:** 1-5 unless noted. Higher = more/better, except Learning Curve (higher = harder)
and Lock-in Risk (higher = more lock-in).

---

## Decision Flowchart

```
START: What is your primary requirement?
|
+-- Need graph-based complex orchestration with durable state?
|   +-- YES --> LangGraph v1.0
|       Best for: stateful workflows, conditional routing, time-travel debugging
|       Trade-off: steepest learning curve
|
+-- Need fastest prototype for role-based multi-agent?
|   +-- YES --> CrewAI v1.9
|       Best for: quick demos, collaborative agents, event-driven flows
|       Trade-off: less control over orchestration internals
|
+-- Need type-safe structured outputs as first priority?
|   +-- YES --> Pydantic AI v1.62
|       Best for: structured task agents, type-safe pipelines, span-based evals
|       Trade-off: manual orchestration for multi-agent
|
+-- Google Cloud native with multi-language and A2A?
|   +-- YES --> Google ADK v1.0
|       Best for: Gemini-first, multimodal, polyglot teams, Vertex AI deployment
|       Trade-off: strongest with Gemini models
|
+-- OpenAI-only stack with simple handoffs?
|   +-- YES --> OpenAI Agents SDK
|       Best for: tool-use agents, conversational routing, built-in guardrails
|       Trade-off: thin orchestration, less mature multi-agent
|
+-- Software engineering or document automation?
|   +-- YES --> Claude Agent SDK v0.2
|       Best for: long-running code tasks, MCP-native, context-heavy work
|       Trade-off: pre-v1.0, Anthropic-only
|
+-- Need to optimize prompts algorithmically?
|   +-- YES --> DSPy v2.6
|       Best for: systematic prompt optimization, research-grade reasoning
|       Trade-off: steep learning curve, optimizer latency
|
+-- AWS-native with OTel-first observability?
|   +-- YES --> Strands Agents SDK (emerging)
|
+-- Want minimal code, open-source models, HuggingFace Hub?
|   +-- YES --> smolagents (emerging)
|
+-- None of the above? --> Evaluate Agno, BeeAI, or custom implementation
```

---

## Key Selection Criteria

### Team and Organization

| Factor | Question to Ask | Impact on Choice |
|--------|----------------|------------------|
| **Language preference** | Is the team Python-only, or multi-language? | ADK (4 languages) vs Python-only frameworks |
| **Existing ecosystem** | Already using LangChain? OpenAI? Google Cloud? | Ecosystem alignment reduces friction |
| **Team size** | Small team (2-3) or large org? | Small: CrewAI/Pydantic AI. Large: LangGraph/ADK |
| **ML expertise** | Strong ML background or application developers? | DSPy for ML experts. CrewAI for app devs |

### Technical Requirements

| Factor | Question to Ask | Impact on Choice |
|--------|----------------|------------------|
| **Model provider strategy** | Single provider or multi-model? | Single: provider SDK. Multi: LangGraph, Pydantic AI, ADK |
| **Orchestration complexity** | Simple pipeline or complex state machine? | Simple: CrewAI, OpenAI SDK. Complex: LangGraph |
| **Structured output needs** | How critical is output type safety? | Critical: Pydantic AI. Nice-to-have: any framework |
| **Multimodal** | Audio, video, or image processing? | ADK (streaming), smolagents (multimodal) |

### Operational Requirements

| Factor | Question to Ask | Impact on Choice |
|--------|----------------|------------------|
| **Deployment target** | Cloud (which?), on-prem, edge? | Google: ADK. AWS: Strands. Edge: Cloudflare. On-prem: any OSS |
| **Observability needs** | Basic logging or full distributed tracing? | Full: LangGraph (LangSmith), Pydantic AI (Logfire) |
| **Compliance/audit** | Regulated industry? | LangGraph (audit trails), ADK (Vertex AI governance) |
| **Scale expectations** | Hundreds or millions of requests/day? | High scale: LangGraph, ADK, Cloudflare Agents |
| **Cost sensitivity** | Can you afford frontier models for everything? | Cost-sensitive: DSPy optimization, model routing |

---

## Combination Patterns

Many production systems combine frameworks rather than choosing one:

| Pattern | Example | When |
|---------|---------|------|
| **LangGraph + Pydantic AI** | LangGraph orchestration, Pydantic AI for typed agent logic | Need both complex orchestration AND type safety |
| **CrewAI + LangGraph** | CrewAI for rapid prototyping, migrate complex flows to LangGraph | Start fast, harden later |
| **Google ADK + LangGraph** | ADK agents-as-tools wrapping LangGraph sub-graphs | Google Cloud deployment with complex sub-workflows |
| **Any framework + DSPy** | Use DSPy to optimize prompts, deploy in production framework | Optimize reasoning quality before deployment |
| **Any framework + Mem0** | Framework for orchestration, Mem0 for persistent memory | Need cross-session memory with relevance decay |

---

## What NOT to Choose (Anti-Patterns)

- **Do not choose LangGraph** just because it is popular. If your workflow is a simple sequential
  pipeline, LangGraph's graph abstraction adds complexity without benefit.
- **Do not choose CrewAI** for systems requiring fine-grained state control. The role-based
  abstraction trades control for convenience.
- **Do not choose a provider SDK** (OpenAI, Claude) if you need model flexibility. Provider
  lock-in is real and switching costs are high.
- **Do not build custom** when a framework covers 80% of your needs. The remaining 20% is rarely
  worth the maintenance burden of a bespoke system.
- **Do not choose based on benchmarks alone.** Framework choice is primarily about developer
  ergonomics, ecosystem fit, and operational requirements -- not which framework scores highest
  on a leaderboard.

---

## Sources

Data in this document is drawn from:
- LangChain State of Agent Engineering (Nov-Dec 2025, 1,340 respondents)
- Official framework documentation and release notes (as of February 2026)
- Production adoption reports from Uber, LinkedIn, Klarna, Databricks
- Research survey compiled in `/tmp/research_survey.md`
