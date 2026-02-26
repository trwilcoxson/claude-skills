---
name: privacy-impact-assessment
description: Performs a comprehensive privacy impact assessment (PIA/DPIA) using LINDDUN GO threat analysis, regulatory gap analysis, and Privacy by Design evaluation. Use when the user asks for a privacy impact assessment, PIA, DPIA, data protection impact assessment, LINDDUN analysis, privacy review, data protection assessment, or privacy compliance review.
---

# Privacy Impact Assessment Skill

You are performing a privacy impact assessment (PIA/DPIA). This skill provides a systematic methodology for evaluating how personal data is collected, used, shared, and protected — identifying privacy risks and regulatory gaps before they become incidents or enforcement actions.

This skill complements the `threat-model` skill (which focuses on security architecture) by focusing specifically on **privacy risks, data protection compliance, and individual rights**. When run as part of a threat model team assessment, outputs feed into the validation-specialist and report-analyst pipeline. When run standalone, it produces a complete privacy assessment report.

Define `{output_dir}` as `{project_root}/threat-model-output/` unless the user specifies a different location. Create the directory if it does not exist.

## Reference Files

- **LINDDUN GO threats**: [references/linddun-go-threats.md](references/linddun-go-threats.md) — verified threat categories (L/I/N/D/D/U/N) with threat types, descriptions, indicators
- **GDPR articles**: [references/gdpr-article-reference.md](references/gdpr-article-reference.md) — verified GDPR article numbers, titles, and key content
- **Global regulations**: [references/global-privacy-regulations.md](references/global-privacy-regulations.md) — CCPA/CPRA, HIPAA, LGPD, PIPEDA, PIPL, POPIA, and other regulations with verified section numbers
- **Data classification**: [references/data-classification-taxonomy.md](references/data-classification-taxonomy.md) — PII types, sensitivity levels, required controls
- **Privacy by Design**: [references/privacy-by-design-patterns.md](references/privacy-by-design-patterns.md) — 7 foundational principles with assessment questions and implementation patterns
- **DPIA output template**: [references/dpia-output-template.md](references/dpia-output-template.md) — required output sections and formatting rules
- **Checklists**: [references/privacy-checklists.md](references/privacy-checklists.md) — per-phase completeness checklists
- **Agent output protocol**: [references/agent-output-protocol.md](references/agent-output-protocol.md) — standardized finding format for team assessments

## Anti-Hallucination Rule

**For every regulation article you cite, verify it exists in the appropriate reference file in `references/`. For every LINDDUN threat type, verify it against `references/linddun-go-threats.md`. Do NOT cite articles or threat types from memory — look them up. The validation-specialist will reject hallucinated IDs.**

If you need to cite a regulation or article not present in the reference files, explicitly state: "Note: [citation] is not in the reference files and should be independently verified."

## Phase 1 — Data Inventory and Mapping

Gather a complete picture of all personal data processing before any risk analysis. This phase is purely observational — do not form risk judgments yet.

Consult [references/data-classification-taxonomy.md](references/data-classification-taxonomy.md) for classification and [references/privacy-checklists.md](references/privacy-checklists.md) Phase 1 checklist.

### 1.1 Personal Data Discovery

Use Glob and Grep to discover:
- Database schemas, ORM models, migrations — identify fields containing personal data
- API request/response schemas — identify PII in payloads
- Form definitions, UI components — identify collection points
- Log configurations — check for PII in logs
- Analytics/tracking code — identify behavioral data collection
- Cookie/storage usage — identify client-side PII storage
- Third-party SDK integrations — identify data sharing
- Configuration files — identify data retention settings

### 1.2 Data Categories

For each personal data element discovered, classify using the taxonomy in [references/data-classification-taxonomy.md](references/data-classification-taxonomy.md):
- **Category**: Contact, Account, Device/Technical, Demographic, Financial, Health, Biometric, etc.
- **Sensitivity Level**: 1 (Public) through 5 (Restricted)
- **Specific elements**: List exact fields, not just categories

### 1.3 Data Sources

For each data category, identify:
- **Direct collection**: Forms, registrations, user input
- **Indirect collection**: Cookies, device fingerprinting, tracking pixels
- **Third-party sources**: Data brokers, partner APIs, social login
- **Inference/derivation**: Profiling, analytics, ML predictions

### 1.4 Processing Purposes

Document every purpose for which personal data is processed:
- Primary purposes (service delivery, contract performance)
- Secondary purposes (analytics, marketing, improvement)
- Ancillary purposes (logging, debugging, backups)

### 1.5 Legal Basis

For each purpose, identify the legal basis. Cite the specific regulation article:
- Consent — GDPR Art. 6(1)(a), CCPA §1798.120
- Contract performance — GDPR Art. 6(1)(b)
- Legal obligation — GDPR Art. 6(1)(c)
- Vital interests — GDPR Art. 6(1)(d)
- Public task — GDPR Art. 6(1)(e)
- Legitimate interests — GDPR Art. 6(1)(f)

**Verify every article citation against [references/gdpr-article-reference.md](references/gdpr-article-reference.md) or [references/global-privacy-regulations.md](references/global-privacy-regulations.md).**

### 1.6 Recipients and Sharing

Identify all data recipients:
- Internal teams and their access scope
- Data processors (cloud providers, SaaS tools, analytics)
- Third parties (partners, advertisers, data brokers)
- Government/regulatory bodies

### 1.7 Retention

Document retention practices:
- Stated retention periods per data category
- Actual retention mechanisms (auto-deletion, manual purge, no mechanism)
- Backup retention and its impact on deletion
- Legal hold requirements

### 1.8 Cross-Border Transfers

Identify all jurisdictional boundaries data crosses:
- Source and destination jurisdictions
- Transfer mechanism (SCCs, adequacy decision, BCRs, consent, derogation)
- Cite the applicable regulation article (e.g., GDPR Art. 46, LGPD Art. 33)

### 1.9 Data Inventory Table

Produce a comprehensive data inventory table:

| Data Category | Specific Elements | Source | Purpose | Legal Basis (cite article) | Retention | Recipients | Sensitivity Level | Cross-Border? | Transfer Mechanism |
|---|---|---|---|---|---|---|---|---|---|

**File Output**: Save Phase 1 output to `{output_dir}/privacy-assessment.md` (begin the file; subsequent phases append).

## Phase 2 — Data Flow Analysis

Map how personal data moves through the system. Consult [references/privacy-checklists.md](references/privacy-checklists.md) Phase 2 checklist.

### 2.1 Collection Points

For each collection point, document:
- Location (URL, API endpoint, SDK, form)
- What data is collected
- Notice provided at point of collection
- Consent mechanism (if applicable)
- Whether collection is necessary for stated purpose

### 2.2 Transmission Paths

For each data flow between components:
- Protocol and encryption (TLS version, certificate pinning)
- Whether PII is in URL parameters, headers, or body
- Intermediaries that can observe data in transit (CDNs, proxies, load balancers)

### 2.3 Storage Locations

For each storage location containing personal data:
- Type (database, cache, file system, object storage, logs, backups)
- Encryption at rest (algorithm, key management)
- Access controls (who/what can read, write, delete)
- Geographic location (for cross-border analysis)

### 2.4 Processing Operations

Document processing that transforms or uses personal data:
- Aggregation and analytics
- Profiling and automated decision-making
- AI/ML model training or inference
- Data enrichment or combination

### 2.5 Third-Party Sharing

For each third-party data flow:
- What data is shared
- Purpose of sharing
- Contractual protections (DPA, processor agreement)
- Whether third party acts as controller or processor

### 2.6 Retention and Deletion

Map the deletion lifecycle:
- How deletion requests propagate through the system
- Backup and replica deletion
- Third-party deletion obligations
- Verification that deletion is complete

### 2.7 Data Flow Diagram

If the system has more than 5 data flows involving personal data, produce an annotated data flow diagram highlighting:
- Personal data paths (distinct from non-personal data)
- Trust boundary crossings
- Encryption state changes
- Third-party sharing points

## Phase 3 — LINDDUN Privacy Threat Assessment

Systematically assess privacy threats using the LINDDUN GO methodology. Consult [references/linddun-go-threats.md](references/linddun-go-threats.md) for all threat types and indicators.

**For each of the 7 LINDDUN categories**, assess every applicable threat type against the data inventory and data flows from Phases 1-2.

### 3.1 L — Linkability

Assess L1 (data items), L2 (actions), L3 (identities) per [references/linddun-go-threats.md](references/linddun-go-threats.md). Check for:
- Persistent identifiers across contexts
- Shared databases without access segregation
- Analytics combining data from multiple sources
- Cross-service authentication without pseudonymization

### 3.2 I — Identifiability

Assess I1 (identifiers), I2 (quasi-identifiers), I3 (context) per reference. Check for:
- Direct identifiers stored when pseudonyms would suffice
- Insufficient anonymization leaving quasi-identifiers
- Behavioral data creating unique fingerprints
- Metadata exposure in APIs or logs

### 3.3 N — Non-repudiation (unwanted)

Assess N1 (sending), N2 (receiving), N3 (action) per reference. Check for:
- Detailed audit trails accessible to non-security staff
- Digital signatures beyond what is needed
- Transaction receipts with excessive detail

### 3.4 D — Detectability

Assess D1 (data), D2 (actions), D3 (identities) per reference. Check for:
- Different error messages for existing vs non-existing users
- Observable database query timing differences
- Metadata in API responses revealing data existence
- Cache behavior differences

### 3.5 D — Disclosure of Information

Assess D1 (access control failure), D2 (data breach), D3 (inference), D4 (surplus data) per reference. Check for:
- Overly broad API responses
- PII in application logs
- Insufficient access controls
- Shared credentials or service accounts

### 3.6 U — Unawareness

Assess U1 (transparency), U2 (intervenability), U3 (user control) per reference. Check for:
- Missing or inadequate privacy notices
- No consent management mechanism
- No DSAR fulfillment process
- Automated decisions with no human review option

### 3.7 N — Non-compliance

Assess N1 (consent), N2 (data subject rights), N3 (data protection principles), N4 (accountability), N5 (international transfers) per reference. Check for:
- No documented legal basis
- Data collected beyond stated purpose
- Missing ROPA
- Cross-border transfers without safeguards

### 3.8 LINDDUN Threat Table

Produce a threat assessment table:

| Threat ID | LINDDUN Category | Threat Type | Affected Data/Flow | Severity | Existing Controls | Gap | Regulatory Impact |
|---|---|---|---|---|---|---|---|

Use finding IDs with prefix `PA-` per [references/agent-output-protocol.md](references/agent-output-protocol.md).

**Verify every threat type cited exists in [references/linddun-go-threats.md](references/linddun-go-threats.md).**

## Phase 4 — Regulatory Gap Analysis

Map current practices against applicable privacy regulations. Consult [references/gdpr-article-reference.md](references/gdpr-article-reference.md) and [references/global-privacy-regulations.md](references/global-privacy-regulations.md).

### 4.1 Determine Applicable Regulations

Based on Phase 1 findings (data subjects' locations, data types, organization type), determine which regulations apply:
- EU/EEA data subjects → GDPR
- California consumers → CCPA/CPRA
- Health data in US → HIPAA
- Children's data in US → COPPA
- Brazilian data subjects → LGPD
- Other jurisdictions per [references/global-privacy-regulations.md](references/global-privacy-regulations.md)

### 4.2 Per-Requirement Assessment

For each applicable regulation, assess compliance against key requirements:

| Requirement | Regulation & Article | Status | Evidence | Remediation Needed |
|---|---|---|---|---|

Status must be one of: **Compliant** / **Partially Compliant** / **Non-Compliant** / **Not Assessed**

**Verify every regulation article cited against the appropriate reference file.**

### 4.3 Key Assessment Areas

For each applicable regulation, specifically assess:
- **Legal basis**: Is there a valid legal basis for each processing activity?
- **Transparency**: Are privacy notices adequate and accessible?
- **Data subject rights**: Can individuals exercise their rights (access, deletion, portability, objection)?
- **Data protection by design**: Are privacy controls built in from the start?
- **Security measures**: Are technical and organizational measures appropriate?
- **Breach notification**: Is there a breach notification process meeting regulatory timelines?
- **DPO/governance**: Is a DPO designated if required? Is there a privacy governance structure?
- **ROPA**: Are records of processing activities maintained?
- **Cross-border transfers**: Are transfer mechanisms adequate?
- **DPIA obligation**: Does this processing require a DPIA under the applicable regulation?

### 4.4 Regulatory Compliance Matrix

Produce a compliance matrix summarizing the status across all applicable regulations.

## Phase 5 — Privacy by Design Assessment

Assess the system against the 7 foundational Privacy by Design principles. Consult [references/privacy-by-design-patterns.md](references/privacy-by-design-patterns.md) for principle definitions, assessment questions, and implementation patterns.

For each principle:

1. **Apply the assessment questions** from the reference file
2. **Evaluate current implementation** against the implementation patterns
3. **Rate**: Strong / Adequate / Weak / Absent
4. **Document specific observations** — what is done well, what is missing
5. **Recommend specific improvements** — reference implementation patterns from the reference file

### 5.1 Privacy by Design Summary Table

| Principle | Rating | Key Observation | Recommendation |
|---|---|---|---|

## Phase 6 — Risk Evaluation

Evaluate and prioritize all identified risks from Phases 3-5. This phase synthesizes findings into actionable risk rankings.

### 6.1 Likelihood Assessment

For each identified privacy risk, assess likelihood (1-5):
- 1 — Rare: Requires exceptional circumstances
- 2 — Unlikely: Could occur but improbable
- 3 — Possible: Might occur in normal operations
- 4 — Likely: Expected to occur in foreseeable future
- 5 — Almost certain: Expected to occur regularly

Consider: existing controls, threat landscape, attack complexity, insider access.

### 6.2 Impact on Individuals

Assess impact on data subjects (not just organizational liability):
- 1 — Negligible: Minor inconvenience
- 2 — Limited: Significant inconvenience, recoverable
- 3 — Significant: Serious consequences for individuals
- 4 — Maximum: Irreversible consequences, financial loss, discrimination
- 5 — Catastrophic: Threat to life, liberty, or physical safety

Consider: data sensitivity, number of affected individuals, reversibility, vulnerability of data subjects.

### 6.3 Severity Calculation

Severity = Likelihood x Impact. Apply bands:
- **Critical** (20-25): Immediate remediation required
- **High** (12-19): Remediation within 30 days
- **Medium** (6-11): Remediation within 90 days
- **Low** (1-5): Accept or remediate at next opportunity

### 6.4 Risk Register

Produce the risk register:

| Risk ID | Risk Description | LINDDUN Category | Likelihood | Impact on Individuals | Severity | Recommended Mitigation | Regulatory Citation | Effort |
|---|---|---|---|---|---|---|---|---|

### 6.5 Prioritized Recommendations

For each recommendation:
- **Technical measures**: Specific code, configuration, or architecture changes
- **Organizational measures**: Policies, procedures, training
- **Privacy-Enhancing Technologies (PETs)**: Where applicable (differential privacy, homomorphic encryption, secure multi-party computation, federated learning, k-anonymity, etc.)
- **Regulatory citation**: Which requirement it addresses
- **Effort estimate**: Low / Medium / High

## Technical Privacy Controls

When assessing or recommending privacy controls, consider these categories:

### Data Minimization
- Collection limitation (only necessary fields)
- Processing limitation (purpose-bound access)
- Storage limitation (retention enforcement, auto-deletion)
- Disclosure limitation (need-to-know, field-level access)

### Pseudonymization and Anonymization
- Tokenization (reversible pseudonymization)
- Hashing with salt (one-way pseudonymization)
- k-Anonymity, l-diversity, t-closeness (statistical anonymization)
- Data masking (display-level protection)

### Encryption
- At rest: AES-256, database-level, field-level, application-level
- In transit: TLS 1.2+, certificate pinning, mTLS
- Key management: HSM, KMS, key rotation, access controls
- Crypto-shredding (encryption-based deletion)

### Consent Management
- Consent collection (granular, per-purpose, freely given)
- Consent storage (timestamped, auditable)
- Consent withdrawal (easy, effective, propagated)
- Preference center (user-facing control)

### Retention Management
- Automated deletion schedules
- Backup and replica cleanup
- Litigation hold integration
- Deletion verification

### Privacy-Enhancing Technologies (PETs)
- Differential privacy (statistical queries with noise)
- Federated learning (distributed ML without data centralization)
- Homomorphic encryption (computation on encrypted data)
- Secure multi-party computation (joint computation without sharing)
- Synthetic data generation (testing without real PII)
- Zero-knowledge proofs (verification without disclosure)

## AI/ML Privacy Considerations

When the system includes AI/ML components, additionally assess:

### Training Data Privacy
- Is personal data used in training? Legal basis?
- Can training data be extracted from the model (membership inference)?
- Is there a mechanism to remove an individual's data from the model (machine unlearning)?

### Inference Privacy
- Does the model process personal data at inference time?
- Can model outputs reveal sensitive attributes (attribute inference)?
- Are model explanations privacy-safe (no individual data leakage)?

### Automated Decision-Making
- Does the system make automated decisions with legal or significant effects? (GDPR Art. 22)
- Is there meaningful human oversight?
- Can individuals contest automated decisions?
- Is the logic of automated decisions explained?

### AI-Specific Regulations
- EU AI Act risk classification (if applicable)
- Transparency obligations for AI systems
- Data governance requirements for training data

## Output Format

Follow the agent output protocol in [references/agent-output-protocol.md](references/agent-output-protocol.md) for the standardized finding format. Use finding prefix `PA-` (e.g., PA-001, PA-002).

### Output Report Structure

The output file (`{output_dir}/privacy-assessment.md`) must contain these 10 sections in order. Consult [references/dpia-output-template.md](references/dpia-output-template.md) for detailed section requirements.

1. **Executive Summary** — Overall privacy posture, top risks, urgent remediation needs
2. **Scope and Methodology** — Systems assessed, regulations considered, methodology, limitations
3. **Data Inventory** — Complete personal data inventory table from Phase 1
4. **Data Flow Analysis** — Annotated data flow analysis from Phase 2
5. **LINDDUN Privacy Threat Assessment** — Systematic assessment from Phase 3
6. **Regulatory Compliance Matrix** — Per-requirement compliance from Phase 4
7. **Privacy by Design Assessment** — 7-principle assessment from Phase 5
8. **Risk Register** — Prioritized risk table from Phase 6
9. **Recommendations** — Prioritized remediation with technical/organizational measures
10. **Positive Observations** — Privacy controls and practices working well

### Citation Verification Checklist (before finalizing)

Before writing the final output, verify:
- [ ] Every GDPR article cited exists in [references/gdpr-article-reference.md](references/gdpr-article-reference.md)
- [ ] Every non-GDPR regulation section cited exists in [references/global-privacy-regulations.md](references/global-privacy-regulations.md)
- [ ] Every LINDDUN threat type cited exists in [references/linddun-go-threats.md](references/linddun-go-threats.md)
- [ ] Every data classification level matches [references/data-classification-taxonomy.md](references/data-classification-taxonomy.md)
- [ ] Every Privacy by Design principle matches [references/privacy-by-design-patterns.md](references/privacy-by-design-patterns.md)
- [ ] All finding IDs use PA- prefix and are sequential
- [ ] All severity scores follow OWASP Risk Rating bands (Critical 20-25, High 12-19, Medium 6-11, Low 1-5)

If any citation cannot be verified against reference files, mark it with: "**[UNVERIFIED]** — not in reference files, independently verify."

## Guidelines

- Every finding must include a concrete remediation step with both technical and organizational measures.
- When information is missing, state assumptions explicitly.
- Prioritize by impact on individuals, not just organizational liability.
- Reference specific data elements, flows, and storage locations by name throughout.
- Scale analysis proportionally — do not inflate findings to fill a template.
- For small systems with minimal PII, a focused assessment covering the most relevant phases is acceptable.
- For systems processing special category data (GDPR Art. 9) or children's data, apply maximum rigor.
- Always consider the data subject's perspective — what would a reasonable person expect?
- Save intermediate outputs to files for large systems or when context length is a concern.
- Include an Execution Log section at the end per [references/agent-output-protocol.md](references/agent-output-protocol.md).
