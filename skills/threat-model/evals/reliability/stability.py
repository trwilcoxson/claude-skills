"""Cross-run stability: does the system reliably surface the same high-severity core
when pointed at the same target N times?

Findings are matched across runs by approximate semantic key (normalized names of the
recon entities a finding references, plus its STRIDE-LM categories) because TM-NNN
numbering and wording vary run to run. This is a stability indicator, not exact identity.
"""
from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path

HIGH = {"HIGH", "CRITICAL"}


def _norm_tokens(text: str) -> set[str]:
    toks = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"the", "a", "an", "service", "svc", "of", "to", "and", "app", "aws", "data"}
    return {t for t in toks if t not in stop and len(t) > 2}


def _core(run_dir: Path) -> list[dict]:
    recon = json.loads((run_dir / "recon.json").read_text())
    findings = json.loads((run_dir / "findings.json").read_text())["findings"]
    names = {}
    for bucket in ["components", "data_stores", "entry_points", "trust_boundaries", "external_deps"]:
        for el in recon.get(bucket, []):
            names[el["id"]] = el["name"]
    out = []
    for f in findings:
        if f.get("severity") not in HIGH:
            continue
        refs = f.get("asset_refs", []) + f.get("surface_refs", [])
        key = set()
        for r in refs:
            key |= _norm_tokens(names.get(r, r))
        key |= _norm_tokens(f.get("title", ""))
        out.append({"id": f["id"], "key": key, "stride": set(f.get("stride_lm", [])),
                    "cwe": set(f.get("cwe", [])), "severity": f["severity"], "title": f.get("title", "")})
    return out


def _match(a: dict, b: dict) -> bool:
    if not (a["stride"] & b["stride"]):
        return False
    inter = len(a["key"] & b["key"])
    union = len(a["key"] | b["key"]) or 1
    # Conservative deterministic fallback. Matching free-text findings across runs is a semantic
    # task (token-only under-merges reworded duplicates; CWE-chaining over-merges via shared CWEs),
    # so the harness prefers the LLM stability-matcher (prompts/stability-matcher.md) when present
    # and uses this only as a cheap floor. It under-reports stability — treat as a lower bound.
    return inter / union >= 0.34


def core_findings(run_dirs: list[Path]) -> list[dict]:
    """HIGH+ findings per run, flattened for an LLM matcher (run index, id, title, cwe, assets)."""
    out = []
    for ri, rd in enumerate(run_dirs):
        recon = json.loads((rd / "recon.json").read_text())
        names = {}
        for bucket in ["components", "data_stores", "entry_points", "trust_boundaries", "external_deps"]:
            for el in recon.get(bucket, []):
                names[el["id"]] = el["name"]
        for f in json.loads((rd / "findings.json").read_text())["findings"]:
            if f.get("severity") not in HIGH:
                continue
            refs = f.get("asset_refs", []) + f.get("surface_refs", [])
            out.append({"run": ri + 1, "id": f["id"], "title": f.get("title", ""),
                        "severity": f["severity"], "cwe": f.get("cwe", []),
                        "assets": [names.get(r, r) for r in refs]})
    return out


def from_clusters(clusters: list[dict], n_runs: int, core_sizes: list[int]) -> dict:
    """Build the report stability shape from an LLM matcher's cross-run clusters.

    Each cluster: {label, severity, runs: [run ints it appears in]}.
    """
    total = len(clusters)
    stable = [c for c in clusters if len(set(c["runs"])) == n_runs]
    run_sets = [set() for _ in range(n_runs)]
    for ci, c in enumerate(clusters):
        for r in set(c["runs"]):
            if 1 <= r <= n_runs:
                run_sets[r - 1].add(ci)
    jac = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            a, b = run_sets[i], run_sets[j]
            jac.append(len(a & b) / (len(a | b) or 1))
    return {
        "n_runs": n_runs,
        "core_sizes": core_sizes,
        "total_distinct_core": total,
        "stable_core_count": len(stable),
        "stable_core_ratio": round(len(stable) / total, 3) if total else None,
        "mean_pairwise_jaccard": round(sum(jac) / len(jac), 3) if jac else None,
        "matcher": "llm",
        "stable_core": [{"title": c["label"], "severity": c["severity"]} for c in stable],
        "unstable": [{"title": c["label"], "severity": c["severity"], "in_runs": len(set(c["runs"]))}
                     for c in clusters if len(set(c["runs"])) < n_runs],
    }


def analyze(run_dirs: list[Path]) -> dict:
    cores = [_core(rd) for rd in run_dirs]
    n = len(cores)
    # cluster findings across runs by connected components over pairwise matches
    nodes = [(ri, fi, f) for ri, core in enumerate(cores) for fi, f in enumerate(core)]
    parent = {(ri, fi): (ri, fi) for ri, fi, _ in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for (ri, fi, fa), (rj, fj, fb) in combinations(nodes, 2):
        if ri != rj and _match(fa, fb):
            union((ri, fi), (rj, fj))

    clusters: dict = {}
    for ri, fi, f in nodes:
        clusters.setdefault(find((ri, fi)), []).append((ri, f))
    cluster_list = []
    for members in clusters.values():
        runs_present = {ri for ri, _ in members}
        cluster_list.append({
            "runs_present": sorted(runs_present),
            "n_runs": len(runs_present),
            "title": members[0][1]["title"],
            "severity": members[0][1]["severity"],
        })
    stable = [c for c in cluster_list if c["n_runs"] == n]

    # pairwise jaccard on cluster membership between runs
    run_sets = [set() for _ in range(n)]
    for ci, members in enumerate(clusters.values()):
        for ri, _ in members:
            run_sets[ri].add(id(members))
    # recompute membership cleanly by cluster index
    run_cluster_ids = [set() for _ in range(n)]
    for idx, members in enumerate(clusters.values()):
        for ri, _ in members:
            run_cluster_ids[ri].add(idx)
    jac = []
    for i, j in combinations(range(n), 2):
        a, b = run_cluster_ids[i], run_cluster_ids[j]
        jac.append(len(a & b) / (len(a | b) or 1))
    mean_jac = round(sum(jac) / len(jac), 3) if jac else None

    return {
        "n_runs": n,
        "core_sizes": [len(c) for c in cores],
        "total_distinct_core": len(cluster_list),
        "stable_core_count": len(stable),
        "stable_core_ratio": round(len(stable) / len(cluster_list), 3) if cluster_list else None,
        "mean_pairwise_jaccard": mean_jac,
        "stable_core": [{"title": c["title"], "severity": c["severity"]} for c in stable],
        "unstable": [{"title": c["title"], "severity": c["severity"], "in_runs": c["n_runs"]}
                     for c in cluster_list if c["n_runs"] < n],
    }
