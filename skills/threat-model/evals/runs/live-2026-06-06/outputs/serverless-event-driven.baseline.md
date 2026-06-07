# Threat Model: Serverless Event-Driven Document Processing Pipeline (AWS, us-east-1)

## Scope and Data Sensitivity

This pipeline ingests and processes customer PII: full names, email addresses, document text, and uploaded ID documents. ID documents are among the highest-sensitivity data classes — exposure enables identity theft and likely triggers breach-notification obligations (state laws, GDPR if EU subjects, plus standards like SOC 2 / PCI-adjacent expectations). The PII classification raises the impact ceiling on nearly every finding below from "incident" to "reportable breach."

I'll use a STRIDE-organized walkthrough across the trust boundaries, then summarize prioritized risks and remediations.

---

## Data Flow and Trust Boundaries

```
[Untrusted Internet]
   |  (1) POST /upload  -- API key only, no WAF, no JWT/Cognito
   v
[API Gateway] --> [Ingest Lambda] -- returns presigned PUT URL (15 min, no conditions)
   |  (2) direct PUT to S3 (client-controlled)
   v
[S3 customer-uploads bucket] -- BPA OFF, GetObject to Principal:*, no default SSE
   |  (3) ObjectCreated event
   v
[EventBridge] -- rule matches client-supplied `source` field
   |  (4) fan-out
   v
[SQS queue] -- no DLQ, no SSE
   |  (5) poll
   v
[Worker Lambda(s)] -- shared IAM role: s3:* dynamodb:* sqs:* on Resource:*
   |             -- plaintext env vars: 3rd-party tokens + DB passphrase
   v
[DynamoDB Documents] -- name, email, document text
```

Trust boundaries: Internet → API Gateway (1); client → S3 (2, the presigned URL hands a browser-side actor direct write access); S3 → event pipeline (3); event pipeline → compute (4,5); compute → data stores. The most dangerous property of this design is that boundary (2) lets an untrusted client write directly to your storage, and boundary (1) is guarded only by a shared secret.

---

## Findings by STRIDE

### Spoofing / Authentication

**S1 — API key is not authentication (Critical).** API Gateway API keys are intended for usage-plan throttling and identification, not authN/authZ. They are commonly embedded in client apps, leak in logs/repos/browser traffic, and do not identify a user. With no Cognito/JWT authorizer on the upload routes, anyone holding (or guessing the distribution path of) the key can request presigned URLs and inject documents. There is no per-user identity, so you cannot attribute uploads, scope them, or revoke a single bad actor.

**S2 — No user binding on presigned URLs.** Because the requester is not authenticated to a principal, the presigned URL the ingest Lambda mints is not tied to any tenant/user. Any caller can obtain a write capability into the shared `customer-uploads` bucket.

**S3 — Spoofable EventBridge routing on `source` (High).** The EventBridge rule matches a *client-supplied* `source` field in the event detail. If any path lets a client influence that field (e.g., object metadata propagated into the event, or a custom PutEvents path), an attacker can forge or misroute events — suppressing processing, triggering unintended rules, or replaying/injecting events into the wrong flow. EventBridge `source`/`detail-type` should be set by trusted producers only; never branch security-relevant routing on attacker-controlled content.

### Tampering

**T1 — Unrestricted presigned PUT (High).** The presigned URL has no `content-length-range` and no `content-type` condition. A client can upload arbitrarily large files (cost/DoS, see D-section), wrong/malicious file types, or polyglot files designed to exploit the parser. The 15-minute expiry is reasonable, but with no size/type constraints the capability is far broader than intended.

**T2 — Malicious document content → parser exploitation.** Worker Lambdas "parse" attacker-supplied files. Document parsers (PDF, Office, image/OCR, XML) are a classic exploitation surface: XXE, zip-bombs, decompression bombs, formula/macro injection, malformed-structure RCE in native libraries. Combined with the over-broad IAM role (below), parser compromise becomes account-level compromise.

**T3 — Data integrity in transit/at rest.** No default SSE on S3 and no SSE on SQS means message bodies and objects sit unencrypted at rest. There's no integrity control (e.g., object-lock, versioning) mentioned, so objects can be overwritten and there's no tamper-evident trail.

### Repudiation

**R1 — Weak attribution.** No per-request identity (S1) means uploads cannot be reliably attributed. No DLQ means failed/poisoned messages vanish rather than being captured for forensics. The model doesn't mention CloudTrail data events on the bucket, S3 access logging, or API Gateway access logs — without these, an intrusion is hard to reconstruct. Treat absence of audit logging as a gap to confirm and close.

### Information Disclosure (the most severe cluster here)

**I1 — Public-readable PII bucket (Critical).** Block Public Access is OFF and the bucket policy grants `s3:GetObject` to `Principal: "*"`. This means uploaded ID documents and any objects are world-readable to anyone who can enumerate or guess object keys. This is a direct, internet-facing PII exposure — effectively a standing data breach. This is the single highest-priority item.

**I2 — No encryption at rest across the pipeline (High).** No default SSE on S3, no SSE on SQS, and a "DynamoDB-encryption passphrase" implies app-managed crypto rather than KMS-backed SSE. Unencrypted PII at rest fails common compliance baselines and widens blast radius if any store is exposed.

**I3 — Secrets in plaintext Lambda env vars (Critical).** Third-party API tokens and the DynamoDB passphrase are stored as plaintext environment variables. Env vars are readable by anyone with `lambda:GetFunctionConfiguration`, appear in the console, can leak into logs/exceptions/tracing, and are exposed to any code running in the function (including a compromised dependency or a parser exploit, T2). The "encryption passphrase" living next to the data it protects defeats the purpose of the encryption. These belong in Secrets Manager or SSM Parameter Store (SecureString), fetched at runtime, with KMS encryption and rotation.

**I4 — Object-key enumeration.** Even without the world-readable policy, predictable key naming plus a leaked API key would allow enumeration. With I1 active, enumeration is trivial.

### Denial of Service

**D1 — No WAF, no real authn, no DoS controls (High).** The public endpoint has no WAF and only an API key. There's no described rate limiting beyond a possible usage plan. Attackers can flood the ingest endpoint, mint many presigned URLs, and push large/many objects.

**D2 — Cost-amplification / financial DoS.** Unbounded upload size (T1) + Lambda-per-message processing + DynamoDB writes + no backpressure means an attacker can drive S3 storage, Lambda invocation, and DynamoDB cost arbitrarily high. This is a denial-of-wallet attack.

**D3 — No DLQ → poison-message loops (High).** With no SQS dead-letter queue, a message the worker can't process (malformed file, parser crash) is retried until it expires, repeatedly invoking the worker, blocking throughput, and silently dropping data with no capture point. A single crafted file can stall or degrade the pipeline. Add a DLQ plus a redrive policy and a `maxReceiveCount`.

**D4 — No source-event validation → event flooding.** Spoofable routing (S3) plus public write (I1/S1) lets an attacker generate event storms.

### Elevation of Privilege

**E1 — One over-privileged shared IAM role (Critical).** All Lambdas share a single execution role granting `s3:*`, `dynamodb:*`, and `sqs:*` on `Resource: "*"`. Consequences:
- **Blast radius:** Any single function compromise (most likely via parser exploit T2 or a poisoned dependency) yields full read/write/delete over *all* S3 buckets, *all* DynamoDB tables, and *all* SQS queues in the account — not just this pipeline's resources. `s3:*` includes `DeleteObject`, `PutBucketPolicy`, etc.; `dynamodb:*` includes `DeleteTable` and full scans of every table.
- **No least privilege / no separation of duties:** the ingest function (which only needs to mint a presigned PUT for one bucket prefix) has the same power as the worker.
- **Lateral movement & exfiltration:** a compromised worker can read every object in every bucket and exfiltrate the whole account's data, then cover tracks.

This finding multiplies the severity of every other finding: it converts a single parser bug or leaked secret into account-wide compromise.

---

## Compliance / Privacy Overlay

Because the data is PII including ID documents: I1 (public bucket) is almost certainly a reportable breach condition as-is. I2/I3 (no encryption at rest, secrets in plaintext) and R1 (no audit trail) will fail GDPR Art. 32, most state breach statutes, and SOC 2 / ISO 27001 controls. Data-residency is single-region us-east-1, single account — note there is no environment isolation (dev/prod), which compounds blast radius.

---

## Prioritized Risk Register

| ID | Risk | STRIDE | Likelihood | Impact | Priority |
|----|------|--------|------------|--------|----------|
| I1 | World-readable PII bucket (`GetObject` to `*`, BPA off) | Info Disc | High | Critical | **P0 — fix now** |
| E1 | Single shared role with `*:*` on `Resource:*` | EoP | Med | Critical | **P0** |
| I3 | Secrets + DB passphrase in plaintext env vars | Info Disc | Med | Critical | **P0** |
| S1 | API key used as authentication; no JWT/Cognito | Spoofing | High | High | **P0** |
| T1/T2 | Unconstrained presigned PUT → malicious file → parser exploit | Tampering | Med | High | **P1** |
| I2 | No encryption at rest (S3/SQS), app-managed DB crypto | Info Disc | High | High | **P1** |
| D3 | No DLQ → poison-message loops, silent data loss | DoS | High | Med | **P1** |
| S3 | EventBridge routing on client-supplied `source` | Spoofing | Med | Med-High | **P1** |
| D1/D2 | No WAF, no rate limit → flood + denial-of-wallet | DoS | High | Med | **P1** |
| R1 | Missing audit logging (CloudTrail data events, access logs) | Repudiation | High | Med | **P2** |

---

## Remediation Roadmap

**P0 — Stop the active exposure**
1. **Turn Block Public Access ON** at account + bucket level; remove the `Principal:"*"` `GetObject` statement. Serve objects via presigned GET or CloudFront+OAC only. Audit existing objects — assume they were exposed and follow breach-response.
2. **Split the IAM role** into per-function least-privilege roles. Ingest role: `s3:PutObject` (or only presign capability) scoped to one bucket/prefix. Worker role: `s3:GetObject` on that prefix, `dynamodb:PutItem`/`BatchWriteItem` on the `Documents` table ARN, `sqs:ReceiveMessage`/`DeleteMessage` on the specific queue ARN. Eliminate all `*` actions and `Resource:"*"`.
3. **Move secrets to Secrets Manager / SSM SecureString**, KMS-encrypted, fetched at runtime, with rotation. Remove plaintext env vars. Reconsider the app-managed "DB passphrase" — prefer DynamoDB encryption at rest with a customer-managed KMS key instead of a self-rolled passphrase.
4. **Add a real authorizer** (Cognito user pools or a JWT/Lambda authorizer) on the upload routes; demote the API key to throttling/identification only. Bind presigned URLs to the authenticated principal/tenant prefix.

**P1 — Harden the pipeline**
5. **Constrain presigned URLs:** add `content-length-range` and `content-type` conditions; keep the 15-min expiry; consider per-tenant key prefixes.
6. **Sandbox/validate parsing:** verify file type by magic bytes, enforce size limits, disable XXE/external entity resolution, guard against decompression bombs, run AV/malware scanning (e.g., GuardDuty Malware Protection for S3) before processing.
7. **Enable encryption everywhere:** S3 default SSE-KMS, SQS SSE-KMS, DynamoDB SSE with CMK. Enforce TLS-only access via bucket/queue policies (`aws:SecureTransport`).
8. **Add an SQS DLQ** with a redrive policy and `maxReceiveCount`; alarm on DLQ depth. Make `source`/routing fields trusted-producer-set only; never branch routing logic on client-controlled content — validate/allow-list it.
9. **Add WAF** (rate-based rules, common rule sets, size constraints) in front of API Gateway; set usage-plan throttles and per-function reserved concurrency to cap denial-of-wallet.

**P2 — Detect and prove**
10. Enable CloudTrail (incl. S3 data events), S3 server access logging, API Gateway access logs, and Lambda/structured app logs. Add GuardDuty, AWS Config rules (BPA, public bucket, unencrypted resources, wildcard IAM), and Security Hub. Set up budget/anomaly alarms.
11. Consider account/environment isolation (separate prod account, separate per-stage roles) to bound blast radius.

---

## Key Assumptions / Things to Confirm
- I assumed no CloudTrail data events, S3 access logging, or API GW access logs are configured (not stated). Confirm — if present, R1 downgrades.
- I assumed the "DynamoDB-encryption passphrase" indicates application-layer crypto rather than KMS SSE. Confirm the actual scheme.
- I assumed the `source` field can in some path be influenced by clients; verify whether any client-reachable producer sets event detail used in routing.
- Whether a usage plan with throttling exists on the API key is unstated; I assumed minimal/none for D1.

**Bottom line:** the combination of a world-readable PII bucket (I1), a single account-wide `*:*` role (E1), and plaintext secrets (I3) means this system should be treated as already breached for ID-document data. Address those three plus real authentication (S1) before anything else; they convert ordinary bugs into catastrophic, account-wide PII loss.