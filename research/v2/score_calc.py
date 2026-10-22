#!/usr/bin/env python3
"""Deterministic score computation for v2.2 records (SCORE_SPEC arithmetic).

S = (wG*rG + wM*rM + wX*rX + sum(wE_j*rE_j)) / 4, weights sum 100.
Unknowns -> raw/display null, L (unknowns as 0) / U (as 4), coverage =
judged weight / 100. Weights are the draft proposal frozen for this run;
any calibration change requires a new rubric hash and re-run manifest.

Usage: python3 research/v2/score_calc.py <record.json> [<record.json> ...]
       (or --check to recompute in place for every *.json under a seat dir)
"""
import hashlib
import json
import sys
from pathlib import Path

W = {"G": 15, "M": 25, "X": 20}
WE = {"measurement": 10, "causality": 10, "holdout": 10, "statistics": 5, "cost": 5}
assert sum(W.values()) + sum(WE.values()) == 100

RATING_KEYS = ["G", "M", "X", "E.measurement", "E.causality", "E.holdout",
               "E.statistics", "E.cost"]


def get_rating(rec: dict, key: str):
    ratings = rec.get("ratings", {})
    if key in ratings:  # flat form: "E.measurement" (contract literal)
        return ratings[key]
    if key.startswith("E."):
        return (ratings.get("E") or {}).get(key[2:])
    return ratings.get(key)


def compute(rec: dict) -> dict:
    judged_w, lo, hi, unknown = 0, 0.0, 0.0, 0
    for key in RATING_KEYS:
        w = WE[key[2:]] if key.startswith("E.") else W[key]
        r = get_rating(rec, key)
        val = (r or {}).get("rating")
        stat = (r or {}).get("status")
        if stat == "unknown" or val is None:
            unknown += 1  # lo adds 0, hi adds 4*w/4
            hi += w * 4 / 4
        else:
            judged_w += w
            lo += w * val / 4
            hi += w * val / 4
    raw = None if unknown else round(lo, 6)
    return {
        "raw": raw,
        "display": None if raw is None else round(raw, 1),
        "lower": round(lo, 1),
        "upper": round(hi, 1),
        "coverage": judged_w / 100,
        "rubric_hash": RUBRIC_HASH,
    }


RUBRIC_HASH = hashlib.sha256(
    Path(__file__).resolve().parents[2].joinpath("research/SCORE_SPEC.md").read_bytes()
).hexdigest()


def main() -> None:
    args = sys.argv[1:]
    files: list[Path]
    if args and args[0] == "--check":
        seat_dir = Path(args[1])
        files = sorted(seat_dir.glob("*.json"))
    else:
        files = [Path(a) for a in args]
    for f in files:
        if f.name == "batch-report.json":
            continue
        rec = json.loads(f.read_text())
        st = rec.get("status")
        st = st.get("state", st.get("value")) if isinstance(st, dict) else st
        if st != "reviewed":
            continue
        sc = compute(rec)
        old = rec.get("score") or {}
        if old.get("raw") is not None and sc["raw"] is not None and abs(old["raw"] - sc["raw"]) > 1e-6:
            print(f"{f.name}: MISMATCH recorded {old.get('raw')} != computed {sc['raw']}")
            sys.exit(1)
        if (old.get("raw") is None) != (sc["raw"] is None):
            print(f"{f.name}: MISMATCH recorded raw={old.get('raw')} but computed {sc['raw']} "
                  f"(rating shapes unreadable?)")
            sys.exit(1)
            print(f"{f.name}: MISMATCH recorded {old.get('raw')} != computed {sc['raw']}")
            sys.exit(1)
        if old.get("raw") is None:
            rec["score"] = sc
            f.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            print(f"{f.name}: score filled {sc['display']}")
        else:
            print(f"{f.name}: score verified {sc['display']}")


if __name__ == "__main__":
    main()
