# Claude Code Skills

Custom slash commands (skills) for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Why Deterministic Tools + LLM

LLMs cannot reliably lint code. They approximate pattern matching across thousands of lines, miss real bugs, hallucinate nonexistent ones, and produce different results on every run. They cannot execute tests, compute branch coverage, trace types through import chains, or check a live CVE database for vulnerable dependencies.

Static analysis tools can. `ruff check` produces the same verified output every time. `mypy` builds a full type graph and proves correctness. `pytest` actually runs the code. `pip-audit` queries real vulnerability databases. These are facts, not opinions.

What LLMs *are* good at: prioritizing a wall of 500 warnings, explaining why a finding matters, suggesting concrete fixes, and catching architectural problems no linter can detect — bad abstractions, SRP violations, unclear naming, wrong design patterns.

These skills combine both. Deterministic tools provide the ground truth. The LLM reasons over it. You get 100% of static analysis findings plus architectural judgment that tools can't provide.

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

## Installation

Copy any skill's `.md` file to your Claude Code commands directory:

```bash
# Global (available in all projects)
cp skills/python-quality/python-quality.md ~/.claude/commands/python-quality.md

# Project-specific
cp skills/python-quality/python-quality.md .claude/commands/python-quality.md
```

Then restart Claude Code or start a new session. The skill will appear in autocomplete when you type `/`.

## Structure

```
skills/
  python-quality/
    python-quality.md    # The skill file (copy to ~/.claude/commands/)
```

## License

MIT
