## ADDED Requirements

### Requirement: Structure-only verification
The eval SHALL verify only the presence, shape, and internal consistency of each visual against the
manifest id-sets and counts. It SHALL NOT judge content correctness; a visual that is present and
structurally consistent but analytically wrong SHALL still pass the deterministic check, leaving
correctness to the diagram judge.

#### Scenario: Present but wrong content
- **WHEN** a required visual is present and structurally consistent with the manifests but its analysis is wrong
- **THEN** the deterministic check passes and the error is reported only by the diagram judge

### Requirement: Conditional gating, never forced
Each visual SHALL be verified only when its precondition holds; when the precondition is false the
check SHALL be skipped, not failed, so a visual is never forced on a system that does not need it.

#### Scenario: Precondition false
- **WHEN** a system has no authentication surface
- **THEN** the auth-sequence check is skipped and its absence is not a defect

#### Scenario: Precondition true and visual missing
- **WHEN** a precondition holds but the required visual is absent
- **THEN** the check records a defect

### Requirement: Gating uses skill-declared facts, not code inference
Verification thresholds SHALL be derived from facts the skill emitted (declared kill chains, boundary
kind, dependency manifest), never from the eval inferring content such as clustering findings into
chains or deciding a dependency is risky.

#### Scenario: Required tree count
- **WHEN** the eval determines how many attack trees are required
- **THEN** the count is the number of kill chains the skill declared in the findings manifest, not a count the eval computes by clustering findings

### Requirement: Per-visual structure checks
The eval SHALL apply structure/consistency checks per visual: attack tree (single root, ≥1 AND/OR
gate, connected DAG, leaf techniques ⊆ findings techniques); sequence diagram (≥2 participants, ≥1
message, balanced block keywords, participants ⊆ recon ids); STRIDE matrix (seven category columns,
zero blank cells, set-equality between finding element/category pairs and matrix cells); heat map
(5×5 shape, every finding placed once at its own L×I cell, band == band(L×I)); ATT&CK layer
(technique set == distinct findings techniques, valid JSON keys/regex); attack-flow (connected
digraph, distinct source and sink, nodes reference finding/asset ids); RBAC matrix (≥2 role rows,
full population, anonymous row, columns ⊆ recon ids); SBOM graph (rooted, ≥1 external-dependency
leaf, nodes ⊆ recon external deps).

#### Scenario: STRIDE matrix faithful to findings
- **WHEN** the STRIDE matrix is verified
- **THEN** the set of (element, category) pairs carrying a finding id equals the set of (element, category) pairs in the findings, and no cell is blank

#### Scenario: Heat-map cell consistent with score
- **WHEN** a finding appears in the heat map
- **THEN** it is placed in the cell matching its own likelihood and impact and the cell's band equals band(likelihood × impact)

### Requirement: Diagram judge assesses correctness of the new visuals
The diagram judge SHALL assess the semantic correctness of each new visual against the real system —
attack-tree gate logic, sequence-protocol accuracy, matrix n/a justification, ATT&CK mapping
correctness, attack-flow realism, RBAC permission correctness, SBOM accuracy — separately from the
deterministic structure checks.

#### Scenario: Judging an attack tree
- **WHEN** the diagram judge reviews an attack tree
- **THEN** it assesses whether the root is the true objective and whether AND/OR gates are logically correct, independent of the structural pass
