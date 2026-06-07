#!/usr/bin/env python3
"""Reference-free reliability harness CLI.

There is no per-target answer key. A target is just a real system you point at
(targets/<id>.yaml = id + source + local repo path). The system is run N times;
this scores each run's manifests against checks derived from the target itself,
folds in the agent-judged layers (quality, adversarial recall, recon completeness),
measures cross-run stability, and renders one reliability report.

  check  --run <dir> --repo <path>                 deterministic checks on one run
  report --runs-root <dir> --repo <path> ...        score all runs + agents + stability -> HTML
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import checks
import report as report_mod
import stability as stability_mod

HERE = Path(__file__).resolve().parent


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _run_dirs(root: Path) -> list[Path]:
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "findings.json").exists())


def cmd_check(a) -> None:
    res = checks.run_checks(Path(a.run), Path(a.repo))
    (Path(a.run) / "scored.json").write_text(json.dumps(res, indent=2))
    s = res["scores"]
    print(f"structure={'pass' if s['structure_pass'] else 'FAIL'} "
          f"consistency={'pass' if s['consistency_pass'] else 'FAIL'} "
          f"grounding={s['grounding']} coverage={s['coverage']} defects={len(res['defects'])}")
    for d in res["defects"]:
        print(f"  [{d['layer']}] {d['code']}: {d['detail']}")


def _load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def cmd_report(a) -> None:
    repo = Path(a.repo)
    rdirs = _run_dirs(Path(a.runs_root))
    if not rdirs:
        raise SystemExit(f"no run dirs with findings.json under {a.runs_root}")
    runs = [checks.run_checks(rd, repo) for rd in rdirs]
    for rd, r in zip(rdirs, runs):
        (rd / "scored.json").write_text(json.dumps(r, indent=2))

    agents_dir = Path(a.agents) if a.agents else Path(a.runs_root) / "agents"
    agents = {
        "quality": _load(agents_dir / "quality.json"),
        "recall": _load(agents_dir / "recall.json"),
        "recon_audit": _load(agents_dir / "recon-audit.json"),
    }
    stab = None
    if len(rdirs) > 1:
        clusters_file = agents_dir / "stability-clusters.json"
        if clusters_file.exists():
            clusters = json.loads(clusters_file.read_text())["clusters"]
            core = stability_mod.core_findings(rdirs)
            sizes = [sum(1 for c in core if c["run"] == i + 1) for i in range(len(rdirs))]
            stab = stability_mod.from_clusters(clusters, len(rdirs), sizes)
        else:
            stab = stability_mod.analyze(rdirs)  # heuristic fallback (under-reports)
    target = {"id": a.target, "source": a.source}
    out = Path(a.out)
    out.write_text(report_mod.render(target, runs, agents, stab, _now()))
    print(f"wrote {out}")
    for i, r in enumerate(runs):
        s = r["scores"]
        print(f"  run {i+1}: structure={'pass' if s['structure_pass'] else 'FAIL'} "
              f"consistency={'pass' if s['consistency_pass'] else 'FAIL'} "
              f"grounding={s['grounding']} coverage={s['coverage']} defects={len(r['defects'])}")
    if stab:
        print(f"  stability: stable core {stab['stable_core_count']}/{stab['total_distinct_core']} "
              f"(jaccard {stab['mean_pairwise_jaccard']})")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("check"); pc.add_argument("--run", required=True); pc.add_argument("--repo", required=True)
    pc.set_defaults(func=cmd_check)
    pr = sub.add_parser("report")
    pr.add_argument("--runs-root", required=True); pr.add_argument("--repo", required=True)
    pr.add_argument("--target", required=True); pr.add_argument("--source", default="")
    pr.add_argument("--agents", default=None); pr.add_argument("--out", default="reliability.html")
    pr.set_defaults(func=cmd_report)
    a = p.parse_args(); a.func(a)


if __name__ == "__main__":
    main()
