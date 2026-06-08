#!/usr/bin/env python3
"""tm-observe — uncluttered "what agent is doing what" view over a run-event stream.

A pure, read-only function of events.ndjson -> terminal text. No analysis, no scheduling, no agent
spawning; the same file always renders the same output. Views:
  --tail   (default) one fixed-column line per event
  --tree   grouped stage -> persona with durations
  --once   final per-persona summary
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SYM = {"start": "▶", "done": "✔", "error": "✖"}  # ▶ ✔ ✖


def _load(path: str) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def _order(events: list[dict]) -> list[dict]:
    return sorted(events, key=lambda e: (e["seq"] if e.get("seq") is not None else 10**18, e.get("ts", "")))


def _hhmmss(ts: str) -> str:
    # ISO ts -> HH:MM:SS without importing a clock (pure string slice)
    m = ts.split("T")
    return m[1][:8] if len(m) == 2 else ts[:8]


def _metrics(m: dict) -> str:
    if not m:
        return ""
    if "elapsed_ms" in m and m["elapsed_ms"] is not None:
        s = m["elapsed_ms"] / 1000
        m = {**m, "elapsed": f"{int(s//60)}m{int(s%60):02d}s" if s >= 60 else f"{s:.0f}s"}
        m.pop("elapsed_ms")
    return "  ".join(f"{k}={v}" for k, v in m.items() if v is not None)


def tail(events: list[dict]) -> str:
    out = []
    for e in _order(events):
        out.append(f"{_hhmmss(e.get('ts',''))}  {e.get('side',''):5}  {e.get('stage',''):11}  "
                   f"{e.get('persona',''):18}  {SYM.get(e.get('status'),' ')} {e.get('status',''):5} "
                   f"{e.get('action',''):10} {_metrics(e.get('metrics',{}))}".rstrip())
    return "\n".join(out)


def tree(events: list[dict]) -> str:
    by_stage: dict[str, list[dict]] = {}
    for e in _order(events):
        by_stage.setdefault(e.get("stage", ""), []).append(e)
    out = []
    for stage, evs in by_stage.items():
        out.append(f"{stage}")
        # pair start/done per (persona, action)
        starts = {}
        for e in evs:
            key = (e.get("persona"), e.get("action"))
            if e["status"] == "start":
                starts[key] = e
            elif e["status"] in ("done", "error"):
                dur = _metrics(e.get("metrics", {}))
                mark = SYM.get(e["status"], " ")
                out.append(f"  {mark} {e.get('persona',''):20} {e.get('action',''):12} {dur}")
        # personas that started but never finished
        seen_done = {(e.get("persona"), e.get("action")) for e in evs if e["status"] in ("done", "error")}
        for key, e in starts.items():
            if key not in seen_done:
                out.append(f"  {SYM['start']} {e.get('persona',''):20} {e.get('action',''):12} (running)")
    return "\n".join(out)


def once(events: list[dict]) -> str:
    agg: dict[tuple, dict] = {}
    for e in _order(events):
        k = (e.get("side", ""), e.get("stage", ""), e.get("persona", ""))
        a = agg.setdefault(k, {"events": 0, "status": ""})
        a["events"] += 1
        a["status"] = e.get("status", a["status"])
    out = [f"{'side':5}  {'stage':11}  {'persona':18}  {'events':>6}  last"]
    for (side, stage, persona), a in agg.items():
        out.append(f"{side:5}  {stage:11}  {persona:18}  {a['events']:>6}  {a['status']}")
    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("events", help="path to events.ndjson")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--tail", action="store_true", help="one line per event (default)")
    g.add_argument("--tree", action="store_true", help="grouped by stage -> persona")
    g.add_argument("--once", action="store_true", help="final per-persona summary")
    a = p.parse_args()
    events = _load(a.events)
    print(tree(events) if a.tree else once(events) if a.once else tail(events))


if __name__ == "__main__":
    main()
