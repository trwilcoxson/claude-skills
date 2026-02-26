# PCI-DSS v4.0 Requirements

## How to Use This Reference

ID format: `[Req].[Sub].[Detail]` (e.g., `8.3.6`). There are 12 principal requirements organized under 6 goals. When citing PCI-DSS requirements, use the exact numeric ID format shown below.

PCI-DSS v4.0 was published March 2022, with mandatory compliance by March 31, 2025. Requirements marked **(FUTURE-DATED)** had an extended compliance deadline of March 31, 2025 for existing implementations.

## Goal 1: Build and Maintain a Secure Network and Systems

### Requirement 1: Install and Maintain Network Security Controls

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 1.1.1 | All security policies and operational procedures identified, kept up to date, in use, and known to all affected parties | Documentation, communication |
| 1.1.2 | Roles and responsibilities for performing activities documented, assigned, and understood | Personnel accountability |
| 1.2.1 | Configuration standards for NSCs are defined, implemented, maintained | Firewall/router configuration standards |
| 1.2.2 | All changes to network connections and NSC configurations are approved and managed | Change management for network |
| 1.2.5 | All services, protocols, and ports allowed are identified, approved, and have a defined business need | Port/protocol management |
| 1.2.6 | Security features defined for all services, protocols, and ports in use that are considered insecure | Compensating controls for insecure protocols |
| 1.2.7 | Configurations of NSCs reviewed at least every six months | Periodic review |
| 1.2.8 | Configuration files for NSCs are secured and synchronized | Config file protection |
| 1.3.1 | Inbound traffic to the CDE is restricted to only that which is necessary | Inbound filtering |
| 1.3.2 | Outbound traffic from the CDE is restricted to only that which is necessary | Outbound filtering |
| 1.3.3 | NSCs installed between all wireless networks and the CDE | Wireless isolation |
| 1.4.1 | NSCs implemented between trusted and untrusted networks | DMZ, perimeter defense |
| 1.4.2 | Inbound traffic from untrusted networks to trusted networks is restricted to communications with system components providing publicly accessible services | Public-facing component isolation |
| 1.4.5 | The disclosure of internal IP addresses and routing information is limited | IP address masking |
| 1.5.1 | Security controls implemented on any computing devices that connect to both untrusted networks and the CDE | Personal firewall or equivalent |

### Requirement 2: Apply Secure Configurations to All System Components

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 2.1.1 | All security policies and operational procedures identified, kept up to date, in use | Documentation |
| 2.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 2.2.1 | Configuration standards developed for all system components, consistent with industry-accepted hardening standards | CIS, STIG, vendor guidance |
| 2.2.2 | Vendor default accounts managed | Default credentials removed or disabled |
| 2.2.3 | Primary functions requiring different security levels managed on separate system components | Function separation |
| 2.2.4 | Only necessary services, protocols, daemons, and functions enabled | Minimize attack surface |
| 2.2.5 | If any insecure services, protocols, or daemons are present, business justification documented | Risk acceptance |
| 2.2.6 | System security parameters configured to prevent misuse | Security hardening |
| 2.2.7 | All non-console administrative access encrypted using strong cryptography | Encrypted admin access |
| 2.3.1 | Wireless environments managed, all defaults changed at installation | Wireless security |
| 2.3.2 | Wireless vendor defaults changed, including encryption keys, passwords, SNMP community strings | Wireless hardening |

## Goal 2: Protect Account Data

### Requirement 3: Protect Stored Account Data

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 3.1.1 | All processes and mechanisms for protecting stored account data are defined and understood | Documentation |
| 3.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 3.2.1 | Account data storage is kept to a minimum through data retention and disposal policies | Data minimization |
| 3.3.1 | SAD is not retained after authorization, even if encrypted | Post-auth SAD deletion |
| 3.3.1.1 | Full track data not retained after authorization | Track data deletion |
| 3.3.1.2 | Card verification code not retained after authorization | CVV/CVC deletion |
| 3.3.1.3 | Personal identification number (PIN) and PIN block not retained after authorization | PIN deletion |
| 3.3.2 | SAD stored before completion of authorization is encrypted with strong cryptography | Pre-auth SAD encryption |
| 3.3.3 | If SAD is stored for issuers, it is protected with strong cryptography | Issuer SAD protection |
| 3.4.1 | PAN is masked when displayed (first 6 and last 4 digits maximum) | PAN masking |
| 3.4.2 | When using remote-access technologies, PAN copy/relocate prevention implemented | Remote access PAN controls |
| 3.5.1 | PAN is rendered unreadable anywhere it is stored by using strong cryptography | PAN encryption at rest |
| 3.5.1.1 | Hashes used to render PAN unreadable are keyed cryptographic hashes | Keyed hashing for PAN |
| 3.5.1.2 | If disk-level or partition-level encryption used, only to render PAN unreadable on removable media | Disk encryption limitation |
| 3.6.1 | Procedures defined and implemented to protect cryptographic keys | Key management procedures |
| 3.6.1.1 | Additional requirement for service providers: documented cryptographic architecture | Crypto architecture documentation |
| 3.7.1 | Key-management policies and procedures are implemented | Key lifecycle management |
| 3.7.2 | Cryptographic keys restricted to fewest custodians necessary | Key custodian minimization |
| 3.7.3 | Cryptographic keys stored in fewest possible locations and forms | Key storage minimization |

### Requirement 4: Protect Cardholder Data with Strong Cryptography During Transmission Over Open, Public Networks

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 4.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 4.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 4.2.1 | Strong cryptography and security protocols implemented to safeguard PAN during transmission over open, public networks | TLS 1.2+, strong ciphers |
| 4.2.1.1 | Inventory of trusted keys and certificates maintained | Certificate inventory |
| 4.2.1.2 | Wireless networks transmitting PAN or connected to the CDE use industry best practices for authentication and transmission | Wireless encryption |
| 4.2.2 | PAN is secured with strong cryptography whenever sent via end-user messaging technologies | Messaging encryption |

## Goal 3: Maintain a Vulnerability Management Program

### Requirement 5: Protect All Systems and Networks from Malicious Software

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 5.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 5.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 5.2.1 | Anti-malware solution deployed on all system components except those determined to not be at risk | Anti-malware deployment |
| 5.2.2 | Anti-malware solution detects all known types of malware and removes, blocks, or contains | Detection capability |
| 5.2.3 | System components not at risk from malware are evaluated periodically to confirm no malware risk | Periodic re-evaluation |
| 5.3.1 | Anti-malware solution kept current via automatic updates | Signature updates |
| 5.3.2 | Anti-malware solution performs periodic scans and active/real-time scans | Scanning schedule |
| 5.3.3 | Anti-malware mechanisms and processes are active and cannot be disabled by users unless specifically documented | Anti-tamper |
| 5.3.4 | Audit logs for anti-malware are enabled and retained | Anti-malware logging |
| 5.4.1 | Mechanisms in place to detect and protect personnel against phishing attacks | Anti-phishing controls |

### Requirement 6: Develop and Maintain Secure Systems and Software

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 6.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 6.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 6.2.1 | Bespoke and custom software developed securely | Secure SDLC |
| 6.2.2 | Software development personnel trained in secure coding at least once every 12 months | Developer training |
| 6.2.3 | Bespoke and custom software reviewed prior to release to identify and correct potential coding vulnerabilities | Code review |
| 6.2.3.1 | If manual code review is performed, code is reviewed by separate individuals with code-review and secure-coding expertise | Independent code review |
| 6.2.4 | Software engineering techniques or methods prevent or mitigate common software attacks | OWASP prevention |
| 6.3.1 | Security vulnerabilities identified and managed through a vulnerability management process | Vulnerability tracking |
| 6.3.2 | An inventory of bespoke and custom software and third-party software components is maintained | Software inventory |
| 6.3.3 | Critical and high security patches/updates installed within one month of release | Patch timeline |
| 6.4.1 | For public-facing web applications, address new threats and vulnerabilities on an ongoing basis | WAF, vulnerability assessment |
| 6.4.2 | For public-facing web applications, an automated technical solution deployed that detects and prevents web-based attacks | WAF deployment |
| 6.4.3 | All payment page scripts managed, authorized, and integrity assured | Script inventory and integrity |
| 6.5.1 | Changes to all system components in the production environment are managed via change control processes | Change management |
| 6.5.2 | Upon completion of a significant change, all applicable PCI-DSS requirements confirmed to be in place | Post-change validation |
| 6.5.3 | Pre-production environments separated from production and separation enforced with access controls | Environment separation |
| 6.5.4 | Roles and functions separated between production and pre-production environments | Duty separation |
| 6.5.5 | Live PANs not used in pre-production environments unless controls equivalent to production | Test data management |
| 6.5.6 | Test data and test accounts removed before production system becomes active | Test data cleanup |

## Goal 4: Implement Strong Access Control Measures

### Requirement 7: Restrict Access to System Components and Cardholder Data by Business Need to Know

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 7.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 7.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 7.2.1 | An access control model defined that grants access based on business need to know | Need-to-know access model |
| 7.2.2 | Access assigned to users, including privileged users, based on job classification and function | Role-based access |
| 7.2.3 | Required privileges approved by authorized personnel | Privilege approval |
| 7.2.4 | All user accounts and related access privileges reviewed at least every six months | Access reviews |
| 7.2.5 | All application and system accounts and related access privileges assigned and managed appropriately | Service account management |
| 7.2.5.1 | All access by application and system accounts reviewed periodically | Service account reviews |
| 7.2.6 | All user access to query repositories of stored cardholder data restricted | CHD query access |
| 7.3.1 | An access control system in place that restricts access based on user need to know and is set to deny all by default | Access enforcement |
| 7.3.2 | The access control system configured to enforce permissions assigned per access control model | Consistent enforcement |
| 7.3.3 | The access control system set to deny all by default | Default deny |

### Requirement 8: Identify Users and Authenticate Access to System Components

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 8.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 8.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 8.2.1 | All users assigned a unique ID before access to system components or cardholder data | Unique user IDs |
| 8.2.2 | Group, shared, or generic accounts only used when necessary and managed per defined conditions | Shared account controls |
| 8.2.3 | Additional requirement for service providers: service providers with remote access use unique authentication factors for each customer | Per-customer auth |
| 8.2.4 | Addition, deletion, and modification of user IDs, authentication factors, and other identifier objects managed | Identity lifecycle |
| 8.2.5 | Access for terminated users immediately revoked | Timely deprovisioning |
| 8.2.6 | Inactive user accounts removed or disabled within 90 days | Inactive account cleanup |
| 8.2.7 | Accounts used by third parties managed per defined conditions | Third-party account management |
| 8.2.8 | If a user session has been idle for more than 15 minutes, re-authentication required | Session timeout |
| 8.3.1 | All user access to system components authenticated via at least one authentication factor | Authentication required |
| 8.3.2 | Strong cryptography used to render all authentication factors unreadable during transmission and storage | Credential protection |
| 8.3.4 | Invalid authentication attempts limited — account locked after no more than 10 attempts | Account lockout |
| 8.3.5 | If passwords/passphrases are used, set and reset to unique values per user, changed if compromised | Password management |
| 8.3.6 | If passwords/passphrases are used, minimum length of 12 characters (or 8 if system cannot support 12) | Password complexity |
| 8.3.7 | Individuals not allowed to submit new password/passphrase that is same as any of last four used | Password history |
| 8.3.9 | If passwords/passphrases are the only authentication factor, passwords changed at least once every 90 days | Password rotation |
| 8.3.10 | Additional requirement for service providers: if passwords are the only factor, guidance provided to customer users on password requirements | Customer password guidance |
| 8.3.10.1 | Additional requirement for service providers: if passwords are the only factor for customer user access, passwords must comply with complexity requirements | Customer password enforcement |
| 8.4.1 | MFA implemented for all non-console access into the CDE for personnel with administrative access | Admin MFA |
| 8.4.2 | MFA implemented for all access into the CDE | CDE access MFA |
| 8.4.3 | MFA implemented for all remote network access originating from outside the entity's network | Remote access MFA |
| 8.5.1 | MFA systems implemented to prevent misuse including replay attacks | MFA security |
| 8.6.1 | If accounts used by systems or applications can be used for interactive login, managed on an exception basis | System account controls |
| 8.6.2 | Passwords/passphrases for system or application accounts that can be used interactively not hard coded | No hardcoded credentials |
| 8.6.3 | Passwords/passphrases for system and application accounts protected against misuse | System credential protection |

### Requirement 9: Restrict Physical Access to Cardholder Data

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 9.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 9.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 9.2.1 | Appropriate facility entry controls in place to restrict physical access to systems in the CDE | Physical access controls |
| 9.2.2 | Physical and/or logical controls to restrict use of publicly accessible network jacks | Network jack controls |
| 9.2.3 | Physical access to wireless access points, gateways, and networking/communications hardware restricted | Wireless hardware security |
| 9.2.4 | Access to consoles in sensitive areas restricted via locking when not in use | Console security |
| 9.3.1 | Physical access to sensitive areas controlled for authorized on-site personnel | On-site access control |
| 9.4.1 | All media with cardholder data physically secured | Media security |
| 9.4.2 | All media with cardholder data classified in accordance with sensitivity | Media classification |
| 9.4.3 | Media with cardholder data sent outside the facility secured via tracked, approved courier or other delivery method | Media transport |
| 9.4.5 | Inventory logs of all electronic media with cardholder data maintained | Media inventory |
| 9.4.6 | Hard-copy materials with cardholder data destroyed when no longer needed | Hard-copy destruction |
| 9.4.7 | Electronic media with cardholder data rendered unrecoverable when no longer needed | Electronic media destruction |
| 9.5.1 | POI devices protected from tampering and unauthorized substitution | POI device security |

## Goal 5: Regularly Monitor and Test Networks

### Requirement 10: Log and Monitor All Access to System Components and Cardholder Data

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 10.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 10.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 10.2.1 | Audit logs enabled and active for all system components and cardholder data | Logging enabled |
| 10.2.1.1 | Audit logs capture all individual user access to cardholder data | CHD access logging |
| 10.2.1.2 | Audit logs capture all actions taken by any individual with administrative access | Admin action logging |
| 10.2.1.3 | Audit logs capture all access to audit logs | Log access logging |
| 10.2.1.4 | Audit logs capture all invalid logical access attempts | Failed logon logging |
| 10.2.1.5 | Audit logs capture all changes to identification and authentication credentials | Credential change logging |
| 10.2.1.6 | Audit logs capture initialization of new audit logs, and starting, stopping, or pausing of existing audit logs | Log lifecycle logging |
| 10.2.1.7 | Audit logs capture all creation and deletion of system-level objects | System object logging |
| 10.2.2 | Audit logs record sufficient information for each auditable event | Log detail requirements |
| 10.3.1 | Read access to audit logs files limited to those with a job-related need | Log access restriction |
| 10.3.2 | Audit log files protected to prevent modifications by individuals | Log integrity |
| 10.3.3 | Audit log files, including those for external-facing technologies, promptly backed up to a secure, centralized internal log server or media | Log backup |
| 10.3.4 | File integrity monitoring or change-detection mechanisms used on audit logs | Log tampering detection |
| 10.4.1 | Audit logs reviewed at least once daily to identify anomalies or suspicious activity | Daily log review |
| 10.4.1.1 | Automated mechanisms used to perform audit log reviews | Automated log analysis |
| 10.4.2 | Logs of all other system components reviewed periodically | Periodic log review |
| 10.4.3 | Exceptions and anomalies identified during the review process are addressed | Exception handling |
| 10.5.1 | Retain audit log history for at least 12 months, with at least the most recent 3 months immediately available for analysis | Log retention |
| 10.6.1 | System clocks and time synchronized using time-synchronization technology | Time synchronization |
| 10.6.2 | Time synchronization technology set to receive time from industry-accepted external sources | NTP configuration |
| 10.6.3 | Time-synchronization settings and data are protected | Time integrity |
| 10.7.1 | Additional requirement for service providers: failures of critical security control systems detected, alerted, and addressed promptly | Control failure detection |

### Requirement 11: Test Security of Systems and Networks Regularly

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 11.1.1 | All security policies and operational procedures identified and in use | Documentation |
| 11.1.2 | Roles and responsibilities documented, assigned, and understood | Personnel |
| 11.2.1 | Authorized and unauthorized wireless access points managed | Wireless AP detection |
| 11.2.2 | An inventory of authorized wireless access points maintained | Wireless AP inventory |
| 11.3.1 | Internal vulnerability scans performed at least once every three months | Internal vulnerability scanning |
| 11.3.1.1 | All other applicable vulnerabilities (not ranked as high-risk or critical) are managed | Non-critical vulnerability management |
| 11.3.1.2 | Internal vulnerability scans performed via authenticated scanning | Authenticated scanning |
| 11.3.1.3 | Internal vulnerability scans performed after any significant change | Post-change scanning |
| 11.3.2 | External vulnerability scans performed at least once every three months by a PCI SSC Approved Scanning Vendor (ASV) | External ASV scanning |
| 11.3.2.1 | External vulnerability scans performed after any significant change | Post-change external scanning |
| 11.4.1 | External penetration testing performed at least once every 12 months and after any significant infrastructure or application upgrade | External pen testing |
| 11.4.2 | Internal penetration testing performed at least once every 12 months and after any significant infrastructure or application upgrade | Internal pen testing |
| 11.4.3 | Exploitable vulnerabilities found during penetration testing are corrected and testing repeated | Pen test remediation |
| 11.4.4 | If segmentation is used to isolate the CDE, penetration tests performed to verify segmentation controls | Segmentation testing |
| 11.4.5 | Additional requirement for service providers: if segmentation is used, penetration tests on segmentation controls performed at least once every six months | Service provider segmentation testing |
| 11.5.1 | Intrusion-detection and/or intrusion-prevention techniques used to detect and/or prevent intrusions | IDS/IPS |
| 11.5.1.1 | Intrusion-detection and/or intrusion-prevention techniques detect, alert on/prevent, and address covert malware communication channels | Covert channel detection |
| 11.5.2 | A change-detection mechanism deployed to alert personnel to unauthorized modification of critical files | File integrity monitoring |
| 11.6.1 | A change- and tamper-detection mechanism deployed on payment pages to alert personnel to unauthorized modification | Payment page integrity |

## Goal 6: Maintain an Information Security Policy

### Requirement 12: Support Information Security with Organizational Policies and Programs

| ID | Requirement | Key Details |
|----|-------------|-------------|
| 12.1.1 | An overall information security policy is established, published, maintained, and disseminated | Security policy |
| 12.1.2 | Information security policy reviewed at least once every 12 months and updated as needed | Annual policy review |
| 12.1.3 | Security policy clearly defines information security roles and responsibilities for all personnel | Role definitions |
| 12.1.4 | Responsibility for information security formally assigned to a Chief Information Security Officer or equivalent | CISO assignment |
| 12.2.1 | Acceptable use policies for end-user technologies defined and implemented | AUP |
| 12.3.1 | Each PCI-DSS requirement that provides flexibility is supported by a targeted risk analysis | Risk-based approach |
| 12.3.2 | A targeted risk analysis is performed for each PCI-DSS requirement met with the customized approach | Customized approach risk analysis |
| 12.3.3 | Cryptographic cipher suites and protocols in use documented and reviewed at least once every 12 months | Crypto review |
| 12.3.4 | Hardware and software technologies in use reviewed at least once every 12 months | Technology review |
| 12.4.1 | Additional requirement for service providers: executive management establishes responsibility for PCI-DSS compliance | Executive accountability |
| 12.5.1 | An inventory of system components in scope for PCI-DSS maintained, including description of function/use | Scope inventory |
| 12.5.2 | PCI-DSS scope documented and confirmed at least once every 12 months and upon significant change | Annual scope validation |
| 12.6.1 | A formal security awareness program implemented | Security awareness |
| 12.6.2 | Security awareness program reviewed at least once every 12 months and updated as needed | Awareness program review |
| 12.6.3 | Personnel receive security awareness training upon hire and at least once every 12 months | Annual security training |
| 12.6.3.1 | Security awareness training includes awareness of threats and vulnerabilities that could impact the security of the CDE | CDE-specific training |
| 12.6.3.2 | Security awareness training includes awareness of acceptable use of end-user technologies | Technology use training |
| 12.8.1 | A list of all third-party service providers with which account data is shared or that could affect security maintained | TPP inventory |
| 12.8.2 | Written agreements maintained with all TPPs confirming they are responsible for the security of account data | TPP agreements |
| 12.8.3 | An established process for engaging TPPs including proper due diligence prior to engagement | TPP due diligence |
| 12.8.4 | A program to monitor TPPs' PCI-DSS compliance status at least once every 12 months | TPP monitoring |
| 12.8.5 | Information maintained about which PCI-DSS requirements are managed by each TPP and which by the entity | Responsibility matrix |
| 12.9.1 | Additional requirement for TPPs: TPPs acknowledge in writing to customers responsibility for protecting account data | TPP acknowledgment |
| 12.10.1 | An incident response plan exists and is ready to be activated in the event of a suspected or confirmed security incident | IR plan |
| 12.10.2 | The incident response plan is reviewed, tested, and updated at least once every 12 months | IR plan testing |
| 12.10.3 | Specific personnel designated to be available on a 24/7 basis to respond to suspected or confirmed security incidents | 24/7 IR team |
| 12.10.4 | Personnel responsible for responding to suspected and confirmed security incidents are appropriately and periodically trained | IR training |
| 12.10.4.1 | Frequency of periodic training for incident response personnel is defined | IR training frequency |
| 12.10.5 | The security incident response plan includes monitoring and responding to alerts from security monitoring systems | Alert response |
| 12.10.6 | The security incident response plan is modified and evolved according to lessons learned and industry developments | IR plan evolution |
| 12.10.7 | Incident response procedures are in place to be initiated upon detection of stored PAN anywhere it is not expected | Unexpected PAN detection |

## Quick Reference: Requirement Structure

| Goal | Requirements | Focus |
|------|-------------|-------|
| Build and Maintain Secure Network | Req 1, Req 2 | Network security controls, secure configurations |
| Protect Account Data | Req 3, Req 4 | Stored data protection, transit encryption |
| Vulnerability Management | Req 5, Req 6 | Anti-malware, secure development |
| Strong Access Control | Req 7, Req 8, Req 9 | Need-to-know, authentication, physical access |
| Monitor and Test | Req 10, Req 11 | Logging, vulnerability scanning, pen testing |
| Security Policy | Req 12 | Policies, awareness, IR, vendor management |
