# Claude Code Skills

Custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that provide specialized workflows, domain expertise, and tool integrations.

> **Security assessment moved.** The threat-model skill and the paired compliance / privacy
> assessment skills, their specialist agents, the evaluation harness, and the OpenSpec design now live
> in their own project: **[trwilcoxson/threat-model-suite](https://github.com/trwilcoxson/threat-model-suite)**.
> This repo now holds general-purpose skills only.

## Available Skills

### `/python-quality` — Python Code Quality Pipeline

> **Design philosophy:** LLMs approximate pattern matching and produce different results each run. Static analysis tools (`ruff`, `mypy`, `pytest`, `pip-audit`) produce verified, deterministic output. This skill runs deterministic tools first, then hands the results to the LLM for prioritization and reasoning.

Runs comprehensive Python code quality checks in a single invocation. Orchestrates lint, format, type check, test, security scan, dependency audit, and dead code detection with smart tool deduplication.

**Features:**
- Unified Ruff-first strategy (replaces Black, pycodestyle, pydocstyle, Bandit, isort) with fallback to individual tools
- Virtual environment auto-detection (venv, uv, poetry)
- Pre-commit integration with smart deduplication
- `--fix` mode for auto-correction
- Type checking with mypy/pyright/ty priority chain
- Test execution with coverage reporting (pytest-cov)
- Security scanning (Ruff S rules / Bandit fallback)
- Dependency vulnerability audit (pip-audit) + outdated check
- Dead code detection (vulture)
- Structured report with severity-prioritized issues, fix suggestions, and PASS/WARN/FAIL verdict

**Usage:**
```
/python-quality              # Check current directory
/python-quality src/         # Check specific path
/python-quality --fix        # Auto-fix what's possible
/python-quality src/ --fix   # Both
```

### `agentic-ai-requirements` — Agentic AI System Assessment

Assess, design, and score agentic AI systems against a comprehensive enterprise-grade requirements framework. Covers 12 categories, 88+ requirements, and MUST/SHOULD/MAY priority levels. Grounded in Feb 2026 state-of-the-art across LangGraph, CrewAI, Pydantic AI, Google ADK, OpenAI Agents SDK, Claude Agent SDK, DSPy, MCP/A2A protocols, NIST AI RMF, EU AI Act, and OWASP Top 10 for LLMs.

**Modes:**
- **ASSESS** — Evaluate an existing agentic AI codebase (4-phase: reconnaissance → requirement mapping → anti-pattern detection → scored report)
- **DESIGN** — Architect a new agent system against the requirements framework
- **CHECKLIST** — Lightweight quick-reference scoring (30 MUST + 36 SHOULD items)

**Usage:**
```
Assess my agent system against agentic AI requirements
Design an agent system for [use case]
Run the agentic AI checklist against this project
```

### `software-architect` — Software Architecture Assistant

Comprehensive architecture assistant covering the full lifecycle of software design decisions. Auto-detects 7 modes based on user intent, with 12 deep-reference files loaded progressively.

**Modes:** PLAN (greenfield design), REVIEW (health rating), SCORECARD (elite 9-section review), DECIDE (ADRs, MADR 3.0), DOCUMENT (C4/arc42/ADRs from code), DEBT (SQALE technical-debt assessment), MIGRATE (Strangler Fig, Branch by Abstraction, Parallel Run).

**Usage:**
```
Design the architecture for [system]
Review the architecture of this codebase
Run the architecture scorecard against this system
Plan a migration from monolith to microservices
```

### `grill-my-architecture-docs` — Architecture Doc Completeness Grilling

Relentlessly interviews you about a software architecture document through a chosen stakeholder lens until the doc is complete enough for that audience to sign off — one question at a time, recommending an answer for each, and writing settled answers back into the doc inline. Each lens has its own enterprise-grade rubric: a security grill is a full threat model, a finops grill is a cost and unit-economics audit. Reads local files or pulls the page from Confluence/Jira via the Atlassian MCP. It builds a context brief on the system before applying any rubric, and gives every rubric item an explicit verdict (gap / covered / not-applicable) so no category is silently skipped.

**Modes:** SECURITY (STRIDE-per-element + assume-breach lateral movement, annotated DFDs, identity, network, cloud landing zone, controls-to-framework mapping), FINOPS (cost drivers, unit economics, multi-year forecast, spend guardrails), COMPLIANCE (GDPR / SOC 2 / HIPAA / PCI data governance + audit evidence), RELIABILITY (SLOs, failure modes, tested DR/failover, degraded modes), PRODUCT (value, scope, metrics, customer SLAs, ownership), ENGINEERING (interface contracts, delivery semantics, stability surface), DATA (event taxonomy, schemas, lineage, data contracts), ARCHITECTURE (target-state alignment, ADRs, lock-in/exit, legacy sunset). No mode runs a cross-cutting triage that scores every lens.

**Usage:**
```
/grill-my-architecture-docs security ./design.md
/grill-my-architecture-docs finops "Payments platform page in Confluence"
/grill-my-architecture-docs                     # cross-cutting triage → recommends a deep lens
```

## Installation

Each skill is a directory you copy into your Claude Code skills folder:

```bash
# Global (all projects)
cp -r skills/python-quality             ~/.claude/skills/python-quality
cp -r skills/agentic-ai-requirements    ~/.claude/skills/agentic-ai-requirements
cp -r skills/software-architect         ~/.claude/skills/software-architect
cp -r skills/grill-my-architecture-docs ~/.claude/skills/grill-my-architecture-docs
```

Then restart Claude Code or start a new session.

## Structure

```
skills/
  python-quality/
    python-quality.md     # The skill file
  agentic-ai-requirements/
    SKILL.md              # 3-mode assessment framework with progressive reference loading
    references/           # requirements, patterns, safety, compliance, anti-patterns
  software-architect/
    SKILL.md              # 7-mode architecture assistant with progressive reference loading
    references/           # patterns, C4, ADR, arc42, debt, fitness, migration
  grill-my-architecture-docs/
    SKILL.md              # mode router + shared grill protocol (context brief, per-item verdicts)
    modes/                # 8 per-stakeholder rubrics + overview triage, loaded one at a time
```

## Related

- **[threat-model-suite](https://github.com/trwilcoxson/threat-model-suite)** — the agentic security-assessment system (threat modeling + privacy + compliance), its specialist agents, the reference-free evaluation harness, and the OpenSpec design.

## License

MIT
