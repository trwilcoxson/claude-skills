"""Reference-free deterministic checks over one threat-model run.

Everything here is derived from (target repo, emitted manifests) — there is no
per-target answer key. A check either passes for any well-formed, faithful threat
model or it flags a concrete defect.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import diagram_checks

STRIDE_LM = {"S", "T", "R", "I", "D", "E", "LM"}
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# Report-template sections expected in any complete model (matched loosely on heading text).
REPORT_SECTIONS = ["executive summary", "system overview", "architecture", "findings", "remediation"]


def band(score: int) -> str:
    if score <= 4:
        return "LOW"
    if score <= 9:
        return "MEDIUM"
    if score <= 16:
        return "HIGH"
    return "CRITICAL"


class Defects:
    def __init__(self) -> None:
        self.items: list[dict[str, str]] = []

    def add(self, layer: str, code: str, detail: str) -> None:
        self.items.append({"layer": layer, "code": code, "detail": detail})

    def by_layer(self, layer: str) -> list[dict]:
        return [d for d in self.items if d["layer"] == layer]


def _load_json(path: Path, d: Defects, label: str):
    if not path.exists():
        d.add("structure", "missing-artifact", f"{label} not produced ({path.name})")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        d.add("structure", "invalid-json", f"{label} is not valid JSON: {e}")
        return None


def _require(obj: dict, keys: list[str], d: Defects, where: str) -> bool:
    ok = True
    for k in keys:
        if k not in obj:
            d.add("structure", "missing-field", f"{where}: missing '{k}'")
            ok = False
    return ok


# -- grounding against the real repo ----------------------------------------

def _resolves_in_repo(repo: Path, evidence: str) -> bool:
    ev = evidence.strip()
    # 1. direct path or glob
    if (repo / ev).exists():
        return True
    try:
        if any(repo.glob(ev)):
            return True
    except (ValueError, OSError):
        pass
    # 2. literal string present somewhere in the tree (cheap grep, skip .git)
    try:
        r = subprocess.run(
            ["grep", "-rqIF", "--exclude-dir=.git", ev, str(repo)],
            capture_output=True, timeout=20,
        )
        if r.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass
    # 3. basename of a path-looking evidence string
    base = ev.split("/")[-1]
    if base and base != ev:
        try:
            if any(repo.rglob(base)):
                return True
        except (ValueError, OSError):
            pass
    return False


def run_checks(run_dir: Path, repo: Path) -> dict[str, Any]:
    d = Defects()
    recon = _load_json(run_dir / "recon.json", d, "recon manifest")
    findings_doc = _load_json(run_dir / "findings.json", d, "findings manifest")
    report = run_dir / "report.md"

    # ---- structure: report.md present + has the expected sections
    raw_report = ""
    if not report.exists() or report.stat().st_size < 500:
        d.add("structure", "missing-report", "report.md absent or trivially short")
        report_text = ""
    else:
        raw_report = report.read_text()
        report_text = raw_report.lower()
        for sec in REPORT_SECTIONS:
            if sec not in report_text:
                d.add("structure", "missing-section", f"report.md has no '{sec}' section")

    surface_ids: set[str] = set()
    recon_ids: set[str] = set()
    grounded = ungrounded = 0
    if recon and _require(recon, ["components", "data_stores", "entry_points", "trust_boundaries", "external_deps"], d, "recon"):
        for bucket in ["components", "data_stores", "entry_points", "trust_boundaries", "external_deps"]:
            for el in recon.get(bucket, []):
                if not _require(el, ["id", "name", "evidence"], d, f"recon.{bucket}"):
                    continue
                recon_ids.add(el["id"])
                if bucket in ("entry_points", "data_stores", "trust_boundaries"):
                    surface_ids.add(el["id"])
                # grounding: at least one evidence string must resolve in the repo
                evs = el["evidence"] if isinstance(el["evidence"], list) else [el["evidence"]]
                if any(_resolves_in_repo(repo, e) for e in evs):
                    grounded += 1
                else:
                    ungrounded += 1
                    d.add("grounding", "ungrounded-element",
                          f"recon {el['id']} '{el['name']}' — no evidence resolves in repo: {evs}")

    # ---- findings: consistency + grounding refs
    covered: set[str] = set()
    counts = {s: 0 for s in SEVERITIES}
    n_findings = 0
    cwe_total = mitre_total = 0
    if findings_doc and _require(findings_doc, ["findings", "summary_counts", "no_issue_surface"], d, "findings"):
        for f in findings_doc["findings"]:
            n_findings += 1
            fid = f.get("id", "?")
            if not _require(f, ["id", "stride_lm", "likelihood", "impact", "severity", "asset_refs", "surface_refs"], d, fid):
                continue
            # value domains
            for cat in f["stride_lm"]:
                if cat not in STRIDE_LM:
                    d.add("structure", "bad-stride-lm", f"{fid}: '{cat}' not a STRIDE-LM category")
            if f["severity"] in SEVERITIES:
                counts[f["severity"]] += 1
            else:
                d.add("structure", "bad-severity", f"{fid}: severity '{f['severity']}'")
            # consistency: severity must equal band(L x I)
            try:
                expect = band(int(f["likelihood"]) * int(f["impact"]))
                if f["severity"] != expect:
                    d.add("consistency", "severity-formula",
                          f"{fid}: severity {f['severity']} != band(L{f['likelihood']} x I{f['impact']})={expect}")
            except (ValueError, TypeError):
                d.add("structure", "bad-LxI", f"{fid}: non-integer likelihood/impact")
            # grounding: refs must resolve to recon ids
            for ref in f.get("asset_refs", []) + f.get("surface_refs", []):
                if recon_ids and ref not in recon_ids:
                    d.add("grounding", "dangling-ref", f"{fid}: ref '{ref}' not in recon manifest")
            covered.update(s for s in f.get("surface_refs", []) if s in surface_ids)
            covered.update(a for a in f.get("asset_refs", []) if a in surface_ids)
            # id well-formedness (fabrication is only partially checkable offline)
            for c in f.get("cwe", []):
                cwe_total += 1
                if not re.fullmatch(r"CWE-\d+", c):
                    d.add("consistency", "malformed-cwe", f"{fid}: '{c}'")
            for m in f.get("mitre", []):
                mitre_total += 1
                if not re.fullmatch(r"T\d{4}(\.\d{3})?", m):
                    d.add("consistency", "malformed-mitre", f"{fid}: '{m}'")

        # summary counts must match reality
        for s in SEVERITIES:
            declared = findings_doc["summary_counts"].get(s)
            if declared != counts[s]:
                d.add("consistency", "count-mismatch", f"summary_counts.{s}={declared} but {counts[s]} findings present")

        # cross-artifact: report.md TM-NNN count vs manifest
        if report_text:
            report_tm = len(set(re.findall(r"tm-\d{3}", report_text)))
            if report_tm and abs(report_tm - n_findings) > 1:
                d.add("consistency", "report-manifest-drift",
                      f"report.md references {report_tm} TM ids but findings.json has {n_findings}")

        # coverage: every surface element examined (a finding, or explicitly no-issue)
        no_issue = set(findings_doc.get("no_issue_surface", []))
        uncovered = surface_ids - covered - no_issue
        for s in sorted(uncovered):
            d.add("coverage", "uncovered-surface", f"surface '{s}' has no finding and is not marked no-issue")

    # diagram verification (its own defect layer)
    diag = diagram_checks.check(raw_report, recon, findings_doc)
    d.items.extend(diag["defects"])

    scores = _scores(d, grounded, ungrounded, surface_ids, covered, findings_doc)
    scores.update(diag["scores"])
    return {
        "defects": d.items,
        "stats": {
            "findings": n_findings,
            "counts": counts,
            "recon_elements": len(recon_ids),
            "surface_elements": len(surface_ids),
            "surface_covered": len(covered),
            "grounded": grounded,
            "ungrounded": ungrounded,
            "cwe_ids": cwe_total,
            "mitre_ids": mitre_total,
            "diagram": diag["stats"],
        },
        "scores": scores,
    }


def _scores(d: Defects, grounded: int, ungrounded: int, surface_ids: set, covered: set, findings_doc) -> dict:
    structure_ok = not d.by_layer("structure")
    consistency_ok = not d.by_layer("consistency")
    g_total = grounded + ungrounded
    grounding = round(grounded / g_total, 3) if g_total else None
    no_issue = set(findings_doc.get("no_issue_surface", [])) if findings_doc else set()
    examined = len((covered | no_issue) & surface_ids)
    coverage = round(examined / len(surface_ids), 3) if surface_ids else None
    return {
        "structure_pass": structure_ok,
        "consistency_pass": consistency_ok,
        "grounding": grounding,
        "coverage": coverage,
    }


if __name__ == "__main__":
    import sys
    out = run_checks(Path(sys.argv[1]), Path(sys.argv[2]))
    print(json.dumps(out, indent=2))
