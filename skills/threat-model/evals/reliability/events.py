"""Run-event stream (`tm.run-event/1`) for pipeline observability.

A persona emits a `start` when it begins and a `done` when its output lands. The payload is a
projection of what already goes into that persona's Execution Log — this module only serializes it.
It performs no analysis. `from_transcripts` derives the same stream from a completed workflow run's
agent transcripts, so observability works over the runs the harness actually performs.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "tm.run-event/1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(stream_path: str | Path, *, run_id: str, stage: str, persona: str, status: str,
         side: str = "", action: str = "", metrics: dict | None = None, note: str = "",
         seq: int | None = None, ts: str | None = None) -> dict[str, Any]:
    """Append one event. status in {start, done, error}. Caller reports; this does not analyze."""
    rec = {"schema": SCHEMA, "ts": ts or _now(), "run_id": run_id, "seq": seq, "side": side,
           "stage": stage, "persona": persona, "action": action, "status": status,
           "metrics": metrics or {}, "note": note}
    with open(stream_path, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


# -- derive events from a completed workflow run's transcripts ---------------

# prompt-file -> (persona, stage, side)
_ROLES = [
    ("executor.md", ("executor", "execute", "eval")),
    ("quality-judge.md", ("quality-judge", "judge", "eval")),
    ("recon-auditor.md", ("recon-auditor", "judge", "eval")),
    ("red-team.md", ("red-team", "judge", "eval")),
    ("gap-validator.md", ("gap-validator", "judge", "eval")),
    ("diagram-judge.md", ("diagram-judge", "judge", "eval")),
    ("stability-matcher.md", ("stability-matcher", "match", "eval")),
]


def _first_user(lines: list[dict]) -> str:
    for l in lines:
        m = l.get("message", {}) or {}
        if l.get("type") == "user" or m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, list):
                c = " ".join(str(x.get("text", "")) if isinstance(x, dict) else str(x) for x in c)
            return str(c)
    return ""


def _classify(text: str) -> tuple[str, str, str, str]:
    persona, stage, side = "agent", "run", "eval"
    for marker, (p, st, sd) in _ROLES:
        if marker in text:
            persona, stage, side = p, st, sd
            break
    m = re.search(r"\{out_dir\}=\S*?/(run\d+)|run_dir\}=\S*?/(run\d+)|/(run\d+)\b", text)
    action = next((g for g in (m.groups() if m else []) if g), "")
    tgt = re.search(r"/eval_targets/(\w+)", text)
    if tgt and not action:
        action = tgt.group(1)
    return persona, stage, side, action


def from_transcripts(transcript_dir: str | Path, run_id: str) -> list[dict[str, Any]]:
    """Build start/done events from agent-*.jsonl files (real timestamps)."""
    events: list[dict[str, Any]] = []
    for f in sorted(Path(transcript_dir).glob("agent-*.jsonl")):
        lines = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        ts = [l["timestamp"] for l in lines if l.get("timestamp")]
        if not ts:
            continue
        persona, stage, side, action = _classify(_first_user(lines))
        a, b = ts[0], ts[-1]
        elapsed = None
        try:
            elapsed = int((datetime.fromisoformat(b.replace("Z", "+00:00"))
                           - datetime.fromisoformat(a.replace("Z", "+00:00"))).total_seconds() * 1000)
        except ValueError:
            pass
        common = {"schema": SCHEMA, "run_id": run_id, "side": side, "stage": stage,
                  "persona": persona, "action": action, "note": ""}
        events.append({**common, "ts": a, "status": "start", "metrics": {}})
        events.append({**common, "ts": b, "status": "done", "metrics": {"elapsed_ms": elapsed}})
    events.sort(key=lambda e: e["ts"])
    for i, e in enumerate(events):
        e["seq"] = i
    return events


def write(stream_path: str | Path, events: list[dict]) -> None:
    Path(stream_path).write_text("".join(json.dumps(e) + "\n" for e in events))


if __name__ == "__main__":
    import sys
    evs = from_transcripts(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "run")
    write(sys.argv[3] if len(sys.argv) > 3 else "events.ndjson", evs)
    print(f"wrote {len(evs)} events")
