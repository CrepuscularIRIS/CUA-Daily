"""Validate quote-grounded evidence rows (research/EVIDENCE_SCHEMA.md): enums + every quote must occur in the paper file.

Usage: python research/check_evidence.py <evidence.jsonl> [<expected_ids.txt>]
"""

import json
import re
import sys
from pathlib import Path

YPNU = {"yes", "partial", "no", "unclear"}
YNU = {"yes", "no", "unclear"}
KEYS = {
    "online_eval": YPNU, "held_out_env": YPNU, "variance": YNU, "strong_baselines": YPNU, "budget_matched": YPNU,
    "cost_reported": YPNU, "component_ablation": YNU,
    "validator_check": {"tested", "untested", "none", "na", "unclear"},
    "code": {"yes", "announced", "no", "unclear"},
}
NO_QUOTE = {"unclear", "na"}  # values that need no quote
FULLTEXT = Path("research/fulltext")


def squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())  # ignore whitespace, hyphenation breaks, punctuation from PDF/HTML


def check(row: dict, text: str) -> list[str]:
    ev = row.get("evidence") or {}
    errors = [f"missing {k}" for k in KEYS if k not in ev]
    hay = squash(text)
    for k, allowed in KEYS.items():
        item = ev.get(k) or {}
        value, quote = item.get("value"), item.get("quote")
        if value not in allowed:
            errors.append(f"{k}.value={value!r}")
        elif value not in NO_QUOTE:
            if not quote or len(quote.split()) > 45:
                errors.append(f"{k}: non-unclear value needs a quote of ≤45 words")
            elif squash(quote) not in hay:
                errors.append(f"{k}: quote not found in file: {quote[:60]!r}")
    return errors


def main(argv: list[str]) -> int:
    rows = [json.loads(l) for l in open(argv[0], encoding="utf-8") if l.strip()]
    bad = 0
    for r in rows:
        path = FULLTEXT / f"{str(r.get('arxiv')).replace(':', '_')}.txt"
        if not path.exists():
            print(f"{r.get('arxiv')}: no fulltext file {path}")
            bad += 1
            continue
        for err in check(r, path.read_text(encoding="utf-8")):
            bad += 1
            print(f"{r['arxiv']}: {err}")
    if len(argv) > 1:
        want = set(open(argv[1]).read().split())
        got = [r.get("arxiv") for r in rows]
        if set(got) != want or len(got) != len(set(got)):
            bad += 1
            print(f"id mismatch: missing={sorted(want - set(got))[:10]} extra={sorted(set(got) - want)[:10]}")
    print(f"{len(rows)} rows, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
