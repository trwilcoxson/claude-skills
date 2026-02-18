# Analysis Checklists

## Contents
- Phase 1 — Reconnaissance Checklist
- Phase 2 — Structural Diagram Checklist
- Phase 3 — Threat Identification Checklist
- Phase 4 — Risk Quantification Checklist
- Phase 5 — False Negative Hunting Checklist
- Phase 6 — False Positive Validation Checklist
- Phase 7 — Visual Validation Checklist
- Phase 8 — Final Report Checklist

Use these checklists to ensure thoroughness at each phase. Check off items as you complete them. For large systems, save each phase's output to its own file as noted.

## Phase 1 — Reconnaissance Checklist

### Input Analysis
- [ ] Examined all provided images and documentation
- [ ] Identified business context, compliance requirements, and risk appetite (PASTA Stage 1)

### Code Scanning
- [ ] Code scanning complete: entry points, auth, authz, data stores, integrations, IaC, network topology

### Inventories
- [ ] Threat actor profiles: 3-5 actors spanning external and internal categories, each with type/motivation/capability/access/relevance
- [ ] Attack surface catalog: every entry point with name, location, protocol, auth, exposure, input types
- [ ] Security control inventory: all controls with implementation location, coverage, strength, and gap analysis
- [ ] Asset inventory: all data assets classified, all actors enumerated, tech stack documented
- [ ] All assumptions explicitly stated

### Output
- [ ] Structured reconnaissance summary produced
- [ ] Output saved to file (01-reconnaissance.md) for large systems

## Phase 2 — Structural Diagram Checklist

### Layer Strategy
- [ ] Layer strategy determined per mermaid-layers.md §6 (≤5 → 2-layer, 6-20 → 4-layer, >20 → 4-layer + sub-diagrams)
- [ ] L1 (Architecture) produced with neutral styling only
- [ ] L2 (Trust & Identity) produced with boundary subgraphs and AUTH/ADMIN edges (if 4-layer)
- [ ] L3 (Data) produced with classification zones and KEY edges (if 4-layer)

### Structural Content
- [ ] Every component from Phase 1 inventory appears in the diagram
- [ ] All components use neutral styling (:::neutral), NOT risk-based colors
- [ ] External entities use :::external styling
- [ ] Data stores use :::dataStore styling
- [ ] Symbol taxonomy followed from mermaid-spec.md §3 (correct shapes per type)

### Typed Edges
- [ ] Every edge has a typed label — no bare `-->` without label text
- [ ] Edge prefixes match the 8-type spec: (none), [CTRL], [AUTH], [KEY], [ADMIN], [ASYNC], [REPL], [BUILD]
- [ ] Edge labels include protocol, data type, and sensitivity classification
- [ ] linkStyle colors applied for typed edges (AUTH=blue, ADMIN=red, ASYNC=green, REPL=purple, BUILD=orange)

### Ownership & Metadata
- [ ] Ownership markers present on nodes: [team:X], [managed], [self-managed], [vendor:X]
- [ ] Component metadata in enriched node labels (Name + Tech + Security Features)
- [ ] Version stamp comment present: `%% Version: {date} | Phase: 2 | System: {name}`

### Quality
- [ ] NO threat annotation notes present (analysis has not happened yet)
- [ ] Structural legend included (no risk colors in legend)
- [ ] Mermaid syntax is valid (classDef at end, proper quoting, correct shapes)
- [ ] No orphaned nodes (every node has at least one connection)
- [ ] Layout direction is appropriate (TD for hierarchical, LR for pipeline)
- [ ] Density within limits (≤15 nodes per subgraph, ≤25 total)
- [ ] Validated against mermaid-review-checklist.md
- [ ] Output saved to file (02-structural-diagram.md) for large systems

## Phase 3 — Threat Identification Checklist

Identify threats ONLY in this phase. Do NOT assign likelihood, impact, or severity scores.

### STRIDE-LM Assessment
- [ ] All seven STRIDE-LM categories assessed for every component and data flow
- [ ] AI/ML and agentic threats assessed (if applicable, otherwise N/A)

### Cross-Framework Classification
- [ ] Cross-framework classification complete (MITRE, OWASP, CWE, CIA) using verified IDs only

### Design-Level and Domain Assessment
- [ ] Design-level and domain-specific assessment complete (secure design principles, zero trust, business logic, cloud-native, API depth as applicable)

### Auth Sequence Diagram
- [ ] Auth sequence diagram produced if system has AuthN/AuthZ (mermaid-diagrams.md §3)
- [ ] Participant IDs match node IDs from Phase 2 DFD
- [ ] Both success and failure paths shown

### Output Format
- [ ] Each threat has unique ID (TM-001, TM-002, ...)
- [ ] Each threat has: title, STRIDE-LM category, affected components, cross-framework IDs, description
- [ ] No likelihood, impact, or severity scores assigned (that is Phase 4)
- [ ] Framework IDs verified against reference tables
- [ ] Output saved to file (03-threat-identification.md) for large systems

## Phase 4 — Risk Quantification Checklist

Score each threat identified in Phase 3.

- [ ] Relevant threat actor(s) selected from Phase 1 profiles for each threat
- [ ] Attack path modeled for each threat (PASTA Stage 6: entry point, steps, preconditions, controls to bypass)
- [ ] Attack paths reference Phase 1 attack surface catalog for entry points
- [ ] Attack paths reference Phase 1 control inventory for existing mitigations
- [ ] Likelihood scored 1-5 for each threat with written justification
- [ ] Likelihood justified against selected threat actor's capability and access level
- [ ] Business impact assessed across all four dimensions (PASTA Stage 7: financial, operational, reputational, regulatory)
- [ ] Impact references Phase 1 asset inventory for data sensitivity context
- [ ] Impact scored 1-5 for each threat (highest dimension) with written justification
- [ ] OWASP Risk Rating calculated (Likelihood x Impact) for each threat
- [ ] Severity band assigned (LOW 1-4, MEDIUM 5-9, HIGH 10-16, CRITICAL 17-25)
- [ ] Scores are consistent: similar threats have similar scores
- [ ] Output saved to file (04-risk-quantification.md) for large systems

## Phase 5 — False Negative Hunting Checklist

- [ ] Every low-risk or no-findings component re-examined with adversarial mindset
- [ ] 3-5 complete kill chains traced with coverage gaps flagged
- [ ] Insider threat, supply chain, and temporal threat scenarios modeled
- [ ] Trust boundary bypass paths, data aggregation, side-channel, and cascade failure risks assessed
- [ ] AI/ML-specific threats reviewed in depth (if applicable)
- [ ] Newly discovered threats assigned IDs and scored using Phase 4 methodology
- [ ] Attack tree diagrams produced for kill chains with ≥3 steps (mermaid-diagrams.md §2)
- [ ] Output saved to file (05-false-negative-hunting.md) for large systems

## Phase 6 — False Positive Validation Checklist

### Per Finding
- [ ] Concrete step-by-step attack path documented (or finding downgraded/removed)
- [ ] Existing mitigating controls checked against Phase 1 Security Control Inventory
- [ ] Context validated against actual deployment model and data sensitivity
- [ ] Confidence level assigned (HIGH / MEDIUM / LOW)
- [ ] Finding deduplicated against overlapping cross-framework findings

### Framework ID Verification
- [ ] Every MITRE ATT&CK technique ID cross-referenced against frameworks.md reference table
- [ ] Every CWE ID cross-referenced against frameworks.md reference table
- [ ] IDs not found in reference tables removed or replaced with plain-text description
- [ ] No fabricated or unverified framework IDs remain in findings

### Overall Validation
- [ ] All findings lacking realistic attack paths removed or marked as theoretical
- [ ] Severity ratings consistent across similar findings
- [ ] OWASP Risk Rating scores (Likelihood x Impact) re-validated
- [ ] No critical findings accidentally downgraded
- [ ] Output saved to file (06-validated-findings.md) for large systems

## Phase 7 — Visual Validation Checklist

### L4 Threat Overlay Production
- [ ] Started from L1 structural diagram as base
- [ ] Components with CRITICAL/HIGH findings colored :::highRisk
- [ ] Components with MEDIUM findings colored :::medRisk
- [ ] Components with only LOW findings colored :::lowRisk
- [ ] Components with NO validated findings kept as :::noFindings (not :::lowRisk)
- [ ] Enriched node labels with machine-parseable annotations: `Name\nTech\n⚠ STRIDE · LxI=Score BAND\nCWE IDs`
- [ ] STRIDE abbreviations use single letters (S,T,R,I,D,E,LM)
- [ ] LxI calculation correct, BAND matches score (CRITICAL 20-25, HIGH 12-19, MEDIUM 6-11, LOW 1-5)
- [ ] CWE IDs verified against frameworks.md
- [ ] Attack path overlays using ==> thick arrows with red linkStyle (L4 only)
- [ ] Attack path overlays appear ONLY in L4 (not in L1-L3)

### Completeness
- [ ] Every component from Phase 1 inventory present
- [ ] Every data store represented
- [ ] Every external entity and actor represented
- [ ] Every data flow identified in reconnaissance drawn
- [ ] All trust boundaries drawn
- [ ] New components or flows discovered in Phases 3-5 added

### Accuracy
- [ ] Trust boundaries correctly reflect validated security zones
- [ ] Data flow directions correct
- [ ] Component types use correct shapes
- [ ] Data flow labels accurate

### Visual Quality
- [ ] No orphaned nodes
- [ ] Consistent layout direction
- [ ] Subgraph nesting clean and not overly deep
- [ ] Labels readable and concise
- [ ] Risk-overlay legend present and accurate (includes noFindings explanation)

### Review Checklist
- [ ] L4 diagram validated against mermaid-review-checklist.md (all 8 sections)
- [ ] Version stamp present
- [ ] Visual completeness checklist updated with risk overlay completion status

### Output
- [ ] L4 Mermaid diagram produced in fenced code block
- [ ] Saved as {name}-L4-threat.mmd
- [ ] Output saved to file (07-final-diagram.md) for large systems

## Phase 8 — Final Report Checklist

### Report Completeness
- [ ] Executive summary with threat counts, top 3 risks, and posture rating
- [ ] System overview, asset inventory, threat actor profiles, and attack surface summary
- [ ] Final Mermaid diagram with risk-overlay legend
- [ ] Threat summary table and detailed findings grouped by severity
- [ ] Remediation recommendations with dependency ordering and implementation waves
- [ ] LINDDUN privacy assessment, positive observations, false negative results, and assumptions
- [ ] Update triggers and review cadence defined
- [ ] Component and data flow names consistent between diagram and findings
- [ ] Complete report saved to file (08-threat-model-report.md)
