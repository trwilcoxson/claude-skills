# Agent Output Protocol

## Contents
- Purpose
- Required Document Structure (Metadata, Summary, Findings, Observations, Assumptions, Cross-References)
- Standardized Finding Format
- Agent-Specific Prefixes (TM-, CR-, PA-, GRC-, VS-)
- Severity Definitions (OWASP Risk Rating, CVSS v3.1, Qualitative)
- Confidence Levels (HIGH, MEDIUM, LOW)
- Cross-Reference Requirements
- File Naming Convention
- Validation Rules
- Example Output Snippet

## Purpose

This protocol defines the standardized output format for all specialist agents in the security assessment pipeline. Following this format ensures:
- Downstream agents (validation-specialist, report-analyst) can reliably parse outputs
- Cross-agent finding deduplication works correctly
- Severity and confidence are comparable across agents
- Findings can be traced back to their source

All specialist agents (code-review-agent, privacy-agent, grc-agent, and the security-architect's threat model phases) MUST follow this protocol when writing output files to `{output_dir}/`.

## Required Document Structure

Every agent output file MUST contain these sections in order:

```markdown
# [Agent Name] — [Assessment Type]

## Metadata
| Field | Value |
|-------|-------|
| Agent | [agent name: security-architect, code-security-specialist, privacy-specialist, compliance-specialist] |
| Date | [ISO 8601 date, e.g., 2025-01-15] |
| Target System | [system name from reconnaissance] |
| Scope | [what was analyzed — components, files, data flows] |
| Methodology | [frameworks used, e.g., STRIDE-LM + PASTA, CVSS v3.1, LINDDUN, SOC 2 + ISO 27001] |
| Scoring System | [OWASP Risk Rating / CVSS v3.1 / Qualitative — specify which] |

## Summary
- Total findings: N (C critical, H high, M medium, L low)
- Top 3 risks: [brief descriptions]
- Key recommendation: [single most important action]

## Findings
[Each finding in standardized format — see Finding Format below]

## Observations
[Positive security observations — things done well]

## Assumptions & Limitations
[What was not analyzed, what was assumed, scope boundaries]

## Cross-References
[Links to other agent outputs, diagram component IDs, related finding IDs from other agents]
```

## Standardized Finding Format

ALL findings from ALL agents MUST use this format:

```markdown
### [SEVERITY] [ID]: [Title]

| Field | Value |
|-------|-------|
| ID | [agent-prefix]-NNN |
| Severity | CRITICAL / HIGH / MEDIUM / LOW |
| Confidence | HIGH / MEDIUM / LOW |
| Affected Component(s) | [matching diagram node IDs from Phase 2 structural diagram] |
| Scoring System | [OWASP Risk Rating / CVSS v3.1 / Qualitative] |
| Score | [numeric score, vector string, or N/A] |
| Cross-Framework | [MITRE: Txxxx | CWE-NNN | OWASP category] |

**Description**: [What is the issue and why it matters]

**Evidence**: [Specific evidence — code location, configuration, architecture observation]

**Attack Scenario**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Existing Mitigations**: [Controls already in place that partially address this]

**Recommendation**: [Specific remediation guidance]
```

## Agent-Specific Prefixes

Each agent uses a unique prefix for finding IDs to enable cross-referencing:

| Agent | Prefix | Example IDs |
|-------|--------|-------------|
| security-architect (threat model) | TM- | TM-001, TM-002 |
| code-review-agent | CR- | CR-001, CR-002 |
| privacy-agent | PA- | PA-001, PA-002 |
| grc-agent | GRC- | GRC-001, GRC-002 |
| validation-specialist | VS- | VS-001 (for new findings discovered during validation) |

## Severity Definitions

All agents MUST use these severity definitions (mapped to their scoring system):

### OWASP Risk Rating (threat model, privacy)
| Severity | Score Range (L×I) | Description |
|----------|-------------------|-------------|
| CRITICAL | 20-25 | Immediate exploitation likely, severe business impact |
| HIGH | 12-19 | Realistic attack path, significant business impact |
| MEDIUM | 6-11 | Plausible attack, moderate business impact |
| LOW | 1-5 | Theoretical or low-impact finding |

### CVSS v3.1 (code review)
| Severity | Score Range | Description |
|----------|------------|-------------|
| CRITICAL | 9.0-10.0 | Trivially exploitable, complete system compromise |
| HIGH | 7.0-8.9 | Exploitable with moderate complexity, significant impact |
| MEDIUM | 4.0-6.9 | Exploitable under specific conditions, limited impact |
| LOW | 0.1-3.9 | Difficult to exploit, minimal impact |

### Qualitative (GRC/compliance)
| Severity | Description |
|----------|-------------|
| CRITICAL | Regulatory violation likely resulting in enforcement action or audit failure |
| HIGH | Material gap auditors will flag as deficiency |
| MEDIUM | May result in qualified finding or management letter comment |
| LOW | Minor gap unlikely to impact audit outcome |

## Confidence Levels

All agents MUST assign confidence to every finding:

| Level | Definition | Evidence Required |
|-------|-----------|-------------------|
| HIGH | Clear attack path or gap, confirmed by code/config/documentation evidence | Direct observation, code evidence, confirmed configuration |
| MEDIUM | Plausible attack path or gap, some assumptions required | Indirect evidence, architectural inference, partial documentation |
| LOW | Theoretical threat or gap, significant assumptions required | No direct evidence, based on patterns or general knowledge |

## Cross-Reference Requirements

Every finding SHOULD include cross-references where applicable:

- **Diagram references**: Use the exact node ID from the Phase 2 structural diagram (e.g., `API`, `UserDB`, `Auth`)
- **Related findings**: Reference findings from other agents using their prefixed IDs (e.g., "Related: TM-004, CR-007")
- **Framework IDs**: Use only verified IDs from `references/frameworks.md` — never hallucinate IDs
- **Remediation links**: If a finding maps to a remediation in the final report, note the R-ID

## File Naming Convention

Agent outputs MUST follow this naming:

| Agent | Output File |
|-------|------------|
| security-architect | `01-reconnaissance.md` through `08-threat-model-report.md` |
| code-review-agent | `code-security-review.md` |
| privacy-agent | `privacy-assessment.md` |
| grc-agent | `compliance-gap-analysis.md` |
| validation-specialist | `validation-report.md` |

## Validation Rules

The validation-specialist checks every agent output against these rules:

1. **Structure**: All required sections present in correct order
2. **Finding IDs**: Sequential within agent, correct prefix, no duplicates
3. **Severity**: Consistent with scoring system — a CVSS 4.2 should not be labeled CRITICAL
4. **Confidence**: Assigned to every finding
5. **Cross-framework IDs**: All MITRE ATT&CK and CWE IDs verified against `references/frameworks.md`
6. **Component references**: All affected components match nodes in the Phase 2 diagram
7. **Completeness**: Summary counts match actual finding counts
8. **No placeholders**: No TODO, TBD, [INSERT], or {placeholder} text

## Example Output Snippet

```markdown
# Code Security Specialist — Code Security Review

## Metadata
| Field | Value |
|-------|-------|
| Agent | code-security-specialist |
| Date | 2025-01-15 |
| Target System | ECS Payment Platform |
| Scope | auth-service/, api-gateway/, payment-handler/ |
| Methodology | CVSS v3.1, OWASP ASVS 4.0 |
| Scoring System | CVSS v3.1 |

## Summary
- Total findings: 8 (1 critical, 3 high, 2 medium, 2 low)
- Top 3 risks: SQL injection in payment query, hardcoded API key, missing rate limiting
- Key recommendation: Parameterize all database queries immediately

## Findings

### CRITICAL CR-001: SQL Injection in Payment Query Handler

| Field | Value |
|-------|-------|
| ID | CR-001 |
| Severity | CRITICAL |
| Confidence | HIGH |
| Affected Component(s) | PaymentSvc |
| Scoring System | CVSS v3.1 |
| Score | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) |
| Cross-Framework | MITRE: T1190 | CWE-89 | OWASP A03:2021 |

**Description**: The payment query handler constructs SQL queries using string concatenation with user-supplied input, allowing SQL injection.

**Evidence**: `payment-handler/src/queries.py:47` — `cursor.execute(f"SELECT * FROM payments WHERE id = {payment_id}")`

**Attack Scenario**:
1. Attacker submits crafted payment_id via API: `1 OR 1=1; DROP TABLE payments--`
2. Unparameterized query executes injected SQL
3. Attacker exfiltrates payment records or destroys data

**Existing Mitigations**: WAF with basic SQL injection rules (partial — can be bypassed with encoding)

**Recommendation**: Use parameterized queries: `cursor.execute("SELECT * FROM payments WHERE id = %s", (payment_id,))`
```
