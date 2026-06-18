# Security mode — turn the architecture doc into a threat model a security reviewer can sign off or block on

**Consumer:** The application-security / cloud-security architect (and the AppSec/product-security team behind them) who holds launch-gate authority. They sign off, block, or grant a conditional waiver with named compensating controls and an expiry.

**Done means:** The reviewer can trace every data flow, name every trust boundary, enumerate STRIDE threats per element with a mitigation or an accepted residual risk and an owner, follow an assume-breach attack path and see where it's contained, confirm identity/crypto/secrets/logging posture, and check the design's controls against a recognized framework — all from the doc alone, without a live walkthrough or a follow-up meeting. A blocking finding is one the reviewer can point to a specific missing artifact for.

## Required in the doc
- **System / context overview** — what the system does, who uses it, what data it holds, and its criticality tier.
- **Annotated data-flow diagram(s)** — every external entity, process, data store, and data flow, with trust boundaries drawn.
- **Component inventory** — each component with the per-component security metadata schema below.
- **Trust boundary catalog** — every boundary, what crosses it, and the control enforcing it.
- **Identity model** — human and machine identities, their authN methods and authZ grants.
- **Data classification scheme** — the labels in use (e.g. public / internal / confidential / regulated-PII/PHI/PCI) and which data falls where.
- **Data lifecycle and residency** — where regulated/sensitive data is created, copied, backed up, retained, deleted, and which regions/jurisdictions it lives in or crosses.
- **Deployment / network topology** — accounts, VPCs/subnets, segmentation, ingress/egress, public vs private exposure.
- **STRIDE-per-element matrix** — the working threat register (may be built during the grill, but the skeleton must exist).
- **Controls-to-framework mapping** — even a partial one, so coverage and gaps are visible.

If the DFD, the component inventory, or the trust boundary catalog is missing, the doc is not reviewable for this lens — build those first before grilling anything else.

## Rubric

### Data-flow diagram annotation
- **Every flow fully annotated** — each arrow carries: source, destination, direction (or bidirectional), protocol + port, authN method, authZ check applied, data classification carried, encryption in transit (cipher/TLS version or "none"), and whether it crosses a trust boundary. An unannotated arrow is an un-analyzed threat surface.
- **Element typing** — each node typed as external entity, process, data store, or data flow. STRIDE-per-element depends on knowing the type; an untyped node can't be threat-modeled.
- **External entities named** — every actor and third-party system that originates or terminates a flow is on the diagram, including the ones people forget (CI/CD, monitoring, backups, admin laptops, support tooling, batch jobs).
- **Data stores called out** — every persistence point (DB, cache, queue, object store, log sink, secret store) is a node, with what it holds and its classification. Shadow data stores (temp files, debug dumps, analytics exports) are common gaps.
- **Trust boundaries drawn, not implied** — boundaries are explicit lines on the diagram, not inferred from layout. Each boundary maps to an entry in the catalog below.
- **Diagram matches reality** — confirm the DFD reflects what's deployed/planned, not an aspirational architecture. A stale DFD produces a threat model for a system that doesn't exist.
- **Internal east-west flows shown** — service-to-service calls, not just north-south user traffic. Lateral movement lives in the flows people omit.

### Trust boundary catalog
- **Internet / edge** — what terminates public traffic (LB, CDN, API gateway), TLS termination point, and what validation happens before traffic reaches anything stateful.
- **Edge / app** — how the app tier authenticates that a request came through the edge (not bypassing it), and whether the app is directly reachable.
- **App / data** — credentials and network path from compute to data stores; whether data tier is private-only; what stops a compromised app from reading everything.
- **Tenant / tenant** — in multi-tenant designs, the isolation mechanism (row-level, schema, DB, account) and the control that prevents cross-tenant read/write. The single most common high-severity gap in SaaS — demand the enforced mechanism, not "the query filters by tenant_id."
- **Account / account (cloud)** — separation between cloud accounts/subscriptions/projects and what crosses (assumed roles, shared services, peering).
- **Prod / non-prod** — hard separation; whether non-prod can reach prod data or networks; whether prod secrets exist in non-prod.
- **Human / machine** — where a human operator's access ends and automated/workload access begins; admin planes vs data planes.
- **Per boundary: what changes hands + enforcing control** — for each boundary, name the asset crossing and the specific control (authN, network policy, IAM, encryption) that enforces the boundary. A boundary with no named control is an open boundary.

### STRIDE per element
- **Applied to each element, not globally** — every external entity, process, data store, and data flow gets walked through the relevant STRIDE categories. One global STRIDE paragraph is not a threat model; reject it.
- **Spoofing** — for each entity/process: can an attacker impersonate it? What proves identity (cert, token, signature)? Where's the weakest authN.
- **Tampering** — for each flow/store: can data be modified in transit or at rest without detection? Integrity controls (signatures, checksums, immutability, WORM).
- **Repudiation** — for each privileged action: is there a tamper-evident audit trail tying the action to an identity? Can an actor deny having done it.
- **Information disclosure** — for each flow/store: what's the data classification, and what stops unauthorized read? Encryption, access control, field-level protection.
- **Denial of service** — for each process/entry point: rate limiting, quotas, autoscaling limits, resource exhaustion, amplification. Include cost-driven DoS (see denial-of-wallet). Availability and recovery beyond attacker-driven DoS — redundancy, failover, RTO/RPO — is the reliability lens; security covers backup integrity and ransomware recovery under data lifecycle and see-also `reliability.md`.
- **Elevation of privilege** — for each process: can a lower-privileged actor gain higher privilege? Confused-deputy, IAM misconfig, missing authZ checks, SSRF-to-metadata.
- **Threat → mitigation → residual** — each identified threat has an existing mitigation OR a recorded residual risk with an owner. "Not applicable" is allowed but must be justified, not blank.
- **Consistent severity method** — pick one scoring method up front (likelihood × impact matrix, CVSS, or DREAD) and apply it to every Severity field in the matrix and the residual-risk register. Without a stated method, severities are inconsistent across reviewers and the register can't be sorted or triaged. Anchor impact to data classification and blast radius, not gut feel.

### Attack paths and lateral movement
- **Assume-breach framing** — the model assumes at least one control fails. Demand explicit foothold scenarios, not just perimeter defense.
- **Initial footholds enumerated** — at minimum: compromised user credential, compromised service credential/token, RCE in one internet-facing service, malicious insider with legit access, supply-chain implant in a dependency or build.
- **Next-hop reachability** — from each foothold, what can the attacker reach? Trace network reachability + credential reuse + assumable roles. This is where flat networks and over-broad IAM get exposed.
- **Privilege-escalation paths** — from initial access to higher privilege: IAM role chaining, secret pivoting, metadata service, CI/CD takeover, admin-plane access.
- **Blast radius** — for each foothold, what data/systems are exposed before any control stops the attacker. Quantify against data classification.
- **Choke points and segmentation** — where does the design contain spread? Network segmentation, IAM permission boundaries, separate accounts, deny-by-default egress. If there are no choke points, that's the finding.
- **Single-credential blast radius** — if one credential/token/key is stolen, what's reachable? Drives scoping and rotation requirements.

### Identity — human
- **SSO / federation** — IdP, federation protocol (OIDC/SAML), and whether all human access routes through it. Local accounts are a finding.
- **MFA** — enforced where, phishing-resistant or not, and any exceptions. MFA gaps on admin/break-glass are blocking.
- **Privileged access** — who has admin, how it's granted, and whether it's standing or just-in-time. Standing admin is a residual risk to record.
- **JIT elevation** — request/approval/expiry for elevated access; logged and time-boxed.
- **Break-glass** — emergency access procedure, where the credential lives, how its use is detected and reviewed. Undocumented break-glass = unmonitored superuser.
- **Authorization model** — RBAC/ABAC/ReBAC, where it's enforced (gateway, service, data), and least-privilege scoping per role. "Authenticated == authorized" is a gap.
- **Insider and operational controls** — what limits a legitimate operator or support agent acting in bad faith: separation of duties, dual-control on destructive/bulk actions, scoped and logged production access, and access review/deprovisioning on role change or exit. Standing broad operator access with no second control is an insider single point of failure. (Physical and personnel security beyond access controls is the compliance lens — see also `compliance.md`.)

### Identity — machine / workload
- **Service accounts inventory** — every non-human identity, what it's for, and its privilege scope. Orphaned/over-privileged service accounts are a top lateral-movement vector.
- **Workload identity** — how workloads get credentials (workload federation, instance/pod identity, IRSA/Workload Identity) vs long-lived static keys. Static keys in compute are a finding.
- **mTLS / SPIFFE** — service-to-service authN; is identity cryptographic or network-trust-based ("it's in the VPC so it's fine" is not authN).
- **Least-privilege grants** — each machine identity scoped to exactly its needs; no wildcard `*` actions/resources. Demand the actual policy shape, not "scoped appropriately."
- **Credential blast radius** — per machine identity, what one stolen credential reaches (ties to lateral-movement section).

### Network detail
- **Segmentation** — network tiers/zones and what's allowed between them; deny-by-default posture. Flat networks are a blocking finding for anything regulated.
- **Ingress controls** — what's internet-facing, what fronts it (LB/gateway/WAF), and what validation occurs.
- **Egress controls** — outbound restrictions; can compromised compute exfiltrate freely or call C2? Open egress is a common gap.
- **VPC / subnet / security-group / NACL design** — the actual network constructs and rules; public vs private subnets; which workloads sit where.
- **Private connectivity** — PrivateLink/peering/private endpoints vs public exposure for internal services and managed services. Data-store public exposure is blocking.
- **WAF** — presence, managed + custom rules, and what it covers (and doesn't).
- **DDoS posture** — L3/4 and L7 protection, autoscaling limits, and rate limiting at the edge.
- **East-west traffic control** — service-to-service network policy, microsegmentation, and whether internal calls are authenticated and restricted.

### Per-component security metadata
Each component in the inventory must carry this schema; a component missing fields can't be risk-ranked:
- **Owner** — team accountable for its security.
- **Runtime / platform** — language/framework, where it runs (container, function, VM, managed service).
- **Internet exposure** — public, private, or internal-only.
- **Data classes handled** — which classification labels flow through or rest in it.
- **Upstream / downstream dependencies** — what it calls and what calls it.
- **AuthN / authZ posture** — how it authenticates callers and enforces authorization.
- **Criticality tier** — business/security criticality, driving review depth and SLAs.
- **Location** — cloud account/subscription/project and region.

### Cloud account / landing zone
- **Account topology** — account/subscription/project layout as a security boundary; workload separation (per-env, per-tier, per-tenant). One account holding everything is a blast-radius finding.
- **Org policies / SCPs / guardrails** — preventative guardrails (deny regions, deny public S3, deny root use) and whether they're enforced org-wide.
- **Centralized logging account** — log aggregation into an account workloads can't tamper with; who can read/delete.
- **IAM permission boundaries** — boundaries capping max privilege even for self-service roles; prevents privilege-escalation via policy attachment.
- **Baseline conformance** — CIS Benchmark / cloud foundations conformance and known deviations. Cite the baseline, not "we follow best practices."

### Cryptography and key management
- **Algorithms** — ciphers/hashes/signature schemes in use; no deprecated primitives (MD5, SHA-1, RSA-1024, static IVs). Roll-your-own crypto is a finding.
- **TLS / mTLS posture** — minimum TLS version (1.2+), cipher policy, where mTLS is required.
- **Encryption at rest** — every data store and backup encrypted; customer-managed vs provider-managed keys per classification.
- **KMS / HSM custody** — where keys live, who can use vs administer them, dual-control on key admin.
- **Key rotation and revocation** — rotation cadence, automated vs manual, and how a compromised key is revoked and re-wrapped.
- **Certificate lifecycle** — issuance, renewal/automation, revocation, and what breaks on expiry. Expired-cert outages signal an unmanaged lifecycle.

### Data lifecycle and residency
- **Backups and snapshots** — every backup, snapshot, and replica is inventoried, encrypted, access-scoped, and in the threat model; an unlisted backup is an unguarded copy of the crown jewels. Many breaches are of the backup, not the primary store.
- **Backup integrity and restore testing** — backups are tamper-evident/immutable and restores are actually exercised, so a corrupted or ransomware-encrypted backup is caught before it's the only copy. An untested backup is an assumption, not a control.
- **Retention and deletion** — defined retention per data class and a deletion path that actually purges (including backups, caches, search indexes, analytics copies); honors deletion-on-request where regulated. Data kept past need is breach surface and a compliance liability.
- **Residency and cross-border movement** — which regions store and process each data class, and every cross-region/cross-border hop (replication, CDN, DR, third-party processors). Unintended cross-border flow is a regulatory finding, not just an architecture detail.
- **Data minimization and propagation** — sensitive data isn't copied into more stores than it needs to be (logs, analytics, lower environments, vendor systems); each extra copy expands blast radius and residency scope.

### Secrets management
- **Where secrets live** — a vault/secrets manager, not env files in images or config in repos.
- **Dynamic vs static** — short-lived/dynamically-issued secrets preferred over long-lived static credentials; flag every static long-lived secret.
- **Rotation** — rotation policy and whether it's automated; orphaned un-rotated secrets are residual risk.
- **No secrets in the doc/repo/logs/diagrams** — actively confirm none are present in the architecture doc itself, the DFD, sample configs, or referenced repos/logs. A secret in the doc is an immediate finding.
- **Access scoping** — which identities can read which secrets; least privilege on the vault itself.

### Logging, detection, and incident response
- **Security-event logging** — authN events, authZ denials, privileged actions, config changes, data access on regulated data — all logged with identity, timestamp, source.
- **Tamper evidence** — logs write to append-only/immutable storage workloads can't alter or delete.
- **SIEM / detection coverage** — where logs go, what detections exist, and which attack paths from the lateral-movement section are actually detectable. Undetectable attack paths are a gap.
- **Retention** — retention periods meeting compliance and IR needs.
- **Detect → contain → investigate** — from this design, how is a compromise detected, how is the affected component isolated, and what evidence supports investigation. If the answer isn't in the doc, IR readiness is unproven.
- **PII / secret redaction in telemetry** — logs/traces/metrics don't capture secrets, tokens, or unmasked regulated data. Sensitive data in logs is both a disclosure threat and a compliance finding.

### Supply chain
- **SBOM** — a software bill of materials exists and is generated per build.
- **Dependency CVE scanning** — including transitive dependencies, in CI, blocking on severity thresholds.
- **Patch / remediation SLA** — time-to-patch by severity; how the team learns of and fixes new CVEs.
- **Build-pipeline integrity** — who can modify the pipeline, isolation of build runners, protection against poisoned builds; CI/CD is a top supply-chain target.
- **Artifact signing** — build artifacts/images signed and verified at deploy; provenance (SLSA-style) where feasible.
- **Third-party / vendor data exposure** — every external service or SaaS that receives regulated/sensitive data is listed with what it gets, how it authenticates, and its blast radius if breached. A vendor with your data and a long-lived key is part of your attack surface. (Contractual controls — DPAs, subprocessor terms — are the compliance lens; security flags the data exposure and the integration's privilege.)

### Controls mapping
- **Map to a recognized framework** — controls mapped to NIST 800-53, CIS Benchmarks, SOC 2 CC, or ISO 27001 so coverage and gaps are visible against an authority. Pick the framework the org is audited against. When obligations overlap (e.g. PCI + SOC 2 + FedRAMP), map to the strictest in-scope authority and note where the others diverge, rather than picking one and dropping the rest — a control met for SOC 2 can still be a gap for FedRAMP.
- **Coverage vs gaps explicit** — the map shows which controls are met, partial, or absent — not just the met ones. Hiding gaps defeats the purpose.
- **Compliance scope flagged** — if regulated data is present (PCI/HIPAA/GDPR/etc.), note the obligations this design must satisfy. Deep compliance review is its own lens — one-line see-also the compliance mode — but security must flag the scope.

### AI and agentic components
*(Only when a model / LLM / agent exists in the design — skip otherwise.)*
- **Model / provider + data handling** — which model/provider, and exactly what data enters prompt, training, fine-tune, and embedding pipelines, plus what the vendor retains and for how long. Regulated data into a retaining vendor is a finding.
- **Prompt injection** — anywhere untrusted content (user input, retrieved docs, tool output, web content) becomes model instructions, the injection path and its mitigation. Treat all model-ingested external text as untrusted.
- **Tool / action abuse** — what tools/actions the agent can invoke and the privilege blast radius if it's manipulated into misusing them; guardrails (allowlists, human-in-the-loop on high-impact actions, output validation, sandboxing).
- **Agent privilege scoping** — the agent runs with least privilege, not a broad service role; a hijacked agent shouldn't be a domain admin.
- **Denial-of-wallet** — metered model/API calls have hard per-identity quotas and kill-switches; an attacker (or a loop) can't run up unbounded spend. Cost is an availability and financial control.

### Other untrusted-input sinks
- **Deserialization** — any deserialization of attacker-controllable data; safe formats/allowlists, never native deserialization of untrusted bytes.
- **File upload** — type/size validation, AV/malware scanning, where files are stored (off the app host, private bucket), and how they're rendered/served (no execution, content-disposition, separate origin).
- **Injection / XXE / SSTI** — SQL/command/template injection and XML external entity handling at each input sink; parameterization and parser hardening.
- **Webhook authenticity** — inbound webhooks verified via HMAC signature with a replay window/nonce; unauthenticated webhooks are forgeable triggers.
- **SSRF** — server-side fetches that take user-influenced URLs; allowlisting, blocked access to cloud metadata (169.254.169.254) and internal services. SSRF-to-metadata is a classic foothold-to-cloud-takeover path.

### Token and session lifecycle
- **Token lifetimes** — access-token TTLs short; long-lived tokens justified and scoped.
- **Refresh and revocation** — refresh-token rotation, and a working revocation path (logout, compromise) that actually invalidates. Tokens you can't revoke are a finding.
- **Storage** — client-side (httpOnly/secure cookies vs localStorage) and server-side session storage; XSS-exfiltration exposure.
- **Audience binding** — tokens bound to their intended audience/resource so a token for one service can't be replayed at another.
- **Cross-hop propagation** — how identity propagates across service hops (token exchange vs blind forwarding); avoid handing an upstream token to a downstream that over-trusts it.

## Grill order
1. **Reviewability gate** — confirm the DFD, component inventory, and trust boundary catalog exist and the DFD is current. If not, build them first; nothing else can be assessed without them.
2. **DFD annotation** — drive every flow to the full annotation schema and every node to a type and classification. This is the substrate.
3. **Trust boundaries** — enumerate all boundaries and the enforcing control on each; surface tenant/tenant and prod/non-prod especially.
4. **Identity (human + machine)** — authN, authZ, least privilege, and single-credential blast radius. Most high-severity findings live here.
5. **STRIDE per element** — walk each element through the categories; fill the matrix with threat → mitigation → residual → owner.
6. **Attack paths / lateral movement** — assume-breach from each foothold; find the choke points or flag their absence.
7. **Network + cloud account / landing zone** — segmentation, egress, public exposure, account boundaries, guardrails.
8. **Crypto, key management, secrets, and data lifecycle** — at-rest/in-transit, custody, rotation, confirm no secrets in the doc; backups/retention/deletion and residency/cross-border movement.
9. **Untrusted-input sinks, AI/agentic, token/session** — injection, SSRF, file upload, prompt injection, denial-of-wallet, token lifecycle.
10. **Logging / detection / IR and supply chain** — can a compromise be detected and investigated; SBOM, CVE scanning, pipeline integrity, signing.
11. **Controls mapping and residual-risk register** — map to the framework, show gaps, and close out the register with owners and decisions. Polish last: severities, waiver expiries, and naming consistency.

## Deliverable
The grill must leave these artifacts in the architecture doc:

- **Annotated DFD** — diagram with typed nodes (external entity / process / data store / data flow), trust boundaries drawn as explicit lines, and every flow labeled with: protocol+port, authN, authZ, data classification, encryption in transit, boundary-crossing flag.

- **STRIDE-per-element matrix** — table, one row per (element × applicable threat):
  | Element | Element type | Threat category (S/T/R/I/D/E) | Threat description | Existing mitigation | Residual risk | Severity | Owner |

- **Trust boundary catalog** — table:
  | Boundary | What crosses it | Direction | Enforcing control | Gaps / residual risk |

- **Lateral-movement / attack-path narrative** — for each initial foothold (compromised user cred, compromised service cred, RCE in internet-facing service, malicious insider, supply-chain implant): reachable next hops, privilege-escalation path, blast radius vs data classification, and the choke point(s) that contain it (or a flag that none exist).

- **Controls coverage map** — table mapping design controls to the chosen framework:
  | Control area | Framework reference (e.g. NIST 800-53 AC-2) | Implemented? (met / partial / absent) | Evidence / where in design | Gap notes |

- **Residual-risk register** — table:
  | Risk ID | Description | Likelihood | Impact | Severity | Decision (mitigate / accept / waiver) | Compensating control | Owner | Review/expiry date |

Each blocking finding maps to a specific missing artifact or empty field above, so the sign-off decision (approve / block / conditional waiver) is defensible.
