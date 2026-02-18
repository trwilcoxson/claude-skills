# Mermaid Diagram Specification

The canonical specification for all Mermaid diagrams in threat model assessments. All other diagram references (layers, templates, companion diagrams) defer to this document for symbol definitions, edge types, and styling rules.

---

## §1 Design Principles

### Visual Hierarchy

1. **Size signals importance**: High-risk components get longer, descriptive labels. External-facing components sit at the top (TD) or left (LR).
2. **Color signals risk**: The classDef palette communicates risk — reds draw attention, greens recede. Let color do the work.
3. **Grouping signals relationships**: Subgraphs for trust zones, network segments, and deployment units create scannable zones.
4. **Flow direction signals data movement**: TD for most systems. LR only for clear pipeline architectures.

### Information Density

Diagrams must be **information-rich**. Every element carries security-relevant context:

- **Node labels**: Component name + key technology + security metadata. Use `\n` for multi-line.
- **Edge labels**: Protocol, data type, sensitivity, and encryption state. Every edge MUST be typed (§4).
- **Subgraph labels**: Trust level, network CIDR, or data classification.

### Aesthetics

1. Consistent spacing — parallel flows at similar lengths.
2. Minimize edge crossings — reorder nodes to reduce crossings.
3. Node labels: 2-4 lines max. Edge labels: 1 line.
4. Visual breathing room — split large zones into sub-zones.
5. Legend in its own subgraph at the bottom.
6. Professional feel — no orphaned nodes, no generic labels like "Server" or "DB".

---

## §2 Rendering Configuration

Use `references/mermaid-config.json` for all Mermaid PNG/SVG output.

### CLI Rendering Command

```bash
npx -y @mermaid-js/mermaid-cli \
  -i {file}.mmd \
  -o {file}.png \
  -c /path/to/references/mermaid-config.json \
  -w 3000 -b white --scale 2
```

**Key parameters**: `-c` applies theme/fonts/spacing, `-w 3000` for high-res output, `--scale 2` for retina/print, `-b white` for clean background.

### Pre-Processing Before Rendering

Strip before CLI rendering:
1. `~~>` wavy arrows → replace with `==>` + `linkStyle N stroke:#cc0000,stroke-width:3px`
2. `note` directives → remove (metadata belongs in enriched node labels)
3. Unescaped special characters → wrap in double quotes
4. Deeply nested subgraphs (3+ levels) → flatten where possible

### HTML Report Rendering

**DO NOT use Mermaid CDN (`mermaid.js`) for client-side rendering in HTML reports.** Always pre-render diagrams to PNG using the CLI command in §2 and embed them with `<img src="filename.png">`.

CDN rendering fails in practice because:
1. `<\/script>` (a JS-only escape) breaks the HTML parser — it never finds the closing `</script>` tag, consuming the entire page as script text.
2. `defer`/`async` on the CDN script creates race conditions with inline JS that calls `mermaid.initialize()`.
3. `file://` URLs block CDN fetches entirely, so reports opened locally show nothing.

The CLI rendering command in §2 above is the only supported method for producing diagram images.

---

## §3 Symbol Taxonomy

Symbols are organized in three tiers. **Core** symbols MUST appear in every baseline diagram. **Cloud Extensions** SHOULD appear when the system uses cloud infrastructure. **Specialized** symbols are OPTIONAL and apply only to specific architecture types.

**These are the only shapes allowed in baseline diagrams.**

### Tier 1 — Core (MUST)

| Symbol | Shape | Mermaid Syntax | Meaning | Required Labels | classDef |
|--------|-------|---------------|---------|-----------------|----------|
| External Entity | Rectangle | `[Text]` | Actor, third-party, user | Name | `external` |
| Process | Stadium | `([Text])` | Application, service, API | Name + Tech + Security features | `neutral` |
| Data Store | Cylinder | `[(Text)]` | Database, cache, file store | Name + Tech + Encryption | `dataStore` |
| Decision/Gateway | Diamond | `{Text}` | Auth check, routing decision | Condition | — |
| Trust Boundary | Dashed subgraph | `subgraph` + `style ... stroke-dasharray` | Security policy domain | Zone name + trust level | — |

### Tier 2 — Cloud Extensions (SHOULD)

| Symbol | Shape | Mermaid Syntax | Meaning | Required Labels | classDef |
|--------|-------|---------------|---------|-----------------|----------|
| Identity/IAM | Diamond | `{Text}` | IAM role, service account, IdP | Name + provider | `identity` |
| Secrets/KMS | Hexagon | `{{Text}}` | Vault, HSM, KMS, cert authority | Name + type | `secrets` |
| Security Control | Subroutine | `[[Text]]` | WAF, IDS, MFA, rate limiter | Name + type | `control` |
| Deployment Pipeline | Parallelogram | `[/Text/]` | CI/CD, container registry | Name + tool | `pipeline` |
| External Dependency | Rectangle | `[Text]` | Third-party SaaS, API | Name + vendor | `externalDep` |

### Tier 3 — Specialized (OPTIONAL)

| Symbol | Shape | Mermaid Syntax | Meaning | When to Use | classDef |
|--------|-------|---------------|---------|-------------|----------|
| Out-of-Scope | Any | Standard + `:::outOfScope` | Excluded component with integration point | Scoped assessments | `outOfScope` |
| Tenant Boundary | Subgraph | Blue dashed `subgraph` | Logical tenant isolation | Multi-tenant SaaS only | — |
| Region Boundary | Subgraph | Purple dashed `subgraph` | Geographic deployment region | Multi-region only | — |
| Network Zone | Subgraph | Subgraph with CIDR label | Network segment (VPC/subnet/VLAN) | Cloud-native / on-premise with VPC | — |
| Data Classification Zone | Subgraph | Sensitivity-colored subgraph | Data sensitivity boundary | Multiple sensitivity levels | — |

---

## §4 Typed Edge Specification

**Rule: EVERY arrow MUST be typed.** Untyped arrows are specification violations.

Each edge type has a distinct line style, label prefix, and linkStyle color. This enables machine-parseable diagrams and consistent visual communication.

| # | Edge Type | Line Style | Prefix | Color | linkStyle | Example |
|---|-----------|-----------|--------|-------|-----------|---------|
| 1 | Data flow | `-->` solid | (none) | default | — | `-->\|"HTTPS: user data [CONF]"\|` |
| 2 | Control/API | `-.->` dashed | `[CTRL]` | default | — | `-.->\|"[CTRL] gRPC: schedule"\|` |
| 3 | AuthN/AuthZ | `--o` circle | `[AUTH]` | blue | `stroke:#2980b9` | `--o\|"[AUTH] SAML assertion"\|` |
| 4 | Secrets/Keys | `==>` thick | `[KEY]` | default | — | `==>\|"[KEY] mTLS cert"\|` |
| 5 | Admin/Ops | `-.->` dashed | `[ADMIN]` | red | `stroke:#cc0000` | `-.->\|"[ADMIN] SSH config"\|` |
| 6 | Async/Event | `-->` solid | `[ASYNC]` | green | `stroke:#27ae60` | `-->\|"[ASYNC] SQS events"\|` |
| 7 | Replication | `-.->` dashed | `[REPL]` | purple | `stroke:#8e44ad` | `-.->\|"[REPL] DB sync"\|` |
| 8 | Build/Deploy | `-->` solid | `[BUILD]` | orange | `stroke:#f39c12` | `-->\|"[BUILD] docker push"\|` |

### Edge Label Format

All edge labels follow this format: `"[PREFIX] Protocol: data description [SENSITIVITY] [ENC|PLAIN]"`

- **PREFIX**: From the table above (omit for Data flow type).
- **Protocol**: HTTPS, gRPC, TCP/TLS, AMQP, etc.
- **Data description**: What is being transmitted.
- **Sensitivity**: `[PUBLIC]`, `[INTERNAL]`, `[CONFIDENTIAL]`, `[RESTRICTED]`.
- **Encryption state**: `[ENC]` or `[PLAIN]` — append when encryption status varies across flows.

### Applying linkStyle Colors

```mermaid
%% After all edges are defined, color typed edges:
linkStyle 2 stroke:#2980b9,stroke-width:2px   %% AUTH edge (index 2)
linkStyle 4 stroke:#cc0000,stroke-width:2px    %% ADMIN edge (index 4)
linkStyle 5 stroke:#27ae60,stroke-width:2px    %% ASYNC edge (index 5)
linkStyle 6 stroke:#8e44ad,stroke-width:2px    %% REPL edge (index 6)
linkStyle 7 stroke:#f39c12,stroke-width:2px    %% BUILD edge (index 7)
```

---

## §5 Threat Annotations

Threat data is embedded in enriched node labels (Phase 7 risk overlay only). **DO NOT use `note right of` syntax** — it is NOT valid in flowchart mode.

### Machine-Parseable Annotation Format

```
ComponentID(["Component Name\nTech · Security Feature\n⚠ {STRIDE} · {L}×{I}={Score} {BAND}\n{MITRE} · {CWE}\n✓ {Mitigation} [{Status}] [R:{Residual}]"]):::{riskClass}
```

| Field | Format | Example |
|-------|--------|---------|
| ThreatID | TM-NNN | TM-004 |
| STRIDE | Comma-separated letters | S,T,I,E |
| LxI=Score | `{L}×{I}={Score}` | 4×4=16 |
| BAND | CRITICAL / HIGH / MEDIUM / LOW | HIGH |
| MITRE | T-number | T1190 |
| CWE | CWE-NNN | CWE-287 |
| Mitigation | Short description | Rate limiting |
| Status | IMPLEMENTED / PLANNED / MISSING | IMPLEMENTED |
| Residual | Residual risk score after mitigation | R:6 |

### Compact Format (for dense diagrams)

When full annotations make labels unreadable, use a 3-line compact format:

```
API(["API Gateway\nNode.js · Express\n⚠ S,T,I,E · 4×4=16 HIGH"]):::highRisk
```

Components with no validated findings use a simple 2-line label:

```
NotifSvc(["Notification Svc\nNode.js"]):::noFindings
```

---

## §6 Accessibility

### Colorblind Safety

The classDef palette is designed for deuteranopia (red-green) accessibility:
- Risk levels use saturation + shape, not hue alone.
- `highRisk` uses red fill + thick stroke. `lowRisk` uses green fill + thin stroke.
- `noFindings` uses neutral grey — visually distinct from all risk colors.

### Consistent Direction

- Use `flowchart TD` for hierarchical systems (most common).
- Use `flowchart LR` only for clear linear pipelines.
- Never mix directions without documented rationale.

### Legend and Version Stamp

Every diagram MUST include:
1. **Legend subgraph** at the bottom showing all symbols, edge types, and risk classes used in that specific diagram.
2. **Version stamp** in a comment: `%% Version: {date} | Phase: {N} | System: {name}`

### Density Limit

If a diagram exceeds **15 nodes in a single subgraph** or **25 nodes total**, split into sub-diagrams:
- Split by trust zone, by layer (see mermaid-layers.md), or by functional domain.
- Each sub-diagram must reference the parent and sibling diagrams by filename.

---

## §7 Ownership Markers

Annotate nodes with ownership metadata to clarify responsibility boundaries:

| Marker | Meaning | Syntax in label |
|--------|---------|----------------|
| `[team:Platform]` | Owning team | Append to node label line |
| `[managed]` | Cloud-managed service | Append to node label line |
| `[self-managed]` | Self-hosted / maintained | Append to node label line |
| `[vendor:AWS]` | Vendor-provided | Append to node label line |
| `[control-owner:Security]` | Team responsible for security control | Append to control node label |

### Example

```mermaid
API(["API Gateway\nNode.js · Express · JWT\n[team:Platform] [self-managed]"]):::neutral
RDS[("User DB\nPostgreSQL 15 · RDS\n[vendor:AWS] [managed]")]:::dataStore
WAF[[CloudFront WAF\n[vendor:AWS] [managed]\n[control-owner:Security]]]:::control
```

---

## §8 classDef Reference

Copy-paste this complete block at the **end** of every diagram, after all nodes and edges.

```mermaid
%% === Structural (all layers) ===
classDef neutral fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
classDef external fill:#cce5ff,stroke:#004085,stroke-width:1px,color:#000
classDef dataStore fill:#e2e3e5,stroke:#383d41,stroke-width:1px,color:#000
classDef identity fill:#d4e6f1,stroke:#2980b9,stroke-width:1px,color:#000
classDef secrets fill:#f9e79f,stroke:#f39c12,stroke-width:2px,color:#000
classDef control fill:#abebc6,stroke:#27ae60,stroke-width:1px,color:#000
classDef pipeline fill:#d5dbdb,stroke:#7f8c8d,stroke-width:1px,color:#000
classDef externalDep fill:#f5f5f5,stroke:#333,stroke-width:3px,stroke-dasharray:3,color:#000
classDef outOfScope fill:#eee,stroke:#999,stroke-width:1px,stroke-dasharray:5,color:#666

%% === Risk overlay (L4 only) ===
classDef highRisk fill:#ffcccc,stroke:#cc0000,stroke-width:2px,color:#000
classDef medRisk fill:#ffe6cc,stroke:#cc7a00,stroke-width:2px,color:#000
classDef lowRisk fill:#ccffcc,stroke:#008000,stroke-width:2px,color:#000
classDef noFindings fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#000
classDef attackPath stroke:#cc0000,stroke-width:3px,color:#cc0000
```

**Key distinction**: `noFindings` (grey) is for components with no validated threats. `lowRisk` (green) is for components where analysis explicitly confirms low risk. They are semantically different.

---

## §9 Common Pitfalls

1. **`~~>` is invalid** — use `==>` + `linkStyle N stroke:#cc0000` instead.
2. **`note` blocks are invalid** in flowchart mode — embed metadata in enriched node labels.
3. **`classDef` placement** — define ALL classDef lines at the **end** of the diagram, after all nodes and edges.
4. **`classDef` vs per-node `style`** — use `classDef` for consistent coloring. Use per-node `style` only for trust boundary subgraphs.
5. **Untyped edges** — every arrow MUST use a typed edge from §4. Bare `-->` without a label is a spec violation.
6. **Missing version stamp** — every diagram needs `%% Version: {date} | Phase: {N} | System: {name}`.
7. **Exceeding density** — split diagrams at 15 nodes per subgraph or 25 nodes total.
