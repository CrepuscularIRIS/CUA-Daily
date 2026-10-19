"""Extract numbered success conditions (S1..) and failure modes (F1..) from patterns/main/*.md
→ research/patterns/conditions.json. Scorers judge papers against these ids, so rerun after editing a main card.
"""

import json
import re
from pathlib import Path

BULLET = re.compile(r"^- \*\*(.+?)\*\*\s*(.*)$")


def section(text: str, start: str, end: str) -> list[dict]:
    body = text.split(start, 1)[1].split(end, 1)[0]
    items, cur = [], None
    for line in body.splitlines():
        if m := BULLET.match(line):
            cur = {"name": m.group(1).rstrip("."), "detail": m.group(2).strip()}
            items.append(cur)
        elif cur and line.startswith("  "):
            cur["detail"] += " " + line.strip()
    return items


def main() -> None:
    out = {}
    for card in sorted(Path("patterns/main").glob("*.md")):
        text = card.read_text(encoding="utf-8")
        s = section(text, "## Success conditions", "## Failure modes")
        f = section(text, "## Failure modes", "## Accepted vs rejected gap")
        assert s and f, card
        out[card.stem] = {"S": [{"id": f"S{i}", **c} for i, c in enumerate(s, 1)],
                          "F": [{"id": f"F{i}", **c} for i, c in enumerate(f, 1)]}
    Path("research/patterns/conditions.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print({k: (len(v["S"]), len(v["F"])) for k, v in out.items()})


if __name__ == "__main__":
    main()
