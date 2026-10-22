#!/usr/bin/env python3
"""problem-core-v1.1 L1 材料切分:从已缓存原文切 摘要+引言;切不出则只用摘要。

用法: python3 research/scoring/tools/cut_l1.py <ids_file> <run_dir>
读 research/corpus.jsonl 与 research/fulltext/<id>.txt,
写 <run_dir>/l1_material/<arxiv>.txt 与 <run_dir>/l1_manifest.tsv(arxiv, material)。
"""
import json
import re
import sys
from pathlib import Path

INTRO = re.compile(r"^\s*#{0,4}\s*(?:\d+\.?\d*|[IVX]+\.?)?\s*introduction\s*$", re.I)
NEXT_SEC = re.compile(r"^\s*#{0,4}\s*(?:\d+\.?\d*\s+\w|\([IVX]+\)|[IVX]{1,4}\.\s+\w|abstract|related work|background|preliminar)", re.I)
CAP = 9000


def cut_intro(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if INTRO.match(ln):
            start = i + 1
            break
    if start is None:
        return ""
    out = []
    total = 0
    for ln in lines[start:]:
        if total > 1200 and NEXT_SEC.match(ln):
            break
        out.append(ln)
        total += len(ln) + 1
        if total >= CAP:
            out.append("[…cut]")
            break
    body = "\n".join(out).strip()
    return body if len(body) > 400 else ""


def main() -> int:
    ids_file, run = Path(sys.argv[1]), Path(sys.argv[2])
    meta = {}
    for l in open("research/corpus.jsonl"):
        d = json.loads(l)
        meta[d["arxiv"]] = d
    (run / "l1_material").mkdir(parents=True, exist_ok=True)
    rows = []
    for aid in [x for x in ids_file.read_text().split() if x]:
        m = meta.get(aid)
        if not m:
            rows.append((aid, "missing"))
            continue
        head = (f"arxiv: {aid} ({m.get('latest_version','')})\ntitle: {m['title']}\n"
                f"source: https://arxiv.org/abs/{aid}\n\n§Abstract\n{m.get('abstract','').strip()}\n")
        ft = Path(f"research/fulltext/{aid}.txt")
        if ft.exists() and ft.stat().st_size >= 3000:
            intro = cut_intro(ft.read_text(errors="ignore"))
            if intro:
                head += f"\n§Introduction (from cached fulltext; cut at ~{CAP} chars)\n{intro}\n"
                rows.append((aid, "abstract_intro"))
            else:
                rows.append((aid, "abstract"))
        else:
            rows.append((aid, "abstract"))
        (run / "l1_material" / f"{aid}.txt").write_text(head, encoding="utf-8")
    with open(run / "l1_manifest.tsv", "w") as f:
        f.write("arxiv\tmaterial\n")
        for aid, lvl in rows:
            f.write(f"{aid}\t{lvl}\n")
    from collections import Counter
    print("L1 material:", dict(Counter(l for _, l in rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
