# Cross-Framework Control Mapping — Verified Reference

> **Purpose**: This file contains verified control equivalences across major compliance frameworks. Agents MUST use this table when performing multi-framework assessments to identify shared controls and avoid redundant findings.

## Important Notes

- **N/A** means this framework does not have a specific, dedicated requirement in this control area (though the topic may be addressed indirectly elsewhere in the framework).
- **Mappings are approximate** — framework requirements vary in scope, depth, and specificity. A mapping indicates conceptual equivalence, not identical requirements.
- SOC 2 references use the 2017 Trust Services Criteria (TSC). CC = Common Criteria, A = Availability, P = Privacy.
- ISO 27001 references use the 2022 Annex A control numbering (ISO 27001:2022).
- NIST references use NIST SP 800-53 Rev. 5 control families.
- PCI-DSS references use v4.0 requirement numbering.
- HIPAA references use 45 CFR Part 164 (Security Rule and Privacy Rule).

---

## Control Equivalence Table

| Control Area | SOC 2 (TSC) | ISO 27001:2022 | NIST 800-53 Rev 5 | PCI-DSS v4.0 | HIPAA |
|---|---|---|---|---|---|
| **Access Control** | CC6.1 | A.5.15, A.8.3 | AC-2, AC-3 | 7.2, 7.3 | §164.312(a)(1) |
| **Authentication** | CC6.1, CC6.6 | A.8.5 | IA-2, IA-5 | 8.2, 8.3 | §164.312(d) |
| **Encryption at Rest** | CC6.1, CC6.7 | A.8.24 | SC-28 | 3.5 | §164.312(a)(2)(iv) |
| **Encryption in Transit** | CC6.1, CC6.7 | A.8.24 | SC-8 | 4.2 | §164.312(e)(1) |
| **Logging & Monitoring** | CC7.2, CC7.3 | A.8.15, A.8.16 | AU-2, AU-3, AU-6 | 10.2, 10.4 | §164.312(b) |
| **Incident Response** | CC7.4, CC7.5 | A.5.24, A.5.25, A.5.26, A.5.27, A.5.28 | IR-1, IR-2, IR-3, IR-4, IR-5, IR-6, IR-7, IR-8 | 12.10 | §164.308(a)(6) |
| **Change Management** | CC8.1 | A.8.32 | CM-3 | 6.5 | N/A |
| **Vulnerability Management** | CC7.1 | A.8.8 | RA-5, SI-2 | 6.3, 11.3 | §164.308(a)(1)(ii)(A) |
| **Backup & Recovery** | A1.2 | A.8.13, A.8.14 | CP-9, CP-10 | N/A | §164.308(a)(7) |
| **Physical Security** | CC6.4 | A.7.1, A.7.2, A.7.3, A.7.4, A.7.5, A.7.6, A.7.7, A.7.8, A.7.9, A.7.10, A.7.11, A.7.12, A.7.13, A.7.14 | PE-1, PE-2, PE-3, PE-4, PE-5, PE-6 | 9.1, 9.2, 9.3, 9.4 | §164.310(a)(1) |
| **Security Awareness Training** | CC1.4 | A.6.3 | AT-2, AT-3 | 12.6 | §164.308(a)(5) |
| **Risk Assessment** | CC3.2, CC3.4 | A.5.12 | RA-3 | 12.2 | §164.308(a)(1)(ii)(A) |
| **Data Classification** | CC6.1 | A.5.12, A.5.13 | RA-2 | 3.2 | N/A |
| **Network Security** | CC6.1, CC6.6 | A.8.20, A.8.21, A.8.22 | SC-7 | 1.2, 1.3 | §164.312(e)(1) |
| **Endpoint Protection** | CC6.8 | A.8.1, A.8.7 | SI-3 | 5.2, 5.3 | §164.308(a)(5)(ii)(B) |
| **Secure Development** | CC8.1 | A.8.25, A.8.26, A.8.27 | SA-11 | 6.2, 6.5 | N/A |
| **Third-Party Management** | CC9.2 | A.5.19, A.5.20, A.5.21, A.5.22 | SA-9, SR-1 | 12.8, 12.9 | §164.308(b)(1) |
| **Business Continuity** | A1.1, A1.2 | A.5.29, A.5.30 | CP-1, CP-2, CP-3, CP-4 | 12.10 | §164.308(a)(7) |
| **Privacy / Data Protection** | P1.1, P1.2 | A.5.34 | PM-25, PT-2 | 3.1, 3.2 | §164.530 |
| **Configuration Management** | CC6.1, CC8.1 | A.8.9 | CM-2, CM-6, CM-7 | 2.2 | N/A |
| **Key Management** | CC6.1 | A.8.24 | SC-12 | 3.6, 3.7 | N/A |
| **Monitoring & Alerting** | CC7.2 | A.8.16 | SI-4 | 10.7, 11.5 | §164.312(b) |
| **Asset Management** | CC6.1 | A.5.9, A.5.10 | CM-8 | 12.5 | §164.310(d)(1) |
| **Personnel Security** | CC1.4, CC1.5 | A.6.1, A.6.2, A.6.5, A.6.6 | PS-1, PS-2, PS-3, PS-4, PS-5, PS-6, PS-7, PS-8 | 12.7 | §164.308(a)(3) |
| **Data Disposal** | CC6.5 | A.8.10 | MP-6 | 3.1, 9.4 | §164.310(d)(2) |

---

## How to Use This Table

1. **Multi-framework assessments**: When a system must comply with multiple frameworks, use this table to identify controls that satisfy requirements across frameworks simultaneously. A single implementation (e.g., MFA) can produce evidence for Access Control + Authentication rows across all applicable frameworks.

2. **Gap identification**: If a control area shows N/A for one framework but has requirements in others, the assessed organization may still want to implement the control as a best practice even though the specific framework does not mandate it.

3. **Evidence reuse**: When collecting evidence for one framework, check this table to identify which other frameworks the same evidence applies to. This reduces assessment effort and ensures consistency.

4. **Scope differences**: Even when two frameworks address the same control area, the specific requirements may differ. For example:
   - PCI-DSS 8.3 requires MFA for all access into the cardholder data environment
   - HIPAA §164.312(d) requires person/entity authentication but does not mandate MFA specifically
   - NIST IA-2 provides multiple enhancement levels for authenticator management

   Always verify the specific requirement text in the individual framework reference files.

5. **Framework-specific references**: For detailed control descriptions and implementation specifications, consult:
   - `soc2-trust-services-criteria.md`
   - `iso27001-annex-a-controls.md`
   - `nist-800-53-controls.md`
   - `pci-dss-v4-requirements.md`
   - `hipaa-security-rule.md`
