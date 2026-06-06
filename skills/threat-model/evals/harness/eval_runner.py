#!/usr/bin/env python3
"""CLI for the threat-model skill eval + benchmark harness.

Deterministic parts (loading, validation, scoring, metrics, reporting, regression /
outgrowth) live here. The parts that need Claude — running the skill on a prompt
(Executor) and grading output against the rubric (Grader) — are agent-driven and
documented in harness/prompts/. This script consumes the JSON those agents produce.

Workflow:
  validate                          schema-check every case
  plan   --run <id> [--arm both]    emit runs/<id>/manifest.json + operator INSTRUCTIONS
  ingest --run <id>                 load + validate the grader result files
  report --run <id>                 score, aggregate, render runs/<id>/report.html
  compare --run <id> [--baseline baselines/current]   regression + outgrowth
  bless  --run <id>                 promote the run's skill arm to the baseline
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import metrics
import report

EVALS_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = EVALS_ROOT / "cases"
RUNS_DIR = EVALS_ROOT / "runs"
BASELINES_DIR = EVALS_ROOT / "baselines"

ARMS = ("skill", "baseline")
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL", "N/A"}
STRIDE = {"S", "T", "R", "I", "D", "E", "LM", "N/A"}


def _fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_cases() -> dict[str, dict]:
    cases: dict[str, dict] = {}
    for path in sorted(CASES_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        errs = validate_case(data, path.name)
        if errs:
            _fail(f"{path.name}:\n  - " + "\n  - ".join(errs))
        if data["id"] in cases:
            _fail(f"duplicate case id {data['id']!r}")
        cases[data["id"]] = data
    return cases


def validate_case(c: dict, where: str) -> list[str]:
    e: list[str] = []
    if not isinstance(c, dict):
        return [f"{where}: not a mapping"]
    for k in ("id", "title", "category", "trigger_phrase", "prompt", "expected", "rubric",
              "pass_threshold", "grounding"):
        if k not in c:
            e.append(f"missing key: {k}")
    if e:
        return e
    if c["category"] not in ("positive", "trigger-negative", "injection-resilience"):
        e.append(f"bad category: {c['category']}")
    if not 0 < c["pass_threshold"] <= 1:
        e.append("pass_threshold must be in (0, 1]")
    exp = c["expected"]
    for k in ("must_trigger", "dfd_layers", "stride_categories", "must_find_threats",
              "top_risk_candidates", "required_report_sections"):
        if k not in exp:
            e.append(f"expected.{k} missing")
    if e:
        return e
    for sc in exp["stride_categories"]:
        if sc not in STRIDE:
            e.append(f"bad stride category: {sc}")
    ids = set()
    for t in exp["must_find_threats"]:
        if t["min_severity"] not in SEVERITIES:
            e.append(f"must_find {t.get('id')}: bad severity {t.get('min_severity')}")
        if t["stride"] not in STRIDE:
            e.append(f"must_find {t.get('id')}: bad stride {t.get('stride')}")
        ids.add(t["id"])
    if exp["must_trigger"] and not c["rubric"]:
        e.append("positive/triggering case needs a non-empty rubric")
    for r in c["rubric"]:
        if not 1 <= r["weight"] <= 5:
            e.append(f"rubric {r.get('id')}: weight out of range")
    return e


def validate_result(r: dict, where: str) -> list[str]:
    e: list[str] = []
    for k in ("case_id", "arm", "triggered", "rubric_scores", "must_find_misses", "metrics"):
        if k not in r:
            e.append(f"{where}: missing {k}")
    if e:
        return e
    if r["arm"] not in ARMS:
        e.append(f"{where}: bad arm {r['arm']}")
    for rs in r["rubric_scores"]:
        if rs.get("verdict") not in ("pass", "partial", "fail"):
            e.append(f"{where}: rubric {rs.get('id')} bad verdict {rs.get('verdict')}")
    return e


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# -- commands ---------------------------------------------------------------

def cmd_validate(_args) -> None:
    cases = load_cases()
    print(f"ok: {len(cases)} case(s) valid")
    for cid, c in sorted(cases.items()):
        kind = "TRIGGER" if c["expected"]["must_trigger"] else "NO-TRIGGER"
        print(f"  {cid:28} {c['category']:20} {kind:11} rubric={len(c['rubric'])}")


def cmd_plan(args) -> None:
    cases = load_cases()
    arms = ARMS if args.arm == "both" else (args.arm,)
    run_dir = RUNS_DIR / args.run
    (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    (run_dir / "results").mkdir(parents=True, exist_ok=True)

    manifest = {"run": args.run, "created": _now(), "arms": list(arms), "tasks": []}
    for cid, c in sorted(cases.items()):
        for arm in arms:
            manifest["tasks"].append({
                "case_id": cid,
                "arm": arm,
                "prompt": c["prompt"],
                "output_path": f"outputs/{cid}.{arm}.md",
                "result_path": f"results/{cid}.{arm}.json",
            })
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    instr = _plan_instructions(args.run, list(arms), manifest["tasks"])
    (run_dir / "INSTRUCTIONS.md").write_text(instr)
    print(f"planned {len(manifest['tasks'])} task(s) -> {run_dir}")
    print(f"next: follow {run_dir / 'INSTRUCTIONS.md'} (Executor then Grader), then `ingest` and `report`.")


def _plan_instructions(run: str, arms: list[str], tasks: list[dict]) -> str:
    lines = [
        f"# Eval run `{run}`",
        "",
        "Two agent roles produce the JSON this harness consumes. Prompt templates are in",
        "`../../harness/prompts/`. Run each task in a **fresh context**.",
        "",
        "## 1. Executor",
        "For each task below, give the Executor the case `prompt`.",
        f"- arm `skill`: thread/session with the threat-model skill loaded.",
        f"- arm `baseline`: identical prompt with **no** skill loaded (the control).",
        "Save raw output to the task's `output_path`. Record wall-clock ms and token usage.",
        "",
        "## 2. Grader",
        "Give the Grader the case file (`cases/<id>.yaml`) and the Executor output. It returns",
        "one JSON object per task at `result_path`, matching `schema/result.schema.json`.",
        "",
        "## Tasks",
    ]
    for t in tasks:
        lines.append(f"- `{t['case_id']}` [{t['arm']}] -> output `{t['output_path']}`, result `{t['result_path']}`")
    lines.append("")
    lines.append("When all result files exist: `python3 harness/eval_runner.py ingest --run " + run + "`")
    return "\n".join(lines) + "\n"


def _load_run(run: str) -> tuple[dict, dict, dict[str, dict]]:
    """Return (manifest, cases, scored_by_case[cid][arm])."""
    run_dir = RUNS_DIR / run
    if not (run_dir / "manifest.json").exists():
        _fail(f"no manifest for run {run!r} — run `plan` first")
    manifest = json.loads((run_dir / "manifest.json").read_text())
    cases = load_cases()
    scored: dict[str, dict] = {}
    missing: list[str] = []
    for t in manifest["tasks"]:
        rp = run_dir / t["result_path"]
        if not rp.exists():
            missing.append(t["result_path"])
            continue
        result = json.loads(rp.read_text())
        errs = validate_result(result, t["result_path"])
        if errs:
            _fail("; ".join(errs))
        result.setdefault("arm", t["arm"])
        s = metrics.score_result(cases[t["case_id"]], result)
        scored.setdefault(t["case_id"], {})[t["arm"]] = s
    return manifest, cases, scored, missing


def cmd_ingest(args) -> None:
    manifest, _cases, scored, missing = _load_run(args.run)
    have = sum(len(v) for v in scored.values())
    print(f"ingested {have}/{len(manifest['tasks'])} result(s)")
    if missing:
        print("missing:")
        for m in missing:
            print(f"  - {m}")
        raise SystemExit(2)
    print("all results present and valid")


def _arm_scores(scored: dict[str, dict], arm: str) -> dict[str, dict]:
    return {cid: a[arm] for cid, a in scored.items() if arm in a}


def cmd_report(args) -> None:
    manifest, cases, scored, _missing = _load_run(args.run)
    arms = {arm: metrics.summarize_arm(list(_arm_scores(scored, arm).values())) for arm in manifest["arms"]}
    compare = _compare_data(args.run, scored) if args.with_compare else None
    out = (RUNS_DIR / args.run / "report.html")
    out.write_text(report.render(args.run, _now(), arms, cases, scored, compare))
    print(f"wrote {out}")
    for arm, s in arms.items():
        if s.get("n"):
            print(f"  {arm:9} pass {s['passed']}/{s['n']} ({s['pass_rate'] * 100:.0f}%)  mean score {s['mean_score']}")


def _compare_data(run: str, scored: dict[str, dict]) -> dict | None:
    base_file = BASELINES_DIR / "current" / "skill.json"
    skill_now = _arm_scores(scored, "skill")
    baseline_now = _arm_scores(scored, "baseline")
    out: dict = {"outgrowth": metrics.outgrowth(baseline_now)} if baseline_now else {}
    if base_file.exists():
        skill_baseline = json.loads(base_file.read_text())
        out["regression"] = metrics.regression(skill_now, skill_baseline)
    return out or None


def cmd_compare(args) -> None:
    _manifest, _cases, scored, _missing = _load_run(args.run)
    data = _compare_data(args.run, scored) or {}
    reg = data.get("regression", [])
    og = data.get("outgrowth", {})
    if reg:
        print(f"REGRESSION: {len(reg)} case(s) lost ground vs baseline")
        for r in reg:
            print(f"  {r['case_id']}: {r['baseline_score']} -> {r['current_score']}"
                  + ("  (pass lost)" if r["pass_lost"] else ""))
    else:
        print("no regression vs baseline")
    if og.get("pass_rate") is not None:
        print(f"OUTGROWTH: base model passes {og['pass_rate'] * 100:.0f}% of positive cases without the skill")
        if og["passing"]:
            print("  passing without skill: " + ", ".join(og["passing"]))


def cmd_bless(args) -> None:
    _manifest, _cases, scored, _missing = _load_run(args.run)
    skill_now = _arm_scores(scored, "skill")
    if not skill_now:
        _fail("run has no skill-arm results to bless")
    dest = BASELINES_DIR / "current"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "skill.json").write_text(json.dumps(skill_now, indent=2))
    (dest / "meta.json").write_text(json.dumps({"from_run": args.run, "blessed": _now()}, indent=2))
    print(f"blessed run {args.run!r} skill arm -> {dest} ({len(skill_now)} case(s))")


def main() -> None:
    p = argparse.ArgumentParser(prog="eval_runner", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(func=cmd_validate)

    pp = sub.add_parser("plan")
    pp.add_argument("--run", required=True)
    pp.add_argument("--arm", choices=["both", "skill", "baseline"], default="both")
    pp.set_defaults(func=cmd_plan)

    pi = sub.add_parser("ingest")
    pi.add_argument("--run", required=True)
    pi.set_defaults(func=cmd_ingest)

    pr = sub.add_parser("report")
    pr.add_argument("--run", required=True)
    pr.add_argument("--with-compare", action="store_true", help="include regression/outgrowth banner")
    pr.set_defaults(func=cmd_report)

    pc = sub.add_parser("compare")
    pc.add_argument("--run", required=True)
    pc.add_argument("--baseline", default=str(BASELINES_DIR / "current"))
    pc.set_defaults(func=cmd_compare)

    pb = sub.add_parser("bless")
    pb.add_argument("--run", required=True)
    pb.set_defaults(func=cmd_bless)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
