"""Validate screening rows (research/SCREEN_RUBRIC.md): enums, one row per expected id.

Usage: python research/check_screen.py <screen.jsonl> <ids.txt>
"""

import json
import sys

TIERS = {"A", "B", "C"}
KINDS = {"method", "benchmark", "dataset", "empirical", "survey", "position", "system"}
PLATFORMS = {"web", "mobile", "desktop", "general"}
COMPONENTS = {"perception", "grounding", "planning", "action_space", "memory", "reflection", "world_model",
              "simulator", "training_data", "rl", "reward_judge", "policy", "multi_agent", "evaluation", "safety",
              "efficiency"}


def check(row: dict) -> list[str]:
    errs = []
    if row.get("tier") not in TIERS:
        errs.append(f"tier={row.get('tier')!r}")
    if row.get("kind") not in KINDS:
        errs.append(f"kind={row.get('kind')!r}")
    if not set(row.get("platforms") or []) <= PLATFORMS:
        errs.append(f"platforms={row.get('platforms')!r}")
    if not set(row.get("components") or []) <= COMPONENTS:
        errs.append(f"components={row.get('components')!r}")
    if row.get("confidence") not in {"high", "low"}:
        errs.append(f"confidence={row.get('confidence')!r}")
    if not isinstance(row.get("reason"), str) or not row["reason"].strip() or len(row["reason"].split()) > 30:
        errs.append("reason empty or > 30 words")
    return errs


def main(argv: list[str]) -> int:
    rows = [json.loads(line) for line in open(argv[0], encoding="utf-8") if line.strip()]
    errs = [f"{r.get('arxiv')}: {e}" for r in rows for e in check(r)]
    want, got = set(open(argv[1]).read().split()), [r.get("arxiv") for r in rows]
    if set(got) != want or len(got) != len(set(got)):
        errs.append(f"id mismatch: missing={sorted(want - set(got))[:10]} extra={sorted(set(got) - want)[:10]}")
    print("\n".join(errs + [f"{len(rows)} rows, {len(errs)} problems"]))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
