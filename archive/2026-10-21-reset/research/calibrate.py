"""Compare a maintainer's re-judgment of gold papers against the reference judgments.

Gold set = research/calibration/gold.jsonl (reference judgments copied from published batches, spanning patterns and bands). A new maintainer or
model re-judges a few gold ids into a separate file; this reports per-paper score drift and item agreement.
Pass = every paper within ±TOL points and evidence_level identical; otherwise the run is flagged for a human.

Usage: python research/calibrate.py <new_judgments.jsonl> [--gold research/calibration/gold.jsonl]
"""

import json
import sys
from pathlib import Path

from score import context, score

TOL = 8


def main(argv: list[str]) -> int:
    gold_path = Path(argv[argv.index("--gold") + 1]) if "--gold" in argv else Path("research/calibration/gold.jsonl")
    gold = {r["arxiv"]: r for r in map(json.loads, gold_path.read_text().splitlines())}
    new = [json.loads(l) for l in Path(argv[0]).read_text().splitlines() if l.strip()]
    main_of, cond = context()
    ok = True
    for r in new:
        g = gold.get(r["arxiv"])
        if not g:
            print(f"{r['arxiv']}: not a gold paper")
            continue
        main = main_of[r["arxiv"]][1]
        sg, sn = score(g, main, cond)["total"], score(r, main, cond)["total"]
        items = [("evidence", k) for k in g["evidence"]] + [("success", k) for k in g["success"]] + [("failure", k) for k in g["failure"]]
        agree = sum(g[a][b]["value"] == r[a][b]["value"] for a, b in items) / len(items)
        lvl = g["evidence_level"]["value"] == r["evidence_level"]["value"]
        passed = abs(sg - sn) <= TOL and lvl
        ok &= passed
        print(f"{r['arxiv']}: gold {sg} new {sn} (Δ{sn - sg:+d}) · item agreement {agree:.0%} · level "
              f"{g['evidence_level']['value']}→{r['evidence_level']['value']} · {'PASS' if passed else 'FLAG'}")
    print("CALIBRATION", "PASS" if ok else "FLAG — do not publish new scores until a human reviews")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
