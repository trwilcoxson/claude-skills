# Privacy by Design Patterns — Verified Reference

This reference provides implementation patterns for the 7 foundational Privacy by Design principles (Cavoukian, 2009). Agents use this to evaluate systems against each principle and recommend specific privacy-enhancing implementations.

---

## The 7 Foundational Principles

### Principle 1: Proactive not Reactive; Preventative not Remedial

Privacy risks are anticipated and prevented before they materialize, rather than addressed after privacy-invasive events occur.

**Design Goal:** Threat model for privacy risks before development.

**Assessment Questions:**
- Does the system anticipate privacy risks before they materialize?
- Are privacy controls built in from the start, not added after incidents?
- Was a privacy risk assessment conducted during the design phase?
- Are there mechanisms to detect emerging privacy risks proactively?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| LINDDUN Analysis | Structured privacy threat modeling | LINDDUN GO threat assessment before development begins |
| PIA/DPIA Before Launch | Privacy impact assessment as a gate | Mandatory PIA/DPIA sign-off before production deployment |
| Privacy Risk Register | Ongoing tracking of privacy risks | Risk register with likelihood/impact scoring, mitigation tracking |
| Automated PII Detection | Detect personal data in unexpected locations | DLP scanning, log analysis for PII, schema scanning |
| Privacy Review Gates | Privacy assessment in release process | Privacy review in CI/CD pipeline, pre-release checklists |

---

### Principle 2: Privacy as the Default Setting

Personal data is automatically protected in any system. No action is required by the individual to protect their privacy.

**Design Goal:** Minimum data collection, opt-in not opt-out.

**Assessment Questions:**
- Is the most privacy-protective option the default?
- Must users take affirmative action to reduce their privacy (opt-in model)?
- Is data collection limited to only what is necessary by default?
- Are retention periods minimized by default?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Data Minimization by Default | Collect only what is necessary | Required vs optional field distinction, progressive data collection |
| Strict Consent | Granular consent per purpose, not bundled | Consent management platform, per-purpose toggles |
| No Pre-Checked Boxes | Opt-in, not opt-out | All consent checkboxes unchecked by default |
| Privacy-Preserving Defaults in UIs | Most protective settings enabled | Privacy settings default to maximum protection; sharing off by default |
| Default Data Retention | Shortest reasonable retention | Auto-deletion policies, retention scheduler, TTL on records |
| Minimal API Responses | Return only requested fields | Field-level selection in APIs, sparse fieldsets, projection |

---

### Principle 3: Privacy Embedded into Design

Privacy is an integral component of the core functionality. It is embedded into the design and architecture, not bolted on as an add-on.

**Design Goal:** Privacy controls integral to architecture, not bolted on.

**Assessment Questions:**
- Is privacy integral to the core functionality, not an afterthought?
- Is privacy embedded into the system architecture?
- Are privacy controls part of the data model, not just the UI?
- Does the architecture minimize unnecessary data exposure between components?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Encryption at Rest/Transit | Protect data wherever it exists | TLS 1.2+/1.3 in transit, AES-256 at rest, field-level encryption for sensitive fields |
| Pseudonymization | Replace identifiers with tokens | Tokenization services, key-based pseudonymization, separate identity stores |
| Access Controls | Principle of least privilege | RBAC/ABAC, per-purpose access policies, need-to-know enforcement |
| Purpose-Bound Processing | Data used only for stated purpose | Per-purpose access control policies, processing activity logs |
| Architectural Separation | Separate identity from activity data | Separate databases for PII vs behavioral data, linked by tokens |

---

### Principle 4: Full Functionality — Positive-Sum, not Zero-Sum

Privacy and functionality are both achieved. Avoid false trade-offs between privacy and utility.

**Design Goal:** Privacy AND functionality, avoid false trade-offs.

**Assessment Questions:**
- Does the design accommodate all legitimate interests without sacrificing privacy?
- Can privacy and core functionality coexist without compromise?
- Are there creative solutions that achieve both business goals and privacy protection?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Differential Privacy | Statistical utility with formal privacy guarantees | Calibrated noise addition to aggregate queries, privacy budget management |
| Federated Learning | ML model training without centralizing raw data | On-device training, gradient sharing only, federated aggregation |
| Privacy-Preserving Authentication | Verify identity without over-collecting | Zero-knowledge proofs for age verification, credential verification without disclosure |
| Synthetic Data | Development and testing without real PII | Data generation matching statistical properties of real data |
| Homomorphic Encryption | Computation on encrypted data | Encrypted analytics, secure aggregation without decryption |
| Secure Multi-Party Computation | Joint computation without sharing raw data | Protocol-based computation across parties, secret sharing |

---

### Principle 5: End-to-End Security — Full Lifecycle Protection

Data is protected from collection through deletion. Security is maintained at every stage of the data lifecycle.

**Design Goal:** Protect data from collection through deletion.

**Assessment Questions:**
- Is personal data secured throughout its entire lifecycle?
- Are there secure deletion mechanisms that work across all storage locations?
- Is data protected at every stage: collection, transit, rest, processing, disposal?
- Are backup and disaster recovery processes privacy-aware?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Secure Ingestion | Protect data at point of collection | HTTPS-only collection endpoints, input validation, minimal client-side storage |
| Processing Isolation | Protect data during processing | Secure enclaves, memory encryption, process isolation, no logging of PII |
| Encrypted Storage | Protect data at rest | AES-256, field-level encryption for sensitive fields, encrypted databases |
| Secure Deletion / Crypto-Shredding | Cryptographic erasure | Delete encryption key to render data unrecoverable; verified deletion across all copies |
| Retention Enforcement | Automated lifecycle management | Retention policies with automated enforcement, lifecycle state tracking, TTL enforcement |
| Key Management | Secure key storage and rotation | HSM/KMS, automated key rotation, separation of duties for key access |
| Backup Privacy | Privacy controls on backups | Encrypted backups, retention limits on backups, tested restoration with deletion verification |

---

### Principle 6: Visibility and Transparency — Keep it Open

All processing activities are documented, verifiable, and visible to data subjects and oversight bodies.

**Design Goal:** Accountability and auditability.

**Assessment Questions:**
- Are all processing activities documented and verifiable?
- Can data subjects verify that privacy promises are being kept?
- Are privacy policies accurate and understandable?
- Is there independent verification of privacy practices?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Privacy Dashboards | Give users visibility into their data | Self-service data access portal, processing history, consent status |
| Consent Receipts | Proof of consent transactions | Machine-readable consent receipts (Kantara Initiative format), consent audit trail |
| Processing Logs | Record all processing activities | ROPA automation, processing activity registry, data lineage tracking |
| Privacy Impact Assessments Published | Transparency of risk assessments | PIA/DPIA summaries available to stakeholders |
| Breach Notification Procedures | Documented response plans | Incident response playbooks, notification templates, regulatory timeline tracking |
| Audit Logging | Record all access to personal data | Immutable audit logs, access tracking, query logging for PII stores |
| Algorithmic Transparency | Explain automated decisions | Decision explanation logs, model interpretability, meaningful information about logic |

---

### Principle 7: Respect for User Privacy — Keep it User-Centric

The interests of the individual are paramount. The system empowers data subjects with strong defaults, appropriate notice, and user-friendly options.

**Design Goal:** User control over their data.

**Assessment Questions:**
- Are individual privacy interests the highest priority?
- Can users easily exercise their data protection rights?
- Is the consent experience clear, not manipulative?
- Are privacy settings accessible and understandable?

**Implementations:**
| Pattern | Description | Technical Implementation |
|---|---|---|
| Self-Service Data Access/Export/Deletion | Automated DSAR fulfillment | Self-service portal, automated data export (JSON/CSV), identity verification, cascading deletion |
| Granular Consent Management | Easy consent granting and withdrawal | Consent management platform, preference center, per-purpose toggles, withdrawal mechanism |
| Data Portability | Structured, machine-readable export | Standard formats (Data Transfer Project), API access, JSON/CSV export |
| Preference Centers | Centralized privacy settings | Privacy settings prominent in UI, plain language, no dark patterns |
| Complaint Mechanism | Easy way to raise privacy concerns | In-app feedback, dedicated privacy contact, escalation path |
| Privacy UX | Intuitive privacy controls | Privacy settings not buried in menus, plain language, no manipulative patterns |

---

## Technical Privacy Patterns — Summary

Common technical implementations that span multiple PbD principles:

| Pattern | Description | Relevant Principles |
|---|---|---|
| **Data Minimization** | Collect only what is needed; field-level justification for each data element | 1, 2, 3 |
| **Purpose Limitation** | Purpose-binding metadata on all data; processing logs per declared purpose | 2, 3, 6 |
| **Pseudonymization** | Replace direct identifiers with tokens; maintain mapping table separately with strict access controls | 3, 5 |
| **Anonymization** | k-anonymity (indistinguishable from k-1 others), l-diversity (diverse sensitive values), t-closeness (distribution similarity), differential privacy (mathematical guarantee) | 3, 4 |
| **Consent Management** | Consent receipts (Kantara Initiative), granular opt-in per purpose, easy withdrawal mechanisms, consent version tracking | 2, 6, 7 |
| **Data Subject Rights Automation** | Self-service portals for access/export/deletion, automated DSAR response pipelines, data inventory for right-to-erasure cascading | 6, 7 |
| **Cross-Border Transfer Safeguards** | Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs), adequacy decisions, data localization where required | 5, 6 |
| **Retention Management** | Automated retention policies per purpose, retention schedules aligned to legal requirements, crypto-shredding for expired data | 2, 5 |
