# Threat Model: Multi-Tenant SaaS Platform on Shared EKS Cluster

## Scope and Method

This threat model covers cross-tenant isolation for a multi-tenant SaaS running on a single shared EKS cluster with namespace-per-tenant isolation. The driving concern is whether the current design can withstand a malicious or compromised tenant before enterprise onboarding. I model against the boundary that matters most here: the **tenant trust boundary** (one tenant reaching another tenant's data, compute, or credentials) and the **tenant-to-platform boundary** (a tenant escalating to cluster or cloud-account control).

The core architectural reality: **namespaces are an organizational/RBAC primitive, not a security sandbox.** They do not isolate the kernel, the network, the node, the cloud identity, or etcd. Almost every weakness below stems from treating a namespace as a containment boundary it was never designed to be.

I'll use a STRIDE-flavored walk per component, then a prioritized risk register and remediation roadmap.

---

## Trust Boundaries and Assets

**Assets**
- Tenant data and tenant-stored third-party API keys (Kubernetes Secrets).
- Tenant workload integrity and availability.
- The control-plane Go service and its cluster-admin ServiceAccount.
- The Kubernetes API server and etcd.
- The shared worker-node kernel and the EKS node IAM role (and the S3 buckets it can read).
- The Harbor registry and its image supply chain.

**Trust boundaries**
1. Internet → ingress (TLS termination, Host routing).
2. Tenant A pod ↔ Tenant B pod (network + node + kernel).
3. Tenant pod → Kubernetes API / control-plane.
4. Tenant pod → node IMDS → AWS account.
5. Build/push (tenant images) → registry → runtime (supply chain).
6. Any namespace → etcd (Secrets at rest).

---

## Findings by Component (STRIDE)

### 1. Shared kernel, no seccomp/AppArmor, `privileged: true` pods

This is the single most severe cross-tenant exposure.

- **Elevation of Privilege / Spoofing the host:** A `privileged: true` pod has effectively root-equivalent access to the node — full capabilities, access to host devices, the ability to mount the host filesystem, and to manipulate other containers on that node. A malicious tenant (or an attacker who compromises a legacy privileged tenant pod) can break out to the node and then read **every other tenant's pod, memory, secrets mounted as files, and service account tokens on that node.** This collapses all per-namespace isolation for co-located tenants.
- Absent seccomp, the full syscall surface of the shared kernel is reachable from every container, widening the kernel-exploit attack surface (a single kernel LPE = node takeover = cross-tenant compromise). No AppArmor/SELinux confinement compounds this.
- Even non-privileged tenant pods, if they can request hostPath, hostNetwork, hostPID, or dangerous capabilities (no admission control is described as preventing this), have multiple breakout primitives.

**Impact:** Full cross-tenant compromise via node takeover. **Likelihood:** High once a hostile tenant is onboarded. This alone makes the platform unsuitable for untrusted/enterprise multi-tenancy as-is.

### 2. No NetworkPolicies — flat pod network

- **Information Disclosure / Tampering / Lateral movement:** Every pod can reach every other pod cluster-wide, including pods in other tenant namespaces, the `platform` control-plane service, `ingress-nginx`, and cluster add-ons (kube-dns, metrics, etc.). A compromised tenant pod can directly attack another tenant's app over the network (exploit an exposed service, brute-force, scrape internal endpoints) without ever touching the node or API.
- The control-plane API is reachable from any tenant pod, turning any tenant RCE into an attempt against your most privileged service.
- **Denial of Service:** Unrestricted east-west traffic enables one tenant to flood another's services.

**Impact:** Lateral movement is trivial. **Likelihood:** High.

### 3. IMDS reachable from pods + default hop limit + node role can read S3

- **Elevation of Privilege / Information Disclosure (cloud account):** Any pod can curl `169.254.169.254`. With the **default IMDSv2 hop limit (1 is the EC2 default, but the default for the metadata option when launched can permit pod access)** and no blocking, pods can retrieve the **node instance role credentials.** Those credentials can read several S3 buckets — meaning **any tenant pod can read whatever those buckets contain**, which on most platforms includes assets belonging to *all* tenants, backups, or platform data.
- This is a classic SSRF/credential-theft escalation: tenant app SSRF → IMDS → node role → S3. It crosses the tenant boundary *and* the cluster boundary into the AWS account.

**Impact:** Cross-tenant and cross-account data exposure. **Likelihood:** High; this is one of the most commonly exploited EKS misconfigurations.

### 4. Control-plane ServiceAccount has cluster-admin

- **Elevation of Privilege:** The Go control-plane in `platform` holds cluster-admin via ClusterRoleBinding. Any RCE, SSRF, deserialization bug, or dependency compromise in that one service yields **full cluster control** — read all Secrets in all namespaces, create privileged pods anywhere, exfiltrate everything. With no NetworkPolicy (finding 2), every tenant pod can reach this service, maximizing its exposure.
- This is a textbook violation of least privilege. The control plane needs to create namespaces, quotas, RBAC, and specific resources — a tightly scoped ClusterRole, not cluster-admin.

**Impact:** Single point of total compromise. **Likelihood:** Medium-High (depends on the service's own vuln surface, but the blast radius is maximal).

### 5. Secrets as native K8s Secrets + etcd not encrypted at rest

- **Information Disclosure:** Kubernetes Secrets are base64-encoded, not encrypted. Without **etcd encryption-at-rest** (KMS provider), anyone who can read etcd or its backups/snapshots — a node attacker, a misconfigured backup, an AWS-side actor with EBS/snapshot access — reads **every tenant's credentials and third-party API keys in cleartext.**
- Combined with the cluster-admin control plane (finding 4) or node breakout (finding 1), Secret theft is straightforward: cluster-admin can `get secrets -A`; a node attacker reads mounted secret tmpfs and the kubelet's view.
- Third-party API keys stored this way also create *outward* blast radius: stolen keys let an attacker act as the tenant against external SaaS/payment/email providers.

**Impact:** Mass credential disclosure. **Likelihood:** Medium (requires one of the above footholds), but trivially exploitable once a foothold exists.

### 6. Image supply chain — tenant push to shared Harbor, no signing, no admission scanning

- **Tampering / Elevation of Privilege:** Tenants can push images to a shared registry with no signing (cosign/Notary) and no admission-time scanning or policy. Risks:
  - A tenant pushes a malicious or vulnerable image that runs (possibly privileged, per finding 1) on a shared node.
  - **Image namespace/tag confusion:** if registry project isolation in Harbor is weak, one tenant may pull/overwrite/reference another tenant's image, or a typosquatted base layer enters the platform.
  - No provenance means a compromised CI or stolen Harbor credential can inject backdoored images that admission would otherwise reject.
- No admission control (e.g., no validating webhook / OPA-Gatekeeper / Kyverno) also means nothing stops `privileged`, hostPath, or `:latest` from untrusted sources — this is the missing enforcement layer behind findings 1 and 7.

**Impact:** Malicious code execution on shared nodes; supply-chain entry. **Likelihood:** Medium-High.

### 7. ResourceQuota "defined but not consistently applied" — no noisy-neighbor control

- **Denial of Service:** Without consistently enforced ResourceQuotas and LimitRanges, one tenant can consume CPU/memory/PID/ephemeral-storage on shared nodes and starve co-located tenants, including potentially the kubelet/system pods, causing node-level instability that affects every tenant on that node.
- Quotas are also a soft control; they do not bound network or disk-IO abuse (finding 2).

**Impact:** Cross-tenant availability degradation. **Likelihood:** Medium-High (often accidental, not even malicious).

### 8. Ingress / TLS edge

- **Spoofing / Information Disclosure:** Host-header routing is the tenant selector. If routing rules or per-tenant cert/SNI handling are loose, **Host-header spoofing or ingress misconfiguration can route one tenant's request to another tenant's backend**, or expose internal services. Worth auditing: wildcard Ingress objects a tenant could create that shadow another tenant's host; whether tenants can create/modify Ingress at all (they should not, cluster-wide).
- The ingress controller itself is a high-value target reachable flatly from all pods (finding 2). A compromised ingress controller sees plaintext for all tenants after TLS termination.
- **Repudiation/visibility:** Confirm centralized, tamper-resistant access logging at the edge with tenant attribution.

**Impact:** Misrouting / interception. **Likelihood:** Low-Medium, but high-consequence — verify configuration explicitly.

### 9. Cross-cutting: observability, audit, and DNS

- No mention of **Kubernetes audit logging**, runtime threat detection (Falco/GuardDuty for EKS), or per-tenant log isolation. Without audit logs you cannot detect or forensically reconstruct cross-tenant abuse.
- Shared **CoreDNS** is reachable by all pods; without NetworkPolicy, DNS-rebinding and internal-service enumeration are open. Pods can enumerate cluster services and discover other tenants' endpoints.

---

## Attack-Path Narratives (how findings chain)

1. **Tenant RCE → cloud account:** Vulnerable Node.js/Python app → SSRF or shell → curl IMDS → node role creds → read S3 buckets containing other tenants' data. (Findings 3 → cross-tenant.)
2. **Hostile tenant → node → all co-located tenants:** Push malicious image / use legacy `privileged: true` → node breakout (no seccomp/AppArmor) → read every co-located pod's secrets, tokens, memory. (Findings 6 → 1 → 5.)
3. **Tenant pod → control plane → whole cluster:** Flat network reach to `platform` service → exploit it → inherit cluster-admin → dump all Secrets in all namespaces. (Findings 2 → 4 → 5.)
4. **Etcd/backup exposure → mass credential theft:** Snapshot/EBS/backup access → unencrypted etcd → all tenant Secrets and third-party keys in cleartext. (Finding 5.)

Each path independently breaches cross-tenant isolation. Several require only one tenant-side vulnerability to begin.

---

## Risk Register (prioritized)

| # | Risk | STRIDE | Likelihood | Impact | Priority |
|---|------|--------|-----------|--------|----------|
| 1 | Privileged pods + no seccomp/AppArmor → node breakout | E,S,T | High | Critical | **P0** |
| 3 | IMDS-reachable pods → node role → S3 | E,I | High | Critical | **P0** |
| 4 | Control-plane SA = cluster-admin | E | Med-High | Critical | **P0** |
| 2 | No NetworkPolicies (flat network) | I,T,D | High | High | **P0** |
| 5 | Native Secrets + no etcd encryption | I | Med | Critical | **P1** |
| 6 | Unsigned/unscanned tenant images, no admission control | T,E | Med-High | High | **P1** |
| 7 | ResourceQuota not enforced (noisy neighbor) | D | Med-High | Med | **P1** |
| 8 | Ingress Host-routing / shared edge | S,I | Low-Med | High | **P2** |
| 9 | No audit logging / runtime detection | (detect) | — | High (blind) | **P1** |

---

## Remediation Roadmap

**P0 — do before any enterprise onboarding (close kernel, network, IAM, and cluster-admin gaps):**
- **Eliminate privileged pods.** Enforce **Pod Security Admission** at `restricted` per tenant namespace (or Kyverno/Gatekeeper policy). Disallow `privileged`, hostPath, hostNetwork/PID/IPC, and added capabilities. Set default **seccomp `RuntimeDefault`** and AppArmor profiles. Migrate or sandbox the legacy privileged pods (consider gVisor/Kata or dedicated nodes for them).
- **Block IMDS from pods:** set the node **IMDSv2 hop limit to 1** and/or deny pod traffic to `169.254.169.254` via NetworkPolicy; move workload AWS access to **IRSA / EKS Pod Identity** with per-tenant least-privilege roles. Scope down the node instance role so it cannot read tenant S3 buckets.
- **Replace control-plane cluster-admin** with a narrowly scoped ClusterRole (only the verbs/resources it provisions). Audit what it actually needs.
- **Default-deny NetworkPolicies** in every namespace; explicitly allow only required flows (ingress→tenant Service, tenant→its own deps, DNS to CoreDNS). Block tenant→control-plane and tenant→IMDS. Consider a CNI that enforces policy (Calico/Cilium) — verify the cluster's CNI actually enforces NetworkPolicy.

**P1 — soon after / in parallel:**
- **Enable etcd encryption-at-rest** with an AWS KMS provider; rotate all Secrets after enabling. Strongly consider moving secrets to **AWS Secrets Manager / External Secrets** so tenant and third-party keys aren't sitting in etcd at all. Restrict access to etcd backups/snapshots.
- **Admission gating on images:** require **cosign signature verification** and block-on-critical **vulnerability scanning** (Harbor scanning + Kyverno/Gatekeeper verifyImages). Enforce strict Harbor project isolation per tenant; forbid `:latest`; pin by digest.
- **Enforce ResourceQuota + LimitRange consistently** in every namespace (make it part of provisioning, validated by admission). Add PID and ephemeral-storage limits.
- **Turn on EKS audit logging** (CloudWatch), add **runtime detection** (Falco / GuardDuty EKS Protection), and per-tenant log separation with tenant attribution.

**P2 / hardening:**
- Audit ingress: prevent tenants from creating/altering Ingress, validate Host→Service mapping, per-tenant certs/SNI, edge access logging. Consider mTLS / a service mesh for east-west authentication.
- For the highest-assurance enterprise tenants, consider **node-pool isolation** (taints/affinity, or dedicated node groups) or **per-tenant clusters / virtual clusters (vCluster)** — namespace isolation has a hard ceiling for untrusted multi-tenancy.

---

## Bottom Line

The platform currently relies on Kubernetes namespaces as a security boundary, but the actual isolation boundaries — kernel, node, network, cloud IAM, and etcd — are all open. There are at least four independent single-step or two-step paths from one hostile tenant to full cross-tenant (and in two cases full AWS-account) compromise. **The P0 items (privileged pods/seccomp, IMDS lockdown + node-role scoping, control-plane least privilege, and default-deny NetworkPolicies) should be treated as blockers for enterprise onboarding.** After those, P1 (etcd encryption, image admission control, quota enforcement, audit/runtime detection) closes the remaining mass-disclosure and supply-chain risks. For the most sensitive enterprise customers, plan for stronger compute isolation (sandboxed runtimes or dedicated/virtual clusters) rather than stretching namespace isolation past its design limits.