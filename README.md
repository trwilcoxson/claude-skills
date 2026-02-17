# Claude Code Skills

Custom slash commands (skills) for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Why Deterministic Tools + LLM

LLMs cannot reliably lint code. They approximate pattern matching across thousands of lines, miss real bugs, hallucinate nonexistent ones, and produce different results on every run. They cannot execute tests, compute branch coverage, trace types through import chains, or check a live CVE database for vulnerable dependencies.

Static analysis tools can. `ruff check` produces the same verified output every time. `mypy` builds a full type graph and proves correctness. `pytest` actually runs the code. `pip-audit` queries real vulnerability databases.

LLMs are good at prioritizing a wall of 500 warnings, explaining why a finding matters, suggesting concrete fixes, and catching architectural problems no linter can detect — bad abstractions, SRP violations, unclear naming, wrong design patterns.

These skills run deterministic tools first, then hand the results to the LLM for prioritization and reasoning. You get full static analysis coverage plus architectural judgment.

## Available Skills

### `/python-quality` — Python Code Quality Pipeline

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

### `/threat-model` — Architectural Threat Modeling

Produces an architectural threat model with Mermaid data flow diagrams, STRIDE-LM threat identification, PASTA attack simulation, and OWASP Risk Rating prioritization.

**Features:**
- 8-phase structured analysis (reconnaissance through final report)
- Two-pass Mermaid diagrams: structural DFD + risk overlay
- STRIDE-LM coverage across all components (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege, Lateral Movement)
- PASTA likelihood/impact scoring mapped to OWASP Risk Rating severity bands
- MITRE ATT&CK and CWE cross-referencing
- Remediation roadmap with wave-based prioritization
- Designed for use by the [security-architect agent](https://github.com/trwilcoxson/claude-agents)

**Included files:**
- `SKILL.md` — Main skill definition with 8-phase methodology
- `references/frameworks.md` — MITRE ATT&CK, CWE, OWASP reference tables
- `references/mermaid-conventions.md` — Mermaid diagram syntax and styling standards
- `references/analysis-checklists.md` — Phase-specific validation checklists
- `report-template.md` — Deterministic report template enforcing consistent section ordering, table structures, and cross-reference integrity across all runs

**Usage:**
```
/threat-model                # Run against current project
```

## Installation

Copy any skill's directory to your Claude Code skills directory:

```bash
# Global (available in all projects)
cp -r skills/python-quality ~/.claude/skills/python-quality
cp -r skills/threat-model ~/.claude/skills/threat-model

# Project-specific
cp -r skills/python-quality .claude/skills/python-quality
cp -r skills/threat-model .claude/skills/threat-model
```

Then restart Claude Code or start a new session. The skill will appear in autocomplete when you type `/`.

## Structure

```
skills/
  python-quality/
    python-quality.md                      # The skill file
  threat-model/
    SKILL.md                               # Main skill definition (8-phase methodology)
    report-template.md                     # Deterministic report template
    references/
      frameworks.md                        # MITRE ATT&CK, CWE, OWASP tables
      mermaid-conventions.md               # Diagram syntax standards
      analysis-checklists.md               # Phase validation checklists
```

## License

MIT
