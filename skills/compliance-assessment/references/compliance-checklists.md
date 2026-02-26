# Compliance Assessment — Phase Checklists

> **Purpose**: These checklists ensure completeness at each phase of a compliance assessment. Agents MUST verify all items before proceeding to the next phase. Incomplete phases produce unreliable assessments.

---

## Phase 1: Scope & Framework Selection

Before proceeding to Phase 2, verify ALL of the following:

- [ ] **Frameworks identified** — All applicable compliance frameworks explicitly listed (e.g., SOC 2 Type II, HIPAA Security Rule, PCI-DSS v4.0, ISO 27001:2022, NIST 800-53 Rev 5)
- [ ] **Framework justification documented** — Rationale for why each framework applies (e.g., "HIPAA applies because the system processes ePHI for covered entities")
- [ ] **System boundaries defined** — Clear description of what is in scope: repositories, services, infrastructure, third-party integrations
- [ ] **Data types cataloged** — All sensitive data types identified (PII, PHI, PCI, financial, proprietary) with storage locations and flow paths
- [ ] **Deployment model noted** — Cloud provider(s), region(s), deployment architecture (IaaS/PaaS/SaaS), shared responsibility boundaries
- [ ] **Regulatory jurisdiction identified** — Geographic and legal jurisdictions that affect requirements (e.g., US federal, state-specific like CCPA, EU for GDPR)
- [ ] **Stakeholders identified** — Who owns the system, who is responsible for compliance, who will remediate findings
- [ ] **Prior assessments reviewed** — Any previous audit reports, penetration tests, or compliance assessments referenced for context
- [ ] **Scope exclusions documented** — What is explicitly out of scope and why (e.g., "Physical security excluded — managed by AWS under shared responsibility model")

---

## Phase 2: Control Inventory

Before proceeding to Phase 3, verify ALL of the following:

- [ ] **Control families mapped** — All control families/categories for each selected framework identified and listed
- [ ] **Baseline selected** — For frameworks with baselines (e.g., NIST 800-53 Low/Moderate/High), the appropriate baseline is selected and justified
- [ ] **Scope exclusions justified** — Any controls excluded from assessment have documented rationale (e.g., "PE-* physical security controls excluded per shared responsibility — AWS SOC 2 report covers these")
- [ ] **Control IDs verified** — Every control ID cross-checked against the corresponding reference file in `references/`:
  - `soc2-trust-services-criteria.md`
  - `iso27001-annex-a-controls.md`
  - `nist-800-53-controls.md`
  - `pci-dss-v4-requirements.md`
  - `hipaa-security-rule.md`
- [ ] **Addressable vs Required noted** — For HIPAA, each control correctly classified as Required (R) or Addressable (A) per `hipaa-security-rule.md`
- [ ] **Total control count documented** — Number of applicable controls per framework recorded for dashboard calculations
- [ ] **Cross-framework overlaps identified** — Preliminary mapping of equivalent controls using `cross-framework-mapping.md`

---

## Phase 3: Evidence Collection

Before proceeding to Phase 4, verify ALL of the following:

- [ ] **Every control status has evidence** — No control assessed as Compliant or Partial without at least one piece of supporting evidence
- [ ] **File paths verified** — All referenced file paths are absolute and confirmed to exist in the assessed codebase
- [ ] **Configuration values checked** — Security-relevant configs (auth settings, encryption settings, logging configs, network rules) extracted and documented
- [ ] **Code reviewed** — Security-critical code paths examined (authentication, authorization, input validation, cryptographic operations, data handling)
- [ ] **Infrastructure-as-code reviewed** — Terraform, CloudFormation, Kubernetes manifests, Docker configs, CI/CD pipelines examined where available
- [ ] **Documentation reviewed** — README files, architecture docs, runbooks, incident response plans, security policies examined where available
- [ ] **"No evidence found" explicitly stated** — For any control where evidence could not be located, the agent documents what was searched and where
- [ ] **Evidence is specific** — No generic statements like "access controls are in place." Evidence must cite specific mechanisms (e.g., "RBAC enforced via middleware in `/src/auth/rbac.ts` lines 45-92")
- [ ] **Negative evidence captured** — Absence of expected controls documented (e.g., "No rate limiting found on `/api/auth/login` endpoint")

---

## Phase 4: Gap Analysis

Before proceeding to Phase 5, verify ALL of the following:

- [ ] **Every gap rated by risk** — Each Not Implemented and Partial finding has a risk level (Critical/High/Medium/Low) with justification
- [ ] **Risk justification grounded** — Risk ratings reference specific factors: data sensitivity, exploitability, blast radius, regulatory penalty exposure, likelihood
- [ ] **Remediation suggested for every gap** — Each gap has at least one specific, actionable remediation step
- [ ] **Remediation is specific** — No vague recommendations. "Implement encryption" is unacceptable; "Enable AES-256 encryption at rest for the PostgreSQL RDS instance storing patient records using AWS KMS CMK" is acceptable
- [ ] **Cross-framework gaps identified** — Gaps that affect multiple frameworks simultaneously are flagged (e.g., missing encryption affects both PCI-DSS 3.5 and HIPAA §164.312(a)(2)(iv))
- [ ] **Compliant controls confirmed** — Controls marked Compliant have sufficient evidence to withstand auditor scrutiny
- [ ] **Partial controls have clear gap description** — What is implemented vs what is missing is clearly delineated
- [ ] **N/A controls justified** — Every N/A designation has a documented reason

---

## Phase 5: Cross-Framework Mapping

Before proceeding to Phase 6, verify ALL of the following:

- [ ] **Shared controls identified** — Controls that satisfy requirements across multiple frameworks are mapped using `cross-framework-mapping.md`
- [ ] **Unique requirements noted** — Framework-specific requirements that have no equivalent in other assessed frameworks are highlighted
- [ ] **Mapping verified against reference** — All cross-framework mappings checked against `cross-framework-mapping.md` for accuracy
- [ ] **Scope differences acknowledged** — Where two frameworks address the same area but with different specificity, the differences are documented
- [ ] **Evidence reuse documented** — Where a single implementation satisfies multiple frameworks, this is explicitly stated to avoid redundant remediation
- [ ] **N/A mappings correct** — Control areas marked N/A for a framework are verified against the reference table

---

## Phase 6: Remediation Roadmap

Before finalizing the report, verify ALL of the following:

- [ ] **Priorities assigned** — Every gap has a priority: P1 (Immediate/0-30 days), P2 (Short-term/30-90 days), P3 (Medium-term/90-180 days), P4 (Long-term/180+ days)
- [ ] **Priority aligns with risk** — Critical and High risk findings are P1 or P2; Medium findings are P2 or P3; Low findings are P3 or P4
- [ ] **Timeline is realistic** — Remediation estimates consider implementation complexity, testing, and deployment
- [ ] **Dependencies identified** — Remediation items that depend on other items are flagged (e.g., "Implement centralized logging before configuring SIEM alerts")
- [ ] **Cost considerations noted** — Where remediation involves tooling, infrastructure, or staffing changes, approximate effort/cost is noted
- [ ] **Quick wins highlighted** — Low-effort, high-impact remediations are identified for immediate action
- [ ] **Ownership suggested** — Each remediation item has a suggested owner role (e.g., "DevOps team", "Security team", "Application developers")

---

## Final Quality Checklist

Before delivering the report, the agent MUST verify ALL of the following:

- [ ] **No hallucinated control IDs** — Every control ID in the report exists in the corresponding reference file. Run a verification pass comparing cited IDs against reference files.
- [ ] **No generic findings** — Every finding references specific files, configs, code, or explicitly states "No evidence found." No finding should be copy-pasteable into a report for a different system without modification.
- [ ] **All evidence is grounded** — File paths exist, config values are real, code references are accurate
- [ ] **Math is verified** — Dashboard percentages are arithmetically correct: `(Compliant + Partial*0.5) / (Total - N/A) * 100`. Verify each row and the combined total.
- [ ] **Cross-references are consistent** — Findings in the framework-specific section match the remediation roadmap priority, the cross-framework mapping table, and the dashboard counts
- [ ] **Report follows template** — All sections from `gap-analysis-template.md` are present with no missing sections
- [ ] **Executive summary is accurate** — Summary statistics match the detailed findings (number of Critical, High, Medium, Low findings)
- [ ] **Scope and limitations are honest** — The report does not claim more coverage than was actually performed
- [ ] **Remediation roadmap is complete** — Every gap appears in exactly one roadmap time horizon
- [ ] **No contradictions** — A control is not simultaneously Compliant in the findings and listed as a gap in the roadmap
