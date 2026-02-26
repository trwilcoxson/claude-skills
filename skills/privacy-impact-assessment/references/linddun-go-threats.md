# LINDDUN GO Privacy Threat Catalog

## How to Use This Reference

When citing LINDDUN threats, use the category letter (L/I/N/D/D/U/N) and threat type name exactly as listed below. Verify both the category and threat type exist in this reference before including them in the assessment.

LINDDUN GO is a lightweight, systematic privacy threat modeling methodology. Each category represents a distinct privacy concern. Assess all 7 categories against every data flow and data store identified during the data inventory and data flow analysis phases.

---

## L — Linkability

The ability to link two or more data items, actions, or identities belonging to the same individual or group.

| Threat Type | Description | Example |
|---|---|---|
| L1: Linkability of data items | Multiple data records can be linked to the same individual | Linking browsing history with purchase records via common user ID |
| L2: Linkability of actions | Actions across sessions or contexts can be linked to the same individual | Correlating login times with activity patterns across services |
| L3: Linkability of identities | Identities across different systems can be linked | Same email used across services enables cross-platform profiling |

### Common Indicators
- Persistent identifiers across contexts (user IDs, cookies, device fingerprints)
- Shared databases without access segregation
- Analytics systems combining data from multiple sources
- Cross-service authentication without pseudonymization
- Common join keys across datasets (email, phone, account ID)

---

## I — Identifiability

The ability to identify a data subject from available data, whether directly or through combination.

| Threat Type | Description | Example |
|---|---|---|
| I1: Identifying through identifiers | Direct identification via personally identifiable information | Name, email address, SSN, phone number in data stores |
| I2: Identifying through quasi-identifiers | Indirect identification via combination of attributes | ZIP code + date of birth + gender uniquely identifies an individual |
| I3: Identifying through context | Identification from behavioral or contextual data patterns | Unique browsing pattern or writing style identifies a user |

### Common Indicators
- Storing direct identifiers when pseudonyms would suffice
- Insufficient anonymization (quasi-identifiers remain)
- Behavioral data that creates unique fingerprints
- Metadata exposure in APIs or logs
- Small populations where aggregate data identifies individuals

---

## N — Non-repudiation (unwanted)

The inability of a data subject to deny having performed an action, where such proof is undesirable from the individual's privacy perspective.

| Threat Type | Description | Example |
|---|---|---|
| N1: Non-repudiation of sending | Irrefutable proof that the subject sent a message or data | Email read receipts, cryptographically signed messages |
| N2: Non-repudiation of receiving | Irrefutable proof that the subject received information | Delivery confirmations, acknowledgment receipts |
| N3: Non-repudiation of action | Irrefutable proof that the subject performed an action | Detailed audit logs of user actions exposed to non-security staff |

### Common Indicators
- Detailed audit trails accessible beyond security/compliance teams
- Digital signatures on user actions beyond what is necessary
- Transaction receipts with excessive detail shared broadly
- Immutable logs of sensitive actions without access controls
- Read receipts or tracking pixels in communications

---

## D — Detectability

The ability to determine whether an item of interest (data, action, identity) exists, without necessarily learning its content.

| Threat Type | Description | Example |
|---|---|---|
| D1: Detectability of data | Existence of specific data can be determined | Timing attacks reveal whether a record exists in the database |
| D2: Detectability of actions | Existence of an action or processing can be determined | Observable metadata reveals that processing occurred on certain data |
| D3: Detectability of identities | Existence of an identity or account can be determined | User enumeration via different login error messages |

### Common Indicators
- Different error messages for existing vs non-existing users
- Observable database query timing differences
- Metadata in API responses revealing data existence
- Cache behavior differences based on data presence
- HTTP status codes that distinguish between "not found" and "forbidden"

---

## D — Disclosure of Information

Unauthorized or excessive exposure of personal data content to parties who should not have access.

| Threat Type | Description | Example |
|---|---|---|
| D1: Information disclosure via access control failure | Unauthorized access to personal data | Broken access control exposing other users' records |
| D2: Information disclosure via data breach | Mass exposure of personal data | Database compromise exposing PII at scale |
| D3: Information disclosure via inference | Deriving sensitive information from non-sensitive data | Inferring health conditions from purchase patterns |
| D4: Information disclosure via surplus data | Excessive data exposed in responses or interfaces | API returning full user profile when only name is needed |

### Common Indicators
- Overly broad API responses returning unnecessary fields
- PII in application logs, error messages, or debug output
- Insufficient access controls on data stores
- Shared credentials or service accounts with broad access
- Verbose error messages containing personal data

---

## U — Unawareness

The data subject's lack of awareness about or inability to control the processing of their personal data.

| Threat Type | Description | Example |
|---|---|---|
| U1: Lack of transparency | Data processing not adequately communicated to subjects | No privacy notice, or notice buried deep in terms of service |
| U2: Lack of intervenability | Data subject cannot intervene in or control processing | No mechanism to withdraw consent or restrict processing |
| U3: Lack of user control | Data subject cannot exercise their data protection rights | DSAR process nonexistent or extremely difficult to use |

### Common Indicators
- Missing or inadequate privacy notices
- No consent management mechanism
- No data subject access request (DSAR) fulfillment process
- Automated decisions with no human review option
- No opt-out mechanism for non-essential processing
- Privacy settings hidden or difficult to find
- No notification of changes to processing activities

---

## N — Non-compliance

Failure to comply with applicable privacy laws, regulations, or organizational policies regarding personal data processing.

| Threat Type | Description | Example |
|---|---|---|
| N1: Non-compliance with consent requirements | Invalid or missing consent for processing | Processing without legal basis, pre-checked consent boxes |
| N2: Non-compliance with data subject rights | Required rights not supported or implemented | No deletion mechanism, no data portability, no access process |
| N3: Non-compliance with data protection principles | Core privacy principles violated | Purpose limitation, data minimization, or storage limitation breached |
| N4: Non-compliance with accountability | Required documentation or governance missing | No ROPA, no DPIA where required, no DPO designated when mandatory |
| N5: Non-compliance with international transfer rules | Unlawful cross-border data transfers | No SCCs, no adequacy decision, no BCRs for international transfers |

### Common Indicators
- No documented legal basis for each processing activity
- Data collected or used beyond the stated purpose
- No retention schedule or deletion mechanism
- Missing Record of Processing Activities (ROPA)
- Cross-border transfers without appropriate safeguards
- No data processing agreements with processors
- Consent mechanisms that do not meet regulatory standards (not freely given, not specific, not informed)
