"""Build research/corpus.jsonl: every arXiv paper cited by the computer-use / GUI-agent lists in refs/lists/.

Each record keeps provenance (which list, which section heading) because the section a
curator filed a paper under is a cheap prior for screening (agent method vs benchmark vs off-topic).
Metadata comes from the arXiv export API (stdlib only). Re-run safely: cached ids are skipped.

Usage: python research/build_corpus.py [--lists refs/lists] [--out research/corpus.jsonl]
"""

import argparse
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_ID = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
API = "https://export.arxiv.org/api/query?max_results={n}&id_list={ids}"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
BATCH = 100


def harvest(lists_dir: Path) -> dict[str, list[dict]]:
    """arXiv id -> list of {list, section} where it was cited."""
    found: dict[str, list[dict]] = {}
    for repo in sorted(p for p in lists_dir.iterdir() if p.is_dir()):
        for md in sorted(repo.rglob("*.md")):
            path = []  # heading stack
            for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
                if m := HEADING.match(line):
                    level = len(m[1])
                    path = path[: level - 1] + [m[2].strip()]
                for aid in ARXIV_ID.findall(line):
                    src = {"list": repo.name, "section": " > ".join(path[-2:])}
                    if src not in found.setdefault(aid, []):
                        found[aid].append(src)
    osu = lists_dir / "GUI-Agents-Paper-List/papers.yaml"  # curated source of truth; its README omits some entries
    if osu.exists():
        import yaml
        for p in yaml.safe_load(osu.read_text(encoding="utf-8")) or []:
            for aid in ARXIV_ID.findall(f"arxiv.org/abs/{p.get('arxiv_id') or ''} {p.get('link') or ''}"):
                src = {"list": "GUI-Agents-Paper-List", "section": " > ".join(p.get("envs") or [])}
                if src not in found.setdefault(aid, []):
                    found[aid].append(src)
    return found


def fetch_metadata(ids: list[str]) -> dict[str, dict]:
    url = API.format(n=len(ids), ids=",".join(ids))
    req = urllib.request.Request(url, headers={"User-Agent": "cua-radar/0.1"})  # plain http times out from cloud boxes
    with urllib.request.urlopen(req, timeout=60) as r:
        root = ET.fromstring(r.read())
    out = {}
    for e in root.findall("a:entry", NS):
        full = e.findtext("a:id", "", NS).rsplit("/", 1)[-1]  # e.g. 2507.19457v2
        aid = full.split("v")[0]
        text = lambda tag, ns="a": " ".join((e.findtext(f"{ns}:{tag}", "", NS) or "").split())
        out[aid] = {
            "latest_version": full,
            "title": text("title"),
            "abstract": text("summary"),
            "published": text("published")[:10],
            "updated": text("updated")[:10],
            "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
            "primary_category": (e.find("x:primary_category", NS).get("term")
                                 if e.find("x:primary_category", NS) is not None else None),
            "comment": text("comment", "x") or None,
            "journal_ref": text("journal_ref", "x") or None,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lists", default="refs/lists", type=Path)
    ap.add_argument("--out", default="research/corpus.jsonl", type=Path)
    args = ap.parse_args()

    found = harvest(args.lists)
    cached = {}
    if args.out.exists():
        cached = {r["arxiv"]: r for r in map(json.loads, args.out.read_text().splitlines())}

    todo = sorted(a for a in found if a not in cached or "title" not in cached[a])
    meta = {}
    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        for attempt in range(3):
            try:
                meta.update(fetch_metadata(chunk))
                break
            except Exception as e:  # network/API hiccup: back off, then give up on this chunk
                print(f"batch {i}: {e!r}, retry {attempt + 1}/3")
                time.sleep(10 * (attempt + 1))
        time.sleep(3)  # arXiv API etiquette
        print(f"fetched {min(i + BATCH, len(todo))}/{len(todo)}")

    records = []
    for aid in sorted(found):
        rec = {"arxiv": aid, "sources": found[aid], "n_lists": len({s["list"] for s in found[aid]})}
        rec |= meta.get(aid) or {k: v for k, v in cached.get(aid, {}).items() if k not in rec}
        records.append(rec)
    args.out.parent.mkdir(exist_ok=True)
    args.out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    missing = sum("title" not in r for r in records)
    print(f"wrote {len(records)} records to {args.out} ({missing} without metadata)")


if __name__ == "__main__":
    main()
