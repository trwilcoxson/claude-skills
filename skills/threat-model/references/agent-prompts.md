# Agent Spawn Prompt Templates

All prompt templates for agents spawned during threat model assessments. Substitute `{output_dir}`, `{project_root}`, and `{refs_dir}` with actual paths before use.

## Contents
- [Solo — security-architect Phase 1 prompt](#solo--security-architect-phase-1-prompt)
- [Solo — security-architect Phases 3-6,8 prompt](#solo--security-architect-phases-3-68-prompt)
- [Diagram-specialist Phase 2 prompt](#diagram-specialist-phase-2-prompt)
- [Diagram-specialist Phase 7 prompt](#diagram-specialist-phase-7-prompt)
- [Solo — report-analyst prompt](#solo--report-analyst-prompt)
- [Team — security-architect Phase 1 prompt](#team--security-architect-phase-1-prompt)
- [Team — security-architect Phases 3-6,8 prompt](#team--security-architect-phases-3-68-prompt)
- [Team — privacy-agent prompt](#team--privacy-agent-prompt)
- [Team — grc-agent prompt](#team--grc-agent-prompt)
- [Team — code-review-agent prompt](#team--code-review-agent-prompt)
- [Team — validation-specialist prompt](#team--validation-specialist-prompt)
- [Team — report-analyst prompt](#team--report-analyst-prompt)

---

## Solo — security-architect Phase 1 prompt

> You are performing Phase 1 (Reconnaissance) of a solo threat model assessment against the project at {project_root}. Write output to {output_dir}/. Create the output directory if it does not exist. You have the threat-model skill loaded — execute ONLY Phase 1. Write 01-reconnaissance.md and visual-completeness-checklist.md. Be thorough — this reconnaissance is the foundation for all subsequent phases. Do NOT proceed to Phase 2 or any other phase. EXECUTION LOG: At the end of 01-reconnaissance.md, include an ## Execution Log section per the agent output protocol at {refs_dir}/agent-output-protocol.md — document process health, what went well, issues encountered, what was skipped, and assumptions made during this phase.

---

## Solo — security-architect Phases 3-6,8 prompt

> You are performing Phases 3-6 and 8 of a solo threat model assessment against the project at {project_root}. Output directory: {output_dir}/. FIRST: Read back 01-reconnaissance.md and 02-structural-diagram.md from {output_dir}/ to re-establish context — these were produced by prior agents in this pipeline. You have the threat-model skill loaded — execute Phases 3, 4, 5, 6, and 8 (summary only). Write 03-threat-identification.md, 04-risk-quantification.md, 05-false-negative-hunting.md, 06-validated-findings.md, and 08-threat-model-report.md. Phase 8 is a SUMMARY ONLY — see the Phase 8 section in the skill for the reduced format. Do NOT produce Phase 2 or Phase 7 diagrams — those are handled by the diagram-specialist. Reference component names from 02-structural-diagram.md to ensure consistency with the diagrams. EXECUTION LOG: At the end of 08-threat-model-report.md, include an ## Execution Log section per the agent output protocol — document process health, what went well, issues encountered, what was skipped, and assumptions made across all phases you executed.

---

## Diagram-specialist Phase 2 prompt

> You are producing Phase 2 (Structural Diagram) of the threat model. Read your full instructions from {refs_dir}/diagram-specialist-agent.md. Output directory: {output_dir}/. Read 01-reconnaissance.md and visual-completeness-checklist.md from {output_dir}/ to understand the system. Read ALL Mermaid reference files from {refs_dir}/: mermaid-spec.md, mermaid-layers.md, mermaid-diagrams.md, mermaid-templates.md, mermaid-review-checklist.md, and mermaid-config.json. Follow the Phase 2 instructions in your agent definition. Write 02-structural-diagram.md to {output_dir}/. The project root is {project_root}. EXECUTION LOG: At the end of 02-structural-diagram.md, include an ## Execution Log section — document process health, diagram complexity (node count, edge count, subgraph count), any Mermaid syntax issues encountered, visual completeness categories covered vs skipped, and self-assessed diagram quality.

---

## Diagram-specialist Phase 7 prompt

> You are producing Phase 7 (Visual Validation / Risk Overlay) of the threat model. Read your full instructions from {refs_dir}/diagram-specialist-agent.md. Output directory: {output_dir}/. Read these files from {output_dir}/: 02-structural-diagram.md, 04-risk-quantification.md, 05-false-negative-hunting.md, 06-validated-findings.md, and visual-completeness-checklist.md. Read ALL Mermaid reference files from {refs_dir}/: mermaid-spec.md, mermaid-layers.md, mermaid-diagrams.md, mermaid-templates.md, mermaid-review-checklist.md, mermaid-config.json, and frameworks.md (for CWE ID verification in annotations). Follow the Phase 7 instructions in your agent definition. Write 07-final-diagram.md to {output_dir}/. Update visual-completeness-checklist.md with risk overlay completion status. The project root is {project_root}. EXECUTION LOG: At the end of 07-final-diagram.md, include an ## Execution Log section — document process health, risk annotations applied (count by severity), attack paths overlaid, any findings that could not be mapped to diagram components, and self-assessed overlay quality.

---

## Solo — report-analyst prompt

> Generate the consolidated security assessment report from the threat model outputs. OUTPUT DIRECTORY: {output_dir}/. AVAILABLE INPUTS: 01-reconnaissance.md through 08-threat-model-report.md (note: 08 is a summary — the full report structure comes from the template). No team agents ran — this was a solo assessment. Skip Sections X and XI in the report structure and note in Assumptions that privacy and compliance assessments were not performed. FIRST: Read the report template at {refs_dir}/report-template.md. Follow the template EXACTLY. You have Bash access. GENERATE ALL FOUR FORMATS using your docx, pdf, pptx, and frontend-design skills: 1. report.html 2. report.docx 3. report.pdf 4. executive-summary.pptx. CRITICAL: You MUST generate all four files yourself. When installing Python packages, ALWAYS use a venv: python3 -m venv /tmp/report-venv && source /tmp/report-venv/bin/activate && pip install python-docx python-pptx reportlab Pillow. Render Mermaid diagrams to PNG: npx -y @mermaid-js/mermaid-cli -i file.mmd -o file.png -c {refs_dir}/mermaid-config.json -w 3000 --scale 2 -b white. The project root is {project_root}. HTML GENERATION RULES (MANDATORY): (1) Embed diagrams as pre-rendered PNG images using <img src="structural-diagram.png"> and <img src="risk-overlay-diagram.png"> — NEVER use Mermaid CDN (mermaid.js) for client-side rendering. (2) NEVER write <\/script> in HTML output — this JS-only escape breaks the HTML parser. Always write </script> literally. (3) Do not use defer/async on script tags that inline JS depends on. (4) All CSS and JS must be inline in the single HTML file (no external dependencies except the PNG images). BEFORE DECLARING DONE: Verify all files exist and are non-empty. For report.html, additionally verify: grep for '<img' to confirm PNG embeds exist, grep for 'mermaid' to confirm no CDN usage, grep for '<\\/script>' to confirm no broken escapes. GENERATION LOG (MANDATORY): After all files are generated, write {output_dir}/report-generation-log.md with: (1) a table of each deliverable (report.html, report.docx, report.pdf, executive-summary.pptx, structural-diagram.png, risk-overlay-diagram.png) with status (SUCCESS/FAILED), file size, and any errors encountered; (2) diagram rendering results (mermaid-cli exit codes, any warnings); (3) HTML validation check results (each grep check: PASS/FAIL with details); (4) corrections applied from validation-report.md (if team mode); (5) any issues encountered during generation and how they were handled; (6) overall self-assessed quality (HIGH/MEDIUM/LOW) with justification.

---

## Team — security-architect Phase 1 prompt

> You are performing Phase 1 (Reconnaissance) of a team security assessment against the project at {project_root}. Write output to {output_dir}/. Create the output directory if it does not exist. You have the threat-model skill loaded — execute ONLY Phase 1. Write 01-reconnaissance.md and visual-completeness-checklist.md. Be thorough — specialist agents (privacy, compliance, code review) and the diagram-specialist will read your 01-reconnaissance.md to understand the system. Do NOT proceed to Phase 2 or any other phase. The parent conversation handles all orchestration. EXECUTION LOG: At the end of 01-reconnaissance.md, include an ## Execution Log section per the agent output protocol at {refs_dir}/agent-output-protocol.md — document process health, what went well, issues encountered, what was skipped, and assumptions made during this phase.

---

## Team — security-architect Phases 3-6,8 prompt

> You are performing Phases 3-6 and 8 of a team security assessment against the project at {project_root}. Output directory: {output_dir}/. FIRST: Read back 01-reconnaissance.md and 02-structural-diagram.md from {output_dir}/ to re-establish context — these were produced by prior agents in this pipeline. You have the threat-model skill loaded — execute Phases 3, 4, 5, 6, and 8 (summary only). Write 03-threat-identification.md, 04-risk-quantification.md, 05-false-negative-hunting.md, 06-validated-findings.md, and 08-threat-model-report.md. Phase 8 is a SUMMARY ONLY — see the Phase 8 section in the skill for the reduced format. Do NOT produce Phase 2 or Phase 7 diagrams — those are handled by the diagram-specialist. Reference component names from 02-structural-diagram.md to ensure consistency with the diagrams. Be thorough — the parent conversation handles all orchestration. EXECUTION LOG: At the end of 08-threat-model-report.md, include an ## Execution Log section per the agent output protocol — document process health, what went well, issues encountered, what was skipped, and assumptions made across all phases you executed.

---

## Team — privacy-agent prompt

> Perform a full privacy impact assessment for the project at {project_root}. You have the privacy-impact-assessment skill loaded — follow its methodology and use its reference files in {refs_dir}/ to verify all regulation citations and LINDDUN threat types. Read the reconnaissance at {output_dir}/01-reconnaissance.md to understand the system. Follow the agent output protocol at {refs_dir}/agent-output-protocol.md — this includes the MANDATORY Execution Log section at the end of your output documenting process health, issues, skips, and assumptions. CRITICAL: For every regulation article you cite, verify it exists in {refs_dir}/gdpr-article-reference.md or {refs_dir}/global-privacy-regulations.md. For every LINDDUN threat type, verify it against {refs_dir}/linddun-go-threats.md. Write your output to {output_dir}/privacy-assessment.md. Include: data inventory, LINDDUN analysis, regulatory implications (GDPR, CCPA, HIPAA as applicable), privacy-specific recommendations.

---

## Team — grc-agent prompt

> Perform compliance gap analysis for the project at {project_root}. You have the compliance-assessment skill loaded — follow its methodology and use its reference files in {refs_dir}/ to verify all compliance control IDs. Read the reconnaissance at {output_dir}/01-reconnaissance.md to understand the system. Follow the agent output protocol at {refs_dir}/agent-output-protocol.md — this includes the MANDATORY Execution Log section at the end of your output documenting process health, issues, skips, and assumptions. CRITICAL: For every compliance control ID you cite, verify it exists in the appropriate reference file: {refs_dir}/soc2-trust-services-criteria.md, {refs_dir}/iso27001-annex-a-controls.md, {refs_dir}/nist-800-53-controls.md, {refs_dir}/pci-dss-v4-requirements.md, or {refs_dir}/hipaa-security-rule.md. Use {refs_dir}/cross-framework-mapping.md to verify cross-framework mappings. Write your report to {output_dir}/compliance-gap-analysis.md. Include: framework coverage (SOC 2, PCI-DSS, HIPAA, ISO 27001, NIST CSF as applicable), control mapping, gap analysis, remediation roadmap.

---

## Team — code-review-agent prompt

> Perform a targeted code security review for the project at {project_root}. Read the reconnaissance at {output_dir}/01-reconnaissance.md to understand the system and identify high-risk components. Follow the agent output protocol at {refs_dir}/agent-output-protocol.md — this includes the MANDATORY Execution Log section at the end of your output documenting process health, issues, skips, and assumptions. Focus on the top 3-5 highest-risk files/components identified in the reconnaissance. Write your findings to {output_dir}/code-security-review.md. Use CVSS v3.1 scoring. Include code evidence for every finding.

---

## Team — validation-specialist prompt

> You are the validation specialist. Read your full instructions from {refs_dir}/validation-specialist-agent.md. Read ALL assessment outputs in {output_dir}/: the 8 threat model phases (01-08; note that 08 is a summary), plus privacy-assessment.md, compliance-gap-analysis.md, and code-security-review.md. Also read the visual completeness checklist at {output_dir}/visual-completeness-checklist.md. Reference files are at {refs_dir}/ — this includes frameworks.md, agent-output-protocol.md, mermaid-spec.md, mermaid-layers.md, AND compliance framework references (soc2-trust-services-criteria.md, iso27001-annex-a-controls.md, nist-800-53-controls.md, pci-dss-v4-requirements.md, hipaa-security-rule.md, cross-framework-mapping.md) AND privacy references (gdpr-article-reference.md, global-privacy-regulations.md, linddun-go-threats.md). Use these to verify compliance and privacy IDs in Steps 5b and 5c. Perform all 8 validation steps from your instructions. Write {output_dir}/validation-report.md with all findings. The project root is {project_root}.

---

## Team — report-analyst prompt

> Generate the consolidated security assessment report from ALL outputs. OUTPUT DIRECTORY: {output_dir}/. Read ALL .md files in {output_dir}/ as inputs (01-reconnaissance.md through 08-threat-model-report.md — note that 08 is a summary, the full report structure comes from the template — plus privacy-assessment.md, compliance-gap-analysis.md, code-security-review.md, validation-report.md, visual-completeness-checklist.md). FIRST: Read the report template at {refs_dir}/report-template.md. Follow the template EXACTLY. You have Bash access. GENERATE ALL FOUR FORMATS using your docx, pdf, pptx, and frontend-design skills: 1. report.html 2. report.docx 3. report.pdf 4. executive-summary.pptx. CRITICAL: You MUST generate all four files yourself. When installing Python packages, ALWAYS use a venv: python3 -m venv /tmp/report-venv && source /tmp/report-venv/bin/activate && pip install python-docx python-pptx reportlab Pillow. Render Mermaid diagrams to PNG: npx -y @mermaid-js/mermaid-cli -i file.mmd -o file.png -c {refs_dir}/mermaid-config.json -w 3000 --scale 2 -b white. Deduplicate findings across all sources. Apply corrections from validation-report.md. The project root is {project_root}. HTML GENERATION RULES (MANDATORY): (1) Embed diagrams as pre-rendered PNG images using <img src="structural-diagram.png"> and <img src="risk-overlay-diagram.png"> — NEVER use Mermaid CDN (mermaid.js) for client-side rendering. (2) NEVER write <\/script> in HTML output — this JS-only escape breaks the HTML parser. Always write </script> literally. (3) Do not use defer/async on script tags that inline JS depends on. (4) All CSS and JS must be inline in the single HTML file (no external dependencies except the PNG images). BEFORE DECLARING DONE: Verify all files exist and are non-empty. For report.html, additionally verify: grep for '<img' to confirm PNG embeds exist, grep for 'mermaid' to confirm no CDN usage, grep for '<\\/script>' to confirm no broken escapes. GENERATION LOG (MANDATORY): After all files are generated, write {output_dir}/report-generation-log.md with: (1) a table of each deliverable (report.html, report.docx, report.pdf, executive-summary.pptx, structural-diagram.png, risk-overlay-diagram.png) with status (SUCCESS/FAILED), file size, and any errors encountered; (2) diagram rendering results (mermaid-cli exit codes, any warnings); (3) HTML validation check results (each grep check: PASS/FAIL with details); (4) corrections applied from validation-report.md; (5) any issues encountered during generation and how they were handled; (6) overall self-assessed quality (HIGH/MEDIUM/LOW) with justification.
