#!/usr/bin/env python3
"""problem-core-v1.1 记录机械校验(L1/L2 通用):ID 一一对应、枚举合法、封顶规则、facts 定位、subcard 结构。

用法: python3 research/scoring/tools/l1_check.py <run_dir> <batch_id ...>
不带 batch_id 时校验全部已完成批次;exit 0 = 全部通过。结构通过不代表科学判断正确。
"""
import json
import sys
from pathlib import Path

Q1 = {"measured_own", "measured_cited_checked", "measured_cited_unchecked", "proof",
      "counterexample", "constraint_conflict", "asserted", "unknown"}
Q2 = {"challenges_barrier", "open_failure", "new_bottleneck", "vertical_port", "prior_solved", "unknown"}
Q3 = {"capability", "judgment", "incremental", "local"}
Q4 = {"fits", "partial", "misfit", "unknown"}
TIER = {"P0", "P1", "P2", "P3", None}
EV = {"confirmed", "pending_method", "pending_experiment", "pending_material"}
PRIO = {"high", "medium", "low", "none"}
NA = {"to_l2", "to_l3", "park", "exclude"}
FAM = {"F0", "F1", "F2", "F3", "F4", "F5"}
REQ = ("paper_id", "stage", "status", "material", "problem_statement", "families",
       "q1_basis", "q2_open", "q3_change", "q4_fit", "problem_tier",
       "evidence_status", "priority", "next_action", "facts", "biggest_gap")


def tier_cap(r: dict) -> list[str]:
    t, p = [], r.get("problem_tier")
    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    if r.get("q4_fit") == "misfit" and p and rank[p] > 1:
        t.append(f"q4=misfit 但档位 {p} > P1")
    if r.get("q1_basis") in ("asserted", "measured_cited_unchecked") and p and rank[p] > 2:
        t.append(f"q1={r['q1_basis']} 但档位 {p} > P2")
    if r.get("q2_open") == "vertical_port" and p and rank[p] > 1:
        t.append("q2=vertical_port 但档位 > P1")
    return t


def check_batch(run: Path, bid: str) -> list[str]:
    out, probs = run / "batches" / f"{bid}.jsonl", []
    inp = run / "batches" / f"{bid}-inputs.tsv"
    if not out.exists():
        return [f"{bid}: 输出缺失"]
    ids = [l.split("\t")[0] for l in inp.read_text().splitlines()[1:] if l.strip()] if inp.exists() else []
    seen = set()
    for ln, line in enumerate(out.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            probs.append(f"{bid} L{ln}: JSON 解析失败 {e}")
            continue
        pid = r.get("paper_id", "?")
        if pid in seen:
            probs.append(f"{bid}: {pid} 重复")
        seen.add(pid)
        miss = [k for k in REQ if k not in r]
        if miss:
            probs.append(f"{bid}/{pid}: 缺字段 {','.join(miss)}")
            continue
        if r["q1_basis"] not in Q1: probs.append(f"{bid}/{pid}: q1_basis 非法 {r['q1_basis']}")
        if r["q2_open"] not in Q2: probs.append(f"{bid}/{pid}: q2_open 非法 {r['q2_open']}")
        if r["q3_change"] not in Q3: probs.append(f"{bid}/{pid}: q3_change 非法 {r['q3_change']}")
        if r["q4_fit"] not in Q4: probs.append(f"{bid}/{pid}: q4_fit 非法 {r['q4_fit']}")
        if r["problem_tier"] not in TIER: probs.append(f"{bid}/{pid}: problem_tier 非法")
        if r["evidence_status"] not in EV: probs.append(f"{bid}/{pid}: evidence_status 非法")
        if r["priority"] not in PRIO: probs.append(f"{bid}/{pid}: priority 非法")
        if r["next_action"] not in NA: probs.append(f"{bid}/{pid}: next_action 非法")
        fam = r.get("families") or []
        if not (1 <= len(fam) <= 2) or any(f not in FAM for f in fam):
            probs.append(f"{bid}/{pid}: families 非法 {fam}")
        probs += [f"{bid}/{pid}: {m}" for m in tier_cap(r)]
        st = r["status"]
        if st == "out_of_scope" and r["next_action"] != "exclude":
            probs.append(f"{bid}/{pid}: out_of_scope 应 exclude")
        if st == "scored" or st == "assessed":
            pass
        if r["next_action"] == "exclude" and st != "out_of_scope" and r.get("problem_tier") != "P0":
            probs.append(f"{bid}/{pid}: exclude 但既非 OOS 也非 P0")
        facts = r.get("facts") or []
        if len(facts) > 2 or any(not (f.get("loc") or "").strip() for f in facts):
            probs.append(f"{bid}/{pid}: facts 需 ≤2 条且带 loc")
    for i in ids:
        if i not in seen:
            probs.append(f"{bid}: {i} 缺输出行")
    for p in seen:
        if ids and p not in ids:
            probs.append(f"{bid}: {p} 不在输入清单")
    return probs


def main() -> int:
    run = Path(sys.argv[1])
    bids = sys.argv[2:] or sorted(
        p.name[:-6] for p in (run / "batches").glob("*.jsonl"))
    all_p = []
    for b in bids:
        all_p += check_batch(run, b)
    if all_p:
        print("\n".join(all_p[:40]))
        print(f"FAIL: {len(all_p)} 个问题")
        return 1
    print(f"OK: {len(bids)} 批全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
