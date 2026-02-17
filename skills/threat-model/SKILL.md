---
name: threat-model
description: Produces an architectural threat model with Mermaid data flow diagrams, STRIDE-LM threat identification, PASTA attack simulation, and OWASP Risk Rating prioritization. Use when the user asks for a threat model, threat analysis, security architecture review, attack surface analysis, data flow diagram (DFD), or asks to analyze an architecture or system design for security risks.
argument-hint: [architecture diagram, codebase path, or system description]
---

# Threat Modeling Skill

You are performing an architectural threat model. This skill complements the `security-reviewer` agent (which operates at code level) by operating at the **architecture and design level**. After completing the threat model, suggest the user run `security-reviewer` against high-risk components identified in this analysis.

Follow all eight phases sequentially. Consult the reference files in `references/` throughout. Save intermediate outputs to files when analyzing systems with more than 10 components or when context length is a concern. Always offer to save to files.

Define `{output_dir}` as `{project_root}/threat-model-output/` unless the user specifies a different location. Create the directory if it does not exist.

## Phase 1 — Reconnaissance

Gather complete system understanding before any analysis. Do not form threat hypotheses yet — this phase is purely observational.

### 1.1 Visual Comprehension
If the user provided images (architecture diagrams, whiteboard photos, screenshots), examine them carefully. Extract every component, connection, boundary, label, and annotation visible.

### 1.2 Documentation Review
Read all provided docs, specs, READMEs, ADRs, and design documents. Note stated assumptions, constraints, and security requirements.

### 1.3 Code Scanning
Use Glob and Grep to discover:
- Entry points: API routes, event handlers, message consumers, CLI commands
- Authentication and authorization: middleware, guards, decorators, policies, tokens
- Configuration: environment variables, config files, secrets management
- Infrastructure as Code: Terraform, CloudFormation, Kubernetes manifests, Docker files
- Data schemas: database migrations, ORM models, protobuf/GraphQL/OpenAPI schemas
- External integrations: HTTP clients, SDK usage, queue producers/consumers

### 1.4 Asset Inventory
List every data asset with sensitivity classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED). Include data at rest, in transit, and in processing.

### 1.5 Actor Enumeration
Identify all human actors (end users, admins, operators, support staff) and system actors (services, cron jobs, third-party integrations, CI/CD pipelines).

### 1.6 Threat Actor Profiles
Select 3-5 relevant threat actor profiles. For each, document type, motivation, capability (1-5), access level, and relevance to this system. These profiles directly feed PASTA likelihood scoring in Phase 4. Reference specific actors when justifying likelihood scores.

### 1.7 Attack Surface Catalog
Document every entry point with location, protocol, authentication, exposure level, and input types.

### 1.8 Security Control Inventory
Catalog every existing security control with implementation location, coverage, and strength assessment. This inventory is the authoritative reference for Phase 6 (false positive validation) when checking existing mitigations.

### 1.9 Reconnaissance Summary
Output a structured summary listing all components discovered, data assets, actors, threat actor profiles, attack surface entries, security controls, trust boundaries identified, and technology stack. Flag any gaps where information is missing — explicitly state assumptions.

**File Output**: Save Phase 1 output to `{output_dir}/01-reconnaissance.md`.

## Phase 2 — Structural Diagram

Produce a Mermaid flowchart Data Flow Diagram that accurately represents the architecture BEFORE any risk analysis. Do NOT apply risk colors or threat annotations — those come in Phase 7.

Consult [references/mermaid-conventions.md](references/mermaid-conventions.md) for structural diagram conventions.

1. Draw every process, data store, and external entity discovered in Phase 1.
2. Group components within trust boundary subgraphs using dashed styling.
3. Label every data flow with protocol, data type, and sensitivity level.
4. Use **neutral styling** for all components — apply only the `external` and `dataStore` classDefs for type distinction. Do NOT apply `highRisk`, `medRisk`, or `lowRisk` classes yet.
5. Add component metadata notes (tech stack, auth mechanism, encryption, rate limits).
6. Do NOT add threat annotation notes yet.
7. Include a structural legend reflecting component types and trust boundaries only.
8. Validate Mermaid syntax mentally before outputting — avoid common pitfalls listed in the conventions reference.

Output the diagram in a fenced code block with `mermaid` language tag.

**File Output**: Save to `{output_dir}/02-structural-diagram.md`.

## Phase 3 — Threat Identification

Single cognitive objective: **IDENTIFY threats**. Do NOT score likelihood or impact yet. Scoring happens in Phase 4.

Consult [references/frameworks.md](references/frameworks.md) for all framework definitions. Consult [references/analysis-checklists.md](references/analysis-checklists.md) for checklists.

### STRIDE-LM Assessment
Assess all seven STRIDE-LM categories for every component and data flow. Consult [frameworks.md](references/frameworks.md) for assessment guidance.

### AI/ML Security Assessment (if applicable)
If the system includes AI/ML or agentic components, assess AI-specific threats. Consult [frameworks.md](references/frameworks.md) for patterns.

### Cross-Framework Classification
Classify each threat with MITRE ATT&CK technique, CWE ID, OWASP category, and CIA impact. Use only IDs verified against [frameworks.md](references/frameworks.md).

### Design-Level Analysis
Evaluate against secure design principles (defense in depth, least privilege, fail-safe defaults, separation of duties, economy of mechanism, zero trust).

### Business Logic Threats
Analyze race conditions, workflow bypass, state manipulation, and TOCTOU vulnerabilities.

### Zero Trust Assessment
Evaluate whether the system assumes network position equals trust. Flag implicit trust relationships between components that lack per-request authentication or authorization.

### Cloud-Native Threats (if applicable)
Assess cloud-native threats if applicable. Consult [frameworks.md](references/frameworks.md).

### API Depth Analysis (if applicable)
For systems with significant API surface, assess protocol-specific threats. Consult [frameworks.md](references/frameworks.md).

### Output Format
Produce a flat list of identified threats. For each threat, document:

| Field | Content |
|-------|---------|
| **Threat ID** | TM-001, TM-002, ... (sequential) |
| **Title** | Concise descriptive title |
| **STRIDE-LM category** | One or more of S, T, R, I, D, E, LM |
| **Affected component(s)** | Names matching the Phase 2 diagram |
| **Affected data flow(s)** | Names matching the Phase 2 diagram |
| **Cross-framework** | MITRE technique ID, CWE ID, OWASP category, CIA impact |
| **Description** | Brief description of the threat scenario — what could go wrong and why |

Do NOT assign likelihood, impact, or severity scores. That is Phase 4's responsibility.

**File Output**: Save to `{output_dir}/03-threat-identification.md`.

## Phase 4 — Risk Quantification

Single cognitive objective: **SCORE each threat** identified in Phase 3. Read back `{output_dir}/03-threat-identification.md` if context is limited.

Consult [references/frameworks.md](references/frameworks.md) for scoring guidance.

For each threat from Phase 3, perform the following:

### 4.1 Threat Actor Selection
Select the relevant threat actor(s) from the Phase 1 profiles. Identify which actor(s) would realistically pursue this attack and why.

### 4.2 PASTA Stage 6 — Attack Modeling
Build a concrete attack path for each threat:
1. **Entry point**: How does the attacker gain initial access? Reference the Phase 1 Attack Surface Catalog for specific entry points.
2. **Attack steps**: What sequence of actions achieves the objective?
3. **Preconditions**: What must be true for the attack to succeed?
4. **Existing controls to bypass**: Reference the Phase 1 Security Control Inventory. What controls stand in the way and how might they be circumvented?

### 4.3 Likelihood Scoring (1-5)
Assign likelihood 1-5 with written justification. See [frameworks.md](references/frameworks.md) for scoring guidance. Justify by referencing the specific threat actor profile and attack path.

### 4.4 PASTA Stage 7 — Business Impact Analysis
Assess business impact across financial, operational, reputational, and regulatory dimensions. Reference the Phase 1 Asset Inventory for data sensitivity. See [frameworks.md](references/frameworks.md).

### 4.5 Impact Scoring (1-5)
Take the highest dimension score. Justify by identifying the driving dimension. Use the scoring guidance in [references/frameworks.md](references/frameworks.md).

### 4.6 OWASP Risk Rating
Calculate Risk = Likelihood x Impact. Apply severity bands from [frameworks.md](references/frameworks.md).

### Output Format
Produce a scored threat table with all Phase 3 fields plus: Threat Actor, Attack Path Summary, Likelihood (1-5), Impact (1-5), Risk Score, Severity Band.

**File Output**: Save to `{output_dir}/04-risk-quantification.md`.

## Phase 5 — False Negative Hunting

Switch to an **expansive, adversarial mindset**. Assume Phases 3-4 missed threats. Consult [references/analysis-checklists.md](references/analysis-checklists.md) for the Phase 4 checklist. Read back `{output_dir}/03-threat-identification.md` and `{output_dir}/04-risk-quantification.md` from files if context is limited.

1. **Re-examine every "low risk" component**: Challenge your own assessment. What if this component is compromised? What blast radius does it create?

2. **Kill chain tracing**: Trace 3-5 complete attack paths from initial access through lateral movement to objective (data exfiltration, service disruption, privilege escalation). For each kill chain, flag any step where Phase 3 had no coverage.

3. **Insider threat scenarios**: Model attacks from a malicious employee, compromised developer account, or rogue admin. What controls prevent abuse of legitimate access?

4. **Supply chain review**: Examine third-party dependencies, build pipelines, package registries, container base images. What happens if any upstream dependency is compromised?

5. **Temporal threats**: Consider key rotation gaps, certificate expiry, configuration drift over time, secret sprawl, log retention limits.

6. **Cross-boundary analysis**: For every trust boundary, enumerate all possible bypass paths. Can an attacker reach a high-trust zone without passing through expected controls?

7. **AI-specific threats** (if ML components present): Training data poisoning, model inversion, membership inference, prompt injection chains, tool abuse.

8. **Data aggregation risks**: Can combining multiple low-sensitivity data sources produce high-sensitivity information?

9. **Side-channel risks**: Timing attacks, error message information leakage, resource consumption patterns.

10. **Cascade failures**: If component A fails, what happens to B, C, D? Can a targeted failure cascade to system-wide impact?

Document all newly identified threats using the same Phase 3 identification format (Threat ID, Title, STRIDE-LM, components, cross-framework, description). Then apply the full Phase 4 scoring to each new threat (threat actor, attack path, likelihood, impact, risk score, severity).

**File Output**: Save to `{output_dir}/05-false-negative-hunting.md`.

## Phase 6 — False Positive Validation

Switch to a **skeptical, evidence-based mindset**. Consult [references/analysis-checklists.md](references/analysis-checklists.md) for the Phase 5 checklist.

For **every** finding from Phases 3, 4, and 5:

1. **Realistic attack path**: Does a concrete, step-by-step attack path exist? If the path requires unrealistic preconditions, downgrade or remove.

2. **Existing mitigations**: Reference the Phase 1 Security Control Inventory as the authoritative source. Check if the architecture already includes controls that mitigate this threat (WAF, rate limiting, encryption, monitoring, etc.). If fully mitigated, note the control and mark as mitigated rather than removing.

3. **Context validation**: Validate against the actual deployment model and data sensitivity. A threat to a public marketing site differs from the same threat to a payment system.

4. **Confidence assignment**: Assign each finding a confidence level:
   - **HIGH**: Clear attack path, confirmed by code/config evidence
   - **MEDIUM**: Plausible attack path, some assumptions required
   - **LOW**: Theoretical threat, significant assumptions required

5. **Deduplication**: Merge findings that describe the same underlying issue discovered through different frameworks. Reference all applicable framework classifications in the merged finding.

### Framework ID Verification Step
Before finalizing, cross-reference every MITRE technique ID and CWE ID in the findings against the reference tables in [references/frameworks.md](references/frameworks.md). Remove or replace any ID that does not appear in the tables. This is a hard requirement — no hallucinated IDs in the final output.

### Overall Validation
- Remove or clearly mark any finding that lacks a realistic attack path.
- Ensure severity ratings are consistent across similar findings.
- Verify that OWASP Risk Rating scores (Likelihood x Impact) align with the validated understanding.
- Confirm no critical findings were accidentally downgraded.

**File Output**: Save to `{output_dir}/06-validated-findings.md`.

## Phase 7 — Visual Validation

Apply risk analysis results to the structural diagram from Phase 2.

Consult [references/mermaid-conventions.md](references/mermaid-conventions.md) for risk-overlay conventions.

1. **Start from the Phase 2 structural diagram**. Read back `{output_dir}/02-structural-diagram.md` if needed.

2. **Apply risk color coding**: Based on Phase 6 validated findings, apply `highRisk`, `medRisk`, and `lowRisk` classDefs to components. A component's risk level is determined by the highest-severity validated threat affecting it.

3. **Add threat annotation notes**: For components with validated threats, add Mermaid `note` blocks with STRIDE-LM category abbreviations, OWASP Risk Rating score (LxI=Score BAND), and top CWE IDs.

4. **Completeness check**: Cross-reference the diagram against the Phase 1 asset inventory. Every component, data store, external entity, and actor must appear. Flag and add any missing elements discovered during Phases 3-5.

5. **Accuracy check**: Verify trust boundaries correctly reflect the validated security zones. Verify data flow directions are correct. Verify component types use correct shapes.

6. **Visual quality check**: No orphaned nodes. Consistent layout direction. Clean subgraph nesting. Labels are readable. Legend is accurate and now includes risk color entries.

Produce the final corrected Mermaid diagram in a fenced code block.

**File Output**: Save to `{output_dir}/07-final-diagram.md`.

## Phase 8 — Final Report

Produce the complete threat model report with the following sections.

### Report Structure

1. **Executive Summary**: 3-5 sentence overview. Total threats found by severity. Top 3 risks. Overall security posture assessment (CRITICAL / CONCERNING / MODERATE / ACCEPTABLE / STRONG).

2. **System Overview**: Brief description of the system, its purpose, key components, and deployment model. Reference source materials analyzed.

3. **Threat Model Diagram**: The final validated Mermaid diagram from Phase 7 with legend.

4. **Asset Inventory Table**: All data assets with sensitivity classification, storage location, encryption status, and access controls.

5. **Threat Actor Profiles**: Summary of the 3-5 threat actor profiles from Phase 1, including which threats each actor is associated with from the analysis.

6. **Threat Summary Table**: All validated findings in a table with columns: ID | Threat | STRIDE-LM | Likelihood | Impact | Risk Score | CIA | MITRE ATT&CK | CWE | OWASP | Confidence | Severity.

7. **Detailed Findings**: Grouped by severity (CRITICAL, HIGH, MEDIUM, LOW). Each finding includes:
   - Title and ID
   - Affected component(s)
   - STRIDE-LM category
   - Attack scenario (step-by-step)
   - Threat actor(s) and their motivation
   - PASTA likelihood rating with justification
   - PASTA business impact rating with justification
   - OWASP Risk Rating score and severity band
   - Cross-framework references (MITRE, CWE, OWASP)
   - CIA impact
   - Existing mitigations (if any)
   - Recommended remediation
   - Confidence level

8. **Design Recommendations**: Prioritized list grouped by severity. Each recommendation includes the threat(s) it addresses, implementation guidance, and effort estimate (LOW/MEDIUM/HIGH).

9. **Remediation Dependency Ordering**: After listing recommendations by severity, provide a "Recommended Implementation Order" section:
   - Identify dependencies between remediations (e.g., "Add certificate authority" must precede "Enable mTLS").
   - Group into implementation waves:
     - **Wave 1 — Prerequisites**: Foundational changes that other remediations depend on
     - **Wave 2 — Critical Fixes**: CRITICAL and HIGH severity remediations
     - **Wave 3 — Hardening**: MEDIUM severity remediations and defense-in-depth improvements
     - **Wave 4 — Monitoring & Observability**: Logging, alerting, and detection improvements
   - Mark quick wins: high impact, low effort, no dependencies.
   - Use dependency notation: `R-003 -> R-007 -> R-012` meaning implement in that order.

10. **LINDDUN Privacy Assessment**: Summary of privacy threats identified, regulatory implications (GDPR, CCPA, HIPAA as applicable), and privacy-specific recommendations.

11. **Positive Observations**: Security controls and design decisions that are working well.

12. **False Negative Hunting Results**: Summary of Phase 5 findings — what additional threats were discovered and what areas remain uncertain.

13. **Assumptions and Limitations**: What was assumed, what was not analyzed, what additional information would improve the model. Scope boundaries.

14. **Threat Model Lifecycle Triggers**: Define update triggers including architecture changes, incidents, compliance changes, and minimum annual cadence.

**File Output**: Save the complete report to `{output_dir}/08-threat-model-report.md`.

## Scaling Guidelines

Adapt the depth of analysis to the system's size. These are concrete rules, not suggestions.

### Small Systems (5 or fewer components, 8 or fewer data flows)
- **Phase 1**: Lightweight — threat actor profiles can be 2-3 most relevant actors. Attack surface catalog and control inventory can be inline tables rather than exhaustive catalogs.
- **Phase 3**: STRIDE-LM assessment can be a single table covering all components rather than per-component narratives.
- **Phase 4**: Scoring can be presented in a combined table with identification (inline with Phase 3 output format).
- **Phase 5**: 1-2 kill chains sufficient.
- **Phase 8**: Report sections can be combined where sparse. Executive summary and system overview can merge. LINDDUN section can be omitted if no personal data is processed.

### Medium Systems (6-20 components, 9-30 data flows)
- Execute all phases as described above with full depth.
- **Phase 3**: Group STRIDE-LM assessment by trust zone rather than individual component where components within a zone share identical threat profiles. Still enumerate unique threats per component where profiles differ.

### Large Systems (more than 20 components, more than 30 data flows)
- **Phase 1**: Mandatory file-based output — context WILL compress. Save each subsection (asset inventory, attack surface, control inventory) as it is completed.
- **Phase 3**: Batch threat identification by trust zone. Produce per-zone threat tables. Cross-zone threats get their own section.
- **Phase 4**: Score only MEDIUM-or-higher likelihood threats in full detail. LOW likelihood threats receive summary scoring (single-line justification).
- **Phase 5**: 5 or more kill chains required, and they must span multiple trust zones.
- **Phase 7**: Consider producing per-zone diagrams in addition to the full system diagram if the full diagram becomes unreadable.
- **Phase 8**: Produce an executive summary readable in isolation (no references to detailed findings required to understand it). Consider splitting detailed findings by domain or trust zone into appendix sections.

## Guidelines

- Every finding must include a concrete remediation step.
- When information is missing, state assumptions explicitly.
- Prioritize by realistic risk, not theoretical severity.
- Reference specific components, data flows, and trust boundaries by name throughout.
- Scale analysis proportionally — do not inflate findings to fill a template.
- Save intermediate outputs to files for large systems or when context length is a concern.
