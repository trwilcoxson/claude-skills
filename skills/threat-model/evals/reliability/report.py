"""Self-contained HTML reliability report for one target across N runs."""
from __future__ import annotations

import html
from typing import Any

CSS = """
body{font:14px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;max-width:1050px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}
h1{font-size:1.5rem;margin-bottom:.1rem}h2{margin-top:1.8rem;border-bottom:1px solid #eee;padding-bottom:.2rem}
.sub{color:#666;margin-top:0}
table{border-collapse:collapse;width:100%;margin:.6rem 0}th,td{border:1px solid #ddd;padding:.45rem .6rem;text-align:left}
th{background:#f4f5f7}.num{text-align:right;font-variant-numeric:tabular-nums}
.ok{color:#1a7f37;font-weight:600}.bad{color:#cf222e;font-weight:600}.mut{color:#888}
.banner{padding:.7rem 1rem;border-radius:6px;margin:1rem 0}
.green{background:#e8f5e9;border:1px solid #66bb6a}.amber{background:#fff4e5;border:1px solid #f0b429}.red{background:#fdecea;border:1px solid #ef5350}
code{background:#f0f1f3;padding:.05rem .3rem;border-radius:3px}li{margin:.15rem 0}
"""


def _e(x: Any) -> str:
    return html.escape(str(x))


def _pct(v) -> str:
    return f"{v*100:.0f}%" if isinstance(v, (int, float)) else '<span class="mut">—</span>'


def _yn(v) -> str:
    return '<span class="ok">pass</span>' if v else '<span class="bad">FAIL</span>'


def _contract(runs: list[dict]) -> str:
    rows = ""
    for i, r in enumerate(runs):
        sc, st = r["scores"], r["stats"]
        rows += (f"<tr><td>run {i+1}</td><td>{_yn(sc['structure_pass'])}</td>"
                 f"<td>{_yn(sc['consistency_pass'])}</td><td class='num'>{_pct(sc['grounding'])}</td>"
                 f"<td class='num'>{_pct(sc['coverage'])}</td>"
                 f"<td>{_yn(sc.get('diagram_pass'))}</td>"
                 f"<td class='num'>{st['findings']}</td>"
                 f"<td class='num'>{st['surface_covered']}/{st['surface_elements']}</td>"
                 f"<td class='num'>{len(r['defects'])}</td></tr>")
    return ("<table><thead><tr><th>Run</th><th>Structure</th><th>Consistency</th><th>Grounding</th>"
            "<th>Coverage</th><th>Diagram</th><th>Findings</th><th>Surface examined</th><th>Defects</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")


def _diagram(runs: list[dict]) -> str:
    rows = ""
    for i, r in enumerate(runs):
        ds = r["stats"].get("diagram", {})
        rows += (f"<tr><td>run {i+1}</td><td>{_e(ds.get('layers'))}</td>"
                 f"<td class='num'>{_pct(ds.get('edges_annotated_frac'))}</td>"
                 f"<td class='num'>{_pct(ds.get('ownership_frac'))}</td>"
                 f"<td class='num'>{ds.get('subgraphs', '—')}</td>"
                 f"<td>{'yes' if ds.get('l4_links_findings') else '<span class=bad>no</span>'}</td></tr>")
    return ("<p>The diagram is verified against the skill's own spec: required layers (L1–L4 per scaling), "
            "typed/annotated flows (§4), trust-boundary subgraphs, component ownership markers (§7), and an "
            "L4 risk overlay linked to the findings (§5). Semantic correctness is left to the diagram judge.</p>"
            "<table><thead><tr><th>Run</th><th>Layers present</th><th>Flows annotated</th>"
            "<th>Component metadata</th><th>Trust-boundary subgraphs</th><th>L4→findings linked</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")


def _defects(runs: list[dict]) -> str:
    alld = [(i + 1, d) for i, r in enumerate(runs) for d in r["defects"]]
    if not alld:
        return '<p class="ok">No deterministic defects across any run — the structural/consistency/grounding/coverage contract held on every run.</p>'
    out = "<table><thead><tr><th>Run</th><th>Layer</th><th>Code</th><th>Detail</th></tr></thead><tbody>"
    for i, d in alld:
        out += f"<tr><td>{i}</td><td>{_e(d['layer'])}</td><td><code>{_e(d['code'])}</code></td><td>{_e(d['detail'])}</td></tr>"
    return out + "</tbody></table>"


def _quality(q: dict | None) -> str:
    if not q:
        return '<p class="mut">no quality judgment recorded</p>'
    parts = [f"<p>Mean attack-path soundness: <b>{_pct(q.get('mean_soundness'))}</b> · "
             f"proportionality: <b>{_e(q.get('proportionality','?'))}</b> "
             f"(judged on run 1, {q.get('n_judged','?')} findings sampled).</p>"]
    weak = q.get("weak_findings") or []
    if weak:
        parts.append("<p>Findings the judge flagged as weak (path or severity not defensible):</p><ul>"
                     + "".join(f"<li><code>{_e(w.get('id'))}</code> — {_e(w.get('reason'))}</li>" for w in weak) + "</ul>")
    return "".join(parts)


def _recall(rc: dict | None) -> str:
    if not rc:
        return '<p class="mut">no adversarial recall recorded</p>'
    gaps = rc.get("confirmed_gaps") or []
    if not gaps:
        return '<p class="ok">An independent red-team agent found no significant (HIGH+) grounded risk the model missed.</p>'
    out = "<p>Confirmed recall gaps (grounded in the repo, HIGH+, not covered by the model, survived a second-agent check):</p><ul>"
    for g in gaps:
        out += f"<li><b>{_e(g.get('title'))}</b> [{_e(g.get('severity'))}] — {_e(g.get('why_missed') or g.get('detail',''))}</li>"
    return out + "</ul>"


def _recon_audit(ra: dict | None) -> str:
    if not ra:
        return '<p class="mut">no recon-completeness audit recorded</p>'
    missed = ra.get("missed_subsystems") or []
    if not missed:
        return '<p class="ok">Recon enumerated every major subsystem present in the repo (coverage denominator is trustworthy).</p>'
    return ("<p class=\"bad\">Recon missed subsystems present in the repo — coverage % above is optimistic for these:</p><ul>"
            + "".join(f"<li>{_e(m)}</li>" for m in missed) + "</ul>")


def _stability(s: dict | None) -> str:
    if not s:
        return '<p class="mut">single run — no stability measured</p>'
    out = [f"<p>Core (HIGH+) sizes per run: {_e(s['core_sizes'])} · stable core (present in all {s['n_runs']} runs): "
           f"<b>{s['stable_core_count']}/{s['total_distinct_core']}</b> ({_pct(s['stable_core_ratio'])}) · "
           f"mean pairwise overlap: <b>{_pct(s['mean_pairwise_jaccard'])}</b>.</p>"]
    if s.get("stable_core"):
        out.append("<p>Stable core (the system reliably surfaces these every run):</p><ul>"
                   + "".join(f"<li>[{_e(c['severity'])}] {_e(c['title'])}</li>" for c in s["stable_core"]) + "</ul>")
    if s.get("unstable"):
        out.append("<p>Variable (appeared in some runs, not all — acceptable for breadth, watch if HIGH+):</p><ul>"
                   + "".join(f"<li>[{_e(c['severity'])}] {_e(c['title'])} — {c['in_runs']}/{s['n_runs']} runs</li>" for c in s["unstable"]) + "</ul>")
    return "".join(out)


def _verdict(runs, recall, stability) -> str:
    total_def = sum(len(r["defects"]) for r in runs)
    gaps = (recall or {}).get("confirmed_gaps") or []
    stable_ratio = (stability or {}).get("stable_core_ratio")
    if total_def == 0 and not gaps and (stable_ratio is None or stable_ratio >= 0.8):
        return ('<div class="banner green"><b>Reliable on this target.</b> Deterministic contract held on every run, '
                'no confirmed recall gaps, and the high-severity core is stable across runs.</div>')
    cls = "red" if (total_def or gaps) else "amber"
    bits = []
    if total_def:
        bits.append(f"{total_def} deterministic defect(s)")
    if gaps:
        bits.append(f"{len(gaps)} confirmed recall gap(s)")
    if stable_ratio is not None and stable_ratio < 0.8:
        bits.append(f"unstable core ({_pct(stable_ratio)})")
    return f'<div class="banner {cls}"><b>Reliability issues on this target:</b> {", ".join(bits)}. See sections below.</div>'


def render(target: dict, runs: list[dict], agents: dict, stability: dict | None, generated: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>reliability — {_e(target['id'])}</title><style>{CSS}</style></head><body>
<h1>threat-model — reliability report</h1>
<p class="sub">target <code>{_e(target['id'])}</code> · {_e(target.get('source',''))} · {len(runs)} run(s) · generated {_e(generated)}</p>
{_verdict(runs, agents.get('recall'), stability)}
<h2>Deterministic contract (per run)</h2>
<p>Reference-free: structure, internal consistency (<code>severity == band(L×I)</code>, counts, refs), grounding against the real repo, and coverage of the system's own discovered surface. Should hold on every run regardless of target.</p>
{_contract(runs)}
<h3>Diagram verification</h3>
{_diagram(runs)}
<h3>Defects</h3>
{_defects(runs)}
<h2>Reasoning quality (judged, sampled)</h2>
{_quality(agents.get('quality'))}
<h2>Adversarial recall (reference-free completeness)</h2>
{_recall(agents.get('recall'))}
<h2>Recon completeness (coverage-denominator guard)</h2>
{_recon_audit(agents.get('recon_audit'))}
<h2>Stability across runs</h2>
{_stability(stability)}
</body></html>"""
