# Privacy Impact Assessment — Phase Checklists

These checklists ensure completeness at each phase of the privacy impact assessment. Agents must verify all items before proceeding to the next phase. Mark each item as complete before advancing.

---

## Phase 1: Data Inventory

- [ ] All personal data fields in the system have been cataloged (database columns, API fields, form inputs, log entries, cookies, local storage)
- [ ] Each data element has been assigned a sensitivity level per `data-classification-taxonomy.md` (PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED)
- [ ] Data sources have been identified for each element (user input, third-party API, derived/computed, system-generated)
- [ ] Processing purposes have been documented for each data element (why it is collected and used)
- [ ] Legal bases have been assigned per applicable regulation (e.g., GDPR Art. 6(1) basis, CCPA collection justification)
- [ ] Retention periods have been noted for each data element (how long it is kept and why)
- [ ] Data recipients have been identified (internal teams, processors, third parties, sub-processors)
- [ ] Data subjects have been categorized (customers, employees, prospects, children, patients, etc.)
- [ ] Data volume estimates have been recorded (number of records, number of data subjects)
- [ ] High-risk data combinations have been flagged per `data-classification-taxonomy.md`
- [ ] Special category data (GDPR Art. 9) has been specifically identified and justified
- [ ] Children's data processing has been identified and age thresholds noted

---

## Phase 2: Regulatory Mapping

- [ ] All applicable regulations have been identified based on: data subject locations, business operations, data types, industry sector
- [ ] Jurisdiction analysis is complete (where data subjects are located, where processing occurs, where data is stored)
- [ ] Regulatory requirements have been mapped to specific data flows and processing activities
- [ ] Cross-border transfer requirements have been identified (GDPR Art. 44-49, PIPL Art. 38-43, LGPD Art. 33-36, etc.)
- [ ] Sector-specific regulations have been assessed (HIPAA for health data, PCI-DSS for payment data, COPPA for children's data, GLBA for financial data)
- [ ] State/provincial laws have been considered (US state privacy laws, Quebec Law 25, etc.)
- [ ] Regulatory thresholds have been verified (CCPA $25M/100K consumers/50% revenue, PIPL >1M individuals for security assessment)
- [ ] Data Protection Officer requirements have been assessed per applicable regulations
- [ ] DPIA/PIA mandatory triggers have been checked (GDPR Art. 35(3) high-risk processing types)

---

## Phase 3: LINDDUN Threat Analysis

- [ ] **Linkability** threats assessed: Can data subjects' actions or data be linked across domains, sessions, or datasets?
- [ ] **Identifiability** threats assessed: Can data subjects be identified from the data processed?
- [ ] **Non-repudiation** threats assessed: Can data subjects deny having performed an action? (Excessive non-repudiation harms privacy)
- [ ] **Detectability** threats assessed: Can the existence of personal data or processing be detected by unauthorized parties?
- [ ] **Disclosure of Information** threats assessed: Can personal data be exposed to unauthorized parties?
- [ ] **Unawareness** threats assessed: Are data subjects unaware of how their data is collected, processed, or shared?
- [ ] **Non-compliance** threats assessed: Does processing fail to comply with applicable regulations, policies, or consent?
- [ ] All 7 LINDDUN categories have been assessed against each system component handling personal data
- [ ] Threats have been mapped to specific components, data flows, and data elements (not generic)
- [ ] Risk levels have been assigned based on likelihood and impact (CRITICAL / HIGH / MEDIUM / LOW)
- [ ] Existing controls have been documented for each identified threat
- [ ] LINDDUN threat types have been verified against `linddun-go-threats.md`

---

## Phase 4: Data Subject Rights Assessment

- [ ] All applicable data subject rights have been identified per regulation (GDPR Art. 12-22, CCPA §1798.100-135, LGPD Art. 18, PIPL Art. 44-50, etc.)
- [ ] Right to Access: implementation mechanism verified (self-service portal, manual process, API)
- [ ] Right to Rectification/Correction: mechanism for correcting inaccurate data verified
- [ ] Right to Erasure/Deletion: deletion mechanism verified across all data stores (primary, backups, caches, processors)
- [ ] Right to Restrict Processing: mechanism for restricting processing while retaining data verified
- [ ] Right to Data Portability: export format verified (machine-readable, commonly used format)
- [ ] Right to Object: mechanism for objecting to specific processing purposes verified
- [ ] Automated Decision-Making: Art. 22 rights assessed if automated decisions with legal/significant effects exist
- [ ] CCPA-specific rights assessed: opt-out of sale/sharing (§1798.120), limit sensitive PI (§1798.121), non-discrimination (§1798.125)
- [ ] Response timelines verified against regulatory requirements (GDPR: 1 month, CCPA: 45 days, PIPEDA: 30 days)
- [ ] Identity verification mechanisms for rights requests assessed
- [ ] Gap analysis complete: each right rated as Implemented / Partial / Not Implemented with specific gaps documented

---

## Phase 5: Privacy by Design Evaluation

- [ ] **Principle 1 (Proactive)** evaluated: privacy risk assessment, threat modeling, privacy-aware defaults
- [ ] **Principle 2 (Default)** evaluated: data minimization, opt-in consent, minimal collection
- [ ] **Principle 3 (Embedded)** evaluated: encryption, pseudonymization, access controls, purpose-bound processing
- [ ] **Principle 4 (Positive-Sum)** evaluated: privacy-preserving analytics, no false trade-offs
- [ ] **Principle 5 (End-to-End)** evaluated: lifecycle protection, secure deletion, key management
- [ ] **Principle 6 (Transparency)** evaluated: processing logs, privacy notices, audit trails, consent receipts
- [ ] **Principle 7 (User-Centric)** evaluated: DSAR mechanisms, consent management, data portability, preference centers
- [ ] All 7 principles rated: Strong / Adequate / Weak / Absent
- [ ] Technical controls assessed against patterns in `privacy-by-design-patterns.md`
- [ ] Organizational measures reviewed (privacy policies, training, DPO, incident response)

---

## Phase 6: Recommendations

- [ ] All findings from Phases 1-5 have been captured as recommendations
- [ ] Findings are prioritized: CRITICAL (immediate action), HIGH (short-term), MEDIUM (planned), LOW (improvement)
- [ ] Each recommendation is specific and actionable (not generic — includes what to do, where, and why)
- [ ] Each recommendation includes: affected component, specific action, estimated effort, regulatory driver
- [ ] Remediation timeline has been suggested for each priority level
- [ ] Quick wins have been identified (high-impact, low-effort items)
- [ ] Dependencies between recommendations have been noted

---

## Final Quality Checklist

This checklist verifies the overall quality and integrity of the assessment output.

### Citation Integrity
- [ ] No hallucinated regulation citations: every GDPR article/recital verified against `gdpr-article-reference.md`
- [ ] No hallucinated non-GDPR citations: every non-GDPR citation verified against `global-privacy-regulations.md`
- [ ] Citations not found in reference files are marked as **[UNVERIFIED]**
- [ ] LINDDUN threat types verified against `linddun-go-threats.md` (7 categories: L-I-N-D-D-U-N)
- [ ] Data sensitivity classifications verified against `data-classification-taxonomy.md`
- [ ] Privacy by Design principle names and descriptions verified against `privacy-by-design-patterns.md`

### Evidence Grounding
- [ ] Every finding references specific data elements, code paths, configurations, or documentation actually observed in the target system
- [ ] No generic findings (e.g., "improve privacy practices" without citing specific deficiency)
- [ ] No speculative data elements listed in the data inventory (every element traceable to actual system artifact)
- [ ] Risk levels are justified by specific evidence, not assumed

### Completeness
- [ ] All sections of the output template (`dpia-output-template.md`) are filled in
- [ ] All applicable regulations have been addressed in the gap analysis
- [ ] All identified data subject rights have been assessed
- [ ] All 7 LINDDUN categories have been covered
- [ ] All 7 Privacy by Design principles have been evaluated
- [ ] Assumptions and limitations are documented

### Consistency
- [ ] Risk levels are consistent across sections (same finding does not have different severity in different sections)
- [ ] Data elements in the inventory match those referenced in threat analysis and gap analysis
- [ ] Regulatory citations in the gap analysis match those in the data subject rights assessment
- [ ] Recommendation priorities align with finding severity levels
