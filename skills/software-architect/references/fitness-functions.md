# Fitness Functions: Automated Architecture Governance

A comprehensive reference for implementing fitness functions -- automated checks that verify architecture characteristics remain within acceptable bounds over time. This document covers categories, implementation patterns across ecosystems, CI/CD integration, and a recommended starter pack.

---

## What are Fitness Functions?

A fitness function is an automated, objective assessment of some architecture characteristic. The term originates from evolutionary computing (where a fitness function evaluates how well a candidate solution meets the desired criteria) and was applied to software architecture by Neal Ford, Rebecca Parsons, and Patrick Kua in "Building Evolutionary Architectures" (O'Reilly, 2017).

### Core Idea

Every architecture has constraints and quality attributes: "the domain layer must not depend on the adapter layer," "P99 latency must stay below 200ms," "no service may have a critical CVE in its dependency tree." These constraints are typically documented in wikis, ADRs, or tribal knowledge. The problem is that documented constraints are violated constantly. Developers are not malicious -- they simply do not have every architectural rule memorized, and manual code review is inconsistent.

Fitness functions make constraints executable. They run in CI/CD pipelines, in pre-commit hooks, or as scheduled jobs. When a constraint is violated, the build fails. This shifts architecture governance from "review and hope" to "automate and enforce."

### Key Principle

**If a constraint is not automated, it will be violated.** This is not cynicism; it is an observation borne out by decades of software engineering. The only reliable way to maintain an architecture characteristic over time is to write a test for it. Fitness functions are those tests.

### Properties of Good Fitness Functions

- **Automated**: Runs without human intervention. A fitness function that requires someone to manually inspect a dashboard is not a fitness function -- it is a monitoring task.
- **Objective**: Produces a pass/fail result against a clearly defined threshold. No subjective interpretation.
- **Continuous**: Runs on every commit, pull request, or deploy. Not a quarterly manual audit.
- **Actionable**: When it fails, the developer knows exactly what to fix and why.
- **Fast**: Ideally completes in under 60 seconds. Slow fitness functions get moved to nightly builds and lose their preventive power.

---

## Categories of Fitness Functions

### 1. Structural Fitness Functions

Structural fitness functions enforce the physical organization of code: what can depend on what, how large modules can grow, and what boundaries must be respected.

**Module Dependency Rules**

Enforce that dependencies flow in one direction. In a hexagonal architecture, the domain layer must not import from the adapter layer. In a layered architecture, the presentation layer must not bypass the service layer to access the repository layer directly.

- No circular dependencies between top-level modules
- No cross-boundary imports (domain must not import adapters, infrastructure must not import UI)
- Dependency flow must match the declared architecture (e.g., domain -> application -> adapter, never the reverse)

**Coupling Metrics**

- **Afferent coupling (Ca)**: Number of modules that depend on this module. High Ca means the module is heavily depended upon -- changes to it are risky.
- **Efferent coupling (Ce)**: Number of modules this module depends on. High Ce means the module has many dependencies -- it is fragile.
- **Instability (I)**: Ce / (Ca + Ce). Ranges from 0 (maximally stable) to 1 (maximally unstable). Stable modules should be abstract; unstable modules should be concrete.
- **Threshold**: Module coupling ratio (inter-module dependencies / total dependencies) should stay below 0.7.

**Component Size Limits**

- Maximum lines per file: 500
- Maximum functions per class: 20
- Maximum parameters per function: 5
- Maximum cyclomatic complexity per function: 15
- Maximum module size: 5,000 lines (including tests)

**API Surface Area**

- Maximum number of public exports per module
- All public APIs must have type signatures (no `any`, no missing type hints)
- Public APIs must have docstrings

### 2. Performance Fitness Functions

Performance fitness functions ensure the system meets its latency, throughput, and resource consumption targets.

**Latency**

- P50, P95, P99 latency thresholds per endpoint or operation
- Example: P99 < 200ms for user-facing API endpoints, P99 < 500ms for batch operations
- Measured via load testing (k6, locust, wrk) or production monitoring (Prometheus, Datadog)

**Throughput**

- Minimum requests per second at defined concurrency level
- Example: The /api/search endpoint must handle 500 req/s at P99 < 200ms with 50 concurrent users
- Regression detection: throughput must not degrade by more than 10% between releases

**Bundle Size (Frontend)**

- Maximum JavaScript bundle size (gzipped): e.g., 200KB for initial load
- Maximum CSS bundle size: e.g., 50KB
- Measured via bundlesize, size-limit, or Lighthouse CI
- Prevents creeping dependency bloat that degrades page load time

**Database Query Performance**

- No query may exceed 100ms in test environment with representative data
- No N+1 query patterns (detected via query counting in tests)
- All queries must use indexes (no full table scans on tables > 10K rows)

**Resource Consumption**

- Maximum memory usage per service instance: e.g., 512MB
- Maximum CPU usage at idle: e.g., 5%
- Startup time limit: e.g., service must be ready to accept requests within 10 seconds

### 3. Security Fitness Functions

Security fitness functions catch vulnerabilities before they reach production.

**No Hardcoded Secrets**

Scan source code, configuration files, and commit history for patterns matching API keys, passwords, tokens, private keys, and connection strings.

Common patterns to detect:
```
# AWS Access Key
AKIA[0-9A-Z]{16}

# Generic API key assignment
(api_key|apikey|api_secret|secret_key)\s*[:=]\s*['"][A-Za-z0-9/+=]{16,}['"]

# Generic password assignment
(password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]

# Private key header
-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----

# JWT token
eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+
```

Tools: gitleaks, trufflehog, detect-secrets (Yelp).

**Dependency Vulnerability Scanning**

- Zero critical or high severity CVEs in production dependencies
- Medium severity CVEs must be triaged within 30 days
- Tools: pip-audit (Python), npm audit (JavaScript), govulncheck (Go), trivy (containers), Dependabot/Renovate (automated PRs)

**HTTPS Enforcement**

- All external communication uses TLS
- No HTTP URLs in configuration (except localhost for development)
- HSTS headers present on all public endpoints

**Authentication Coverage**

- All public endpoints require authentication except explicitly whitelisted paths (health checks, public assets)
- No endpoint returns data without verifying authorization
- Detected via route analysis and integration tests

**SQL Injection Prevention**

- No string concatenation or formatting in SQL query construction
- All database access uses parameterized queries or ORM methods
- Detected via static analysis (bandit for Python, eslint-plugin-security for JS)

**SBOM Generation**

- Software Bill of Materials generated for every release
- SBOM validated against known vulnerability databases
- Tools: syft, CycloneDX, SPDX

### 4. Observability Fitness Functions

Observability fitness functions ensure the system can be understood and debugged in production.

**Structured Logging**

- All log statements use structured format (JSON) with required fields: timestamp, level, service, trace_id, message
- No `print()` statements in production code
- Log levels used correctly (no `ERROR` for expected conditions, no `DEBUG` in production config)

**Distributed Tracing**

- All HTTP handlers create tracing spans
- All outbound HTTP/gRPC calls propagate trace context
- Span names follow naming convention
- Tools: OpenTelemetry SDK checks, custom lint rules

**SLO Definitions**

- Every service has defined SLOs (availability, latency, error rate)
- SLOs are codified (not just in a wiki) in a machine-readable format
- Example: `slo.yaml` files checked into each service repository

**Alert Rules**

- Every SLO has corresponding alert rules
- Alert rules are tested (unit tests for alerting rules using tools like Prometheus unit testing)
- Every alert has a linked runbook

**Runbook Coverage**

- Every alert in the monitoring system has an associated runbook
- Runbooks are reviewed quarterly (staleness check)

### 5. Data Fitness Functions

Data fitness functions protect the integrity, compatibility, and privacy of the system's data.

**Schema Backward Compatibility**

- New schema versions must be backward compatible with the previous version
- For Protobuf: no renumbering fields, no removing required fields, no changing field types
- For database migrations: no dropping columns in use, no renaming without a migration period
- Tools: buf (Protobuf), schema-registry compatibility checks (Kafka), Atlas (SQL)

**Data Retention Policy Enforcement**

- Data older than the retention period is automatically deleted or archived
- Verified via scheduled tests that query for data beyond retention window

**PII Detection in Logs and Traces**

- Scan log output for patterns matching email addresses, phone numbers, SSNs, credit card numbers
- Patterns:
```
# Email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# US Phone
\b\d{3}[-.]?\d{3}[-.]?\d{4}\b

# SSN
\b\d{3}-\d{2}-\d{4}\b

# Credit Card (Luhn-checkable)
\b(?:\d[ -]*?){13,16}\b
```

**Backup Verification**

- Automated restore tests run weekly/monthly
- Restore time measured and compared against RTO (Recovery Time Objective)
- Restored data integrity verified via checksums

### 6. Testing Fitness Functions

Testing fitness functions ensure the test suite itself maintains quality.

**Coverage Thresholds**

- Line coverage: minimum 70%
- Branch coverage: minimum 60%
- New code coverage (diff coverage): minimum 80%
- Tools: coverage.py (Python), istanbul/c8 (JavaScript), go tool cover (Go)

**No Skipped Tests in CI**

- Tests marked as `skip`, `xfail`, or `pending` are flagged in CI
- Skipped tests must have an associated issue/ticket
- Maximum allowed skipped tests: 5 (or 1% of test suite, whichever is larger)

**Contract Test Coverage**

- Every API boundary between services has contract tests
- Contract tests are run as part of CI for both provider and consumer
- Tools: Pact, Schemathesis, Dredd

**Mutation Testing**

- Mutation testing score > 60%
- Identifies tests that pass regardless of code changes (weak tests)
- Tools: mutmut (Python), Stryker (JavaScript/TypeScript), go-mutesting (Go)

**No Flaky Tests**

- Tests that fail non-deterministically are automatically quarantined
- Quarantined tests must be fixed within 5 business days or deleted
- Flaky rate tracked: target < 1% of total test runs
- Tools: pytest-repeat, Jest retry, CI dashboard analytics

---

## Implementation Patterns per Ecosystem

### Python

```python
# ---- Structural: pytest-archon for dependency rules ----
# tests/architecture/test_dependencies.py

from archon import arch_rule

def test_domain_does_not_import_adapters():
    """Domain layer must not depend on adapter layer."""
    (arch_rule("domain")
        .should_not_import("adapters")
        .check("src"))

def test_domain_does_not_import_infrastructure():
    """Domain layer must not depend on infrastructure."""
    (arch_rule("domain")
        .should_not_import("infrastructure")
        .check("src"))

def test_no_circular_dependencies():
    """No module may have circular imports."""
    (arch_rule("src")
        .should_not_have_circular_dependencies()
        .check("src"))


# ---- Structural: Custom file size check ----
# tests/architecture/test_module_size.py

import os

MAX_FILE_LINES = 500

def test_no_oversized_files():
    """No source file may exceed 500 lines."""
    violations = []
    for root, dirs, files in os.walk("src"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path) as fh:
                    line_count = sum(1 for _ in fh)
                if line_count > MAX_FILE_LINES:
                    violations.append(f"{path}: {line_count} lines")
    assert not violations, f"Files exceeding {MAX_FILE_LINES} lines:\n" + "\n".join(violations)


# ---- Security: Check for bare except ----
# tests/architecture/test_security.py

import ast
import os

def test_no_bare_except():
    """No bare except: blocks allowed."""
    violations = []
    for root, dirs, files in os.walk("src"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path) as fh:
                    tree = ast.parse(fh.read(), filename=path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        violations.append(f"{path}:{node.lineno}")
    assert not violations, f"Bare except blocks found:\n" + "\n".join(violations)


# ---- Testing: Coverage threshold ----
# pyproject.toml
# [tool.coverage.report]
# fail_under = 70


# ---- Security: bandit configuration ----
# Run: bandit -r src/ -ll --format json --output bandit-report.json
# -ll = only medium and higher severity
```

### TypeScript

```typescript
// ---- Structural: dependency-cruiser ----
// .dependency-cruiser.cjs

module.exports = {
  forbidden: [
    {
      name: "no-circular",
      severity: "error",
      comment: "No circular dependencies allowed",
      from: {},
      to: { circular: true }
    },
    {
      name: "no-domain-to-adapter",
      severity: "error",
      comment: "Domain layer must not import from adapters",
      from: { path: "^src/domain" },
      to: { path: "^src/adapters" }
    },
    {
      name: "no-domain-to-infrastructure",
      severity: "error",
      comment: "Domain layer must not import from infrastructure",
      from: { path: "^src/domain" },
      to: { path: "^src/infrastructure" }
    },
    {
      name: "no-orphans",
      severity: "warn",
      comment: "Modules should be reachable from the entry point",
      from: { orphan: true },
      to: {}
    }
  ],
  options: {
    doNotFollow: { path: "node_modules" },
    tsPreCompilationDeps: true,
    tsConfig: { fileName: "tsconfig.json" }
  }
};

// Run: npx dependency-cruiser --validate .dependency-cruiser.cjs src/


// ---- Structural: eslint-plugin-boundaries ----
// .eslintrc.cjs (relevant section)
// {
//   plugins: ["boundaries"],
//   settings: {
//     "boundaries/elements": [
//       { type: "domain", pattern: "src/domain/*" },
//       { type: "application", pattern: "src/application/*" },
//       { type: "adapters", pattern: "src/adapters/*" }
//     ]
//   },
//   rules: {
//     "boundaries/element-types": [2, {
//       default: "disallow",
//       rules: [
//         { from: "domain", allow: [] },
//         { from: "application", allow: ["domain"] },
//         { from: "adapters", allow: ["domain", "application"] }
//       ]
//     }]
//   }
// }


// ---- Performance: bundle size budget ----
// bundlesize.config.json
// {
//   "files": [
//     { "path": "dist/main.*.js", "maxSize": "200 kB" },
//     { "path": "dist/vendor.*.js", "maxSize": "150 kB" },
//     { "path": "dist/styles.*.css", "maxSize": "50 kB" }
//   ]
// }
// Run: npx bundlesize --config bundlesize.config.json


// ---- Testing: Jest coverage thresholds ----
// jest.config.ts
// {
//   coverageThreshold: {
//     global: {
//       branches: 60,
//       functions: 70,
//       lines: 70,
//       statements: 70
//     }
//   }
// }
```

### Go

```go
// ---- Structural: go-arch-lint ----
// archfile.yml (project root)
//
// version: 2
// allow:
//   depOnAnyVendor: true
//
// components:
//   domain:
//     in: internal/domain/**
//   application:
//     in: internal/application/**
//   adapters:
//     in: internal/adapters/**
//
// deps:
//   domain:
//     canDependOn: []
//   application:
//     canDependOn: [domain]
//   adapters:
//     canDependOn: [domain, application]
//
// Run: go-arch-lint check --project-path .


// ---- Security: govulncheck ----
// Run: govulncheck ./...
// Checks all dependencies for known vulnerabilities in the Go vulnerability database.


// ---- Testing: coverage ----
// Run: go test -coverprofile=coverage.out ./...
// go tool cover -func=coverage.out
// Custom threshold check:
// total=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
// if (( $(echo "$total < 70" | bc -l) )); then echo "FAIL: coverage $total% < 70%"; exit 1; fi


// ---- Structural: no circular dependencies ----
// Go's compiler prevents circular imports between packages natively.
// But you may want to check for "logical" cycles via dependency analysis:
// Run: go mod graph | tsort 2>&1 | grep -i cycle
```

### Java

```java
// ---- Structural: ArchUnit ----
// src/test/java/architecture/LayerRulesTest.java

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.dependencies.SlicesRuleDefinition.slices;

class LayerRulesTest {

    private final JavaClasses classes = new ClassFileImporter()
            .importPackages("com.example.myapp");

    @Test
    void domainShouldNotDependOnAdapters() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..domain..")
                .should().dependOnClassesThat()
                .resideInAPackage("..adapters..");
        rule.check(classes);
    }

    @Test
    void domainShouldNotDependOnInfrastructure() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..domain..")
                .should().dependOnClassesThat()
                .resideInAPackage("..infrastructure..");
        rule.check(classes);
    }

    @Test
    void noCircularDependenciesBetweenSlices() {
        ArchRule rule = slices()
                .matching("com.example.myapp.(*)..")
                .should().beFreeOfCycles();
        rule.check(classes);
    }

    @Test
    void servicesShouldNotAccessRepositoriesDirectly() {
        // Controllers must go through services, not directly to repos
        ArchRule rule = noClasses()
                .that().resideInAPackage("..controllers..")
                .should().dependOnClassesThat()
                .resideInAPackage("..repositories..");
        rule.check(classes);
    }
}

// ---- Security: SpotBugs + Find Security Bugs plugin ----
// Run: mvn com.github.spotbugs:spotbugs-maven-plugin:check
//      -Dspotbugs.plugins=com.h3xstream.findsecbugs:findsecbugs-plugin

// ---- Testing: JaCoCo coverage thresholds ----
// pom.xml (relevant section):
// <plugin>
//   <groupId>org.jacoco</groupId>
//   <artifactId>jacoco-maven-plugin</artifactId>
//   <executions>
//     <execution>
//       <id>check</id>
//       <goals><goal>check</goal></goals>
//       <configuration>
//         <rules>
//           <rule>
//             <limits>
//               <limit>
//                 <counter>LINE</counter>
//                 <minimum>0.70</minimum>
//               </limit>
//               <limit>
//                 <counter>BRANCH</counter>
//                 <minimum>0.60</minimum>
//               </limit>
//             </limits>
//           </rule>
//         </rules>
//       </configuration>
//     </execution>
//   </executions>
// </plugin>
```

---

## CI/CD Integration

Fitness functions must run in CI/CD to be effective. Below is a comprehensive GitHub Actions workflow that covers structural, security, performance, and testing fitness functions.

### GitHub Actions: Full Example

```yaml
name: Architecture Fitness Functions
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  structural:
    name: Structural Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Check module boundaries
        run: pytest tests/architecture/test_dependencies.py -v

      - name: Check file size limits
        run: pytest tests/architecture/test_module_size.py -v

      - name: Check cyclomatic complexity
        run: |
          radon cc src/ -s -n C --json | python -c "
          import json, sys
          data = json.load(sys.stdin)
          violations = []
          for path, funcs in data.items():
              for func in funcs:
                  if func['complexity'] > 15:
                      violations.append(f\"{path}:{func['lineno']} {func['name']} complexity={func['complexity']}\")
          if violations:
              print('Complexity violations:')
              for v in violations: print(f'  {v}')
              sys.exit(1)
          print('All functions within complexity threshold.')
          "

      - name: Check for duplicated code
        run: |
          jscpd src/ --min-lines 10 --threshold 5 --reporters consoleFull --format "python"

  security:
    name: Security Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for gitleaks

      - name: Secret scanning
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency vulnerability scan
        run: |
          pip install pip-audit
          pip-audit --strict --desc

      - name: Static security analysis
        run: |
          pip install bandit
          bandit -r src/ -ll --format json --output bandit-report.json
          bandit -r src/ -ll  # Also print to stdout for CI logs

      - name: Check for bare except blocks
        run: pytest tests/architecture/test_security.py -v

  testing:
    name: Testing Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=term-missing --cov-report=xml --cov-fail-under=70

      - name: Check for skipped tests
        run: |
          pytest --co -q 2>/dev/null | grep -c "skip" | xargs -I{} sh -c '
            if [ {} -gt 5 ]; then
              echo "FAIL: {} skipped tests exceeds threshold of 5"
              exit 1
            else
              echo "OK: {} skipped tests (threshold: 5)"
            fi
          '

  performance:
    name: Performance Checks
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # Wait for startup

      - name: Run load tests
        run: |
          pip install locust
          locust -f tests/performance/locustfile.py \
            --headless \
            --users 50 \
            --spawn-rate 10 \
            --run-time 60s \
            --csv=results \
            --only-summary

      - name: Check P99 latency
        run: |
          python -c "
          import csv
          with open('results_stats.csv') as f:
              reader = csv.DictReader(f)
              for row in reader:
                  if row['Name'] == 'Aggregated':
                      p99 = float(row['99%'])
                      if p99 > 200:
                          print(f'FAIL: P99 latency {p99}ms exceeds 200ms threshold')
                          exit(1)
                      print(f'OK: P99 latency {p99}ms (threshold: 200ms)')
          "

      - name: Teardown
        if: always()
        run: docker compose down
```

### Pre-Commit Hook Integration

For faster feedback, run lightweight fitness functions as pre-commit hooks.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: architecture-tests
        name: Architecture boundary checks
        entry: pytest tests/architecture/ -x -q
        language: system
        pass_filenames: false
        always_run: true
```

---

## Starter Pack: 10 Recommended Fitness Functions

Every project, regardless of size or domain, benefits from these ten foundational fitness functions. They cover the most critical architecture characteristics and catch the most common violations.

### 1. No Circular Module Dependencies

| Field | Value |
|-------|-------|
| **Category** | Structural |
| **Why** | Circular dependencies create tightly coupled modules that cannot be tested, deployed, or reasoned about independently. They are the single most common structural defect. |
| **Tools** | dependency-cruiser (JS/TS), pytest-archon (Python), go-arch-lint (Go), ArchUnit (Java) |
| **Threshold** | Zero circular dependencies |
| **CI Command (Python)** | `pytest tests/architecture/test_dependencies.py::test_no_circular_dependencies -v` |
| **CI Command (JS/TS)** | `npx dependency-cruiser --output-type err --validate .dependency-cruiser.cjs src/` |

### 2. Domain Layer Isolation

| Field | Value |
|-------|-------|
| **Category** | Structural |
| **Why** | The domain layer contains business rules -- the most valuable and stable code. If it depends on infrastructure (databases, HTTP frameworks, message brokers), changes to infrastructure force changes to business logic. |
| **Tools** | Same as above |
| **Threshold** | Zero imports from domain to adapters/infrastructure |
| **CI Command (Python)** | `pytest tests/architecture/test_dependencies.py::test_domain_does_not_import_adapters -v` |
| **CI Command (Java)** | `mvn test -Dtest=LayerRulesTest#domainShouldNotDependOnAdapters` |

### 3. No Hardcoded Secrets

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Why** | Hardcoded secrets in source code are the leading cause of credential leaks. Once committed, they persist in git history even after deletion. |
| **Tools** | gitleaks, trufflehog, detect-secrets |
| **Threshold** | Zero secrets detected |
| **CI Command** | `gitleaks detect --source=. --verbose --redact` |

### 4. No Critical Dependency CVEs

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Why** | Known vulnerabilities in dependencies are the easiest attack vector. Automated scanning catches them before deployment. |
| **Tools** | pip-audit (Python), npm audit (JS), govulncheck (Go), trivy (containers) |
| **Threshold** | Zero critical or high severity CVEs |
| **CI Command (Python)** | `pip-audit --strict --desc` |
| **CI Command (JS)** | `npm audit --audit-level=high` |
| **CI Command (Go)** | `govulncheck ./...` |

### 5. Minimum Test Coverage 70%

| Field | Value |
|-------|-------|
| **Category** | Testing |
| **Why** | Coverage below 70% indicates large areas of untested code where bugs hide. The threshold is a floor, not a target -- aim higher for critical paths. |
| **Tools** | coverage.py (Python), istanbul/c8 (JS), go tool cover (Go), JaCoCo (Java) |
| **Threshold** | Line coverage >= 70%, branch coverage >= 60% |
| **CI Command (Python)** | `pytest --cov=src --cov-fail-under=70` |
| **CI Command (JS)** | `jest --coverage --coverageThreshold='{"global":{"lines":70,"branches":60}}'` |

### 6. P99 Latency Under SLO

| Field | Value |
|-------|-------|
| **Category** | Performance |
| **Why** | Performance regressions creep in gradually. Without automated detection, they are only noticed when users complain. |
| **Tools** | k6, locust, wrk, Lighthouse CI (frontend) |
| **Threshold** | P99 < defined SLO (e.g., 200ms for user-facing endpoints) |
| **CI Command** | `k6 run --out json=results.json tests/performance/load_test.js` |
| **Frequency** | On every merge to main (or nightly for expensive tests) |

### 7. Schema Backward Compatibility

| Field | Value |
|-------|-------|
| **Category** | Data |
| **Why** | Breaking schema changes cause cascading failures across services. Backward compatibility ensures that producers and consumers can be deployed independently. |
| **Tools** | buf (Protobuf), Confluent Schema Registry (Avro/JSON Schema), Atlas (SQL migrations) |
| **Threshold** | Zero breaking changes detected |
| **CI Command (Protobuf)** | `buf breaking --against '.git#branch=main'` |
| **CI Command (SQL)** | `atlas migrate lint --dev-url "sqlite://dev" --dir "file://migrations"` |

### 8. No PII in Logs

| Field | Value |
|-------|-------|
| **Category** | Observability / Compliance |
| **Why** | PII (Personally Identifiable Information) in logs creates compliance risk (GDPR, CCPA, HIPAA) and security exposure. Log aggregation systems are often less secured than databases. |
| **Tools** | Custom regex scanning, Presidio (Microsoft), or dedicated log scanning tools |
| **Threshold** | Zero PII patterns detected in log output |
| **CI Command** | Run integration tests, capture log output, scan with regex for email/phone/SSN/credit card patterns |
| **Example Check** | `pytest tests/ --capture=sys 2>&1 \| grep -cP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'` should return 0 |

### 9. API Contract Tests Pass

| Field | Value |
|-------|-------|
| **Category** | Testing |
| **Why** | Integration between services breaks when APIs change without coordination. Contract tests verify that providers honor the contracts their consumers depend on. |
| **Tools** | Pact (polyglot), Schemathesis (OpenAPI), Dredd (API Blueprint) |
| **Threshold** | All contract tests pass |
| **CI Command (Pact)** | `pytest tests/contracts/ -v` (consumer side), `pact-verifier --provider-base-url=http://localhost:8000 --pact-url=pacts/` (provider side) |
| **CI Command (Schemathesis)** | `schemathesis run http://localhost:8000/openapi.json --checks all` |

### 10. Maximum Module Size

| Field | Value |
|-------|-------|
| **Category** | Structural |
| **Why** | Oversized modules are a leading indicator of future god classes, tangled dependencies, and merge conflicts. Enforcing size limits encourages decomposition. |
| **Tools** | Custom script (LOC check), cloc, tokei |
| **Threshold** | No source file > 500 lines; no module directory > 5,000 lines total |
| **CI Command** | `pytest tests/architecture/test_module_size.py -v` |

---

## Fitness Function Maturity Model

Use this model to assess your team's current level of automated architecture governance and identify the next steps for improvement.

### Level 0: No Automated Governance

- Architecture decisions exist as tribal knowledge or in wiki pages nobody reads
- Code review is the only enforcement mechanism, and it is inconsistent
- Violations are discovered in production (outages, security incidents, performance complaints)
- **Action**: Start with Level 1. Pick 3 fitness functions from the starter pack and implement them this week.

### Level 1: Basic Linting and Test Coverage

- Linter runs in CI (ESLint, ruff, golint)
- Formatter enforced (Prettier, Black, gofmt)
- Basic test coverage threshold (50-60%)
- No architectural boundary enforcement
- **What's missing**: Structural rules, security scanning, performance baselines
- **Action**: Add no-circular-deps, secret scanning, and dependency audit. Raise coverage to 70%.

### Level 2: Structural Rules + Security Scanning

- Module dependency rules enforced in CI
- Domain layer isolation verified automatically
- Secret scanning on every PR (gitleaks)
- Dependency vulnerability scanning (pip-audit, npm audit)
- Coverage at 70%+ with branch coverage tracked
- **What's missing**: Performance baselines, data governance, observability checks
- **Action**: Add P99 latency tests, schema compatibility checks, and PII-in-logs detection.

### Level 3: Full Governance

- All six fitness function categories represented in CI
- Structural + performance + security + data + observability + testing
- Fitness functions run on every PR and on merge to main
- Dashboard tracks fitness function results over time
- New fitness functions added when new architecture constraints are introduced
- Debt assessment conducted quarterly using the results
- **What's missing**: Automated remediation, predictive capabilities
- **Action**: Explore automated dependency updates (Dependabot/Renovate with auto-merge for patch versions), automated performance regression detection with statistical analysis.

### Level 4: Self-Healing Architecture

- Automated remediation for common violations (auto-format, auto-fix lint issues, auto-merge dependency patches)
- Anomaly detection on performance metrics (statistical change detection, not just static thresholds)
- Architecture decisions tracked as code (ADRs in the repo, linked to fitness functions)
- Fitness functions evolve with the architecture (when a new service is added, fitness functions are scaffolded automatically)
- Cross-service governance (platform team maintains shared fitness function library)
- **This level is aspirational for most teams.** Focus on achieving Level 3 consistently before pursuing Level 4.

---

## Evolving Fitness Functions

Fitness functions are not set-and-forget. They must evolve alongside the architecture.

### When to Add New Fitness Functions

- A new architecture decision is made (e.g., "we will use event sourcing for the order service") -- add a fitness function to verify the decision is followed
- A production incident reveals a class of defect (e.g., a PII leak in logs) -- add a fitness function to prevent recurrence
- A new service is introduced -- ensure it has the baseline fitness functions from the starter pack
- A debt assessment identifies a systemic issue -- add a fitness function to prevent new instances

### When to Update Thresholds

- Coverage threshold should ratchet up as the codebase matures (start at 60%, move to 70%, aim for 80%)
- Performance thresholds should tighten as the system stabilizes (start generous, narrow as baselines become clear)
- Complexity thresholds may need to relax for genuinely complex domains (e.g., financial calculations) -- document exceptions explicitly

### When to Remove Fitness Functions

- The constraint being tested is no longer relevant (e.g., a technology was deprecated)
- The fitness function is consistently green for 6+ months and the underlying risk has been eliminated
- The fitness function is too slow and a faster alternative exists
- False positive rate exceeds 10% (fix the fitness function or remove it -- false positives erode trust)

---

## Anti-Patterns

**Fitness functions that test the wrong thing**: A fitness function that checks line count but not complexity may encourage developers to use single-line expressions that are harder to read. Always ensure the fitness function measures the quality attribute you actually care about.

**Thresholds set too aggressively**: If you set coverage to 95% on day one, developers will write meaningless tests to hit the number. Start with achievable thresholds and ratchet up as the culture matures.

**Too many fitness functions**: Each fitness function has a maintenance cost. A failing fitness function that nobody understands or maintains is worse than no fitness function at all. Start with the starter pack, then add deliberately.

**Fitness functions only in CI**: If a fitness function takes 10 minutes to run, developers will not run it locally and will be surprised by CI failures. Keep fitness functions fast (under 60 seconds) and provide local execution instructions.

**No ownership**: Every fitness function must have an owner -- a team or individual responsible for maintaining it, updating thresholds, and investigating failures. Unowned fitness functions rot.
