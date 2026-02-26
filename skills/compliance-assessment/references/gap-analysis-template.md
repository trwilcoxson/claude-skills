# Compliance Gap Analysis — Output Template

> **Purpose**: This template defines the required output format for compliance gap analysis reports produced by the GRC agent. All sections are mandatory unless explicitly marked optional.

> **CRITICAL**: Every finding MUST cite specific files, configurations, or code evidence from the assessed system. Generic findings that could apply to any system are unacceptable. If evidence cannot be found, the finding must state "No evidence found" with a description of what was searched.

---

## Report Structure

```markdown
# Compliance Gap Analysis Report

## Metadata

| Field | Value |
|-------|-------|
| **Agent** | [Agent name and version] |
| **Date** | [YYYY-MM-DD] |
| **Target System** | [System/application name and description] |
| **Frameworks Assessed** | [List all frameworks, e.g., SOC 2 Type II, HIPAA Security Rule] |
| **Assessment Scope** | [What was included — repos, infrastructure, configs, docs] |
| **Scope Exclusions** | [What was explicitly excluded and why] |
| **Assessment Method** | [Static code analysis, config review, documentation review, etc.] |

---

## Executive Summary

[2-4 paragraph summary covering:]
- Overall compliance posture across assessed frameworks
- Number of findings by severity (Critical, High, Medium, Low)
- Top 3 risk areas requiring immediate attention
- Key strengths observed in the current implementation
- Estimated effort to reach full compliance

---

## Compliance Status Dashboard

| Framework | Version | Total Reqs | Compliant | Partial | Not Implemented | N/A | % Complete |
|-----------|---------|-----------|-----------|---------|-----------------|-----|-----------|
| [Framework 1] | [Version] | [N] | [N] | [N] | [N] | [N] | [X.X%] |
| [Framework 2] | [Version] | [N] | [N] | [N] | [N] | [N] | [X.X%] |
| **Combined** | — | [N] | [N] | [N] | [N] | [N] | [X.X%] |

> **Calculation**: % Complete = (Compliant + (Partial * 0.5)) / (Total Reqs - N/A) * 100

---

## Framework-Specific Findings

### [Framework Name] — [Version]

#### [Control ID]: [Control Name]

| Field | Detail |
|-------|--------|
| **Status** | Compliant / Partial / Not Implemented / N/A |
| **Evidence** | [Specific file paths, config values, code references, or "No evidence found — searched X, Y, Z"] |
| **Gap Description** | [What is missing or incomplete — be specific] |
| **Risk Level** | Critical / High / Medium / Low |
| **Risk Justification** | [Why this risk level was assigned] |
| **Remediation** | [Specific, actionable steps to close the gap] |
| **Priority** | P1 (Immediate) / P2 (Short-term) / P3 (Medium-term) / P4 (Long-term) |
| **Estimated Effort** | [Hours/days estimate and complexity: Low/Medium/High] |

> Repeat the finding block above for each control assessed within the framework.
> Group findings by control family/category where possible.

---

## Cross-Framework Control Mapping

> For systems assessed against multiple frameworks, identify shared controls to avoid redundant remediation.

| Control Area | Framework A Control | Framework B Control | Shared Implementation | Status |
|---|---|---|---|---|
| [e.g., Access Control] | [e.g., CC6.1] | [e.g., §164.312(a)(1)] | [e.g., RBAC via Okta] | [Compliant/Partial/Gap] |

> Reference `cross-framework-mapping.md` for verified equivalences.

---

## Remediation Roadmap

### Immediate (0-30 days) — Critical & High Risk

| # | Finding | Framework(s) | Risk | Remediation | Owner | Est. Effort |
|---|---------|-------------|------|-------------|-------|-------------|
| 1 | [Finding summary] | [Framework IDs] | Critical | [Action] | [TBD] | [X days] |

### Short-Term (30-90 days) — High & Medium Risk

| # | Finding | Framework(s) | Risk | Remediation | Owner | Est. Effort |
|---|---------|-------------|------|-------------|-------|-------------|
| 1 | [Finding summary] | [Framework IDs] | High | [Action] | [TBD] | [X days] |

### Medium-Term (90-180 days) — Medium Risk

| # | Finding | Framework(s) | Risk | Remediation | Owner | Est. Effort |
|---|---------|-------------|------|-------------|-------|-------------|
| 1 | [Finding summary] | [Framework IDs] | Medium | [Action] | [TBD] | [X days] |

### Long-Term (180+ days) — Low Risk & Strategic Improvements

| # | Finding | Framework(s) | Risk | Remediation | Owner | Est. Effort |
|---|---------|-------------|------|-------------|-------|-------------|
| 1 | [Finding summary] | [Framework IDs] | Low | [Action] | [TBD] | [X days] |

---

## Assumptions & Limitations

### Assumptions
- [List assumptions made during the assessment, e.g., "Cloud provider manages physical security controls"]
- [e.g., "Documentation reviewed reflects current operational state"]
- [e.g., "Code in main branch represents production deployment"]

### Limitations
- [List limitations of the assessment, e.g., "No runtime testing performed — static analysis only"]
- [e.g., "Infrastructure-as-code not available — cloud configs assessed via documentation only"]
- [e.g., "Organizational policies not available for review — assessed technical controls only"]
- [e.g., "Interview-based controls (e.g., security awareness training effectiveness) not assessed"]

### Out of Scope
- [List items explicitly excluded and rationale]
```

---

## Template Usage Rules for Agents

1. **Never skip sections.** Every section in the template must appear in the output, even if the content is "No findings in this category."

2. **Evidence is mandatory.** Every finding must include at least one of:
   - A file path (absolute) with line number or config key
   - A code snippet showing the relevant implementation or lack thereof
   - A configuration value or setting reference
   - An explicit "No evidence found" statement with what was searched

3. **Math must be verifiable.** The % Complete calculation in the dashboard must be arithmetically correct. Agents must show their work: `(Compliant + Partial*0.5) / (Total - N/A) * 100`.

4. **Control IDs must be real.** Every control ID cited must exist in the corresponding framework reference file (`soc2-trust-services-criteria.md`, `iso27001-annex-a-controls.md`, etc.). Agents MUST verify IDs against reference files before including them.

5. **Risk levels must be justified.** A risk level without justification is invalid. Use factors like: data sensitivity, exploitability, blast radius, regulatory impact, likelihood.

6. **Remediation must be specific.** "Implement access controls" is unacceptable. "Configure RBAC in AWS IAM with least-privilege policies for the prod-api role, restricting S3 access to the healthcare-data bucket" is acceptable.

7. **Cross-references must be consistent.** A finding cited in the Framework-Specific section must appear in the Remediation Roadmap at the correct priority level and in the Cross-Framework table if it maps to multiple frameworks.
