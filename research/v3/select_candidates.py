#!/usr/bin/env python3
"""sol-batch-v3 选题:合并批次 → 排序 → top15 候选 + 问题清单 + 补材料候选。

用法: python3 research/v3/select_candidates.py <run_dir>
写 <run_dir>/candidates.tsv 并在 stdout 打印摘要;selection.md 由总控/Opus 阶段补写。
"""
import json
import sys
from pathlib import Path


def main() -> int:
    run = Path(sys.argv[1])
    rows = []
    for f in sorted((run / "batches").glob("b*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                d["_batch"] = f.stem
                rows.append(d)
    scored = [r for r in rows if r["status"] == "scored"]
    needs = [r for r in rows if r["status"] == "needs_material"]
    oos = [r for r in rows if r["status"] == "out_of_scope"]
    # SELECTION: score 降序,同分 E→M 降序,再 paper_id
    ranked = sorted(scored, key=lambda r: (-r["screen_score"],
                                           -(r["ratings"]["E"] or 0),
                                           -(r["ratings"]["M"] or 0),
                                           r["paper_id"]))
    blocked = [r for r in ranked if r.get("claim_support") in ("contradicted", "unresolved")]
    blocked_ids = {r["paper_id"] for r in blocked}
    candidates = [r for r in ranked if r["paper_id"] not in blocked_ids][:15]
    with open(run / "candidates.tsv", "w") as f:
        f.write("rank\tpaper_id\tscreen_score\tG\tM\tX\tE\tclaim_support\tclaim_type\ttitle?\tbatch\n")
        for i, r in enumerate(candidates, 1):
            g = r["ratings"]
            f.write(f"{i}\t{r['paper_id']}\t{r['screen_score']}\t{g['G']}\t{g['M']}\t{g['X']}\t{g['E']}"
                    f"\t{r.get('claim_support','')}\t{r.get('claim_type','')}\t\t{r['_batch']}\n")
    print(f"总记录 {len(rows)} | scored {len(scored)} | needs_material {len(needs)} | out_of_scope {len(oos)}")
    print(f"问题清单(contradicted/unresolved,不入候选): {len(blocked)}")
    print("top15 候选:")
    for i, r in enumerate(candidates, 1):
        print(f"  {i:2d}. {r['paper_id']:<14} {r['screen_score']:>6.2f}  "
              f"{r['ratings']['G']}/{r['ratings']['M']}/{r['ratings']['X']}/{r['ratings']['E']}  "
              f"{r.get('claim_support','')}  {r.get('move','')[:50]}")
    if needs:
        print(f"needs_material {len(needs)} 篇(null 分,不参与排序): "
              + ", ".join(r["paper_id"] for r in needs[:20]) + ("…" if len(needs) > 20 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
