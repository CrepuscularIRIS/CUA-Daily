"""Find arXiv versions of OpenReview submissions by title, so full text comes from arXiv HTML
instead of rate-limited OpenReview PDFs. Writes research/or_arxiv_map.jsonl {or_id, arxiv, title_match}.

Usage: python research/or_to_arxiv.py
"""

import difflib
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"a": "http://www.w3.org/2005/Atom"}
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def search(title: str) -> tuple[str | None, float]:
    words = [w for w in norm(title).split() if len(w) > 2][:12]
    q = urllib.parse.quote(" AND ".join(f"ti:{w}" for w in words))
    with urllib.request.urlopen(f"https://export.arxiv.org/api/query?search_query={q}&max_results=5", timeout=60) as r:
        root = ET.fromstring(r.read())
    best, score = None, 0.0
    for e in root.findall("a:entry", NS):
        s = difflib.SequenceMatcher(None, norm(title), norm(e.findtext("a:title", "", NS))).ratio()
        if s > score:
            best, score = e.findtext("a:id", "", NS).rsplit("/", 1)[-1].split("v")[0], s
    return (best, score) if score >= 0.92 else (None, score)


def main() -> None:
    pull = {"or:" + p["forum"]: p for p in map(json.loads, Path("research/openreview_pull.jsonl").read_text().splitlines())}
    out = Path("research/or_arxiv_map.jsonl")
    done = {json.loads(l)["or_id"] for l in out.read_text().splitlines()} if out.exists() else set()
    with out.open("a") as f:
        for oid in Path("research/or_ab_ids.txt").read_text().split():
            if oid in done:
                continue
            try:
                aid, s = search(pull[oid]["title"])
            except Exception as e:  # transient API error: skip, rerun picks it up
                print(f"{oid}: {e!r}")
                time.sleep(10)
                continue
            f.write(json.dumps({"or_id": oid, "arxiv": aid, "title_match": round(s, 3)}) + "\n")
            f.flush()
            time.sleep(3)
    print("done")


if __name__ == "__main__":
    main()
