## ADDED Requirements

### Requirement: Attack trees for multi-step kill chains
The skill SHALL render one attack tree per declared kill chain when the assessment declares three or
more kill chains, as a Mermaid `flowchart TD` with a single root goal node, AND/OR refinement gates,
and leaf technique nodes (Schneier convention). When fewer than three kill chains are declared, the
attack tree is not required.

#### Scenario: Three or more kill chains
- **WHEN** the findings manifest declares three or more kill chains
- **THEN** the report contains one attack-tree flowchart per declared chain, each with a single root goal, at least one AND or OR gate, and technique leaves drawn from the findings

#### Scenario: Few or no multi-step chains
- **WHEN** fewer than three kill chains are declared
- **THEN** no attack tree is required and its absence is not a defect

### Requirement: Authentication / scenario sequence diagram
The skill SHALL render a Mermaid `sequenceDiagram` when the system has an authentication or
authorization surface, with participants that correspond to diagram node ids and both a success path
and an explicit failure path.

#### Scenario: Auth surface present
- **WHEN** recon shows an authentication/authorization surface (an auth-related entry point, or a finding tagged Spoofing or Elevation of Privilege)
- **THEN** the report contains a sequence diagram whose participants map to DFD nodes and that shows success and failure paths

### Requirement: STRIDE-per-element coverage matrix
The skill SHALL render a fully populated STRIDE-per-element coverage matrix for every threat model:
rows are the discovered elements (or trust-zone groups for large systems), columns are the seven
STRIDE-LM categories, and every cell carries a finding id, an `n/a` marker, or a `clean` marker — no
blank cells.

#### Scenario: Every assessment
- **WHEN** a threat model is produced
- **THEN** the report contains a matrix with the seven STRIDE-LM columns and a non-blank cell for every element/category pair

### Requirement: Likelihood by Impact risk heat map
The skill SHALL render a 5×5 Likelihood-by-Impact risk heat map plotting every scored finding at the
cell matching its likelihood and impact, banded by the OWASP severity bands the skill already uses.

#### Scenario: Scored findings exist
- **WHEN** the findings manifest contains at least one finding with likelihood and impact scores
- **THEN** the report contains a 5×5 grid placing each finding id at its (likelihood, impact) cell

### Requirement: MITRE ATT&CK technique layer
The skill SHALL render a MITRE ATT&CK technique view (a markdown heatmap, plus a Navigator JSON layer
when five or more techniques are mapped) covering the techniques referenced by the findings.

#### Scenario: Findings map to techniques
- **WHEN** at least one finding carries a MITRE technique id
- **THEN** the report includes an ATT&CK technique view whose techniques are exactly those referenced by the findings

### Requirement: Attack-flow kill-chain graph
The skill SHALL render a directed attack-flow graph for each top declared kill chain when three or
more kill chains are declared, showing the temporal/lateral progression from initial access to
objective.

#### Scenario: Top kill chains
- **WHEN** three or more kill chains are declared
- **THEN** the report contains a directed attack-flow graph for each top chain with a distinct entry and objective

### Requirement: RBAC authorization matrix
The skill SHALL render a role-by-resource authorization matrix, including an explicit
anonymous/unauthenticated row, when the system has two or more declared roles or principals.

#### Scenario: Multiple roles
- **WHEN** two or more roles/principals are declared for the system
- **THEN** the report contains a fully populated role-by-resource matrix including an anonymous row

### Requirement: SBOM dependency graph
The skill SHALL render a dependency graph rooted at the application showing external dependencies when
the recon declares external dependencies backed by a manifest.

#### Scenario: External dependencies with a manifest
- **WHEN** recon declares external dependencies and a dependency manifest is in evidence
- **THEN** the report contains a dependency graph rooted at the application with external-dependency leaves

### Requirement: Neutral verification facts emitted by the skill
The skill SHALL emit neutral structured facts so verification can gate on declared facts rather than
inferring content: declared kill chains (id, goal, member finding ids), trust-boundary kind, and a
dependency manifest/risk reference. These facts express the LLM's reasoning, not the eval's.

#### Scenario: Kill chain declared
- **WHEN** the analysis identifies a multi-step kill chain
- **THEN** the findings manifest lists it under kill_chains with a goal and the member finding ids

#### Scenario: Trust boundary classified
- **WHEN** recon records a trust boundary
- **THEN** the recon manifest records its kind (e.g. process, network, trust, tenant, cicd, region)

### Requirement: Diagram acceptance gate covers applicable visuals
The skill's Diagram acceptance gate SHALL require every applicable visual (by its precondition) to be
present before a threat model is finalized, or explicitly marked not-applicable with a reason.

#### Scenario: Finalizing a model with an auth surface
- **WHEN** the system has an auth surface and the model is being finalized
- **THEN** the acceptance gate requires the sequence diagram to be present before the model is accepted
