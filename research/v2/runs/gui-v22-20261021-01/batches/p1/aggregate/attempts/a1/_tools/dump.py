"""Print a compact side-by-side view of both seat records for one paper (read-only)."""
import json
import sys
from pathlib import Path

BATCH = Path(__file__).resolve().parents[4]
KEYS8 = ["G", "M", "X", "E.measurement", "E.causality", "E.holdout", "E.statistics", "E.cost"]


def ratings(d: dict) -> dict:
    r = d["ratings"]
    out = {}
    for k in KEYS8:
        if k in r:
            out[k] = r[k]
        elif k.startswith("E.") and "E" in r:
            out[k] = r["E"][k[2:]]
    return out


def j(x) -> str:
    return json.dumps(x, ensure_ascii=False)


def main(pk: str, part: str) -> None:
    seats = {s: json.loads((BATCH / f"seats/{s}/attempts/a1/{pk}.json").read_text()) for s in ("sol", "son55")}
    for s, d in seats.items():
        print(f"===== {s} =====")
        if part in ("all", "head"):
            print("paper:", j(d["paper"]))
            print("assessment:", j(d["assessment"]))
            print("gap:", j(d["gap"]))
            print("rs:", j(d["rs_pattern"]))
            print("domain:", j(d["domain_pattern"]))
        if part in ("all", "claims"):
            for c in d["claims"]:
                print("claim:", j(c))
        if part in ("all", "ratings"):
            for k, v in ratings(d).items():
                print(f"R {k}: {v['status']} {v['rating']} | {v['reason']} | ev={v.get('evidence_ids')} ce={v.get('counterevidence_ids')}")
            print("score:", j(d["score"]))
        if part in ("all", "exp"):
            only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
            for e in d["expectations"]:
                if only is None or e["id"] in only:
                    print(f"X {e['id']} {e.get('applicable')} {e['status']} [{e.get('score_item')}] {e['reason']}")
        if part == "evidence":
            for e in d["evidence"]:
                print(f"{e['evidence_id']} [{e['kind']}] {e['locator']} :: {e['quote'][:220]}")
        if part == "sig":
            print(j(d["signatures"]))
            print(j(d["pattern_mapping"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "all")
