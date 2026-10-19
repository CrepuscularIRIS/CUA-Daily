"""Attach OpenReview outcome labels (oral/spotlight/poster/reject/withdrawn/...) to corpus papers.

This is the contrast signal RS's 15+31 cards are built on (Oral vs Reject vs high-cited).
Uses the public search endpoint, no login; titles are matched after normalization.

Usage: python research/openreview_labels.py --ids research/ab_ids.txt [--out research/openreview.jsonl]
"""

import argparse
import difflib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

SEARCH = "https://api2.openreview.net/notes/search?term={q}&limit=5"
PENDING_VENUE = re.compile(r"ICLR 2027 Conference Submission|Submitted to ICLR 2027")  # ponytail: bump each cycle; still-in-review ≠ reject


def norm(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


# Most informative record wins when a title matches several (DBLP/CoRR import + real submission)
PRIORITY = ["oral", "spotlight", "poster", "accept", "reject", "withdrawn", "pending", "workshop", "none"]


def label(venue: str) -> str:
    v = venue.lower()
    if not v or v.startswith("corr") or v == "crossref":
        return "none"  # arXiv mirror / metadata import, says nothing about peer review
    if "arr" in v.split() and "submission" in v:
        return "pending"  # ponytail: ACL Rolling Review submission; outcome lives elsewhere
    for key in ("withdrawn", "desk rejected", "oral", "spotlight", "poster"):
        if key in v:
            return key.replace("desk rejected", "reject")
    if PENDING_VENUE.search(venue):
        return "pending"
    if v.startswith("submitted to") or v.endswith("conference submission"):
        return "reject"
    if "workshop" in v or "workshop" in venue:
        return "workshop"
    return "accept"


def lookup(title: str) -> dict | None:
    url = SEARCH.format(q=urllib.parse.quote(title[:200]))
    req = urllib.request.Request(url, headers={"User-Agent": "cua-radar/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        notes = json.load(r).get("notes", [])
    matches = []
    for n in notes:
        c = n.get("content", {})
        cand = (c.get("title") or {}).get("value", "")
        if difflib.SequenceMatcher(None, norm(title), norm(cand)).ratio() >= 0.92:
            matches.append(n)
    if not matches:
        return None
    venue_of = lambda n: (n["content"].get("venue") or {}).get("value", "")
    best = min(matches, key=lambda n: PRIORITY.index(label(venue_of(n))))
    best_score = round(difflib.SequenceMatcher(None, norm(title), norm(best["content"]["title"]["value"])).ratio(), 3)
    venue = (best["content"].get("venue") or {}).get("value", "")
    return {"forum": best["forum"], "venue": venue,
            "venueid": (best["content"].get("venueid") or {}).get("value", ""),
            "label": label(venue), "title_match": round(best_score, 3)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", type=Path, required=True)
    ap.add_argument("--corpus", type=Path, default=Path("research/corpus.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("research/openreview.jsonl"))
    args = ap.parse_args()

    titles = {r["arxiv"]: r["title"] for r in map(json.loads, args.corpus.read_text().splitlines())}
    done = {}
    if args.out.exists():
        done = {r["arxiv"]: r for r in map(json.loads, args.out.read_text().splitlines())}
    ids = [i for i in args.ids.read_text().split() if i not in done and i in titles]
    with args.out.open("a") as f:
        for k, aid in enumerate(ids, 1):
            try:
                hit = lookup(titles[aid])
            except Exception as e:  # rate limit / transient: record and move on, rerun picks it up
                print(f"{aid}: {e!r}")
                time.sleep(20)
                continue
            f.write(json.dumps({"arxiv": aid, **(hit or {"label": "none"})}, ensure_ascii=False) + "\n")
            f.flush()
            time.sleep(1.2)
            if k % 50 == 0:
                print(f"{k}/{len(ids)}")
    print("done")


if __name__ == "__main__":
    assert label("ICLR 2026 Oral") == "oral" and label("Submitted to ICLR 2025") == "reject"
    assert label("ICLR 2026 Conference Withdrawn Submission") == "withdrawn"
    assert label("ICLR 2025 Conference Submission") == "reject"
    assert label("CoRR 2026") == label("") == "none" and label("ACL ARR 2026 May Submission") == "pending"
    assert label("Submitted to ICLR 2027") == label("ICLR 2027 Conference Submission") == "pending" and label("NeurIPS 2025 poster") == "poster"
    main()
