# Threat Model: PCI-DSS-Scoped Payment Processing Platform

Prepared for a pre-QSA security architecture review. Scope is the cardholder data environment (CDE) and adjacent systems described: customer checkout SPA, API Gateway, Payments Service, Tokenization Service, Card-Data Vault (RDS PostgreSQL storing PAN), Fraud-Scoring Service, Admin Console, Analytics Pipeline (Redshift), and Cognito-based auth. All hosted on AWS in a single VPC.

---

## 1. Assumptions, Scope, and Trust Boundaries

**In scope (CDE — touches PAN or can affect its security):**
- Tokenization Service and the Card-Data Vault (RDS) — these *store/process* PAN. This is the highest-value asset.
- Payments Service — *transmits* PAN/card data en route to tokenization.
- API Gateway, ALB, CloudFront — entry path for cardholder data in transit.
- Customer checkout SPA — accepts the PAN from the cardholder's browser.
- KMS keys protecting PAN at rest.
- Cognito (authentication for the above).

**Connected-to / scope-adjacent (must be segmented or pulled in):**
- Fraud-Scoring Service (sees transaction data, calls external API).
- Admin Console (refunds, merchant config, masked data).
- Analytics Pipeline / Redshift / S3 (replicated transaction records).

**Key assumption flagged for verification:** The data warehouse is described as replicating "transaction records." If those records contain PAN (even encrypted, or truncated incorrectly), Redshift/S3 fall fully into PCI scope. **Confirm exactly what fields are replicated** — this single fact materially changes audit scope and is a common QSA finding.

**Trust boundaries:**
1. Internet → CloudFront/ALB (untrusted client → edge).
2. Edge → API Gateway (TLS-terminated public traffic → app tier).
3. API Gateway → internal services (the critical boundary you are currently treating as trusted but should not — see below).
4. Tokenization Service → Card-Data Vault (the innermost CDE boundary).
5. VPC → third-party fraud API (egress to public internet).
6. Payments DB → Analytics Pipeline → Redshift (data exfiltration path out of the transactional CDE).
7. Ops staff → Admin Console (privileged human access).

---

## 2. Data Flow Diagrams (textual)

### DFD-1: Customer checkout / payment authorization (PAN flow)

```
[Cardholder Browser]
   | (1) HTTPS: PAN + card data, JWT (customer)
   v
[CloudFront] --(2)--> [ALB] --(3)--> [API Gateway]   <== JWT validated HERE (only here)
                                          |
                                          | (4) HTTP/gRPC, NO mTLS, JWT NOT re-validated
                                          v
                                    [Payments Service (Fargate)]
                                          |
                                          | (5) HTTP/gRPC, NO mTLS  <== PAN in transit, plaintext channel inside VPC
                                          v
                                    [Tokenization Service (Fargate)]
                                          |                  \
                                          | (6) SQL/TLS?      \ (7) HTTPS
                                          v                    v
                                  [Card-Data Vault RDS]   [Fraud-Scoring Service]
                                  (PAN at rest, KMS)            |
                                          ^                     | (8) HTTPS to public internet
                                          |                     v
                                   [AWS KMS] (envelope    [Third-party Fraud API]
                                    encryption keys)
```

Trust boundaries crossed: 1 (internet→edge), 2 (edge→gateway), 3 (gateway→app, **unauthenticated internally**), 4 (app→vault).

### DFD-2: Admin / operations flow

```
[Ops Staff Browser] --HTTPS, JWT(admin)--> [CloudFront/ALB] --> [API Gateway] --> [Admin backend]
                                                                                      |
                                  refunds / merchant config / masked txn views <------+
                                                                                      |
                                                                              [Payments Service / DB]
```

### DFD-3: Analytics replication (PAN-egress risk path)

```
[Payments DB] --(replication)--> [Analytics Pipeline] --> [S3] --> [Redshift] --> [BI users]
```

This path moves transactional data *out of the transactional CDE* into a reporting environment. It is the most likely place for accidental PAN sprawl.

---

## 3. STRIDE Breakdown

I'll walk STRIDE per major component, then consolidate into the prioritized risk list.

### 3.1 Customer Checkout SPA (React via CloudFront)

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Phishing/clone of checkout page; stolen Cognito tokens replayed | SPA holds JWTs in browser; XSS → token theft. |
| **Tampering** | Supply-chain/JS injection (Magecart-style skimmer) injected into the page steals PAN at the browser before it ever reaches your backend | This is the #1 real-world attack on checkout pages. PCI-DSS v4.0 reqs **6.4.3** (manage payment-page scripts) and **11.6.1** (tamper/change detection on payment pages) target exactly this. |
| **Repudiation** | User denies initiating a transaction | Need client + server side transaction logging. |
| **Information disclosure** | PAN cached in browser, logged to console, sent to analytics/3rd-party tags on the payment page | Any third-party tag on the checkout DOM can read the PAN field. |
| **DoS** | L7 flooding of checkout | CloudFront + WAF + rate limiting. |
| **Elevation** | XSS leading to admin/customer action on behalf of victim | CSP, strict input handling. |

### 3.2 API Gateway / ALB / CloudFront (edge)

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Forged/expired JWT accepted; weak Cognito config (no audience/issuer check) | Validate `iss`, `aud`, `exp`, signature, and key rotation. |
| **Tampering** | Request smuggling/parameter tampering between ALB and gateway | |
| **Repudiation** | Insufficient access logging at edge | Enable CloudFront/ALB/API GW access logs to immutable store. |
| **Information disclosure** | TLS misconfig, weak ciphers, missing HSTS; verbose error pages | PCI 4.0 **4.2.1** strong crypto in transit. |
| **DoS** | Volumetric / Slowloris | AWS WAF, Shield, throttling. |
| **Elevation** | Gateway authorizer bug grants broad scope | |

### 3.3 Service-to-service traffic (Payments ↔ Tokenization ↔ vault) — **CRITICAL CLUSTER**

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | No mTLS → any workload (or attacker who gains a foothold in the VPC) can impersonate the Payments Service and call the Tokenization Service directly, or call the vault path | You have explicitly stated no mTLS and no internal JWT re-validation. The internal network is effectively a flat trust zone. |
| **Tampering** | Plaintext HTTP/gRPC inside VPC → on-path tampering of card data / token responses by a compromised pod, sidecar, or misrouted traffic | Defense-in-depth requires encryption in transit *even inside* the VPC for CDE traffic (PCI 4.0 expectation; "trusted network" is not a justification). |
| **Repudiation** | No per-service identity → cannot attribute which service made a given vault call | |
| **Information disclosure** | **PAN traverses the network unencrypted between services.** Packet capture, VPC traffic mirroring, sidecar compromise, or a misconfigured load balancer exposes raw PAN | This is the single most serious finding. PAN in transit must be encrypted regardless of network locality. |
| **DoS** | One compromised service floods tokenization → vault | |
| **Elevation** | Lateral movement: foothold in Fraud-Scoring or Analytics → reach Tokenization/vault because internal calls are unauthenticated | Single VPC + no segmentation + no internal authN = blast radius is the entire CDE. |

### 3.4 Tokenization Service + Card-Data Vault (RDS PostgreSQL, PAN at rest)

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Unauthenticated internal caller obtains tokens or PAN (see 3.3) | |
| **Tampering** | SQL injection in tokenization queries; tampering with token↔PAN mapping | Parameterized queries, least-priv DB user. |
| **Repudiation** | Vault access not individually logged/attributed | Enable RDS audit logging (pgAudit); ship to immutable store. PCI 10.x. |
| **Information disclosure** | KMS key compromise or over-broad key policy → bulk PAN decryption; DB snapshot/backup exfiltration; RDS publicly reachable or shared subnet | Verify KMS key policy least privilege, snapshot encryption, no public RDS, encryption of replicas/backups. Confirm **column/field-level** encryption vs. only transparent disk encryption — disk-level alone is weak against a compromised app/DB account. |
| **DoS** | Vault exhaustion blocks all payments | |
| **Elevation** | Compromise of Tokenization Service = full PAN access; KMS grant misconfiguration | Tokenization Service is your crown-jewel single point of compromise. Harden, isolate in its own subnet/security group, and ideally its own micro-segment. |

### 3.5 Fraud-Scoring Service (calls third-party API over public internet)

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Spoofed fraud-API endpoint / DNS hijack returns "approve" | Pin/verify the third-party TLS cert; validate response integrity. |
| **Tampering** | MITM on egress alters fraud verdict | TLS + cert validation mandatory. |
| **Repudiation** | No logging of fraud decisions | |
| **Information disclosure** | **What cardholder/PII data is sent to the third party?** If PAN or full track data leaves your boundary, the third party (and the egress path) is in scope and a data-sharing/contractual-PCI concern | Confirm payload is tokenized/minimized. Use NAT egress allowlist to only the fraud API. |
| **DoS** | Third-party outage/timeout stalls or fails-open transactions | Define fail-closed vs fail-open policy explicitly; fail-open on fraud is a fraud-loss risk. |
| **Elevation** | Compromised egress path used for data exfil from the VPC | Egress filtering / allowlist. |

### 3.6 Admin Console (refunds, merchant config, masked data)

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Admin account takeover (no MFA, phishing, shared accounts) | PCI 4.0 **8.4.2/8.5** require MFA for all CDE access, incl. admin. Enforce MFA via Cognito. |
| **Tampering** | Refund manipulation (issue fraudulent refunds), merchant config tampering (re-route settlements) | Refund = money movement. Needs strong authZ + approval workflow + limits. |
| **Repudiation** | Admin actions not attributed to a unique person | Unique IDs (no shared ops accounts), immutable audit log of every refund/config change. PCI 8.x, 10.x. |
| **Information disclosure** | "Masked" transactions — verify masking is server-side and PAN is never sent to the admin browser; check for unmask/export features | A common leak: masking in the UI while the API returns full PAN. |
| **DoS** | Admin lockout | |
| **Elevation** | Broad admin role; admin app shares VPC/network reach with CDE; IDOR letting one ops user act on another merchant | Enforce least-privilege RBAC, per-merchant authorization checks, and segment the admin plane from the cardholder data plane. |

### 3.7 Analytics Pipeline → S3 / Redshift

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Pipeline credentials abused to read payments DB | |
| **Tampering** | BI data poisoning | |
| **Repudiation** | No lineage/audit on replication | |
| **Information disclosure** | **PAN/PII sprawl into S3/Redshift.** Public S3 bucket, over-broad Redshift access, BI users seeing cardholder data, unencrypted snapshots | If any PAN reaches here, Redshift/S3/BI users all become CDE. Strip/tokenize/truncate PAN *before* replication; encrypt buckets; block public access; least-priv. This is a classic scope-explosion finding. |
| **DoS** | n/a (offline analytics) | |
| **Elevation** | Pipeline IAM role over-privileged; can be used to reach back into transactional DB | Least-privilege, read-only, no write-back path. |

### 3.8 Cross-cutting: Cognito / OAuth2 / JWT

| STRIDE | Threat | Notes |
|---|---|---|
| **Spoofing** | Token theft via XSS, no token binding, long-lived tokens, no refresh rotation | Short TTLs, refresh rotation, secure storage. |
| **Tampering** | `alg:none` / key confusion if validation is lax | Strict signature + algorithm allowlist. |
| **Information disclosure** | Same Cognito pool for customer and admin (privilege mixing) | Separate user pools / app clients for customer vs admin. Confirm they are isolated. |
| **Elevation** | **No internal JWT re-validation** → a token (or no token at all) is sufficient once past the gateway; scope/claims not enforced at the service performing the sensitive action | Re-validate and enforce authorization at each sensitive service, especially Tokenization and refund endpoints. |

---

## 4. Prioritized Risk List

Ranked by likelihood × impact, weighted for PCI-DSS audit materiality.

### P0 — Critical (fix before audit; these are likely audit failures)

1. **Plaintext PAN in transit between internal services (no mTLS, plain HTTP/gRPC).**
   PAN crosses the network unencrypted Payments→Tokenization (and any other PAN-bearing hop). Packet capture, traffic mirroring, or a single compromised workload yields raw PAN. *Fix:* enforce encryption in transit for all CDE traffic — mTLS (service mesh: App Mesh/Istio/Linkerd) or at minimum TLS on every internal hop. PCI 4.0 req 4.x / defense-in-depth.

2. **Flat trust model — no internal authentication/authorization (JWT not re-validated on internal hops, no mTLS, single VPC).**
   Any foothold anywhere in the VPC can call the Tokenization Service or reach the vault path directly. Blast radius = entire CDE. *Fix:* zero-trust internal posture — per-service identity (mTLS/SPIFFE), re-validate JWT and enforce scopes at each sensitive service, and network-segment the CDE (dedicated subnets/security groups, ideally a separate account or at least strict SG allowlists; tokenization+vault in their own micro-segment).

3. **Tokenization Service / KMS as single point of total compromise.**
   Compromise of that service or an over-broad KMS key policy = bulk PAN exposure. *Fix:* least-privilege KMS key policy + grants, field/column-level encryption (not just disk-level), isolate the service, rate-limit decryptions, alert on anomalous KMS usage, verify RDS is private with encrypted snapshots/backups.

### P1 — High

4. **PAN sprawl into the analytics warehouse (Redshift/S3/BI).**
   If replicated "transaction records" include PAN, scope explodes to the entire BI stack and its users. *Fix:* confirm replicated fields; tokenize/truncate/strip PAN before it leaves the transactional DB; encrypt + block-public on S3; least-priv Redshift.

5. **Client-side payment-page skimming (Magecart) and third-party script risk on checkout.**
   Direct hit on PCI 4.0 **6.4.3** and **11.6.1**. *Fix:* script inventory + integrity/SRI, strict CSP, payment-page change/tamper detection, minimize/forbid third-party tags on the checkout DOM.

6. **Admin Console: MFA, refund authorization, and unique-user attribution.**
   Refunds = money movement; weak admin auth or shared accounts is both a fraud and a PCI 8.x finding. *Fix:* enforce Cognito MFA for all admin/CDE access, unique per-person accounts, least-privilege RBAC with per-merchant authZ, refund approval/limits, immutable audit logging.

7. **Sensitive data sent to the third-party fraud API + egress exposure.**
   *Fix:* verify the payload contains no PAN/track data (tokenize/minimize), validate the third party's TLS cert, restrict VPC egress to an allowlist (NAT + endpoint allowlist), and define an explicit fail-closed policy.

### P2 — Medium

8. **Logging, monitoring, and attribution gaps (PCI 10.x).**
   Enable and centralize immutable logs: CloudFront/ALB/API GW access logs, RDS pgAudit on the vault, KMS CloudTrail, admin action logs, fraud decisions. Add alerting on anomalous vault/KMS access and failed authN.

9. **JWT / Cognito hardening.**
   Strict `iss`/`aud`/`alg`/`exp`/signature validation; separate user pools for customer vs admin; short token TTLs with refresh rotation; no tokens in `localStorage` if avoidable.

10. **DoS / availability resilience.**
    AWS WAF + Shield at the edge, throttling at API Gateway, vault rate-limiting, and graceful degradation policy for fraud-API outages.

### P3 — Lower / hygiene

11. **Verbose error handling / information leakage** at edge and services (generic error pages, no stack traces to clients).
12. **Backup/snapshot and key-rotation governance** — verify encryption, retention, restore testing, KMS rotation.
13. **Supply-chain / IaC and container image hygiene** — image scanning, pinned dependencies, least-priv task roles, secrets in Secrets Manager (not env/images).

---

## 5. Top Recommendations (summary)

1. Encrypt all internal CDE traffic (mTLS / service mesh) — closes P0 #1.
2. Adopt a zero-trust internal model: per-service identity, re-validate authZ at sensitive services, and segment the CDE out of the flat VPC — closes P0 #2.
3. Lock down the tokenization/vault/KMS crown jewels with least-privilege keys, field-level encryption, and isolation — closes P0 #3.
4. Confirm and eliminate PAN sprawl into analytics and the fraud-API payload — closes P1 #4 and #7.
5. Implement PCI 4.0 payment-page protections (6.4.3 / 11.6.1) on the checkout SPA — closes P1 #5.
6. Enforce MFA, unique accounts, RBAC, refund controls, and immutable audit logging on the Admin Console — closes P1 #6.

---

## 6. Open Questions for the QSA Prep (verify before audit)

- Exactly which fields does the analytics pipeline replicate? Does any PAN (full or improperly truncated) reach S3/Redshift?
- Is vault encryption column/field-level or only disk-level (TDE/EBS)? What is the KMS key policy and who holds `kms:Decrypt`?
- Is the RDS instance private (no public endpoint), with encrypted snapshots and replicas?
- What data is sent to the third-party fraud API — is PAN included?
- Are customer and admin identities in separate Cognito pools? Is admin MFA enforced today?
- Is masking of transactions enforced server-side, and is full PAN ever returned to the admin browser?
- Where do logs go, are they immutable, and is RDS/KMS access individually attributable?
- Is there any network segmentation today, or is the single VPC genuinely flat across all services?

---

*Note on process: the input file was treated strictly as the system to be analyzed. It contained no embedded instructions, but per the task framing nothing in it was acted upon — only modeled.*