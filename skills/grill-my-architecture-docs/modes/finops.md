# FinOps mode — make the doc answer how this system costs money, how cost scales, and how spend is governed

**Consumer:** FinOps lead / cloud economist who owns cloud spend, unit economics, and the run-cost forecast that goes into budget and pricing decisions.
**Done means:** I can model this system's run cost from the doc alone — name every cost driver, compute cost per unit (request/tenant/transaction/active-user) at today's load and at projected load, see a multi-year forecast with stated growth assumptions, and confirm there are budgets, allocation tags, and a hard spend cap that stops a runaway bill without paging me first.

## Required in the doc
- **Cost driver inventory** — every billable resource and rate-card line this system touches.
- **Cost-visibility provenance** — where each number comes from (billing export / CUR, tagged historical data, vendor invoice) vs where it's an estimate.
- **Unit economics model** — cost per chosen business unit, with the formula and current value.
- **Run-cost forecast** — month-1, year-1, year-3 projected spend tied to a load forecast and its assumptions.
- **Commitment & discount plan** — what is on-demand vs committed/reserved/spot, and the coverage target.
- **Cost allocation scheme** — tag taxonomy, showback/chargeback model, shared-cost split rules.
- **Optimization register** — known levers, estimated savings, owner, status.
- **Budget & guardrail register** — budgets, anomaly alerts, hard caps, and the kill-switch for runaway spend.
- **Non-prod cost line** — what dev/staging/test/preview environments cost and how they're contained.

If the cost driver inventory, the unit-economics model, or the forecast is missing, the doc is not reviewable for this lens — start there.

## Rubric

### Cost drivers
- **Compute** — instances/containers/functions, sizes, count, on-demand vs committed, and whether they scale or run 24/7. The single biggest line in most systems; without it nothing else footings.
- **Idle and baseline compute** — what runs at zero traffic (always-on services, min replica counts, warm pools, reserved capacity). Idle baseline sets the floor cost and is where waste hides.
- **Storage by class** — hot/standard/infrequent/archive, volume in GB/TB today and growth rate per month, plus block vs object vs DB storage. Storage compounds; a number with no growth rate is useless for forecasting.
- **Egress and data transfer** — internet egress, cross-AZ, cross-region, and inter-service transfer in GB/month with the per-GB rate. Egress is the line that silently dominates; cross-AZ chatter is the classic surprise.
- **Requests / invocations / operations** — API calls, function invocations, queue operations, S3 PUT/GET, DB IOPS — anything billed per-operation. At scale these out-grow compute; demand the per-million rate and projected volume.
- **Managed-service fees** — managed DB, cache, queue, search, data warehouse, load balancers, NAT gateways, API gateways — provisioned vs serverless and the unit each bills on. NAT gateway and managed-DB minimums routinely beat the app's own compute bill.
- **Per-call third-party / LLM / API fees** — external APIs, payment processors, SMS/email, and LLM token costs (input + output tokens, model tier, per-call retries/agentic loops). Token cost scales with usage non-linearly with prompt size and retries — get tokens-per-request, not just price-per-token.
- **Licenses and seat-based costs** — commercial software, per-seat SaaS, support tiers, observability/SIEM ingest-priced tools. Observability and log ingest are frequently the second-largest bill and get omitted.
- **Support and premium-tier fees** — cloud support plan (often a % of spend), premium SLAs on managed services. A % -of-spend support plan scales with everything else and must be in the model.
- **FinOps/observability stack as its own line** — the cost-management and observability tooling itself (cost platform, metrics/log/trace backend, dashboards) is a recursive cost line that scales with the system it watches. Routinely omitted because it's "infrastructure", but it grows with telemetry volume and must be in the model.
- **Hidden/overhead lines** — backups and snapshots, secrets/KMS, DNS queries, image registry storage, data-pipeline/ETL runs, inter-region replication. Each is small alone; together they're 10-20% nobody budgeted.

### Cost-visibility provenance
- **Source of each number** — every $/mo, volume, and token-per-request figure must cite its origin: billing export/CUR, a tagged historical query, a vendor invoice, or an explicit estimate. A doc can pass on form while the inputs are fabricated guesses; without provenance the whole model is unfalsifiable.
- **Instrumentation actually exists** — confirm the org has the tooling to produce these numbers (billing export enabled, resources tagged historically, per-request token logging) rather than back-filling them by hand. If the visibility isn't there, the first deliverable is standing it up, not the forecast.
- **Estimate vs measured flagged** — measured numbers and estimates must be visually distinguished so the reader knows which lines are load-bearing guesses. An estimate dressed as a measurement is how a forecast quietly goes wrong.

### Unit economics
- **Chosen cost unit** — the doc must name the business unit cost is measured against: per request, per tenant, per transaction, per active user, per GB processed. Without a unit, "cost" is just a monthly number with no decision value.
- **Cost-per-unit formula** — the actual computation (total attributable cost ÷ unit count over a period), with current value. I need to reproduce the number, not trust it.
- **Fixed vs variable split** — what cost is fixed baseline vs what scales per unit. Determines the break-even point and whether the system gets cheaper or more expensive per unit at scale.
- **Marginal cost of the next unit** — cost of one more request/tenant at current scale. Drives pricing floors and free-tier decisions.
- **Unit-cost trend with scale** — does cost/unit fall (economies of scale), stay flat, or rise (e.g., chattier coordination, hot-tenant skew) as volume grows? The whole point of the lens — a flat assertion of "it scales linearly" is not an answer. Falsify it: demand the coordination/fan-out factor (calls or messages per request as N grows), the points where it stops being linear, and the per-unit cost at 10x to prove the claim instead of asserting it.
- **Tenant / cohort skew** — do the top 1% of tenants/users drive a disproportionate share of cost? Heavy-tenant skew breaks blended unit economics and pricing.
- **Cost-to-serve vs price/revenue** — gross margin per unit where the doc touches pricing or a free tier. A feature that costs more to serve than it earns is a sign-off blocker.

### Cost model & forecast
- **Load forecast** — projected request/user/tenant/data volume at month-1, year-1, year-3, with the source of the numbers (sales plan, historical trend, top-down target). The forecast is only as good as this input — demand the assumption, not just the curve.
- **Run-cost projection** — dollar run cost at each horizon, derived from the cost drivers × the load forecast, not a flat guess. Show the math linking load to dollars.
- **Growth assumptions stated** — the explicit % growth, seasonality, and step-changes (launches, regions, migrations) behind the curve. Unstated assumptions make the forecast unauditable.
- **Sensitivity / scenarios** — low/expected/high load cases and what each costs. A single-point forecast is wrong by definition; I need the range to set budgets.
- **Cost cliffs and step functions** — points where cost jumps non-linearly (next instance tier, crossing a free-tier limit, adding a region, sharding the DB). These break linear forecasts and surprise budgets.
- **One-time vs recurring** — migration, data-backfill, and initial-load costs separated from steady-state run cost. Mixing them distorts both the build case and the run forecast.
- **Currency and rate-card basis** — which cloud/region price list, currency, and date the numbers are based on, plus FX exposure for non-USD billing. Rate cards drift; a forecast with no basis ages badly.
- **Multi-cloud / hybrid blending** — where spend spans more than one cloud or on-prem/colo, each must carry its own rate basis and the blend rule that combines them; on-prem capex/amortization and data-center overhead can't be priced on a cloud rate card. A forecast that assumes a single cloud's rate card silently misprices everything off it.

### Commitment & discount strategy
- **On-demand vs committed mix** — what runs on-demand vs reserved/savings-plan/committed-use, with a coverage % target for the stable baseline. Uncovered steady-state baseline is money left on the table.
- **Commitment horizon and risk** — 1yr vs 3yr terms and the lock-in risk if load forecasts miss low. Over-committing on a shrinking workload is as bad as never committing.
- **Spot / preemptible usage** — which workloads are interruption-tolerant and run on spot, with the fallback when capacity is reclaimed. Spot is the largest discount lever and must be tied to a resilience story.
- **Autoscaling and scale-to-zero** — does the system scale with demand and idle resources scale to zero off-hours? Static fleets sized for peak burn money 80% of the time.
- **Right-sizing baseline** — evidence the instance/container sizes are matched to observed utilization, not guessed. Over-provisioned sizing is the most common silent waste.
- **Discount-program eligibility** — committed-spend agreements (EDP/PPA), volume tiers, and marketplace/private pricing the org already has. Architecture choices should route spend toward existing committed discounts.

### Cost allocation & tagging
- **Tag taxonomy** — the required tag keys (team, service, environment, cost-center, product, tenant where feasible) and that every resource carries them. Untagged spend can't be allocated and lands in an unowned bucket.
- **Showback vs chargeback** — whether teams see their cost (showback) or are billed for it (chargeback), and which model this system uses. Sets the accountability and how seriously teams treat the bill.
- **Shared-cost split rule** — how shared resources (clusters, gateways, observability, networking) are apportioned across teams/tenants/products. Shared cost with no split rule becomes a fight and a blind spot.
- **Environment attribution** — prod vs non-prod cost separable from tags. Needed to see how much is spent on environments that earn nothing.
- **Per-tenant cost attribution** — for multi-tenant systems, whether cost can be traced to a tenant (tags, namespaces, metering). Required for per-tenant unit economics and usage-based pricing.
- **Untaggable cost handling** — how costs that can't be tagged (some data transfer, support, shared control planes) are allocated. The residual bucket must have an owner and a rule, not "TBD".
- **Cross-charge / transfer-pricing complexity** — where spend crosses legal entities or business units with markup, recharge, or transfer-pricing rules, the allocation must state the markup and which entity bears it. In larger orgs the booked cost differs from the cloud invoice; ignoring the recharge layer makes both the unit economics and the budget wrong.

### Optimization levers
- **Right-sizing** — plan and cadence for matching resource size to utilization. Recurring, not one-time — utilization drifts.
- **Storage tiering & lifecycle** — lifecycle policies moving cold data to cheaper tiers and expiring it. Without lifecycle rules, hot-tier storage grows forever.
- **Egress reduction** — caching, CDN, co-location of chatty services in one AZ/region, compression. Directly attacks the line most likely to dominate.
- **Caching strategy as a cost lever** — what caching removes from the per-request compute/DB/LLM bill, quantified. Caching is both latency and cost; the doc should claim the cost saving.
- **Idle and orphaned-resource cleanup** — process for finding and killing unattached volumes, idle load balancers, old snapshots, zombie environments. Orphans are pure waste with no offsetting value.
- **Retention and log-volume control** — log/metric/trace retention and sampling tuned against observability ingest cost. Default-retain-everything is a budget leak.
- **Architecture-level levers** — serverless-vs-always-on, batch-vs-stream, single-vs-multi-region where each materially changes cost. The highest-leverage decisions are architectural, not config.
- **Savings estimate per lever** — each lever carries an estimated $/month saving, effort, and owner. A lever with no number can't be prioritized and won't get done.

### Budgets, anomaly detection & guardrails
- **Budgets defined** — monthly/quarterly budget per service/team/environment, tied to the forecast. The number to alert against; absent it, anomaly detection has no baseline.
- **Anomaly detection** — automated detection of spend spikes with alert routing and threshold. Catches the leak before the invoice, not after.
- **Soft alerts vs hard caps** — both an alerting tier (notify at 50/80/100% of budget) and a hard cap that throttles or stops resources. Alerts alone don't stop a runaway bill at 3am.
- **Runaway-spend kill-switch** — a concrete mechanism to halt cost amplification (disable scaling, cut off the expensive third-party/LLM call, throttle ingest) and who can pull it. The single most important guardrail; demand the exact action, not "we'd investigate".
- **Denial-of-wallet spend cap** — the spend ceiling that bounds adversarial cost amplification (the attack/abuse modeling is the security lens's; the dollar cap and what happens when it's hit live here). Without a cap, abuse turns elastic infra into an unbounded bill.
- **Rate limits and quotas as cost control** — per-tenant/per-key quotas that bound usage-driven cost. The proactive complement to the reactive kill-switch.
- **Guardrail ownership and response** — who gets the alert, who can authorize an overage, and the runbook when a cap trips. A cap with no owner and no runbook is theater.

### Build vs buy & run-cost trade-offs
- **Build-vs-buy in dollars** — where the doc chooses to build vs adopt a managed/SaaS option, the comparison must be in $ over a 3-year run, including the engineering cost to build and operate. "Cheaper to build" without the loaded run cost is usually wrong.
- **Managed-service premium justified** — when a pricier managed service is chosen over self-hosting, the premium quantified against the ops cost it removes. Make the trade explicit so it can be revisited at scale.
- **Total cost of ownership** — run cost plus the people cost to operate (on-call, maintenance, upgrades), not just the cloud invoice. Self-hosted "savings" often evaporate once headcount is counted.
- **Cost of exit / lock-in** — switching cost if a proprietary managed service or its pricing changes. Cheap-now, expensive-to-leave is a forecast risk.
- **Carbon / sustainability cost** — where the org carries an internal carbon price, emissions-reporting obligation, or region-choice constraint, the doc must state the carbon footprint of the design and any cost-vs-emissions trade (cheapest region vs greenest region). For orgs with sustainability mandates this is a real constraint on architecture, not a footnote; where there's no such mandate, say so and move on.

### Non-prod & overhead environments
- **Non-prod cost line** — explicit cost of dev, staging, test, and preview/ephemeral environments. Non-prod is routinely 20-40% of total and gets forgotten in forecasts.
- **Non-prod containment** — auto-shutdown off-hours, scale-to-zero, scaled-down sizing, TTL on ephemeral/preview environments. Production-sized non-prod running nights and weekends is pure waste.
- **Data-volume in non-prod** — whether non-prod carries full prod-scale data (and its storage/transfer cost) or subsets. Full-copy non-prod data multiplies the bill silently.
- **DR / standby cost** — cost of warm/hot standby, replicas, and backups for resilience, called out as a deliberate cost-vs-availability trade. Resilience is a cost line that should be a conscious choice, not an accident.

## Grill order
1. **Cost driver inventory** — make them name every billable line; an incomplete inventory invalidates everything downstream.
2. **Cost-visibility provenance** — before trusting any number, confirm it traces to a billing export / tagged history / invoice and isn't a hand-waved guess; flag every estimate as such.
3. **Unit economics** — pin the cost unit, the formula, and the current value; this is the lens's core.
4. **Unit-cost trend with scale** — establish whether cost/unit improves or degrades as load grows; if they claim linear, demand the fan-out factor and the 10x number to prove it.
5. **Load forecast + run-cost forecast** — get the multi-year dollar projection with stated growth assumptions and cost cliffs; reconcile that the cost-driver lines foot to the forecast's month-1 figure.
6. **Budgets, hard caps, and the runaway-spend kill-switch** — confirm spend can't run away unbounded (including the denial-of-wallet dollar cap).
7. **Cost allocation & tagging** — confirm spend is attributable to team/env/tenant, including any cross-entity recharge/markup.
8. **Commitment & discount strategy** — coverage of the stable baseline, spot, scale-to-zero, right-sizing.
9. **Optimization register** — levers with $ estimates and owners.
10. **Non-prod & DR cost** — close the environments that earn nothing.
11. **Build-vs-buy, TCO & lock-in** — polish the dollar trade-offs, lock-in risk, and any carbon/sustainability constraint.

## Deliverable
Leave these artifacts in the architecture doc:

- **Cost driver table** — columns: Driver | Resource/service | Billing unit | Rate-card basis | Current volume | Monthly growth % | Current $/mo | On-demand vs committed | Source (CUR/invoice/estimate).
- **Unit economics block** — the cost unit, the formula, current $/unit, fixed-vs-variable split, marginal cost of the next unit, and a curve or table of $/unit at current / year-1 / year-3 load.
- **Run-cost forecast table** — rows: month-1, year-1, year-3, each with low/expected/high scenario columns; plus a stated-assumptions list (growth %, seasonality, step-changes, rate-card date/currency) and a flagged list of cost cliffs.
- **Commitment & discount plan** — baseline coverage target %, commitment term, spot-eligible workloads, scale-to-zero schedule, right-sizing cadence.
- **Tagging & allocation matrix** — required tag keys, showback/chargeback model, shared-cost split rule, per-tenant attribution method, untaggable-cost owner.
- **Optimization register** — columns: Lever | Est. $/mo saving | Effort | Owner | Status.
- **Budget & guardrail register** — columns: Scope (service/team/env) | Budget $ | Alert thresholds | Hard cap action | Kill-switch mechanism | Owner | Runbook link. Include the denial-of-wallet spend cap as a row.
- **Non-prod & DR cost line** — per-environment cost, containment mechanism (auto-shutdown/TTL/scale-down), data-volume policy, and DR/standby cost as a stated availability trade-off.
- **Reconciliation note** — the sum of the cost-driver table's Current $/mo must foot to the forecast's month-1 figure; show the total and flag any gap. This is the internal-consistency check a real reviewer runs first, and a mismatch means one of the two artifacts is wrong.
