# Mermaid Diagram Templates

Copy-paste-ready templates for common architecture patterns. Each template includes all 4 layers with `{PLACEHOLDER}` markers for customization. Templates render as valid Mermaid out of the box.

**Prerequisites**: Read [mermaid-spec.md](mermaid-spec.md) for symbol taxonomy (§3), typed edges (§4), and classDef reference (§8). Read [mermaid-layers.md](mermaid-layers.md) for layer definitions.

---

## §1 Symbol Legend

Complete legend subgraph showing all 3 symbol tiers, all 8 edge types, and all risk classes. Include this (or a subset) at the bottom of every diagram.

```mermaid
flowchart TD
    subgraph SymbolLegend["Symbol Legend"]
        style SymbolLegend fill:#f8f9fa,stroke:#dee2e6

        subgraph Tier1["Tier 1 — Core"]
            SL_Ext[External Entity]:::external
            SL_Proc([Process]):::neutral
            SL_DS[(Data Store)]:::dataStore
            SL_Dec{Decision}
        end

        subgraph Tier2["Tier 2 — Cloud Extensions"]
            SL_IAM{IAM / Identity}:::identity
            SL_Sec{{Secrets / KMS}}:::secrets
            SL_Ctrl[[Security Control]]:::control
            SL_Pipe[/CI-CD Pipeline/]:::pipeline
            SL_EDep[External Dep]:::externalDep
        end

        subgraph Tier3["Tier 3 — Specialized"]
            SL_OOS["Out of Scope"]:::outOfScope
            SL_TB["--- = Trust Boundary"]
            SL_TN["--- = Tenant Boundary (blue)"]
            SL_RG["--- = Region Boundary (purple)"]
            SL_NZ["--- = Network Zone (CIDR)"]
            SL_DZ["shaded = Data Classification Zone"]
        end
    end

    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
    classDef identity fill:#d4e6f1,stroke:#2980b9,stroke-width:1px,color:#000
    classDef secrets fill:#f9e79f,stroke:#f39c12,stroke-width:2px,color:#000
    classDef control fill:#abebc6,stroke:#27ae60,stroke-width:1px,color:#000
    classDef pipeline fill:#d5dbdb,stroke:#7f8c8d,stroke-width:1px,color:#000
    classDef externalDep fill:#f5f5f5,stroke:#333,stroke-width:3px,stroke-dasharray:3,color:#000
    classDef outOfScope fill:#eee,stroke:#999,stroke-width:1px,stroke-dasharray:5,color:#666
```

---

## §2 Edge Legend

Standalone edge-typing legend. Include in diagrams that use multiple edge types.

```mermaid
flowchart LR
    subgraph EdgeLegend["Edge Type Legend"]
        style EdgeLegend fill:#f8f9fa,stroke:#dee2e6

        E1A[ ] --> E1B[ ]
        E1A ---|"Data flow (default)"| E1B

        E2A[ ] -.-> E2B[ ]
        E2A ---|"[CTRL] Control/API"| E2B

        E3A[ ] --o E3B[ ]
        E3A ---|"[AUTH] AuthN/AuthZ (blue)"| E3B

        E4A[ ] ==> E4B[ ]
        E4A ---|"[KEY] Secrets/Keys"| E4B

        E5A[ ] -.-> E5B[ ]
        E5A ---|"[ADMIN] Admin/Ops (red)"| E5B

        E6A[ ] --> E6B[ ]
        E6A ---|"[ASYNC] Async/Event (green)"| E6B

        E7A[ ] -.-> E7B[ ]
        E7A ---|"[REPL] Replication (purple)"| E7B

        E8A[ ] --> E8B[ ]
        E8A ---|"[BUILD] Build/Deploy (orange)"| E8B
    end
```

---

## §3 SaaS Template

Standard SaaS architecture: User → CDN → LB → API → Auth → DB + Cache + Queue → Worker → External.

### L1: Architecture

```mermaid
flowchart TD
    %% Version: {DATE} | Phase: 2 | System: {SYSTEM_NAME} | Layer: L1
    User["{USER_TYPE}"]:::external
    Admin["{ADMIN_TYPE}"]:::external

    CDN(["{CDN_NAME}\n{CDN_TECH}\n[vendor:{VENDOR}] [managed]"]):::neutral
    LB(["{LB_NAME}\n{LB_TECH}\n[team:{TEAM}] [self-managed]"]):::neutral
    API(["{API_NAME}\n{API_TECH}\n[team:{TEAM}] [self-managed]"]):::neutral
    Auth(["{AUTH_NAME}\n{AUTH_TECH}\n[team:{TEAM}] [self-managed]"]):::neutral
    Worker(["{WORKER_NAME}\n{WORKER_TECH}\n[team:{TEAM}] [self-managed]"]):::neutral

    DB[("{DB_NAME}\n{DB_TECH}\n[vendor:{VENDOR}] [managed]")]:::dataStore
    Cache[("{CACHE_NAME}\n{CACHE_TECH}\n[vendor:{VENDOR}] [managed]")]:::dataStore
    Queue[("{QUEUE_NAME}\n{QUEUE_TECH}\n[vendor:{VENDOR}] [managed]")]:::dataStore

    ExtPay["{PAYMENT_PROVIDER}"]:::externalDep
    ExtEmail["{EMAIL_PROVIDER}"]:::externalDep

    User -->|"HTTPS: web requests [PUBLIC]"| CDN
    Admin -.->|"[ADMIN] HTTPS: admin API [RESTRICTED]"| CDN
    CDN -->|"HTTPS: proxied requests [INTERNAL]"| LB
    LB -->|"HTTP: routed requests [INTERNAL]"| API
    API --o|"[AUTH] gRPC: token validation [RESTRICTED]"| Auth
    API -->|"TCP/TLS: queries [CONFIDENTIAL]"| DB
    API -->|"TCP: session data [CONFIDENTIAL]"| Cache
    API -->|"[ASYNC] AMQP/TLS: events [INTERNAL]"| Queue
    Queue -->|"[ASYNC] AMQP/TLS: jobs [INTERNAL]"| Worker
    Worker -->|"HTTPS: payment requests [RESTRICTED]"| ExtPay
    Worker -->|"HTTPS: email sends [CONFIDENTIAL]"| ExtEmail
    Auth -->|"TCP/TLS: credential lookup [RESTRICTED]"| DB

    subgraph Legend
        style Legend fill:#f8f9fa,stroke:#dee2e6
        L1[External Entity]:::external
        L2([Process]):::neutral
        L3[(Data Store)]:::dataStore
        L4[External Dep]:::externalDep
        L5["-->  Data flow"]
        L6["-.-> [CTRL] Control"]
        L7["--o  [AUTH] AuthN/AuthZ"]
        L8["-->  [ASYNC] Async/Event"]
    end

    classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
    classDef externalDep fill:#f5f5f5,stroke:#333,stroke-width:3px,stroke-dasharray:3,color:#000
```

### L4: Threat Overlay

```mermaid
flowchart TD
    %% Version: {DATE} | Phase: 7 | System: {SYSTEM_NAME} | Layer: L4
    User["{USER_TYPE}"]:::external
    Admin["{ADMIN_TYPE}"]:::external

    subgraph DMZ["DMZ — Low Trust"]
        style DMZ stroke:#e74c3c,stroke-width:2px,stroke-dasharray: 5 5
        CDN(["{CDN_NAME}\n{CDN_TECH}\n⚠ {STRIDE} · {L}×{I}={SCORE} {BAND}"]):::{RISK_CLASS}
        LB(["{LB_NAME}\n{LB_TECH}\n⚠ {STRIDE} · {L}×{I}={SCORE} {BAND}"]):::{RISK_CLASS}
    end

    subgraph AppTier["Application Tier — Medium Trust"]
        style AppTier stroke:#f39c12,stroke-width:2px,stroke-dasharray: 5 5
        API(["{API_NAME}\n{API_TECH}\n⚠ {STRIDE} · {L}×{I}={SCORE} {BAND}\n{CWE_IDS}"]):::{RISK_CLASS}
        Auth(["{AUTH_NAME}\n{AUTH_TECH}\n⚠ {STRIDE} · {L}×{I}={SCORE} {BAND}\n{CWE_IDS}"]):::{RISK_CLASS}
        Worker(["{WORKER_NAME}\n{WORKER_TECH}"]):::noFindings
    end

    subgraph DataTier["Data Tier — High Trust"]
        style DataTier stroke:#27ae60,stroke-width:2px,stroke-dasharray: 5 5
        DB[("{DB_NAME}\n{DB_TECH}\n⚠ {STRIDE} · {L}×{I}={SCORE} {BAND}")]:::{RISK_CLASS}
        Cache[("{CACHE_NAME}")]:::noFindings
        Queue[("{QUEUE_NAME}")]:::noFindings
    end

    User -->|"HTTPS: requests [PUBLIC]"| CDN
    CDN -->|"HTTPS: proxied [INTERNAL]"| LB
    LB -->|"HTTP: routed [INTERNAL]"| API
    API ==>|"[AUTH] gRPC: tokens [RESTRICTED]"| Auth
    Auth ==>|"TCP/TLS: credentials [RESTRICTED]"| DB

    subgraph Legend
        style Legend fill:#f8f9fa,stroke:#dee2e6
        RL1[External]:::external
        RL2([High Risk]):::highRisk
        RL3([Medium Risk]):::medRisk
        RL4([Low Risk]):::lowRisk
        RL5([No Findings]):::noFindings
        RL6["==> Attack Path (red)"]
        RL7["--- Trust Boundary"]
    end

    classDef highRisk fill:#ffcccc,stroke:#cc0000,stroke-width:2px,color:#000
    classDef medRisk fill:#ffe6cc,stroke:#cc7a00,stroke-width:2px,color:#000
    classDef lowRisk fill:#ccffcc,stroke:#008000,stroke-width:2px,color:#000
    classDef noFindings fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
```

---

## §4 Event-Driven Template

Event-driven architecture: Producers → Event Bus → Consumers → Data Stores. Emphasizes `[ASYNC]` edges.

### L1: Architecture

```mermaid
flowchart TD
    %% Version: {DATE} | Phase: 2 | System: {SYSTEM_NAME} | Layer: L1
    ProdA(["{PRODUCER_A}\n{TECH}\n[team:{TEAM}]"]):::neutral
    ProdB(["{PRODUCER_B}\n{TECH}\n[team:{TEAM}]"]):::neutral

    EventBus(["{EVENT_BUS_NAME}\n{EVENT_TECH}\n[vendor:{VENDOR}] [managed]"]):::neutral
    DLQ[("{DLQ_NAME}\n Dead Letter Queue")]:::dataStore

    ConsA(["{CONSUMER_A}\n{TECH}\n[team:{TEAM}]"]):::neutral
    ConsB(["{CONSUMER_B}\n{TECH}\n[team:{TEAM}]"]):::neutral

    StoreA[("{STORE_A}\n{TECH}")]:::dataStore
    StoreB[("{STORE_B}\n{TECH}")]:::dataStore

    ExtAPI["{EXTERNAL_API}"]:::externalDep

    ProdA -->|"[ASYNC] {PROTOCOL}: {EVENT_A} [{SENSITIVITY}]"| EventBus
    ProdB -->|"[ASYNC] {PROTOCOL}: {EVENT_B} [{SENSITIVITY}]"| EventBus
    EventBus -->|"[ASYNC] {PROTOCOL}: {EVENT_A} [{SENSITIVITY}]"| ConsA
    EventBus -->|"[ASYNC] {PROTOCOL}: {EVENT_B} [{SENSITIVITY}]"| ConsB
    EventBus -->|"[ASYNC] failed events [INTERNAL]"| DLQ
    ConsA -->|"TCP/TLS: writes [{SENSITIVITY}]"| StoreA
    ConsB -->|"HTTPS: API calls [{SENSITIVITY}]"| ExtAPI
    ConsB -->|"TCP/TLS: writes [{SENSITIVITY}]"| StoreB

    classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
    classDef externalDep fill:#f5f5f5,stroke:#333,stroke-width:3px,stroke-dasharray:3,color:#000
```

---

## §5 K8s Template

Kubernetes architecture: Ingress → Services → Pods → PVs, K8s API → Kubelet → etcd. Emphasizes `[CTRL]` and `[BUILD]` edges.

### L1: Architecture

```mermaid
flowchart TD
    %% Version: {DATE} | Phase: 2 | System: {SYSTEM_NAME} | Layer: L1
    User["{USER_TYPE}"]:::external
    Dev[Developer]:::external

    subgraph K8sCluster["{CLUSTER_NAME} — K8s Cluster"]
        Ingress(["{INGRESS_NAME}\nNGINX Ingress\n[self-managed]"]):::neutral
        SvcA(["{SVC_A_NAME}\n{TECH}\n[team:{TEAM}]"]):::neutral
        SvcB(["{SVC_B_NAME}\n{TECH}\n[team:{TEAM}]"]):::neutral
        PodA(["{POD_A}\n{TECH}"]):::neutral
        PodB(["{POD_B}\n{TECH}"]):::neutral
    end

    subgraph CtrlPlane["K8s Control Plane"]
        K8sAPI([K8s API Server]):::neutral
        Kubelet([Kubelet]):::neutral
        etcd[(etcd)]:::dataStore
    end

    subgraph CICD["CI/CD Pipeline"]
        GHActions[/GitHub Actions/]:::pipeline
        ECR[/Container Registry/]:::pipeline
    end

    PV[("{PV_NAME}\n{STORAGE_TECH}")]:::dataStore

    User -->|"HTTPS: requests [PUBLIC]"| Ingress
    Ingress -->|"HTTP: routed [INTERNAL]"| SvcA
    Ingress -->|"HTTP: routed [INTERNAL]"| SvcB
    SvcA -->|"HTTP: proxied [INTERNAL]"| PodA
    SvcB -->|"HTTP: proxied [INTERNAL]"| PodB
    PodA -->|"TCP/TLS: data [{SENSITIVITY}]"| PV

    K8sAPI -.->|"[CTRL] HTTPS: scheduling [RESTRICTED]"| Kubelet
    Kubelet -.->|"[CTRL] HTTPS: health checks [INTERNAL]"| PodA
    Kubelet -.->|"[CTRL] HTTPS: health checks [INTERNAL]"| PodB
    K8sAPI -->|"TCP/TLS: cluster state [RESTRICTED]"| etcd

    Dev -->|"[BUILD] HTTPS: git push [INTERNAL]"| GHActions
    GHActions -->|"[BUILD] HTTPS: docker push [INTERNAL]"| ECR
    ECR -.->|"[CTRL] HTTPS: image pull [INTERNAL]"| Kubelet

    classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
    classDef pipeline fill:#d5dbdb,stroke:#7f8c8d,stroke-width:1px,color:#000
```
