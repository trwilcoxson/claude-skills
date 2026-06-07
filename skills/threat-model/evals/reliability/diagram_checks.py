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


def check(report_text: str, recon: dict | None, findings_doc: dict | None) -> dict[str, Any]:
    defects: list[dict[str, str]] = []

    def add(code: str, detail: str) -> None:
        defects.append({"layer": "diagram", "code": code, "detail": detail})

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
    if unlabeled:
        add("untyped-edges", f"{len(unlabeled)}/{n_edges} edges have no label (spec §4: every arrow MUST be typed)")
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

    # ---- requirement 4: component metadata / ownership markers
    nodes = [n for b in blocks for n in _nodes(b)]
    owned = [n for n in nodes if re.search(OWNERSHIP, n)]
    own_frac = round(len(owned) / len(nodes), 3) if nodes else None
    if own_frac is not None and own_frac < 0.5:
        add("sparse-component-metadata", f"only {int(own_frac*100)}% of nodes carry ownership markers "
                                         f"([team:]/[vendor:]/[managed]); spec §7 wants metadata on components")

    # ---- requirement 5: risk layering linked to findings
    l4 = "\n".join(layers.get("L4", []))
    hi_components = set()
    if findings_doc:
        for f in findings_doc.get("findings", []):
            if f.get("severity") in ("HIGH", "CRITICAL"):
                hi_components.update(f.get("asset_refs", []))
    if "L4" in present:
        if not re.search(RISK_CLASS, l4):
            add("no-risk-coloring", "L4 overlay has no risk-class styling (highRisk/criticalRisk)")
        if not re.search(THREAT_ANNOT, l4):
            add("no-threat-annotations", "L4 overlay nodes carry no threat annotations (⚠ / L×I=score / BAND); spec §5")
        tm_in_l4 = set(re.findall(r"TM-\d{3}", l4))
        if hi_components and not tm_in_l4:
            add("risk-layer-not-linked", "L4 overlay does not reference any TM-NNN finding id — risk layer not linked to the report's findings")
        missing_hi = sorted(c for c in hi_components if c not in l4)
        if hi_components and len(missing_hi) > len(hi_components) * 0.5:
            add("high-findings-not-on-overlay",
                f"{len(missing_hi)}/{len(hi_components)} HIGH+ finding components are absent from the L4 overlay")

    diag_defect = bool(defects)
    return {
        "defects": defects,
        "stats": {"blocks": len(blocks), "layers": sorted(present), "size": size,
                  "edges": n_edges, "edges_annotated_frac": ann_frac,
                  "nodes": len(nodes), "ownership_frac": own_frac,
                  "subgraphs": subgraphs, "l4_links_findings": bool(re.search(r"TM-\d{3}", l4))},
        "scores": {"diagram_pass": not diag_defect,
                   "required_layers_present": not missing,
                   "flows_annotated": ann_frac,
                   "component_metadata": own_frac,
                   "risk_layer_linked": "L4" in present and bool(re.search(r"TM-\d{3}", l4))},
    }


if __name__ == "__main__":
    import json
    import sys
    rd = sys.argv[1]
    rep = open(f"{rd}/report.md").read()
    recon = json.load(open(f"{rd}/recon.json"))
    findings = json.load(open(f"{rd}/findings.json"))
    print(json.dumps(check(rep, recon, findings), indent=2))
