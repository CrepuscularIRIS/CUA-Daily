#!/usr/bin/env python3
"""Minimal fixtures for the v2.2 mechanical checks (run: python3 research/v2/test_check_tools.py)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_calc import compute  # noqa: E402


def base_record(seat: str, key: str = "2501.00001", **over) -> dict:
    r = {
        "schema_version": "radar-review-v2.2", "run_id": "t", "batch_id": "t",
        "attempt_id": "a1", "seat": seat,
        "paper": {"paper_key": key, "claim_type": "system_method"},
        "provenance": {}, "materials": [],
        "rs_pattern": {"primary": "reframe_as_solvable_object", "supporting": [],
                       "matches": [{"main_id": "reframe_as_solvable_object", "sub_id": "C00",
                                    "role": "primary", "fit": "good"}],
                       "outside_taxonomy": False},
        "domain_pattern": {"namespace": "gui", "matches": []},
        "assessment": {"evidence_level": "online", "claim_support": "scoped"},
        "ratings": {k: {"status": "resolved", "rating": 2, "reason": "x"}
                    for k in ("G", "M", "X")},
        "status": "reviewed",
    }
    r["score"] = compute(r)
    r["ratings"]["E"] = {k: {"status": "resolved", "rating": 2, "reason": "x"}
                         for k in ("measurement", "causality", "holdout", "statistics", "cost")}
    for k, v in over.items():
        r[k] = v
    return r


def make_batch(tmp: Path, sol_recs, son_recs) -> Path:
    bdir = tmp / "runs" / "t" / "batches" / "t"
    for seat, recs in (("sol", sol_recs), ("son55", son_recs)):
        d = bdir / "seats" / seat / "attempts" / "a1"
        d.mkdir(parents=True, exist_ok=True)
        for r in recs:
            (d / f"{r['paper']['paper_key']}.json").write_text(json.dumps(r))
    (bdir / "manifest.json").write_text(json.dumps(
        {"papers": [{"paper_key": p} for p in sorted(
            {r["paper"]["paper_key"] for r in sol_recs} | {r["paper"]["paper_key"] for r in son_recs})]}))
    return bdir


def main() -> None:
    ok = [base_record("sol"), base_record("son55")]
    # 1. score arithmetic: all-2 ratings -> 50.0
    sc = compute(ok[0])
    assert sc["raw"] == 50.0 and sc["coverage"] == 1.0, sc
    # 2. unknown -> null score, L=0-based, coverage drops
    rec = base_record("sol")
    rec["ratings"]["G"] = {"status": "unknown", "rating": None, "reason": "x"}
    sc2 = compute(rec)
    assert sc2["raw"] is None and sc2["lower"] == 42.5 and sc2["upper"] == 57.5, sc2
    assert abs(sc2["coverage"] - 0.85) < 1e-9, sc2
    # 3. not_reported counts as 0 but judged
    rec3 = base_record("sol")
    rec3["ratings"]["E"]["cost"] = {"status": "not_reported", "rating": 0,
                                    "reason": "x", "search_scope": ["appendix"]}
    sc3 = compute(rec3)
    assert sc3["raw"] == 47.5 and sc3["coverage"] == 1.0, sc3
    # 4. wrong parent card is flagged
    rec4 = base_record("sol")
    rec4["rs_pattern"]["matches"][0]["sub_id"] = "C21"  # parent is reframe..., ok
    rec5 = base_record("sol")
    rec5["rs_pattern"]["matches"][0] = {"main_id": "decompose_and_delegate", "sub_id": "C00"}
    errs = []
    import check_batch as cb
    cb.check_record(rec5, "x", errs)
    assert any("not under parent" in e for e in errs), errs
    # 5. unknown with rating is flagged; out-of-range rating flagged
    rec6 = base_record("sol")
    rec6["ratings"]["M"] = {"status": "unknown", "rating": 3, "reason": "x"}
    errs = []
    cb.check_record(rec6, "x", errs)
    assert any("unknown but rating" in e for e in errs), errs
    rec7 = base_record("sol")
    rec7["ratings"]["M"] = {"status": "resolved", "rating": 5, "reason": "x"}
    errs = []
    cb.check_record(rec7, "x", errs)
    assert any("not int 0..4" in e for e in errs), errs
    # 6. coverage diff: missing paper in one seat
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        make_batch(tmp, [base_record("sol")], [base_record("son55"), base_record("son55", "2501.00002")])
        rc = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "check_batch.py"), "t", "t"],
            capture_output=True, text=True, env={**__import__("os").environ, "CUA_RADAR_RUNS": str(tmp / "runs")})
        assert rc.returncode == 1 and "missing papers" in rc.stdout, (rc.returncode, rc.stdout, rc.stderr)
        conf = json.loads((tmp / "runs/t/batches/t/conflicts.json").read_text())
        assert conf["n_conflict_papers"] == 0
    # 7. rating diff produces a conflict entry
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        s = base_record("sol"); s["ratings"]["G"]["rating"] = 3
        n = base_record("son55")
        make_batch(tmp, [s], [n])
        rc = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "check_batch.py"), "t", "t"],
            capture_output=True, text=True, env={**__import__("os").environ, "CUA_RADAR_RUNS": str(tmp / "runs")})
        conf = json.loads((tmp / "runs/t/batches/t/conflicts.json").read_text())
        assert rc.returncode == 0, (rc.stdout, rc.stderr)
        assert conf["n_conflict_papers"] == 1 and conf["conflicts"]["2501.00001"][0]["field"] == "rating.G"
    print("all fixture checks passed")


if __name__ == "__main__":
    main()
