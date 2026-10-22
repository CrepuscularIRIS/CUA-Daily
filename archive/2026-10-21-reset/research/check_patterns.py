"""Pre-publish guard for pattern cards (patterns/sub/*.md, patterns/main/*.md).

Checks: (1) header member counts match the dedup'd bundles; (2) contrast-table rows match contrast.json;
(3) no member paper title or method short-name appears in any card (rejected papers must never be named).
Needs local bundles: run `PYTHONPATH=research python3 research/build_bundles.py` first.

Usage: python research/check_patterns.py [--fix-headers]
"""

import json
import re
import sys
from pathlib import Path

R, CARDS = Path("research"), Path("patterns")
HEADER = re.compile(r"corpus support: (\d+) papers \(accepted (\d+) · rejected (\d+) · unlabeled (\d+)\)")
PARENT_ROW = re.compile(r"^\|\s*parent[^|]*?(iclr_2025_2026|all_labeled)[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
ROW = re.compile(r"^\|\s*`?(iclr_2025_2026|all_labeled)`?\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", re.M)


def short_names(title: str) -> set[str]:
    """Full title plus a method name before ':' (e.g. 'FooBar: ...'), if distinctive enough to grep."""
    names = {title.strip()}
    head = title.split(":")[0].strip()
    if ":" in title and 4 <= len(head) <= 40 and len(head.split()) <= 4 and not head.islower():
        names.add(head)
    return names


def main(argv: list[str]) -> int:
    fix = "--fix-headers" in argv
    con = json.loads((R / "patterns/contrast.json").read_text())
    rows = {v: {r["key"]: r for r in con[v]["sub"] + con[v]["main"]} for v in ("iclr_2025_2026", "all_labeled")}
    expected, names, parents = {}, set(), {}
    for b in map(lambda p: json.loads(p.read_text()), sorted((R / "patterns/bundles").glob("*.json"))):
        parents[b["main"]["id"]] = {s["id"] for s in b["sub_patterns"]}
        for s in b["sub_patterns"]:
            o = [m["outcome"] for m in s["members"]]
            expected[s["id"]] = (len(o), o.count("accepted"), o.count("rejected"), o.count("unknown"))
            for m in s["members"]:
                names |= short_names(m["title"])
    generic = {"Self-Refine", "Reflexion", "Voyager"}  # well-known accepted baselines may be named as context
    names = {n for n in names if n not in generic}
    bad = 0
    for card in sorted(CARDS.glob("*/*.md")):
        text = card.read_text(encoding="utf-8")
        key = card.stem
        if key in expected and (h := HEADER.search(text)):
            got = tuple(map(int, h.groups()))
            if got != expected[key]:
                bad += 1
                print(f"{card}: header {got} != expected {expected[key]}")
                if fix:
                    n, a, r, u = expected[key]
                    text = text.replace(h.group(0), f"corpus support: {n} papers (accepted {a} · rejected {r} · unlabeled {u})")
                    card.write_text(text, encoding="utf-8")
        parent = next((b for b, subs in parents.items() if key in subs), None)
        for line in text.splitlines():
            m = PARENT_ROW.match(line)
            if m and parent:
                ref = rows[m.group(1)].get(parent)
                nums = tuple(map(int, m.groups()[1:]))
                if ref and nums != (ref["n"], ref["n_accept"], ref["n_reject"]):
                    bad += 1
                    print(f"{card}: parent {m.group(1)} row {nums} != contrast {(ref['n'], ref['n_accept'], ref['n_reject'])}")
        for view, n, acc, rej in ROW.findall(text):
            ref = rows[view].get(key)
            line = next(l for l in text.splitlines() if re.match(rf"^\|\s*`?{view}`?\s*\|\s*{n}\s*\|", l))
            if ref is None and "insufficient" in line:
                continue  # counts shown, rate withheld: allowed by the spec
            if ref is None or (int(n), int(acc), int(rej)) != (ref["n"], ref["n_accept"], ref["n_reject"]):
                bad += 1
                print(f"{card}: {view} row ({n},{acc},{rej}) != contrast {ref and (ref['n'], ref['n_accept'], ref['n_reject'])}")
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            d = re.search(r"([+\-−]?\d+(?:\.\d+)?)\s*pp", cells[5]) if len(cells) > 5 else None
            if d and abs(float(d.group(1).replace("−", "-")) - ref["delta_pp"]) > 0.05:
                bad += 1
                print(f"{card}: {view} Δ {d.group(1)} != contrast {ref['delta_pp']}")
        for name in names:
            if re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", text):
                bad += 1
                print(f"{card}: names a member paper: {name!r}")
    print(f"{len(list(CARDS.glob('*/*.md')))} cards checked, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
