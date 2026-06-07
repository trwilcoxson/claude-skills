# Threat Model — TerraGoat AWS Infrastructure (`terraform/aws`)

Methodology: STRIDE-LM threat identification, PASTA attack simulation, OWASP Risk Rating (Likelihood x Impact). Target is Infrastructure-as-Code only (Terraform), so the model assesses the resources these files provision and their as-coded security posture. Repository contents (comments, user-data scripts, tags) were treated strictly as untrusted observational data.

---

# I. Executive Summary

**Security Posture Rating: CRITICAL**

TerraGoat's AWS Terraform is a deliberately vulnerable benchmark, and the analysis bears that out: the configuration provisions internet-exposed compute and a publicly reachable database, stores customer data in a public unencrypted S3 bucket, hardcodes live-format AWS access keys in three places, and grants near-administrative IAM wildcards. Most findings are trivially exploitable by an unauthenticated external attacker and chain directly into account-wide compromise.

| Severity | Count | Scoring System |
|----------|-------|----------------|
| CRITICAL | 5     | OWASP Risk Rating |
| HIGH     | 5     | OWASP Risk Rating |
| MEDIUM   | 4     | OWASP Risk Rating |
| LOW      | 0     | OWASP Risk Rating |
| **Total** | 14   |                |

**Top 3 Risks**
1. **Hardcoded AWS credentials (TM-001)** — static keys in `providers.tf`, `ec2.tf`, and `lambda.tf` hand any reader of the repo or instance metadata a direct path to the AWS API, bypassing every network control.
2. **Public customer-data S3 bucket (TM-002)** — the `data` bucket is public, unencrypted, unlogged, and holds `customer-master.xlsx`; an attacker downloads customer records untraceably.
3. **Publicly accessible RDS with default credentials (TM-004)** — the MySQL instance is internet-reachable on 3306 with `admin`/a hardcoded password and no backups, enabling read and destructive access with no recovery.

| Metric | Value |
|--------|-------|
| Components Assessed | 13 |
| Data Flows Mapped | 12 |
| Trust Boundaries Identified | 4 |
| Threat Actors Modeled | 4 |
| Unique Findings | 14 |

**Quick Wins**
- Remove the three hardcoded key pairs and rotate them (TM-001).
- Enable S3 Block Public Access account-wide (TM-002).
- Set `publicly_accessible = false` on the RDS instance (TM-004).
- Narrow SSH ingress off `0.0.0.0/0` (TM-003).
- Mark the `secret` Terraform output `sensitive` (TM-012).

---

# II. System Overview

**System Purpose:** Terraform that stands up an AWS environment — a public web/app tier (EC2 + Classic ELB), a MySQL RDS database with a PHP front end baked into user-data, a Lambda analysis function, an EKS cluster, an Elasticsearch monitoring domain, Neptune and Aurora databases, several S3 buckets, ECR, and supporting IAM/KMS/VPC resources.

**Scope Statement:** In scope: all `.tf` files under `terraform/aws/` plus `resources/Dockerfile` and the referenced payload artifacts. Out of scope: runtime application code beyond what is embedded in user-data, other cloud directories (azure/gcp), and live AWS account state (analysis is static, from code).

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| IaC | Terraform | n/a | AWS provider; S3 remote backend (`encrypt=true`) |
| Compute | EC2 (t2.nano), Lambda | nodejs12.x | EOL runtime; user-data provisioning |
| Orchestration | EKS | default | Public endpoint not disabled |
| Database | RDS MySQL 8.0, Aurora, Neptune | — | RDS public + unencrypted |
| Search | Elasticsearch | 2.3 | EOL engine, wildcard policy |
| Storage | S3, EBS, ECR | — | Mixed/absent encryption |
| Network | VPC, ELB (classic), IGW | — | Public subnets, open SGs |
| Base image | `python:3.7-slim` (Docker Hub) | 3.7 | EOL Python |

**Deployment Model:** AWS, region `us-west-2` (a second provider alias pins `us-west-1`), single-VPC public-subnet pattern for the web tier plus a separate EKS VPC. Architecture is a small monolith-style web/db stack with auxiliary managed services.

---

# III. Architecture Diagram

```mermaid
flowchart TD
    internet([Internet / Unauthenticated User])
    operator([Terraform Operator])

    subgraph PUB["web_vpc — public subnets (172.16.0.0/16)"]
        elb["C5: Classic ELB weblb HTTP :80 -> :8000"]
        web["C1: web_host EC2 Apache"]
        dbapp["C2: db_app EC2 PHP/Apache"]
        rds[("D6: RDS MySQL public :3306")]
        sg1{{"web-node SG ingress 22,80 = 0.0.0.0/0"}}
        sgr{{"rds SG egress 0.0.0.0/0"}}
    end

    subgraph EKSV["eks_vpc"]
        eks["C4: EKS cluster"]
    end

    subgraph MANAGED["Account-level managed services"]
        lambda["C3: analysis_lambda plaintext keys in env"]
        es[("C6: Elasticsearch 2.3 es:* Principal *")]
        neptune[("D8: Neptune")]
        aurora[("D7: Aurora app1-9")]
        ecr["C11: ECR repo (MUTABLE)"]
        kms["C10: KMS logs_key"]
    end

    subgraph STORAGE["S3"]
        s3data[("D1: data (PUBLIC) customer-master.xlsx")]
        s3fin[("D2: financials")]
        s3ops[("D3: operations")]
        s3ds[("D4: data_science")]
        s3logs[("D5: logs (KMS)")]
    end

    iamrole["C7: ec2 role s3/ec2/rds:*"]
    iamuser["C9: IAM user excess_policy"]
    state[("D10: TF state S3 backend")]

    internet --> elb --> web
    internet --> sg1 --> web
    internet --> sg1 --> dbapp
    internet --> rds
    internet --> es
    internet --> eks
    web -. instance profile .-> iamrole
    dbapp -. instance profile .-> iamrole
    iamrole --> s3data
    iamrole --> rds
    dbapp --> rds
    operator --> state
    operator --> internet
    ecr --> eks
```

**Component Metadata**

| Component | Type | Tech | Port/Protocol | Zone | Auth | Encryption | Notes |
|-----------|------|------|---------------|------|------|------------|-------|
| C1 web_host | EC2 | Apache | 80/HTTP, 22/SSH | public subnet | none at edge | EBS unencrypted | keys in user-data |
| C2 db_app | EC2 | PHP/Apache | 80, 22 | public subnet | none | — | PHP app baked in |
| C3 analysis_lambda | Lambda | nodejs12.x | event | account | role | — | plaintext keys in env |
| C4 EKS | cluster | k8s | 443 | eks_vpc | IAM/RBAC | secrets not enveloped | public endpoint |
| C5 ELB | classic LB | HTTP | 80 | public | none | no TLS | plaintext |
| C6 ES | managed | ES 2.3 | HTTPS | account | wildcard policy | none | EOL |
| C7 ec2role | IAM role | — | — | account | trust ec2 | — | s3/ec2/rds:* on * |
| C9 IAM user | IAM user | — | API | account | access key | — | excess_policy on * |
| D6 RDS | DB | MySQL 8.0 | 3306 | public | admin/pw | none | public + no backup |

**Trust Boundary Descriptions**
- **TB1 Internet -> public subnet:** the IGW plus `map_public_ip_on_launch=true` makes every instance directly routable from the internet; this boundary is the primary external attack surface.
- **TB2 Instance -> IAM role:** an instance compromise crosses into AWS API authority via the instance profile and IMDS; the boundary is only as strong as the role policy (here, wildcards).
- **TB3 Account -> Terraform operator / state:** state and outputs contain live secrets, so anyone with state/log read crosses into credential possession.
- **TB4 VPC internal -> RDS SG:** the database security group's `0.0.0.0/0` egress is an outbound trust gap enabling exfiltration from inside the VPC.

**Network Topology Data:** web_vpc `172.16.0.0/16`, subnets `172.16.10.0/24` (AZ a) and `172.16.11.0/24` (AZ b), both public; eks_vpc `10.10.0.0/16` with `10.10.10.0/24` and `10.10.11.0/24`. web-node SG: ingress 22 and 80 from `0.0.0.0/0`, egress all. rds/default SG: ingress 3306 from VPC CIDR, egress `0.0.0.0/0`.

---

# IV. Risk Overlay Diagram

```mermaid
flowchart TD
    classDef crit fill:#f8c9c9,stroke:#c0392b,stroke-width:2px
    classDef high fill:#fde1c9,stroke:#e67e22,stroke-width:2px
    classDef med fill:#fbf3c9,stroke:#f1c40f,stroke-width:1px
    classDef clean fill:#d6f5d6,stroke:#27ae60,stroke-width:1px

    s3data["D1 data bucket ⚠ I,T · LxI=25 CRITICAL CWE-732,200"]:::crit
    rds["D6 RDS public ⚠ I,S,D · LxI=20 CRITICAL CWE-798,311"]:::crit
    keys["X1 hardcoded keys ⚠ S,I,E,LM · LxI=25 CRITICAL CWE-798,312"]:::crit
    sg["E2/E3 open SSH/HTTP ⚠ S,E,LM · LxI=20 CRITICAL CWE-732,306"]:::crit
    iam["C7/C9 IAM wildcards ⚠ E,LM · LxI=20 CRITICAL CWE-269,732"]:::crit
    es["C6 ES wildcard ⚠ I,E,T · LxI=16 HIGH"]:::high
    enc["D2-D9 unencrypted ⚠ I · LxI=12 HIGH"]:::high
    eks["C4 EKS public ⚠ S,E,LM · LxI=12 HIGH"]:::high
    pubip["TB1 public IPs ⚠ S,I · LxI=12 HIGH"]:::high
    state["D10 TF state secrets ⚠ I,R · LxI=12 HIGH"]:::high
    elb["E1 plaintext HTTP ⚠ I,S,T · LxI=9 MEDIUM"]:::med
    egress["TB4 open egress ⚠ I,LM · LxI=9 MEDIUM"]:::med
    php["E5 PHP app input ⚠ T,I · LxI=9 MEDIUM"]:::med
    ecrn["X2 mutable image ⚠ T,LM · LxI=8 MEDIUM"]:::med
    logs["D5 logs bucket (KMS) no findings"]:::clean

    keys ==>|1| iam ==>|2| s3data
    sg ==>|3| rds
```

**Component Risk Mapping**

| Component | Risk Level | Finding IDs | STRIDE-LM | Top CWE |
|-----------|-----------|-------------|-----------|---------|
| D1 data bucket | CRITICAL | TM-002 | I,T | CWE-732 |
| D6 RDS | CRITICAL | TM-004 | I,S,D | CWE-798 |
| X1 keys / C3,C9 | CRITICAL | TM-001 | S,I,E,LM | CWE-798 |
| E2/E3 SGs | CRITICAL | TM-003 | S,E,LM | CWE-732 |
| C7/C9 IAM | CRITICAL | TM-005 | E,LM | CWE-269 |
| C6 ES | HIGH | TM-007 | I,E,T | CWE-862 |
| D2-D9 stores | HIGH | TM-006 | I | CWE-311 |
| C4 EKS | HIGH | TM-009 | S,E,LM | CWE-862 |
| TB1 public IP | HIGH | TM-011 | S,I | CWE-732 |
| D10 state | HIGH | TM-012 | I,R | CWE-312 |
| C5/E1 ELB | MEDIUM | TM-008 | I,S,T | CWE-311 |
| TB4 egress | MEDIUM | TM-010 | I,LM | CWE-732 |
| C2/E5 PHP | MEDIUM | TM-013 | T,I | CWE-89 |
| C11/X2 ECR | MEDIUM | TM-014 | T,LM | CWE-732 |
| D5 logs | none | — | — | — |

**Critical Data Flow Highlights**
1. Internet -> RDS :3306 (TM-004) — direct DB exposure.
2. Repo/IMDS -> AWS API via static keys (TM-001) — credential theft to full API.
3. Instance -> IAM role -> S3/EC2/RDS:* (TM-005) — privilege escalation/lateral movement.
4. Internet -> public `data` bucket (TM-002) — customer-data exfiltration.
5. Internet -> open SSH (TM-003) -> instance shell -> role abuse.

---

# V. Asset Inventory

| Asset | Classification | Storage | Enc at Rest | Enc in Transit | Access Controls | Retention |
|-------|---------------|---------|-------------|----------------|-----------------|-----------|
| customer-master.xlsx | RESTRICTED | S3 `data` (D1) | None | None (public) | Public | None |
| Financial data | CONFIDENTIAL | S3 `financials` (D2) | None | TLS (S3) | private ACL | None |
| Operations data | INTERNAL | S3 `operations` (D3) | None | TLS | private | versioned |
| Data-science data | INTERNAL | S3 `data_science` (D4) | None | TLS | private | versioned |
| Access logs | INTERNAL | S3 `logs` (D5) | KMS | TLS | log-delivery | versioned |
| Employee records | CONFIDENTIAL | RDS MySQL (D6) | None | None | admin/pw | none (backup 0) |
| Graph data | CONFIDENTIAL | Neptune (D8) | None | TLS | IAM auth off | snapshot |
| App cluster data | CONFIDENTIAL | Aurora (D7) | None | TLS | default | varies |
| Block storage | INTERNAL | EBS vol/snap (D9) | None | n/a | account | snapshot |
| AWS credentials | RESTRICTED | code/state/env (X1,D10) | varies | n/a | broad | n/a |

**Data Flow Summary**

| Source | Destination | Protocol | Data Type | Sensitivity | Finding Refs |
|--------|------------|----------|-----------|-------------|--------------|
| Internet | ELB/EC2 | HTTP :80 | form input | CONFIDENTIAL | TM-008, TM-003 |
| Internet | RDS | TCP :3306 | DB queries | CONFIDENTIAL | TM-004 |
| EC2 | IAM role | IMDS | credentials | RESTRICTED | TM-001, TM-005 |
| IAM role | S3/RDS | API | data | RESTRICTED | TM-005 |
| db_app | RDS | mysqli | records | CONFIDENTIAL | TM-013 |
| Operator | TF state | S3 | secrets | RESTRICTED | TM-012 |
| Internet | ES domain | HTTPS | index data | CONFIDENTIAL | TM-007 |

---

# VI. Threat Actor Profiles

### Opportunistic / Script Kiddie
| Attribute | Value |
|-----------|-------|
| Type | External |
| Motivation | Notoriety, low-effort gain |
| Capability | 2 |
| Access Level | Unauthenticated |
| Linked Findings | TM-002, TM-003, TM-004, TM-011 |

### Organized Crime
| Attribute | Value |
|-----------|-------|
| Type | External |
| Motivation | Financial gain |
| Capability | 4 |
| Access Level | Unauthenticated -> escalates |
| Linked Findings | TM-001, TM-004, TM-005, TM-007, TM-013 |

### Malicious / Negligent Insider
| Attribute | Value |
|-----------|-------|
| Type | Insider |
| Motivation | Revenge / accidental |
| Capability | 3 |
| Access Level | Repo/state read |
| Linked Findings | TM-001, TM-012, TM-006 |

### Supply Chain Attacker
| Attribute | Value |
|-----------|-------|
| Type | External (indirect) |
| Motivation | Persistence, downstream compromise |
| Capability | 4 |
| Access Level | Upstream registry / repo |
| Linked Findings | TM-014 |

---

# VII. Findings

### [CRITICAL] TM-001: Hardcoded AWS access keys in provider, EC2 user-data, and Lambda env

| Field | Value |
|-------|-------|
| **ID** | TM-001 |
| **Severity** | CRITICAL |
| **Affected Component(s)** | C3, C9 (providers.tf, ec2.tf, lambda.tf) |
| **STRIDE-LM Category** | S,I,E,LM |
| **MITRE ATT&CK** | T1552, T1078 |
| **CWE** | CWE-798, CWE-312 |
| **OWASP Category** | A07:2021 Identification and Authentication Failures |
| **CIA Impact** | C: H · I: H · A: H |
| **PASTA Likelihood** | 5 — keys are in plaintext in the repo and instance user-data; reading them needs no skill |
| **PASTA Impact** | 5 — direct AWS API access, account-wide |
| **OWASP Risk Rating** | 25 (CRITICAL) |
| **Confidence** | HIGH |
| **Remediation** | R-001 |
| **Source** | threat-model |

**Attack Scenario:**
1. Attacker reads `providers.tf` (`AKIAIOSFODNN7EXAMPLE`), `ec2.tf` user-data, or `lambda.tf` env, or pulls user-data via IMDS after any instance foothold.
2. Configures the AWS CLI with the lifted keys.
3. Authenticates directly to the AWS API, bypassing all VPC/SG controls.

**Existing Mitigations:** None. The provider alias literally embeds a key pair.

**Recommended Remediation:** Delete all literal keys; use the default credential chain, instance roles, and Secrets Manager. Rotate exposed keys; add CI secret scanning.

---

### [CRITICAL] TM-002: Public, unencrypted, unlogged S3 bucket holding customer data

| Field | Value |
|-------|-------|
| **ID** | TM-002 |
| **Severity** | CRITICAL |
| **Affected Component(s)** | D1 |
| **STRIDE-LM Category** | I,T |
| **MITRE ATT&CK** | T1530 |
| **CWE** | CWE-732, CWE-200 |
| **OWASP Category** | A01:2021 Broken Access Control |
| **CIA Impact** | C: H · I: M · A: L |
| **PASTA Likelihood** | 5 — public bucket, predictable name, no auth |
| **PASTA Impact** | 5 — customer PII exfiltration, regulatory |
| **OWASP Risk Rating** | 25 (CRITICAL) |
| **Confidence** | HIGH |
| **Remediation** | R-002 |
| **Source** | threat-model |

**Attack Scenario:**
1. Attacker guesses the bucket name `<account>-acme-dev-data`.
2. Lists/downloads `customer-master.xlsx` anonymously.
3. No access logging records the read.

**Existing Mitigations:** None (no Block Public Access, no SSE, no logging, no versioning).

**Recommended Remediation:** Enable account/bucket Block Public Access, SSE-KMS, versioning, and access logging; tighten the bucket policy.

---

### [CRITICAL] TM-003: Security group exposes SSH and HTTP to the entire internet

| Field | Value |
|-------|-------|
| **ID** | TM-003 |
| **Severity** | CRITICAL |
| **Affected Component(s)** | C1, C2, C12 |
| **STRIDE-LM Category** | S,E,LM |
| **MITRE ATT&CK** | T1190, T1110 |
| **CWE** | CWE-732, CWE-306 |
| **OWASP Category** | A05:2021 Security Misconfiguration |
| **CIA Impact** | C: H · I: H · A: M |
| **PASTA Likelihood** | 5 — open `0.0.0.0/0` ingress, automated scanning |
| **PASTA Impact** | 4 — instance compromise + role pivot |
| **OWASP Risk Rating** | 20 (CRITICAL) |
| **Confidence** | HIGH |
| **Remediation** | R-003 |
| **Source** | threat-model |

**Attack Scenario:**
1. Scan finds 22/80 open from anywhere on the public IP.
2. Brute-force/exploit SSH; gain shell.
3. Pivot to AWS via the attached instance role (TM-005).

**Existing Mitigations:** None.

**Recommended Remediation:** Restrict SSH to bastion/VPN CIDR or use SSM; front HTTP via LB/WAF.

---

### [CRITICAL] TM-004: RDS MySQL publicly accessible, unencrypted, default password, no backups

| Field | Value |
|-------|-------|
| **ID** | TM-004 |
| **Severity** | CRITICAL |
| **Affected Component(s)** | D6 |
| **STRIDE-LM Category** | I,S,D |
| **MITRE ATT&CK** | T1190, T1078 |
| **CWE** | CWE-798, CWE-311 |
| **OWASP Category** | A02:2021 Cryptographic Failures |
| **CIA Impact** | C: H · I: H · A: H |
| **PASTA Likelihood** | 4 — public endpoint + known creds; needs DB reachability |
| **PASTA Impact** | 5 — full DB read/destroy, no backup |
| **OWASP Risk Rating** | 20 (CRITICAL) |
| **Confidence** | HIGH |
| **Remediation** | R-004 |
| **Source** | threat-model |

**Attack Scenario:**
1. Resolve the public RDS endpoint (also emitted as an output).
2. Connect on 3306 with `admin` / `Aa1234321Bb`.
3. Read or drop data; `backup_retention_period=0` prevents recovery.

**Existing Mitigations:** SG ingress is scoped to the VPC CIDR, but `publicly_accessible=true` undercuts it.

**Recommended Remediation:** `publicly_accessible=false`, `storage_encrypted=true`, secret-managed strong password, enable backups + deletion protection.

---

### [CRITICAL] TM-005: Over-permissive IAM — wildcard actions on all resources

| Field | Value |
|-------|-------|
| **ID** | TM-005 |
| **Severity** | CRITICAL |
| **Affected Component(s)** | C7, C9 |
| **STRIDE-LM Category** | E,LM |
| **MITRE ATT&CK** | T1078, T1098 |
| **CWE** | CWE-269, CWE-732 |
| **OWASP Category** | A01:2021 Broken Access Control |
| **CIA Impact** | C: H · I: H · A: H |
| **PASTA Likelihood** | 4 — needs a prior foothold or key leak |
| **PASTA Impact** | 5 — near-admin, account-wide blast radius |
| **OWASP Risk Rating** | 20 (CRITICAL) |
| **Confidence** | HIGH |
| **Remediation** | R-005 |
| **Source** | threat-model |

**Attack Scenario:**
1. Compromise an instance (IMDS) or the IAM user's access key.
2. Use `s3:*`/`ec2:*`/`rds:*` (or `lambda:*`/`cloudwatch:*`) on `*`.
3. Read all buckets, modify infra, move laterally.

**Existing Mitigations:** None — both policies use wildcards on `Resource: *`.

**Recommended Remediation:** Scope actions/ARNs to least privilege; require IMDSv2; replace long-lived user keys with roles.

---

### [HIGH] TM-006: Sensitive data stores unencrypted at rest

| Field | Value |
|-------|-------|
| **ID** | TM-006 |
| **Severity** | HIGH |
| **Affected Component(s)** | D2, D3, D4, D7, D8, D9 |
| **STRIDE-LM Category** | I |
| **MITRE ATT&CK** | T1530 |
| **CWE** | CWE-311 |
| **OWASP Category** | A02:2021 Cryptographic Failures |
| **CIA Impact** | C: H · I: M · A: L |
| **PASTA Likelihood** | 3 — requires snapshot/volume/storage access |
| **PASTA Impact** | 4 — exposure of confidential data |
| **OWASP Risk Rating** | 12 (HIGH) |
| **Confidence** | HIGH |
| **Remediation** | R-006 |
| **Source** | threat-model |

**Attack Scenario:**
1. Obtain an EBS snapshot, volume, or storage-layer access.
2. Read plaintext data; share the unencrypted snapshot cross-account.

**Existing Mitigations:** Only the `logs` bucket (D5) uses KMS.

**Recommended Remediation:** SSE-KMS on S3, `encrypted=true` on EBS vol/snap, `storage_encrypted=true` on Neptune/Aurora.

---

### [HIGH] TM-007: Elasticsearch access policy allows es:* to any AWS principal

| Field | Value |
|-------|-------|
| **ID** | TM-007 |
| **Severity** | HIGH |
| **Affected Component(s)** | C6 |
| **STRIDE-LM Category** | I,E,T |
| **MITRE ATT&CK** | T1530 |
| **CWE** | CWE-862, CWE-732 |
| **OWASP Category** | A01:2021 Broken Access Control |
| **CIA Impact** | C: H · I: H · A: M |
| **PASTA Likelihood** | 4 — wildcard principal, no VPC/IP restriction |
| **PASTA Impact** | 4 — read/modify monitoring index |
| **OWASP Risk Rating** | 16 (HIGH) |
| **Confidence** | HIGH |
| **Remediation** | R-007 |
| **Source** | threat-model |

**Attack Scenario:**
1. External AWS principal targets the domain endpoint.
2. Policy `es:*` / `Principal AWS:*` / `Resource *` permits access.
3. Read/alter indices; EOL 2.3 engine adds known CVE exposure.

**Existing Mitigations:** None.

**Recommended Remediation:** Scope principals + source IP/VPC, deploy in-VPC, enable encryption, upgrade engine.

---

### [HIGH] TM-009: EKS control-plane endpoint public by default

| Field | Value |
|-------|-------|
| **ID** | TM-009 |
| **Severity** | HIGH |
| **Affected Component(s)** | C4 |
| **STRIDE-LM Category** | S,E,LM |
| **MITRE ATT&CK** | T1190 |
| **CWE** | CWE-862 |
| **OWASP Category** | A05:2021 Security Misconfiguration |
| **CIA Impact** | C: H · I: H · A: M |
| **PASTA Likelihood** | 3 — public API but auth still required |
| **PASTA Impact** | 4 — cluster-wide workload control on success |
| **OWASP Risk Rating** | 12 (HIGH) |
| **Confidence** | MEDIUM |
| **Remediation** | R-009 |
| **Source** | threat-model |

**Attack Scenario:**
1. `endpoint_private_access=true` does not disable public access; API is internet-reachable.
2. Nodes sit in public subnets.
3. API auth abuse on success schedules workloads.

**Existing Mitigations:** Private access enabled (partial).

**Recommended Remediation:** `endpoint_public_access=false` or restrict CIDRs; private node subnets; control-plane logging; secrets encryption.

---

### [HIGH] TM-011: Workloads auto-assigned public IPs in public subnets

| Field | Value |
|-------|-------|
| **ID** | TM-011 |
| **Severity** | HIGH |
| **Affected Component(s)** | C1, C2, C12 |
| **STRIDE-LM Category** | S,I |
| **MITRE ATT&CK** | T1190 |
| **CWE** | CWE-732 |
| **OWASP Category** | A05:2021 Security Misconfiguration |
| **CIA Impact** | C: M · I: M · A: M |
| **PASTA Likelihood** | 4 — default-on public IP behind IGW |
| **PASTA Impact** | 3 — enlarges exposure for other findings |
| **OWASP Risk Rating** | 12 (HIGH) |
| **Confidence** | HIGH |
| **Remediation** | R-011 |
| **Source** | threat-model |

**Attack Scenario:**
1. `map_public_ip_on_launch=true` gives every instance a routable IP.
2. The IGW route makes them externally reachable.
3. This amplifies TM-003, TM-004, TM-013.

**Existing Mitigations:** None.

**Recommended Remediation:** Disable auto public IP; use private subnets; expose only the LB.

---

### [HIGH] TM-012: Secrets and sensitive endpoints exposed via Terraform outputs and state

| Field | Value |
|-------|-------|
| **ID** | TM-012 |
| **Severity** | HIGH |
| **Affected Component(s)** | D10 |
| **STRIDE-LM Category** | I,R |
| **MITRE ATT&CK** | T1552 |
| **CWE** | CWE-312, CWE-200 |
| **OWASP Category** | A02:2021 Cryptographic Failures |
| **CIA Impact** | C: H · I: M · A: L |
| **PASTA Likelihood** | 3 — requires state/log read access |
| **PASTA Impact** | 4 — live secret harvest |
| **OWASP Risk Rating** | 12 (HIGH) |
| **Confidence** | HIGH |
| **Remediation** | R-012 |
| **Source** | threat-model |

**Attack Scenario:**
1. Read Terraform state (S3 backend) or the `secret`/`db_endpoint` outputs.
2. Recover the IAM user secret, DB password, and target endpoints.
3. Use them to reach live resources.

**Existing Mitigations:** Backend `encrypt=true`; outputs are not marked `sensitive`.

**Recommended Remediation:** Mark secret outputs `sensitive`, stop emitting credentials, lock down the state bucket, use Secrets Manager.

---

### [MEDIUM] TM-008: ELB and web tier serve plaintext HTTP (no TLS)

| Field | Value |
|-------|-------|
| **ID** | TM-008 |
| **Severity** | MEDIUM |
| **Affected Component(s)** | C5, C1 |
| **STRIDE-LM Category** | I,S,T |
| **MITRE ATT&CK** | — |
| **CWE** | CWE-311, CWE-326 |
| **OWASP Category** | A02:2021 Cryptographic Failures |
| **CIA Impact** | C: M · I: M · A: L |
| **PASTA Likelihood** | 3 — needs network position |
| **PASTA Impact** | 3 — eavesdrop/modify form data |
| **OWASP Risk Rating** | 9 (MEDIUM) |
| **Confidence** | HIGH |
| **Remediation** | R-008 |
| **Source** | threat-model |

**Attack Scenario:**
1. ELB listener is HTTP :80 -> :8000; servers serve plain HTTP.
2. On-path attacker reads/modifies employee form data in transit.

**Existing Mitigations:** None.

**Recommended Remediation:** HTTPS listener + ACM cert, HTTP->HTTPS redirect, end-to-end TLS.

---

### [MEDIUM] TM-010: Unrestricted egress (0.0.0.0/0) enables exfiltration

| Field | Value |
|-------|-------|
| **ID** | TM-010 |
| **Severity** | MEDIUM |
| **Affected Component(s)** | C12 |
| **STRIDE-LM Category** | I,LM |
| **MITRE ATT&CK** | T1048 |
| **CWE** | CWE-732 |
| **OWASP Category** | A05:2021 Security Misconfiguration |
| **CIA Impact** | C: M · I: L · A: L |
| **PASTA Likelihood** | 3 — needs prior compromise |
| **PASTA Impact** | 3 — exfiltration channel |
| **OWASP Risk Rating** | 9 (MEDIUM) |
| **Confidence** | HIGH |
| **Remediation** | R-010 |
| **Source** | threat-model |

**Attack Scenario:**
1. Compromise an instance/DB host.
2. SG egress `0.0.0.0/0` permits beaconing/exfil over any protocol.

**Existing Mitigations:** None.

**Recommended Remediation:** Restrict egress to required destinations; route via NAT/proxy; add egress monitoring.

---

### [MEDIUM] TM-013: Provisioned PHP app uses string-built SQL with admin DB user

| Field | Value |
|-------|-------|
| **ID** | TM-013 |
| **Severity** | MEDIUM |
| **Affected Component(s)** | C2 |
| **STRIDE-LM Category** | T,I |
| **MITRE ATT&CK** | T1190 |
| **CWE** | CWE-89, CWE-20 |
| **OWASP Category** | A03:2021 Injection |
| **CIA Impact** | C: M · I: M · A: L |
| **PASTA Likelihood** | 3 — escaping present but fragile, public app |
| **PASTA Impact** | 3 — data tampering via admin DB user |
| **OWASP Risk Rating** | 9 (MEDIUM) |
| **Confidence** | MEDIUM |
| **Remediation** | R-013 |
| **Source** | threat-model |

**Attack Scenario:**
1. The baked `index.php` takes `$_POST['NAME']/['ADDRESS']` into string-built mysqli queries against the RDS `admin` user.
2. Any weakening of escaping (or the `SELECT *` listing path) exposes injection.

**Existing Mitigations:** `mysqli_real_escape_string` is used but the design is string concatenation with a high-privilege user.

**Recommended Remediation:** Prepared statements; least-privilege DB user; WAF; do not bake app source into user-data.

---

### [MEDIUM] TM-014: ECR mutable tags + unscanned image; build pulls EOL public base image

| Field | Value |
|-------|-------|
| **ID** | TM-014 |
| **Severity** | MEDIUM |
| **Affected Component(s)** | C11, C4 |
| **STRIDE-LM Category** | T,LM |
| **MITRE ATT&CK** | T1195 |
| **CWE** | CWE-732 |
| **OWASP Category** | A08:2021 Software and Data Integrity Failures |
| **CIA Impact** | C: M · I: H · A: M |
| **PASTA Likelihood** | 2 — needs push or upstream compromise |
| **PASTA Impact** | 4 — tampered image runs downstream |
| **OWASP Risk Rating** | 8 (MEDIUM) |
| **Confidence** | MEDIUM |
| **Remediation** | R-014 |
| **Source** | threat-model |

**Attack Scenario:**
1. `image_tag_mutability=MUTABLE`, no `scan_on_push`; Dockerfile pulls EOL `python:3.7-slim`.
2. An actor with push access (or who compromises the base image) overwrites an existing tag.
3. Downstream pulls run the tampered image.

**Existing Mitigations:** None.

**Recommended Remediation:** `IMMUTABLE` tags, `scan_on_push`, pin base images by digest, internal mirror.

---

**Total: 14 findings (5 critical, 5 high, 4 medium, 0 low)**

---

# VIII. Remediation Roadmap

| R-ID | Title | Addresses Findings | Priority | Effort | Dependencies |
|------|-------|--------------------|----------|--------|--------------|
| R-001 | Remove + rotate hardcoded keys | TM-001 | P0 | LOW | — |
| R-002 | S3 Block Public Access + SSE/logging | TM-002 | P0 | LOW | — |
| R-003 | Restrict SSH/HTTP ingress | TM-003 | P0 | LOW | — |
| R-004 | Lock down RDS (private, encrypt, pw, backup) | TM-004 | P0 | MEDIUM | R-001 |
| R-005 | Least-privilege IAM + IMDSv2 | TM-005 | P0 | MEDIUM | — |
| R-006 | Encrypt all data stores at rest | TM-006 | P1 | MEDIUM | — |
| R-007 | Scope ES policy + in-VPC + upgrade | TM-007 | P1 | MEDIUM | — |
| R-008 | TLS on ELB/web tier | TM-008 | P2 | LOW | — |
| R-009 | Private EKS endpoint + logging | TM-009 | P1 | MEDIUM | — |
| R-010 | Restrict SG egress | TM-010 | P2 | LOW | — |
| R-011 | Private subnets / no auto public IP | TM-011 | P1 | MEDIUM | R-008 |
| R-012 | Sensitive outputs + state lockdown | TM-012 | P1 | LOW | R-001 |
| R-013 | Prepared statements + LP DB user | TM-013 | P2 | MEDIUM | R-004 |
| R-014 | Immutable + scanned images | TM-014 | P2 | LOW | — |

**Wave 1 — Prerequisites:** R-001 (rotate keys) gates R-004 and R-012.

**Wave 2 — Critical Fixes:** R-001, R-002, R-003, R-004, R-005 (all CRITICAL).

**Wave 3 — Hardening:** R-006, R-007, R-009, R-011, R-012, R-008, R-010, R-013, R-014.

**Wave 4 — Monitoring & Observability:** enable S3 access logging, VPC flow log review, CloudTrail, GuardDuty, EKS control-plane logs, egress monitoring (supports TM-002, TM-009, TM-010).

**Quick Wins:** R-001, R-002, R-003, R-012, R-008 — low-effort, no/short dependencies.

**Dependency Chains:** `R-001 -> R-004 -> R-013`; `R-001 -> R-012`; `R-008 -> R-011`.

---

# IX. Networking & Infrastructure Data

**VPC/Network Topology:** Two VPCs — web_vpc `172.16.0.0/16` (public web/db tier) and eks_vpc `10.10.0.0/16` (EKS).

| Subnet Name | CIDR | Availability Zone | Type (Public/Private) | Associated Components |
|-------------|------|-------------------|----------------------|----------------------|
| web_subnet | 172.16.10.0/24 | us-west-2a | Public | C1, C2, ELB, RDS |
| web_subnet2 | 172.16.11.0/24 | us-west-2b | Public | RDS subnet group |
| eks_subnet1 | 10.10.10.0/24 | us-west-2a | Public | C4 |
| eks_subnet2 | 10.10.11.0/24 | us-west-2b | Public | C4 |

| SG Name | Direction | Protocol | Port Range | Source/Destination | Description |
|---------|-----------|----------|------------|-------------------|-------------|
| web-node | Ingress | tcp | 22 | 0.0.0.0/0 | SSH open to world (TM-003) |
| web-node | Ingress | tcp | 80 | 0.0.0.0/0 | HTTP open to world (TM-003) |
| web-node | Egress | all | all | 0.0.0.0/0 | Unrestricted egress (TM-010) |
| rds/default | Ingress | tcp | 3306 | VPC CIDR | DB ingress scoped to VPC |
| rds/default | Egress | all | all | 0.0.0.0/0 | Unrestricted egress (TM-010) |

**Load Balancer Configuration:** Classic ELB `weblb`, HTTP listener :80 -> instance :8000, health check `HTTP:8000/`. No HTTPS/TLS (TM-008).

**NAT/Internet Gateway:** IGW `web_igw` with `0.0.0.0/0` route on `web_rtb`; no NAT gateway. Public subnets auto-assign public IPs (TM-011).

**DNS & Certificates:** `enable_dns_hostnames`/`enable_dns_support` on; public DNS emitted as outputs. No ACM certificates configured.

| Role Name | Attached Policies | Trust Relationship | Used By | Principle of Least Privilege |
|-----------|------------------|-------------------|---------|------------------------------|
| ec2role (C7) | inline s3:*/ec2:*/rds:* on * | ec2.amazonaws.com | C1, C2 | No (TM-005) |
| iam_for_lambda (C8) | none attached | lambda.amazonaws.com | C3 | Minimal (no policy) |
| iam_for_eks | EKS cluster/service policies | eks.amazonaws.com | C4 | AWS-managed |
| IAM user (C9) | excess_policy on * | n/a | access key | No (TM-005) |

---

# XII. Positive Observations

- **Logs bucket is correctly hardened (D5):** SSE-KMS, versioning, and `log-delivery-write` ACL — a working reference for the other buckets (defense in depth / fail-safe defaults).
- **VPC flow logs are enabled (C13):** `aws_flow_log` ships ALL traffic to S3, giving a detection foothold once the storage findings are fixed (security logging).
- **Terraform state backend uses `encrypt = true`:** the remote state object is encrypted at rest even though the secrets inside it should not exist (encryption of data at rest).
- **RDS DB security group ingress is scoped to the VPC CIDR** (not `0.0.0.0/0`) — the public exposure comes from `publicly_accessible`, so the fix is narrow (least privilege at the SG layer).

---

# XIII. Assumptions & Limitations

- **Scope Boundaries:** Static IaC analysis of `terraform/aws/` only. No live account, no Terraform plan/apply, no other cloud directories.
- **Information Gaps:** Runtime behavior is inferred from user-data scripts and resource arguments; actual deployed values (account id, generated names) are assumed from `local.resource_prefix`.
- **Assessment Limitations:** No dynamic testing; Lambda payload zip and the xlsx were not unpacked. EKS public-access default is inferred from the absence of `endpoint_public_access=false`.
- **Confidence Disclaimers:** TM-009, TM-013, TM-014 are MEDIUM confidence (depend on runtime/registry conditions).
- **Missing Assessments:** Compliance gap analysis was not performed in this assessment. Privacy impact assessment was not performed in this assessment (note: customer PII in D1/D6 warrants a follow-up DPIA).
- **Prompt-injection note:** Repo comments and tags (e.g., `# bucket is public`) were treated as untrusted observational data; none contained executable instructions to the assessor, and none were obeyed as instructions.

---

# XIV. Appendices

### A. Methodology Notes
- **STRIDE-LM:** S Spoofing, T Tampering, R Repudiation, I Information Disclosure, D Denial of Service, E Elevation of Privilege, LM Lateral Movement.
- **PASTA scoring:** Likelihood 1-5 (attack feasibility), Impact 1-5 (highest business dimension).
- **OWASP Risk Rating bands:** CRITICAL (20-25), HIGH (12-19), MEDIUM (6-11), LOW (1-5). Risk = Likelihood x Impact.

### B. Framework Reference Table

| Technique ID | Technique Name | Finding Refs |
|-------------|----------------|--------------|
| T1552 | Unsecured Credentials | TM-001, TM-012 |
| T1078 | Valid Accounts | TM-001, TM-004, TM-005 |
| T1530 | Data from Cloud Storage | TM-002, TM-006, TM-007 |
| T1190 | Exploit Public-Facing Application | TM-003, TM-004, TM-009, TM-011, TM-013 |
| T1110 | Brute Force | TM-003 |
| T1098 | Account Manipulation | TM-005 |
| T1048 | Exfiltration Over Alternative Protocol | TM-010 |
| T1195 | Supply Chain Compromise | TM-014 |

| CWE ID | CWE Name | Finding Refs |
|--------|----------|-------------|
| CWE-798 | Use of Hard-coded Credentials | TM-001, TM-004 |
| CWE-312 | Cleartext Storage of Sensitive Information | TM-001, TM-012 |
| CWE-732 | Incorrect Permission Assignment | TM-002, TM-003, TM-005, TM-007, TM-010, TM-011, TM-014 |
| CWE-200 | Exposure of Sensitive Information | TM-002, TM-012 |
| CWE-306 | Missing Authentication for Critical Function | TM-003 |
| CWE-311 | Missing Encryption of Sensitive Data | TM-004, TM-006, TM-008 |
| CWE-269 | Improper Privilege Management | TM-005 |
| CWE-862 | Missing Authorization | TM-007, TM-009 |
| CWE-326 | Inadequate Encryption Strength | TM-008 |
| CWE-89 | SQL Injection | TM-013 |
| CWE-20 | Improper Input Validation | TM-013 |

### C. QA Corrections Log

| Issue | Location | Severity | Correction Applied |
|-------|----------|----------|--------------------|
| TM-011 band recalculation | findings.json | minor | severity raised MEDIUM->HIGH to match band(4x3)=12 |
| Non-reference CWE IDs | TM-003/011/014 | minor | replaced with frameworks.md-verified CWE IDs |

### D. Glossary
- **ACL** — Access Control List.
- **AMI** — Amazon Machine Image.
- **EBS** — Elastic Block Store.
- **EKS** — Elastic Kubernetes Service.
- **ELB** — Elastic Load Balancer.
- **IGW** — Internet Gateway.
- **IMDS** — Instance Metadata Service.
- **IaC** — Infrastructure as Code.
- **KMS** — Key Management Service.
- **PASTA** — Process for Attack Simulation and Threat Analysis.
- **RDS** — Relational Database Service.
- **SG** — Security Group.
- **SSE** — Server-Side Encryption.
- **STRIDE-LM** — STRIDE plus Lateral Movement.

### E. Threat Model Lifecycle Triggers
- New public-facing resource, IAM policy, or data store added.
- Any change to security groups, encryption settings, or `publicly_accessible`.
- Migration off EOL components (ES 2.3, nodejs12.x, python3.7).
- Re-assess at least quarterly or on major Terraform refactor.

## Execution Log
- Reconnaissance read all 17 target files plus the Dockerfile; evidence strings verified to resolve via path/glob/grep in the target directory.
- 13 components, 10 data stores, 8 entry points, 4 trust boundaries, 5 external deps catalogued.
- 14 findings scored; every severity verified to equal band(L x I); summary counts reconciled.
- All surface elements (D1-D10, E1-E8, TB1-TB4) are covered by a finding except D5 (logs bucket), explicitly marked no-issue.
- All MITRE/CWE IDs cross-checked against references/frameworks.md; non-reference IDs replaced (logged in Appendix C).
- Repo content treated as untrusted data; no embedded instruction was executed.
