# NIST 800-53 Rev 5 — Security and Privacy Controls (Moderate Baseline)

## How to Use This Reference

ID format: `[FAMILY]-[NUMBER]` with optional enhancement `([ENHANCEMENT])`. Example: `AC-2(1)` is the first enhancement of Account Management in the Access Control family. There are 20 control families.

This reference focuses on the **Moderate baseline** — the most commonly applicable baseline for systems processing sensitive but unclassified information. Controls listed are those selected for the moderate baseline. Not every control in a family is included in the moderate baseline.

## Control Family Summary

| ID | Family Name | Moderate Baseline Key Controls |
|----|-------------|-------------------------------|
| AC | Access Control | AC-1 through AC-22 (selected) |
| AT | Awareness and Training | AT-1 through AT-4 |
| AU | Audit and Accountability | AU-1 through AU-12 (selected) |
| CA | Assessment, Authorization and Monitoring | CA-1 through CA-9 (selected) |
| CM | Configuration Management | CM-1 through CM-11 (selected) |
| CP | Contingency Planning | CP-1 through CP-10 (selected) |
| IA | Identification and Authentication | IA-1 through IA-12 (selected) |
| IR | Incident Response | IR-1 through IR-8 (selected) |
| MA | Maintenance | MA-1 through MA-5 (selected) |
| MP | Media Protection | MP-1 through MP-7 (selected) |
| PE | Physical and Environmental Protection | PE-1 through PE-17 (selected) |
| PL | Planning | PL-1 through PL-4 (selected) |
| PM | Program Management | PM-1 through PM-16 (selected) |
| PS | Personnel Security | PS-1 through PS-8 (selected) |
| PT | PII Processing and Transparency | PT-1 through PT-8 (selected) |
| RA | Risk Assessment | RA-1 through RA-7 (selected) |
| SA | System and Services Acquisition | SA-1 through SA-22 (selected) |
| SC | System and Communications Protection | SC-1 through SC-28 (selected) |
| SI | System and Information Integrity | SI-1 through SI-16 (selected) |
| SR | Supply Chain Risk Management | SR-1 through SR-12 (selected) |

## Key Controls — Moderate Baseline

### AC — Access Control

| ID | Name | Key Requirements |
|----|------|-----------------|
| AC-1 | Policy and Procedures | Develop, document, disseminate, review, and update access control policy and procedures |
| AC-2 | Account Management | Manage information system accounts including creating, enabling, modifying, disabling, removing |
| AC-2(1) | Automated System Account Management | Employ automated mechanisms to support account management functions |
| AC-2(2) | Automated Temporary and Emergency Account Management | Automatically remove or disable temporary and emergency accounts |
| AC-2(3) | Disable Accounts | Disable accounts when no longer required or after a defined period of inactivity |
| AC-2(4) | Automated Audit Actions | Automatically audit account creation, modification, enabling, disabling, removal |
| AC-3 | Access Enforcement | Enforce approved authorizations for logical access to information and system resources |
| AC-4 | Information Flow Enforcement | Enforce approved authorizations for controlling information flows within and between systems |
| AC-5 | Separation of Duties | Define system access authorizations to support separation of duties; separate duties of individuals |
| AC-6 | Least Privilege | Employ the principle of least privilege, allowing only authorized access needed for tasks |
| AC-6(1) | Authorize Access to Security Functions | Explicitly authorize access to security-relevant information and functions |
| AC-6(2) | Non-Privileged Access for Nonsecurity Functions | Require users to use non-privileged accounts for nonsecurity functions |
| AC-6(5) | Privileged Accounts | Restrict privileged accounts to specific personnel or roles |
| AC-6(9) | Log Use of Privileged Functions | Log the execution of privileged functions |
| AC-6(10) | Prohibit Non-Privileged Users from Executing Privileged Functions | Prevent non-privileged users from executing privileged functions |
| AC-7 | Unsuccessful Logon Attempts | Enforce a limit of consecutive invalid logon attempts; automatically lock account or delay |
| AC-8 | System Use Notification | Display system use notification message or banner before granting access |
| AC-11 | Device Lock | Prevent further access after a period of inactivity by initiating a device lock |
| AC-12 | Session Termination | Automatically terminate a user session after defined conditions |
| AC-14 | Permitted Actions Without Identification or Authentication | Identify and document specific user actions that can be performed without I&A |
| AC-17 | Remote Access | Establish and document usage restrictions and implementation guidance for remote access |
| AC-17(1) | Monitoring and Control | Employ automated mechanisms to monitor and control remote access methods |
| AC-17(2) | Protection of Confidentiality and Integrity Using Encryption | Implement cryptographic mechanisms to protect confidentiality and integrity of remote access |
| AC-18 | Wireless Access | Establish configuration and connection requirements for wireless access |
| AC-19 | Access Control for Mobile Devices | Establish configuration requirements and connection requirements for mobile devices |
| AC-20 | Use of External Systems | Establish terms and conditions for authorized use of external systems |
| AC-22 | Publicly Accessible Content | Designate individuals authorized to post information onto publicly accessible systems |

### AT — Awareness and Training

| ID | Name | Key Requirements |
|----|------|-----------------|
| AT-1 | Policy and Procedures | Develop and disseminate awareness and training policy and procedures |
| AT-2 | Literacy Training and Awareness | Provide security and privacy literacy training to system users |
| AT-2(2) | Insider Threat | Include awareness training on recognizing and reporting insider threats |
| AT-3 | Role-Based Training | Provide role-based security and privacy training before access authorization |
| AT-4 | Training Records | Document and monitor individual training activities |

### AU — Audit and Accountability

| ID | Name | Key Requirements |
|----|------|-----------------|
| AU-1 | Policy and Procedures | Develop and disseminate audit and accountability policy |
| AU-2 | Event Logging | Identify events that need to be logged; coordinate event logging with other organizations |
| AU-3 | Content of Audit Records | Ensure audit records contain required information (what, when, where, source, outcome, identity) |
| AU-3(1) | Additional Audit Information | Generate audit records containing additional detailed information |
| AU-4 | Audit Log Storage Capacity | Allocate audit log storage capacity |
| AU-5 | Response to Audit Logging Process Failures | Alert personnel or roles on audit logging failures; take defined additional actions |
| AU-6 | Audit Record Review, Analysis, and Reporting | Review and analyze records for indications of inappropriate or unusual activity |
| AU-6(1) | Automated Process Integration | Integrate audit review, analysis, and reporting with automated mechanisms |
| AU-6(3) | Correlate Audit Record Repositories | Analyze and correlate audit records across different repositories |
| AU-7 | Audit Record Reduction and Report Generation | Provide audit record reduction and report generation supporting on-demand review |
| AU-7(1) | Automatic Processing | Provide ability to process, sort, and search audit records |
| AU-8 | Time Stamps | Use internal system clocks to generate time stamps for audit records |
| AU-9 | Protection of Audit Information | Protect audit information and tools from unauthorized access, modification, deletion |
| AU-9(4) | Access by Subset of Privileged Users | Authorize access to audit functionality to only a subset of privileged users |
| AU-11 | Audit Record Retention | Retain audit records for a defined time period to support after-the-fact investigations |
| AU-12 | Audit Record Generation | Provide audit record generation capability and allow personnel to select events to audit |

### CA — Assessment, Authorization and Monitoring

| ID | Name | Key Requirements |
|----|------|-----------------|
| CA-1 | Policy and Procedures | Develop assessment, authorization, and monitoring policy |
| CA-2 | Control Assessments | Assess security and privacy controls periodically |
| CA-3 | Information Exchange | Approve and manage the exchange of information between systems |
| CA-5 | Plan of Action and Milestones | Develop and update POA&M for findings from assessments and monitoring |
| CA-6 | Authorization | Authorize the system before operation; update the authorization |
| CA-7 | Continuous Monitoring | Develop continuous monitoring strategy; monitor controls on an ongoing basis |
| CA-9 | Internal System Connections | Authorize internal connections to the system |

### CM — Configuration Management

| ID | Name | Key Requirements |
|----|------|-----------------|
| CM-1 | Policy and Procedures | Develop configuration management policy and procedures |
| CM-2 | Baseline Configuration | Develop, document, and maintain a baseline configuration of the system |
| CM-2(2) | Automation Support for Accuracy and Currency | Employ automated mechanisms to maintain an up-to-date baseline configuration |
| CM-3 | Configuration Change Control | Determine types of changes under configuration control; approve, document, and track changes |
| CM-3(2) | Testing, Validation, and Documentation of Changes | Test, validate, and document changes before implementation |
| CM-4 | Impact Analyses | Analyze changes to determine potential security and privacy impacts |
| CM-5 | Access Restrictions for Change | Define, document, approve, and enforce access restrictions for system changes |
| CM-6 | Configuration Settings | Establish and document mandatory configuration settings using security configuration checklists |
| CM-7 | Least Functionality | Configure the system to provide only mission-essential capabilities; prohibit or restrict functions |
| CM-7(1) | Periodic Review | Review the system periodically to identify unnecessary functions, ports, protocols, and services |
| CM-7(2) | Prevent Program Execution | Prevent program execution in accordance with policies regarding software program usage |
| CM-8 | System Component Inventory | Develop and document an inventory of system components |
| CM-8(1) | Updates During Installation and Removal | Update the component inventory when changes occur |
| CM-10 | Software Usage Restrictions | Use software and documentation in accordance with contract agreements and copyright laws |
| CM-11 | User-Installed Software | Establish policies governing the installation of software by users |

### CP — Contingency Planning

| ID | Name | Key Requirements |
|----|------|-----------------|
| CP-1 | Policy and Procedures | Develop contingency planning policy and procedures |
| CP-2 | Contingency Plan | Develop contingency plan coordinating with other plans; distribute to key personnel |
| CP-2(1) | Coordinate with Related Plans | Coordinate contingency plan development with other organizational plans |
| CP-2(3) | Resume Mission and Business Functions | Plan for the resumption of mission and business functions within a defined time period |
| CP-3 | Contingency Training | Provide contingency training to system users |
| CP-4 | Contingency Plan Testing | Test the contingency plan periodically using defined tests |
| CP-4(1) | Coordinate with Related Plans | Coordinate contingency plan testing with related plans |
| CP-6 | Alternate Storage Site | Establish alternate storage site with protections equivalent to the primary site |
| CP-7 | Alternate Processing Site | Establish alternate processing site to permit the transfer of operations |
| CP-8 | Telecommunications Services | Establish alternate telecommunications services |
| CP-9 | System Backup | Conduct backups of user-level and system-level information; protect backup confidentiality and integrity |
| CP-9(1) | Testing for Reliability and Integrity | Test backup information periodically to verify media reliability and information integrity |
| CP-10 | System Recovery and Reconstitution | Provide for the recovery and reconstitution of the system to a known state |

### IA — Identification and Authentication

| ID | Name | Key Requirements |
|----|------|-----------------|
| IA-1 | Policy and Procedures | Develop identification and authentication policy and procedures |
| IA-2 | Identification and Authentication (Organizational Users) | Uniquely identify and authenticate organizational users |
| IA-2(1) | Multi-Factor Authentication to Privileged Accounts | Implement MFA for access to privileged accounts |
| IA-2(2) | Multi-Factor Authentication to Non-Privileged Accounts | Implement MFA for access to non-privileged accounts |
| IA-2(8) | Access to Accounts — Replay Resistant | Implement replay-resistant authentication mechanisms |
| IA-2(12) | Acceptance of PIV Credentials | Accept and verify PIV-compliant credentials |
| IA-3 | Device Identification and Authentication | Uniquely identify and authenticate devices before establishing connection |
| IA-4 | Identifier Management | Manage system identifiers for users, processes, and devices |
| IA-5 | Authenticator Management | Manage system authenticators (verify identity, set initial content, establish administrative procedures) |
| IA-5(1) | Password-Based Authentication | For password-based authentication, enforce minimum complexity and change requirements |
| IA-5(2) | Public Key-Based Authentication | For PKI-based authentication, validate certificates by constructing and verifying certification paths |
| IA-5(6) | Protection of Authenticators | Protect authenticators commensurate with the security category of the information |
| IA-6 | Authentication Feedback | Obscure feedback of authentication information during the authentication process |
| IA-7 | Cryptographic Module Authentication | Employ mechanisms for authentication to a cryptographic module |
| IA-8 | Identification and Authentication (Non-Organizational Users) | Uniquely identify and authenticate non-organizational users |
| IA-8(1) | Acceptance of PIV Credentials from Other Agencies | Accept and verify PIV-compliant credentials from other agencies |
| IA-8(2) | Acceptance of External Authenticators | Accept only external authenticators that are NIST-compliant |
| IA-8(4) | Use of Defined Profiles | Conform to defined profiles for identity management |
| IA-11 | Re-Authentication | Require users to re-authenticate when defined circumstances or situations require |
| IA-12 | Identity Proofing | Identity proof users that require accounts |

### IR — Incident Response

| ID | Name | Key Requirements |
|----|------|-----------------|
| IR-1 | Policy and Procedures | Develop incident response policy and procedures |
| IR-2 | Incident Response Training | Provide incident response training to system users |
| IR-3 | Incident Response Testing | Test the incident response capability periodically |
| IR-4 | Incident Handling | Implement incident handling capability (preparation, detection, analysis, containment, eradication, recovery) |
| IR-4(1) | Automated Incident Handling Processes | Employ automated mechanisms to support the incident handling process |
| IR-5 | Incident Monitoring | Track and document incidents on an ongoing basis |
| IR-6 | Incident Reporting | Require personnel to report suspected incidents within defined time period |
| IR-6(1) | Automated Reporting | Employ automated mechanisms to assist in the reporting of incidents |
| IR-7 | Incident Response Assistance | Provide incident response support resource integral to the incident response capability |
| IR-8 | Incident Response Plan | Develop an incident response plan that provides a roadmap for implementation |

### MA — Maintenance

| ID | Name | Key Requirements |
|----|------|-----------------|
| MA-1 | Policy and Procedures | Develop system maintenance policy and procedures |
| MA-2 | Controlled Maintenance | Schedule, perform, document, and review records of system maintenance and repairs |
| MA-3 | Maintenance Tools | Approve, control, and monitor the use of maintenance tools |
| MA-3(1) | Inspect Tools | Inspect maintenance tools for improper or unauthorized modifications |
| MA-3(2) | Inspect Media | Check media containing diagnostic and test programs for malicious code |
| MA-5 | Maintenance Personnel | Establish a process for the authorization of maintenance personnel |

### MP — Media Protection

| ID | Name | Key Requirements |
|----|------|-----------------|
| MP-1 | Policy and Procedures | Develop media protection policy and procedures |
| MP-2 | Media Access | Restrict access to defined types of digital and non-digital media |
| MP-3 | Media Marking | Mark information system media indicating distribution limitations |
| MP-4 | Media Storage | Physically control and securely store media |
| MP-5 | Media Transport | Protect and control media during transport outside of controlled areas |
| MP-6 | Media Sanitization | Sanitize media prior to disposal, release, or reuse |
| MP-6(1) | Review, Approve, Track, Document, and Verify | Review, approve, track, document, and verify media sanitization actions |
| MP-7 | Media Use | Restrict the use of certain types of media on systems |

### PE — Physical and Environmental Protection

| ID | Name | Key Requirements |
|----|------|-----------------|
| PE-1 | Policy and Procedures | Develop physical and environmental protection policy and procedures |
| PE-2 | Physical Access Authorizations | Develop, approve, and maintain a list of individuals with authorized access to the facility |
| PE-3 | Physical Access Control | Enforce physical access authorizations at facility entry/exit points |
| PE-4 | Access Control for Transmission | Control physical access to information system distribution and transmission lines |
| PE-5 | Access Control for Output Devices | Control physical access to output devices to prevent unauthorized individuals from obtaining output |
| PE-6 | Monitoring Physical Access | Monitor physical access to the facility and review physical access logs |
| PE-6(1) | Intrusion Alarms and Surveillance Equipment | Monitor physical intrusion alarms and surveillance equipment |
| PE-8 | Visitor Access Records | Maintain visitor access records to the facility |
| PE-9 | Power Equipment and Cabling | Protect power equipment and power cabling for the system from damage and destruction |
| PE-10 | Emergency Shutoff | Provide the capability of shutting off power to the system in emergency situations |
| PE-11 | Emergency Power | Provide a short-term UPS to facilitate an orderly shutdown or switchover to long-term alternate power |
| PE-12 | Emergency Lighting | Employ and maintain automatic emergency lighting for the facility |
| PE-13 | Fire Protection | Employ and maintain fire suppression and detection devices and systems |
| PE-14 | Environmental Controls | Maintain temperature and humidity levels within the facility; monitor environmental conditions |
| PE-15 | Water Damage Protection | Protect the system from damage resulting from water leakage |
| PE-16 | Delivery and Removal | Authorize, monitor, and control entry and exit of information system components |
| PE-17 | Alternate Work Site | Employ controls at alternate work sites equivalent to primary site |

### PL — Planning

| ID | Name | Key Requirements |
|----|------|-----------------|
| PL-1 | Policy and Procedures | Develop planning policy and procedures |
| PL-2 | System Security and Privacy Plans | Develop system security and privacy plans that describe security categorization, boundaries, and controls |
| PL-4 | Rules of Behavior | Establish and make available rules that describe user responsibilities and expected behavior |

### PS — Personnel Security

| ID | Name | Key Requirements |
|----|------|-----------------|
| PS-1 | Policy and Procedures | Develop personnel security policy and procedures |
| PS-2 | Position Risk Designation | Assign a risk designation to all organizational positions |
| PS-3 | Personnel Screening | Screen individuals prior to authorizing access to the information system |
| PS-4 | Personnel Termination | Upon termination of individual employment, disable system access within a defined time period |
| PS-5 | Personnel Transfer | Review and confirm ongoing need for current access authorizations when individuals are reassigned or transferred |
| PS-6 | Access Agreements | Require individuals to sign appropriate access agreements prior to being granted access |
| PS-7 | External Personnel Security | Establish personnel security requirements for external providers |
| PS-8 | Personnel Sanctions | Employ a formal sanctions process for individuals failing to comply with security policies |

### RA — Risk Assessment

| ID | Name | Key Requirements |
|----|------|-----------------|
| RA-1 | Policy and Procedures | Develop risk assessment policy and procedures |
| RA-2 | Security Categorization | Categorize system and information processed in accordance with applicable laws |
| RA-3 | Risk Assessment | Conduct risk assessments considering likelihood and impact of unauthorized access, use, disclosure |
| RA-5 | Vulnerability Monitoring and Scanning | Monitor and scan for vulnerabilities and remediate in accordance with risk assessment |
| RA-5(2) | Update Vulnerabilities to Be Scanned | Update the list of information system vulnerabilities scanned |
| RA-5(5) | Privileged Access | Implement privileged access authorization for vulnerability scanning activities |
| RA-7 | Risk Response | Respond to findings from assessments, monitoring, and audits |

### SA — System and Services Acquisition

| ID | Name | Key Requirements |
|----|------|-----------------|
| SA-1 | Policy and Procedures | Develop system and services acquisition policy and procedures |
| SA-2 | Allocation of Resources | Determine, document, and allocate resources required for information security |
| SA-3 | System Development Life Cycle | Manage the system using a system development life cycle that incorporates security |
| SA-4 | Acquisition Process | Include security and privacy functional requirements in the acquisition process |
| SA-4(10) | Use of Approved PIV Products | Employ only approved products on the FIPS 201-approved products list |
| SA-5 | System Documentation | Obtain administrator and user documentation for the information system |
| SA-8 | Security and Privacy Engineering Principles | Apply security and privacy engineering principles in system design |
| SA-9 | External System Services | Require that providers of external system services comply with organizational security requirements |
| SA-9(2) | Identification of Functions, Ports, Protocols, and Services | Require providers to identify functions, ports, protocols, and services required |
| SA-10 | Developer Configuration Management | Require the developer to perform configuration management during development |
| SA-11 | Developer Testing and Evaluation | Require the developer to create and implement a security assessment plan |
| SA-22 | Unsupported System Components | Replace or provide justification for use of unsupported system components |

### SC — System and Communications Protection

| ID | Name | Key Requirements |
|----|------|-----------------|
| SC-1 | Policy and Procedures | Develop system and communications protection policy and procedures |
| SC-2 | Separation of System and User Functionality | Separate user functionality from system management functionality |
| SC-4 | Information in Shared System Resources | Prevent unauthorized and unintended information transfer via shared resources |
| SC-5 | Denial-of-Service Protection | Protect against or limit the effects of denial-of-service attacks |
| SC-7 | Boundary Protection | Monitor and control communications at managed interfaces at external boundaries and key internal boundaries |
| SC-7(3) | Access Points | Limit the number of external network connections to the system |
| SC-7(4) | External Telecommunications Services | Implement a managed interface for each external telecommunication service |
| SC-7(5) | Deny by Default — Allow by Exception | Deny network traffic by default and allow by exception (deny all, permit by exception) |
| SC-7(7) | Split Tunneling for Remote Devices | Prevent split tunneling for remote devices connecting to the system |
| SC-8 | Transmission Confidentiality and Integrity | Protect the confidentiality and integrity of transmitted information |
| SC-8(1) | Cryptographic Protection | Implement cryptographic mechanisms to prevent unauthorized disclosure and detect changes during transmission |
| SC-10 | Network Disconnect | Terminate network connection at end of session or after a defined period of inactivity |
| SC-12 | Cryptographic Key Establishment and Management | Establish and manage cryptographic keys using approved key management technology and processes |
| SC-13 | Cryptographic Protection | Determine the required cryptographic protections, select type of cryptography, implement cryptographic protections |
| SC-15 | Collaborative Computing Devices and Applications | Prohibit remote activation of collaborative computing devices |
| SC-17 | Public Key Infrastructure Certificates | Issue public key certificates under an appropriate certificate policy or obtain from an approved provider |
| SC-18 | Mobile Code | Define acceptable and unacceptable mobile code and mobile code technologies |
| SC-20 | Secure Name/Address Resolution Service (Authoritative Source) | Provide additional data origin authentication and integrity verification artifacts |
| SC-21 | Secure Name/Address Resolution Service (Recursive or Caching Resolver) | Request and perform data origin authentication and data integrity verification |
| SC-22 | Architecture and Provisioning for Name/Address Resolution Service | Ensure systems are fault-tolerant and implement internal/external role separation |
| SC-23 | Session Authenticity | Protect the authenticity of communications sessions |
| SC-28 | Protection of Information at Rest | Protect the confidentiality and integrity of information at rest |
| SC-28(1) | Cryptographic Protection | Implement cryptographic mechanisms to prevent unauthorized disclosure and modification of information at rest |

### SI — System and Information Integrity

| ID | Name | Key Requirements |
|----|------|-----------------|
| SI-1 | Policy and Procedures | Develop system and information integrity policy and procedures |
| SI-2 | Flaw Remediation | Identify, report, and correct information system flaws |
| SI-2(2) | Automated Flaw Remediation Status | Employ automated mechanisms to determine the state of system components regarding flaw remediation |
| SI-3 | Malicious Code Protection | Implement malicious code protection at system entry and exit points |
| SI-4 | System Monitoring | Monitor the system to detect attacks, indicators of potential attacks, and unauthorized connections |
| SI-4(2) | Automated Tools and Mechanisms for Real-Time Analysis | Employ automated tools and mechanisms to support near real-time analysis of events |
| SI-4(4) | Inbound and Outbound Communications Traffic | Monitor inbound and outbound communications traffic for unusual or unauthorized activities |
| SI-4(5) | System-Generated Alerts | Alert personnel or roles when indicators of compromise or potential compromise occur |
| SI-5 | Security Alerts, Advisories, and Directives | Receive system security alerts, advisories, and directives from external organizations |
| SI-7 | Software, Firmware, and Information Integrity | Employ integrity verification tools to detect unauthorized changes |
| SI-8 | Spam Protection | Employ spam protection mechanisms at system entry points |
| SI-10 | Information Input Validation | Check the validity of specified information inputs |
| SI-11 | Error Handling | Generate error messages that provide information necessary for corrective actions without revealing information exploitable by adversaries |
| SI-12 | Information Management and Retention | Manage and retain information within the system and information output per applicable requirements |
| SI-16 | Memory Protection | Implement security controls to protect system memory from unauthorized code execution |

### SR — Supply Chain Risk Management

| ID | Name | Key Requirements |
|----|------|-----------------|
| SR-1 | Policy and Procedures | Develop supply chain risk management policy and procedures |
| SR-2 | Supply Chain Risk Management Plan | Develop a plan for managing supply chain risks |
| SR-3 | Supply Chain Controls and Processes | Establish processes to identify and address weaknesses in the supply chain |
| SR-5 | Acquisition Strategies, Tools, and Methods | Employ acquisition strategies, tools, and methods to protect against supply chain risks |
| SR-6 | Supplier Assessments and Reviews | Assess and review the supply chain-related risks from suppliers or contractors |
| SR-8 | Notification Agreements | Establish agreements with suppliers for notification of supply chain compromises |
| SR-10 | Inspection of Systems or Components | Inspect systems or components at defined intervals for evidence of tampering |
| SR-11 | Component Authenticity | Develop and implement anti-counterfeit policies for components |
| SR-12 | Component Disposal | Dispose of system components using approved disposal methods |

## Quick Reference: Family Abbreviations

| Abbreviation | Full Name |
|-------------|-----------|
| AC | Access Control |
| AT | Awareness and Training |
| AU | Audit and Accountability |
| CA | Assessment, Authorization and Monitoring |
| CM | Configuration Management |
| CP | Contingency Planning |
| IA | Identification and Authentication |
| IR | Incident Response |
| MA | Maintenance |
| MP | Media Protection |
| PE | Physical and Environmental Protection |
| PL | Planning |
| PM | Program Management |
| PS | Personnel Security |
| PT | PII Processing and Transparency |
| RA | Risk Assessment |
| SA | System and Services Acquisition |
| SC | System and Communications Protection |
| SI | System and Information Integrity |
| SR | Supply Chain Risk Management |
