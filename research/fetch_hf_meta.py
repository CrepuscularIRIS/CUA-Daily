"""Fetch Hugging Face Papers metadata (linked GitHub repo, stars, upvotes) → research/hf_meta.jsonl.

Code availability must not depend on whether a condensed full text happened to keep the footnote with the
repo link, so score.py resolves code from this file too. Re-run safely: fetched ids are skipped. HTTP 429 stops the
run with exit code 75 after one Retry-After wait (research/net.py); transient errors write nothing.

Usage: python research/fetch_hf_meta.py [--ids research/ab_ids.txt]
"""

import argparse
import json
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from net import RateLimited, get  # noqa: E402

EXIT_RATE_LIMITED = 75
PACE = 1.0  # huggingface.co API

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
                d = json.loads(get(API.format(id=aid), timeout=30, pace=PACE))
                rec = {"arxiv": aid, "github": d.get("githubRepo"), "stars": d.get("githubStars"), "upvotes": d.get("upvotes")}
            except RateLimited as e:
                print(f"{aid}: {e}; stopping, rerun later", flush=True)
                sys.exit(EXIT_RATE_LIMITED)
            except urllib.error.HTTPError as e:
                rec = {"arxiv": aid, "github": None, "stars": None, "upvotes": None, "http": e.code}
            except Exception as e:  # transient; rerun picks it up
                print(f"{aid}: {e!r}")
                continue
            f.write(json.dumps(rec) + "\n")
            f.flush()
    print("done")


if __name__ == "__main__":
    main()
