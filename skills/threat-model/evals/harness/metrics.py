"""Deterministic scoring and aggregation for threat-model evals.

The grader agent returns per-rubric verdicts and must-find hits/misses. The harness
owns the arithmetic so the pass/fail signal never depends on a model doing math.
"""
from __future__ import annotations

from statistics import mean
from typing import Any

VERDICT_FRACTION = {"pass": 1.0, "partial": 0.5, "fail": 0.0}


def weighted_score(case: dict[str, Any], result: dict[str, Any]) -> float:
    """Fraction of rubric weight earned, recomputed from verdicts (grader math ignored)."""
    weights = {r["id"]: r["weight"] for r in case["rubric"]}
    earned = 0.0
    total = 0.0
    for rs in result.get("rubric_scores", []):
        w = weights.get(rs["id"])
        if w is None:
            continue
        earned += w * VERDICT_FRACTION.get(rs["verdict"], 0.0)
        total += w
    return earned / total if total else 0.0


def missed_critical(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    sev = {t["id"]: t["min_severity"] for t in case["expected"]["must_find_threats"]}
    return [mid for mid in result.get("must_find_misses", []) if sev.get(mid) == "CRITICAL"]


def passed(case: dict[str, Any], result: dict[str, Any]) -> bool:
    if result.get("triggered") != case["expected"]["must_trigger"]:
        return False
    if missed_critical(case, result):
        return False
    return weighted_score(case, result) >= case["pass_threshold"]


def score_result(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    s = weighted_score(case, result)
    return {
        "case_id": case["id"],
        "arm": result["arm"],
        "is_positive": case["expected"]["must_trigger"],
        "triggered": result.get("triggered"),
        "trigger_ok": result.get("triggered") == case["expected"]["must_trigger"],
        "weighted_score": round(s, 4),
        "passed": passed(case, result),
        "must_find_misses": result.get("must_find_misses", []),
        "missed_critical": missed_critical(case, result),
        "metrics": result.get("metrics", {}),
        "rubric_scores": result.get("rubric_scores", []),
        "summary": result.get("summary", ""),
    }


def _safe_mean(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None]
    return round(mean(vals), 1) if vals else None


def summarize_arm(scored: list[dict[str, Any]]) -> dict[str, Any]:
    if not scored:
        return {"n": 0}
    n = len(scored)
    npass = sum(1 for s in scored if s["passed"])
    return {
        "n": n,
        "passed": npass,
        "pass_rate": round(npass / n, 4),
        "mean_score": round(mean(s["weighted_score"] for s in scored), 4),
        "mean_elapsed_ms": _safe_mean([s["metrics"].get("elapsed_ms") for s in scored]),
        "mean_tokens_in": _safe_mean([s["metrics"].get("tokens_in") for s in scored]),
        "mean_tokens_out": _safe_mean([s["metrics"].get("tokens_out") for s in scored]),
    }


def regression(skill_now: dict[str, dict], skill_baseline: dict[str, dict], eps: float = 0.05) -> list[dict]:
    """Cases where the current skill arm lost ground vs the blessed baseline.

    Signals 'the model changed — improve the skill' per the Skills 2.0 spec.
    """
    out = []
    for cid, now in skill_now.items():
        base = skill_baseline.get(cid)
        if not base:
            continue
        regressed_pass = base["passed"] and not now["passed"]
        regressed_score = now["weighted_score"] < base["weighted_score"] - eps
        if regressed_pass or regressed_score:
            out.append({
                "case_id": cid,
                "baseline_score": base["weighted_score"],
                "current_score": now["weighted_score"],
                "pass_lost": regressed_pass,
            })
    return out


def outgrowth(baseline_arm_now: dict[str, dict]) -> dict[str, Any]:
    """How many cases the base model passes WITHOUT the skill loaded.

    A high pass rate here signals the model outgrew the skill (consider retiring it).
    """
    positive = {cid: s for cid, s in baseline_arm_now.items() if s["is_positive"]}
    if not positive:
        return {"passing": [], "pass_rate": None}
    passing = [cid for cid, s in positive.items() if s["passed"]]
    return {"passing": passing, "pass_rate": round(len(passing) / len(positive), 4)}
