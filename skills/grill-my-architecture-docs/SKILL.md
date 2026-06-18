---
name: grill-my-architecture-docs
description: Relentlessly interview the user about a software architecture document through a chosen stakeholder lens — security, finops, compliance, reliability, product, engineering, data, or architecture-review — each with its own enterprise-grade rubric, closing every gap inline. Use when the user wants to stress-test, gap-check, threat-model, or finish an architecture/design doc for a specific audience, or mentions "grill my architecture docs". Invoke as /grill-my-architecture-docs <mode> <path-or-Atlassian-hint>; omit the mode for a cross-cutting triage. Works on local files or Confluence/Jira via the Atlassian MCP.
---

<modes>

My first argument is the stakeholder lens; everything after it points at the document(s) — a local path, or a hint for finding the page in Confluence/Jira. The lenses do not share a rubric. A security grill is an enterprise threat model; a finops grill is a cost and unit-economics audit; they have nothing in common but the protocol below. Pick the lens, then go deep on it — don't dilute a security pass with product questions.

| Argument | Lens | Rubric |
| --- | --- | --- |
| `security`, `sec`, `appsec`, `threat` | Security / threat modeling | [modes/security.md](modes/security.md) |
| `finops`, `cost`, `cost-optimization` | FinOps / cost | [modes/finops.md](modes/finops.md) |
| `compliance`, `privacy`, `legal`, `audit` | Compliance, privacy, legal | [modes/compliance.md](modes/compliance.md) |
| `reliability`, `ops`, `sre`, `operations` | Operations / SRE | [modes/reliability.md](modes/reliability.md) |
| `product`, `po`, `business` | Product owner / business | [modes/product.md](modes/product.md) |
| `engineering`, `eng`, `dev`, `impl` | Engineering / implementers | [modes/engineering.md](modes/engineering.md) |
| `data`, `analytics` | Data / analytics | [modes/data.md](modes/data.md) |
| `architecture`, `ea`, `review-board` | Enterprise architecture review | [modes/architecture.md](modes/architecture.md) |
| *(none)*, `all`, `overview` | Cross-cutting triage | [modes/overview.md](modes/overview.md) |

Load only the selected mode file. If the argument matches no lens, show me this table and ask which one. With no mode, run the overview: survey every lens shallowly, report which are weakest, and recommend the deep mode(s) to run next.

</modes>

<protocol>

The shared loop for every mode:

1. **Locate the document** (see below) and read the whole thing before grilling.
2. **Understand the system first.** Before touching the rubric, build a short context brief: what the business does and who this serves, the sensitivity of the data, the system's scale and criticality, the deployment and tech context, the regulatory exposure, and — most important — what this document is *for* (a new build, a change, a review) and how large its blast radius is. Infer it from the doc and the codebase; ask me only what you can't. This brief calibrates how hard to push on each rubric item. See <using-the-rubric>.
3. **Build the coverage map.** Walk *every* item in the selected mode's rubric and give each an explicit verdict — covered, a gap, or not applicable — with a one-line reason for anything you mark covered or N/A, judged against what the doc actually says and the context brief, not what you assume the system does. Add any context-specific concern the rubric didn't name.
4. **Grill one question at a time.** Walk the map in the mode's grill order, gaps first. For each, name the consequence ("a security reviewer can't sign off without knowing where PII crosses a trust boundary"), give the recommended answer you'd write — drafted from the doc and the codebase — then wait for my answer. Push back on vague answers, or ones that contradict the code or an earlier answer. If the codebase can answer it, read the code instead of asking me.
5. **Capture as you go.** Write each settled answer down immediately, preserving the doc's structure — into the local file if that's the source, or into a local staging copy if the source is a live Confluence/Jira page (never the live page mid-session). See <writing-back> for how a staged copy reaches the live page.
6. **Produce the mode's deliverable.** Each rubric ends with the concrete artifact to leave in the doc — an annotated data-flow diagram and STRIDE matrix for security, a unit-cost model for finops, and so on. Build it as answers land, not at the end.
7. **Record what's deferred** under an "Open questions" section, with the stakeholder it affects and why it matters. Never drop a gap silently.

End only when every rubric item is resolved — covered, deferred, or marked not-applicable with a reason — and the context-specific concerns you surfaced are resolved too.

</protocol>

<using-the-rubric>

The rubric is a floor, not a script. Avoid failing in either direction:

- **Don't follow it blindly.** A checklist walked without understanding the system produces generic, low-value questions and misses what actually matters here. Let the context brief set the depth and order — a single-tenant internal tool and a multi-tenant fintech platform both hit the security rubric, but not at the same intensity. Spend the grill where the risk and the stakes are.
- **Don't silently skip.** Every rubric item gets a verdict — relevant gap, already covered, or not applicable with a reason. "Not applicable" is a fine answer; an item you never considered is not. This is how the skill guarantees no category is forgotten.
- **Go past the list.** When the context raises a concern the rubric doesn't name, grill it anyway and record it. The rubric catches the known gaps for this lens; your judgment catches the ones specific to this system.

</using-the-rubric>

<locating-the-document>

- **Local file** — if I give a path or point at a downloaded or exported doc, read it.
- **Confluence / Jira** — if the doc lives in Atlassian, load the Atlassian MCP tools with ToolSearch (search `atlassian`, `confluence`, `jira`) and identify three capabilities by name before you start: page/CQL title search, fetch-page-body, and update/publish. Search by title or CQL, then fetch the page body. If more than one page matches, show me the candidates and confirm which before grilling. Treat update/publish as the dangerous one — it stays gated behind my approval (see <writing-back>).
- **Neither available** — ask me for a path, a pasted copy, or to connect the Atlassian MCP. Don't grill from memory.

If a path or page resolves but its body won't load — permission denied, an empty export, an unparseable PDF or binary — say so and fall back to asking me. Never build the coverage map from a doc you couldn't actually read. Pin the write-back path (direct edit vs staged-then-approved) before the first answer lands.

</locating-the-document>

<writing-back>

- **Local docs** — edit the file directly as answers land.
- **Confluence / Jira pages** — write to a local staging copy during the session; never edit the live page mid-grill. At the end, show me the full diff and publish through the Atlassian MCP's update tool only after I approve, since that publishes to everyone who watches the page.

Keep diagrams in sync with the words. When an answer changes a boundary, a data flow, or a component, update the diagram if it's editable; when it isn't — an image, a draw.io/Gliffy macro, an externally rendered PlantUML diagram — drop a precise "diagram out of date: <what changed>" note beside it and surface that in the final diff, rather than letting the prose and the picture quietly disagree.

</writing-back>
