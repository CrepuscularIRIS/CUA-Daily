"""Merge research/patterns/assign_*.jsonl (one per judge batch) into research/patterns/assignments.jsonl.

A later batch file wins for a re-assigned paper. Safe to run concurrently with writers: incomplete trailing lines are
skipped. Usage: python research/merge_assign.py
"""

import json
from pathlib import Path

P = Path("research/patterns")


def main() -> None:
    out: dict[str, dict] = {}
    for f in sorted(P.glob("assign_*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("arxiv") and r.get("sub_pattern"):
                out[r["arxiv"]] = {k: r.get(k) for k in ("arxiv", "sub_pattern", "fit", "fit_note")}
    (P / "assignments.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out.values()))
    print(f"{len(out)} assignments")


if __name__ == "__main__":
    main()
