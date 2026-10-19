"""Fetch ICLR reviews / meta-review / decision for contrast-set papers into research/reviews/<id>.json.

Reviews are what RS's "failure modes" and "reviewer expectations" panels are distilled from.
Kept local (gitignored); only derived, paraphrased artifacts get committed.
On HTTP 429 it waits exactly Retry-After (max 3 times), then gives up; finished forums are skipped on rerun.

Usage: python research/fetch_reviews.py --env <.env>
"""

import argparse
import json
import os
import time
import urllib.error
from pathlib import Path

from openreview_pull import call, load_env

KEEP = ("summary", "strengths", "weaknesses", "questions", "rating", "confidence", "soundness",
        "contribution", "metareview", "decision", "justification_for_why_not_higher_score",
        "justification_for_why_not_lower_score", "additional_comments_on_reviewer_discussion")


def targets() -> dict[str, str]:
    """id used in our files -> OpenReview forum id, for every ICLR-labeled paper in the contrast set."""
    out = {oid: oid.split(":", 1)[1] for oid in Path("research/or_ab_ids.txt").read_text().split()}
    for r in map(json.loads, Path("research/openreview.jsonl").read_text().splitlines()):
        if r.get("forum") and r.get("venueid", "").startswith("ICLR.cc/") and r["label"] != "pending":
            out[r["arxiv"]] = r["forum"]
    return out


def condense(notes: list[dict]) -> list[dict]:
    rows = []
    for n in notes:
        kind = (n.get("invitations") or [""])[0].rsplit("/", 1)[-1]
        if kind in ("Official_Review", "Meta_Review", "Decision"):
            c = {k: (v or {}).get("value") for k, v in n["content"].items() if k in KEEP}
            rows.append({"kind": kind, **c})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", type=Path)
    ap.add_argument("--out", type=Path, default=Path("research/reviews"))
    args = ap.parse_args()
    load_env(args.env)
    args.out.mkdir(exist_ok=True)
    try:
        token = call("/login", body={"id": os.environ["OPENREVIEW_USER"], "password": os.environ["OPENREVIEW_PASS"]})["token"]
        todo = {k: f for k, f in targets().items() if not (args.out / f"{k.replace(':', '_')}.json").exists()}
        print(f"{len(todo)} forums to fetch", flush=True)
        for i, (key, forum) in enumerate(todo.items(), 1):
            for wait in range(4):  # authenticated limit is 500 req / 3600 s sliding window; honor Retry-After
                try:
                    notes = call(f"/notes?forum={forum}&limit=200", token).get("notes", [])
                    break
                except urllib.error.HTTPError as e:
                    if e.code != 429 or wait == 3:
                        raise
                    secs = int(e.headers.get("Retry-After", "600")) + 5
                    print(f"429: waiting {secs}s", flush=True)
                    time.sleep(secs)
            (args.out / f"{key.replace(':', '_')}.json").write_text(
                json.dumps({"id": key, "forum": forum, "notes": condense(notes)}, ensure_ascii=False))
            time.sleep(6)
            if i % 25 == 0:
                print(i, flush=True)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise SystemExit("rate limited (429): stopping; rerun later to resume") from None
        raise
    print("done")


if __name__ == "__main__":
    main()
