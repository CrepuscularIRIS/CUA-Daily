"""Pull harness-RSI-like submissions from ICLR on OpenReview, INCLUDING rejected/withdrawn ones.

Awesome lists only keep papers curators liked, so they carry almost no Reject signal; ICLR makes
rejected submissions public, which gives RS-style Oral/Accept-vs-Reject contrast.
Needs OPENREVIEW_USER / OPENREVIEW_PASS (env, or --env file). Credentials are never printed or written.

Usage: python research/openreview_pull.py --env ~/competitor/ResearchStudio/ResearchStudio-Idea/.env
"""

import argparse
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api2.openreview.net"
VENUES = {  # venueid -> outcome label
    "ICLR.cc/2025/Conference": "accept", "ICLR.cc/2025/Conference/Rejected_Submission": "reject",
    "ICLR.cc/2025/Conference/Withdrawn_Submission": "withdrawn",
    "ICLR.cc/2026/Conference": "accept", "ICLR.cc/2026/Conference/Rejected_Submission": "reject",
    "ICLR.cc/2026/Conference/Withdrawn_Submission": "withdrawn",
    "ICLR.cc/2027/Conference/Submission": "pending",
}
# Recall-oriented: stage-1 screening decides A/B/C afterwards.
MATCH = re.compile(
    r"self-?improv|self-?evolv|self-?refin\w* agent|recursive self|harness|scaffold|meta-?agent|godel|gödel"
    r"|prompt optimi[sz]|program optimi[sz]|workflow (?:optimi[sz]|search|generation)|agentic workflow"
    r"|skill (?:librar|induction|discovery|learning)|agent (?:memory|experience)|experience (?:replay|library)"
    r"|context engineering|playbook|tool (?:creation|making)|automated (?:agent|design of agentic)"
    r"|evolutionary (?:search|coding)|code evolution|open-?ended (?:agent|evolution)",
    re.I,
)


def load_env(path: Path | None) -> None:
    if path and path.exists():
        for line in path.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip() in ("OPENREVIEW_USER", "OPENREVIEW_PASS") and k.strip() not in os.environ:
                os.environ[k.strip()] = v.strip().strip("\"'")


def call(path: str, token: str | None = None, body: dict | None = None) -> dict:
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json", "User-Agent": "cua-radar/0.1",
                                          **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", type=Path)
    ap.add_argument("--out", type=Path, default=Path("research/openreview_pull.jsonl"))
    args = ap.parse_args()
    load_env(args.env)
    try:
        token = call("/login", body={"id": os.environ["OPENREVIEW_USER"], "password": os.environ["OPENREVIEW_PASS"]})["token"]
    except KeyError as e:
        raise SystemExit(f"missing credential env var {e}") from None

    rows = []
    for venueid, outcome in VENUES.items():
        offset, seen, kept = 0, 0, 0
        while True:
            q = urllib.parse.urlencode({"content.venueid": venueid, "limit": 1000, "offset": offset,
                                        "select": "id,forum,content.title,content.abstract,content.venue,content.keywords"})
            notes = call(f"/notes?{q}", token).get("notes", [])
            for n in notes:
                c = n["content"]
                val = lambda k: (c.get(k) or {}).get("value") or ""
                kw = val("keywords")
                text = " ".join([val("title"), val("abstract"), " ".join(kw) if isinstance(kw, list) else kw])
                if MATCH.search(text):
                    rows.append({"forum": n["forum"], "title": val("title"), "abstract": val("abstract"),
                                 "venue": val("venue"), "venueid": venueid, "outcome": outcome})
                    kept += 1
            seen += len(notes)
            if len(notes) < 1000:
                break
            offset += 1000
            time.sleep(1)
        print(f"{venueid}: {seen} notes, {kept} matched", flush=True)
    args.out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} to {args.out}")


if __name__ == "__main__":
    main()
