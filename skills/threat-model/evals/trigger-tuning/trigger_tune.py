#!/usr/bin/env python3
"""Trigger tuning for the threat-model skill description (Skills 2.0 feature H).

The skill only fires if its frontmatter `description` makes Claude pick it. This tool
measures that, deterministically where it can:

  split                      60/40 train / held-out partition (stable hash of query id)
  template --out obs.json    emit an observation file to fill in
  report --observations f    score each candidate description on the held-out set, pick a winner

The measurement itself is agent-driven: for each candidate description and each query, run the
activation decision 3x (per the spec) and record how often the skill triggered. Feed those counts
back via the observation file. Iterate the wording up to ~5 candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
QUERIES = ROOT / "queries.yaml"
HELD_OUT_FRACTION = 0.40


def load_queries() -> list[dict]:
    return yaml.safe_load(QUERIES.read_text())["queries"]


def held_out(qid: str) -> bool:
    """Stable partition: hash the id, last two digits land in the held-out 40%."""
    h = int(hashlib.sha1(qid.encode()).hexdigest(), 16) % 100
    return h >= (1 - HELD_OUT_FRACTION) * 100


def cmd_split(_args) -> None:
    qs = load_queries()
    train = [q["id"] for q in qs if not held_out(q["id"])]
    test = [q["id"] for q in qs if held_out(q["id"])]
    print(f"train ({len(train)}): {', '.join(train)}")
    print(f"held-out ({len(test)}): {', '.join(test)}")


def cmd_template(args) -> None:
    qs = load_queries()
    obs = {
        "runs_per_query": 3,
        "candidates": {
            "current": {q["id"]: {"triggered": 0, "runs": 3} for q in qs},
        },
        "_note": "Add more candidate keys (e.g. 'rev2') with the same shape. 'triggered' = how many of 'runs' activations fired the skill.",
    }
    Path(args.out).write_text(json.dumps(obs, indent=2))
    print(f"wrote {args.out} — fill in 'triggered' counts per query per candidate")


def _score(candidate: dict, qs: list[dict], scope: str) -> dict:
    by_id = {q["id"]: q for q in qs}
    pos, neg = [], []
    for qid, rec in candidate.items():
        q = by_id.get(qid)
        if not q:
            continue
        if scope == "held-out" and not held_out(qid):
            continue
        rate = rec["triggered"] / rec["runs"] if rec["runs"] else 0.0
        (pos if q["should_trigger"] else neg).append((qid, rate))
    tpr = sum(r for _, r in pos) / len(pos) if pos else None          # want high
    far = sum(r for _, r in neg) / len(neg) if neg else None          # false activation, want low
    bal = ((tpr or 0) + (1 - (far or 0))) / 2 if (pos or neg) else None
    return {"tpr": tpr, "false_activation": far, "balanced": bal,
            "misses": [qid for qid, r in pos if r < 1.0],
            "false_fires": [qid for qid, r in neg if r > 0.0]}


def cmd_report(args) -> None:
    qs = load_queries()
    obs = json.loads(Path(args.observations).read_text())
    rows = {name: _score(cand, qs, "held-out") for name, cand in obs["candidates"].items()}
    ranked = sorted(rows.items(), key=lambda kv: (kv[1]["balanced"] or 0), reverse=True)
    best = ranked[0][0] if ranked else None
    out = Path(args.out)
    out.write_text(_render(rows, best))
    print(f"wrote {out}")
    for name, s in ranked:
        b = f"{s['balanced'] * 100:.0f}%" if s["balanced"] is not None else "—"
        t = f"{s['tpr'] * 100:.0f}%" if s["tpr"] is not None else "—"
        f = f"{s['false_activation'] * 100:.0f}%" if s["false_activation"] is not None else "—"
        mark = "  <- best" if name == best else ""
        print(f"  {name:12} balanced {b}  trigger {t}  false-fire {f}{mark}")


def _render(rows: dict, best: str | None) -> str:
    def pct(v):
        return f"{v * 100:.0f}%" if v is not None else "—"

    body = ""
    for name, s in sorted(rows.items(), key=lambda kv: (kv[1]["balanced"] or 0), reverse=True):
        star = " ★" if name == best else ""
        body += (
            f"<tr><td>{html.escape(name)}{star}</td><td class='num'>{pct(s['balanced'])}</td>"
            f"<td class='num'>{pct(s['tpr'])}</td><td class='num'>{pct(s['false_activation'])}</td>"
            f"<td>{', '.join(s['misses']) or '—'}</td><td>{', '.join(s['false_fires']) or '—'}</td></tr>"
        )
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>trigger tuning</title>
<style>body{{font:14px -apple-system,Segoe UI,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:.4rem .6rem;text-align:left}}
th{{background:#f4f5f7}}.num{{text-align:right;font-variant-numeric:tabular-nums}}</style></head><body>
<h1>threat-model — trigger tuning (held-out set)</h1>
<p>Balanced = (trigger rate on positives + non-fire rate on negatives) / 2. Higher is better.</p>
<table><thead><tr><th>Candidate description</th><th class='num'>Balanced</th><th class='num'>Trigger (pos)</th>
<th class='num'>False-fire (neg)</th><th>Missed positives</th><th>False fires</th></tr></thead>
<tbody>{body}</tbody></table></body></html>"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("split").set_defaults(func=cmd_split)
    pt = sub.add_parser("template")
    pt.add_argument("--out", default="observations.json")
    pt.set_defaults(func=cmd_template)
    pr = sub.add_parser("report")
    pr.add_argument("--observations", required=True)
    pr.add_argument("--out", default="trigger-report.html")
    pr.set_defaults(func=cmd_report)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
