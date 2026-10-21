"""Offline test of research/merge_judgments.py on temp trees. Run: python3 test_merge_judgments.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
AID = "2501.00001"
TEXT = "We evaluate on OSWorld with a success rate of 34.5 percent. Baselines are matched in size."

SOL_REC = {"arxiv": AID, "version_read": "v1", "title_zh": "t", "one_line": "a paper", "one_line_zh": "一篇",
           "evidence": {"online_eval": {"value": "yes", "quote": "NOT IN TEXT success rate"},
                        "variance": {"value": "no", "quote": ""}},
           "evidence_level": {"value": "online", "quote": "We evaluate on OSWorld"},
           "success": {"S1": {"value": "yes", "quote": "success rate of 34.5"}, "S2": {"value": "no", "quote": ""}},
           "failure": {"F1": {"value": "no", "quote": ""}},
           "anti": {"AP1": {"value": "no", "mitigated": "unclear", "quote": ""},
                    "AP2": {"value": "yes", "mitigated": "yes", "quote": "Baselines are matched"}}}
SON_REC = {"arxiv": AID, "version_read": "v2", "title_zh": "t2", "one_line": "another paper", "one_line_zh": "两篇",
           "evidence": {"online_eval": {"value": "yes", "quote": "success rate of 34.5"},
                        "variance": {"value": "no", "quote": ""}},
           "evidence_level": {"value": "online", "quote": "We evaluate on OSWorld"},
           "success": {"S1": {"value": "no", "quote": ""}, "S2": {"value": "no", "quote": ""}},
           "failure": {"F1": {"value": "no", "quote": ""}},
           "anti": {"AP1": {"value": "no", "mitigated": "no", "quote": ""},
                    "AP2": {"value": "no", "mitigated": "unclear", "quote": ""}}}
SOL_ASG = {"arxiv": AID, "sub_pattern": "K01", "fit": "good", "fit_note": "fits"}
SON_ASG = {"arxiv": AID, "sub_pattern": "K02", "fit": "good", "fit_note": "other"}


def tree(sol_asg=SOL_ASG, son_asg=SON_ASG, published=None) -> Path:
    td = tempfile.mkdtemp()
    root = Path(td) / "research"
    (root / "fulltext").mkdir(parents=True)
    (root / "fulltext" / f"{AID}.txt").write_text(TEXT, encoding="utf-8")
    jp, ap = root / "judgments" / "passes", root / "patterns" / "assign_passes"
    jp.mkdir(parents=True); ap.mkdir(parents=True)
    jp.joinpath("bT.sol.jsonl").write_text(json.dumps(SOL_REC) + "\n", encoding="utf-8")
    jp.joinpath("bT.son55.jsonl").write_text(json.dumps(SON_REC) + "\n", encoding="utf-8")
    ap.joinpath("assign_bT.sol.jsonl").write_text(json.dumps(sol_asg) + "\n", encoding="utf-8")
    ap.joinpath("assign_bT.son55.jsonl").write_text(json.dumps(son_asg) + "\n", encoding="utf-8")
    if published is not None:
        (root / "patterns").mkdir(parents=True, exist_ok=True)
        (root / "patterns" / "assignments.jsonl").write_text(json.dumps(published) + "\n", encoding="utf-8")
    return root


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(REPO / "research/merge_judgments.py"), "bT",
                           "--root", str(root), *args], capture_output=True, text=True)


def jl1(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> None:
    # --- new-paper mode (no published assignment): dual-seat assign merge, FLAGs, arbitration ---
    root = tree()
    r = run(root)
    assert r.returncode == 0, r.stderr
    rec = jl1(root / "judgments/bT.jsonl")
    # agree + quote fallback: sol's quote is not in the fulltext -> seat 2's quote wins
    assert rec["evidence"]["online_eval"] == {"value": "yes", "quote": "success rate of 34.5"}, rec["evidence"]
    # conflict -> unclear placeholder; no-vs-unclear -> unclear without FLAG; text fields from seat 1
    assert rec["success"]["S1"]["value"] == "unclear"
    assert rec["one_line"] == "a paper" and rec["version_read"] == "v1"
    # anti value conflict -> 'no'; mitigated conflict on a non-present anti is silent (seat 1's value)
    assert rec["anti"]["AP2"]["value"] == "no" and rec["anti"]["AP1"]["mitigated"] == "unclear"
    con = jl1(root / "judgments/passes/bT.conflicts.json")["conflicts"]
    assert {c["field"] for c in con} == {"success.S1", "anti.AP2.value", "version_read", "assign.sub_pattern"}, con
    assert jl1(root / "patterns/assign_bT.jsonl")["sub_pattern"] == "K01"
    # arbitration: switch sub_pattern to seat 2's, resolve S1 with a verbatim quote, bad quote is skipped
    (root / "judgments/passes/bT.arb.jsonl").write_text("".join(json.dumps(x) + "\n" for x in [
        {"arxiv": AID, "field": "assign.sub_pattern", "value": "K02"},
        {"arxiv": AID, "field": "success.S1", "value": "yes", "quote": "success rate of 34.5"},
        {"arxiv": AID, "field": "evidence.variance", "value": "yes", "quote": "NO SUCH QUOTE"}]) + "\n",
        encoding="utf-8")
    r = run(root, "--apply-arb")
    assert r.returncode == 0, r.stderr
    rec = jl1(root / "judgments/bT.jsonl")
    assert rec["success"]["S1"] == {"value": "yes", "quote": "success rate of 34.5"}
    assert rec["evidence"]["variance"]["value"] == "no", "bad-quote decision must be skipped"
    assert rec["one_line"] == "another paper", "base-switch takes seat 2's text fields"
    assert jl1(root / "patterns/assign_bT.jsonl")["sub_pattern"] == "K02"
    assert jl1(root / "judgments/passes/bT.conflicts.json")["conflicts"] == []
    # mismatched paper sets fail loudly
    (root / "judgments/passes/bT.son55.jsonl").write_text(
        json.dumps({**SON_REC, "arxiv": "2501.00002"}) + "\n", encoding="utf-8")
    assert run(root).returncode != 0

    # --- fixed-assignment mode (paper already published): published row stands, dissent -> proposals ---
    root = tree(sol_asg=SON_ASG, son_asg=SON_ASG, published=SOL_ASG)  # both seats dissent K02 vs published K01
    r = run(root)
    assert r.returncode == 0, r.stderr
    con = jl1(root / "judgments/passes/bT.conflicts.json")["conflicts"]
    assert "assign.sub_pattern" not in {c["field"] for c in con}, "published assignment must not FLAG"
    assert jl1(root / "patterns/assign_bT.jsonl")["sub_pattern"] == "K01", "canonical row is the published one"
    props = [json.loads(l) for l in (root / "patterns/reassign_proposals.jsonl").read_text().splitlines()]
    assert len(props) == 2 and all(p["sub_pattern"] == "K02" and p["batch"] == "bT" for p in props), props
    # arbitration cannot switch a published assignment
    (root / "judgments/passes/bT.arb.jsonl").write_text(
        json.dumps({"arxiv": AID, "field": "assign.sub_pattern", "value": "K02"}) + "\n", encoding="utf-8")
    (root / "judgments/passes/bT.conflicts.json").write_text(
        json.dumps({"batch": "bT", "count": 0, "conflicts": []}), encoding="utf-8")
    r = run(root, "--apply-arb")
    assert r.returncode == 0 and "proposal process" in r.stdout, r.stdout
    assert jl1(root / "patterns/assign_bT.jsonl")["sub_pattern"] == "K01"

    # --- calibration mode: no assign passes at all -> published rows silently, no proposals ---
    root = tree()
    for f in (root / "patterns/assign_passes").iterdir():
        f.unlink()
    (root / "patterns/assignments.jsonl").write_text(json.dumps(SOL_ASG) + "\n", encoding="utf-8")
    r = run(root)
    assert r.returncode == 0, r.stderr
    con = jl1(root / "judgments/passes/bT.conflicts.json")["conflicts"]
    assert "assign.sub_pattern" not in {c["field"] for c in con}
    assert jl1(root / "patterns/assign_bT.jsonl")["sub_pattern"] == "K01"
    print("test_merge_judgments: all assertions passed")


if __name__ == "__main__":
    main()
