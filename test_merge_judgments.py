"""Offline test of research/merge_judgments.py on a temp tree. Run: python3 test_merge_judgments.py"""

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


def setup(root: Path) -> None:
    (root / "fulltext").mkdir(parents=True)
    (root / "fulltext" / f"{AID}.txt").write_text(TEXT, encoding="utf-8")
    jp, ap = root / "judgments" / "passes", root / "patterns" / "assign_passes"
    jp.mkdir(parents=True); ap.mkdir(parents=True)
    jp.joinpath("bT.sol.jsonl").write_text(json.dumps(SOL_REC) + "\n", encoding="utf-8")
    jp.joinpath("bT.son55.jsonl").write_text(json.dumps(SON_REC) + "\n", encoding="utf-8")
    ap.joinpath("assign_bT.sol.jsonl").write_text(json.dumps(SOL_ASG) + "\n", encoding="utf-8")
    ap.joinpath("assign_bT.son55.jsonl").write_text(json.dumps(SON_ASG) + "\n", encoding="utf-8")


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(REPO / "research/merge_judgments.py"), "bT",
                           "--root", str(root), *args], capture_output=True, text=True)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "research"
        setup(root)
        r = run(root)
        assert r.returncode == 0, r.stderr
        rec = json.loads((root / "judgments/bT.jsonl").read_text(encoding="utf-8"))
        # agree + quote fallback: sol's quote is not in the fulltext -> seat 2's quote wins
        assert rec["evidence"]["online_eval"] == {"value": "yes", "quote": "success rate of 34.5"}, rec["evidence"]
        # conflict -> unclear placeholder; text fields from seat 1
        assert rec["success"]["S1"]["value"] == "unclear"
        assert rec["one_line"] == "a paper" and rec["version_read"] == "v1"
        # anti value conflict -> 'no'; mitigated conflict -> 'unclear'
        assert rec["anti"]["AP2"]["value"] == "no" and rec["anti"]["AP1"]["mitigated"] == "unclear"
        con = json.loads((root / "judgments/passes/bT.conflicts.json").read_text(encoding="utf-8"))["conflicts"]
        fields = {c["field"] for c in con}
        assert fields == {"success.S1", "anti.AP1.mitigated", "anti.AP2.value", "version_read", "assign.sub_pattern"}, fields
        # assignment merge kept sol's sub_pattern
        asg = json.loads((root / "patterns/assign_bT.jsonl").read_text(encoding="utf-8"))
        assert asg["sub_pattern"] == "K01"
        # arbitration: switch sub_pattern to seat 2's, resolve S1 with a verbatim quote, one bad quote is skipped
        arb = [{"arxiv": AID, "field": "assign.sub_pattern", "value": "K02"},
               {"arxiv": AID, "field": "success.S1", "value": "yes", "quote": "success rate of 34.5"},
               {"arxiv": AID, "field": "evidence.variance", "value": "yes", "quote": "NO SUCH QUOTE"}]
        (root / "judgments/passes/bT.arb.jsonl").write_text(
            "".join(json.dumps(x) + "\n" for x in arb), encoding="utf-8")
        r = run(root, "--apply-arb")
        assert r.returncode == 0, r.stderr
        rec = json.loads((root / "judgments/bT.jsonl").read_text(encoding="utf-8"))
        assert rec["success"]["S1"] == {"value": "yes", "quote": "success rate of 34.5"}
        assert rec["evidence"]["variance"]["value"] == "no", "bad-quote decision must be skipped"
        # re-based on seat 2: text fields now seat 2's, AP2 judgement calls come from seat 2's pass
        assert rec["one_line"] == "another paper"
        asg = json.loads((root / "patterns/assign_bT.jsonl").read_text(encoding="utf-8"))
        assert asg["sub_pattern"] == "K02"
        con = json.loads((root / "judgments/passes/bT.conflicts.json").read_text(encoding="utf-8"))["conflicts"]
        assert con == [], "base-switch retires the paper's old per-item flags wholesale"
        # mismatched paper sets fail loudly
        jp = root / "judgments/passes"
        jp.joinpath("bT.son55.jsonl").write_text(
            json.dumps({**SON_REC, "arxiv": "2501.00002"}) + "\n", encoding="utf-8")
        assert run(root).returncode != 0
        # calibration mode: no assign passes -> fall back to published assignments, no assign FLAG
        root.joinpath("patterns/assign_bT.jsonl").unlink()
        for f in (root / "patterns/assign_passes").iterdir():
            f.unlink()
        jp.joinpath("bT.son55.jsonl").write_text(json.dumps(SON_REC) + "\n", encoding="utf-8")
        root.joinpath("patterns/assignments.jsonl").write_text(json.dumps(SOL_ASG) + "\n", encoding="utf-8")
        r = run(root)
        assert r.returncode == 0, r.stderr
        con = json.loads((root / "judgments/passes/bT.conflicts.json").read_text(encoding="utf-8"))["conflicts"]
        assert "assign.sub_pattern" not in {c["field"] for c in con}
        asg = json.loads((root / "patterns/assign_bT.jsonl").read_text(encoding="utf-8"))
        assert asg["sub_pattern"] == "K01"
    print("test_merge_judgments: all assertions passed")


if __name__ == "__main__":
    main()
