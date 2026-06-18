# Product mode — make the doc let a sponsor greenlight and a PM plan: value, scope, metrics, and commitments

**Consumer:** the executive sponsor who funds and prioritizes the work, plus the product manager who plans delivery against it. The sponsor holds the go/no-go and budget; the PM holds the roadmap.
**Done means:** the sponsor can decide to fund or kill this from the doc alone — they see the problem, the value, what it costs, who owns it, and what happens if they say no — and the PM can build a phased plan, set targets, and brief stakeholders without a follow-up meeting.

## Required in the doc
- **Problem & customer** — who hurts, what the pain is, evidence it's real.
- **Capabilities → architecture map** — the features this delivers, traced to the components/boxes that deliver them.
- **Scope & phasing** — MVP, later phases, and explicit non-goals.
- **Do-nothing alternative** — the cost of not building and why the status quo loses.
- **Why now** — the timing driver and what slips if the window is missed.
- **Success metrics** — business-term outcomes with where each is instrumented.
- **Customer impact** — behavior changes, migrations, downtime, deprecations.
- **Commitments** — customer-facing SLAs (with breach terms) kept distinct from internal SLOs; a11y/i18n targets.
- **Cost, timeline & dependencies** — budget envelope, schedule, and what gates it.
- **Ownership / RACI** — the single named team accountable to fund and run this after launch.

## Rubric

### Problem & customer
- **Named customer/segment** — demand the specific user or buyer this serves (segment, persona, internal team), not "users." If the doc can't name who, the sponsor can't size the market or the value.
- **Problem statement with evidence** — the pain in the customer's terms, backed by something real: support tickets, churn data, sales-lost reasons, usage gaps, a regulatory letter. A problem asserted without evidence is a hobby, not a funding case.
- **Frequency & severity** — how often the pain occurs and how much it costs the customer (or us) each time. Drives whether this is worth funding versus a backlog item.
- **Jobs-to-be-done** — what the customer is trying to accomplish, so the sponsor can judge whether the proposed capabilities actually close the gap versus polishing the wrong thing.
- **Who feels it internally** — which internal org bleeds today (support load, ops toil, revenue at risk). Ties the problem to a budget owner who wants it solved.
- **Market size & competitive position** — for customer-facing work, the addressable market (rough TAM/SAM or count of affected accounts) and how this stacks against competitors or the in-house alternative: feature parity, gaps, where we win. Sponsors fund against a market, not a feature; a build with no view of who else serves this can't be sized or differentiated.

### Value & business case
- **Value in business terms** — revenue gained, cost avoided, churn reduced, risk retired, or time saved — quantified or bounded with a stated assumption. "Better UX" is not a business case; "cuts onboarding drop-off from 40% to 20%, ~$X ARR" is. A bounded estimate with its assumptions written down (range, basis, confidence) is acceptable; demand that, not a spurious-precision ROI. Block only when there is no number and no stated basis at all — that is a vision, not a case.
- **Value mechanism** — the causal chain from capability to outcome (build X → customers do Y → metric Z moves). Exposes magical thinking before money is committed.
- **Confidence & assumptions** — the load-bearing assumptions behind the value (adoption rate, conversion lift, pricing) and how confident we are. Lets the sponsor discount the upside honestly.
- **Monetization / who pays** — if customer-facing, how value is captured (new SKU, tier, usage, retention); if internal, whose budget benefits. A capability with no capture path is a cost center.
- **Total cost of ownership** — not just build cost but run cost, support cost, and the opportunity cost of the team not doing something else. Sponsors fund TCO, not the sprint.

### Capabilities mapped to architecture
- **Feature → component trace** — every user-visible capability mapped to the architecture box/service that delivers it. This is the bridge from product intent to the engineering doc; without it the PM can't tell what's real versus aspirational.
- **Capability completeness** — confirm the listed capabilities actually satisfy the stated jobs-to-be-done, with no silent gap where the doc promises an outcome the architecture doesn't deliver.
- **Net-new vs. reused** — which capabilities are new build versus existing components extended. Drives cost and risk; reuse is cheaper and faster, net-new is where schedule slips.
- **Cut-line traceability** — which capabilities are MVP versus deferred, mapped to the same boxes, so descoping is a product decision with a known architecture impact, not a surprise.

### Scope, phasing & non-goals
- **MVP definition** — the smallest releasable thing that delivers real value and tests the core assumption, with its own success criteria. Prevents a 12-month big-bang the sponsor can't course-correct.
- **Phase plan** — phases after MVP, each with the increment of value it adds and a rough sequence. Lets the PM build a roadmap and the sponsor fund in tranches.
- **Explicit non-goals** — what this deliberately does NOT do, in writing. The single highest-leverage scope-control item; unwritten non-goals become scope creep and missed dates.
- **Out-of-scope-for-now vs. never** — distinguish deferred from rejected. Affects architecture decisions (leave a seam vs. don't) and stakeholder expectations.
- **Scope-to-value alignment** — confirm the MVP scope actually maps to the headline value claim; a common failure is an MVP that ships everything except the part that moves the metric.

### Do-nothing alternative
- **Cost of inaction** — what it costs to keep the status quo: lost revenue, growing toil, rising risk, customer attrition, mounting tech debt. The sponsor's real choice is build vs. don't, so the don't case must be stated.
- **Why status quo loses** — why the current workaround, manual process, or competitor's product is no longer acceptable. If the do-nothing case is survivable, the doc should say so honestly — that's a valid finding.
- **Decay over time** — whether the cost of inaction grows, stays flat, or is a one-time miss. Changes the urgency and the funding shape.

### Top risks & mitigations
- **Named top risks** — the handful of things most likely to sink the value, date, or budget (adoption falls short, a key dependency slips, vendor lock-in, a load-bearing assumption is wrong, staffing falls through), pulled into one list instead of scattered across the doc. A sponsor approving a one-pager expects to see the downside named, not to reconstruct it.
- **Likelihood, impact & mitigation** — for each top risk, a rough likelihood/impact read and the mitigation or fallback. A risk with no mitigation is either a blocker to resolve before funding or an exposure the sponsor must consciously accept; force that choice now rather than at the post-mortem.
- **Kill / pivot triggers** — the conditions under which this should be stopped or reshaped (MVP misses its metric, a leading indicator stays flat, a dependency dies). Lets the sponsor fund knowing the off-ramp exists, not feel locked in.

### Why now / timing drivers
- **The driver** — the concrete reason this is now and not next year: a competitor launch, a regulatory effective date, a contractual commitment, a platform EOL, a renewal cycle, a market window. "Leadership wants it" is not a timing driver.
- **The deadline & its source** — the actual date and who set it (regulator, contract, customer, internal OKR), so the PM can work backward and the sponsor knows the date's hardness.
- **What slips if missed** — the consequence of missing the window: lost deal, fine, breach, customer defection, or just opportunity cost. Distinguishes a hard date from a soft preference.
- **Latest-responsible-start** — the date by which funding must be committed for the deadline to be met, accounting for lead times and dependencies. Forces the go/no-go to be timely.

### Success metrics
- **Outcome metrics in business terms** — the 1-3 metrics that define success (adoption, conversion, retention, cost-per-X, NPS, revenue), with current baseline and target value. A doc with no target can't be judged a success or failure later.
- **Counter-metrics / guardrails** — what must NOT get worse (latency, churn elsewhere, support volume, cost). Stops a "win" that's actually a net loss.
- **Instrumentation** — where each metric is measured and by what system (analytics event, data warehouse table, billing system, dashboard). An uninstrumented metric is a wish; demand the source and that it exists or is in scope to build.
- **Measurement window & owner** — when success is evaluated (30/60/90 days) and who owns reporting it. Prevents metrics that nobody ever checks.
- **Leading indicators** — early signals that show the bet is working before the lagging outcome lands. Lets the sponsor decide to double down or cut early.

### Customer & user impact
- **Behavior changes** — what users must do differently, and whether they must be retrained, re-onboarded, or notified. Hidden change-management cost sinks launches.
- **Migration plan** — if existing customers/data move, the path, the effort on them, and who bears it. A migration with no plan is a launch-blocking surprise.
- **Downtime & maintenance windows** — any planned outage, its duration, blast radius, and customer comms. The PM owns the comms; the sponsor owns the risk acceptance.
- **Deprecations & sunsets** — what gets removed, the timeline, the notice period, and the contractual/contractual-comms obligations. Deprecating a thing customers depend on without a runway is a trust and legal hazard.
- **Backward compatibility** — what breaks for whom, and whether old behavior is preserved during transition. Drives both architecture (dual-run, versioning) and customer goodwill.
- **Pricing/packaging impact** — if this changes what customers pay or get, the change and who approves it. Cross-checks with the monetization claim.
- **Go-to-market readiness** — for customer-facing launches, what non-engineering work gates shipping: sales enablement, support/docs, marketing, pricing setup, partner comms, and who owns each. A feature that's code-complete but has no docs, no trained support, and no sales motion isn't launchable; the PM owns this gap and it routinely surfaces late.

### Commitments: SLAs vs. SLOs
- **Customer-facing SLAs** — the contractual availability/performance/support commitments made to customers, stated as commitments (e.g., 99.9% monthly uptime, P1 response in 1h). These bind the company legally; the architecture must be able to meet them.
- **Breach terms & credits** — what the company owes when an SLA is missed (service credits, escalation, termination rights). Real money and real liability; the sponsor must know the downside exposure.
- **Internal SLOs kept distinct** — the engineering targets (often stricter than the SLA, with error budgets) that exist to keep the SLA safe. Demand the doc not conflate the two — an SLO is an internal goal, an SLA is a promise with penalties. Confusing them either over-promises to customers or under-engineers the system.
- **Support model & hours** — the support tier, coverage hours, and escalation path being committed to. A 24/7 P1 SLA implies on-call staffing the run-team must fund — surface it now.
- **Commitment feasibility** — confirm the architecture can actually meet the SLAs claimed. A promised SLA the system can't hit is a future breach the sponsor is unknowingly signing up for.

### Accessibility, i18n & localization
- **A11y conformance target** — the explicit standard and level (e.g., WCAG 2.2 AA) the product commits to, and whether it's a legal requirement (ADA, EN 301 549, Section 508) for the target market. Retrofitting accessibility is far costlier than building it in; an unstated target means it won't be built.
- **Locales in/out of scope** — which languages, regions, currencies, date/number formats, and right-to-left support are in scope for MVP versus later, and which are explicitly out. Drives real architecture (string externalization, currency handling) and real cost.
- **Regulatory/regional constraints** — data residency, regional content, or market-specific rules that gate which regions can launch. The PM needs this for the rollout plan; the sponsor needs it for the addressable market.
- **Localization ownership & cost** — who produces translations and regional QA, and the ongoing cost per added locale. Localization is a recurring run cost, not a one-time build.

### Build vs. buy
- **Build-vs-buy decision in sponsor terms** — the recommendation (build, buy, partner, extend) with the reason framed as cost/time/differentiation, not engineering taste. The sponsor decides where to spend the team's scarce hours.
- **Differentiation test** — whether this capability is core differentiation (build) or commodity (buy). Building commodity infra is the most common way teams waste a budget.
- **Total cost comparison** — build cost+timeline+run vs. vendor license+integration+lock-in, over a 3-year horizon. A vendor that's cheaper to start can be costlier to own.
- **Vendor/partner dependency** — if buy/partner, who the vendor is, the contract status, lock-in risk, and exit cost. Becomes a schedule and continuity dependency the sponsor underwrites.

### Cost, timeline & dependencies
- **Budget envelope** — the order-of-magnitude cost to build and the annual cost to run, with the team size assumed. Sponsors fund a number, not a vision; "TBD" blocks approval.
- **Timeline with milestones** — MVP date and phase dates, with the key milestones a PM can plan against. Tie back to the why-now deadline and flag any gap.
- **Schedule-gating dependencies** — the things outside this team's control that gate the date: another team's deliverable, a vendor, a platform migration, a hiring plan, a procurement cycle. Unsurfaced dependencies are the top cause of missed dates.
- **Critical path** — which dependency is on the critical path and what its slip does to the launch. Lets the PM manage the right risk and the sponsor escalate the right thing.
- **Staffing reality** — whether the team to do this exists, must be hired, or must be pulled off other work (and what that other work loses). The sponsor is approving a reallocation, not just a budget line.

### Cross-team dependencies & agreements
- **Dependency inventory** — every other team this needs something from (API, capacity, data, review, sign-off), what's needed, and by when. The PM coordinates these; missing ones become launch blockers.
- **Agreement status** — for each dependency, whether the other team has actually committed (agreed/in-discussion/unaware), with a name. "We'll need platform team" is not an agreement; an unaware dependency is a fiction in the plan.
- **Conflicts & contention** — where this competes with another team's roadmap or shared-resource capacity, and how it's resolved. Sponsors break ties; surface the tie.
- **Upstream/downstream consumers** — who consumes this team's output and must change to adopt it, and whether they're aligned. A capability nobody downstream adopts delivers zero value.
- **Approval & sign-off chain** — the gating approvals beyond the sponsor that a launch needs: legal/contracts, security review, privacy/compliance, finance/procurement. Each has its own lead time and can veto; an unscheduled legal or security gate is the classic reason a "done" launch sits for weeks.

### Ownership & accountability (RACI)
- **Single accountable team** — the one named team (not "the platform team," not "shared") that owns this capability, staffs it, and funds its run after launch. Diffuse ownership means it rots; the sponsor must know exactly who is on the hook.
- **Run-cost owner** — whose budget pays for hosting, support, on-call, and maintenance once the project funding ends. Build budgets are easy to find; run budgets are where things die.
- **RACI for the launch** — who is Responsible, Accountable, Consulted, Informed across the major workstreams (build, launch, support, comms, metrics). Removes the "I thought you had it" failure.
- **Decision owner / escalation** — who makes the go/no-go and scope-cut calls during delivery, and the escalation path to the sponsor. Keeps delivery moving without re-convening the sponsor for every choice.
- **Post-launch ownership transition** — who owns the thing after the project team disbands, and that they've agreed. Orphaned launches are the sponsor's recurring nightmare.

## Grill order
1. **Problem & named customer with evidence** — if the problem isn't real and owned, nothing else matters; kill or sharpen here first.
2. **Value, market & do-nothing alternative** — the funding case is build-vs-don't against a sized market; both sides and the competitive read must be on the page before a sponsor reads further.
3. **Why now** — establish whether this is timely or can wait; a soft date changes the whole decision.
4. **Scope, MVP & non-goals** — pin the cut line and write the non-goals; this is where scope creep is cheapest to prevent.
5. **Success metrics & instrumentation** — define what winning looks like and confirm it's measurable, not aspirational.
6. **Capabilities → architecture map** — trace features to boxes so product intent and engineering reality are reconciled.
7. **Commitments: SLAs vs. SLOs, a11y, i18n** — surface the binding promises and conformance targets the company is signing up for.
8. **Customer impact: migrations, downtime, deprecations** — make the change-management and trust costs explicit.
9. **Cost, timeline, dependencies, approvals & cross-team agreements** — turn the vision into a fundable, schedulable plan with real commitments and a named approval/sign-off chain.
10. **Top risks, mitigations & GTM readiness** — pull the scattered exposures into one list with mitigations and kill triggers, and check the non-engineering work that gates launch.
11. **Ownership / RACI & run-cost owner** — name the single accountable team and who pays to run it; close before sign-off.
12. **Build-vs-buy & polish** — confirm the spend-where decision and tidy remaining gaps.

## Deliverable
Leave these artifacts in the architecture doc:

- **One-pager decision summary** — problem, customer, value (quantified), cost envelope, timeline, why-now, recommendation. The thing the sponsor reads to greenlight.
- **Capability → architecture trace table** — columns: Capability | Job it serves | Component/box | New or reused | Phase (MVP/P2/…) | Owner.
- **Scope & non-goals table** — columns: In scope (MVP) | Later phase | Out of scope (never) | Rationale.
- **Success metrics table** — columns: Metric | Baseline | Target | Counter-metric guardrail | Instrumentation source | Measurement window | Reporting owner.
- **Commitments register** — columns: Commitment | Type (customer SLA / internal SLO) | Target | Breach term / credit | Owner | Feasible per architecture (y/n). Plus an a11y/i18n row set: conformance target, in-scope locales, out-of-scope locales, residency constraints.
- **Customer impact matrix** — columns: Change | Affected customers/segment | Behavior change | Migration effort | Downtime | Deprecation notice period | Comms owner.
- **Dependency, approval & RACI register** — columns: Dependency / workstream / sign-off | Other team or approver | What's needed | By when | Agreement status (agreed/in-discussion/unaware) | On critical path (y/n) | R/A/C/I. Include legal, security, privacy, and finance/procurement gates as rows.
- **Top-risks register** — columns: Risk | Likelihood | Impact | Mitigation / fallback | Owner | Kill or pivot trigger.
- **GTM readiness checklist** — the non-engineering launch gates (sales enablement, support/docs, marketing, pricing setup, partner comms) with an owner and status for each.
- **Cost & timeline summary** — build cost, annual run cost, run-cost owner, MVP date, phase dates, latest-responsible-start, schedule-gating dependencies.

See also: the engineering and reliability lenses for SLA/SLO feasibility against the architecture, and the compliance lens for the legal and privacy sign-offs named above.
