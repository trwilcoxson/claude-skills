# Claude Code Skills

Custom slash commands (skills) for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

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
