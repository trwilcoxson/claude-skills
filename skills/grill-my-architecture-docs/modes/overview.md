# Overview mode — cross-cutting triage

Use this when no lens was named. The job here is not to grill everything to enterprise depth — it's to survey the document across every stakeholder lens, find which lenses are weakest, and recommend which deep mode(s) to run next. Grill only the cross-cutting items below. For a lens that's badly underserved, hand off to its mode file rather than improvising depth on the spot.

## Cross-cutting — every architecture doc needs these, regardless of audience

- **Problem and context** — what business problem this solves, who the users are, and what's explicitly out of scope (non-goals).
- **System context diagram** — the system as one box with the external systems, actors, and integrations around it (C4 level 1).
- **Container / component view** — the major moving parts, their responsibilities, and how they talk (sync, async, queue, batch).
- **Quality attributes (NFRs)** — performance, scalability, availability, durability, security, maintainability, each with a concrete target ("p99 < 200ms", not "fast").
- **Key decisions and trade-offs** — the genuinely contested choices, the alternatives weighed, and why this one won.
- **Assumptions and constraints** — what must hold for the design to work; technical, organizational, regulatory, budget.
- **Risks and open questions** — known weaknesses, unknowns, and what would change the design if they resolved differently.
- **Ownership** — the named team that owns, runs, and funds this after launch (not "the platform team").
- **Glossary** — domain and technical terms used consistently; flag any term used two ways.

## Lens triage — one probe each; if it fails, run the deep mode

- **Security** — is there a data-flow diagram with trust boundaries and a threat model? If not → [security](security.md).
- **FinOps** — is there a cost model tied to load, with the main cost drivers named? If not → [finops](finops.md).
- **Compliance / privacy** — is regulated/PII data inventoried with lawful basis, residency, and retention? If not → [compliance](compliance.md).
- **Reliability / SRE** — are there SLOs, failure modes, and a *tested* DR/failover story? If not → [reliability](reliability.md).
- **Product / business** — are scope, non-goals, success metrics, and customer-facing SLAs stated? If not → [product](product.md).
- **Engineering** — are interface contracts, the data model, consistency, and delivery semantics specified? If not → [engineering](engineering.md).
- **Data / analytics** — is the event taxonomy, schemas, and warehouse lineage defined? If not → [data](data.md).
- **Architecture review** — is there target-state alignment, ADRs, lock-in/exit cost, and a legacy sunset plan? If not → [architecture](architecture.md).

## Deliverable

A coverage scorecard (lens → covered / partial / missing) and a recommended order for the deep grills, with the cross-cutting gaps above fixed inline as they're settled.
