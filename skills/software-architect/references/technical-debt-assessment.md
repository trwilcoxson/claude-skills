# Technical Debt Assessment Methodology

A systematic framework for identifying, quantifying, and prioritizing technical debt across a codebase. This reference provides detection signals, quantification tools, and reporting templates for conducting thorough debt assessments.

---

## What is Technical Debt?

Technical debt is the implied cost of future rework caused by choosing an expedient solution now instead of a better approach that would take longer. The term, coined by Ward Cunningham, draws a deliberate analogy to financial debt: you borrow against the future to ship faster today, but you pay interest on that loan in the form of increased maintenance effort, slower feature delivery, and elevated risk of defects.

Technical debt is not inherently bad. Just as a business may take on financial debt strategically, a team may consciously accept technical shortcuts to meet a market window. The problem arises when debt is invisible, unmanaged, or allowed to compound unchecked.

### Martin Fowler's Technical Debt Quadrant

Fowler categorizes technical debt along two axes: **deliberate vs. inadvertent** and **prudent vs. reckless**. Understanding which quadrant a debt item falls into shapes how you respond to it.

| | Prudent | Reckless |
|---|---------|----------|
| **Deliberate** | "We know this is a shortcut, but we must ship now and will address it next sprint." The team understands the tradeoff and accepts it consciously. Typical example: skipping an abstraction layer to meet a deadline. | "We don't have time for design." The team knows they are cutting corners but has no plan to address it. Example: copy-pasting an entire module instead of extracting shared logic. |
| **Inadvertent** | "Now we know how we should have built it." The team did its best with available knowledge, but learning revealed a better design. Example: realizing after six months that the initial data model doesn't support new requirements. | "What's a layered architecture?" The team doesn't know enough to recognize it is accruing debt. Example: business logic scattered across controllers, templates, and database triggers. |

Prudent debt (both deliberate and inadvertent) is a natural part of software development. Reckless debt, especially inadvertent-reckless, is the most dangerous because it compounds silently.

### Why It Matters

Technical debt compounds like financial debt. A single shortcut may cost 30 minutes to address today. Left for six months, it may cost three days because other code has been built on top of it, tests depend on its behavior, and the original author has left the team. The compounding nature means that the cost of remediation grows nonlinearly with time. Teams that ignore debt eventually hit a "debt wall" where feature velocity drops to near zero because every change requires navigating a minefield of accumulated shortcuts.

---

## SQALE Taxonomy

The SQALE (Software Quality Assessment based on Lifecycle Expectations) method provides a standardized way to categorize technical debt. Each category maps to a quality attribute, and debt items are classified by the attribute they degrade.

### Testability

Debt that makes the system harder to verify through automated testing.

- **Missing tests**: Critical paths with no unit or integration coverage. Business logic that can only be verified manually.
- **Untestable code**: Functions with hidden dependencies (global state, singletons, hardcoded external calls) that cannot be isolated for testing. Constructors that perform I/O. Methods with 10+ parameters.
- **Test anti-patterns**: Tests that depend on execution order. Tests that hit real databases or external services without mocking. Tests with no assertions (tests that "pass" by not throwing). Brittle snapshot tests that break on any UI change.

### Reliability

Debt that increases the probability of failures in production.

- **Error handling gaps**: Bare `except:` or `catch(Exception)` blocks that swallow all errors. Missing error handling on network calls. No retry logic for transient failures. Missing circuit breakers on external dependencies.
- **Resource leaks**: Database connections not closed in `finally` blocks. File handles left open. Thread pools that grow without bound. Memory allocated in loops without release.
- **Race conditions**: Shared mutable state accessed from multiple threads without synchronization. Check-then-act patterns without locking. Non-atomic read-modify-write sequences on shared resources.

### Changeability

Debt that makes the system resistant to modification.

- **Tight coupling**: Module A cannot function without Module B, and vice versa. Changes to one module cascade across multiple others. Concrete dependencies instead of interfaces.
- **God classes**: Single classes with 2,000+ lines, 50+ methods, and responsibilities spanning multiple domains. These attract more code because developers add functionality to the class that "already does everything."
- **Feature envy**: Methods that use more data from other classes than from their own. A sign that logic is in the wrong place.
- **Missing abstractions**: Repeated conditional logic (if type == X then ... elif type == Y then ...) instead of polymorphism. String-typed fields used where enums or value objects belong.

### Efficiency

Debt that degrades runtime performance.

- **N+1 queries**: ORM code that fetches a list of parent records and then issues a separate query for each parent's children. Common in Django, Rails, and SQLAlchemy without eager loading.
- **Unbounded collections**: API endpoints that return all records without pagination. In-memory lists that grow without limit. Missing `LIMIT` clauses on database queries.
- **Missing caching**: Expensive computations repeated on every request. Database queries for data that changes infrequently. No HTTP cache headers on static assets.
- **Memory leaks**: Event listeners registered but never removed. Growing caches without eviction policies. Closures that capture large objects unnecessarily.

### Security

Debt that exposes the system to attack.

- **Hardcoded secrets**: API keys, passwords, tokens, or connection strings embedded in source code or configuration files committed to version control.
- **SQL injection**: String concatenation or f-strings used to build SQL queries instead of parameterized queries or ORM methods.
- **Missing input validation**: User-supplied data passed directly to database queries, file system operations, or shell commands without sanitization. Missing request body validation on API endpoints.
- **Outdated dependencies**: Libraries with known CVEs (Common Vulnerabilities and Exposures), especially those rated critical or high severity.

### Maintainability

Debt that makes the codebase harder to understand and work with.

- **Dead code**: Functions, classes, imports, or entire files that are never called or referenced. Feature flags that are permanently on or off. Commented-out code blocks.
- **Duplicated logic**: The same algorithm implemented in multiple places. When a bug is found, it must be fixed in all copies, and one is inevitably missed.
- **Inconsistent naming**: The same concept referred to by different names across the codebase (user vs. account vs. member vs. customer for the same entity). Inconsistent casing conventions.
- **Missing documentation**: Public APIs with no docstrings. Complex algorithms with no explanatory comments. Missing ADRs (Architecture Decision Records) for non-obvious design choices.

### Portability

Debt that ties the system to a specific environment.

- **Vendor lock-in**: Direct use of cloud-provider-specific APIs (AWS SDK calls in business logic) without an abstraction layer. Proprietary database features used without a migration path.
- **Hardcoded paths**: Absolute file paths (`/home/deploy/app/config.yml`) instead of environment variables or relative paths. Hardcoded URLs instead of configuration.
- **Platform-specific code**: OS-specific system calls without platform detection. Shell scripts that assume bash on Linux when the team also deploys to containers with Alpine (ash).

### Reusability

Debt that prevents code from being leveraged in new contexts.

- **Copy-paste code**: Entire functions or modules duplicated across services with minor variations. A sign that a shared library should be extracted.
- **Tightly coupled to specific use case**: Utility functions that embed business-specific assumptions. A "generic" HTTP client that hardcodes a specific API's authentication scheme.

---

## Detection Signals

Concrete, measurable signals that indicate the presence of technical debt, organized by the level at which they are detected.

### Code-Level Signals

| Signal | Threshold | Detection Method |
|--------|-----------|-----------------|
| Cyclomatic complexity | > 15 per function | `radon cc -s -n C src/` (Python), `eslint --rule 'complexity: [error, 15]'` (JS/TS) |
| File length | > 500 lines | `wc -l` or `find src/ -name '*.py' -exec awk 'END{if(NR>500)print FILENAME,NR}' {} \;` |
| Function length | > 50 lines | `radon cc -s src/` (Python), ESLint `max-lines-per-function` rule |
| Duplicated blocks | > 10 lines repeated 3+ times | `jscpd --min-lines 10 --min-tokens 50 src/` or `pylint --load-plugins=pylint.extensions.mccabe` |
| TODO/FIXME/HACK count | Increasing trend | Grep: `grep -rn 'TODO\|FIXME\|HACK\|XXX\|WORKAROUND' src/ --include='*.py'` |
| TypeScript `any` usage | > 0 in production code | Grep: `grep -rn ': any' src/ --include='*.ts' --include='*.tsx'` |
| Python missing type hints | > 20% of public functions | `mypy --strict src/` or `pyright` |
| Long parameter lists | > 5 parameters | Custom AST analysis or linter rules |
| Deeply nested code | > 4 levels of nesting | `radon cc` or ESLint `max-depth` |

**Grep patterns for automated detection:**

```bash
# Hardcoded secrets
grep -rn 'password\s*=\s*["\x27][^"\x27]*["\x27]' src/ --include='*.py'
grep -rn 'api_key\s*=\s*["\x27]' src/ --include='*.py'
grep -rn 'AKIA[0-9A-Z]{16}' src/    # AWS Access Key pattern

# SQL injection risk (Python)
grep -rn 'execute(.*%s\|execute(.*f"\|execute(.*format(' src/ --include='*.py'

# Bare except blocks (Python)
grep -rn 'except:' src/ --include='*.py'

# Console.log left in production (JavaScript/TypeScript)
grep -rn 'console\.log' src/ --include='*.ts' --include='*.js'

# Dead imports (requires tooling: autoflake for Python, eslint for JS)
# Commented-out code blocks
grep -rn '^\s*#.*=\|^\s*#.*def \|^\s*#.*class ' src/ --include='*.py'
```

### Dependency-Level Signals

| Signal | Threshold | Detection Method |
|--------|-----------|-----------------|
| Known CVEs (critical/high) | 0 allowed | `pip-audit --strict` (Python), `npm audit --audit-level=high` (JS), `govulncheck ./...` (Go) |
| Major versions behind | > 2 major versions | `pip list --outdated` (Python), `npm outdated` (JS), `go list -m -u all` (Go) |
| Abandoned dependencies | No commit in 12+ months | Check GitHub/PyPI last release date. `npm view <pkg> time` for JS. |
| Dependency bloat | Declared but unused | `deptry .` (Python), `depcheck` (JS) |
| License compatibility | Copyleft in proprietary project | `pip-licenses` (Python), `license-checker` (JS) |
| Transitive depth | > 5 levels | `pipdeptree` (Python), `npm ls --all` (JS) |

### Testing-Level Signals

| Signal | Threshold | Detection Method |
|--------|-----------|-----------------|
| Line coverage | < 60% | `pytest --cov --cov-report=term-missing` (Python), `jest --coverage` (JS) |
| Branch coverage | < 50% | Same tools with branch coverage enabled |
| No integration tests | 0 integration tests | Check for `tests/integration/` directory or test files with external dependencies |
| Flaky test rate | > 5% | CI dashboard; `pytest-repeat` for local detection |
| Missing contract tests | API boundaries untested | Check for Pact files or Schemathesis configs |
| No performance tests | 0 load/perf tests | Check for k6, locust, or JMeter configs |
| Test-to-code ratio | < 0.5 | Compare LOC in `src/` vs `tests/` |

### Architecture-Level Signals

| Signal | Threshold | Detection Method |
|--------|-----------|-----------------|
| Circular dependencies | 0 allowed | `pydeps --no-show src/` (Python), `dependency-cruiser --output-type err src/` (JS/TS), `go vet` (Go) |
| Module coupling ratio | > 0.7 | Custom analysis: (inter-module imports) / (total imports) |
| Shared mutable state | 0 across module boundaries | Code review; grep for global/module-level mutable variables |
| Direct DB access from multiple layers | Domain logic importing ORM | Grep: `grep -rn 'from.*models import\|import.*models' src/api/ src/handlers/` |
| Missing API versioning | Public API with no version prefix | Check route definitions for `/v1/`, `/v2/` prefixes |
| Synchronous call chains | > 3 services deep | Distributed tracing analysis (Jaeger, Zipkin) |
| Monolith indicators | Single deploy unit > 100K LOC | `cloc src/` |
| Missing health checks | Services without `/health` endpoint | Grep route definitions |

---

## Quantification Framework

Every identified debt item must be quantified to enable prioritization. Use the following fields for each item.

| Field | Description | Example |
|-------|-------------|---------|
| **ID** | Unique identifier, sequential within assessment | DEBT-001 |
| **Category** | SQALE category from the taxonomy above | Changeability |
| **Description** | Concise statement of what the debt is | `OrderService` class has 2,400 lines with 47 methods spanning order creation, payment processing, inventory management, and email notifications |
| **Location** | File(s) and line range(s) affected | `src/services/order_service.py:1-2400` |
| **Remediation Cost** | Estimated effort to fix, in t-shirt sizes mapped to person-days | L (5 person-days) |
| **Interest** | Ongoing cost per sprint if the debt is not fixed | High (>2d) -- every feature touching orders requires reading 2,400 lines, and bugs in one responsibility break others |
| **Priority Score** | Interest rating (Low=0.25, Med=1, High=3) divided by Remediation Cost (S=0.5, M=2, L=5, XL=10) | 3 / 5 = 0.60 |
| **Risk** | Worst-case consequence if the debt remains | Payment processing bug introduced by unrelated order-status change, causing revenue loss |

### Remediation Cost Scale

| Size | Person-Days | Examples |
|------|------------|---------|
| **S** | 0.5 | Remove dead code, fix a naming inconsistency, add missing type hints to one module |
| **M** | 2 | Extract a class, add integration tests for one API boundary, upgrade one dependency |
| **L** | 5 | Refactor a god class into 3-4 focused classes, introduce an abstraction layer, add contract tests |
| **XL** | 10+ | Replace a data store, decompose a monolith module into services, redesign authentication |

### Interest Rate Scale

| Rating | Cost per Sprint | Symptoms |
|--------|----------------|----------|
| **Low** | < 0.5 days | Rarely touched code, cosmetic issues, minor style inconsistencies |
| **Medium** | 0.5 - 2 days | Moderately touched code, developers occasionally confused, minor bugs from the area |
| **High** | > 2 days | Hot path code, frequent bugs, significant time spent understanding or working around the debt |

---

## Debt Heatmap

A debt heatmap provides a visual summary of where debt concentrates in the system. It enables leadership and engineering to quickly identify the modules that need the most attention.

### Construction

1. **Define rows**: List every top-level module or service in the system. For a monolith, these are the major packages or directories. For a microservices architecture, these are the individual services.

2. **Define columns**: Use the eight SQALE categories: Testability, Reliability, Changeability, Efficiency, Security, Maintainability, Portability, Reusability.

3. **Score each cell**: For each module-category intersection, assign a severity based on the count and impact of debt items in that cell.
   - **Green (0)**: No significant debt detected.
   - **Yellow (1)**: 1-2 low-severity items. Acceptable but worth monitoring.
   - **Orange (2)**: Multiple items or one high-severity item. Should be addressed within the quarter.
   - **Red (3)**: Critical debt that is actively causing problems. Should be addressed within the current sprint or next sprint.

4. **Aggregate**: Sum each row to identify the most debt-laden modules. Sum each column to identify systemic quality issues that span the codebase.

### Example Heatmap

| Module | Test | Rel | Change | Eff | Sec | Maint | Port | Reuse | Total |
|--------|------|-----|--------|-----|-----|-------|------|-------|-------|
| auth-service | 1 | 2 | 1 | 0 | 3 | 1 | 0 | 0 | 8 |
| order-service | 2 | 2 | 3 | 2 | 1 | 3 | 0 | 2 | 15 |
| payment-gateway | 1 | 1 | 1 | 0 | 2 | 1 | 2 | 0 | 8 |
| notification-svc | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 1 | 5 |
| **Column Total** | **4** | **6** | **5** | **3** | **6** | **7** | **2** | **3** | |

In this example, `order-service` is the clear hotspot. Across the system, Maintainability and Reliability are the weakest categories.

### Interpreting the Heatmap

- **Row hotspots** (high total for a single module): Focus refactoring efforts on this module. Consider whether it should be decomposed.
- **Column hotspots** (high total for a single category): Indicates a systemic practice gap. Address through team-wide initiatives (e.g., if Security is the worst column, run a security training and establish security fitness functions).
- **Diagonal patterns**: If the same modules are red across multiple categories, they likely share a root cause (often a god module or a module that has been neglected during rapid feature development).

---

## Prioritization Strategy

Not all debt should be paid down immediately. Some debt is cheap to carry and expensive to fix. The goal is to maximize the return on remediation effort.

### Quick Wins (Do First)

Items with a high priority score AND small remediation cost. These deliver the most value per unit of effort.

- **Criteria**: Priority Score > 1.0 AND Remediation Cost = S or M
- **Examples**: Removing dead code that confuses developers, adding type hints to a frequently-modified module, fixing bare except blocks, removing hardcoded secrets.
- **Approach**: Batch these into a single "debt sprint" or distribute them as warm-up tasks at the start of each sprint.

### Strategic Investments (Plan into Roadmap)

Items with high interest but high remediation cost. These require dedicated time and cannot be done as side work.

- **Criteria**: Interest = High AND Remediation Cost = L or XL
- **Examples**: Decomposing a god class, introducing an abstraction layer, replacing a data store, redesigning authentication.
- **Approach**: Write a design document. Break the work into incremental steps. Allocate 15-20% of sprint capacity to debt reduction. Track progress across sprints.

### Accept and Monitor (Document and Revisit)

Items with low interest. The cost of carrying them is minimal, and fixing them would divert effort from higher-value work.

- **Criteria**: Interest = Low regardless of Remediation Cost
- **Examples**: Cosmetic inconsistencies in rarely-touched code, minor naming convention violations in legacy modules, slightly outdated documentation.
- **Approach**: Document in the debt register. Revisit quarterly. If the module becomes a hotspot, re-prioritize.

### Pay Down Incrementally (Boy Scout Rule)

Attach small debt reduction tasks to feature work. When a developer touches a module to add a feature, they also address one or two debt items in that module.

- **Rule**: "Leave the code better than you found it." Every pull request should reduce debt, not increase it.
- **Implementation**: Add a checklist item to the PR template: "Did you address any existing debt in the files you touched?"
- **Tracking**: Reduce the debt register as items are resolved. Track the net change in debt per sprint (items added vs. items resolved).

---

## Debt Report Template

Use this template to produce a standardized assessment report that can be shared with engineering leadership and used to drive prioritization decisions.

```markdown
# Technical Debt Assessment Report

**Date**: YYYY-MM-DD
**Assessor**: [name]
**Scope**: [repository/service/system name]
**Assessment Method**: Automated analysis + manual review
**Tools Used**: [list tools: radon, eslint, pip-audit, jscpd, etc.]

---

## Executive Summary

- **Total debt items identified**: X
- **Critical (Red)**: X items
- **High (Orange)**: X items
- **Medium (Yellow)**: X items
- **Low (Green)**: X items
- **Estimated total remediation effort**: X person-days
- **Estimated quick wins (< 1 day each)**: X items, Y person-days total
- **Top 3 hotspot modules**: [module1, module2, module3]
- **Top 3 systemic issues**: [category1, category2, category3]

---

## Debt Heatmap

| Module | Test | Rel | Change | Eff | Sec | Maint | Port | Reuse | Total |
|--------|------|-----|--------|-----|-----|-------|------|-------|-------|
| [module] | [0-3] | ... | ... | ... | ... | ... | ... | ... | [sum] |
| **Total** | | | | | | | | | |

---

## Critical & High Priority Items

| ID | Category | Description | Location | Rem. Cost | Interest | Priority | Risk |
|----|----------|-------------|----------|-----------|----------|----------|------|
| DEBT-001 | Security | Hardcoded AWS credentials | config.py:12 | S (0.5d) | High | 6.0 | Data breach |
| DEBT-002 | Changeability | OrderService god class | order_service.py:1-2400 | L (5d) | High | 0.6 | Cascading bugs |
| ... | | | | | | | |

---

## Quick Wins (< 1 day each)

- [ ] DEBT-001: Move hardcoded credentials to environment variables (0.5d)
- [ ] DEBT-005: Remove 340 lines of dead code in utils.py (0.5d)
- [ ] DEBT-008: Add type hints to auth module (0.5d)
- [ ] DEBT-012: Fix 14 bare except blocks (0.5d)

---

## Strategic Investments

| ID | Description | Estimated Effort | Proposed Timeline |
|----|-------------|-----------------|-------------------|
| DEBT-002 | Decompose OrderService into Order, Payment, Inventory, Notification services | 5d | Sprint 14-15 |
| DEBT-003 | Introduce repository pattern to decouple domain from database | 10d | Sprint 16-18 |

---

## Recommended Fitness Functions

To prevent new debt from accumulating, implement these automated checks:

1. **No hardcoded secrets**: Run gitleaks in CI on every PR
2. **No critical CVEs**: Run pip-audit/npm audit in CI
3. **Minimum 70% line coverage**: Enforce in CI, fail PR if below threshold
4. **No circular dependencies**: Run dependency-cruiser or pydeps in CI
5. **Maximum file length 500 lines**: Custom CI check
6. **No bare except blocks**: Linter rule (ruff/pylint/eslint)
7. **No `any` types in TypeScript**: `strict: true` in tsconfig.json
8. **Domain layer isolation**: Architectural test in CI

---

## Trend Tracking

| Sprint | Items Added | Items Resolved | Net Change | Total Open |
|--------|------------|----------------|------------|------------|
| Sprint 12 | 5 | 3 | +2 | 47 |
| Sprint 13 | 2 | 7 | -5 | 42 |
| Sprint 14 | 3 | 4 | -1 | 41 |

Target: Net negative debt change every sprint.
```

---

## Running an Assessment: Step-by-Step

1. **Scope**: Define what you are assessing (single repo, single service, entire system).
2. **Automated scan**: Run static analysis, dependency checks, coverage reports, and duplication detection. Collect raw data.
3. **Manual review**: Walk through the codebase focusing on architecture-level signals that automated tools miss (coupling, missing abstractions, inappropriate shared state).
4. **Catalog**: Create a debt item for each finding using the quantification framework.
5. **Score**: Assign remediation cost and interest to each item. Calculate priority scores.
6. **Heatmap**: Build the module-by-category heatmap.
7. **Prioritize**: Sort items into quick wins, strategic investments, and accept-and-monitor.
8. **Report**: Generate the report and share with the team.
9. **Act**: Execute quick wins immediately. Schedule strategic investments into the roadmap. Implement fitness functions to prevent regression.
10. **Repeat**: Reassess quarterly. Track trends over time.
