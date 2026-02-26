# Data Classification Taxonomy — Verified Reference

This reference provides standardized data types and sensitivity levels for privacy assessments. Agents use this taxonomy to classify personal data during the data inventory phase. The sensitivity level determines required protection controls and influences risk severity scoring.

---

## Sensitivity Levels (4-Tier)

| Level | Name | Description | Required Controls |
|---|---|---|---|
| **PUBLIC** | Public | No privacy impact if disclosed. Non-personal, publicly available data. | Standard access controls |
| **INTERNAL** | Internal | Low privacy impact. Business data, internal communications, aggregated/anonymized data. | Access control, basic monitoring |
| **CONFIDENTIAL** | Confidential | Moderate privacy impact. PII, customer data, standard personal identifiers. | Encryption at rest and in transit, RBAC, monitoring, retention limits, DPA with processors |
| **RESTRICTED** | Restricted | High privacy impact. Special categories (GDPR Art. 9), financial data, health data, children's data, credentials. | End-to-end encryption, compartmentalized access, continuous monitoring, DLP, audit logging, MFA for access, enhanced safeguards per regulation |

---

## Personal Data Categories (with GDPR Art. 4 references)

GDPR Art. 4(1) defines personal data as "any information relating to an identified or identifiable natural person."

### Basic Identity (CONFIDENTIAL)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| Name | Full name, first/last name, maiden name, alias, nickname | Art. 4(1) — identified natural person |
| Photo | Profile photo, headshot, ID photo | Art. 4(1); Art. 4(14) if used for biometric identification |
| Online Identifiers | Username, user ID, account handle | Art. 4(1); Recital 30 — online identifiers |
| Date of Birth | Full DOB, birth year, age | Art. 4(1) |

### Contact Information (CONFIDENTIAL)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| Email | Personal email, work email | Art. 4(1) |
| Phone | Mobile, landline, fax | Art. 4(1) |
| Address | Home address, mailing address, postal code | Art. 4(1) |
| Social Media Handles | Twitter/X handle, LinkedIn profile, Instagram username | Art. 4(1); Recital 30 |

### Financial Data (RESTRICTED)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| Bank Accounts | Account number, routing number, IBAN, SWIFT | Art. 4(1); also PCI-DSS, GLBA |
| Credit/Debit Cards | Card number, CVV, expiration date | PCI-DSS; CCPA §1798.121 (sensitive PI) |
| Income | Salary, wages, bonuses, tax returns | Art. 4(1) |
| Credit History | Credit score, credit report, debt records | Art. 4(1); FCRA |
| Tax Records | Tax ID, tax filings, W-2/1099 forms | Art. 4(1) |

### Employment Data (CONFIDENTIAL)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| Employer | Company name, department, division | Art. 4(1) |
| Job Title | Title, role, seniority level | Art. 4(1) |
| Salary | Compensation, benefits, stock options | Art. 4(1) |
| Performance | Reviews, ratings, disciplinary records | Art. 4(1) |
| Work History | Previous employers, dates of employment, references | Art. 4(1) |

### Online Activity (CONFIDENTIAL)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| IP Address | IPv4, IPv6 address | Art. 4(1); Recital 30 — online identifier |
| Cookies | Session cookies, tracking cookies, advertising IDs | Recital 30; ePrivacy Directive Art. 5(3) |
| Browsing History | URLs visited, pages viewed, referrer data | Art. 4(1) when linked to individual; CCPA §1798.140 |
| Search History | Search queries, search terms | Art. 4(1) when linked to individual |
| Device IDs | IMEI, MAC address, advertising ID, browser fingerprint | Recital 30 — online identifiers |

### Location Data (CONFIDENTIAL to RESTRICTED)

| Data Element | Examples | Default Level | Notes |
|---|---|---|---|
| GPS Data | Precise coordinates, real-time location | RESTRICTED | CCPA §1798.121 (sensitive PI) |
| Travel Patterns | Route history, frequent locations | RESTRICTED | Behavioral profiling risk |
| Home/Work Addresses | Residential address, office address | CONFIDENTIAL | Art. 4(1) |
| Check-ins | Social media check-ins, venue visits | CONFIDENTIAL | Escalates to RESTRICTED with frequency data |

### Communication Data (CONFIDENTIAL to RESTRICTED)

| Data Element | Examples | Default Level | Notes |
|---|---|---|---|
| Email Content | Email body, subject lines | RESTRICTED | ePrivacy Directive; ECPA (18 U.S.C. §2510) |
| Messages | Chat messages, DMs, SMS content | RESTRICTED | Content of communications |
| Call Records | Call logs, duration, participants | CONFIDENTIAL | Metadata vs content distinction |
| Metadata | Timestamps, sender/recipient, frequency | CONFIDENTIAL | Can reveal patterns even without content |

### Government IDs (RESTRICTED)

| Data Element | Examples | GDPR Reference |
|---|---|---|
| SSN / National ID | Social Security Number, national identification number | Most regulations treat as high sensitivity |
| Passport | Passport number, issuing country | Art. 4(1); high sensitivity |
| Driver's License | License number, state/country of issue | Art. 4(1); high sensitivity |
| Tax ID | TIN, EIN, ITIN | Art. 4(1); high sensitivity |

---

## Special Categories (GDPR Art. 9) — RESTRICTED

Processing of these categories is **prohibited** under GDPR Art. 9(1) unless an Art. 9(2) exception applies.

| Category | Description | GDPR Reference |
|---|---|---|
| Racial or Ethnic Origin | Race, ethnicity, national origin, tribal affiliation | Art. 9(1) |
| Political Opinions | Political party affiliation, political views, voting history | Art. 9(1) |
| Religious or Philosophical Beliefs | Religious affiliation, philosophical beliefs, spiritual practices | Art. 9(1) |
| Trade Union Membership | Union membership, union activities, collective bargaining | Art. 9(1) |
| Genetic Data | DNA sequences, genetic test results, family genetic history | Art. 4(13): "personal data relating to the inherited or acquired genetic characteristics of a natural person which give unique information about the physiology or the health of that natural person and which result, in particular, from an analysis of a biological sample from the natural person in question" |
| Biometric Data (for identification) | Fingerprint, facial geometry, voice print, iris scan, gait analysis | Art. 4(14): "personal data resulting from specific technical processing relating to the physical, physiological or behavioural characteristics of a natural person, which allow or confirm the unique identification of that natural person, such as facial images or dactyloscopic data" |
| Health Data | Diagnosis, prescriptions, treatment records, mental health records, disability | Art. 4(15): "personal data related to the physical or mental health of a natural person, including the provision of health care services, which reveal information about his or her health status" |
| Sex Life or Sexual Orientation | Sexual orientation, sex life, gender identity | Art. 9(1) |

---

## Criminal Data (GDPR Art. 10) — RESTRICTED

| Category | Description | GDPR Reference |
|---|---|---|
| Criminal Convictions and Offenses | Criminal records, court proceedings, arrest records, sentencing, pending charges | Art. 10: processing only under control of official authority or when authorized by Union or Member State law providing appropriate safeguards |

> **Note:** Criminal data is governed separately from Art. 9 special categories. Art. 10 requires official authority or specific legal authorization, distinct from the Art. 9(2) exceptions.

---

## Children's Data — RESTRICTED

| Regulation | Age Threshold | Consent Requirement |
|---|---|---|
| GDPR Art. 8 | Under **16** (member states may lower to **13**) | Consent of holder of parental responsibility; verification required |
| COPPA (US) | Under **13** | Verifiable parental consent before collection |
| CCPA/CPRA | Under **16** for opt-in to sale/sharing; parent consent under **13** | Affirmative authorization (opt-in) for sale or sharing of minors' PI |
| PIPL (China) | Under **14** | Parent or guardian consent required |
| LGPD (Brazil) | Children and adolescents (Art. 14) | Specific and prominent consent from at least one parent/legal guardian; in the child's best interest |
| PDPA (Singapore) | No specific age threshold | Consent from parent/guardian for minors; general consent obligation applies |
| UK GDPR / DPA 2018 | Under **13** (DPA 2018 §9) | Consent of holder of parental responsibility |

---

## High-Risk Combinations

When multiple data elements are combined, the composite sensitivity may exceed the individual elements. Flag these combinations:

| Combination | Individual Levels | Combined Level | Risk Rationale |
|---|---|---|---|
| Name + Health Condition | CONFIDENTIAL + RESTRICTED | **RESTRICTED** | Direct identification of health status; GDPR Art. 9 |
| Name + Location Over Time | CONFIDENTIAL + CONFIDENTIAL | **RESTRICTED** | Behavioral profiling; movement pattern inference |
| Email + Browsing History | CONFIDENTIAL + CONFIDENTIAL | **CONFIDENTIAL** (elevated) | Cross-site tracking; behavioral profiling |
| Device ID + App Usage | CONFIDENTIAL + CONFIDENTIAL | **CONFIDENTIAL** (elevated) | Device fingerprinting; behavioral profiling |
| Name + Financial Records | CONFIDENTIAL + RESTRICTED | **RESTRICTED** | Wealth profiling; identity theft risk |
| Name + Political Opinions | CONFIDENTIAL + RESTRICTED | **RESTRICTED** | Political profiling; Art. 9 special category |
| IP Address + Browsing + Location | CONFIDENTIAL + CONFIDENTIAL + CONFIDENTIAL | **RESTRICTED** | De-anonymization risk; comprehensive tracking |
| Employee ID + Performance + Health | CONFIDENTIAL + CONFIDENTIAL + RESTRICTED | **RESTRICTED** | Employment discrimination risk |

> **Principle:** When in doubt about combination risk, classify at the higher sensitivity level. A conservative classification protects against underestimating privacy impact.
