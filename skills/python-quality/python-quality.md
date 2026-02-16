---
description: Run comprehensive Python code quality checks (lint, format, type, test, security, deps)
argument-hint: "<target-path> --fix"
allowed-tools: Bash, Read, Grep, Glob
---

Run a comprehensive Python code quality pipeline. Parse `$ARGUMENTS`:
- If `--fix` is present anywhere, enable **autofix mode** (tools auto-correct where possible).
- The remaining argument is the target path. Defaults to `.` if not provided.
- **Sanitize the target path:** reject any path containing shell metacharacters (`;`, `|`, `&`, `$`, backticks). Always wrap the target path in double quotes in all shell commands.

Execute all phases sequentially, producing a final structured report.

## Output Management (IMPORTANT — follow throughout all phases)

Tool output on real codebases can be enormous. To avoid overwhelming context:

- **General rule:** if any command produces more than 80 lines of output, show only the first 40 lines and the final summary line, then note `"... and N more (truncated)"`.
- **Ruff lint:** use `--output-format=concise` for compact one-line-per-violation output. If output exceeds 40 lines, show the first 40 and the final summary line (e.g., `Found N errors [M fixable]`).
- **Ruff format:** in normal mode, use `--check` **without** `--diff` to get just the list of files needing formatting. Only add `--diff` if 5 or fewer files need changes.
- **mypy/pyright/ty:** capture the summary line at the end (e.g., `Found 42 errors in 15 files`). Only show individual errors if count < 30.
- **pytest:** the `-q` flag keeps it concise. If output exceeds 80 lines, focus on the summary line.
- **vulture:** if > 40 items, report only the count.
- **JSON output (bandit, pip-audit, pip list):** read the JSON output and extract only the relevant summary (issue count, package names, severity levels). Never include raw JSON in the final report.

---

## Phase 1: Discovery

### 1a. Configuration files

Check for and read these files (if they exist) at the project root:
- `pyproject.toml` — note sections: `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`
- `setup.cfg`
- `.pre-commit-config.yaml`
- `ruff.toml` or `.ruff.toml`
- `.flake8`
- `mypy.ini` or `.mypy.ini`
- `tox.ini`
- `uv.lock`, `poetry.lock`, `Pipfile.lock`
- `.python-version`

### 1b. Pre-commit hook detection

From `.pre-commit-config.yaml`, extract hooks. Inspect both the `repo` URL and hook `id`:
- `ruff` / `ruff-pre-commit` (repo contains `astral-sh/ruff`) → covers Ruff check
- `ruff-format` → covers Ruff format
- `black` / `black-jupyter` → covers formatting
- `mypy` / `mirrors-mypy` → covers mypy
- `pyright` → covers pyright
- `pycodestyle` / `flake8` → covers pycodestyle
- `pydocstyle` → covers pydocstyle
- `bandit` → covers Bandit
- `isort` → covers import sorting

### 1c. Virtual environment detection (CRITICAL)

Many projects install tools only inside a virtualenv. Detect and configure the command prefix.

**Check in this order** (manager-based prefixes first — they handle env resolution automatically):

1. Check if `$VIRTUAL_ENV` is already set (venv is active) — tools are on PATH, no prefix needed.
2. If `uv.lock` exists → use `uv run` as prefix. However, `uv run` only works for tools in the project's dependencies. When checking tool availability, if `uv run {tool} --version` fails, also try bare `{tool} --version` (system PATH fallback) before declaring the tool missing.
3. If `poetry.lock` exists → use `poetry run` as prefix. Same fallback logic: if `poetry run {tool} --version` fails, try bare `{tool} --version`.
4. If none of the above matched, check for venv directories: `.venv/bin/python`, `venv/bin/python`, `.env/bin/python`. If found, resolve the venv bin directory to an **absolute path** (e.g., `/Users/me/project/.venv/bin/`) and prefix commands with it. This prevents breakage if commands run from a subdirectory. Same fallback: if the prefixed command fails, try bare command.
5. If nothing matched, use bare commands (system-level tools).

Store the resolved primary prefix and apply it to tool commands. Remember the fallback-to-system-PATH rule for every tool availability check.

### 1d. Ruff config detection

Determine whether the project has **lint-level** Ruff configuration:
- `has_ruff_lint_config = true` if ANY of these exist:
  - `ruff.toml` or `.ruff.toml` file exists
  - `pyproject.toml` contains `[tool.ruff.lint]` with `select` or `extend-select` keys
  - `pyproject.toml` contains `[tool.ruff]` with `select` or `extend-select` keys
- If `has_ruff_lint_config` is false, the skill will provide its own `--select` rules.

### 1e. Detect source layout

Identify the project's source directory for accurate type checking and coverage:
- If `pyproject.toml` has `[tool.coverage.run]` with `source`, record that as `SOURCE_DIR`.
- Else if a `src/` layout exists (directory `src/` with a Python package inside), set `SOURCE_DIR` to `src`.
- Else if there is exactly one top-level directory containing `__init__.py`, use that as `SOURCE_DIR`.
- Otherwise, **leave `SOURCE_DIR` unset**. (Do NOT default to `.` — that causes `--cov=.` which inflates coverage by including test files.)

### 1f. Verify Python files exist

Quick check: run `find "{TARGET_PATH}" -name "*.py" -type f -print -quit` (prints first match and stops). If no `.py` files are found, skip all subsequent phases and report: "No Python files found at target path. Nothing to analyze."

### 1g. Package manager and Python version

- Detect package manager: `uv.lock` → uv, `poetry.lock` → poetry, `Pipfile.lock` → pipenv, else pip.
- Record Python version: run `{CMD_PREFIX}python --version`.

### State to track

As you complete each phase, keep mental note of:
- `CMD_PREFIX`: command prefix from 1c (always an absolute path if venv-based)
- `TARGET_PATH`: sanitized target path (always quoted in commands)
- `SOURCE_DIR`: source directory from 1e, or unset
- `has_ruff_lint_config`: boolean from 1d
- `pre_commit_hooks`: list of hook IDs that **completed successfully** in Phase 2
- `missing_tools`: tools not installed (with pip install commands)
- Phase results and issues found (compiled into the report in Phase 8)

---

## Phase 2: Pre-commit

**Condition:** Only run if `.pre-commit-config.yaml` exists in the project root.

1. Check if pre-commit is installed:
   ```bash
   {CMD_PREFIX}pre-commit --version 2>/dev/null
   ```
   If not installed, record as missing (`pip install pre-commit`) and skip.

2. Run pre-commit. Use the Bash tool's timeout parameter set to 120000ms (2 minutes) to avoid hanging on first-run hook installation:
   ```bash
   {CMD_PREFIX}pre-commit run --all-files --show-diff-on-failure 2>&1 || true
   ```
   If the command times out, record: "Pre-commit timed out after 120s (may need hook installation) — skipping."

3. Parse the output. Note which **specific hooks** passed or auto-fixed files. If any hooks auto-fixed files, note: "Pre-commit auto-fixed files — subsequent phases will check the post-fix state."

4. Only mark a tool as "covered by pre-commit" if its corresponding hook **completed successfully** (passed or auto-fixed). A hook that failed or was skipped does NOT count as coverage.

---

## Phase 3: Lint, Format, Security, Imports & Complexity

**Strategy:** Use Ruff as the unified tool when available. Fall back to individual tools only when Ruff is not installed.

### 3a. Check for Ruff

```bash
{CMD_PREFIX}ruff --version 2>/dev/null
```

### If Ruff IS available (preferred path):

**Skip all of:** Black, pycodestyle, pydocstyle, Bandit, isort. Ruff covers them.

**Always run Ruff in Phase 3**, even if pre-commit also ran Ruff. Ruff is fast (~100ms on most projects), and re-running ensures consistent rule coverage — pre-commit hooks may use different `args` or rule sets. If pre-commit auto-fixed files, this run checks the post-fix state, which is useful.

**Linting:**

If `has_ruff_lint_config` is true (project has its own Ruff lint rules):
```bash
# Respect project config — do not pass --select
# In --fix mode:
{CMD_PREFIX}ruff check --output-format=concise --fix "{TARGET_PATH}" 2>&1 || true
# In normal mode:
{CMD_PREFIX}ruff check --output-format=concise "{TARGET_PATH}" 2>&1 || true
```

If `has_ruff_lint_config` is false (no project-level lint config):
```bash
# Provide sensible defaults
# In --fix mode:
{CMD_PREFIX}ruff check --select E,W,F,I,S,C90,UP,B,A,SIM --output-format=concise --fix "{TARGET_PATH}" 2>&1 || true
# In normal mode:
{CMD_PREFIX}ruff check --select E,W,F,I,S,C90,UP,B,A,SIM --output-format=concise "{TARGET_PATH}" 2>&1 || true
```

What the default rules cover:
- `E,W` — pycodestyle (PEP 8)
- `F` — pyflakes (undefined names, unused imports)
- `I` — isort (import sorting)
- `S` — flake8-bandit (security — replaces standalone Bandit)
- `C90` — mccabe (cyclomatic complexity, threshold 10)
- `UP` — pyupgrade (modernize Python syntax)
- `B` — flake8-bugbear (common bugs and design problems)
- `A` — flake8-builtins (shadowing builtins)
- `SIM` — flake8-simplify (simplification opportunities)

**Why `D` (pydocstyle) and `N` (pep8-naming) are excluded from defaults:**
- `D` rules produce hundreds of warnings on any project without a configured docstring convention (`google`, `numpy`, `pep257`). If the project's Ruff config includes `[tool.ruff.lint.pydocstyle]` with a `convention`, they will be included via the project-config path.
- `N` rules produce false positives with common patterns (unittest methods, library conventions).

**Formatting:**
```bash
# In --fix mode:
{CMD_PREFIX}ruff format "{TARGET_PATH}" 2>&1 || true
# In normal mode (no --diff to avoid enormous output; just list files):
{CMD_PREFIX}ruff format --check "{TARGET_PATH}" 2>&1 || true
```

Add to fix commands (with issue counts if applicable):
- `ruff check --fix .`
- `ruff format .`

### If Ruff is NOT available (fallback path):

Run individual tools. Each tool: check availability with `{CMD_PREFIX}tool --version 2>/dev/null` (with system PATH fallback per 1c), skip if not installed (record in `missing_tools`). Skip any tool whose pre-commit hook completed successfully.

**3b. Black:**
```bash
{CMD_PREFIX}black --check --diff "{TARGET_PATH}" 2>&1 || true
```

**3c. pycodestyle** (skip if flake8 ran via pre-commit):
```bash
{CMD_PREFIX}pycodestyle "{TARGET_PATH}" 2>&1 || true
```

**3d. Bandit** (security):
```bash
{CMD_PREFIX}bandit -r "{TARGET_PATH}" -f json 2>&1 || true
```
Read the output. Bandit writes JSON to stdout and logging to stderr — both may appear in the output. Look for the JSON object with a `results` key. An empty `results` array means no issues (PASS). If the output contains no valid JSON, Bandit likely crashed — record as "Bandit error" and note the error message.

For security findings, reference:
- B101 (assert): stripped in optimized bytecode, never use for access control
- B301/B302 (pickle): arbitrary code execution risk
- B608 (SQL injection): use parameterized queries
- B403 (subprocess): shell injection risk

**3e. isort:**
```bash
{CMD_PREFIX}isort --check-only --diff "{TARGET_PATH}" 2>&1 || true
```

---

## Phase 4: Type Check

**Skip if pre-commit already ran the type checker successfully.**

Detect and use the best available type checker. Priority order (most reliable first):

1. **mypy** (most established, best ecosystem support):
   ```bash
   {CMD_PREFIX}mypy --version 2>/dev/null
   ```

2. **pyright** (faster, checks unannotated code by default):
   ```bash
   {CMD_PREFIX}pyright --version 2>/dev/null
   ```

3. **ty** (fastest, but still in beta — results may be incomplete):
   ```bash
   {CMD_PREFIX}ty --version 2>/dev/null
   ```
   If ty is the only checker available, note in the report: "ty is beta — results may have gaps."

If none are installed, record as missing (`pip install mypy`).

### mypy-specific hardening (IMPORTANT):

If mypy is the selected checker:
- If **no mypy config exists** (no `[tool.mypy]` in pyproject.toml, no `mypy.ini`, no `.mypy.ini`, no mypy section in `setup.cfg`), add these flags:
  - `--ignore-missing-imports` — suppresses noise from untyped third-party libraries
  - `--exclude '(\.venv|venv|\.env|\.git|node_modules|build|dist|__pycache__)'` — prevents scanning non-source directories
- If a mypy config exists, trust it and run without extra flags.
- **Never** run `--install-types` — it modifies the environment without user consent.

```bash
# With config:
{CMD_PREFIX}mypy "{TARGET_PATH}" 2>&1 || true
# Without config:
{CMD_PREFIX}mypy --ignore-missing-imports --exclude '(\.venv|venv|\.env|\.git|node_modules|build|dist|__pycache__)' "{TARGET_PATH}" 2>&1 || true
```

---

## Phase 5: Tests + Coverage

```bash
{CMD_PREFIX}pytest --version 2>/dev/null
```
If not installed, record as missing (`pip install pytest`) and skip.

### Determine test path

Do NOT blindly pass `$TARGET_PATH` to pytest — tests often live in a different directory:
- If `[tool.pytest.ini_options]` in `pyproject.toml` has `testpaths`, use those paths.
- Else if `$TARGET_PATH` is `.`, let pytest use its default discovery (pass no path argument).
- Else if `$TARGET_PATH` points to a source directory (not `tests/`), check if `tests/` or `test/` exists at the project root and use that instead.
- Otherwise, pass `$TARGET_PATH` as-is.

### Determine coverage source

Check if pytest-cov is available:
```bash
{CMD_PREFIX}python -c "import pytest_cov" 2>/dev/null
```

Coverage is only included if `SOURCE_DIR` is set (from Phase 1e). If `SOURCE_DIR` is unset, skip coverage — running `--cov=.` inflates numbers by including test files.

### Run tests

If pytest-cov is available AND `SOURCE_DIR` is set:
```bash
{CMD_PREFIX}pytest {TEST_PATH} --tb=short -q --cov="{SOURCE_DIR}" --cov-report=term:skip-covered --cov-branch --cov-fail-under=0 2>&1 || true
```
Notes:
- `term:skip-covered` omits files with 100% coverage from the report, keeping output compact. The overall percentage is still shown.
- `--cov-fail-under=0` overrides any project-level `fail_under` threshold so low coverage doesn't mask actual test pass/fail results in this pipeline.

If pytest-cov is unavailable or `SOURCE_DIR` is unset:
```bash
{CMD_PREFIX}pytest {TEST_PATH} --tb=short -q 2>&1 || true
```

Record: tests passed, failed, skipped, errors, and coverage percentage (if available). If pytest-cov is missing, add to missing tools: `pip install pytest-cov` (informational).

---

## Phase 6: Dependency Audit

### 6a. Vulnerability scan

```bash
{CMD_PREFIX}pip-audit --version 2>/dev/null
```
If not installed, record as missing (`pip install pip-audit`) and skip.

If installed:
```bash
{CMD_PREFIX}pip-audit --format=json 2>&1 || true
```
Read the output. Look for valid JSON with a `dependencies` key. If the output contains no valid JSON, pip-audit likely failed — record the error message. For successful runs, extract vulnerability count and affected packages. Add upgrade commands to fix commands.

### 6b. Outdated dependencies (informational)

For uv-managed projects, use the built-in `uv pip` subcommand (no `run` prefix needed):
```bash
uv pip list --outdated --format=json 2>/dev/null || true
```

For all other projects:
```bash
{CMD_PREFIX}pip list --outdated --format=json 2>/dev/null || true
```

Read the JSON. If more than 20 outdated packages, report only the count and the 5 with the largest version gap. This is **informational only** — never mark as failure.

---

## Phase 7: Dead Code Detection (Optional/Informational)

```bash
{CMD_PREFIX}vulture --version 2>/dev/null
```
If not installed, note in missing tools (`pip install vulture`) and skip. This phase is optional.

If installed:
```bash
{CMD_PREFIX}vulture "{TARGET_PATH}" --min-confidence 80 2>&1 || true
```

Mark all results as **informational** (severity: LOW). Dead code detection has inherent false positives from dynamic imports, plugin systems, framework magic (Django models, Flask routes, pytest fixtures, etc.).

---

## Phase 8: Report

Run `{CMD_PREFIX}python --version 2>&1` if not already captured.

Produce this structured summary:

```
=== PYTHON QUALITY REPORT ===
Target: <target path>
Mode: <normal | autofix>
Python: <version>
Env: <venv (.venv) | uv | poetry | system>

--- Phase Results ---
1. Discovery:            OK    — <config files found, env detected>
2. Pre-commit:           <PASS | FAIL | SKIP | TIMEOUT>  — <N hooks passed, M failed>
3. Lint/Format/Security: <PASS | FAIL | SKIP>  — <tool(s) used>: <issue counts by category>
4. Type Check:           <PASS | FAIL | SKIP>  — <tool used>: <error count>
5. Tests + Coverage:     <PASS | FAIL | SKIP>  — <passed/failed/skipped> (coverage: <N%> | n/a)
6. Dep Audit:            <PASS | FAIL | SKIP>  — <vulnerability count>, <N outdated>
7. Dead Code:            <INFO | SKIP>  — <N unused items found>

--- Missing Tools ---
<list each missing tool with its pip install command, or "None — all tools available">
Install all: pip install <space-separated list>

--- Top 5 Issues ---
<Prioritized by severity:
 1. Security vulnerabilities / dependency CVEs (HIGH)
 2. Test failures (HIGH)
 3. Type errors (MED)
 4. Lint errors — bugs/bugbear (MED)
 5. Style/format issues (LOW)
Format:
 N. [RULE_CODE] description at FILE:LINE (severity: HIGH|MED|LOW)
If fewer than 5 issues, list all. If no issues: "No issues found.">

--- Fix Suggestions ---
<For each top issue, a concrete fix:
 1. [S105] hardcoded-password-string at auth.py:42
    FIX: password = os.environ["DB_PASSWORD"]
 2. [D100] Missing docstring at utils.py:1
    FIX: Add module docstring
If no issues: omit this section entirely.>

--- Quick Fix Commands ---
<Copy-pasteable commands with {CMD_PREFIX} resolved to actual prefix:>
ruff check --fix .                    # Auto-fix N linting issues
ruff format .                         # Auto-format N files
pip install --upgrade PKG>=X.Y        # Fix CVE-YYYY-NNNNN
<If in autofix mode: "Auto-fix already applied. N issues remain requiring manual fixes.">
<If no fixes needed: "No auto-fixable issues found.">

--- Verdict ---
<PASS | WARN | FAIL>
FAIL if: any HIGH severity security issue, any test failure, any dependency vulnerability with known exploit
WARN if: medium-severity lint issues, coverage < 60%, outdated deps, missing tools
PASS if: all clean or only LOW informational items
=== END REPORT ===
```

**Important notes:**
- All paths in shell commands MUST be wrapped in double quotes.
- All `|| true` suffixes prevent a failing tool from halting the pipeline.
- Group issues by tool and sort by severity.
- When Ruff has project-level lint config, respect it — do not pass `--select`.
- In autofix mode, report what was auto-fixed and what remains as manual work.

**Single-file target:** If `$TARGET_PATH` is a specific `.py` file (not a directory):
- Ruff check, Ruff format, mypy, pyright, ty, vulture, bandit: pass the file path directly — all support single-file arguments.
- pytest: only pass the file to pytest if it matches `test_*.py` or `*_test.py`. Otherwise, use default test discovery (no path argument) and skip coverage.
- pip-audit, outdated deps: run as normal (they audit the environment, not individual files).
- pre-commit: run as normal (`--all-files` is independent of the target argument).
- Coverage: skip `--cov` for single-file targets (coverage of one file requires knowing its importable module name).
