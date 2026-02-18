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

Then restart Claude Code or start a new session. The skill will appear in autocomplete when you type `/`.

## Structure

```
skills/
  threat-model/
    SKILL.md              # Orchestration guide + 8-phase methodology
    references/           # 11 reference files (frameworks, mermaid, templates)
  python-quality/
    python-quality.md     # The skill file
```

## Related

- **[claude-agents](https://github.com/trwilcoxson/claude-agents)** — Specialist agent definitions for the threat-model pipeline (security-architect, report-analyst, code-review-agent, privacy-agent, grc-agent, validation-specialist). Includes the [architecture design document](https://github.com/trwilcoxson/claude-agents/blob/main/docs/ARCHITECTURE.md).

## License

MIT
