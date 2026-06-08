"""Deterministic verification of the threat-model DIAGRAM against the skill's own spec.

Parses the Mermaid blocks the run produced (in report.md) and checks the taxonomy a robust
threat model must have: the required layers (L1-L4 per scaling), fully annotated/typed flows,
trust-boundary subgraphs, component metadata (ownership markers), and an L4 risk layer that
links to the findings (TM-NNN). Maps to the five diagram requirements; semantic correctness
(are boundaries placed right, are annotations accurate) is left to prompts/diagram-judge.md.
"""
from __future__ import annotations

import re
from typing import Any

EDGE_OPS = r"(?:-->|-\.->|--o|==>|--x|<-->)"
SENSITIVITY = r"\[(?:PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED)\]"
TYPED_PREFIX = r"\[(?:CTRL|AUTH|KEY|ADMIN|ASYNC|REPL|BUILD)\]"
OWNERSHIP = r"\[(?:team:|vendor:|managed|self-managed|control-owner:)"
RISK_CLASS = r":::(?:critical|high|med|medium|low)Risk|classDef\s+(?:critical|high|med|medium|low)Risk"
THREAT_ANNOT = r"⚠|×\s*\d|\d×\d|=\d+\s*(?:CRITICAL|HIGH|MEDIUM|LOW)"


def _blocks(report_text: str) -> list[str]:
    return re.findall(r"```mermaid\s(.*?)```", report_text, re.DOTALL)


def _layer_of(block: str) -> str | None:
    m = re.search(r"Layer:\s*(L[1-4])", block)
    if m:
        return m.group(1)
    low = block.lower()
    if "threat overlay" in low or "risk overlay" in low:
        return "L4"
    if "trust" in low and "identit" in low:
        return "L2"
    return None


def _edges(block: str) -> list[tuple[str, str | None]]:
    """Return (raw_line, label-or-None) for each edge operator occurrence."""
    out = []
    for line in block.splitlines():
        if re.search(EDGE_OPS, line):
            lbl = re.search(r"\|\s*\"?(.*?)\"?\s*\|", line)
            out.append((line.strip(), lbl.group(1) if lbl else None))
    return out


def _nodes(block: str) -> list[str]:
    # node definition lines: an id followed by a shape opener, or any :::class assignment
    out = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith(("%%", "classDef", "linkStyle", "style", "subgraph", "end", "class ")):
            continue
        if re.search(r"\w+\s*(?:\(\[|\[\(|\[\[|\{\{|\[/|\[|\(|\{)", s) or ":::" in s:
            out.append(s)
    return out


def _md_tables(text: str) -> list[dict]:
    """Extract GitHub-flavored markdown tables as {header:[...], rows:[[...]]}."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        sep = i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$", lines[i + 1])
        if "|" in lines[i] and sep:
            header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            rows, j = [], i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            out.append({"header": header, "rows": rows})
            i = j
        else:
            i += 1
    return out


def _section(text: str, *keywords: str) -> str:
    """Text from the first heading containing any keyword up to the next heading."""
    out, capture = [], False
    for ln in text.splitlines():
        if re.match(r"^#{1,6}\s", ln):
            if capture:
                break
            if any(k.lower() in ln.lower() for k in keywords):
                capture = True
            continue
        if capture:
            out.append(ln)
    return "\n".join(out)


def _typed(blocks: list[str], *types: str) -> list[str]:
    return [b for b in blocks if any(re.search(r"%%\s*type:\s*" + re.escape(t), b.lower()) for t in types)]


AUTH_VOCAB = ("login", "signin", "sign-in", "oauth", "oidc", "jwt", "saml", "session", "mfa",
              "otp", "auth", "token", "apikey", "api key", "password")


def analytical_checks(report_text: str, blocks: list[str], recon: dict | None, findings_doc: dict | None) -> dict[str, Any]:
    """Presence/shape/consistency of the analytical & communication visuals.

    Each visual is gated by a precondition derived from SKILL-DECLARED facts (kill_chains, roles,
    dep manifest, finding STRIDE/MITRE) — never from inferring content. Structure-only: a visual that
    is present and internally consistent passes even if its analysis is wrong (the judge handles that).
    """
    defects: list[dict[str, str]] = []
    warnings: list[str] = []

    def D(code: str, detail: str) -> None:
        defects.append({"layer": "diagram", "code": code, "detail": detail})

    recon = recon or {}
    findings_doc = findings_doc or {}
    findings = findings_doc.get("findings", [])
    kill_chains = findings_doc.get("kill_chains", [])
    roles = recon.get("roles", [])
    deps = recon.get("external_deps", [])
    recon_ids = {e["id"] for b in ("components", "data_stores", "entry_points", "trust_boundaries", "external_deps")
                 for e in recon.get(b, []) if isinstance(e, dict) and "id" in e}
    all_mitre = {m for f in findings for m in f.get("mitre", [])}
    present: list[str] = []

    # attack tree + attack-flow — gate: >=3 declared kill chains
    if len(kill_chains) >= 3:
        trees = [b for b in blocks if re.search(r"\{\s*(AND|OR)\s*\}", b)] + _typed(blocks, "attack-tree")
        trees = list(dict.fromkeys(trees))
        if not trees:
            D("no-attack-tree", f"{len(kill_chains)} kill chains declared but no attack tree (flowchart with AND/OR gates)")
        else:
            present.append("attack-tree")
            extra = {t for b in trees for t in re.findall(r"T\d{4}(?:\.\d{3})?", b)} - all_mitre
            if extra:
                warnings.append(f"attack tree references techniques absent from findings: {sorted(extra)[:5]}")
            if len(trees) < min(len(kill_chains), 5):
                warnings.append(f"{len(trees)} attack tree(s) for {len(kill_chains)} declared kill chains")
        flows = _typed(blocks, "attack-flow", "kill-chain")
        if not flows:
            D("no-attack-flow", f"{len(kill_chains)} kill chains declared but no attack-flow / kill-chain graph")
        else:
            present.append("attack-flow")

    # auth sequence — gate: auth surface (entry-point vocab OR S/E finding); name match may only SKIP
    auth_entry = any(any(k in (e.get("name", "") + " " + " ".join(e.get("evidence", []))).lower() for k in AUTH_VOCAB)
                     for e in recon.get("entry_points", []))
    auth_finding = any("S" in f.get("stride_lm", []) or "E" in f.get("stride_lm", []) for f in findings)
    if auth_entry or auth_finding:
        seqs = [b for b in blocks if "sequencediagram" in b.lower()[:60]]
        if not seqs:
            D("no-auth-sequence", "auth surface present but no sequenceDiagram rendered")
        else:
            present.append("auth-sequence")
            b = seqs[0]
            parts = re.findall(r"participant\s+(\w+)", b)
            if len(parts) < 2:
                D("auth-sequence-thin", f"sequence diagram has {len(parts)} participant(s) (<2)")
            if not re.search(r"--?>>?|->|-x", b):
                D("auth-sequence-no-arrows", "sequence diagram has no message arrows")
            opens = len(re.findall(r"\b(?:alt|opt|loop|par|rect)\b", b))
            if opens and len(re.findall(r"\bend\b", b)) < opens:
                warnings.append("sequence diagram block keywords (alt/opt/.../end) unbalanced")
            if recon_ids and parts and all(p not in recon_ids for p in parts):
                warnings.append("sequence participants do not map to recon ids")

    # STRIDE-per-element coverage matrix — gate: always
    stride = {"S", "T", "R", "I", "D", "E", "LM"}
    matrix = next((t for t in _md_tables(report_text) if stride.issubset({c.strip().upper() for c in t["header"]})), None)
    if not matrix:
        D("no-stride-matrix", "no STRIDE-per-element coverage matrix (table with S,T,R,I,D,E,LM columns)")
    else:
        present.append("stride-matrix")
        blanks = sum(1 for r in matrix["rows"] for c in r[1:] if not c.strip())
        if blanks:
            D("stride-matrix-blanks", f"STRIDE matrix has {blanks} blank cell(s); every cell must be TM-id / n/a / clean")
        body = " ".join(c for r in matrix["rows"] for c in r)
        miss = [f["id"] for f in findings if f["id"] not in body]
        if miss:
            warnings.append(f"{len(miss)} finding(s) not placed in STRIDE matrix: {miss[:5]}")

    # L×I risk heat map — gate: >=1 scored finding
    scored = [f for f in findings if isinstance(f.get("likelihood"), int) and isinstance(f.get("impact"), int)]
    if scored:
        hm = _section(report_text, "heat map", "heatmap", "risk matrix", "likelihood")
        if not hm or not re.search(r"TM-\d{3}", hm):
            D("no-risk-heatmap", "scored findings exist but no Likelihood×Impact heat map plotting them")
        else:
            present.append("risk-heatmap")
            miss = [f["id"] for f in scored if f["id"] not in hm]
            if miss:
                warnings.append(f"{len(miss)} scored finding(s) not plotted on heat map: {miss[:5]}")

    # MITRE ATT&CK technique layer — gate: >=1 finding with a technique
    if all_mitre:
        nav = [b for b in re.findall(r"```json\s(.*?)```", report_text, re.DOTALL) if '"techniques"' in b and '"domain"' in b]
        att = _section(report_text, "att&ck", "attack navigator", "mitre att", "technique heatmap")
        if not nav and not re.search(r"T\d{4}", att):
            D("no-attack-layer", "findings map to ATT&CK techniques but no ATT&CK technique layer/heatmap rendered")
        else:
            present.append("attack-layer")
            shown = {t for src in ([att] + nav) for t in re.findall(r"T\d{4}(?:\.\d{3})?", src)}
            if all_mitre - shown:
                warnings.append(f"ATT&CK layer missing techniques from findings: {sorted(all_mitre - shown)[:5]}")

    # RBAC / authorization matrix — gate: >=2 declared roles
    if len(roles) >= 2:
        rbac = _section(report_text, "rbac", "authorization matrix", "access control matrix", "role-by-resource")
        if not rbac or not re.search(r"anon|unauth", rbac.lower()):
            D("no-rbac-matrix", f"{len(roles)} roles declared but no RBAC/authorization matrix with an anonymous row")
        else:
            present.append("rbac-matrix")

    # SBOM / dependency graph — gate: external deps backed by a manifest
    if deps and any(e.get("manifest") for e in deps):
        sbom = _typed(blocks, "sbom", "dependency")
        sec = _section(report_text, "sbom", "dependency", "software bill")
        if not sbom and not (sec and "externaldep" in sec.lower()):
            D("no-sbom-graph", "external dependencies with a manifest but no SBOM / dependency graph")
        else:
            present.append("sbom")

    return {"defects": defects, "warnings": warnings,
            "stats": {"analytical_present": present, "kill_chains": len(kill_chains), "roles": len(roles)}}


def check(report_text: str, recon: dict | None, findings_doc: dict | None) -> dict[str, Any]:
    defects: list[dict[str, str]] = []
    warnings: list[str] = []

    def add(code: str, detail: str) -> None:
        defects.append({"layer": "diagram", "code": code, "detail": detail})

    def warn(detail: str) -> None:
        warnings.append(detail)

    blocks = _blocks(report_text)
    if not blocks:
        add("no-diagram", "report.md contains no ```mermaid diagram blocks")
        return {"defects": defects, "stats": {"blocks": 0}, "scores": {"diagram_pass": False}}

    layers = {}
    for b in blocks:
        L = _layer_of(b)
        if L:
            layers.setdefault(L, []).append(b)

    # ---- requirement 1: taxonomy / required layers per scaling
    size = 0
    if recon:
        size = len(recon.get("components", [])) + len(recon.get("data_stores", []))
    required = {"L1", "L2", "L3", "L4"} if size > 5 else {"L1", "L4"}
    present = set(layers)
    missing = sorted(required - present)
    if missing:
        add("missing-layers", f"system size {size} needs {sorted(required)}; missing {missing} "
                              f"(present: {sorted(present) or 'none-tagged'})")
    if not re.search(r"%%\s*Version:", "\n".join(blocks)):
        add("no-version-stamp", "no `%% Version:` stamp on any diagram (spec §6)")
    if "legend" not in report_text.lower():
        add("no-legend", "no legend subgraph found (spec §6 requires a legend)")
    if not re.search(r"classDef", "\n".join(blocks)):
        add("no-classdefs", "no classDef block (spec §8) — risk/role styling absent")

    # ---- requirement 2: fully annotated / typed flows
    all_edges = [e for b in blocks for e in _edges(b)]
    n_edges = len(all_edges)
    unlabeled = [e for e in all_edges if not e[1]]
    annotated = [e for e in all_edges if e[1] and (re.search(SENSITIVITY, e[1]) or re.search(TYPED_PREFIX, e[1]))]
    ann_frac = round(len(annotated) / n_edges, 3) if n_edges else None
    if n_edges and len(unlabeled) / n_edges > 0.10:
        add("untyped-edges", f"{len(unlabeled)}/{n_edges} edges unlabeled (>10%; spec §4: every arrow MUST be typed)")
    elif unlabeled:
        warn(f"{len(unlabeled)}/{n_edges} edges unlabeled (spec §4 wants every arrow typed)")
    if ann_frac is not None and ann_frac < 0.6:
        add("under-annotated-flows", f"only {int(ann_frac*100)}% of edges carry a sensitivity/type "
                                     f"annotation ([CONFIDENTIAL]/[AUTH]/etc.); spec §4 wants every flow annotated")

    # ---- requirement 3: trust boundaries
    subgraphs = len(re.findall(r"\bsubgraph\b", "\n".join(blocks)))
    n_tb = len(recon.get("trust_boundaries", [])) if recon else 0
    if size > 5 and "L2" in present and subgraphs == 0:
        add("no-trust-boundary-subgraphs", "L2 present but no subgraph trust-boundary zones drawn")
    if n_tb and subgraphs < min(n_tb, 2):
        add("few-trust-boundaries", f"recon lists {n_tb} trust boundaries but the diagram has {subgraphs} subgraph zone(s)")

    # ---- requirement 4: component metadata / ownership markers (on L1 process/data-store nodes)
    l1_text = "\n".join(layers.get("L1") or blocks[:1])
    comp_nodes = [n for n in _nodes(l1_text) if re.search(r"\(\[|\[\(", n)]  # process ([..]) / data store [(..)]
    owned = [n for n in comp_nodes if re.search(OWNERSHIP, n)]
    own_frac = round(len(owned) / len(comp_nodes), 3) if comp_nodes else None
    if own_frac is not None and own_frac < 0.1:
        add("no-component-metadata", f"L1 components carry almost no ownership markers ({int(own_frac*100)}%); spec §7")
    elif own_frac is not None and own_frac < 0.5:
        warn(f"only {int(own_frac*100)}% of L1 components carry ownership markers ([team:]/[vendor:]/[managed]); spec §7 wants more")

    # ---- requirement 5: risk layering linked to findings (matched by TM-NNN, the shared id scheme)
    l4 = "\n".join(layers.get("L4", []))
    hi_tm = [f["id"] for f in (findings_doc.get("findings", []) if findings_doc else [])
             if f.get("severity") in ("HIGH", "CRITICAL")]
    if "L4" in present:
        if not re.search(RISK_CLASS, l4):
            add("no-risk-coloring", "L4 overlay has no risk-class styling (highRisk/criticalRisk)")
        if not re.search(THREAT_ANNOT, l4):
            add("no-threat-annotations", "L4 overlay nodes carry no threat annotations (⚠ / L×I=score / BAND); spec §5")
        tm_in_l4 = set(re.findall(r"TM-\d{3}", l4))
        if hi_tm and not tm_in_l4:
            add("risk-layer-not-linked", "L4 overlay references no TM-NNN finding id — risk layer not linked to findings")
        elif hi_tm:
            covered_hi = [t for t in hi_tm if t in tm_in_l4]
            if len(covered_hi) / len(hi_tm) < 0.8:
                add("high-findings-not-on-overlay",
                    f"only {len(covered_hi)}/{len(hi_tm)} HIGH+ findings are annotated in the L4 overlay")
            elif len(covered_hi) < len(hi_tm):
                warn(f"{len(hi_tm) - len(covered_hi)}/{len(hi_tm)} HIGH+ findings not annotated in L4 overlay")

    # analytical & communication visuals (gated by skill-declared facts; structure-only)
    an = analytical_checks(report_text, blocks, recon, findings_doc)
    defects.extend(an["defects"])
    warnings.extend(an["warnings"])

    diag_defect = bool(defects)
    return {
        "defects": defects,
        "stats": {"blocks": len(blocks), "layers": sorted(present), "size": size,
                  "edges": n_edges, "edges_annotated_frac": ann_frac,
                  "components": len(comp_nodes), "ownership_frac": own_frac,
                  "subgraphs": subgraphs, "l4_links_findings": bool(re.search(r"TM-\d{3}", l4)),
                  "visuals_present": an["stats"]["analytical_present"],
                  "kill_chains": an["stats"]["kill_chains"],
                  "warnings": warnings},
        "scores": {"diagram_pass": not diag_defect,
                   "required_layers_present": not missing,
                   "flows_annotated": ann_frac,
                   "component_metadata": own_frac,
                   "risk_layer_linked": "L4" in present and bool(re.search(r"TM-\d{3}", l4)),
                   "analytical_visuals": an["stats"]["analytical_present"]},
    }


if __name__ == "__main__":
    import json
    import sys
    rd = sys.argv[1]
    rep = open(f"{rd}/report.md").read()
    recon = json.load(open(f"{rd}/recon.json"))
    findings = json.load(open(f"{rd}/findings.json"))
    print(json.dumps(check(rep, recon, findings), indent=2))
