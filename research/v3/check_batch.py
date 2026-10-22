#!/usr/bin/env python3
"""sol-batch-v3 批次机械校验:ID 一一对应、档位范围、算术、null 传播、必填字段。

用法: python3 research/v3/check_batch.py <run_dir> [batch_id ...]
不带 batch_id 时校验该 run 下全部批次;exit 0 = 全部通过。
"""
import json
import sys
from pathlib import Path

W = {"G": 15, "M": 25, "X": 20, "E": 40}  # gui-v3
AXES = ("G", "M", "X", "E")
REQ = ("paper_id", "version", "source_url", "material_level", "status",
       "claim_type", "move", "gap", "patterns", "ratings", "screen_score",
       "reasons", "evidence", "claim_support", "evidence_level", "caveat", "needs")


def check_batch(run: Path, bid: str) -> list[str]:
    problems: list[str] = []
    inp = run / "batches" / f"{bid}-inputs.tsv"
    out = run / "batches" / f"{bid}.jsonl"
    ids = [l.split("\t")[0] for l in inp.read_text().splitlines()[1:] if l.strip()]
    if not out.exists():
        return [f"{bid}: 输出文件缺失"]
    rows = {}
    for ln, line in enumerate(out.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as e:
            problems.append(f"{bid} L{ln}: JSON 解析失败 {e}")
            continue
        pid = d.get("paper_id", "?")
        if pid in rows:
            problems.append(f"{bid}: {pid} 重复")
        rows[pid] = d
    for i in ids:
        if i not in rows:
            problems.append(f"{bid}: {i} 缺输出行")
    for pid in rows:
        if pid not in ids:
            problems.append(f"{bid}: {pid} 不在输入清单")
    for pid, d in rows.items():
        miss = [k for k in REQ if k not in d]
        if miss:
            problems.append(f"{bid}/{pid}: 缺字段 {','.join(miss)}")
            continue
        st = d["status"]
        r = d["ratings"] or {}
        if st == "scored":
            bad = [a for a in AXES if not (a in r and isinstance(r[a], int) and 0 <= r[a] <= 4)]
            if bad:
                problems.append(f"{bid}/{pid}: 档位缺失/越界 {bad}")
                continue
            exp = sum(W[a] * r[a] for a in AXES) / 4
            got = d["screen_score"]
            if not isinstance(got, (int, float)) or abs(got - exp) > 0.01:
                problems.append(f"{bid}/{pid}: screen_score {got} != 期望 {exp}")
            rs = d["reasons"] or {}
            if any(not (rs.get(a) or "").strip() for a in AXES):
                problems.append(f"{bid}/{pid}: reasons 不全")
        else:
            if any(r.get(a) is not None for a in AXES) or d["screen_score"] is not None:
                problems.append(f"{bid}/{pid}: status={st} 但分数字段非 null")
        ev = d["evidence"] or []
        if not (1 <= len(ev) <= 3) or any(not (e.get("locator") or "").strip() for e in ev):
            problems.append(f"{bid}/{pid}: evidence 需 1–3 条且带 locator")
        for k in ("move", "gap"):
            if not (d.get(k) or "").strip():
                problems.append(f"{bid}/{pid}: {k} 为空")
    return problems


def main() -> int:
    run = Path(sys.argv[1])
    bids = sys.argv[2:] or sorted(
        p.name.split("-")[0] for p in (run / "batches").glob("*-inputs.tsv"))
    all_p = []
    for bid in bids:
        all_p += check_batch(run, bid)
    if all_p:
        print("\n".join(all_p))
        print(f"FAIL: {len(all_p)} 个问题")
        return 1
    print(f"OK: {len(bids)} 批全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
