#!/usr/bin/env python3
"""Fetch complete (uncapped) arXiv HTML fulltext for a v2.2 run.

Writes research/fulltext/review-runs/<run_id>/fulltext/<id>.txt plus
materials.jsonl (sha256, url, status). 404 -> status no_html (needs_fulltext
path); transient errors write nothing so a rerun retries. Existing files with
matching content are skipped (resume).

Usage: python3 research/v2/fetch_full_v22.py <run_id> <id> [<id> ...]
"""
import hashlib
import urllib.error
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from net import RateLimited, get  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
URL = "https://arxiv.org/html/{arxiv}"
STRIP = ("script", "style", "noscript", "svg", "form")


def render(html: str) -> str:
    import base64
    soup = BeautifulSoup(html, "html.parser")
    for t in soup.find_all(STRIP):
        t.decompose()
    parts = []

    def listing_text(el) -> str:
        # LaTeXML stores long listings as data:text/plain;base64 links.
        for a in el.find_all("a", href=True):
            href = a["href"]
            pre = "data:text/plain;base64,"
            if href.startswith(pre):
                try:
                    return base64.b64decode(href[len(pre):]).decode("utf-8", errors="replace").strip()
                except Exception:  # noqa: BLE001 — malformed data URI falls back to text
                    break
        return el.get_text("\n", strip=True)

    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "figcaption", "table",
                             "div", "pre"]):
        cls = el.get("class") or []
        if "ltx_listing" in cls and el.name == "div":
            # only outermost listing divs; nested ones would duplicate content
            if any(p.name == "div" and "ltx_listing" in (p.get("class") or [])
                   for p in el.parents):
                continue
            text = listing_text(el)
            if text:
                parts.append("```\n" + text + "\n```")
            continue
        if el.name == "table":
            rows = []
            for tr in el.find_all("tr"):
                cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
                if any(cells):
                    rows.append(" | ".join(cells))
            text = "\n".join(rows)
        elif el.name == "pre":
            text = el.get_text("\n", strip=True)
        else:
            # skip paragraphs nested inside listings already captured
            if any(p.name == "div" and "ltx_listing" in (p.get("class") or [])
                   for p in el.parents):
                continue
            text = el.get_text(" ", strip=True)
        if text:
            prefix = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "li": "- "}.get(el.name, "")
            parts.append(prefix + text)
    return "\n\n".join(parts)


def main() -> None:
    run_id, ids = sys.argv[1], sys.argv[2:]
    corpus = {}
    cpath = ROOT / "research" / "corpus.jsonl"
    if cpath.exists():
        for line in open(cpath):
            r = json.loads(line)
            corpus[r["arxiv"]] = r.get("latest_version")
    out_dir = ROOT / "research" / "fulltext" / "review-runs" / run_id / "fulltext"
    out_dir.mkdir(parents=True, exist_ok=True)
    mat_path = out_dir.parent / "materials.jsonl"
    done = {}
    if mat_path.exists():
        for line in open(mat_path):
            r = json.loads(line)
            done[r["arxiv"]] = r

    for a in ids:
        ver = corpus.get(a)
        vurl = URL.format(arxiv=ver) if ver and ver != a else None  # e.g. 2501.04575v1
        url = vurl or URL.format(arxiv=a)
        f = out_dir / f"{a}.txt"
        no_html = False
        try:
            body = get(url)
        except RateLimited as e:
            print(f"{a}: RATE-LIMITED ({e}) — stop here, rerun to resume", file=sys.stderr)
            sys.exit(75)
        except urllib.error.HTTPError as e:
            if e.code == 404 and vurl:
                # versioned render missing; fall back to the unversioned one
                try:
                    url = URL.format(arxiv=a)
                    body = get(url)
                except Exception as e2:  # noqa: BLE001
                    if isinstance(e2, urllib.error.HTTPError) and e2.code == 404:
                        body, no_html = None, True
                    else:
                        print(f"{a}: fallback error {e2!r} — not cached", file=sys.stderr)
                        continue
            elif e.code == 404:
                body, no_html = None, True
            else:
                print(f"{a}: HTTP {e.code} — not cached, rerun retries", file=sys.stderr)
                continue
        except Exception as e:  # noqa: BLE001 — any transport error: skip, rerun retries
            print(f"{a}: transient error {e!r} — not cached", file=sys.stderr)
            continue
        if no_html:
            rec = {"arxiv": a, "url": url, "status": "no_html",
                   "sha256": None, "bytes": 0}
        else:
            text = render(body)
            head = f"SOURCE: {url}\nFETCHED: 2026-10-21 (v2.2 uncapped render)\n\n"
            blob = head + text + "\n"
            # never overwrite an existing material: a frozen batch may still point at it.
            target = f
            n = 1
            while target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(blob.encode()).hexdigest():
                n += 1
                target = out_dir / f"{a}.r{n}.txt"
            if target is not f:
                a = f"{a}#r{n}"  # materials.jsonl records the revision id
            target.write_text(blob)
            rec = {"arxiv": a, "url": url, "status": "html",
                   "sha256": hashlib.sha256(blob.encode()).hexdigest(), "bytes": len(blob)}
        done[a] = rec
        with open(mat_path, "a") as mf:
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{a}: {rec['status']} {rec['bytes']}B")


if __name__ == "__main__":
    main()
