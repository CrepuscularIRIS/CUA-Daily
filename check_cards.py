"""Validate frontmatter of cards/*.md against the schema in cards/_TEMPLATE.md.

Stdlib only, so CI and the maintainer agent can run it without `uv sync`.
Usage: python check_cards.py [card.md ...]   (default: all cards except _TEMPLATE.md)
"""

import re
import sys
from pathlib import Path

ENUMS = {
    "tier": {"A", "B"},
    "evidence_level": {"offline", "online", "transfer"},
    "held_out": {"yes", "partial", "no", "unclear"},
    "budget_matched": {"yes", "partial", "no", "unclear"},
    "leakage_risk": {"low", "medium", "high", "unclear"},
    "code_status": {"none", "announced", "released", "verified_run"},
}
LIST_ENUMS = {
    "platforms": {"web", "mobile", "desktop", "general"},
    "components": {"perception", "grounding", "planning", "action_space", "memory", "reflection", "world_model",
                   "simulator", "training_data", "rl", "reward_judge", "policy", "multi_agent", "evaluation", "safety",
                   "efficiency"},
}
NULLABLE = {"arxiv", "openreview", "code", "code_commit", "license"}
REQUIRED = {"id", "title", "authors", "first_seen", "venue", "checked"} | NULLABLE | set(ENUMS) | set(LIST_ENUMS)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SECTIONS = ["## 一句话", "## 机制", "## 作者报告的证据", "## 我们的诊断", "## 代码核查",
            "## 相对已有工作的增量", "## 适合 / 不适合", "## 一个值得验证的问题", "## 来源"]


def parse_frontmatter(text: str) -> dict:
    """Parse the flat `key: value` frontmatter subset the template uses."""
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    block = text[4:text.index("\n---", 4)]
    fields = {}
    for line in block.splitlines():
        line = re.sub(r"\s+#.*$", "", line).strip()  # ponytail: breaks on ' #' inside quoted values; use a YAML lib if titles need it
        if not line or line.startswith("#"):
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        if raw == "null":
            value = None
        elif raw.startswith("[") and raw.endswith("]"):
            value = [v.strip().strip("\"'") for v in raw[1:-1].split(",") if v.strip()]
        else:
            value = raw.strip("\"'")
        fields[key.strip()] = value
    return fields


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        f = parse_frontmatter(text)
    except ValueError as e:
        return [str(e)]
    errors = [f"missing key: {k}" for k in sorted(REQUIRED - f.keys())]
    for k, allowed in ENUMS.items():
        if k in f and f[k] not in allowed:
            errors.append(f"{k}={f[k]!r} not in {sorted(allowed)}")
    for k, allowed in LIST_ENUMS.items():
        if k in f and (not isinstance(f[k], list) or not f[k] or set(f[k]) - allowed):
            errors.append(f"{k}={f[k]!r} must be a non-empty subset of {sorted(allowed)}")
    for k in REQUIRED - NULLABLE:
        if k in f and f[k] is None:
            errors.append(f"{k} must not be null")
    for k in ("first_seen", "checked"):
        if isinstance(f.get(k), str) and not DATE.match(f[k]):
            errors.append(f"{k}={f[k]!r} is not YYYY-MM-DD")
    if f.get("id") and f["id"] != path.stem:
        errors.append(f"id={f['id']!r} must equal filename stem {path.stem!r}")
    if f.get("code_status") == "verified_run" and not f.get("code_commit"):
        errors.append("verified_run requires code_commit")
    errors += [f"missing section: {s}" for s in SECTIONS if s not in text]
    return errors


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in argv] or sorted(p for p in Path("cards").glob("*.md") if p.name != "_TEMPLATE.md")
    failed = 0
    for p in paths:
        errs = check(p)
        failed += bool(errs)
        print(f"{'FAIL' if errs else 'ok  '} {p}")
        for e in errs:
            print(f"     - {e}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
