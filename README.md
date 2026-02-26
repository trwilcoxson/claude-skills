# Claude Code Skills

Custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that provide specialized workflows, domain expertise, and tool integrations.

## Available Skills

### `threat-model` — Architectural Threat Modeling

Produces architectural threat models with Mermaid data flow diagrams, STRIDE-LM threat identification, PASTA attack simulation, and OWASP Risk Rating prioritization. Orchestrates a pipeline of [specialist agents](https://github.com/trwilcoxson/claude-agents) for comprehensive security assessments.

**Features:**
- 8-phase structured methodology (reconnaissance through final report)
- Solo mode (threat model + report) or Team mode (adds privacy, compliance, code review agents)
- Mermaid DFDs with 4-layer structural + risk overlay approach
- Four output formats: HTML (interactive), Word (.docx), PDF, and Executive PPTX
- Cross-agent validation and deduplication

**Usage:**
```
Run a threat model on [target]
```

**Dependencies:** Requires [claude-agents](https://github.com/trwilcoxson/claude-agents) for the specialist agent definitions. See the [architecture doc](https://github.com/trwilcoxson/claude-agents/blob/main/docs/ARCHITECTURE.md) for the full system design.

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

**Categories:** Agent Architecture, Reasoning and Decision Logic, Memory and State, Tool Use and Integration, Multi-Agent Coordination, Evaluation and Testing, Observability and Monitoring, Safety and Security, Ethics and Responsible AI, Deployment and Operations, Documentation and Reproducibility, Governance and Compliance.

**Usage:**
```
Assess my agent system against agentic AI requirements
Design an agent system for [use case]
Run the agentic AI checklist against this project
```

### `software-architect` — Software Architecture Assistant

Comprehensive architecture assistant covering the full lifecycle of software design decisions. Auto-detects 7 modes based on user intent, with 12 deep-reference files loaded progressively.

**Modes:**
- **PLAN** — Greenfield architecture design (7 phases: context → QA workshop → pattern selection → domain decomposition → spec → governance → output)
- **REVIEW** — Architecture assessment with health rating (CRITICAL → EXCELLENT)
- **SCORECARD** — Elite 9-section design review (53 items, 4 STOP-SHIP triggers)
- **DECIDE** — Architecture decision records (MADR 3.0)
- **DOCUMENT** — C4 diagrams, arc42, ADRs from codebase analysis
- **DEBT** — Technical debt assessment with SQALE taxonomy and quantification
- **MIGRATE** — Migration planning (Strangler Fig, Branch by Abstraction, Parallel Run)

**Key principles:** Modular monolith as default, boundaries first, reliability as a feature, automated fitness functions, SLO-driven observability. Covers 2026 patterns including cell-based architecture, AI-native architecture, and platform engineering.

**Usage:**
```
Design the architecture for [system]
Review the architecture of this codebase
Run the architecture scorecard against this system
Should I use microservices or a modular monolith?
Assess the technical debt in this project
Plan a migration from monolith to microservices
```

## Installation

### threat-model

The threat-model skill is installed as a Claude Code skill (not a slash command). Copy the skill directory:

```bash
# Global
cp -r skills/threat-model ~/.claude/skills/threat-model
```

You also need the [specialist agents](https://github.com/trwilcoxson/claude-agents) installed. See that repo's README for agent installation.

### python-quality

Copy the skill directory:

```bash
# Global (available in all projects)
cp -r skills/python-quality ~/.claude/skills/python-quality

# Project-specific
cp -r skills/python-quality .claude/skills/python-quality
```

### agentic-ai-requirements

Copy the skill directory:

```bash
# Global (available in all projects)
cp -r skills/agentic-ai-requirements ~/.claude/skills/agentic-ai-requirements

# Project-specific
cp -r skills/agentic-ai-requirements .claude/skills/agentic-ai-requirements
```

### software-architect

Copy the skill directory:

```bash
# Global (available in all projects)
cp -r skills/software-architect ~/.claude/skills/software-architect

# Project-specific
cp -r skills/software-architect .claude/skills/software-architect
```

Then restart Claude Code or start a new session.

## Structure

```
skills/
  threat-model/
    SKILL.md              # Orchestration guide + 8-phase methodology
    references/           # 11 reference files (frameworks, mermaid, templates)
  agentic-ai-requirements/
    SKILL.md              # 3-mode assessment framework with progressive reference loading
    references/           # 8 reference files (requirements, patterns, safety, compliance, anti-patterns)
  python-quality/
    python-quality.md     # The skill file
  software-architect/
    SKILL.md              # 7-mode architecture assistant with progressive reference loading
    references/           # 12 reference files (patterns, C4, ADR, arc42, debt, fitness, migration)
```

## Related

- **[claude-agents](https://github.com/trwilcoxson/claude-agents)** — Specialist agent definitions for the threat-model pipeline (security-architect, report-analyst, code-review-agent, privacy-agent, grc-agent, validation-specialist). Includes the [architecture design document](https://github.com/trwilcoxson/claude-agents/blob/main/docs/ARCHITECTURE.md).

## License

MIT
