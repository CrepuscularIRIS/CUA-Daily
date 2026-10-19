"""Fetch OpenReview PDFs for screened A/B submissions and write research/fulltext/or_<forum>.txt.

Same file format as fetch_fulltext.py so signature extractors treat both alike. PDF text is cut at
the references and capped; no section parsing (pdftotext layout varies too much to be worth it).
Needs OPENREVIEW_USER / OPENREVIEW_PASS (env or --env). Requires `pdftotext` (poppler).

Usage: python research/fetch_openreview_pdf.py --env <.env> [--ids research/or_ab_ids.txt]
"""

import argparse
import json
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from openreview_pull import API, call, load_env  # same dir; run from repo root with research/ on path

CAP = 26000
# Outcome leaks: camera-ready vs review headers would tell extractors the label. ponytail: author lists still differ (anonymous vs named).
HEADER = re.compile(r"^.*(?:Published as a conference paper|Under review as a conference paper|Accepted at|Submitted to).*$", re.M | re.I)
REFS = re.compile(r"\n\s*(REFERENCES|References|Bibliography)\s*\n")


def pdf_text(data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        out = subprocess.run(["pdftotext", "-q", f.name, "-"], capture_output=True, text=True, timeout=120).stdout
    out = HEADER.sub("", REFS.split(out, maxsplit=1)[0])
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", out)).strip()


def main() -> None:
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", type=Path)
    ap.add_argument("--ids", type=Path, default=Path("research/or_ab_ids.txt"))
    ap.add_argument("--pull", type=Path, default=Path("research/openreview_pull.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("research/fulltext"))
    args = ap.parse_args()
    load_env(args.env)
    token = call("/login", body={"id": os.environ["OPENREVIEW_USER"], "password": os.environ["OPENREVIEW_PASS"]})["token"]
    meta = {"or:" + p["forum"]: p for p in map(json.loads, args.pull.read_text().splitlines())}
    for k, oid in enumerate(args.ids.read_text().split(), 1):
        dest = args.out / f"{oid.replace(':', '_')}.txt"
        if dest.exists():
            continue
        m = meta[oid]
        head = f"# {m['title']}\nOpenReview {m['forum']}\n\n## Abstract\n{m['abstract']}\n\n"
        body = ""
        for attempt in range(6):
            try:
                req = urllib.request.Request(f"{API}/pdf?id={m['forum']}", headers={"Authorization": f"Bearer {token}",
                                                                                  "User-Agent": "cua-radar/0.1"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = pdf_text(r.read())[:CAP]
                break
            except urllib.error.HTTPError as e:
                if e.code != 429:  # missing PDF etc.: abstract-only file, extractor keeps evidence unclear
                    print(f"{oid}: {e!r}")
                    break
                time.sleep(60 * (attempt + 1))  # rate limited: back off, never write a degraded file for a 429
            except Exception as e:
                print(f"{oid}: {e!r}")
                break
        else:
            print(f"{oid}: still rate-limited, skipped (rerun to retry)")
            continue
        tag = "FULLTEXT: pdf" if len(body) > 2000 else "FULLTEXT: none (abstract only; keep evidence fields unclear)"
        dest.write_text(f"{tag}\n{head}## Body\n{body}\n", encoding="utf-8")
        time.sleep(5)
        if k % 25 == 0:
            print(f"{k}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
