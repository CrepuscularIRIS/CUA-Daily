"""Fetch arXiv HTML full text for A/B papers and keep the sections signature extraction needs.

Writes research/fulltext/<id>.txt (abstract + capped intro/method/experiments/limitations).
Papers without an HTML rendering get abstract-only files marked `FULLTEXT: none`, so
extractors know their evidence fields must stay `unclear`. Only HTTP 404 (no HTML rendering) is cached that way:
a transient error writes nothing (a rerun retries it), and HTTP 429 stops the run with exit code 75 after one
Retry-After wait (research/net.py). Re-run safely: existing files are skipped.

Usage: python research/fetch_fulltext.py --ids research/ab_ids.txt
"""

import argparse
import json
import re
import sys
import urllib.error
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from net import RateLimited, get  # noqa: E402

EXIT_RATE_LIMITED = 75  # EX_TEMPFAIL

URL = "https://arxiv.org/html/{id}"
# section class -> cumulative char cap. Related-work sections are dropped; any section that is not
# intro / experiments / limitations counts as method (method sections are usually titled by the method's name).
DROP = re.compile(r"related|background|preliminar|acknowledg|appendix|reference", re.I)
CLASSES = [
    ("intro", re.compile(r"intro", re.I), 5000),
    ("exp", re.compile(r"experiment|evaluation|result|setup|analysis|ablation|benchmark", re.I), 18000),
    ("lim", re.compile(r"limitation|discussion|conclusion|broader|future", re.I), 3000),
    ("method", re.compile(r""), 11000),
]
TOTAL_CAP = 40000  # ≈10k tokens; result tables are kept (baselines, budgets and variance live there)


def sections(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select(".ltx_bibliography, figure.ltx_figure, .ltx_note"):
        tag.decompose()
    for tag in soup.select("math"):  # numbers like 45.2% or ±1.3 are often MathML: keep their TeX alttext
        tag.replace_with(f" {tag.get('alttext', '')} ")
    out = []
    for sec in soup.select("section.ltx_section"):
        h = sec.find(["h2", "h3"])
        title = " ".join(h.get_text(" ").split()) if h else ""
        body = " ".join(sec.get_text(" ").split())
        out.append((title, body[len(title):].strip()))
    return out


def condense(secs: list[tuple[str, str]]) -> str:
    spent: dict[str, int] = {}
    parts, total = [], 0
    for title, body in secs:
        if DROP.search(title):
            continue
        name, cap = next((n, c) for n, pat, c in CLASSES if pat.search(title))
        budget = min(cap - spent.get(name, 0), TOTAL_CAP - total)
        if budget <= 500:
            continue
        chunk = body[:budget]
        parts.append(f"## {title}\n{chunk}{' [...]' if len(body) > budget else ''}")
        spent[name] = spent.get(name, 0) + len(chunk)
        total += len(chunk)
    return "\n\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", type=Path, required=True)
    ap.add_argument("--corpus", type=Path, default=Path("research/corpus.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("research/fulltext"))
    args = ap.parse_args()
    args.out.mkdir(exist_ok=True)
    meta = {r["arxiv"]: r for r in map(json.loads, args.corpus.read_text().splitlines())}
    ids = [i for i in args.ids.read_text().split() if not (args.out / f"{i}.txt").exists()]
    skipped = []
    for k, aid in enumerate(ids, 1):
        m = meta[aid]
        head = f"# {m['title']}\narXiv {m['latest_version']} | {m['published']}\n\n## Abstract\n{m['abstract']}\n\n"
        try:
            body = condense(sections(get(URL.format(id=m["latest_version"])).decode("utf-8", "ignore")))
        except RateLimited as e:
            print(f"{aid}: {e}; stopping — {len(ids) - k + 1} ids left, rerun later", flush=True)
            sys.exit(EXIT_RATE_LIMITED)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print(f"{aid}: {e!r}; not cached, rerun retries it")
                skipped.append(aid)
                continue
            body = ""  # 404 = arXiv has no HTML rendering of this version
        except Exception as e:  # timeout, connection reset, parse error: transient, not cached
            print(f"{aid}: {e!r}; not cached, rerun retries it")
            skipped.append(aid)
            continue
        tag = "FULLTEXT: html" if body else "FULLTEXT: none (abstract only; keep evidence fields unclear)"
        (args.out / f"{aid}.txt").write_text(f"{tag}\n{head}{body}\n", encoding="utf-8")
        if k % 50 == 0:
            print(f"{k}/{len(ids)}", flush=True)
    if skipped:
        print(f"{len(skipped)} ids not fetched (transient errors): {' '.join(skipped)}")
    print("done")


if __name__ == "__main__":
    main()
