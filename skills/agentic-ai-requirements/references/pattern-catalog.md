# Agentic AI Orchestration and Reasoning Pattern Catalog

> Last updated: February 2026. Patterns grounded in production adoption data, framework
> implementations, and academic research.

---

## Part 1: Orchestration Patterns

### Pattern 1: Supervisor/Worker (Hierarchical)

**Description:** A central supervisor agent receives requests, decomposes them into subtasks,
delegates to specialized worker agents, monitors progress, validates outputs, and synthesizes
a final response. The supervisor owns the task lifecycle.

**When to use:**
- Heterogeneous tasks requiring different specialist skills
- Quality control is critical (supervisor validates before returning)
- Audit trail needed (supervisor logs all delegation decisions)
- Complex multi-domain workflows (e.g., Databricks enterprise RAG)

**When NOT to use:**
- Homogeneous parallel work where all workers do the same thing (use Fan-out instead)
- Simple sequential pipelines (supervisor adds overhead without benefit)
- Low-latency requirements (supervisor adds a round-trip per delegation)

**Implementation sketch:**
```python
# LangGraph: supervisor as conditional node
supervisor_node --> route_to_worker(state) --> {security_agent, privacy_agent, grc_agent}
worker_output --> supervisor_node  # supervisor validates and routes next

# CrewAI: hierarchical process
crew = Crew(agents=[supervisor, worker_a, worker_b], process=Process.hierarchical)
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | Supervisor node with conditional edges |
| CrewAI | Yes | `Process.hierarchical` with manager agent |
| Google ADK | Partial | Agents-as-tools (supervisor calls worker agents) |
| OpenAI SDK | Partial | Handoffs from supervisor to workers |
| Pydantic AI | Manual | Custom async orchestrator calling agent instances |

---

### Pattern 2: Sequential Pipeline

**Description:** Agents execute in a fixed, deterministic order. Each agent receives the output
of the previous agent, transforms it, and passes the result forward. The pipeline is linear
with no branching.

**When to use:**
- Well-defined workflows with clear stage boundaries
- Document processing (extract -> transform -> validate -> respond)
- Data pipelines where each stage depends on the previous
- Predictable latency and cost (each stage runs exactly once)

**When NOT to use:**
- Tasks where stages are independent (use Parallel Fan-out instead)
- Tasks requiring dynamic routing based on intermediate results (use State Machine)
- Exploratory tasks where the number of steps is unknown

**Implementation sketch:**
```python
# CrewAI: sequential process
crew = Crew(agents=[extractor, transformer, validator], process=Process.sequential)

# LangGraph: linear chain
graph.add_edge("extract", "transform")
graph.add_edge("transform", "validate")
graph.add_edge("validate", END)
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | Linear edge chain |
| CrewAI | Yes | `Process.sequential` (default) |
| Google ADK | Yes | SequentialAgent |
| Pydantic AI | Manual | Chained `agent.run()` calls |
| Haystack | Yes | Pipeline with sequential component connections |

---

### Pattern 3: Parallel Fan-out/Fan-in

**Description:** Dispatch the same input to multiple agents concurrently. Each agent processes
independently. Results are aggregated by a collector/merger function after all agents complete
(or after a timeout).

**When to use:**
- Independent analysis from multiple perspectives (e.g., security + privacy + compliance)
- Reducing latency by parallelizing independent work
- Ensemble approaches where diversity of analysis improves quality
- Tasks where agents do not need to see each other's intermediate results

**When NOT to use:**
- Agents share mutable state (race conditions, inconsistent results)
- Sequential dependency between agents (Agent B needs Agent A's output)
- Cost-sensitive scenarios where only one perspective is needed

**Implementation sketch:**
```python
# Python asyncio (framework-agnostic, used by SecureFlow)
results = await asyncio.gather(
    security_agent.run(input),
    privacy_agent.run(input),
    grc_agent.run(input),
    return_exceptions=True  # critical: isolate failures
)
# Deterministic aggregation
merged = aggregate_results(results)

# LangGraph: Send API for dynamic fan-out
def fan_out(state):
    return [Send("analyze", {"agent": a, "input": state}) for a in agents]
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | `Send` API for parallel node dispatch |
| CrewAI | Partial | Async task execution within Flows |
| Google ADK | Yes | ParallelAgent |
| Pydantic AI | Manual | `asyncio.gather()` with multiple agent runs |
| OpenAI SDK | Manual | Concurrent API calls |

**Critical implementation detail:** Always use `return_exceptions=True` (or equivalent) so one
failed agent does not crash the entire fan-out. Substitute conservative fallbacks for failed
agents.

---

### Pattern 4: Swarm (Decentralized Handoffs)

**Description:** Agents dynamically hand off to each other based on context. No central
orchestrator. Each agent decides whether to handle the request or pass it to a more appropriate
agent. Intelligence emerges from agent interactions.

**When to use:**
- Conversational routing (customer service, help desk triage)
- Tasks where the "right" agent depends on information discovered during processing
- Systems where agents need to negotiate or collaborate freely

**When NOT to use:**
- Tasks requiring centralized state tracking or audit trails
- High-reliability systems (emergent behavior is hard to test/predict)
- Compliance-sensitive workflows (who made what decision is unclear)

**Implementation sketch:**
```python
# OpenAI Agents SDK: handoffs as first-class primitive
triage_agent = Agent(
    name="triage",
    handoffs=[billing_agent, technical_agent, sales_agent]
)
# Agent decides handoff based on conversation context

# LangGraph: Command-based dynamic routing
def agent_node(state):
    if should_handoff(state):
        return Command(goto="specialist_agent", update={"reason": "..."})
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| OpenAI SDK | Yes | Handoffs (first-class primitive) |
| LangGraph | Yes | `Command` for dynamic routing |
| CrewAI | Partial | Consensual process mode |
| Google ADK | Partial | Agent-to-agent via A2A protocol |
| Pydantic AI | Manual | Custom handoff logic |

---

### Pattern 5: State Machine (Explicit States and Transitions)

**Description:** The system has explicitly defined states and transitions. Each state maps to
an agent or action. Transitions are conditional, based on structured output from the current
state. The entire workflow is a finite automaton.

**When to use:**
- Well-defined workflows with clear states (draft -> review -> approved -> deployed)
- Regulatory workflows requiring auditable state transitions
- Long-running processes that need durable checkpointing at each state
- Workflows with human-in-the-loop gates between states

**When NOT to use:**
- Exploratory or creative tasks where the path is unknown upfront
- Simple request-response interactions (state machine is overkill)
- Highly dynamic workflows where states are discovered at runtime

**Implementation sketch:**
```python
# LangGraph: native state machine
graph = StateGraph(AgentState)
graph.add_node("draft", draft_agent)
graph.add_node("review", review_agent)
graph.add_node("approve", human_approval)
graph.add_conditional_edges("review", route_by_quality, {
    "pass": "approve",
    "fail": "draft",  # loop back for revision
})
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes (core abstraction) | StateGraph with conditional edges |
| CrewAI | Partial | Flows with conditional routing |
| Google ADK | Partial | SequentialAgent with conditional logic |
| Pydantic AI | Manual | Custom state management |
| OpenAI SDK | Manual | Agent handoff chains |

---

### Pattern 6: Hybrid (Deterministic + LLM-Driven)

**Description:** Deterministic code handles routing, aggregation, validation, and orchestration.
LLM-driven agents handle analysis, reasoning, and judgment where ambiguity exists. The
orchestrator is code; the workers are LLMs.

**When to use:**
- Production systems needing both reliability and flexibility
- Any system where some decisions are clear-cut (route based on category) and some require
  judgment (assess risk level)
- Cost-sensitive systems (LLM calls only where needed)

**When NOT to use:**
- Purely deterministic workflows (no LLM needed at all)
- Research/exploration where you want maximum LLM autonomy

**Implementation sketch:**
```python
# SecureFlow pattern (industry best practice)
# Deterministic: dispatch, aggregate, route
results = await asyncio.gather(  # deterministic dispatch
    security_agent.run(input),
    privacy_agent.run(input),
    grc_agent.run(input),
    return_exceptions=True
)
# Deterministic: aggregate and decide
if any(r.requires_review for r in results):  # structured field, not LLM decision
    await create_review_issue(...)           # deterministic action
```

**Why this is the consensus best practice (2025-2026):**

| Dimension | Pure LLM Routing | Hybrid | Pure Deterministic |
|-----------|-----------------|--------|-------------------|
| Cost | High (LLM call per routing decision) | Medium | Low |
| Latency | Variable | Predictable for routing | Fast |
| Reliability | Variable | High for routing, variable for analysis | High |
| Flexibility | High | High where needed | Low |
| Auditability | Difficult | Easy for routing, harder for analysis | Easy |

The Plan-and-Execute variant of this pattern reduces costs by 90% versus using frontier models
for everything, by using LLMs only for planning/analysis and deterministic code for execution.

**Framework support:** All frameworks support this pattern. It is an architectural choice, not a
framework feature.

---

### Pattern 7: Dynamic Composition

**Description:** Agents spawn sub-agents as needed based on runtime conditions. The agent
topology is not fixed at design time but adapts to task complexity, available resources, or
discovered requirements.

**When to use:**
- Unpredictable task complexity (simple requests need 1 agent, complex need 5)
- Resource-constrained environments where you want to minimize active agents
- Systems that evolve over time (new specialist agents added without redesign)

**When NOT to use:**
- Without resource limits (unlimited spawning causes cost/resource explosion)
- When you need deterministic behavior (dynamic composition is inherently variable)
- Simple, well-understood workflows

**Implementation sketch:**
```python
# LangGraph: Command for dynamic node creation
def orchestrator(state):
    complexity = assess_complexity(state["input"])
    if complexity == "high":
        return Command(goto="spawn_specialists", update={"count": 3})
    return Command(goto="single_agent")

# CrewAI Flows: event-driven agent spawning
@flow.listen(TaskReceived)
async def on_task(event):
    agents = select_agents(event.task_type)
    crew = Crew(agents=agents, process=Process.sequential)
    return await crew.kickoff()
```

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | `Command` + `Send` for dynamic routing |
| CrewAI | Yes | Flows event-driven composition |
| Google ADK | Yes | Agents-as-tools (compose at runtime) |
| Pydantic AI | Manual | Dynamic agent instantiation |
| OpenAI SDK | Partial | Dynamic handoff targets |

**Critical safeguard:** Always implement resource limits -- maximum agent count, maximum total
tokens, maximum wall-clock time. Without limits, dynamic composition can cause unbounded cost.

---

## Part 2: Reasoning Patterns

### Pattern 8: ReAct (Reason + Act)

**Description:** The agent interleaves reasoning ("I need to find X") with action (tool call to
find X) in a loop. Each cycle: observe the result, reason about next step, take action. The
most common pattern for tool-using agents.

**When to use:**
- General-purpose tool-using agents
- Tasks requiring information gathering before decision-making
- Situations where the agent must adapt its approach based on tool results

**When NOT to use:**
- Simple tasks where the answer can be generated in one shot (wastes tokens on reasoning)
- Tasks with strict latency requirements (each reason-act cycle adds latency)
- Tasks where all needed information is in the prompt (no tools needed)

**Implementation sketch:**
```python
# Supported natively by most frameworks
# Pydantic AI: tools are registered, agent reasons about when to call them
agent = Agent(
    model="openai:gpt-4o-mini",
    tools=[search_tool, calculator_tool],
    system_prompt="Reason step by step. Use tools when you need information."
)

# DSPy: optimized ReAct
react = dspy.ReAct(signature, tools=[...])
# MIPROv2 optimizer raises ReAct from 24% to 51% on benchmarks
```

**Framework support:** All major frameworks support ReAct natively or via tool registration.

---

### Pattern 9: Plan-and-Execute

**Description:** Phase 1: the agent creates a complete plan (list of steps). Phase 2: each
step is executed (possibly by different agents or tools). Phase 3 (optional): after execution,
replan if results diverge from expectations.

**When to use:**
- Complex multi-step tasks where planning upfront saves wasted effort
- Cost-sensitive scenarios (planning LLM call + cheap execution saves 90% vs ReAct)
- Tasks where the user should approve the plan before execution

**When NOT to use:**
- Simple tasks that do not benefit from upfront planning
- Highly dynamic tasks where the plan becomes obsolete immediately
- Without replanning capability (a rigid plan that cannot adapt is fragile)

**Implementation sketch:**
```python
# LangGraph: plan-and-execute template
# Phase 1: Planner agent generates structured plan
plan = await planner.run("Analyze this codebase for security issues")
# plan.steps = ["1. Scan dependencies", "2. Check auth", "3. Review API"]

# Phase 2: Execute each step
for step in plan.steps:
    result = await executor.run(step, context=accumulated_results)
    accumulated_results.append(result)

# Phase 3: Replan if needed
if needs_replanning(accumulated_results):
    new_plan = await planner.run("Revise plan based on findings", context=results)
```

**Cost advantage:** Using a frontier model for planning and a mid-tier model for execution
achieves 90% cost reduction versus using the frontier model for everything (ReAct pattern).

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | Plan-and-execute template |
| CrewAI | Partial | Sequential process with planning task |
| Pydantic AI | Manual | Custom planner + executor agents |
| Google ADK | Manual | Custom SequentialAgent with planning step |

---

### Pattern 10: Tree-of-Thought

**Description:** The agent explores multiple reasoning paths simultaneously, evaluates each
path's promise, prunes unpromising branches, and selects the best path. Like breadth-first
search over reasoning strategies.

**When to use:**
- Complex reasoning requiring exploration of alternatives
- Tasks where the first approach may not be optimal
- High-stakes decisions where exploring multiple options reduces risk

**When NOT to use:**
- Simple tasks (exploring multiple paths for "what is 2+2?" is wasteful)
- Cost-sensitive scenarios (each branch multiplies LLM calls)
- Latency-sensitive scenarios (parallel exploration adds time)

**Implementation sketch:**
```python
# Conceptual (no framework provides this natively)
paths = []
for approach in ["direct", "decompose", "analogy"]:
    result = await agent.run(f"Solve using {approach}: {problem}")
    score = await evaluator.run(f"Rate this solution: {result}")
    paths.append((result, score))

best = max(paths, key=lambda p: p[1].score)
```

**Framework support:** No framework provides native Tree-of-Thought. Implemented as custom
orchestration over any agent framework. Research-grade pattern; rare in production.

---

### Pattern 11: Reflection/Self-Correction

**Description:** After generating an initial output, the agent (or a separate critic agent)
evaluates the output for completeness, accuracy, and consistency. If deficiencies are found,
the agent revises and re-evaluates, iterating until quality criteria are met or a maximum
iteration count is reached.

**When to use:**
- Quality-critical outputs (reports, analysis, code generation)
- Tasks where first-draft quality is typically insufficient
- When you have clear quality criteria the agent can check against

**When NOT to use:**
- Without termination criteria (infinite reflection loops waste tokens and money)
- Simple factual lookups (reflection adds cost without improving correctness)
- Latency-critical paths (each reflection cycle adds a full LLM round-trip)

**Implementation sketch:**
```python
# LangGraph: reflection as a graph cycle
MAX_ITERATIONS = 3

def generate(state):
    return {"draft": agent.run(state["input"])}

def reflect(state):
    critique = critic.run(f"Evaluate: {state['draft']}")
    return {"critique": critique, "iteration": state["iteration"] + 1}

def should_continue(state):
    if state["iteration"] >= MAX_ITERATIONS:
        return "done"  # terminate regardless
    if state["critique"].passes_quality:
        return "done"
    return "revise"

graph.add_conditional_edges("reflect", should_continue, {
    "done": END,
    "revise": "generate"
})
```

**Research signal:** Reflection improves output quality by 10-25% on complex reasoning tasks.
Always set a maximum iteration count to prevent runaway costs.

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | Cycle in graph with conditional edge |
| CrewAI | Partial | Task callbacks for review |
| Pydantic AI | Manual | Loop with quality check |
| DSPy | Yes | Assertion-based backtracking |

---

### Pattern 12: Mixture of Agents (MoA)

**Description:** Multiple agents independently propose answers to the same question. A
separate aggregator agent synthesizes the proposals into a final answer, weighing each
proposal's strengths. Similar to ensemble methods in ML.

**When to use:**
- High-stakes decisions needing diverse perspectives
- Tasks where different models/prompts have different strengths
- Quality-critical outputs where consensus improves confidence

**When NOT to use:**
- Homogeneous agents (if all agents are the same model with the same prompt, there is no
  diversity and MoA provides no benefit)
- Cost-sensitive scenarios (N agents = N times the cost)
- Simple tasks where one agent is sufficient

**Implementation sketch:**
```python
# Fan-out to diverse agents, then aggregate
proposals = await asyncio.gather(
    agent_gpt4o.run(question),      # different model
    agent_claude.run(question),      # different model
    agent_gemini.run(question),      # different model
)
# Aggregator synthesizes (can be deterministic or LLM-driven)
final = await aggregator.run(
    f"Synthesize these {len(proposals)} analyses: {proposals}"
)
```

**Key insight:** MoA works because diversity of perspective catches blind spots. Using the
same model three times is NOT MoA -- it is redundancy without diversity.

**Framework support:** Implemented as Parallel Fan-out (Pattern 3) + custom aggregation. No
framework provides MoA as a named primitive.

---

### Pattern 13: Debate Pattern

**Description:** Two or more agents argue opposing positions on a question. A judge agent
evaluates the arguments and renders a decision. Optionally, debaters can respond to each
other's arguments across multiple rounds.

**When to use:**
- Nuanced decisions with genuine trade-offs (security vs usability, cost vs quality)
- Decisions where bias in a single agent could lead to poor outcomes
- Compliance/audit contexts where showing both sides strengthens justification

**When NOT to use:**
- Factual questions with clear answers (debating "what is 2+2?" is pointless)
- Latency-sensitive paths (multi-round debate is slow)
- Cost-constrained scenarios (each round multiplies LLM calls)

**Implementation sketch:**
```python
# Two advocates + one judge
pro_argument = await advocate_pro.run(f"Argue FOR: {proposal}")
con_argument = await advocate_con.run(f"Argue AGAINST: {proposal}")

# Optional: allow rebuttals
pro_rebuttal = await advocate_pro.run(f"Respond to: {con_argument}")
con_rebuttal = await advocate_con.run(f"Respond to: {pro_argument}")

# Judge decides
decision = await judge.run(
    f"Given:\nPRO: {pro_argument}\n{pro_rebuttal}\n"
    f"CON: {con_argument}\n{con_rebuttal}\n"
    f"Render a decision with justification."
)
```

**Research signal:** Debate/adversarial patterns with voting protocols improve reasoning
accuracy by 13.2% on complex decision tasks.

**Framework support:** No framework provides debate as a native pattern. Implemented as custom
multi-agent orchestration.

---

### Pattern 14: Iterative Refinement

**Description:** Generate an initial output, evaluate it against quality criteria, and improve
it in successive iterations. Unlike Reflection (Pattern 11), the evaluation may come from
external sources (user feedback, tool validation, test execution) rather than self-critique.

**When to use:**
- Creative/generative tasks (writing, design, code generation)
- Tasks with external validators (compiler, test suite, style checker)
- Workflows where partial progress is valuable (show draft, refine based on feedback)

**When NOT to use:**
- Without a quality threshold for loop termination (infinite refinement = infinite cost)
- Tasks where the first output is typically correct (refinement adds latency for no gain)
- Without measurable quality metrics (subjective "is it better?" loops are unbounded)

**Implementation sketch:**
```python
MAX_ITERATIONS = 5
QUALITY_THRESHOLD = 0.85

draft = await generator.run(task_description)
for i in range(MAX_ITERATIONS):
    # External evaluation (not self-critique)
    eval_result = await run_tests(draft.code)
    quality_score = eval_result.pass_rate

    if quality_score >= QUALITY_THRESHOLD:
        break  # good enough

    # Refine with feedback
    draft = await generator.run(
        f"Improve this code. Test results: {eval_result.failures}"
    )
```

**Key distinction from Reflection:** Reflection uses the agent's own judgment. Iterative
Refinement uses external signals (test results, user feedback, API responses) to drive
improvement. External signals are more reliable.

**Framework support:**
| Framework | Native Support | Mechanism |
|-----------|---------------|-----------|
| LangGraph | Yes | Graph cycles with external evaluation nodes |
| CrewAI | Partial | Task callbacks and iteration |
| Pydantic AI | Manual | Loop with external validation |
| DSPy | Yes | Assertion-based optimization |

---

## Part 3: Pattern Selection Guide

### By Task Complexity

| Complexity | Recommended Pattern | Example |
|------------|-------------------|---------|
| **Simple** (single step, clear answer) | Direct prompting or ReAct | FAQ lookup, data extraction |
| **Moderate** (2-5 steps, some ambiguity) | Sequential Pipeline or State Machine | Document processing, form filling |
| **Complex** (many steps, dynamic routing) | Supervisor/Worker or Hybrid | Multi-domain analysis, enterprise workflows |
| **Exploratory** (unknown steps, discovery) | Plan-and-Execute or Dynamic Composition | Research tasks, codebase analysis |

### By Latency Requirements

| Latency Budget | Recommended Pattern | Avoid |
|---------------|-------------------|-------|
| **< 2 seconds** | Direct prompting, cached ReAct | Tree-of-Thought, Debate, multi-round Reflection |
| **2-10 seconds** | Parallel Fan-out, simple ReAct | Sequential with many steps, multi-round Debate |
| **10-60 seconds** | Supervisor/Worker, Plan-and-Execute | Unbounded iteration, deep Tree-of-Thought |
| **> 60 seconds (async)** | Dynamic Composition, Debate, Iterative Refinement | None (latency unconstrained) |

### By Cost Constraints

| Cost Sensitivity | Recommended Pattern | Cost Optimization |
|-----------------|-------------------|------------------|
| **Minimal budget** | Direct prompting with small model | Skip reasoning patterns entirely |
| **Cost-conscious** | Plan-and-Execute (90% savings vs ReAct) | Frontier model for planning only, mid-tier for execution |
| **Moderate budget** | Hybrid orchestration, cached ReAct | Semantic caching for repeated queries |
| **Unlimited** | MoA, Debate, Tree-of-Thought | Use frontier models throughout |

### By Reliability Needs

| Reliability Requirement | Recommended Pattern | Key Mechanism |
|------------------------|-------------------|---------------|
| **Best-effort** | ReAct, Swarm | Accept variability |
| **Consistent quality** | Hybrid + Reflection | Deterministic routing + self-critique |
| **High-stakes** | MoA or Debate + Human-in-the-Loop | Multi-perspective + human gate |
| **Regulatory/auditable** | State Machine + Supervisor | Explicit states, logged transitions, approval gates |

### By Team Expertise

| Team Background | Recommended Starting Pattern | Why |
|----------------|----------------------------|-----|
| **New to agents** | Sequential Pipeline (CrewAI) | Simplest mental model, fastest results |
| **Backend engineers** | State Machine (LangGraph) | Familiar from workflow engines |
| **ML engineers** | ReAct + DSPy optimization | Comfortable with optimization loops |
| **Full-stack** | Hybrid with Parallel Fan-out | Matches microservices mental model |

---

## Pattern Composition Reference

Production systems rarely use a single pattern. Common compositions:

| Composition | Patterns Combined | Example |
|------------|------------------|---------|
| **SecureFlow** | Parallel Fan-out + Hybrid | Deterministic dispatch to 3 agents, deterministic aggregation |
| **Enterprise RAG** | Sequential + ReAct | Pipeline (embed -> retrieve -> rank) then ReAct for answer synthesis |
| **Code Generation** | Plan-and-Execute + Iterative Refinement | Plan the approach, generate code, run tests, refine until passing |
| **Customer Service** | Swarm + Escalation | Agents hand off based on topic, escalate to human for complex issues |
| **Risk Assessment** | MoA + Supervisor | Multiple analysts propose independently, supervisor synthesizes |
| **Content Creation** | Reflection + Iterative Refinement | Draft, self-critique, incorporate editor feedback, repeat |

---

## Protocol Reference (Agent Communication)

When agents need to communicate across boundaries, these protocols apply:

| Protocol | Type | Best For | Status (Feb 2026) |
|----------|------|----------|-------------------|
| **MCP** (Model Context Protocol) | JSON-RPC client-server | Tool invocation, data exchange | De facto standard. 5,800+ servers. Linux Foundation. |
| **A2A** (Agent-to-Agent) | Peer-to-peer | Cross-org agent interop | 150+ orgs. Linux Foundation. Enterprise focus. |
| **ACP** (Agent Communication Protocol) | REST-native | Multi-part messages, async streaming | Emerging. REST-friendly. |
| **ANP** (Agent Network Protocol) | Open-network | Decentralized identifiers, linked data | Research-grade. |

**Practical guidance:** Use MCP for tool integration. Consider A2A only when agents from
different organizations or frameworks must interoperate. For internal multi-agent systems,
direct function calls or framework-native communication is simpler and faster.

---

## Common Mistakes

1. **Choosing patterns based on novelty, not need.** Tree-of-Thought and Debate are
   intellectually interesting but expensive and slow. Use them only when the quality improvement
   justifies the cost.

2. **Skipping the Hybrid pattern.** Pure LLM orchestration is the most common mistake in
   production agent systems. Deterministic code for routing + LLM for judgment is almost always
   the right split.

3. **No termination criteria on iterative patterns.** Reflection, Iterative Refinement, and
   Debate all loop. Without maximum iteration counts and quality thresholds, they loop forever.

4. **Fan-out without error isolation.** If you run agents in parallel without
   `return_exceptions=True` or equivalent, one failed agent crashes the entire pipeline.

5. **Swarm in regulated environments.** Swarm's emergent behavior is fundamentally at odds
   with audit and compliance requirements. Use Supervisor/Worker or State Machine instead.

6. **Choosing framework before pattern.** The orchestration pattern should drive framework
   selection, not the other way around. Decide what you need architecturally, then pick the
   framework that best supports it.

---

## Sources

Patterns in this catalog are drawn from:
- LangGraph documentation and templates (v1.0, October 2025)
- CrewAI documentation and Flows (v1.8-1.9, January 2026)
- OpenAI Agents SDK documentation (March 2025)
- Google ADK documentation (v1.0, April 2025)
- Databricks supervisor architecture (production patterns)
- Stanford NLP DSPy research (v2.6)
- Kore.ai orchestration pattern analysis
- Stack AI 2026 guide to agentic workflow architectures
- SecureFlow reference implementation (Pydantic AI, February 2026)
- Research survey compiled in `/tmp/research_survey.md`
