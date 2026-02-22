# Agentic AI Anti-Patterns Reference

> Consolidated anti-patterns across all 12 requirement categories. Each anti-pattern describes
> a common mistake, explains why it causes problems, and provides the correct alternative.
> Use this reference during assessments to identify issues in existing or planned systems.

---

## Architecture Anti-Patterns

### AP-1: Agents All the Way Down
**Category:** Agent Architecture & Design
**Description:** Using agents (LLM calls) for tasks that could be accomplished with simple functions, if-statements, or database lookups. Examples: using an LLM to parse a date string, route to one of three endpoints based on a field value, or validate JSON schema conformance.
**Why Harmful:** Every LLM call adds latency (1-10 seconds), cost ($0.001-$0.10), and non-determinism. Using agents for deterministic work multiplies all three without benefit. A system that makes 20 LLM calls where 15 could be simple functions is 3-5x more expensive, slower, and less reliable than it needs to be.
**Instead:** Use the "deterministic by default" principle. For every component, ask: "Does this require judgment, reasoning, or natural language understanding?" If no, use code. Reserve LLM calls for genuinely ambiguous or language-dependent tasks. Document the deterministic vs LLM boundary explicitly.

### AP-2: God Agent
**Category:** Agent Architecture & Design
**Description:** A single agent with 20+ tools, a 5,000-word system prompt, and responsibility for everything from analysis to action-taking to reporting. The system prompt tries to cover every scenario with conditional instructions.
**Why Harmful:** Instruction-following quality degrades as prompt length increases. Tool selection accuracy drops as tool count increases. The agent cannot be evaluated, debugged, or improved independently for different tasks. A single failure mode affects everything.
**Instead:** Apply the Single Responsibility Principle. Each agent should have one clear domain. If an agent's prompt has more than 3 conditional sections ("if the user asks about X, then..."), split it. SecureFlow uses 3 specialized agents (security, privacy, GRC) instead of one "risk analysis" agent. OpenAI recommends fewer than 20 functions per agent call.

### AP-3: LLM Router
**Category:** Agent Architecture & Design
**Description:** Using an LLM call solely to route tasks when the routing logic could be expressed as deterministic code. Example: calling GPT-4o to decide whether a request is "security-related" or "privacy-related" when the input already has a structured `category` field.
**Why Harmful:** Adds 1-5 seconds of latency and $0.01-$0.05 per routing decision for a task that a single if-statement handles in microseconds. Also introduces non-determinism where determinism is desirable -- the same input might be routed differently on different runs.
**Instead:** Use deterministic routing (if-statements, lookup tables, regex matching) for structured inputs. Use LLM routing only when the input is genuinely ambiguous natural language that cannot be classified programmatically. SecureFlow routes deterministically: the orchestrator always runs all three agents in parallel, no LLM routing needed.

### AP-4: Implicit Communication
**Category:** Agent Architecture & Design
**Description:** Agents share state through side effects -- writing to shared files, global variables, or databases -- rather than explicit message passing. Agent B reads a file that Agent A wrote, but this dependency is not documented or enforced.
**Why Harmful:** Creates invisible coupling, race conditions, and debugging nightmares. When Agent B fails, the root cause (Agent A wrote unexpected data) is not traceable from B's logs alone. Testing requires reproducing the exact state that A left behind.
**Instead:** All inter-agent communication should be explicit and mediated. Use the orchestrator to pass data between agents. If agents must share state, use a typed shared state store with access logging. LangGraph's state graph enforces this pattern structurally.

### AP-5: Premature Multi-Agent
**Category:** Agent Architecture & Design
**Description:** Jumping to a multi-agent architecture without first demonstrating that a single agent with multiple tools is insufficient. Building 5 agents from day one because "multi-agent is the future."
**Why Harmful:** Multi-agent adds orchestration complexity, state synchronization, error isolation requirements, inter-agent communication overhead, and debugging difficulty. A single well-designed agent with 5 tools is simpler, cheaper, faster, and easier to debug than 5 agents with 1 tool each.
**Instead:** Start with a single agent. Add agents only when you can demonstrate that: (a) the single agent's prompt is too long for reliable instruction-following, (b) different tasks require fundamentally different model configurations, or (c) you need independent failure isolation between domains. Document the justification in an architecture decision record.

### AP-6: Framework Coupling
**Category:** Agent Architecture & Design
**Description:** Business logic (risk analysis rules, decision criteria, output formatting) that is inseparable from the agent framework. Swapping from Pydantic AI to LangGraph would require rewriting everything, not just the orchestration layer.
**Why Harmful:** Framework lock-in. The agentic AI landscape evolves rapidly -- LangGraph v1.0 was released October 2025, CrewAI Flows launched January 2026, Microsoft Agent Framework targets GA Q1 2026. Business logic coupled to a specific framework cannot benefit from improvements in alternatives.
**Instead:** Separate business logic into framework-agnostic modules. Agent prompts, evaluation criteria, and output schemas should be defined independently of the orchestration framework. The framework handles orchestration; the business logic defines behavior.

---

## Reasoning Anti-Patterns

### AP-7: Prompt-and-Pray
**Category:** Reasoning & Decision Logic
**Description:** Sending a prompt to an LLM with no structured output enforcement, no validation, and no error handling. Parsing the response with string matching or regex. Hoping the output format is consistent across calls.
**Why Harmful:** LLM output is inherently non-deterministic. Without structured output, the same prompt can return JSON one time and markdown the next. Downstream code that parses freeform text breaks unpredictably. 50% of "my agent stopped working" bugs trace back to unstructured output parsing failures.
**Instead:** Enforce structured output with typed schemas (Pydantic models, JSON Schema, Zod). Use framework-native enforcement: Pydantic AI `output_type`, LangGraph `.with_structured_output()`, OpenAI `response_format`. Validate every response before processing.

### AP-8: Infinite Loop
**Category:** Reasoning & Decision Logic
**Description:** Reasoning or reflection cycles with no termination criteria. An agent that "keeps thinking until it gets the right answer" with no maximum iteration count, timeout, or convergence check.
**Why Harmful:** Without termination bounds, a confused agent can loop indefinitely, consuming unlimited tokens and compute. A ReAct loop that cannot find the answer may try the same tool calls repeatedly. Cost can escalate from $0.10 to $100+ for a single request.
**Instead:** Set explicit termination criteria for every loop: maximum iterations (typically 3-5 for reflection, 10-15 for ReAct), timeout (30-120 seconds), convergence check (if the last N outputs are identical, stop), and token budget (maximum tokens per request). Implement all four, not just one.

### AP-9: Single Model Monoculture
**Category:** Reasoning & Decision Logic
**Description:** Using one model (e.g., GPT-4o) for every task regardless of complexity, cost, or latency requirements. Simple classification tasks use the same model as complex multi-step reasoning.
**Why Harmful:** Frontier models cost 10-100x more than mid-tier models. Using GPT-4o for tasks that GPT-4o-mini handles equally well wastes budget. Heterogeneous model architecture (frontier for reasoning, mid-tier for standard tasks, small models for high-frequency work) saves 27-55% in RAG setups and up to 90% with cascade architectures.
**Instead:** Profile each agent's task complexity. Route simple tasks to cheaper/faster models. Use cascade architecture: start with the cheapest model, escalate based on confidence scoring. Document the model selection rationale per agent. Stanford's FrugalGPT achieves 50-98% cost reduction while matching GPT-4 accuracy.

### AP-10: Reasoning Without Action
**Category:** Reasoning & Decision Logic
**Description:** Complex chains of thought that never call tools or produce actionable output. An agent that "analyzes," "considers," "reflects," and "concludes" but never actually does anything or returns structured results.
**Why Harmful:** Consumes tokens and latency without producing value. Often a symptom of vague agent instructions that do not specify concrete output requirements. The agent fills the output with reasoning tokens because it has no clear deliverable.
**Instead:** Every agent should have a concrete deliverable defined in its instructions: a structured output schema, a tool call, or a specific artifact. If an agent's purpose is analysis, the analysis must be captured in a typed schema with actionable fields (severity levels, boolean flags, specific recommendations), not freeform prose.

### AP-11: Hardcoded Reasoning
**Category:** Reasoning & Decision Logic
**Description:** Baking specific reasoning steps into code instead of letting the LLM reason. Example: writing Python code that checks for 50 specific security vulnerabilities by keyword matching, then asking the LLM to format the results -- rather than letting the LLM do the security analysis.
**Why Harmful:** Defeats the purpose of using an LLM. Hardcoded rules cannot handle novel situations, nuanced context, or emerging threats. The system is brittle to any input that does not match the predefined patterns. Updates require code changes rather than prompt updates.
**Instead:** Let LLMs do what they are good at (reasoning, analysis, language understanding) and use code for what code is good at (validation, routing, formatting, enforcement). The boundary should be: LLM reasons and decides; code validates, enforces, and takes action.

---

## Memory Anti-Patterns

### AP-12: Memory Amnesia
**Category:** Memory & State Management
**Description:** No state persistence whatsoever. Every interaction starts from scratch. An agent that helps with multi-step tasks but cannot remember what happened in the previous step after a page refresh or process restart.
**Why Harmful:** Users must repeat context. Multi-turn workflows are impossible. The agent cannot learn from past interactions or maintain conversation continuity. For any task requiring more than one exchange, this is a fundamental usability failure.
**Instead:** Implement at minimum session-level memory (survives within a conversation). For production systems, implement persistent memory appropriate to the use case: conversation state (Redis, database), knowledge (vector store), checkpointing (LangGraph, Pydantic AI durable work). Document the memory architecture explicitly.

### AP-13: Global Mutable State
**Category:** Memory & State Management
**Description:** Multiple agents sharing a single Python dictionary, global variable, or database table without access controls, locking, or conflict resolution. Agent A writes to `shared_state["result"]` while Agent B reads from it, with no synchronization.
**Why Harmful:** Race conditions, data corruption, non-reproducible behavior. In parallel runs (asyncio.gather), two agents can write to the same key simultaneously. Debugging is nearly impossible because the bug depends on timing. State corruption may be silent -- the system returns wrong results without raising errors.
**Instead:** Isolate per-agent state. Use the orchestrator to mediate all shared state access. If agents must share state, use a typed state store with explicit merge functions (LangGraph's reducer pattern). For parallel runs, each agent writes to its own namespace; the orchestrator merges after all agents complete.

### AP-14: Infinite Context
**Category:** Memory & State Management
**Description:** Stuffing the entire conversation history, all retrieved documents, and complete system instructions into every LLM call. Context grows without bound as the conversation progresses, eventually exceeding the context window or degrading output quality.
**Why Harmful:** Context window overflow causes hard failures. Long before overflow, attention dilution degrades output quality -- the LLM attends less to relevant information when surrounded by irrelevant context. Cost scales linearly with input tokens. A 100K-token context costs 50-100x more than a 2K-token context.
**Instead:** Implement context management: summarize older messages, use selective retrieval (include only relevant history), implement context compaction (Claude Agent SDK does this natively). Set explicit context budgets per agent. Use RAG to retrieve relevant information on demand rather than including everything preemptively.

### AP-15: Schema-less State
**Category:** Memory & State Management
**Description:** Agent state stored as untyped dictionaries (`Dict[str, Any]`) with no validation, no documentation of expected fields, and no versioning. Different parts of the code assume different state shapes.
**Why Harmful:** Runtime type errors when a field is missing or has an unexpected type. No IDE support (autocomplete, type checking). Impossible to validate state consistency. State migration (adding new fields, renaming fields) is error-prone because there is no schema to diff.
**Instead:** Define state as typed models (Pydantic BaseModel, TypedDict, dataclass). Validate state on every read and write. Version your state schema and implement migration logic for schema changes. LangGraph requires typed state schemas (TypedDict with Annotated reducers) -- this is the correct pattern.

---

## Tool Use Anti-Patterns

### AP-16: Swiss Army Tool
**Category:** Tool Use & External Integration
**Description:** A single tool that performs many unrelated operations based on a "mode" or "action" parameter. Example: `do_stuff(mode="search|create|delete|update|analyze", target="...", params={...})`.
**Why Harmful:** The LLM must understand a complex, overloaded interface to select the right mode and parameters. Tool description becomes long and confusing. Error handling cannot be specific to the operation type. Least-privilege enforcement is impossible -- the agent needs access to all modes even if it should only search.
**Instead:** One tool, one purpose. `search_documents()`, `create_document()`, `delete_document()` are three separate tools with clear names, simple parameters, and independent permissions. OpenAI recommends fewer than 20 functions, but each should be focused.

### AP-17: Unsafe Code Running
**Category:** Tool Use & External Integration
**Description:** Running agent-generated code (Python, SQL, shell commands) without sandboxing. Using `eval()`, string interpolation to build commands, or shell mode to pass LLM output directly into system calls.
**Why Harmful:** The LLM output is not trusted input. Prompt injection can cause arbitrary code running in the host environment. Even without malicious intent, hallucinated code can delete files, corrupt databases, or exfiltrate data. This is the most dangerous anti-pattern on this list.
**Instead:** Never run agent-generated code in the host environment. Use sandboxed environments: E2B (Firecracker microVMs), Modal (gVisor), Docker containers, or WASI. For shell commands, use argument lists not string interpolation. SecureFlow demonstrates the correct pattern: `asyncio.create_subprocess_exec(*cmd)` with argument lists and no shell mode.

### AP-18: Tool Without Error Handling
**Category:** Tool Use & External Integration
**Description:** Tool implementations that assume external calls always succeed. No try/catch around API calls, no timeout handling, no retry logic, no fallback behavior when the external service is down.
**Why Harmful:** External services fail regularly (rate limits, timeouts, outages, schema changes). A tool that does not handle errors will crash the entire agent pipeline on the first failure. The agent cannot recover or report the failure gracefully.
**Instead:** Every tool must handle: success, transient failure (retry with backoff), permanent failure (return error to agent), and timeout (configurable, typically 30-60s). Return structured error information so the agent can decide whether to retry, use an alternative, or report the failure. Implement circuit breakers for repeated failures.

### AP-19: Privilege Escalation
**Category:** Tool Use & External Integration
**Description:** Tools configured with more permissions than the agent needs. An analysis agent with write access to the database. A reporting tool with admin API keys. A research agent with access to production credentials.
**Why Harmful:** Violates least privilege (OWASP #6: Excessive Agency). If the agent hallucinates a destructive action or is exploited via prompt injection, the damage is limited only by the permissions available. 39% of companies report agents accessing unintended systems.
**Instead:** Create scoped credentials per agent and per tool. Read-only agents get read-only database connections. Reporting tools get read-only API keys. Each tool documents its required permissions and receives exactly those permissions, no more. SecureFlow's GitHub Action uses `issues: write` permission only, not `admin` or `repo`.

### AP-20: Undocumented Tools
**Category:** Tool Use & External Integration
**Description:** Tools registered with the agent that lack descriptions, parameter documentation, example usage, or documented side effects. The LLM must guess what the tool does from its function name alone.
**Why Harmful:** The LLM selects tools and constructs parameters based on the tool description. Poor descriptions lead to incorrect tool selection, malformed parameters, and wasted iterations. "The AI keeps calling the wrong tool" is almost always a tool documentation problem, not a model problem.
**Instead:** Every tool must have: a clear name (verb-noun: `create_issue`, `search_documents`), a description explaining when to use it, typed parameters with descriptions, documented return type, and documented side effects. Test tool selection by giving the agent a task and verifying it selects the correct tool with correct parameters.

---

## Coordination Anti-Patterns

### AP-21: Agent Telephone
**Category:** Multi-Agent Coordination
**Description:** Long chains of agent-to-agent calls where each agent summarizes and passes information to the next. Context degrades at each hop like a game of telephone. By the fifth agent, the original user intent is lost or distorted.
**Why Harmful:** Each agent summarization step loses information. The final agent operates on a degraded representation of the original request. Debugging requires tracing through multiple agents to find where context was lost. Latency and cost compound with each hop.
**Instead:** Minimize agent chain depth. Pass the original context (not summaries) to each agent when possible. Use fan-out (parallel) rather than sequential chains. If chains are necessary, include the original input alongside any intermediate summaries so downstream agents can verify context.

### AP-22: Chatty Agents
**Category:** Multi-Agent Coordination
**Description:** Agents exchanging pleasantries, confirmations, and incremental updates rather than substantive information. "I received your analysis. Let me review it. I have reviewed it. Here are my thoughts..."
**Why Harmful:** Every inter-agent message costs tokens. A "conversation" between agents that could be a single structured message exchange wastes 5-10x the tokens. Latency compounds with each round-trip. The agent logs become cluttered with noise, making debugging harder.
**Instead:** Use structured, one-shot communication. Agent A sends a typed result to the orchestrator. The orchestrator passes it to Agent B. Agent B responds with a typed result. No back-and-forth, no confirmation messages. SecureFlow's agents communicate zero messages to each other -- they each analyze independently and the orchestrator aggregates.

### AP-23: No Failure Boundary
**Category:** Multi-Agent Coordination
**Description:** One agent's failure cascades to the entire system. If the Security agent crashes, the Privacy and GRC agents also fail or produce corrupted output because they shared state or had sequential dependencies.
**Why Harmful:** The system's reliability is determined by its least reliable component. With N agents and 99% individual reliability, overall reliability is 0.99^N (97% for 3 agents, 90% for 10). Without isolation, one flaky API call brings down everything.
**Instead:** Implement error isolation: try/catch per agent, independent contexts, fallback substitution. SecureFlow's `asyncio.gather(return_exceptions=True)` is the gold standard -- each agent failure is caught independently and substituted with a conservative fallback. The pipeline always completes.

### AP-24: Conflicting Agents
**Category:** Multi-Agent Coordination
**Description:** Multiple agents with overlapping responsibilities that produce contradictory outputs without any conflict resolution mechanism. The security agent says "block this" while the usability agent says "allow this," and the system has no way to resolve the conflict.
**Why Harmful:** Ambiguous system behavior. Users receive contradictory information. The system's decisions depend on which agent's output is processed last (or which is arbitrarily chosen). Non-deterministic and non-auditable.
**Instead:** Define clear, non-overlapping responsibilities for each agent. Where overlap is intentional (multiple perspectives on the same issue), implement explicit conflict resolution: conservative merge (take the worse rating), weighted voting, hierarchical override, or human escalation. Document the conflict resolution policy.

---

## Evaluation Anti-Patterns

### AP-25: Vibes-Based Testing
**Category:** Evaluation & Testing
**Description:** No quantitative metrics. The developer runs the system a few times, reads the output, and decides "looks good" or "seems right." No test cases, no expected outcomes, no pass/fail criteria.
**Why Harmful:** Cannot detect regressions. Cannot compare versions. Cannot demonstrate correctness to stakeholders. Cannot onboard new team members who do not share the original developer's intuitions. Only 52% of organizations have implemented evals -- this anti-pattern is alarmingly common.
**Instead:** Implement automated evaluation with at least 5 diverse test cases covering: positive, negative, edge, adversarial, and degenerate inputs. Define explicit expected outcomes. Use both deterministic evaluators (for objective criteria) and LLM judges (for subjective quality). Track pass rates across runs.

### AP-26: Happy Path Only
**Category:** Evaluation & Testing
**Description:** Test cases that only cover expected, well-formed inputs. No edge cases (empty input, maximum-length input), no adversarial inputs (prompt injection attempts), no ambiguous inputs (contradictory requirements), no degenerate inputs (non-English text, special characters).
**Why Harmful:** Production inputs are messy. Users submit empty fields, paste entire documents, include special characters, and occasionally attempt prompt injection. A system that only handles clean inputs will fail unpredictably on real data. OWASP's #1 risk (prompt injection) cannot be detected by happy-path testing.
**Instead:** Include at least one test case for each category: normal, edge, adversarial, ambiguous, and degenerate. SecureFlow's evaluation suite includes: clear positive, clear negative, ambiguous, vague input, and specific domain tests (ML bias, data migration).

### AP-27: Production Debugging
**Category:** Evaluation & Testing
**Description:** No evaluation suite. The only way to test the system is to run it in production (or a production-like environment) and manually inspect output. Bugs are discovered by users, not by tests.
**Why Harmful:** Users experience bugs before developers do. Debugging in production is expensive, stressful, and slow. Without an eval suite, there is no way to verify that a fix does not introduce new regressions. Every code change is a gamble.
**Instead:** Build the evaluation suite BEFORE or DURING development, not after. Run evals in CI/CD on every code change. Set a minimum pass rate threshold and fail the build if it drops below. Budget for LLM API costs in CI -- it is far cheaper than production debugging.

### AP-28: Overfitting Evals
**Category:** Evaluation & Testing
**Description:** Writing prompts that specifically handle known test cases rather than generalizing. The agent's instructions contain "if the input mentions X, respond with Y" for each test case. The eval passes 100% but the system fails on any novel input.
**Why Harmful:** The evaluation provides false confidence. The system appears to work but is actually a lookup table disguised as an agent. Any input not anticipated in the prompt will produce unpredictable results. This is the agent equivalent of training on the test set.
**Instead:** Evaluation cases should be kept separate from agent instructions. Periodically add new test cases that the developers did not specifically optimize for. Use held-out test sets. Rotate test cases. If the eval pass rate drops when new cases are added, the system is overfitting.

### AP-29: Stale Benchmarks
**Category:** Evaluation & Testing
**Description:** An evaluation suite written months ago that has not been updated as the system evolved. New features, new tools, new use cases, and new failure modes are not covered by existing test cases.
**Why Harmful:** The evaluation suite tests the system that existed 3 months ago, not the system that exists today. New features ship untested. Old test cases may no longer be relevant. The pass rate becomes a vanity metric that does not reflect actual system quality.
**Instead:** Update the evaluation suite whenever you change the system. Every new feature should include at least one new test case. Every production bug should result in a new regression test case. Review the test suite quarterly for staleness.

---

## Observability Anti-Patterns

### AP-30: Black Box Agent
**Category:** Observability & Monitoring
**Description:** No logging, no tracing, no visibility into agent decisions. The system receives input and produces output with no intermediate visibility. When something goes wrong, the only debugging tool is to re-run the input and hope the problem reproduces.
**Why Harmful:** Non-deterministic systems do not reproduce reliably. The same input may produce different results on different runs. Without logs or traces, debugging requires guessing. Compliance requires audit trails. Incident response requires understanding what happened.
**Instead:** Implement structured logging for every agent invocation and end-to-end tracing with OpenTelemetry. At minimum: log agent name, input summary, output summary, latency, success/failure, and model used. Use correlation IDs to connect all steps in a single request.

### AP-31: Log Everything
**Category:** Observability & Monitoring
**Description:** Verbose, unstructured logging that captures everything -- full prompts, full responses, debug messages, framework internals -- in freeform text with no consistent format. Logs are 10GB/day and impossible to search.
**Why Harmful:** Too much noise obscures the signal. Searching for a specific request in 10GB of freeform text is impractical. Full prompts in logs may contain PII or secrets. Storage costs escalate. Log analysis tools choke on inconsistent formats.
**Instead:** Use structured JSON logging with consistent fields. Log summaries, not full content (truncate long inputs/outputs). Redact PII and secrets. Use log levels appropriately (DEBUG for development, INFO for production operations, WARN for recoverable issues, ERROR for failures). Set retention policies.

### AP-32: No Cost Tracking
**Category:** Observability & Monitoring
**Description:** Running agents in production without monitoring token usage, model costs, or compute expenses. No dashboards, no budgets, no alerts. The first indication of a cost problem is the monthly invoice.
**Why Harmful:** LLM API costs can spike unexpectedly due to: prompt changes that increase token count, traffic spikes, loops without termination, or model upgrade to a more expensive tier. Without real-time cost tracking, a single bug can generate a surprise bill of hundreds or thousands of dollars.
**Instead:** Track per-request token usage and cost. Aggregate into daily/weekly dashboards. Set budget alerts at 50%, 80%, and 100% of expected spend. Implement cost caps that degrade service rather than exceeding budget. Model routing (using cheaper models for simpler tasks) can save 27-55%.

### AP-33: Alert Fatigue
**Category:** Observability & Monitoring
**Description:** Too many alerts firing for too many metrics with too-sensitive thresholds. Every minor latency fluctuation triggers a page. The on-call engineer receives 50 alerts per day, most of which are false positives.
**Why Harmful:** When everything is an alert, nothing is an alert. Critical issues get lost in the noise. Engineers start ignoring alerts. Response time increases because the team cannot distinguish real problems from noise.
**Instead:** Alert on actionable conditions only. Tier alerts: page (P0/P1 -- system down, data breach), notify (P2 -- degraded performance, elevated error rate), log (P3 -- informational). Use anomaly detection over static thresholds. Require every alert to have a documented runbook. Review and prune alerts quarterly.

---

## Safety Anti-Patterns

### AP-34: Trust All Input
**Category:** Safety, Security & Guardrails
**Description:** No input validation or sanitization. User input is passed directly to the LLM prompt with no size limits, format checks, or content filtering. Agent inputs from tools or other agents are trusted implicitly.
**Why Harmful:** Prompt injection (#1 OWASP risk). Oversized inputs exhaust context windows. Malformed inputs cause parsing failures. Content that should be filtered (hate speech, PII, malicious instructions) reaches the model and may be reflected in output.
**Instead:** Validate all inputs: size limits (min/max length), format validation (expected structure), content filtering (known injection patterns, PII detection). Apply validation to user inputs, tool outputs, inter-agent messages, and RAG retrieval results.

### AP-35: Trust Agent Output
**Category:** Safety, Security & Guardrails
**Description:** Using agent output directly in SQL queries, shell commands, HTML templates, or API calls without validation or sanitization.
**Why Harmful:** LLM output is untrusted input (it can be manipulated via prompt injection). Using it directly in contexts that interpret code enables SQL injection, command injection, XSS, and other injection attacks. The OMNI-LEAK paper (2026) demonstrates data leakage through multi-agent output channels.
**Instead:** Treat all agent output as untrusted. Use parameterized queries for SQL. Use argument lists for shell commands. Escape HTML output. Validate against expected schemas. Apply output guardrails (PII detection, content filtering, system prompt leak detection) before exposing output to users or external systems.

### AP-36: Maximum Privilege
**Category:** Safety, Security & Guardrails
**Description:** Agents configured with admin/root access to all systems because "it's easier" or "we might need it later." A single API key with full permissions shared across all agents and tools.
**Why Harmful:** Violates OWASP's Excessive Agency (#6). If any agent is compromised (prompt injection, hallucination, bug), the blast radius is unlimited. 39% of companies report agents accessing unintended systems. The damage from a compromised admin credential is catastrophic.
**Instead:** Implement least privilege rigorously. Each agent gets scoped credentials for exactly the resources it needs. Read-only agents get read-only access. Create separate API keys per agent/tool. Document the permission matrix. Audit credential scope quarterly.

### AP-37: No Kill Switch
**Category:** Safety, Security & Guardrails
**Description:** No way to quickly disable a runaway agent. The system can only be stopped by deploying new code, restarting servers, or revoking API keys -- all of which take minutes to hours.
**Why Harmful:** When an agent malfunctions (looping without termination, producing harmful output, consuming excessive resources), every minute of continued operation increases damage. An agent creating hundreds of spam issues, sending incorrect emails, or making unauthorized API calls needs to be stopped in seconds, not minutes.
**Instead:** Implement a kill switch that can be activated in under 60 seconds: environment variable or feature flag that disables the system, API endpoint to pause agent processing, circuit breaker that auto-activates on anomalous behavior. Test the kill switch regularly. Document the activation procedure.

### AP-38: Security as Afterthought
**Category:** Safety, Security & Guardrails
**Description:** Building the entire agent system first, then "adding security" at the end. Guardrails, input validation, output filtering, and access controls are bolt-on features rather than architectural decisions.
**Why Harmful:** Security that is not designed in from the start is always incomplete. Retrofitting input validation into a system that passes raw strings everywhere requires touching every component. Adding access controls after the system assumes universal access requires architectural changes. The result is usually incomplete coverage with hidden gaps.
**Instead:** Security is a design requirement, not a feature. Define trust boundaries, input validation, output filtering, access controls, and audit logging in the architecture phase. Implement them alongside core functionality, not after.

### AP-39: Guardrails Without Testing
**Category:** Safety, Security & Guardrails
**Description:** Deploying guardrails (input filters, output validators, content blockers) without adversarial testing. Assuming the guardrails work because they are configured, not because they have been tested against realistic attacks.
**Why Harmful:** Guardrails that have not been adversarially tested provide false confidence. Prompt injection techniques evolve rapidly. A guardrail that blocks "ignore your instructions" may not block encoded variants, multi-turn attacks, or indirect injection through tool outputs.
**Instead:** Test every guardrail with adversarial inputs: known injection patterns, encoded attacks, multi-turn escalation, indirect injection via tool outputs. Use the Guardrails AI Index (benchmark comparing 24 guardrails across 6 categories) to select and evaluate guardrails. Update adversarial test cases quarterly.

---

## Ethics Anti-Patterns

### AP-40: Hidden AI
**Category:** Ethical & Responsible AI
**Description:** Users do not know they are interacting with an AI system. The agent impersonates a human, uses a human name, or provides no disclosure of its AI nature.
**Why Harmful:** Violates EU AI Act transparency requirements (enforceable August 2026, penalties up to 35M EUR). Erodes user trust when discovered. Prevents users from appropriately calibrating their trust in the system's output. Ethically deceptive.
**Instead:** Clearly disclose AI involvement in every user-facing interaction. Use system-level disclosure ("This analysis was generated by an AI agent") rather than requiring the AI to self-identify in each response (which it may fail to do). Design the UI to make AI involvement obvious.

### AP-41: No Harm Analysis
**Category:** Ethical & Responsible AI
**Description:** Deploying an agent system without considering potential negative impacts on affected populations. No analysis of who could be harmed, how, and what mitigations are in place.
**Why Harmful:** Agent systems in high-stakes domains (healthcare, finance, hiring, law enforcement) can cause real harm to real people. Without harm analysis, harmful impacts are discovered after deployment, when damage has already occurred. NIST AI RMF's Map function requires this analysis.
**Instead:** Before deployment, conduct a structured harm analysis: Who are the affected populations? What are the potential negative impacts? What is the severity and likelihood? What mitigations are in place? Document this analysis and review it quarterly.

### AP-42: Bias Blindness
**Category:** Ethical & Responsible AI
**Description:** No monitoring for biased outputs across user groups. The evaluation suite tests overall accuracy but never checks whether the system performs differently for different demographics, languages, or cultural contexts.
**Why Harmful:** LLMs inherit biases from training data. An agent that performs well on average may systematically disadvantage specific groups. Without bias monitoring, disparate impact goes undetected. Regulatory requirements (EU AI Act, NIST AI RMF) increasingly require bias assessment.
**Instead:** Include bias testing in the evaluation suite. Test the same scenarios with different demographic contexts. Monitor production outputs for distributional skew across user groups.

---

## Deployment Anti-Patterns

### AP-43: YOLO Deployment
**Category:** Deployment & Operations
**Description:** No staging environment. Code changes go directly from development to production. No canary deployment, no gradual rollout, no smoke tests in a production-like environment.
**Why Harmful:** Agent systems have more failure modes than traditional software: prompt regressions, model provider changes, tool API updates, and non-deterministic output. A change that passes unit tests may fail in production due to model behavior differences, rate limits, or data distribution differences.
**Instead:** Implement at minimum: a staging environment with the same model provider and tools, evaluation suite before deployment, canary deployment (route 5-10% of traffic to new version), and automatic rollback if error rate exceeds threshold.

### AP-44: No Rollback
**Category:** Deployment & Operations
**Description:** No ability to revert to a previous agent version when a deployment causes issues. Prompts are modified in place. Configuration is changed directly in production. There is no "last known good" state to return to.
**Why Harmful:** When a deployment causes issues (and it will), the response time is determined by how quickly you can fix forward. Without rollback capability, that means debugging and deploying a fix under pressure. With rollback, recovery takes minutes.
**Instead:** Version-control everything: code, prompts, configuration, evaluation cases. Tag releases. Maintain the ability to deploy any previous version within minutes. Use blue-green or canary deployment patterns. Test rollback procedures before you need them.

### AP-45: Monolithic Agent
**Category:** Deployment & Operations
**Description:** The entire agent system (all agents, orchestrator, tools, memory, and API layer) is a single deployment unit. Updating one agent requires redeploying everything. Scaling one component requires scaling everything.
**Why Harmful:** Deployment risk: changing one agent's prompt requires redeploying and retesting the entire system. Scaling waste: if only the research agent needs more capacity, you cannot scale it independently. Blast radius: a bug in one component takes down the entire system.
**Instead:** Design for independent deployment where complexity justifies it. At minimum, externalize prompts and configuration so they can be updated without code deployment. For larger systems, consider microservice-style architecture where individual agents or agent groups can be deployed, scaled, and rolled back independently.

---

## Documentation Anti-Patterns

### AP-46: Tribal Knowledge
**Category:** Documentation & Reproducibility
**Description:** Architecture decisions, operational procedures, and system behavior exist only in developers' heads. "Ask Sarah, she set up the agents" is the documentation strategy. No README, no architecture docs, no runbooks.
**Why Harmful:** Bus factor of 1. When the original developer is unavailable, no one can operate, debug, or extend the system. New team members cannot onboard effectively. Incident response is delayed because procedures are not documented.
**Instead:** Implement comprehensive documentation: README with purpose/architecture/quickstart (DOC-1), version-controlled prompts (DOC-2), pinned dependencies (DOC-3), configuration reference (DOC-4), evaluation methodology (DOC-5).

### AP-47: Unreproducible System
**Category:** Documentation & Reproducibility
**Description:** The system cannot be recreated from the repository alone. Dependencies are unpinned. Environment setup requires undocumented manual steps. Model provider configuration requires tribal knowledge.
**Why Harmful:** Cannot set up development environments. Cannot reproduce bugs. Cannot onboard new developers. Cannot recover from infrastructure failure. Fails the most basic reproducibility requirement of software engineering.
**Instead:** Pin all dependencies with exact versions. Document all environment variables with `.env.example`. Provide setup scripts or containerization (Docker/Compose). Include a "getting started" section that a new developer can follow from zero to running system in under 30 minutes.

### AP-48: Stale Docs
**Category:** Documentation & Reproducibility
**Description:** Documentation that was accurate when written but has not been updated as the system evolved. The architecture diagram shows 3 agents but there are now 5. The README describes deprecated configuration options.
**Why Harmful:** Stale documentation is worse than no documentation because it actively misleads. Developers make incorrect assumptions based on outdated information. Debugging time increases when the documented architecture does not match reality.
**Instead:** Treat documentation as code: update it in the same PR that changes functionality. Generate diagrams from code where possible (Mermaid in README, LangGraph graph visualization). Include documentation review in the PR checklist. Quarterly documentation audits to catch drift.
