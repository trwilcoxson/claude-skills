# threat-model — reliability run: OWASP crAPI (polyglot microservices)

The scale + polyglot test. [crAPI](https://github.com/OWASP/crAPI) is a ~14 MB, ~900-file
intentionally vulnerable microservices app spanning **Java/Spring, Go, Python/Django+Flask, and
TypeScript/React**, with a MongoDB + Postgres data tier, a **LangGraph LLM chatbot**, and an **MCP
tool server**. Run through the same harness with **zero code changes** (only `targets/crapi.yaml`).
3 runs, Claude Opus 4.8, no answer key.

## Verdict

**The harness and skill scale.** On a large polyglot system the deterministic contract still held on
every run, recon stayed complete, the high-severity core was stable, and the skill found both the
classic API vulnerabilities **and** the AI/agentic threats — with the same machinery used on a
9-file web app.

## Deterministic contract (per run) — held on every run

| Run | Structure | Consistency | Grounding | Coverage | Findings | Defects |
|---|---|---|---|---|---|---|
| 1 | pass | pass | 1.00 | 1.00 | 29 | 0 |
| 2 | pass | pass | 1.00 | 1.00 | 28 | 0 |
| 3 | pass | pass | 1.00 | 1.00 | 20 | 0 |

`severity == band(L×I)` held on every finding; every recon element resolved across the four
language trees; every discovered surface was addressed. **Recon completeness: 0 missed subsystems** —
the auditor confirmed recon enumerated all the microservices (web, identity, community, workshop,
chatbot, MCP server, gateway, mailhog).

## Stability (LLM-matched)

**16 of 28 distinct high-severity issues in all 3 runs; overlap 0.68.** The stable core spans the
whole app: JWT algorithm confusion, committed RSA signing key → JWT forgery, OTP-reset with no rate
limit (account takeover), BOLA on vehicle location / service requests / shop orders, OS command
injection in video conversion, BFLA on the admin video-delete endpoint, NoSQL operator injection in
validate-coupon, SQL injection in apply_coupon, SSRF via contact_mechanic, and hardcoded credentials
— i.e. crAPI's documented BOLA/BFLA/injection/JWT challenges, found reliably.

## AI / agentic coverage

On crAPI's LLM components the skill reliably surfaced the agentic threat class (stable across runs):
**excessive agency** (over-permissioned agent with terminal/SQL/MCP tools), **indirect prompt
injection / data exfiltration** via forum/RAG content into the agent, **MCP server auth bypass**, and
a **confused-deputy** chain where MCP/chatbot tools call the backend with a hardcoded admin API key.
This exercises the skill's AI/ML Security section on a real agent system.

## Reasoning quality (judged) & recall

Mean soundness **1.0** (proportionate, every finding traced to real source across the four services).
The red team confirmed **3 recall gaps** — a CRITICAL unauthenticated path-traversal/arbitrary-file
read in the workshop report download, and two BOLA/BFLA gaps (mechanic ServiceRequestView, global
product creation) — different real issues than the model surfaced, generated from the target.

## Why this matters

NodeGoat (9-file web app), TerraGoat (Terraform IaC), and crAPI (4-language microservices + LLM
agent) are three very different systems. The same reference-free harness produced a coherent
reliability profile on all three with no per-target tuning — deterministic contract intact, stable
crown-jewel core, real recall gaps. Adding a target is still just a `targets/*.yaml` and a clone.
