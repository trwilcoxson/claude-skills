# Privacy Impact Assessment — Output Template

This template defines the required output structure for the privacy assessment agent. All sections must be completed. Every finding MUST cite specific data elements, code paths, or configuration evidence.

---

## Metadata

| Field | Value |
|---|---|
| **Agent** | privacy-agent |
| **Date** | {YYYY-MM-DD} |
| **Target System** | {system name and version} |
| **Applicable Regulations** | {list of applicable regulations, e.g., GDPR, CCPA/CPRA, HIPAA} |
| **Assessment Scope** | {description of what was assessed — codebase, architecture, specific components} |
| **Assessment Type** | {PIA / DPIA / Both} |
| **Risk Level (Overall)** | {CRITICAL / HIGH / MEDIUM / LOW} |

---

## 1. Executive Summary

### Overall Risk Assessment

| Metric | Value |
|---|---|
| **Overall Risk Level** | {CRITICAL / HIGH / MEDIUM / LOW} |
| **Total Findings** | {number} |
| **Critical Findings** | {number} |
| **High Findings** | {number} |
| **Medium Findings** | {number} |
| **Low Findings** | {number} |

### Key Findings

{2-3 sentence summary of the most significant privacy risks identified.}

### Regulatory Obligations

{Summary of primary regulatory obligations and compliance status. List which regulations apply and whether the system is broadly compliant, partially compliant, or non-compliant.}

---

## 2. System Description

### System Overview

{Brief description of the system's purpose, architecture, and processing activities.}

### Data Flows

{Description of how personal data flows through the system — collection, processing, storage, sharing, deletion.}

```
{Data flow diagram or description}
```

### Processing Activities

| Activity | Description | Data Types | Legal Basis | Data Subjects |
|---|---|---|---|---|
| {activity name} | {what happens} | {types of data processed} | {legal basis per regulation} | {who the data is about} |

### Data Subjects

| Category | Description | Estimated Volume | Vulnerable Population? |
|---|---|---|---|
| {e.g., Customers} | {description} | {number} | {Yes/No — children, patients, employees, etc.} |

### Data Types Processed

| Data Type | Sensitivity Level | Regulation-Specific Classification |
|---|---|---|
| {e.g., Email address} | {PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED} | {e.g., GDPR Art. 4(1) personal data, CCPA §1798.140 PI} |

---

## 3. Data Inventory

| Data Element | Category | Sensitivity | Source | Purpose | Legal Basis | Retention | Recipients |
|---|---|---|---|---|---|---|---|
| {field name} | {per data-classification-taxonomy.md} | {PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED} | {where collected from} | {why it is processed} | {legal basis per applicable regulation} | {retention period} | {who receives this data — internal teams, processors, third parties} |

> **Verification:** Every data element must be traceable to an actual field in the system (database column, API field, form field, log entry, etc.). Do not list speculative data elements.

---

## 4. LINDDUN Threat Analysis

### Threat Summary

| LINDDUN Category | Threats Identified | Highest Risk Level |
|---|---|---|
| Linkability | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Identifiability | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Non-repudiation | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Detectability | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Disclosure of Information | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Unawareness | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |
| Non-compliance | {count} | {CRITICAL / HIGH / MEDIUM / LOW / N/A} |

### Detailed Threat Analysis

For each identified threat:

| Field | Value |
|---|---|
| **Threat ID** | {LINDDUN-001, LINDDUN-002, etc.} |
| **Category** | {Linkability / Identifiability / Non-repudiation / Detectability / Disclosure of Information / Unawareness / Non-compliance} |
| **Threat Description** | {Specific description of the threat — what could happen, to whom} |
| **Affected Data/Component** | {Specific data elements or system components affected — cite actual fields/paths} |
| **Risk Level** | {CRITICAL / HIGH / MEDIUM / LOW} |
| **Likelihood** | {High / Medium / Low} |
| **Impact** | {High / Medium / Low} |
| **Existing Controls** | {What controls are currently in place, if any} |
| **Recommendations** | {Specific remediation actions} |

> **Verification:** Threat categories MUST match the LINDDUN GO framework as defined in `linddun-go-threats.md`. Do not invent threat categories.

---

## 5. Regulatory Gap Analysis

### Compliance Summary

| Regulation | Compliant | Partial | Non-Compliant | Not Assessed |
|---|---|---|---|---|
| {e.g., GDPR} | {count} | {count} | {count} | {count} |

### Detailed Gap Analysis

For each regulatory requirement assessed:

| Field | Value |
|---|---|
| **Requirement** | {Description of the regulatory requirement} |
| **Citation** | {Exact regulation section/article — e.g., GDPR Art. 13(1)(a), CCPA §1798.100} |
| **Status** | {Compliant / Partial / Non-Compliant} |
| **Evidence** | {What was observed in the system — specific code, config, or documentation} |
| **Gap Description** | {What is missing or insufficient — be specific} |
| **Remediation** | {Specific action to close the gap} |
| **Priority** | {CRITICAL / HIGH / MEDIUM / LOW} |

> **Verification:** Every citation MUST be verified against `gdpr-article-reference.md` (for GDPR) or `global-privacy-regulations.md` (for other regulations). If a citation is not found in these references, mark it as **[UNVERIFIED]**.

---

## 6. Data Subject Rights Assessment

| Right | Regulation | Implementation Status | Mechanism | Gaps |
|---|---|---|---|---|
| Right to Access | {e.g., GDPR Art. 15, CCPA §1798.110} | {Implemented / Partial / Not Implemented} | {How the right is fulfilled — e.g., self-service portal, manual process} | {What is missing} |
| Right to Rectification | {e.g., GDPR Art. 16, CCPA §1798.106} | {status} | {mechanism} | {gaps} |
| Right to Erasure | {e.g., GDPR Art. 17, CCPA §1798.105} | {status} | {mechanism} | {gaps} |
| Right to Restrict Processing | {e.g., GDPR Art. 18} | {status} | {mechanism} | {gaps} |
| Right to Data Portability | {e.g., GDPR Art. 20} | {status} | {mechanism} | {gaps} |
| Right to Object | {e.g., GDPR Art. 21} | {status} | {mechanism} | {gaps} |
| Right Not to Be Subject to Automated Decisions | {e.g., GDPR Art. 22} | {status} | {mechanism} | {gaps} |
| Right to Opt-Out of Sale/Sharing | {e.g., CCPA §1798.120} | {status} | {mechanism} | {gaps} |
| Right to Limit Use of Sensitive PI | {e.g., CCPA §1798.121} | {status} | {mechanism} | {gaps} |
| Right to Non-Discrimination | {e.g., CCPA §1798.125} | {status} | {mechanism} | {gaps} |

> **Note:** Include only rights applicable under the identified regulations. Add regulation-specific rights as needed (e.g., LGPD Art. 18 rights, PIPL Art. 44-50 rights).

---

## 7. Cross-Border Transfer Analysis

*Include this section if personal data crosses jurisdictional boundaries.*

| Transfer | Source Jurisdiction | Destination Jurisdiction | Transfer Mechanism | Legal Basis | Status |
|---|---|---|---|---|---|
| {description of transfer} | {e.g., EU} | {e.g., US} | {e.g., SCCs, BCRs, adequacy decision} | {specific legal provision} | {Adequate / Insufficient / Not Assessed} |

### Transfer Risk Assessment

{Assessment of whether transfer mechanisms are adequate for the data types and volumes involved. Reference GDPR Art. 44-49, PIPL Art. 38-43, LGPD Art. 33-36, or other applicable provisions.}

---

## 8. Privacy by Design Evaluation

Assess the system against each of the 7 foundational principles (reference: `privacy-by-design-patterns.md`).

| Principle | Rating | Evidence | Recommendations |
|---|---|---|---|
| 1. Proactive not Reactive | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 2. Privacy as the Default | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 3. Privacy Embedded into Design | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 4. Full Functionality (Positive-Sum) | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 5. End-to-End Security | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 6. Visibility and Transparency | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |
| 7. Respect for User Privacy | {Strong / Adequate / Weak / Absent} | {What was observed} | {Specific improvements} |

---

## 9. Recommendations

### Critical Priority

| ID | Finding | Affected Component | Recommendation | Estimated Effort | Regulatory Driver |
|---|---|---|---|---|---|
| REC-C-{n} | {finding} | {component/data element} | {specific action} | {S/M/L/XL} | {regulation and section} |

### High Priority

| ID | Finding | Affected Component | Recommendation | Estimated Effort | Regulatory Driver |
|---|---|---|---|---|---|
| REC-H-{n} | {finding} | {component/data element} | {specific action} | {S/M/L/XL} | {regulation and section} |

### Medium Priority

| ID | Finding | Affected Component | Recommendation | Estimated Effort | Regulatory Driver |
|---|---|---|---|---|---|
| REC-M-{n} | {finding} | {component/data element} | {specific action} | {S/M/L/XL} | {regulation and section} |

### Low Priority

| ID | Finding | Affected Component | Recommendation | Estimated Effort | Regulatory Driver |
|---|---|---|---|---|---|
| REC-L-{n} | {finding} | {component/data element} | {specific action} | {S/M/L/XL} | {regulation and section} |

---

## 10. Assumptions and Limitations

### Assumptions

- {List assumptions made during the assessment, e.g., "Assumed database encryption is AES-256 based on configuration files reviewed."}

### Limitations

- {List limitations of the assessment, e.g., "Runtime behavior was not observed; analysis based on static code review only."}
- {e.g., "Third-party processor agreements were not available for review."}

### Out of Scope

- {List items explicitly excluded from assessment scope.}

---

> **CRITICAL: Every finding MUST cite specific data elements, code paths, or configuration evidence. Generic findings such as "the system should improve its privacy practices" are unacceptable. Each finding must reference actual components, fields, or configurations observed in the target system.**
