"""Render the paper board from research/scores.jsonl (format inspired by Aerial-VLN-Arxiv-Daily, plus scores).

Writes papers/README.md (every scored paper, grouped by main pattern, best first) and rewrites the block between
<!-- BOARD:START --> and <!-- BOARD:END --> in README.md with the top-N papers by score. Deterministic; rerun after scoring.
"""

import json
import re
from pathlib import Path

R = Path("research")
TOP_N = 30


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def row(s: dict, meta: dict) -> str:
    m = meta[s["arxiv"]]
    title = m["title"].replace("|", "\\|")
    code = f"[code]({s['code_url']})" if s.get("code_url") else ("✓" if s["code"] == "yes" else "announced" if s["code"] == "announced" else "—")
    if s.get("abstract_only"):
        return (f"| {m['published']} | **[{title}](https://arxiv.org/abs/{m['latest_version']})**<br>{s['title_zh']} "
                f"| [{s['sub_pattern']}](../patterns/sub/{s['sub_pattern']}.md) | not ranked<br><sub>abstract only, no HTML full text</sub> | {code} |")
    return (f"| {m['published']} | **[{title}](https://arxiv.org/abs/{m['latest_version']})**<br>{s['title_zh']}<br><sub>{s['one_line']}</sub> "
            f"| [{s['sub_pattern']}](../patterns/sub/{s['sub_pattern']}.md) | **{s['total']}** {s['band']}<br><sub>E{s['evidence']} X{s['execution']:.0f} L{s['level']} C{s['code']}</sub> | {code} |")


def gallery(readme: str, by_id: dict, meta: dict, per_row: int = 3) -> str:
    """README block <!-- REEL:START/END -->: poster thumbnails for every reel/<id>/ with a poster, best score first."""
    ids = sorted((p.parent.name for p in Path("reel").glob("*/poster.png") if p.parent.name in by_id),
                 key=lambda i: (-by_id[i]["total"], i))
    cells = [f'<td align="center" width="33%"><a href="reel/{i}/poster.pdf"><img src="reel/{i}/poster.png" width="100%"></a><br>'
             f'<sub><b>{meta[i]["title"].split(":")[0][:40]}</b> · {by_id[i]["total"]} {by_id[i]["band"]}<br>'
             f'<a href="reel/{i}/blog_zh.md">中文解读</a> · <a href="reel/{i}/blog_en.md">English</a> · '
             f'<a href="https://arxiv.org/abs/{meta[i]["latest_version"]}">paper</a></sub></td>' for i in ids]
    rows = ["<tr>" + "".join(cells[k:k + per_row]) + "</tr>" for k in range(0, len(cells), per_row)]
    block = "\n".join(["<!-- REEL:START -->", f"## Poster gallery ({len(ids)})", "",
                        "Posters and interpretations of top-scoring papers ([how they are made](reel/README.md)).", "",
                        "<table>", *rows, "</table>", "<!-- REEL:END -->"]) if ids else "<!-- REEL:START -->\n<!-- REEL:END -->"
    if "<!-- REEL:START -->" in readme:
        return re.sub(r"<!-- REEL:START -->.*?<!-- REEL:END -->", lambda _: block, readme, flags=re.S)
    return readme.replace("<!-- BOARD:START -->", block + "\n\n<!-- BOARD:START -->", 1)


def main() -> None:
    scores = sorted(jl(R / "scores.jsonl"), key=lambda s: (s.get("abstract_only", False), -s["total"], s["arxiv"]))
    meta = {r["arxiv"]: r for r in jl(R / "corpus.jsonl")}
    tax = json.loads((R / "patterns/taxonomy.json").read_text())
    head = "| Date | Paper | Sub-pattern | Score | Code |\n|---|---|---|---|---|"
    legend = ("Score (0–100) = **E**vidence (50) + e**X**ecution against the pattern card (30) + evidence **L**evel (10) + "
              "**C**ode (10); every judgment is quote-backed — see [SCORE_SPEC](../research/SCORE_SPEC.md). "
              "It measures what a paper reports and how it executes its move, not the value of the idea.")
    md = ["# Paper board", "", f"{len(scores)} computer-use agent papers scored. {legend}", ""]
    md += [f"- [{m['title']}](#{m['id'].replace('_', '-')})" for m in tax["main"]] + [""]
    for m in tax["main"]:
        rows = [s for s in scores if s["main_pattern"] == m["id"]]
        if not rows:
            continue
        md += [f'<a id="{m["id"].replace("_", "-")}"></a>', f"## {m['title']}", "",
               f"Pattern card: [{m['id']}](../patterns/main/{m['id']}.md) · {len(rows)} papers", "", head]
        md += [row(s, meta) for s in rows] + [""]
    Path("papers").mkdir(exist_ok=True)
    Path("papers/README.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    top = [s for s in scores if not s.get("abstract_only")][:TOP_N]
    block = ["<!-- BOARD:START -->", f"## Top {len(top)} papers by CUA Radar score", "",
             f"Out of {len(scores)} scored so far ({sum(s['band'] == '★★★' for s in scores)} at ★★★ ≥ 70). "
             f"Full board, grouped by pattern: [papers/](papers/README.md). {legend.replace('../', '')}", "",
             head.replace("Sub-pattern", "Pattern")]
    block += [row(s, meta).replace("](../", "](") for s in top]
    block.append("<!-- BOARD:END -->")
    readme = Path("README.md").read_text(encoding="utf-8")
    readme = gallery(readme, {s["arxiv"]: s for s in scores}, meta)
    if "<!-- BOARD:START -->" in readme:
        readme = re.sub(r"<!-- BOARD:START -->.*?<!-- BOARD:END -->", lambda _: "\n".join(block), readme, flags=re.S)  # lambda: titles may contain backslashes
    else:
        readme = readme.replace("## What is here", "\n".join(block) + "\n\n## What is here", 1)
    Path("README.md").write_text(readme, encoding="utf-8")
    print(f"board: {len(scores)} papers, {len(top)} top")


if __name__ == "__main__":
    main()
