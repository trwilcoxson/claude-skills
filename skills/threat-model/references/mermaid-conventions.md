# Mermaid Diagram Conventions for Threat Models

## Component Shapes

Use consistent shapes to distinguish component types at a glance.

| Component Type | Mermaid Syntax | Example |
|---------------|---------------|---------|
| External Entity (actor, third-party) | `[Text]` rectangle | `User[End User]` |
| Process (application, service) | `([Text])` stadium/rounded | `API([API Gateway])` |
| Data Store (database, cache, file) | `[(Text)]` cylinder | `DB[(User Database)]` |
| Decision / Gateway | `{Text}` diamond | `AuthCheck{Auth Valid?}` |

## Two-Pass Diagram Approach

The threat model produces the architecture diagram in two phases to prevent risk assessment from biasing the structural representation.

### Pass 1 — Structural Diagram (Phase 2)

Purpose: Accurately represent the system architecture before analysis introduces bias.

- All processes use a single neutral style: `:::neutral`
- External entities use `:::external` (external is a structural distinction, not a risk judgment)
- Data stores use `:::dataStore`
- Trust boundaries drawn as dashed subgraphs (structural fact)
- Data flow labels include protocol, data type, and sensitivity classification (factual)
- Component metadata notes document tech stack, auth, encryption (factual observations)
- **NO** `highRisk`, `medRisk`, or `lowRisk` classes applied
- **NO** threat annotation notes
- Legend shows only structural elements

### Pass 2 — Risk Overlay (Phase 7)

Purpose: Visualize validated risk assessment on the structural diagram after analysis is complete.

- Start from the Pass 1 diagram
- Replace `:::neutral` with risk-based classes (`:::highRisk`, `:::medRisk`, `:::lowRisk`) based on validated findings
- Components with **no identified threats** remain `:::noFindings` — absence of findings does NOT equal low risk; it may mean insufficient analysis
- Add threat annotation notes with: STRIDE-LM categories, OWASP Risk Rating score (LxI=Score BAND), top CWE IDs
- Update legend to include risk color meanings
- Use `==>` (thick arrows) to highlight critical data flows identified during analysis
- Add a note explaining that grey (`noFindings`) means "no validated findings," not "confirmed safe"

## Trust Boundaries

Represent trust boundaries as subgraphs with dashed borders. Trust boundaries are structural facts and appear in **both passes**.

```mermaid
subgraph DMZ["DMZ — Low Trust"]
    style DMZ stroke:#e74c3c,stroke-width:2px,stroke-dasharray: 5 5
    LB([Load Balancer])
end

subgraph AppTier["Application Tier — Medium Trust"]
    style AppTier stroke:#f39c12,stroke-width:2px,stroke-dasharray: 5 5
    API([API Server])
end

subgraph DataTier["Data Tier — High Trust"]
    style DataTier stroke:#27ae60,stroke-width:2px,stroke-dasharray: 5 5
    DB[(Primary Database)]
end
```

## Data Flow Labels

Label every arrow with protocol, data type, and sensitivity. This is factual metadata and appears in **both passes**.

Format: `"Protocol: data type [SENSITIVITY]"`

Examples:
- `-->|"HTTPS: JSON credentials [RESTRICTED]"|`
- `-->|"gRPC/mTLS: order events [CONFIDENTIAL]"|`
- `-->|"TCP/TLS: SQL queries [INTERNAL]"|`
- `-->|"HTTPS: public content [PUBLIC]"|`

## Arrow Syntax Reference

| Syntax | Meaning | Use In |
|--------|---------|--------|
| `-->` | Standard data flow | Both passes |
| `-.->` | Optional or async flow | Both passes |
| `==>` | Critical/high-sensitivity flow | Risk overlay only |
| `-->\|"label"\|` | Labeled flow | Both passes |

Note: `==>` (thick arrow) should only be used in the risk overlay pass to highlight critical data flows identified during analysis. Do not use it in the structural pass.

## Color Coding with classDef

Define all `classDef` styles at the **end** of the diagram, after all nodes and edges.

```mermaid
%% Structural pass (Phase 2)
classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000

%% Risk overlay (Phase 7)
classDef highRisk fill:#ffcccc,stroke:#cc0000,stroke-width:2px,color:#000
classDef medRisk fill:#ffe6cc,stroke:#cc7a00,stroke-width:2px,color:#000
classDef lowRisk fill:#ccffcc,stroke:#008000,stroke-width:2px,color:#000
classDef noFindings fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
```

Key distinction: `noFindings` (grey) is used in Pass 2 for components where no threats were validated. `lowRisk` (green) is used only when analysis explicitly confirms low risk. They are semantically different even though `noFindings` shares the same visual as `neutral`.

## Threat Annotations

Use Mermaid `note` blocks to annotate threats. These appear **only in the risk overlay pass (Phase 7)**.

```mermaid
note right of API "STRIDE: S,T,I,E,LM\nRisk: 4x4=16 HIGH\nCWE-287, CWE-20"
```

Format: `STRIDE: [categories]\nRisk: [L]x[I]=[Score] [BAND]\n[CWE IDs]`

Keep annotations concise: STRIDE-LM category abbreviations, OWASP Risk Rating likelihood x impact = score with band, and top CWE IDs.

## Component Metadata

Use notes to document technical context. These are factual observations and appear in **both passes**.

```mermaid
note left of DB "PostgreSQL 15\nTLS in transit\nAES-256 at rest\nIAM auth"
```

Include: technology/version, authentication mechanism, encryption, rate limits (where relevant).

## Diagram Legends

### Structural Legend (Phase 2)

```mermaid
subgraph Legend
    style Legend fill:#f8f9fa,stroke:#dee2e6
    L1[External Entity]:::external
    L2([Process]):::neutral
    L3[(Data Store)]:::dataStore
    L4["--- = Trust Boundary"]
    L5["[SENSITIVITY] = Data Classification"]
end
```

### Risk-Overlay Legend (Phase 7)

```mermaid
subgraph Legend
    style Legend fill:#f8f9fa,stroke:#dee2e6
    L1[External Entity]:::external
    L2([High Risk]):::highRisk
    L3([Medium Risk]):::medRisk
    L4([Low Risk]):::lowRisk
    L5([No Findings]):::noFindings
    L6[(Data Store)]:::dataStore
    L7["--- = Trust Boundary"]
end
```

## Full Example

Risk-overlay diagram (Phase 7) with inline comments showing what differs from the structural pass (Phase 2).

```mermaid
flowchart TD
    User[End User]:::external
    Admin[Admin User]:::external
    ThirdParty[Payment Provider]:::external

    subgraph DMZ["DMZ — Untrusted"]
        style DMZ stroke:#e74c3c,stroke-width:2px,stroke-dasharray: 5 5
        %% Pass 1: use :::neutral instead of risk classes
        CDN([CDN / WAF]):::lowRisk
        LB([Load Balancer]):::medRisk
    end

    subgraph AppTier["Application Tier — Semi-Trusted"]
        style AppTier stroke:#f39c12,stroke-width:2px,stroke-dasharray: 5 5
        API([API Gateway]):::highRisk
        Auth([Auth Service]):::highRisk
        OrderSvc([Order Service]):::medRisk
        NotifSvc([Notification Service]):::noFindings
    end

    subgraph DataTier["Data Tier — Trusted"]
        style DataTier stroke:#27ae60,stroke-width:2px,stroke-dasharray: 5 5
        UserDB[(User DB)]:::highRisk
        OrderDB[(Order DB)]:::medRisk
        Cache[(Redis Cache)]:::medRisk
        Queue[(Message Queue)]:::noFindings
    end

    User -->|"HTTPS: web requests [PUBLIC]"| CDN
    %% Pass 1: use --> instead of ==> for all flows
    Admin ==>|"HTTPS: admin API [RESTRICTED]"| CDN
    CDN -->|"HTTPS: proxied requests [INTERNAL]"| LB
    LB -->|"HTTP: routed requests [INTERNAL]"| API
    API ==>|"gRPC: auth tokens [RESTRICTED]"| Auth
    API -->|"gRPC: order data [CONFIDENTIAL]"| OrderSvc
    Auth ==>|"TCP/TLS: credentials [RESTRICTED]"| UserDB
    Auth -->|"TCP: session tokens [CONFIDENTIAL]"| Cache
    OrderSvc -->|"TCP/TLS: order records [CONFIDENTIAL]"| OrderDB
    OrderSvc -->|"AMQP/TLS: order events [INTERNAL]"| Queue
    Queue -->|"AMQP/TLS: notifications [INTERNAL]"| NotifSvc
    OrderSvc ==>|"HTTPS: payment requests [RESTRICTED]"| ThirdParty
    ThirdParty -->|"HTTPS: payment confirmations [CONFIDENTIAL]"| OrderSvc

    %% Component metadata notes appear in BOTH passes
    note right of API "Node.js Express\nJWT validation\nRate limited: 1000/min\nOWASP headers"
    note right of Auth "Go service\nmTLS internal\nbcrypt passwords\nMFA supported"
    note left of UserDB "PostgreSQL 15\nTLS in transit\nAES-256 at rest\nIAM auth\nDaily backups"
    note right of LB "NGINX\nTLS 1.3 termination\nNo WAF rules"

    %% Pass 1: omit all threat annotation notes below
    note right of API "STRIDE: S,T,I,E\nRisk: 4x4=16 HIGH\nCWE-287, CWE-20"
    note right of Auth "STRIDE: S,E,LM\nRisk: 3x4=12 HIGH\nCWE-307, CWE-522"
    note left of UserDB "STRIDE: T,I,D\nRisk: 3x3=9 MEDIUM\nCWE-89, CWE-311"
    note right of LB "STRIDE: T,D\nRisk: 2x3=6 MEDIUM\nCWE-295, CWE-400"
    note right of OrderSvc "STRIDE: T,R,I\nRisk: 2x3=6 MEDIUM\nCWE-862, CWE-352"

    note bottom of Legend "Grey (No Findings) = no validated threats identified.\nThis does NOT mean confirmed safe."

    %% Pass 1: use structural legend instead (External, Process:::neutral, Data Store, Trust Boundary, Sensitivity)
    subgraph Legend
        style Legend fill:#f8f9fa,stroke:#dee2e6
        L1[External Entity]:::external
        L2([High Risk]):::highRisk
        L3([Medium Risk]):::medRisk
        L4([Low Risk]):::lowRisk
        L5([No Findings]):::noFindings
        L6[(Data Store)]:::dataStore
        L7["--- = Trust Boundary"]
    end

    %% Pass 1: use neutral/external/dataStore classDefs only
    classDef highRisk fill:#ffcccc,stroke:#cc0000,stroke-width:2px,color:#000
    classDef medRisk fill:#ffe6cc,stroke:#cc7a00,stroke-width:2px,color:#000
    classDef lowRisk fill:#ccffcc,stroke:#008000,stroke-width:2px,color:#000
    classDef noFindings fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
    classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
    classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
```

## Common Pitfalls

1. **Subgraph nesting**: Mermaid supports nested subgraphs, but deeply nested structures (3+ levels) can render unpredictably. Prefer flat trust boundaries where possible.

2. **Special characters in labels**: Wrap labels containing special characters (parentheses, brackets, quotes) in double quotes. Use HTML entities if needed (`&amp;`, `&lt;`).

3. **`classDef` placement**: Define all `classDef` lines at the **end** of the diagram, after all nodes and edges. Placing them mid-diagram can cause parsing errors.

4. **`classDef` vs per-node `style`**: Use `classDef` for consistent coloring across the diagram. Use per-node `style` only for trust boundary subgraphs (stroke-dasharray). Do not mix both on the same node.

5. **Flow direction**: Use `flowchart TD` (top-down) for most diagrams. Use `flowchart LR` (left-right) only when the system has a clear linear pipeline flow.

6. **Long labels**: Keep node labels short (2-4 words). Put details in notes rather than cramming them into the node label.

7. **Arrow syntax**: Use `-->` for standard flow, `-.->` for optional/async flow, `==>` for critical/high-sensitivity flow (risk overlay only). Be consistent throughout each pass.
