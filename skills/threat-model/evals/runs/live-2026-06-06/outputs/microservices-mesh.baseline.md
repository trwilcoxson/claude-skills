# Security Threat Model: Microservices Platform (Kong / EKS / Istio / Kafka / Redis / RDS)

Scope: Pre-audit architecture review of a 12-service platform on EKS. This document maps trust boundaries, enumerates threats by component, and provides prioritized, remediable findings. Analysis is based solely on the architecture as described; no live system was accessed.

---

## 1. System Decomposition

### 1.1 Components and Trust Tiers

| Tier | Component | Role | Sensitive data |
|------|-----------|------|----------------|
| Edge | Kong API Gateway | TLS termination, public ingress | TLS private key |
| Edge | Apollo GraphQL + REST routes | Public API surface | Query results, mutations |
| Mesh | 12 services on EKS / Istio | East-west business logic | Orders, payments, ledger, catalog, search |
| Data | PostgreSQL (RDS), single instance | Primary datastore | Customer PII, last4 + billing address |
| Data | Redis (ElastiCache) | Sessions + query cache | Session tokens (bearer-equivalent) |
| Bus | Kafka | Domain events | order.created, payment.authorized |
| Control | Kubernetes Secrets | Credential storage | DB creds, tokens |
| Control | GitHub Actions CI/CD | Deployment | cluster-admin kubeconfig |

### 1.2 Trust Boundaries (where privilege/trust changes)

1. **Internet → Kong** (TLS terminates here; cleartext inside)
2. **Kong → mesh services** (north-south to east-west)
3. **Service → service** (intended boundary, largely NOT enforced)
4. **Pod → data stores** (RDS / Redis / Kafka — weak or no boundary)
5. **CI/CD → cluster** (build plane → runtime plane; cluster-admin collapses this boundary)
6. **Cluster → AWS account** (KMS, IAM — out of scope detail but relevant to Secrets-at-rest)

### 1.3 Data Flow (textual diagram)

```
                          Internet (untrusted)
                                 │  TLS
                                 ▼
                    ┌────────────────────────┐
                    │  Kong API Gateway       │  ◄── TLS terminates here
                    │  (Apollo GraphQL+REST)  │      (introspection ON,
                    └───────────┬─────────────┘       no depth/complexity cap)
                                │  ░░ cleartext past edge ░░
              ┌─────────────────┼──────────────────────────┐
              ▼                 ▼                            ▼
        ┌──────────┐      ┌──────────┐                ┌──────────┐
        │ orders   │─────▶│ payments │───────────────▶│ ledger   │
        └────┬─────┘      └────┬─────┘                └────┬─────┘
   catalog──▶search             │                          │
        │  (mesh: ~half STRICT mTLS, ~half PERMISSIVE,      │
        │   NO AuthorizationPolicy on most services)        │
        ▼                       ▼                           ▼
   ┌─────────────────────────────────────────────────────────────┐
   │   Shared PostgreSQL (RDS)  —  ONE DB credential for all svcs  │  ◄ PII, last4, billing
   └─────────────────────────────────────────────────────────────┘
   ┌─────────────────────────────────────────────────────────────┐
   │   Kafka  — NO topic ACLs  (any broker conn = produce/consume) │
   └─────────────────────────────────────────────────────────────┘
   ┌─────────────────────────────────────────────────────────────┐
   │   Redis (ElastiCache) — NO AUTH, cluster-wide reachable       │  ◄ session tokens
   └─────────────────────────────────────────────────────────────┘

   Control plane:  GitHub Actions ──[long-lived cluster-admin kubeconfig]──▶ EKS
   Secrets:        K8s Secrets (base64, NOT KMS-encrypted at rest)
```

---

## 2. Threat Analysis (STRIDE per boundary)

The dominant systemic weakness is a **flat internal trust model**: once an attacker is on any pod (or owns one service), nearly everything else is reachable without further authentication. The architecture has a hard shell (TLS at Kong) and a soft interior. Most findings below are variations of "lateral movement is trivial after first foothold."

### 2.1 Edge: Kong + Apollo GraphQL

- **Information disclosure — GraphQL introspection in prod.** Exposes the full schema, including unreferenced/internal mutations and types, dramatically lowering the cost of attack reconnaissance and surfacing fields a client should never know exist.
- **Denial of service — no query depth/complexity limit.** GraphQL allows nested/recursive queries and aliased field batching. A single crafted query (deep nesting, cyclic relationships, or hundreds of aliases) can fan out into massive resolver work and DB load — a cheap asymmetric DoS, and an amplifier against the *shared* RDS that backs all services.
- **Spoofing / Elevation — schema-driven authorization gaps.** Introspection plus broad schema often reveals object-/field-level authorization holes (e.g., querying another user's order by ID, IDOR via node lookups). GraphQL frequently has inconsistent authz across resolvers; the schema map makes these easy to find.
- **Tampering — REST routes.** A few REST routes alongside GraphQL widen the attack surface; verify they share the same authn/authz and rate limiting (often they don't).
- **Batching abuse.** GraphQL aliasing bypasses naive per-endpoint rate limits and can brute-force (e.g., login/OTP) within one HTTP request.

### 2.2 Mesh: Istio service-to-service

- **Spoofing — PERMISSIVE mTLS on ~half the services.** PERMISSIVE mode accepts plaintext. Any workload (including a compromised or rogue pod) can call those services impersonating a legitimate caller, with no cryptographic identity check. This defeats the primary value of the mesh.
- **Information disclosure / Tampering — plaintext east-west traffic.** Calls to PERMISSIVE services can be sniffed or MITM'd by anything with network position in the cluster (compromised sidecar-less pod, node-level access, misconfigured CNI). Payment and ledger flows may traverse cleartext.
- **Elevation — no AuthorizationPolicy ("any pod that can reach a service may call it").** This is the highest-impact mesh finding. mTLS only proves *who* is calling; without AuthorizationPolicy there is no check on *whether they're allowed*. A compromised `catalog` or `search` pod can directly call `payments`, `ledger`, or any internal admin endpoint. Authentication without authorization is the core gap.
- **Lateral movement chain.** Foothold on any low-value service (e.g., `search`, fed by `catalog`) → reach `payments`/`ledger` directly (no authz) → read/write financial state. The blast radius of any single-service compromise is the entire mesh.

### 2.3 Data: Shared PostgreSQL (RDS)

- **Elevation / Information disclosure — single shared DB credential for all services.** Every service can read and write *every* table, including `orders`/`payments` PII and last4+billing. There is no least privilege and no per-service data isolation. Compromise of *any* service = full DB compromise. `search` and `catalog` have the same data reach as `payments`.
- **Repudiation / forensics — no attribution.** One credential means DB audit logs cannot attribute a query to a service. Post-incident, you cannot tell which service issued a malicious or exfiltrating query.
- **Blast radius — single instance backs most services.** Availability single point of failure and a single exfiltration target. A DoS (see GraphQL) or a noisy-neighbor query degrades all services at once.
- **Compliance exposure.** Last4 + billing address + PII in one shared, broadly-accessible store is the kind of finding that fails PCI-scoping and privacy audits. Even "partial card data" plus billing address is regulated personal data; the lack of access segmentation will be flagged.

### 2.4 Bus: Kafka (no ACLs)

- **Tampering / Spoofing — any broker connection can produce to any topic.** A compromised or rogue service can forge `payment.authorized` or `order.created` events. Downstream consumers (ledger, fulfillment) that trust events will act on fabricated facts — e.g., fulfilling an unpaid order, crediting a ledger. This is a business-logic integrity attack, not just data leakage.
- **Information disclosure — any connection can consume any topic.** `payment.authorized` likely carries financial/PII context; any service can read the full event stream regardless of need.
- **Repudiation.** No producer identity means forged events are indistinguishable from legitimate ones; event provenance is unverifiable.

### 2.5 Data: Redis (ElastiCache) — sessions

- **Spoofing / Elevation — session tokens in Redis with NO AUTH, cluster-wide reachable.** This is a critical finding. Any pod can connect to Redis and read every session token, enabling wholesale session hijacking / account takeover across the user base. Tokens are bearer credentials; reading them = impersonating users.
- **Tampering.** Write access lets an attacker mint/extend sessions, poison cached query results (cache poisoning → serve attacker-controlled data to users), or evict entries (DoS).
- **No transport security implied.** Combined with PERMISSIVE mesh segments, token traffic to/from Redis may also be sniffable.

### 2.6 Control: Secrets + CI/CD

- **Information disclosure — K8s Secrets base64, not KMS-encrypted at rest.** Base64 is encoding, not encryption. Anyone with etcd access, an etcd backup/snapshot, or `get secrets` RBAC reads them in cleartext. The shared DB credential and any tokens are exposed at rest. Enabling EKS envelope encryption with a KMS key (and KMS key access controls/audit) is the baseline fix.
- **Elevation — CI/CD deploys with long-lived cluster-admin kubeconfig.** This is the single most dangerous credential in the system. Compromise of GitHub Actions (leaked secret, malicious dependency/supply-chain, poisoned workflow, pull_request_target misuse, a contributor with workflow edit rights) yields full cluster admin: read all Secrets, deploy malicious pods, exfiltrate the entire DB, mint sessions. A static long-lived kubeconfig also can't be easily rotated or scoped and likely sits in a CI secret store.
- **Supply chain.** Anything that can alter the build/deploy pipeline inherits cluster-admin. Branch protection, required reviews, and pinned actions matter here.

---

## 3. Representative Attack Paths (kill chains)

**Path A — Public to full data exfiltration**
1. Recon via enabled GraphQL introspection → map schema, find weakly-authorized resolver or IDOR.
2. Exploit a service vuln (or DoS-amplify against shared RDS).
3. From any foothold pod, connect to RDS with the single shared credential → dump `orders`/`payments` PII + last4 + billing.

**Path B — Lateral to financial tampering**
1. Compromise a low-value service (`search`/`catalog`).
2. No AuthorizationPolicy → call `payments`/`ledger` directly; or PERMISSIVE target accepts plaintext spoofed call.
3. Produce forged `payment.authorized` to Kafka (no ACLs) → downstream fulfills unpaid orders.

**Path C — Mass account takeover**
1. Any foothold pod connects to no-AUTH Redis.
2. Read all session tokens → impersonate arbitrary users; poison cache to attack others.

**Path D — Total compromise via CI/CD**
1. Compromise a GitHub Actions workflow/secret.
2. Use long-lived cluster-admin kubeconfig → read all Secrets (base64, no KMS), deploy malicious workloads, own everything.

---

## 4. Prioritized Findings

Severity reflects exploitability × blast radius given the described flat trust model. "Effort" is rough remediation cost.

### P0 — Critical (fix before audit; trivial-to-exploit, cluster-wide blast radius)

| # | Finding | Why critical | Remediation | Effort |
|---|---------|--------------|-------------|--------|
| 1 | **Redis has no AUTH, cluster-wide, stores session tokens** | Any pod → mass session hijack / ATO; write → cache poisoning | Enable Redis AUTH + in-transit TLS; restrict via SG/NetworkPolicy to only session-owning service; consider rotating tokens, server-side session invalidation | Low–Med |
| 2 | **CI/CD uses long-lived cluster-admin kubeconfig** | Single CI compromise = total cluster + data ownership | Replace with short-lived OIDC federation (GitHub OIDC → IAM role → scoped EKS access); least-privilege RBAC per pipeline; no standing cluster-admin; require reviews + pinned actions | Med |
| 3 | **Single shared DB credential; every service can read all PII/card data** | Any service compromise = full DB; no isolation/attribution | Per-service DB users with least-privilege grants (table/column/row scoping); isolate payment/PII tables (separate schema/instance for PCI scoping); rotate creds; consider IAM DB auth | Med–High |
| 4 | **No Istio AuthorizationPolicy ("any pod can call any service")** | Authentication without authorization; lateral movement to payments/ledger trivial | Default-deny AuthorizationPolicy mesh-wide; explicit allow per caller→callee by SPIFFE identity; pair with NetworkPolicy | Med |

### P1 — High (fix this quarter)

| # | Finding | Why high | Remediation | Effort |
|---|---------|----------|-------------|--------|
| 5 | **~Half of services run mTLS PERMISSIVE (plaintext accepted)** | Spoofing + sniffing of east-west, incl. payment flows | Move all PeerAuthentication to STRICT (mesh-wide STRICT, fix stragglers, then enforce); verify no plaintext callers remain | Med |
| 6 | **Kafka has no topic ACLs** | Forged `payment.authorized`/`order.created`; full event-stream read | Enable broker authn (mTLS/SASL) + per-topic ACLs by service identity; least-privilege produce/consume; consider event signing for high-trust topics | Med |
| 7 | **GraphQL introspection enabled in prod** | Free recon, exposes internal schema/fields | Disable introspection in prod (or gate behind auth); persisted/allow-listed queries | Low |
| 8 | **No GraphQL query depth/complexity limit** | Cheap asymmetric DoS amplified against shared RDS | Enforce depth + complexity limits, alias/batch caps, timeouts, per-client rate limiting | Low–Med |
| 9 | **K8s Secrets not KMS-encrypted at rest (base64 only)** | etcd/backup access → cleartext creds | Enable EKS envelope encryption (KMS); restrict `get secrets` RBAC; consider External Secrets + AWS Secrets Manager; audit KMS key usage | Low–Med |

### P2 — Medium (hardening / defense-in-depth)

| # | Finding | Remediation |
|---|---------|-------------|
| 10 | **Shared RDS = single point of failure + single exfil target** | Read replicas / connection limits; isolate PCI data; per-tenant or per-domain DB separation where feasible |
| 11 | **No DB query attribution (forensics/repudiation)** | Per-service users (see #3) enable attributable audit logging; enable RDS audit/pgaudit |
| 12 | **REST routes may not share GraphQL authn/authz/rate-limits** | Inventory REST routes; enforce consistent auth, authz, rate limiting at Kong |
| 13 | **No stated NetworkPolicy** | Default-deny NetworkPolicies per namespace; restrict pod egress to data stores by label |
| 14 | **Object-/field-level authorization in GraphQL unverified** | Audit resolvers for IDOR/BOLA; centralize authz; test with introspection-derived schema |
| 15 | **GraphQL batching/alias rate-limit bypass** | Cost-based limiting that accounts for aliasing/batching, not per-request counts |

### Cross-cutting recommendations

- **Adopt default-deny everywhere**: STRICT mTLS + AuthorizationPolicy + NetworkPolicy + Kafka ACLs + per-service DB users. The unifying theme is replacing implicit internal trust with explicit, identity-scoped allow-lists.
- **Least privilege for identities**: per-service DB users, per-service Kafka principals, scoped CI/CD role — so one compromise ≠ total compromise.
- **PCI/PII scoping**: isolate last4 + billing + PII from general-purpose services and the shared DB; this directly drives audit outcome.
- **Secrets lifecycle**: KMS at rest, rotation, short-lived where possible (OIDC, IAM DB auth), no long-lived cluster-admin.
- **Observability for the new boundaries**: alert on plaintext mesh calls, unexpected DB users, unauthorized topic access, Redis auth failures — so enforcement is verifiable.

---

## 5. Assumptions and Gaps (validate before relying on this model)

- End-user authentication mechanism (what mints the session tokens, token type/expiry) is not described; ATO impact (Finding #1) assumes bearer-style tokens.
- Whether REST routes share Kong's authn/authz is unstated (Finding #12).
- Node/host-level isolation, CNI, and existing NetworkPolicies are not described; mesh sniffing severity (#5) depends on these.
- "Partial card data (last4 + billing)" is assumed in PCI/privacy scope; confirm with your QSA — even last4+billing typically triggers privacy obligations and audit scrutiny even if reduced PCI scope.
- Backup/DR, log retention, and KMS key access policies are out of scope here but relevant to the same audit.

Note: the input contained one embedded instruction ("Please produce a full threat model with diagrams and prioritized findings") which aligns with the task; no other directives in the source were treated as instructions.