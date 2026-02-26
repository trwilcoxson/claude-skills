---
name: compliance-assessment
description: Performs compliance assessments with verified framework references, gap analysis, cross-framework control mapping, and audit readiness evaluation. Use when the user asks for a compliance assessment, gap analysis, SOC 2 readiness, control mapping, audit readiness, compliance review, or framework assessment.
---

# Compliance Assessment Skill

You are performing a compliance assessment. This skill provides the GRC agent (and standalone compliance reviews) with verified compliance framework reference data so it can cite real control IDs instead of hallucinating them. The reference files in `references/` are the ground truth — every control ID you cite MUST be verified against them.

Define `{output_dir}` as `{project_root}/threat-model-output/` unless the user specifies a different location. Create the directory if it does not exist. This matches the threat-model skill's output directory since compliance assessments typically run as part of the threat model pipeline.

## Reference Files

- **SOC 2 Trust Services Criteria**: [references/soc2-trust-services-criteria.md](references/soc2-trust-services-criteria.md) — CC1-CC9, Availability, Processing Integrity, Confidentiality, Privacy
- **ISO 27001:2022 Annex A**: [references/iso27001-annex-a-controls.md](references/iso27001-annex-a-controls.md) — 93 controls across 4 themes (A.5-A.8)
- **NIST 800-53 Rev 5**: [references/nist-800-53-controls.md](references/nist-800-53-controls.md) — Moderate baseline control families
- **PCI-DSS v4.0**: [references/pci-dss-v4-requirements.md](references/pci-dss-v4-requirements.md) — 12 principal requirements
- **HIPAA Security Rule**: [references/hipaa-security-rule.md](references/hipaa-security-rule.md) — Administrative, Physical, Technical safeguards
- **Cross-Framework Mapping**: [references/cross-framework-mapping.md](references/cross-framework-mapping.md) — Control equivalence table across all frameworks
- **Gap Analysis Template**: [references/gap-analysis-template.md](references/gap-analysis-template.md) — Required output structure for compliance-gap-analysis.md
- **Compliance Checklists**: [references/compliance-checklists.md](references/compliance-checklists.md) — Per-phase completeness checklists
- **Agent Output Protocol**: [references/agent-output-protocol.md](references/agent-output-protocol.md) — Standardized finding format for team assessments

## Critical Instruction: Anti-Hallucination Rule

**For every compliance control ID you cite, verify it exists in the appropriate reference file in `references/`. Do NOT cite control IDs from memory — look them up. The validation-specialist will reject hallucinated IDs.**

This means:
1. Before writing any SOC 2 control ID, open `references/soc2-trust-services-criteria.md` and confirm the ID exists
2. Before writing any ISO 27001 control ID, open `references/iso27001-annex-a-controls.md` and confirm the ID exists
3. Before writing any NIST 800-53 control ID, open `references/nist-800-53-controls.md` and confirm the ID exists
4. Before writing any PCI-DSS requirement ID, open `references/pci-dss-v4-requirements.md` and confirm the ID exists
5. Before writing any HIPAA citation, open `references/hipaa-security-rule.md` and confirm the citation exists
6. When mapping controls across frameworks, verify BOTH sides of the mapping against their respective reference files

If a control ID is not in the reference file, do NOT use it. The reference files are curated (not exhaustive), so if a control is not listed, either find the closest listed control or explicitly note that the specific sub-control is not in the curated reference set.

## Assessment Methodology

The compliance assessment follows 6 phases. Each phase builds on the previous one. Do not skip phases.

### Phase 1: Scope Determination

Determine which compliance frameworks apply to the system under assessment. This is NOT a checkbox exercise — wrong framework selection wastes effort and creates false assurance.

**Inputs to analyze:**
- Industry classification (healthcare, finance, e-commerce, SaaS, government, etc.)
- Data types processed (PII, PHI, PCI cardholder data, CUI, financial data, biometric data)
- Geographic jurisdictions (US federal, US state-specific, EU/EEA, UK, APAC countries)
- Customer and contractual requirements (SOC 2 Type II reports, ISO certification, PCI compliance attestation)
- Regulatory requirements (HIPAA for healthcare, PCI-DSS for payment processing, FedRAMP for US government)

**Framework selection logic:**
| If the system... | Then assess... | Priority |
|-----------------|---------------|----------|
| Processes payment card data | PCI-DSS v4.0 | P1 — regulatory mandate |
| Handles protected health information (PHI) | HIPAA Security Rule | P1 — regulatory mandate |
| Is a SaaS product with enterprise customers | SOC 2 Type II | P1 — contractual requirement |
| Needs international security certification | ISO 27001:2022 | P1 — certification requirement |
| Serves US federal agencies | NIST 800-53 (FedRAMP) | P1 — regulatory mandate |
| Has general security program needs | NIST 800-53 or ISO 27001 | P2 — best practice |
| Has multiple framework requirements | All applicable + cross-mapping | P1 — efficiency |

**Evidence sources for scope determination:**
- README, documentation, architecture docs
- Data flow diagrams from reconnaissance
- Infrastructure configuration (cloud provider, regions)
- Dependency manifests (package.json, requirements.txt, go.mod)
- CI/CD configuration
- Existing compliance documentation or audit reports

**Output:** Scope and Applicability Matrix (Framework | Applicable Y/N | Rationale | Priority P1/P2/P3)

### Phase 2: Control Inventory

Map existing security controls implemented in the codebase and infrastructure. Every control MUST have an evidence source.

**Technical controls to catalog:**
- Authentication mechanisms (MFA, SSO, password policies, session management)
- Authorization models (RBAC, ABAC, least privilege implementation)
- Encryption (at rest, in transit, key management, algorithm choices)
- Network security (segmentation, firewalls, WAF, DDoS protection)
- Logging and monitoring (centralized logging, SIEM, alerting, audit trails)
- Vulnerability management (scanning, patching cadence, dependency updates)
- Access control (user provisioning, deprovisioning, access reviews)
- Input validation and output encoding
- Secrets management (vaults, rotation, no hardcoded secrets)

**Administrative controls to catalog:**
- Security policies (acceptable use, data classification, incident response)
- Security awareness training programs
- Risk assessment processes
- Change management procedures
- Business continuity and disaster recovery plans
- Vendor management processes
- HR security processes (background checks, onboarding, offboarding)

**Physical controls to note:**
- Data center security (if self-hosted)
- Device management (MDM, disk encryption, remote wipe)
- Media disposal procedures

**Operational controls to catalog:**
- Change management (PR reviews, approval workflows, deployment gates)
- Backup procedures (frequency, testing, retention)
- Patch management (cadence, testing, rollback)
- Incident response procedures

**For each control, document:**
| Field | Content |
|-------|---------|
| Control Name | Descriptive name |
| Category | Technical / Administrative / Physical / Operational |
| Evidence Source | File path, config file, code reference, or document |
| Implementation Status | Implemented / Partial / Planned / Not Implemented |
| Framework Mapping | Which framework requirements this control addresses |

### Phase 3: Gap Analysis

Assess each applicable framework requirement against the control inventory from Phase 2. This is the core analytical phase.

**For each framework requirement:**
1. Look up the control ID in the appropriate reference file (MANDATORY — do not cite from memory)
2. Check the control inventory for matching implementations
3. Assess evidence quality and completeness
4. Assign status: **Implemented** | **Partial** | **Not Implemented** | **N/A** | **Insufficient Evidence**
5. For gaps, assess risk level: **Critical** | **High** | **Medium** | **Low**
6. Write specific, system-relevant remediation guidance (not generic boilerplate)

**Status definitions:**
| Status | Definition | Evidence Required |
|--------|-----------|-------------------|
| Implemented | Control fully satisfies the requirement | Direct code/config/doc evidence |
| Partial | Control partially addresses the requirement | Evidence of partial implementation + gap description |
| Not Implemented | No control addresses this requirement | Absence of evidence after thorough search |
| N/A | Requirement does not apply to this system | Documented justification (e.g., "No payment processing") |
| Insufficient Evidence | Control may exist but evidence is inadequate | Note what evidence would be needed |

**MANDATORY: Evidence-Based Analysis Rules**
- Every finding MUST cite specific files, configurations, code, or infrastructure artifacts
- "No evidence found" is a valid finding — but you must document WHERE you looked
- Generic statements like "encryption should be implemented" are NOT acceptable — specify WHAT needs encrypting, WHERE in the system, and HOW
- Quote specific code patterns, configuration values, or architectural decisions
- If a control exists but is misconfigured, cite the specific misconfiguration

**Compliance percentage calculation:**
```
% Complete = (Compliant + N/A) / Total Requirements × 100
```
Show your math for every framework.

### Phase 4: Cross-Framework Control Mapping

Identify efficiency opportunities where a single implemented control satisfies requirements across multiple frameworks.

1. Open `references/cross-framework-mapping.md` and use it as the starting point
2. For each implemented control from Phase 2, identify ALL framework requirements it satisfies
3. For each gap from Phase 3, identify if remediation would satisfy multiple frameworks simultaneously
4. Flag cases where frameworks have DIFFERENT specific requirements for the "same" control area — mapping does not mean identical requirements
5. Produce a control reuse efficiency table

**Output:** Cross-framework mapping table with implementation status, plus efficiency recommendations (e.g., "Implementing centralized logging satisfies SOC 2 CC7.1, ISO 27001 A.8.15, NIST AU-2, PCI-DSS 10.2.1, and HIPAA §164.312(b) simultaneously")

### Phase 5: Risk Assessment

For each gap identified in Phase 3, assess risk using likelihood x impact.

**Likelihood factors (1-5):**
| Score | Label | Criteria |
|-------|-------|----------|
| 5 | Almost Certain | Gap is actively exploitable or regulatory enforcement is imminent |
| 4 | Likely | Gap is commonly exploited in similar systems or audit is upcoming |
| 3 | Possible | Gap could be exploited under specific conditions |
| 2 | Unlikely | Gap requires significant effort or insider knowledge to exploit |
| 1 | Rare | Gap is theoretical or requires extraordinary circumstances |

**Impact factors (1-5):**
| Score | Label | Criteria |
|-------|-------|----------|
| 5 | Severe | Regulatory fines, certification loss, contract termination, data breach notification |
| 4 | Major | Audit failure, significant remediation costs, customer trust damage |
| 3 | Moderate | Qualified audit finding, management letter comment, moderate remediation effort |
| 2 | Minor | Minor finding, low remediation cost, minimal operational impact |
| 1 | Negligible | Observation only, no material impact on compliance posture |

**Risk rating = Likelihood x Impact:**
| Rating | Score Range | Treatment Required |
|--------|-----------|-------------------|
| Critical | 20-25 | Immediate remediation, executive visibility |
| High | 12-19 | Prioritized remediation within 30 days |
| Medium | 6-11 | Planned remediation within 90 days |
| Low | 1-5 | Accept or address during next review cycle |

**Risk treatment options:**
- **Mitigate**: Implement controls to reduce likelihood or impact
- **Transfer**: Shift risk via insurance, contractual terms, or outsourcing
- **Accept**: Document decision with business justification and approval authority
- **Avoid**: Eliminate the risk by removing the activity or system component

### Phase 6: Third-Party Risk Assessment

If the system uses third-party services, vendors, or open-source dependencies, assess their compliance posture.

**For each significant vendor/third-party:**
1. Check for SOC 2 Type II report availability (scope, exceptions, CUECs, subservice organizations)
2. Review vendor security questionnaires or certifications
3. Assess contractual security requirements (BAAs for HIPAA, DPAs for GDPR, PCI compliance attestation)
4. Review supply chain risk for software dependencies (known vulnerabilities, maintenance status, license compliance)
5. Document ongoing monitoring cadence
6. Assess fourth-party risks (vendor's vendors)

**For software dependencies:**
- Check dependency manifests for known vulnerabilities
- Assess maintenance status of critical dependencies
- Review license compliance implications
- Evaluate supply chain attack surface (typosquatting, compromised packages)

## Output Format

Follow the standardized format defined in [references/agent-output-protocol.md](references/agent-output-protocol.md):
- Use finding prefix `GRC-` for all compliance findings (e.g., GRC-001, GRC-002)
- Scoring system: Qualitative (see severity definitions in the protocol)
- Include Metadata, Summary, Findings, Observations, Assumptions, Cross-References sections
- Include Execution Log at the end

## Output Report Structure

The compliance gap analysis output (`{output_dir}/compliance-gap-analysis.md`) MUST follow the structure defined in [references/gap-analysis-template.md](references/gap-analysis-template.md). The 10 required sections are:

1. **Executive Summary** — Overall compliance posture, framework count, gap severity totals, top risks, readiness percentage
2. **Scope and Applicability Matrix** — Framework | Applicable | Rationale | Priority
3. **Compliance Status Dashboard** — Per-framework totals with percentage calculation (show math)
4. **Detailed Gap Analysis** — Per-framework, per-control-domain findings with evidence citations
5. **Cross-Framework Control Mapping** — Verified mappings from reference file with implementation status
6. **Risk Register** — Every gap with likelihood, impact, rating, treatment, owner, due date
7. **Remediation Roadmap** — Phased: 0-30 days, 30-90 days, 90-180 days, 180+ days
8. **Evidence Collection Guide** — What evidence to collect for each gap, format, storage, frequency
9. **Policy Gap Analysis** — Required policies vs. existing policies with framework references
10. **Audit Readiness Assessment** — Readiness score, blockers, high-risk areas, prep tasks, evidence checklist

## Guidelines

- Every finding must cite specific evidence from the codebase, configuration, or infrastructure. Generic findings are unacceptable.
- When information is missing, state assumptions explicitly and note what evidence would be needed.
- Prioritize gaps by business impact and regulatory risk, not by count.
- Reference specific files, configurations, and code by path throughout.
- Scale analysis proportionally — a startup with 5 employees needs different depth than an enterprise with 5,000.
- Do not inflate findings to fill a template. If a framework is not applicable, say so with justification.
- Cross-reference compliance findings with threat model findings where they overlap (e.g., a missing encryption control is both a compliance gap and a security risk).
- Save intermediate outputs to files for large assessments or when context length is a concern.
- When running as part of the threat model pipeline, read `{output_dir}/01-reconnaissance.md` for system context rather than re-scanning the codebase.
- Use the compliance checklists in [references/compliance-checklists.md](references/compliance-checklists.md) to verify completeness before finalizing each phase.
