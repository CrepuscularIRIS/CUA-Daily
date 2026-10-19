"""Fetch Hugging Face Papers metadata (linked GitHub repo, stars, upvotes) → research/hf_meta.jsonl.

Code availability must not depend on whether a condensed full text happened to keep the footnote with the
repo link, so score.py resolves code from this file too. Re-run safely: fetched ids are skipped.

Usage: python research/fetch_hf_meta.py [--ids research/ab_ids.txt]
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://huggingface.co/api/papers/{id}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", type=Path, default=Path("research/ab_ids.txt"))
    ap.add_argument("--out", type=Path, default=Path("research/hf_meta.jsonl"))
    args = ap.parse_args()
    done = {json.loads(l)["arxiv"] for l in args.out.read_text().splitlines()} if args.out.exists() else set()
    with args.out.open("a") as f:
        for aid in (i for i in args.ids.read_text().split() if i not in done and not i.startswith("or:")):
            try:
                with urllib.request.urlopen(urllib.request.Request(API.format(id=aid), headers={"User-Agent": "cua-radar/0.1"}), timeout=30) as r:
                    d = json.load(r)
                rec = {"arxiv": aid, "github": d.get("githubRepo"), "stars": d.get("githubStars"), "upvotes": d.get("upvotes")}
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(60)
                    continue  # rerun picks it up
                rec = {"arxiv": aid, "github": None, "stars": None, "upvotes": None, "http": e.code}
            except Exception as e:  # transient; rerun picks it up
                print(f"{aid}: {e!r}")
                continue
            f.write(json.dumps(rec) + "\n")
            f.flush()
            time.sleep(0.7)
    print("done")


if __name__ == "__main__":
    main()
