# SOC 2 Trust Services Criteria (2017, updated 2022)

## How to Use This Reference

When citing SOC 2 controls, verify the control ID and description match this file. Use the exact ID format: `CC[category].[number]` for Common Criteria, `A[number].[number]` for Availability, `PI[number].[number]` for Processing Integrity, `C[number].[number]` for Confidentiality, `P[number].[number]` for Privacy.

The Common Criteria (CC series) apply to ALL SOC 2 engagements. The additional categories (A, PI, C, P) apply only when included in the engagement scope.

## Common Criteria (CC)

### CC1 — Control Environment

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC1.1 | COSO Principle 1: Demonstrates commitment to integrity and ethical values | Code of conduct, ethics policies, tone at the top |
| CC1.2 | COSO Principle 2: Board exercises oversight responsibility | Board/governance oversight of security program |
| CC1.3 | COSO Principle 3: Establishes structure, authority, and responsibility | Org chart, security roles, reporting lines |
| CC1.4 | COSO Principle 4: Demonstrates commitment to competence | Hiring, training, certification requirements |
| CC1.5 | COSO Principle 5: Enforces accountability | Performance reviews, security responsibilities in JDs |

### CC2 — Communication and Information

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC2.1 | COSO Principle 13: Uses relevant information | Information quality, data classification |
| CC2.2 | COSO Principle 14: Communicates internally | Security awareness, policy communication |
| CC2.3 | COSO Principle 15: Communicates externally | External communication, incident notification |

### CC3 — Risk Assessment

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC3.1 | COSO Principle 6: Specifies suitable objectives | Security objectives aligned to business |
| CC3.2 | COSO Principle 7: Identifies and analyzes risk | Risk assessment process, threat identification |
| CC3.3 | COSO Principle 8: Assesses fraud risk | Fraud risk assessment |
| CC3.4 | COSO Principle 9: Identifies and analyzes significant change | Change management risk |

### CC4 — Monitoring Activities

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC4.1 | COSO Principle 16: Selects, develops, and performs ongoing/separate evaluations | Continuous monitoring, audits |
| CC4.2 | COSO Principle 17: Evaluates and communicates deficiencies | Deficiency tracking, remediation |

### CC5 — Control Activities

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC5.1 | COSO Principle 10: Selects and develops control activities | Control design and implementation |
| CC5.2 | COSO Principle 11: Selects and develops general controls over technology | IT general controls |
| CC5.3 | COSO Principle 12: Deploys through policies and procedures | Policy enforcement |

### CC6 — Logical and Physical Access Controls

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC6.1 | Logical access security software, infrastructure, and architectures | Authentication, MFA, SSO, access provisioning |
| CC6.2 | Prior to issuing credentials and granting access, registration and authorization | User registration, identity verification |
| CC6.3 | Based on authorization, access to protected assets is modified or removed | Access reviews, deprovisioning, least privilege |
| CC6.4 | Restricts physical access | Data center security, badge access |
| CC6.5 | Discontinues logical and physical protections over disposed assets | Secure disposal, media sanitization |
| CC6.6 | Restricts access through boundaries (network, DMZ, firewall) | Network segmentation, firewalls, VPN |
| CC6.7 | Restricts transmission, movement, and removal of information | Data loss prevention, transfer controls |
| CC6.8 | Prevents or detects unauthorized or malicious software | Anti-malware, endpoint protection |

### CC7 — System Operations

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC7.1 | Detects and monitors security events and anomalies | SIEM, log monitoring, alerting |
| CC7.2 | Monitors system components for anomalies | Infrastructure monitoring, performance |
| CC7.3 | Evaluates security events to determine incidents | Incident triage, classification |
| CC7.4 | Responds to identified security incidents | Incident response plan, containment |
| CC7.5 | Identifies and remediates vulnerabilities | Vulnerability management, patching |

### CC8 — Change Management

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC8.1 | Authorizes, designs, develops, configures, documents, tests, approves, and implements changes | SDLC, change control, testing |

### CC9 — Risk Mitigation

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| CC9.1 | Identifies and assesses risk mitigation activities including vendor management | Third-party risk, vendor assessment |
| CC9.2 | Assesses and manages risks associated with vendors and business partners | Vendor due diligence, contracts, monitoring |

## Additional Trust Service Categories

### Availability (A)

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| A1.1 | Maintains, monitors, and evaluates capacity and demand | Capacity planning, scaling |
| A1.2 | Authorizes, designs, develops, implements, operates, and monitors environmental protections | DR, BCP, redundancy |
| A1.3 | Tests recovery plan procedures | DR testing, failover testing |

### Processing Integrity (PI)

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| PI1.1 | Obtains or generates, uses, and communicates relevant quality information | Data quality controls |
| PI1.2 | Implements policies and procedures over system inputs | Input validation |
| PI1.3 | Implements policies and procedures over system processing | Processing accuracy |
| PI1.4 | Implements policies and procedures to make available or deliver output | Output completeness |
| PI1.5 | Implements policies and procedures to store inputs, items in processing, and outputs | Data retention |

### Confidentiality (C)

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| C1.1 | Identifies and maintains confidential information | Data classification |
| C1.2 | Disposes of confidential information | Secure deletion |

### Privacy (P)

| ID | Criteria | Key Requirements |
|----|----------|-----------------|
| P1.0 | Privacy criteria: Accepts and obtains commitments | Privacy notice, consent management |
| P1.1 | Notice: Provides notice about its privacy practices | Privacy policy, data use disclosures |
| P2.1 | Choice and Consent: Communicates choices to data subjects | Opt-in/opt-out mechanisms |
| P3.1 | Collection: Collects personal information consistent with objectives | Data minimization, purpose limitation |
| P3.2 | Collection: Collects personal information for purposes identified in the notice | Collection aligned to stated purposes |
| P4.1 | Use, Retention, and Disposal: Limits use to purposes identified | Purpose limitation enforcement |
| P4.2 | Use, Retention, and Disposal: Retains and disposes per objectives | Retention schedules, secure deletion |
| P4.3 | Use, Retention, and Disposal: Provides notice of new purposes | Re-consent for new uses |
| P5.1 | Access: Provides data subjects with access | Data subject access requests (DSARs) |
| P5.2 | Access: Authenticates identity before granting access | Identity verification for access requests |
| P6.1 | Disclosure and Notification: Discloses personal information only for identified purposes | Third-party data sharing controls |
| P6.2 | Disclosure and Notification: Creates and retains record of authorized disclosures | Disclosure logging |
| P6.3 | Disclosure and Notification: Provides reliable information about system processing | Processing transparency |
| P6.4 | Disclosure and Notification: Obtains commitments from third parties | Third-party data processing agreements |
| P6.5 | Disclosure and Notification: Notifies affected parties of actual or suspected breaches | Breach notification |
| P6.6 | Disclosure and Notification: Provides notice of changes to privacy commitments | Privacy policy update notification |
| P6.7 | Disclosure and Notification: Provides notice if personal information is used in automated decision-making | Algorithmic transparency |
| P7.1 | Quality: Collects and maintains accurate, complete information | Data quality controls |
| P8.1 | Monitoring and Enforcement: Monitors compliance with privacy commitments | Privacy program monitoring |

## Quick Reference: Control ID Format

| Category | ID Format | Example | Applies When |
|----------|-----------|---------|--------------|
| Common Criteria | CC[1-9].[1-8] | CC6.1 | Always (all SOC 2 engagements) |
| Availability | A1.[1-3] | A1.2 | Availability in scope |
| Processing Integrity | PI1.[1-5] | PI1.3 | Processing Integrity in scope |
| Confidentiality | C1.[1-2] | C1.1 | Confidentiality in scope |
| Privacy | P[1-8].[0-7] | P5.1 | Privacy in scope |
