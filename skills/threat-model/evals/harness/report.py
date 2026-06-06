"""Render a self-contained HTML benchmark report (no external assets)."""
from __future__ import annotations

import html
from typing import Any

CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:2rem auto;max-width:1100px;color:#1a1a1a;padding:0 1rem}
h1{font-size:1.5rem;margin-bottom:.2rem}.sub{color:#666;margin-top:0}
table{border-collapse:collapse;width:100%;margin:1rem 0}
th,td{border:1px solid #ddd;padding:.45rem .6rem;text-align:left;vertical-align:top}
th{background:#f4f5f7}
.num{text-align:right;font-variant-numeric:tabular-nums}
.pass{color:#1a7f37;font-weight:600}.fail{color:#cf222e;font-weight:600}
.banner{padding:.7rem 1rem;border-radius:6px;margin:1rem 0}
.warn{background:#fff4e5;border:1px solid #f0b429}.ok{background:#e8f5e9;border:1px solid #66bb6a}
.delta-up{color:#1a7f37}.delta-down{color:#cf222e}
details{margin:.3rem 0}summary{cursor:pointer;color:#0969da}
.rubric{font-size:13px;background:#fafafa}.muted{color:#888}
code{background:#f0f1f3;padding:.05rem .3rem;border-radius:3px}
"""


def _esc(x: Any) -> str:
    return html.escape(str(x))


def _fmt(v: Any, suffix: str = "") -> str:
    return f"{v}{suffix}" if v is not None else '<span class="muted">—</span>'


def _pct(v: Any) -> str:
    return f"{v * 100:.0f}%" if v is not None else '<span class="muted">—</span>'


def _delta(skill: Any, base: Any, higher_better: bool = True) -> str:
    if skill is None or base is None:
        return '<span class="muted">—</span>'
    d = skill - base
    good = (d > 0) if higher_better else (d < 0)
    cls = "delta-up" if good else ("delta-down" if d else "muted")
    sign = "+" if d > 0 else ""
    return f'<span class="{cls}">{sign}{round(d, 3)}</span>'


def _summary_table(arms: dict[str, dict]) -> str:
    skill = arms.get("skill", {})
    base = arms.get("baseline", {})
    rows = [
        ("Cases run", skill.get("n"), base.get("n"), None),
        ("Pass rate", _pct(skill.get("pass_rate")), _pct(base.get("pass_rate")),
         _delta(skill.get("pass_rate"), base.get("pass_rate"))),
        ("Mean rubric score", skill.get("mean_score"), base.get("mean_score"),
         _delta(skill.get("mean_score"), base.get("mean_score"))),
        ("Mean elapsed (ms)", _fmt(skill.get("mean_elapsed_ms")), _fmt(base.get("mean_elapsed_ms")),
         _delta(skill.get("mean_elapsed_ms"), base.get("mean_elapsed_ms"), higher_better=False)),
        ("Mean tokens in", _fmt(skill.get("mean_tokens_in")), _fmt(base.get("mean_tokens_in")),
         _delta(skill.get("mean_tokens_in"), base.get("mean_tokens_in"), higher_better=False)),
        ("Mean tokens out", _fmt(skill.get("mean_tokens_out")), _fmt(base.get("mean_tokens_out")),
         _delta(skill.get("mean_tokens_out"), base.get("mean_tokens_out"), higher_better=False)),
    ]
    body = "".join(
        f"<tr><td>{_esc(label)}</td><td class='num'>{s}</td>"
        f"<td class='num'>{b}</td><td class='num'>{d if d is not None else ''}</td></tr>"
        for label, s, b, d in rows
    )
    return (
        "<table><thead><tr><th>Metric</th><th class='num'>Skill active</th>"
        "<th class='num'>Baseline (no skill)</th><th class='num'>Δ</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def _case_rows(cases: dict[str, dict], scored_by_case: dict[str, dict]) -> str:
    out = []
    for cid in sorted(cases):
        case = cases[cid]
        arms = scored_by_case.get(cid, {})
        skill = arms.get("skill")
        base = arms.get("baseline")

        def cell(s):
            if not s:
                return '<span class="muted">—</span>'
            verdict = '<span class="pass">PASS</span>' if s["passed"] else '<span class="fail">FAIL</span>'
            return f"{verdict} <span class='muted'>({s['weighted_score']})</span>"

        misses = (skill or base or {}).get("must_find_misses", [])
        miss_txt = ", ".join(_esc(m) for m in misses) if misses else '<span class="muted">none</span>'
        out.append(
            f"<tr><td><code>{_esc(cid)}</code><br><span class='muted'>{_esc(case['category'])}</span></td>"
            f"<td>{cell(skill)}</td><td>{cell(base)}</td><td>{miss_txt}</td></tr>"
        )
        detail = _rubric_detail(case, skill, base)
        if detail:
            out.append(f"<tr class='rubric'><td colspan='4'>{detail}</td></tr>")
    return "".join(out)


def _rubric_detail(case: dict, skill: dict | None, base: dict | None) -> str:
    def block(label, s):
        if not s or not s.get("rubric_scores"):
            return ""
        items = "".join(
            f"<li><b>{_esc(rs['id'])}</b> [{_esc(rs['verdict'])}] "
            f"{_esc(rs.get('justification', ''))}</li>"
            for rs in s["rubric_scores"]
        )
        sm = _esc(s.get("summary", ""))
        return f"<b>{label}</b><ul>{items}</ul>{('<i>' + sm + '</i>') if sm else ''}"

    parts = [p for p in (block("Skill arm", skill), block("Baseline arm", base)) if p]
    if not parts:
        return ""
    return f"<details><summary>rubric detail — {_esc(case['title'])}</summary>{''.join(parts)}</details>"


def _compare_banner(compare: dict[str, Any] | None) -> str:
    if not compare:
        return ""
    reg = compare.get("regression", [])
    out = compare.get("outgrowth", {})
    chunks = []
    if reg:
        ids = ", ".join(_esc(r["case_id"]) for r in reg)
        chunks.append(f"<div class='banner warn'><b>Regression vs baseline:</b> {len(reg)} case(s) "
                      f"lost ground — {ids}. The model may have changed; improve the skill.</div>")
    og = out.get("pass_rate")
    if og is not None and og >= 0.8:
        chunks.append(f"<div class='banner warn'><b>Outgrowth signal:</b> the base model passes "
                      f"{_pct(og)} of positive cases without the skill. Consider whether the skill still earns its keep.</div>")
    if not chunks:
        chunks.append("<div class='banner ok'>No regression vs baseline; skill still provides clear uplift.</div>")
    return "".join(chunks)


def render(run_id: str, generated: str, arms: dict[str, dict], cases: dict[str, dict],
           scored_by_case: dict[str, dict], compare: dict[str, Any] | None = None) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>threat-model evals — {_esc(run_id)}</title><style>{CSS}</style></head><body>
<h1>threat-model skill — eval &amp; benchmark report</h1>
<p class="sub">run <code>{_esc(run_id)}</code> · generated {_esc(generated)}</p>
{_compare_banner(compare)}
<h2>Benchmark — skill active vs baseline</h2>
{_summary_table(arms)}
<h2>Per-case results</h2>
<table><thead><tr><th>Case</th><th>Skill arm</th><th>Baseline arm</th><th>Missed must-finds</th></tr></thead>
<tbody>{_case_rows(cases, scored_by_case)}</tbody></table>
</body></html>"""
