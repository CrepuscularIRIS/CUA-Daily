#!/usr/bin/env python3
"""Inter-seat agreement on a holdout set, measured BEFORE Opus aggregation.

For each holdout paper judged reviewed by both seats, compares the two seats'
mechanically recomputed raw totals (and per-item rating deltas). Acceptance
(SCORE_SPEC): >=8 scorable pairs, median |total diff| <=5, >=90% |diff| <=10.

Usage: python3 research/v2/agreement.py <run_id> <batch_id> [<batch_id> ...]
"""
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_calc import compute  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def seat_scores(bdir: Path, seat: str) -> dict:
    out = {}
    for f in (bdir / "seats" / seat / "attempts" / "a1").glob("*.json"):
        if f.name == "batch-report.json":
            continue
        rec = json.loads(f.read_text())
        if rec.get("status") == "reviewed":
            raw = compute(rec)["raw"]
            if raw is not None:  # scorable pairs only (unknown items -> null)
                out[f.stem] = raw
    return out


def main() -> None:
    run_id, batches = sys.argv[1], sys.argv[2:]
    run = ROOT / "research" / "v2" / "runs" / run_id
    holdout = {p["arxiv"] for p in json.loads((run / "calibration" / "plan.json").read_text())["papers"]
               if p["layer"] == "holdout"}
    sol, son = {}, {}
    for b in batches:
        bdir = run / "batches" / b
        sol |= seat_scores(bdir, "sol")
        son |= seat_scores(bdir, "son55")

    pairs = []
    for k in sorted(holdout & set(sol) & set(son)):
        pairs.append({"paper": k, "sol": sol[k], "son55": son[k],
                      "diff": round(abs(sol[k] - son[k]), 1)})
    diffs = [p["diff"] for p in pairs]
    report = {
        "measured_at": "pre-aggregation",
        "n_pairs": len(pairs),
        "n_required": 8,
        "median_diff": statistics.median(diffs) if diffs else None,
        "p90_within_10": (sum(1 for d in diffs if d <= 10) / len(diffs)) if diffs else None,
        "pairs": pairs,
        "pass": bool(len(pairs) >= 8 and diffs
                     and statistics.median(diffs) <= 5
                     and sum(1 for d in diffs if d <= 10) / len(diffs) >= 0.9),
    }
    print(json.dumps(report, ensure_ascii=False, indent=1))
    out = run / "calibration" / "agreement.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
