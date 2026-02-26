# HIPAA Security Rule — Verified Reference

> **Purpose**: This file contains verified HIPAA Security Rule citations (45 CFR Part 164 Subpart C) for agent use during compliance assessments. Agents MUST cross-reference findings against this table to prevent hallucinated control IDs.

## Required vs Addressable

- **(R) Required**: The implementation specification MUST be implemented as stated.
- **(A) Addressable**: The covered entity must assess whether the specification is reasonable and appropriate. If yes, implement it. If not, document why and implement an equivalent alternative measure, or document why the specification is not applicable.

**Addressable does NOT mean optional.** It means the entity must perform a documented analysis and either implement, implement an alternative, or justify non-implementation.

## How to Cite

Format: `§164.[section]([subsection])([detail])`. Example: `§164.312(a)(2)(iv)` = Encryption and Decryption under Technical Safeguards — Access Control.

---

## §164.308 — Administrative Safeguards

| Citation | Standard / Implementation Specification | R/A | Description |
|----------|----------------------------------------|-----|-------------|
| §164.308(a)(1)(i) | Security Management Process | R | Implement policies and procedures to prevent, detect, contain, and correct security violations |
| §164.308(a)(1)(ii)(A) | Risk Analysis | R | Conduct an accurate and thorough assessment of potential risks and vulnerabilities to ePHI |
| §164.308(a)(1)(ii)(B) | Risk Management | R | Implement security measures sufficient to reduce risks and vulnerabilities to a reasonable and appropriate level |
| §164.308(a)(1)(ii)(C) | Sanction Policy | R | Apply appropriate sanctions against workforce members who fail to comply with security policies |
| §164.308(a)(1)(ii)(D) | Information System Activity Review | R | Implement procedures to regularly review records of information system activity (audit logs, access reports, security incident tracking) |
| §164.308(a)(2) | Assigned Security Responsibility | R | Identify the security official responsible for developing and implementing security policies and procedures |
| §164.308(a)(3)(i) | Workforce Security | R | Implement policies and procedures to ensure all workforce members have appropriate access to ePHI |
| §164.308(a)(3)(ii)(A) | Authorization and/or Supervision | A | Implement procedures for the authorization and/or supervision of workforce members who work with ePHI |
| §164.308(a)(3)(ii)(B) | Workforce Clearance Procedure | A | Implement procedures to determine that the access of a workforce member to ePHI is appropriate |
| §164.308(a)(3)(ii)(C) | Termination Procedures | A | Implement procedures for terminating access to ePHI when employment ends or access is no longer required |
| §164.308(a)(4)(i) | Information Access Management | R | Implement policies and procedures for authorizing access to ePHI consistent with the Privacy Rule |
| §164.308(a)(4)(ii)(A) | Isolating Health Care Clearinghouse Functions | R | If a healthcare clearinghouse is part of a larger organization, protect ePHI from unauthorized access by the larger organization |
| §164.308(a)(4)(ii)(B) | Access Authorization | A | Implement policies and procedures for granting access to ePHI (e.g., through workstations, programs, processes) |
| §164.308(a)(4)(ii)(C) | Access Establishment and Modification | A | Implement policies and procedures that establish, document, review, and modify access to ePHI based on the Privacy Rule |
| §164.308(a)(5)(i) | Security Awareness and Training | R | Implement a security awareness and training program for all workforce members |
| §164.308(a)(5)(ii)(A) | Security Reminders | A | Periodic security updates |
| §164.308(a)(5)(ii)(B) | Protection from Malicious Software | A | Procedures for guarding against, detecting, and reporting malicious software |
| §164.308(a)(5)(ii)(C) | Log-in Monitoring | A | Procedures for monitoring log-in attempts and reporting discrepancies |
| §164.308(a)(5)(ii)(D) | Password Management | A | Procedures for creating, changing, and safeguarding passwords |
| §164.308(a)(6)(i) | Security Incident Procedures | R | Implement policies and procedures to address security incidents |
| §164.308(a)(6)(ii) | Response and Reporting | R | Identify and respond to suspected or known security incidents; mitigate harmful effects; document incidents and outcomes |
| §164.308(a)(7)(i) | Contingency Plan | R | Establish and implement policies and procedures for responding to an emergency or other occurrence that damages systems containing ePHI |
| §164.308(a)(7)(ii)(A) | Data Backup Plan | R | Establish and implement procedures to create and maintain retrievable exact copies of ePHI |
| §164.308(a)(7)(ii)(B) | Disaster Recovery Plan | R | Establish and implement procedures to restore any loss of data |
| §164.308(a)(7)(ii)(C) | Emergency Mode Operation Plan | R | Establish and implement procedures to enable continuation of critical business processes for protection of ePHI during emergency |
| §164.308(a)(7)(ii)(D) | Testing and Revision Procedures | A | Implement procedures for periodic testing and revision of contingency plans |
| §164.308(a)(7)(ii)(E) | Applications and Data Criticality Analysis | A | Assess the relative criticality of specific applications and data in support of contingency plan components |
| §164.308(a)(8) | Evaluation | R | Perform a periodic technical and nontechnical evaluation in response to environmental or operational changes affecting the security of ePHI |
| §164.308(b)(1) | Business Associate Contracts and Other Arrangements | R | Covered entity may permit a business associate to create, receive, maintain, or transmit ePHI only if satisfactory assurances are obtained |
| §164.308(b)(3) | Written Contract or Other Arrangement | R | Document the satisfactory assurances required through a written contract or other arrangement with the business associate |

## §164.310 — Physical Safeguards

| Citation | Standard / Implementation Specification | R/A | Description |
|----------|----------------------------------------|-----|-------------|
| §164.310(a)(1) | Facility Access Controls | R | Implement policies and procedures to limit physical access to electronic information systems and the facilities in which they are housed |
| §164.310(a)(2)(i) | Contingency Operations | A | Establish procedures that allow facility access in support of restoration of lost data under the DR and emergency mode operations plans |
| §164.310(a)(2)(ii) | Facility Security Plan | A | Implement policies and procedures to safeguard the facility and equipment from unauthorized physical access, tampering, and theft |
| §164.310(a)(2)(iii) | Access Control and Validation Procedures | A | Implement procedures to control and validate a person's access to facilities based on their role or function |
| §164.310(a)(2)(iv) | Maintenance Records | A | Implement policies and procedures to document repairs and modifications to the physical components of a facility related to security |
| §164.310(b) | Workstation Use | R | Implement policies and procedures that specify the proper functions to be performed, manner of performance, and physical attributes of surroundings of workstations accessing ePHI |
| §164.310(c) | Workstation Security | R | Implement physical safeguards for all workstations that access ePHI, to restrict access to authorized users |
| §164.310(d)(1) | Device and Media Controls | R | Implement policies and procedures that govern the receipt and removal of hardware and electronic media containing ePHI into and out of a facility |
| §164.310(d)(2)(i) | Disposal | R | Implement policies and procedures to address the final disposition of ePHI and the hardware or electronic media on which it is stored |
| §164.310(d)(2)(ii) | Media Re-use | R | Implement procedures for removal of ePHI from electronic media before it is made available for re-use |
| §164.310(d)(2)(iii) | Accountability | A | Maintain a record of the movements of hardware and electronic media and any person responsible |
| §164.310(d)(2)(iv) | Data Backup and Storage | A | Create a retrievable, exact copy of ePHI when needed, before movement of equipment |

## §164.312 — Technical Safeguards

| Citation | Standard / Implementation Specification | R/A | Description |
|----------|----------------------------------------|-----|-------------|
| §164.312(a)(1) | Access Control | R | Implement technical policies and procedures for electronic information systems that maintain ePHI to allow access only to authorized persons or software programs |
| §164.312(a)(2)(i) | Unique User Identification | R | Assign a unique name and/or number for identifying and tracking user identity |
| §164.312(a)(2)(ii) | Emergency Access Procedure | R | Establish and implement procedures for obtaining necessary ePHI during an emergency |
| §164.312(a)(2)(iii) | Automatic Logoff | A | Implement electronic procedures that terminate an electronic session after a predetermined time of inactivity |
| §164.312(a)(2)(iv) | Encryption and Decryption | A | Implement a mechanism to encrypt and decrypt ePHI |
| §164.312(b) | Audit Controls | R | Implement hardware, software, and/or procedural mechanisms that record and examine activity in information systems that contain or use ePHI |
| §164.312(c)(1) | Integrity | R | Implement policies and procedures to protect ePHI from improper alteration or destruction |
| §164.312(c)(2) | Mechanism to Authenticate ePHI | A | Implement electronic mechanisms to corroborate that ePHI has not been altered or destroyed in an unauthorized manner |
| §164.312(d) | Person or Entity Authentication | R | Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed |
| §164.312(e)(1) | Transmission Security | R | Implement technical security measures to guard against unauthorized access to ePHI being transmitted over an electronic communications network |
| §164.312(e)(2)(i) | Integrity Controls | A | Implement security measures to ensure that electronically transmitted ePHI is not improperly modified without detection until disposed of |
| §164.312(e)(2)(ii) | Encryption | A | Implement a mechanism to encrypt ePHI whenever deemed appropriate |

## §164.314 — Organizational Requirements

| Citation | Standard / Implementation Specification | R/A | Description |
|----------|----------------------------------------|-----|-------------|
| §164.314(a)(1) | Business Associate Contracts or Other Arrangements | R | Covered entity is not in compliance if it knew of a pattern of activity or practice of the business associate that constituted a material breach and did not take reasonable steps to cure |
| §164.314(a)(2)(i) | Business Associate Contracts | R | Contract must establish the permitted and required uses and disclosures of ePHI by the business associate |
| §164.314(a)(2)(ii) | Other Arrangements | R | When other arrangements are permitted, the covered entity must document the arrangements |
| §164.314(b)(1) | Requirements for Group Health Plans | R | Plan documents must incorporate provisions requiring the plan sponsor to implement security measures and ensure adequate separation |
| §164.314(b)(2) | Implementation Specifications | R | Group health plan must ensure plan documents include required provisions |

## §164.316 — Policies and Procedures and Documentation Requirements

| Citation | Standard / Implementation Specification | R/A | Description |
|----------|----------------------------------------|-----|-------------|
| §164.316(a) | Policies and Procedures | R | Implement reasonable and appropriate policies and procedures to comply with the Security Rule |
| §164.316(b)(1) | Documentation | R | Maintain policies and procedures in written (which may be electronic) form |
| §164.316(b)(2)(i) | Time Limit | R | Retain documentation for 6 years from the date of its creation or the date when it last was in effect, whichever is later |
| §164.316(b)(2)(ii) | Availability | R | Make documentation available to those persons responsible for implementing the procedures |
| §164.316(b)(2)(iii) | Updates | R | Review documentation periodically and update as needed in response to environmental or operational changes |

## §164.408 — Breach Notification

| Citation | Standard | R/A | Description |
|----------|---------|-----|-------------|
| §164.408(a) | Notification to Individuals | R | Notify each individual whose unsecured PHI has been, or is reasonably believed to have been, accessed, acquired, used, or disclosed as a result of a breach |
| §164.408(b) | Timeliness of Notification | R | Notification without unreasonable delay and in no case later than 60 calendar days from the date of discovery |
| §164.408(c) | Content of Notification | R | Must include: description of breach, types of information involved, steps individuals should take, what the entity is doing, and contact procedures |

## Quick Reference: Safeguard Counts

| Safeguard Category | Citation Root | Standards | Required Impl Specs | Addressable Impl Specs |
|--------------------|-------------|-----------|---------------------|----------------------|
| Administrative | §164.308 | 9 | 14 | 9 |
| Physical | §164.310 | 4 | 5 | 5 |
| Technical | §164.312 | 5 | 4 | 5 |
| Organizational | §164.314 | 2 | 4 | 0 |
| Policies & Documentation | §164.316 | 2 | 4 | 0 |
