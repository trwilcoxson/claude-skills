# Threat Modeling Frameworks Reference

## Threat Actor Profiles

Reference profiles for common threat actors. Phase 1 selects relevant actors based on system characteristics.

| Actor Type | Motivation | Typical Access | Common Techniques |
|------------|-----------|----------------|-------------------|
| **Nation-State / APT** | Espionage, disruption, strategic advantage | Any — can achieve all access levels | Zero-days, supply chain compromise, long-term persistent access, custom malware, social engineering at scale |
| **Organized Crime** | Financial gain | External; may purchase insider access | Ransomware, credential stuffing, BEC, payment fraud, exploit kits |
| **Hacktivist** | Ideology, publicity, disruption | External | DDoS, defacement, data leaks for embarrassment, social engineering |
| **Malicious Insider** | Revenge, financial gain, ideology | Privileged internal | Data exfiltration, sabotage, privilege abuse, unauthorized access |
| **Negligent Insider** | Unintentional | Legitimate internal | Misconfiguration, phishing victim, credential sharing, shadow IT, accidental data exposure |
| **Opportunistic / Script Kiddie** | Curiosity, notoriety, low-effort gain | External unauthenticated | Automated scanners, known exploits, default credentials, exposed services |
| **Competitor** | Commercial advantage, espionage | External; may use social engineering | Scraping, reverse engineering, trade secret theft, employee poaching |
| **Supply Chain Attacker** | Varies (often nation-state or organized crime proxy) | Indirect — through trusted dependencies | Compromised packages, malicious updates, build pipeline injection, typosquatting |

Assign capability 1-5 based on system context.

### Actor Selection Criteria

Select actors based on the system's data sensitivity, exposure model, and industry. Include both external and internal threat categories.

---

## STRIDE-LM

STRIDE-LM extends the classic STRIDE model with Lateral Movement. Assess each category against every component and data flow.

### Spoofing (Identity)
Can an attacker impersonate a legitimate entity — user, service, or data source?

### Tampering (Integrity)
Can data be modified without detection — in transit, at rest, in processing, or in configuration?

### Repudiation (Accountability)
Can actions be performed without attribution or forensic traceability?

### Information Disclosure (Confidentiality)
Can sensitive data leak to unauthorized parties via errors, logs, side channels, storage, transit, or access control gaps?

### Denial of Service (Availability)
Can availability be disrupted through resource exhaustion, dependency failures, state corruption, or amplification?

### Elevation of Privilege (Authorization)
Can an attacker gain unauthorized access levels through vertical/horizontal escalation, injection, or misconfiguration?

### LM — Lateral Movement
Can an attacker pivot from this component to other parts of the system through network access, credential reuse, trust exploitation, or container/host escape?

---

## AI/ML Security Threats (Supplementary)

Assess these when the system includes AI/ML components, **in addition to** STRIDE-LM.

### A. LLM Application Threats
- Prompt injection (direct)
- Prompt injection (indirect)
- Data poisoning / training data integrity
- Model extraction / model inversion
- Adversarial inputs / safety filter bypass
- Information leakage (training data, system prompts, context)

### B. Agentic AI Threats
- Tool-call injection
- Agent-to-agent trust chain compromise
- Delegation escalation
- Autonomous action with insufficient human-in-the-loop
- Agent memory/state poisoning
- Excessive agency (over-permissioned tools)
- Confused deputy via tool results

### C. RAG-Specific Threats
- Retrieval poisoning
- Embedding space manipulation
- Context window stuffing
- Knowledge base data exfiltration
- Stale/inconsistent retrieval

### D. Multi-Modal Threats
- Image-based prompt injection
- Audio-based injection
- Cross-modal confusion

---

## OWASP Risk Rating Methodology

The prioritization formula used after STRIDE-LM identification and PASTA attack simulation:

**Risk = Likelihood x Impact**

Both Likelihood and Impact are scored 1-5. The product determines the severity band.

### Likelihood Scoring (1-5)

Likelihood is derived from PASTA attack simulation (Stages 4-5).

| Score | Level | Description |
|-------|-------|-------------|
| **1** | Very Low | Requires nation-state resources, zero-days, physical access, or an implausible chain of preconditions |
| **2** | Low | Requires significant expertise, dedicated effort, and insider knowledge; not automatable |
| **3** | Medium | Achievable with moderate skill and publicly available tools; some preconditions needed |
| **4** | High | Straightforward with common tools and basic technical knowledge; few preconditions |
| **5** | Very High | Trivially exploitable, automatable, no special skills or access needed |

### Impact Scoring (1-5)

Impact is derived from PASTA business impact analysis (Stages 6-7). Assess across four dimensions and take the **highest** as the overall impact score:

| Dimension | Low (1-2) | Medium (3) | High (4-5) |
|-----------|-----------|------------|------------|
| **Financial** | Minimal direct cost | Significant but contained loss | Major loss or existential threat |
| **Operational** | No or brief disruption | Partial outage, hours to recover | Major or complete outage, days+ to recover |
| **Reputational** | Internal awareness only | Limited public awareness | Major press coverage or sustained crisis |
| **Regulatory** | No implications or minor gap | Formal finding, corrective action | Investigation, significant fines, or license risk |

Adjust thresholds to the organization's scale.

### Risk Score Matrix

Multiply Likelihood x Impact. Map the product to severity bands:

```
                    IMPACT
              1     2     3     4     5
         +-----------------------------+
    1    |  1     2     3     4     5  |
L   2    |  2     4     6     8    10  |
i   3    |  3     6     9    12    15  |
k   4    |  4     8    12    16    20  |
e   5    |  5    10    15    20    25  |
         +-----------------------------+
```

| Risk Score | Severity | Action |
|-----------|----------|--------|
| 1-4       | LOW      | Accept or address opportunistically |
| 5-9       | MEDIUM   | Schedule remediation in backlog |
| 10-16     | HIGH     | Plan remediation within current cycle |
| 17-25     | CRITICAL | Immediate remediation required |

---

## LINDDUN Privacy Threats

Assess each category for data flows and stores handling personal data.

| Category | Definition | Key Questions |
|----------|-----------|---------------|
| **L**inkability | Can an attacker link two or more items of interest (records, actions, identities)? | Are user actions correlatable across services? Can pseudonymized data be re-identified? |
| **I**dentifiability | Can an attacker identify a data subject from the data? | Is PII minimized? Are identifiers necessary? Can aggregated data identify individuals? |
| **N**on-repudiation | Is the data subject unable to deny involvement? | Are audit trails exposing user behavior unnecessarily? Can users plausibly deny actions? |
| **D**etectability | Can an attacker determine whether a data item about a subject exists? | Do query patterns reveal membership? Can metadata analysis reveal data existence? |
| **D**isclosure | Can an attacker learn the content of a data item? | Is personal data encrypted? Are access controls sufficient? Are there data leak vectors? |
| **U**nawareness | Is the data subject unaware of data collection or processing? | Are privacy notices adequate? Is consent granular? Is data processing transparent? |
| **N**on-compliance | Does the system fail to comply with privacy regulations? | GDPR data subject rights (access, deletion, portability)? CCPA opt-out? HIPAA minimum necessary? Data retention policies? |

---

## MITRE ATT&CK — Key Tactics and Techniques

Reference the most architecturally relevant techniques per tactic.

| Tactic | ID | Relevant Techniques |
|--------|----|-------------------|
| Reconnaissance | TA0043 | T1595 Active Scanning, T1592 Gather Victim Host Info, T1589 Gather Victim Identity Info |
| Resource Development | TA0042 | T1583 Acquire Infrastructure, T1588 Obtain Capabilities |
| Initial Access | TA0001 | T1190 Exploit Public-Facing App, T1078 Valid Accounts, T1195 Supply Chain Compromise |
| Execution | TA0002 | T1059 Command & Scripting, T1203 Exploitation for Client Execution |
| Persistence | TA0003 | T1098 Account Manipulation, T1053 Scheduled Task/Job, T1078 Valid Accounts |
| Privilege Escalation | TA0004 | T1068 Exploitation for Privilege Escalation, T1078 Valid Accounts |
| Defense Evasion | TA0005 | T1070 Indicator Removal, T1562 Impair Defenses, T1036 Masquerading |
| Credential Access | TA0006 | T1110 Brute Force, T1539 Steal Web Session Cookie, T1552 Unsecured Credentials |
| Discovery | TA0007 | T1046 Network Service Scanning, T1087 Account Discovery |
| Lateral Movement | TA0008 | T1021 Remote Services, T1550 Use Alternate Auth Material |
| Collection | TA0009 | T1530 Data from Cloud Storage, T1213 Data from Information Repositories |
| Exfiltration | TA0010 | T1048 Exfiltration Over Alternative Protocol, T1567 Exfiltration Over Web Service |
| Command and Control | TA0011 | T1071 Application Layer Protocol, T1572 Protocol Tunneling |
| Impact | TA0040 | T1485 Data Destruction, T1486 Data Encrypted for Impact, T1498 Network DoS |

---

## OWASP Top 10 (2021)

| ID | Category |
|----|----------|
| A01:2021 | Broken Access Control |
| A02:2021 | Cryptographic Failures |
| A03:2021 | Injection |
| A04:2021 | Insecure Design |
| A05:2021 | Security Misconfiguration |
| A06:2021 | Vulnerable and Outdated Components |
| A07:2021 | Identification and Authentication Failures |
| A08:2021 | Software and Data Integrity Failures |
| A09:2021 | Security Logging and Monitoring Failures |
| A10:2021 | Server-Side Request Forgery (SSRF) |

## OWASP API Security Top 10 (2023)

| ID | Category |
|----|----------|
| API1:2023 | Broken Object Level Authorization |
| API2:2023 | Broken Authentication |
| API3:2023 | Broken Object Property Level Authorization |
| API4:2023 | Unrestricted Resource Consumption |
| API5:2023 | Broken Function Level Authorization |
| API6:2023 | Unrestricted Access to Sensitive Business Flows |
| API7:2023 | Server Side Request Forgery |
| API8:2023 | Security Misconfiguration |
| API9:2023 | Improper Inventory Management |
| API10:2023 | Unsafe Consumption of APIs |

---

## Cloud-Native Threat Patterns

Assess when the system runs in cloud infrastructure.

### IAM & Identity
- Overly permissive IAM roles/policies
- Long-lived access keys
- Cross-account role trust misconfiguration
- Service account key sprawl
- Federated identity trust boundary issues

### Cloud Metadata & Instance Services
- IMDS v1 SSRF to credential theft
- IMDS v2 bypass techniques
- Cloud-init and user-data secrets exposure
- Instance profile over-permission

### Cross-Tenant Isolation
- Shared resource exploitation
- Noisy neighbor DoS
- Tenant ID manipulation / horizontal traversal
- Data isolation failures in shared storage

### Serverless-Specific
- Event injection
- Cold start security gaps
- Ephemeral storage data leakage
- Function chaining privilege escalation
- Overly permissive execution roles

### Object Storage
- Public bucket/blob exposure
- Pre-signed URL abuse
- Bucket policy misconfiguration
- Server-side encryption key management gaps

### Container & Orchestration
- Container escape
- Kubernetes RBAC over-permission
- etcd access / secrets exposure
- Pod-to-pod network policy gaps
- Container image supply chain

---

## Zero Trust Assessment Criteria

Evaluate whether the architecture follows zero trust principles or relies on perimeter security assumptions.

| Principle | Assessment Questions |
|-----------|---------------------|
| **Verify explicitly** | Does every service-to-service call authenticate the caller? Are requests authorized based on identity, not network position? Is authentication performed at every layer, not just the edge? |
| **Least privilege access** | Are permissions scoped to specific resources and actions? Are they time-bound where possible? Are service accounts per-workload with minimal scope? |
| **Assume breach** | Is east-west traffic encrypted and monitored? Can a compromised component be isolated? Is blast radius limited by segmentation? Are secrets rotatable without downtime? |
| **Micro-segmentation** | Are network policies enforced at the workload level (not just subnet)? Can components only reach the specific services they need? Are database connections restricted to authorized services? |
| **Continuous verification** | Are sessions re-validated? Do tokens have reasonable expiry? Is behavior-based anomaly detection in place? Are device/context signals evaluated on each request? |

---

## API Security Depth

Protocol-specific architectural threats beyond the OWASP API Top 10.

### GraphQL
- Introspection in production
- Batching attacks
- Deep nesting / circular query DoS
- Field-level authorization gaps
- Alias-based rate limit bypass

### WebSocket
- Cross-Site WebSocket Hijacking (CSWSH)
- No per-message authentication
- Message injection in shared channels
- Connection state manipulation
- Missing rate limiting on message frequency

### gRPC
- Reflection service in production
- Metadata header injection
- Large message DoS
- Missing per-method authorization
- Protobuf deserialization issues

### API Gateway Bypass
- Direct backend access
- Gateway-backend protocol mismatch
- Header smuggling through gateway
- Rate limit bypass via multiple gateway endpoints

---

## CWE Groups by Architectural Concern

### Authentication
- CWE-287: Improper Authentication
- CWE-306: Missing Authentication for Critical Function
- CWE-798: Use of Hard-coded Credentials
- CWE-521: Weak Password Requirements
- CWE-620: Unverified Password Change

### Authorization
- CWE-862: Missing Authorization
- CWE-863: Incorrect Authorization
- CWE-639: Authorization Bypass Through User-Controlled Key (IDOR)
- CWE-269: Improper Privilege Management
- CWE-732: Incorrect Permission Assignment

### Input Validation
- CWE-20: Improper Input Validation
- CWE-89: SQL Injection
- CWE-79: Cross-site Scripting (XSS)
- CWE-78: OS Command Injection
- CWE-918: Server-Side Request Forgery (SSRF)
- CWE-611: Improper Restriction of XML External Entity Reference

### Cryptography
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm
- CWE-328: Use of Weak Hash
- CWE-330: Use of Insufficiently Random Values
- CWE-311: Missing Encryption of Sensitive Data
- CWE-326: Inadequate Encryption Strength

### Data Protection
- CWE-200: Exposure of Sensitive Information
- CWE-532: Insertion of Sensitive Information into Log File
- CWE-312: Cleartext Storage of Sensitive Information
- CWE-359: Exposure of Private Personal Information
- CWE-209: Generation of Error Message Containing Sensitive Information

### Error Handling
- CWE-755: Improper Handling of Exceptional Conditions
- CWE-754: Improper Check for Unusual or Exceptional Conditions
- CWE-390: Detection of Error Condition Without Action
- CWE-397: Declaration of Throws for Generic Exception

### Resource Management
- CWE-400: Uncontrolled Resource Consumption
- CWE-770: Allocation of Resources Without Limits
- CWE-772: Missing Release of Resource after Effective Lifetime
- CWE-362: Concurrent Execution Using Shared Resource with Improper Synchronization (Race Condition)

---

## CIA Impact Matrix

Rate each pillar as HIGH (H), MEDIUM (M), or LOW (L).

| Rating | Confidentiality | Integrity | Availability |
|--------|----------------|-----------|--------------|
| **HIGH** | Restricted/regulated data exposed (PII, PHI, financial, credentials). Regulatory breach. Mass data exfiltration. | Critical data corrupted with no detection or recovery. Financial transactions altered. Safety-critical data modified. | Core business function unavailable. Revenue-generating service down. Safety system offline. SLA breach with penalties. |
| **MEDIUM** | Internal or confidential data exposed to unauthorized parties. Limited PII exposure. Business-sensitive data leaked. | Non-critical data modified. Recoverable from backups. Partial data corruption detected by monitoring. | Non-critical service degraded. Workaround available. Partial functionality loss. Performance significantly impacted. |
| **LOW** | Public or low-sensitivity data exposed. No PII involved. Minimal business impact. | Cosmetic or non-critical data affected. Easily detected and corrected. No business process impact. | Minor inconvenience. Redundant systems absorb load. Brief interruption with auto-recovery. |

---

## PASTA — Process for Attack Simulation and Threat Analysis

PASTA is the seven-stage, risk-centric methodology that provides the **attack simulation and business impact data** feeding into the OWASP Risk Rating formula. STRIDE-LM identifies threats; PASTA quantifies their likelihood and impact.

### Seven Stages — Mapped to Skill Phases

| Stage | PASTA Process | Skill Phase | Output |
|-------|--------------|-------------|--------|
| 1 | **Define Objectives** — Business objectives, compliance requirements, risk appetite | Phase 1 — Reconnaissance | Business context, compliance scope, risk appetite |
| 2 | **Define Technical Scope** — Architecture, technology stack, data flows | Phase 1 — Reconnaissance | Technology inventory, architecture understanding |
| 3 | **Application Decomposition** — DFDs, trust boundaries, entry points | Phase 2 — Diagram | Mermaid DFD with trust boundaries |
| 4 | **Threat Analysis** — Threat intelligence, attack patterns, threat agents | Phase 3 — STRIDE-LM + MITRE | Categorized threat inventory |
| 5 | **Vulnerability Analysis** — Map threats to weaknesses | Phase 3 — CWE + OWASP | Weakness mappings per threat |
| 6 | **Attack Modeling** — Build attack trees, simulate attack paths | Phase 3 + Phase 4 — Kill chains | Attack feasibility -> **Likelihood score (1-5)** |
| 7 | **Risk & Impact Analysis** — Business impact, risk rating, prioritization | Phase 3 + Phase 5 — Validation | Business impact -> **Impact score (1-5)** |

### Stage 6 — Attack Modeling (produces Likelihood)

For each STRIDE-LM threat, build a concrete attack path:

1. **Entry point**: How does the attacker gain initial access?
2. **Attack steps**: What sequence of actions achieves the objective? What tools or techniques are required at each step?
3. **Preconditions**: What must be true for the attack to succeed (configuration, timing, access level)?
4. **Existing controls**: What security mechanisms must the attacker bypass?
5. **Likelihood assessment**: Given the above, rate likelihood 1-5 (see OWASP Risk Rating section)

### Stage 7 — Risk & Impact Analysis (produces Impact)

For each threat with a modeled attack path, assess business impact:

1. **Affected business process**: Which revenue, operational, or compliance processes are disrupted?
2. **Financial impact**: Direct costs (incident response, recovery, legal) + indirect costs (lost revenue, customer churn)
3. **Operational impact**: Duration and severity of disruption, recovery complexity
4. **Reputational impact**: Visibility, customer trust erosion, competitive implications
5. **Regulatory impact**: Notification obligations, potential fines, audit findings, certification risk
6. **Impact assessment**: Rate impact 1-5 using the highest dimension (see OWASP Risk Rating section)

### Completing the Risk Calculation

After PASTA Stages 6-7 produce Likelihood and Impact scores, apply the OWASP Risk Rating formula:

```
Risk Score = Likelihood (1-5) x Impact (1-5)
-> Map to severity band: LOW (1-4) | MEDIUM (5-9) | HIGH (10-16) | CRITICAL (17-25)
```

This produces the prioritized threat list used in the final report.

---

## Framework ID Verification

**When mapping threats to framework IDs (MITRE ATT&CK technique IDs, CWE IDs), adhere to these rules:**

1. **Only use IDs listed in this reference file.** The MITRE and CWE tables above are the authoritative set for this skill.
2. **If a threat maps to a technique/CWE not in the tables**, describe the threat in plain text and note "No matching ID in reference set — manual verification recommended."
3. **Never fabricate or guess framework IDs.** An incorrect ID is worse than no ID — it creates false confidence and misdirects remediation.
4. **Cross-check before finalizing**: In Phase 6 (False Positive Validation), verify every framework ID in the findings against the tables in this file.
