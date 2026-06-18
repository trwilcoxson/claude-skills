# Compliance mode — make the doc produce the data-governance and control facts an auditor or regulator will demand

**Consumer:** Privacy officer / compliance lead (DPO, SOC 2 control owner, regulatory liaison) who signs the system off as defensible to an auditor or regulator.
**Done means:** From the doc alone the consumer can name every applicable regime and the in-scope components, point to a complete inventory of personal/sensitive data with lawful basis and purpose per data class, prove retention/deletion and data-subject-rights are architecturally achievable, identify every sub-processor and transfer path, and show the system can produce the evidence (logs, access reviews, affected-record lists within breach clocks) that an audit or regulatory inquiry will ask for — without a verbal walkthrough.

## Required in the doc
- **Regulatory scope statement** — which regimes apply (GDPR/UK GDPR, CCPA/CPRA, HIPAA, PCI-DSS, SOC 2, sector/regional add-ons) and which components/data flows fall in scope of each; for PCI, the CDE boundary and target SAQ/ROC route. If the system claims no personal data at all, a field-level proof of that claim instead.
- **DPIA / PIA where triggered** — the high-risk-processing assessment (GDPR Art. 35 or equivalent) as a referenced artifact when a threshold is crossed.
- **Data inventory / record of processing (RoPA-style)** — every personal/sensitive data class, where it lives, where it flows, who touches it.
- **Lawful-basis & purpose register** — per data class: lawful basis (GDPR Art. 6 / special-category Art. 9), declared purpose, consent state if relied on.
- **Retention & deletion schedule** — per data class: retention period, trigger, deletion mechanism, legal-hold interaction.
- **Data-subject-rights (DSR/DSAR) design** — how access, portability, correction, deletion, objection are fulfilled and within what SLA.
- **Cross-border transfer map** — data residency per store, transfer mechanism (SCCs/adequacy/BCRs) for each border crossing.
- **Sub-processor register** — third parties processing personal data, with DPA status.
- **Control & evidence catalog** — the controls protecting the data and the audit evidence the design emits.
- **Breach-response architecture** — detection, declaration path, regulatory clocks, and the means to enumerate affected records.
- **Automated-decision / AI disclosure** — any profiling or automated decisioning that materially affects a person, plus human-review/appeal path.

## Rubric

### Regulatory scope and applicability
- **Regime enumeration** — demand an explicit list of every regime in scope and why (data subjects in EU/UK → GDPR; California residents → CCPA/CPRA; PHI + covered entity/BA → HIPAA; cardholder data → PCI-DSS; customer trust commitments → SOC 2). Missing regimes mean unscoped obligations surface at audit.
- **In-scope component mapping** — each regime tied to the specific services, datastores, and flows it governs. "The whole system is GDPR-compliant" is not auditable; the auditor scopes by data flow.
- **Out-of-scope justification** — where a component is claimed out of scope (e.g., tokenized so PCI scope is reduced, fully anonymized so GDPR no longer applies), demand the technical reason and a re-identification-risk argument. Bad scope reduction is the most common audit finding.
- **Role determination** — controller vs processor (GDPR), business vs service provider (CCPA), covered entity vs business associate (HIPAA), merchant level / SAQ type (PCI). Obligations and liability differ entirely by role; the doc must state which the system is for each data class.
- **Jurisdiction triggers** — what user attribute or data flow pulls each regime in (residency, citizenship, where processing happens). Needed to know when a new market expansion changes the obligation set.
- **Proof of no-PII (when claimed out of scope entirely)** — if the team claims the system processes no personal data and is therefore unscoped, do not accept the assertion: demand a field-by-field walk of every store, log, and free-text/attachment surface showing none carries an identifier, pseudonym, device/IP, or data that re-identifies in combination. "No PII" is the cheapest way to skip the whole rubric and the easiest claim to get wrong; an unproven no-PII claim is itself the top finding.
- **DPIA / PIA threshold gate** — determine whether the processing crosses a mandatory-assessment threshold (GDPR Art. 35 high-risk: large-scale special-category, systematic monitoring, automated decisions with significant effect; equivalent PIA triggers elsewhere). Where it does, demand the DPIA exists and is referenced as a required artifact, not folded into the LIA or AI items. Proceeding with high-risk processing absent a DPIA is a standalone regulatory violation independent of every other control.

### PII / sensitive-data inventory
- **Per-field data classification** — every field carrying personal data classified (identifier, contact, financial, health, biometric, location, behavioral, special-category/Art. 9, children's data). Without field-level classification the minimization and basis tests below cannot be applied.
- **Special-category and regulated subsets** — flag Art. 9 special-category data, PHI (HIPAA), and cardholder data (PAN/CVV/track) explicitly; they carry stricter basis, encryption, and handling rules. CVV must never be stored post-auth (PCI).
- **PCI scope segmentation and SAQ type** — where cardholder data is in scope, demand the cardholder data environment (CDE) boundary: which components store/process/transmit PAN, how they are network-segmented from out-of-scope systems, and what brings adjacent systems into scope. State the assessment route (SAQ A / A-EP / D, or ROC) the architecture targets and what it assumes to qualify (e.g., SAQ A requires fully outsourced payment pages — an iframe/redirect, not a self-hosted form). The wrong segmentation or SAQ assumption silently pulls the whole stack into PCI scope and invalidates the assessment.
- **Children's / minors' data** — flag any processing of minors (GDPR Art. 8 age of consent, COPPA, CPRA opt-in). Triggers parental consent and age-gating obligations.
- **Data-flow and lineage** — for each data class, where it is collected, every store it lands in, every downstream/derived copy (caches, search indexes, analytics warehouse, backups, logs, ML feature stores). Shadow copies are where deletion and breach scope break.
- **Derived and inferred data** — inferences, scores, profiles built from raw PII are themselves personal data; demand they appear in the inventory with their own basis. Commonly missed.
- **Free-text and unstructured stores** — flag fields/blobs/attachments/logs where PII can leak unstructured (support notes, uploaded docs). These defeat field-level deletion and DSAR unless explicitly handled.
- **System of record vs replicas** — name the authoritative store per data class. Without a single source of truth, correction and erasure have no anchor to propagate from and a DSAR can return inconsistent copies — the request can't be proven fulfilled.

### Data minimization — GDPR Art. 5(1)(c) / HIPAA minimum-necessary
- **Necessity test per field** — for each collected field, demand the stated reason it is necessary for the declared purpose. Fields with no necessity justification are minimization findings and must be dropped or justified.
- **Collection vs use gap** — flag data collected "in case it's useful" with no current purpose. Speculative collection violates minimization.
- **Granularity reduction** — challenge whether full-precision data is needed where coarser suffices (exact DOB vs age band, precise geo vs region, full PAN vs last-4). Demand the least-granular form that meets the purpose.
- **Minimum-necessary access (HIPAA)** — where PHI is in scope, access scoped to the minimum needed per role/task, not blanket.
- **Pseudonymization / anonymization posture** — where data can be pseudonymized or anonymized at rest or in analytics, demand it; note that pseudonymized data is still personal data (re-identifiable) while truly anonymized data leaves scope. Demand the line be drawn explicitly with a re-identification argument.

### Purpose limitation — GDPR Art. 5(1)(b)
- **Purpose bound per data class** — each data class tied to one or more declared, specified purposes. Undeclared-purpose data is a finding.
- **Secondary-use control** — flag any reuse of data for a purpose beyond collection (analytics, product metrics, ML training, model fine-tuning). Demand a compatibility assessment or a fresh lawful basis/consent for the new purpose. Reusing customer data to train models without fresh basis is a high-frequency regulator target.
- **ML/analytics basis cross-check** — explicitly tie any pipeline feeding a warehouse, BI tool, or model back to a purpose and basis in the register. The Art. 5(1)(b) purpose-limitation check and the Art. 6 lawful-basis check are separate gates — see Lawful basis below — and the doc must satisfy both, not conflate them.
- **Purpose-based access segregation** — controls that prevent data collected for purpose A being technically reachable for purpose B (separate datasets, row/column policies, query governance). Architectural purpose limitation, not just policy.

### Lawful basis and consent — GDPR Art. 6 / Art. 9
- **Basis per data class** — the specific Art. 6 basis (consent, contract, legal obligation, vital interests, public task, legitimate interests) named per class; Art. 9 condition additionally for special-category. "We're compliant" without a named basis is not reviewable. This is a distinct axis from minimization/purpose (Art. 5): a field can pass necessity and purpose yet still lack a valid basis — demand both be present.
- **Consent capture and proof** — where consent is the basis, how it is captured, versioned, timestamped, and stored as evidence; how granular it is; how withdrawal is recorded and propagated downstream. Consent you can't prove is no consent.
- **Consent withdrawal propagation** — withdrawing consent must reach every downstream copy (suppress marketing, halt processing, stop ML use) within an SLA. Demand the mechanism and the latency.
- **Legitimate-interest balancing** — where LI is relied on, demand the LIA (balancing test) is referenced and the opt-out path exists.
- **CCPA/CPRA opt-out and sale/share** — "Do Not Sell or Share My Personal Information," global privacy control (GPC) honoring, and sensitive-PI use-limitation opt-out. Distinct from GDPR opt-in; demand the architectural handling.

### Data residency and cross-border transfer
- **Residency per store** — physical/cloud region of each datastore, backup, and replica holding personal data. Residency commitments and regime applicability turn on this.
- **Transfer mechanism per crossing** — every border the data crosses tied to a valid mechanism (adequacy decision, SCCs, BCRs, derogations). Post-Schrems II, US transfers need SCCs + transfer impact assessment or DPF certification. Unmechanized transfers are unlawful.
- **Sub-processor location** — where each third party processes/stores data, including their sub-processors and support/access from other regions (e.g., follow-the-sun support touching EU data from outside).
- **Data-localization constraints** — sector/country localization rules (e.g., certain health, financial, government data must stay in-country). Demand these are encoded as architectural constraints, not informal expectations.
- **Backup and DR region scope** — DR/backup regions are transfers and stores too; demand they appear in the residency map. Routinely forgotten.

### Retention, deletion, and legal hold
- **Retention period per data class** — concrete period and the trigger that starts the clock (account closure, last activity, transaction date). "Indefinite" or unstated retention is a finding.
- **Deletion mechanism and proof** — how deletion actually executes across every store, index, cache, and backup; whether it's hard delete, crypto-shred, or soft delete; and what evidence proves it happened. Soft delete that leaves data reachable is not deletion.
- **Backup-expiry deletion** — how deleted records age out of backups given backups can't be surgically edited; demand the backup retention window and the documented gap during which deleted data still exists in backups.
- **DSAR erasure path** — how a right-to-erasure request propagates to every store including derived data, search indexes, logs, and ML training sets; the SLA; and the exceptions (legal obligation to retain). Tie this back to the data-flow/lineage inventory — erasure can only be proven complete if every copy is inventoried.
- **Legal hold vs deletion** — a litigation/legal hold must suspend the erasure and routine-deletion pipeline for the held records without breaking routine deletion for everyone else. Demand the hold mechanism, its scope granularity (per subject/matter), who can place/release it, and the audit trail. Deleting data under hold is spoliation; failing to delete absent hold violates retention.
- **Retention enforcement automation** — whether retention is enforced by an automated job or relies on manual cleanup. Manual retention does not survive audit.

### Data-subject / consumer rights
- **Access & portability** — how a subject's full data set is assembled across all stores for an access request, and exported in a portable, machine-readable form. Demand the assembly mechanism, not a promise.
- **Correction / rectification** — how corrections propagate from the system of record to all replicas and derived data.
- **Deletion / erasure** — covered under Retention above; cross-check that the DSR design and the deletion design name the same mechanism.
- **Objection / restriction** — how processing is halted or restricted for a subject without deleting (Art. 18/21), including stopping ML use and marketing.
- **Identity verification** — how a requester is verified before a DSR is fulfilled, to prevent rights requests becoming an account-takeover or data-exfiltration vector. Both over- and under-verification are findings.
- **Request SLA and tracking** — the regulatory response clock (GDPR 1 month, CCPA 45 days) and the system that logs, tracks, and evidences each request and its fulfillment.
- **Authorized-agent and bulk requests** — handling of agent-submitted (CCPA) and high-volume requests without manual bottleneck.
- **Transparency notice matches actual processing (Art. 13/14)** — the external-facing privacy notice must disclose the real processing: data categories collected, purposes, lawful bases, recipients/sub-processors, retention, transfers, and rights. Demand a reconciliation between the notice and the RoPA/sub-processor/transfer artifacts — a purpose, vendor, or transfer that exists in the architecture but not in the notice (or vice versa) is a transparency violation, and it is a different finding from an incomplete internal RoPA. Internal records being correct does not make the subject-facing disclosure correct.

### Sub-processors, vendors, and contracts
- **Sub-processor register** — every third party that processes personal data (cloud, SaaS, analytics, support, payment, email/SMS, LLM/AI APIs), what data each receives, and for what purpose. LLM/AI vendors are frequently omitted and are processors.
- **DPA / BAA coverage** — a signed DPA (GDPR), service-provider contract (CCPA), or BAA (HIPAA) per processor handling regulated data; flag any vendor receiving data without one.
- **Sub-processor change management** — how new sub-processors are vetted and how customers are notified (many DPAs require notice + objection window).
- **Vendor data flows in the inventory** — vendor egress points appear in the data-flow map and transfer map, not just in a contracts list.
- **AI/LLM data handling clause** — for any LLM/AI vendor, demand the no-training-on-data commitment, retention, and region; prompts/outputs containing PII are a processing and transfer event.

### Auditability, controls, and evidence (SOC 2 CC-series, PCI, HIPAA Security Rule)
- **Control catalog mapped to data** — the access, encryption, logging, and integrity controls protecting each sensitive data class, mapped to the relevant control framework (SOC 2 CC6/CC7, PCI requirements, HIPAA safeguards). A control set not mapped to data classes can't be audited for coverage.
- **Audit-log design and immutability** — what is logged for access to and changes of personal data, log retention, tamper-resistance/append-only, and that logs themselves don't over-collect PII. Auditors ask for access logs first; the design must produce them.
- **Access control and least privilege** — RBAC/ABAC model over personal data, separation of duties, and how privileged/admin access to raw data is restricted and logged. (Mechanism depth is a security-lens concern; here the demand is that access to *regulated data* is governed and evidenced — see also security mode.)
- **Access review / recertification cadence (SOC 2 CC6.x)** — periodic recertification of who has access to personal/sensitive data, the cadence (e.g., quarterly), the owner, and the evidence the review produces. Stale access is a top SOC 2 exception; demand the architecture can generate the entitlement report the review consumes.
- **HIPAA Security Rule technical safeguards** — where PHI is in scope, demand each required technical safeguard be evidenced as a named mechanism, not assumed under "we encrypt": access controls with unique user IDs and emergency access, audit controls (the hardware/software/procedural recording of ePHI access — distinct from app logs), integrity controls proving ePHI is not improperly altered or destroyed, and transmission security for ePHI in motion. These are explicit §164.312 requirements; an auditor checks them one by one, so a doc that only says "encrypted and logged" leaves integrity and audit-control gaps undemonstrated.
- **Encryption posture as evidence** — encryption at rest and in transit per regulated store, key management/rotation, and who holds keys (relevant to crypto-shred deletion and to transfer safeguards). State it as auditable fact, not aspiration. Boundary with the security lens: the security lens owns key-management *design depth* (KMS/HSM choice, rotation cadence, custody/separation, envelope encryption). Here the demand is narrower and must not be dropped on the assumption security covers it — name who holds the keys and confirm crypto-shred is a real deletion path and that customer/regulator key-custody commitments (e.g., BYOK, EU-held keys for transfer safeguards) are met. If both lenses point at each other, key management falls through the crack — claim it explicitly here.
- **Change and config evidence** — how changes to data-handling code/config are reviewed, approved, and logged (CC8). Auditors sample change tickets against deploys.
- **Evidence producibility** — for each obligation above, name the artifact the system can emit on demand (RoPA export, access report, consent ledger, deletion certificate, transfer inventory). If an obligation has no producible evidence, it is not auditable and is a gap.
- **Data integrity / accuracy (Art. 5(1)(d))** — how data is kept accurate and how inaccuracies are corrected and propagated. Inaccurate data driving automated or significant decisions is both an accuracy violation and the basis for a rectification claim or a discrimination challenge; a doc with no accuracy mechanism can't answer either.

### Breach detection and notification
- **Detection and declaration path** — how a suspected breach is detected, who has authority to declare a reportable breach, and the internal escalation. Ambiguous ownership burns the regulatory clock.
- **Regulatory clocks** — the applicable notification deadlines (GDPR 72h to supervisory authority, HIPAA 60 days, US state laws, PCI card-brand timelines) and which the system is bound by. The doc must state the clocks it is racing.
- **Affected-record enumeration within the window** — the architectural ability to determine, within the notification window, which data subjects and which data classes were affected. This is the single hardest breach requirement; if the data-flow inventory and logging can't answer "who was in this store and what did they have," the clock can't be met. Demand the mechanism.
- **Breach scoping by data class** — ability to distinguish a breach of special-category/PHI/cardholder data (stricter, often individual notification) from low-risk data. Drives whether and whom to notify.
- **Notification content readiness** — the data needed for a notice (categories of data, number of subjects, likely consequences, mitigations) is producible from the system, not reconstructed manually.

### Automated decisions, profiling, and AI transparency (GDPR Art. 22, EU AI Act)
- **Automated-decision inventory** — every place a decision that produces legal or similarly significant effects on a person is made by automated processing (credit/eligibility, pricing, fraud blocking, content/account actions, ranking that gates access). Art. 22 restricts solely-automated significant decisions.
- **Human-in-the-loop / review and appeal** — for in-scope decisions, a meaningful human review and an appeal/contest path; demand the architecture supports surfacing the decision, its basis, and an override. "Solely automated" with significant effect and no opt-out is unlawful.
- **Profiling disclosure** — what profiling occurs, the logic involved (meaningful information, not source code), and how it is disclosed to subjects.
- **EU AI Act classification** — where the system is or embeds an AI system, its risk tier (prohibited / high-risk / limited / minimal) and the resulting obligations (risk management, logging, human oversight, transparency). High-risk classification adds conformity and documentation duties; demand the tier be stated.
- **Training-data provenance and basis** — for any model trained on personal data, the lawful basis and purpose for that training (cross-reference Purpose limitation and Lawful basis); special-category training data and scraped data are high-risk.
- **Bias / fairness evidencing** — for significant automated decisions, whether the design can produce the evidence (inputs, outcomes by group) needed to answer a discrimination challenge. Increasingly demanded by regulators.

## Grill order
1. **Regulatory scope and roles** — pin down which regimes apply, to which components, and the system's role (controller/processor, etc.); force a no-PII claim through field-level proof before accepting it, set the PCI CDE boundary/SAQ route, and check the DPIA/PIA threshold. Everything downstream depends on this; an answer that's wrong here invalidates the rest.
2. **PII/sensitive-data inventory with lineage** — get the field-level inventory and every store/derived copy. Nothing else (minimization, deletion, breach scope, DSAR) is provable without it.
3. **Lawful basis + purpose per data class** — close the Art. 6 basis and Art. 5(1)(b) purpose gates as two separate checks; flag any secondary use (analytics/ML) lacking fresh basis.
4. **Minimization** — necessity test per field; drop or justify speculative collection.
5. **Retention, deletion, and legal hold** — period + mechanism per class, DSAR erasure across all copies, and hold-suspends-deletion.
6. **Data-subject rights and transparency** — access/portability/correction/objection mechanisms, identity verification, SLAs against regulatory clocks, and reconciliation of the external privacy notice (Art. 13/14) against the actual processing.
7. **Cross-border transfer and residency** — residency per store, mechanism per crossing, sub-processor locations, backup/DR regions.
8. **Sub-processors and DPAs/BAAs** — register complete (incl. AI/LLM vendors) with contract coverage.
9. **Breach-response architecture** — declaration authority, clocks, and affected-record enumeration within the window.
10. **Auditability and access recertification** — control-to-data mapping, immutable access logs, recertification cadence, HIPAA technical safeguards where PHI is in scope, key-management ownership at the security-lens boundary, and per-obligation evidence producibility.
11. **Automated decisions / AI transparency** — Art. 22 inventory, human review/appeal, profiling disclosure, AI Act tier, training-data basis.
12. **Polish** — accuracy/integrity duties, notification-content readiness, out-of-scope re-identification arguments, vendor-change notice windows.

## Deliverable
Leave these in the architecture doc:

- **Record of Processing (RoPA) table** — one row per data class. Columns: Data class | Example fields | Sensitivity (standard / special-category / PHI / cardholder / children) | System of record | All stores & derived copies (incl. caches, indexes, logs, backups, ML features) | Collection point | Lawful basis (Art. 6 / Art. 9 condition) | Purpose(s) | Necessity justification | Retention period & trigger | Deletion mechanism | Cross-border? (Y/N + mechanism).
- **Lawful-basis & consent register** — Data class | Basis | If consent: capture method, version, withdrawal propagation + SLA | If legitimate interest: LIA reference + opt-out | CCPA sale/share status + GPC handling.
- **Cross-border transfer map** — Store/flow | Source region | Destination region | Mechanism (adequacy / SCCs+TIA / BCR / derogation) | Sub-processor involved. Include backups and DR.
- **Sub-processor register** — Vendor | Data classes received | Purpose | Processing location(s) | DPA/BAA status | AI/LLM training-use commitment.
- **DSR fulfillment matrix** — Right (access / portability / correction / deletion / objection) | Stores touched | Mechanism | Identity-verification step | SLA vs regulatory clock | Exceptions.
- **Control-to-data & evidence matrix** — Control (mapped to SOC 2 CC / PCI req / HIPAA safeguard) | Data classes protected | Owner | Recertification cadence | Evidence artifact the system emits.
- **Breach-response register** — Trigger/detection | Declaration authority | Applicable clock(s) | Affected-record enumeration mechanism | Notification-content source.
- **Automated-decision register** — Decision | Effect on person | Solely automated? | Human review/appeal path | Profiling disclosure | AI Act risk tier | Training-data basis.
- **Transparency-notice reconciliation** — Disclosure item (data categories / purposes / bases / recipients / retention / transfers / rights) | Stated in external notice? | Matches RoPA & sub-processor & transfer artifacts? | Gap. Plus, where applicable: the DPIA/PIA reference (or the threshold determination that none is required), and for a no-PII claim, the field-level proof backing it.

See also: the security mode for key-management, encryption, and access-control design depth that this lens references but does not own.

Each table cell that reads "TBD" or "see policy" without a named mechanism or artifact is an open gap; the grill is not done until every regulated data class has a complete row across the RoPA, transfer, retention, and DSR artifacts and the external notice reconciles against them.
