# Consolidated Security Assessment Report Template

## Contents
- Usage Instructions
- Section I: Executive Summary (posture rating, finding counts, top 3 risks, key metrics, quick wins)
- Section II: System Overview (purpose, scope, tech stack, deployment model)
- Section III: Architecture Diagram — Structural (rendered diagram, component metadata, trust boundaries, network topology)
- Section IV: Risk Overlay Diagram (rendered diagram, component risk mapping, critical data flows)
- Section V: Asset Inventory (data assets, data flow summary)
- Section VI: Threat Actor Profiles
- Section VII: Findings (ordered by severity, standardized format)
- Section VIII: Remediation Roadmap (waves, dependencies, quick wins)
- Section IX: Networking & Infrastructure Data (VPC, subnets, security groups, IAM)
- Section X: Compliance Mapping (conditional — if compliance-gap-analysis.md exists)
- Section XI: Privacy Assessment (conditional — if privacy-assessment.md exists)
- Section XII: Positive Observations
- Section XIII: Assumptions & Limitations
- Section XIV: Appendices (methodology, framework reference, QA log, glossary, lifecycle triggers)
- Diagram Placement Rules
- Table Consistency Rules
- Cross-Reference Integrity Rules

This template defines the **exact structure** for every consolidated report. Follow it precisely — do not reorder, rename, or omit sections (except where conditional markers indicate). This ensures deterministic, diff-comparable output across runs.

## Usage

1. Read this file before every report generation
2. Use the exact heading text shown below (including section numbers)
3. Include all required elements listed under each section
4. Respect conditional markers — include section only if the referenced file exists
5. Place diagrams at the marked locations
6. Use the exact table column headers specified

---

## Section I: EXECUTIVE SUMMARY

**Heading**: `# I. Executive Summary`

**Required elements**:
- **Security Posture Rating**: One of: CRITICAL / CONCERNING / MODERATE / ACCEPTABLE / STRONG
  - Display as a styled badge/callout
- **Finding Counts Table** (exact columns):
  | Severity | Count | Scoring System |
  |----------|-------|----------------|
  | CRITICAL | _n_   | _system_       |
  | HIGH     | _n_   | _system_       |
  | MEDIUM   | _n_   | _system_       |
  | LOW      | _n_   | _system_       |
  | **Total** | _n_  |                |
- **Top 3 Risks**: Each with: title, affected component, business impact (1-2 sentences)
- **Key Metrics Table** (exact columns):
  | Metric | Value |
  |--------|-------|
  | Components Assessed | _n_ |
  | Data Flows Mapped | _n_ |
  | Trust Boundaries Identified | _n_ |
  | Threat Actors Modeled | _n_ |
  | Unique Findings | _n_ |
- **Quick Wins Summary**: Bulleted list of low-effort/high-impact remediations (max 5)

---

## Section II: SYSTEM OVERVIEW

**Heading**: `# II. System Overview`

**Required elements**:
- **System Purpose**: 2-3 sentence description
- **Scope Statement**: What is in scope, what is explicitly out of scope
- **Technology Stack Summary Table** (exact columns):
  | Layer | Technology | Version | Notes |
  |-------|-----------|---------|-------|
- **Deployment Model**: Cloud provider, region, architecture pattern (monolith/microservices/serverless)

---

## Section III: ARCHITECTURE DIAGRAM (Structural)

**Heading**: `# III. Architecture Diagram`

**Required elements**:
- {{DIAGRAM: structural-diagram.png}} — embed rendered PNG (Word/PDF) or Mermaid live render (HTML)
- **Source**: Full Mermaid code block from `02-structural-diagram.md`
- **Component Metadata Table** (exact columns):
  | Component | Type | Tech Stack | Port/Protocol | Subnet/Zone | Auth Method | Encryption | Notes |
  |-----------|------|-----------|---------------|-------------|-------------|------------|-------|
- **Trust Boundary Descriptions**: One paragraph per trust boundary explaining what it protects
- **Network Topology Data**: CIDRs, subnets, security groups, NACLs as sub-tables or structured lists

---

## Section IV: RISK OVERLAY DIAGRAM

**Heading**: `# IV. Risk Overlay Diagram`

**Required elements**:
- {{DIAGRAM: risk-overlay-diagram.png}} — embed rendered PNG (Word/PDF) or Mermaid live render (HTML)
- **Source**: Full Mermaid code block from `07-final-diagram.md`
- **Component Risk Mapping Table** (exact columns):
  | Component | Risk Level | Finding IDs | STRIDE-LM Categories | Top CWE |
  |-----------|-----------|-------------|----------------------|---------|
- **Critical Data Flow Highlights**: Top 5 highest-risk data flows with explanation

---

## Section V: ASSET INVENTORY

**Heading**: `# V. Asset Inventory`

**Required elements**:
- **Data Assets Table** (exact columns):
  | Asset | Classification | Storage Location | Encryption at Rest | Encryption in Transit | Access Controls | Retention |
  |-------|---------------|-----------------|-------------------|---------------------|-----------------|-----------|
  Classification values: PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED
- **Data Flow Summary Table** (exact columns):
  | Source | Destination | Protocol | Data Type | Sensitivity | Finding Refs |
  |--------|------------|----------|-----------|-------------|-------------|

---

## Section VI: THREAT ACTOR PROFILES

**Heading**: `# VI. Threat Actor Profiles`

**Required elements** (one sub-section per actor):
- **Actor Name** (as ### heading)
- **Profile Table** (exact columns):
  | Attribute | Value |
  |-----------|-------|
  | Type | _e.g., External/Insider/Partner_ |
  | Motivation | _e.g., Financial/Espionage/Disruption_ |
  | Capability | _1-5 scale_ |
  | Access Level | _e.g., Unauthenticated/Authenticated/Privileged_ |
  | Linked Findings | _comma-separated finding IDs_ |

---

## Section VII: FINDINGS

**Heading**: `# VII. Findings`

**Ordering**: By severity (CRITICAL first), then by OWASP Risk Rating score descending within each band.

**Required elements per finding**:

```
### [SEVERITY] TM-NNN: Finding Title

| Field | Value |
|-------|-------|
| **ID** | TM-NNN |
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Affected Component(s)** | _component name(s) — matching diagram node IDs_ |
| **STRIDE-LM Category** | _one or more of: S/T/R/I/D/E/LM_ |
| **MITRE ATT&CK** | _technique ID(s)_ |
| **CWE** | _CWE-NNN_ |
| **OWASP Category** | _category name_ |
| **CIA Impact** | C: _H/M/L_ · I: _H/M/L_ · A: _H/M/L_ |
| **PASTA Likelihood** | _1-5_ — _justification_ |
| **PASTA Impact** | _1-5_ — _justification_ |
| **OWASP Risk Rating** | _score_ (_severity band_) |
| **Confidence** | HIGH / MEDIUM / LOW |
| **Remediation** | _R-NNN_ |
| **Source** | _threat-model / code-review / privacy / grc_ |

**Attack Scenario**:
1. Step 1 ...
2. Step 2 ...
3. Step 3 ...

**Existing Mitigations**: ...

**Recommended Remediation**: ...
```

If findings come from code-review-agent (CVSS scoring), include additional row:
| **CVSS v3.1** | _score_ (_vector string_) |

**Finding count at section end**: "Total: N findings (C critical, H high, M medium, L low)"
— This count MUST match the Executive Summary table exactly.

---

## Section VIII: REMEDIATION ROADMAP

**Heading**: `# VIII. Remediation Roadmap`

**Required elements**:
- **Summary Table** (exact columns):
  | R-ID | Title | Addresses Findings | Priority | Effort | Dependencies |
  |------|-------|--------------------|----------|--------|-------------|
- **Wave 1 — Prerequisites**: Items that must be done before other remediations
- **Wave 2 — Critical Fixes**: Address CRITICAL and HIGH findings
- **Wave 3 — Hardening**: Address MEDIUM findings and defense-in-depth
- **Wave 4 — Monitoring & Observability**: Logging, alerting, detection rules
- **Quick Wins Callout**: Box/callout listing remediations achievable in <1 sprint
- **Dependency Chains**: Notation showing R-NNN -> R-NNN -> R-NNN relationships

---

## Section IX: NETWORKING & INFRASTRUCTURE DATA

**Heading**: `# IX. Networking & Infrastructure Data`

**Required elements**:
- **VPC/Network Topology**: Diagram or structured description
- **Subnet Layout Table** (exact columns):
  | Subnet Name | CIDR | Availability Zone | Type (Public/Private) | Associated Components |
  |-------------|------|-------------------|----------------------|----------------------|
- **Security Group Rules Table** (exact columns):
  | SG Name | Direction | Protocol | Port Range | Source/Destination | Description |
  |---------|-----------|----------|------------|-------------------|-------------|
- **Load Balancer Configuration**: Type, listeners, target groups, health checks
- **NAT/Internet Gateway**: Configuration summary
- **DNS & Certificates**: Domain names, certificate status, expiration
- **IAM Role Summary Table** (exact columns):
  | Role Name | Attached Policies | Trust Relationship | Used By | Principle of Least Privilege |
  |-----------|------------------|-------------------|---------|------------------------------|

---

## Section X: COMPLIANCE MAPPING

**Heading**: `# X. Compliance Mapping`

{{IF compliance-gap-analysis.md EXISTS}}

**Required elements**:
- **Framework Coverage Matrix Table** (exact columns):
  | Framework | Total Controls | Compliant | Partial | Non-Compliant | N/A | Coverage % |
  |-----------|---------------|-----------|---------|--------------|-----|-----------|
- **Control Gaps by Framework**: Sub-section per framework with gap details
- **Cross-Framework Control Mapping Table** (exact columns):
  | Control Area | NIST CSF | SOC 2 | ISO 27001 | PCI-DSS | Status |
  |-------------|----------|-------|-----------|---------|--------|

{{IF compliance-gap-analysis.md DOES NOT EXIST}}
Omit this section entirely. Add note in Section XIII: "Compliance gap analysis was not performed in this assessment."

---

## Section XI: PRIVACY ASSESSMENT

**Heading**: `# XI. Privacy Assessment`

{{IF privacy-assessment.md EXISTS}}

**Required elements**:
- **Data Inventory Summary**: Categories of personal data identified
- **LINDDUN Findings Table** (exact columns):
  | ID | LINDDUN Category | Data Flow | Risk Level | Description | Recommendation |
  |----|-----------------|-----------|-----------|-------------|----------------|
- **Regulatory Implications**: Sub-section per applicable regulation (GDPR, CCPA, HIPAA, etc.)
- **Privacy-Specific Recommendations**: Distinct from security recommendations

{{IF privacy-assessment.md DOES NOT EXIST}}
Omit this section entirely. Add note in Section XIII: "Privacy impact assessment was not performed in this assessment."

---

## Section XII: POSITIVE OBSERVATIONS

**Heading**: `# XII. Positive Observations`

**Required elements**:
- At least 3 positive observations (even if minor)
- Each observation: heading, description, which security principle it satisfies
- Format: bulleted list or sub-sections

---

## Section XIII: ASSUMPTIONS & LIMITATIONS

**Heading**: `# XIII. Assumptions & Limitations`

**Required elements**:
- **Scope Boundaries**: What was in/out of scope
- **Information Gaps**: Data that was unavailable or assumed
- **Assessment Limitations**: Time constraints, access limitations, tooling limitations
- **Confidence Disclaimers**: Areas where findings have lower confidence
- **Missing Assessments**: Note any team agents that did not run (privacy, GRC, code review)

---

## Section XIV: APPENDICES

**Heading**: `# XIV. Appendices`

**Required sub-sections** (all mandatory):

### A. Methodology Notes
- STRIDE-LM category definitions
- PASTA scoring scale (1-5 for both likelihood and impact)
- OWASP Risk Rating severity bands: CRITICAL (20-25), HIGH (12-19), MEDIUM (6-11), LOW (1-5)
- If code review findings present: CVSS v3.1 scale and severity mapping

### B. Framework Reference Table
- **MITRE ATT&CK Techniques Used** (exact columns):
  | Technique ID | Technique Name | Finding Refs |
  |-------------|---------------|-------------|
- **CWE IDs Used** (exact columns):
  | CWE ID | CWE Name | Finding Refs |
  |--------|----------|-------------|

### C. QA Corrections Log
- Table of issues found and fixed during consolidation (exact columns):
  | Issue | Location | Severity | Correction Applied |
  |-------|----------|----------|--------------------|
- If no corrections: "No QA corrections were required during consolidation."

### D. Glossary
- Alphabetically ordered term definitions
- Must include all acronyms used in the report

### E. Threat Model Lifecycle Triggers
- Conditions under which this threat model should be updated
- Recommended review cadence

---

## Diagram Placement Rules

1. **Section III**: Structural diagram — `structural-diagram.png` or live Mermaid
2. **Section IV**: Risk overlay diagram — `risk-overlay-diagram.png` or live Mermaid
3. Diagrams MUST be rendered as PNGs for Word/PDF/PPTX formats (see Step 2.5 in report-analyst instructions)
4. Diagrams render live via mermaid.js CDN for HTML format
5. Both diagrams must use consistent Mermaid direction (TD or LR) — do not mix

## Table Consistency Rules

1. All tables in this template show **exact column headers** — use them verbatim
2. Do not add or remove columns without explicit instruction
3. Empty cells should contain "N/A" or "—", never be left blank
4. Numeric cells must contain numbers, not prose descriptions
5. Finding IDs (TM-NNN) must be hyperlinked in HTML format

## Cross-Reference Integrity Rules

1. Every finding ID in Section VII must appear in at least one row of the Component Risk Mapping Table (Section IV)
2. Every R-ID in Section VIII must be referenced by at least one finding in Section VII
3. The finding count in Section I Executive Summary must exactly match the count in Section VII
4. Every component in the Component Metadata Table (Section III) must appear as a node in the structural diagram
5. Every threat actor in Section VI must be referenced by at least one finding in Section VII
6. MITRE ATT&CK and CWE IDs in findings must all appear in Appendix B
