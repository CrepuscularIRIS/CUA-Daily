"""Deterministic part of adding new papers: dedup → arXiv metadata → corpus → full text → HF code metadata → queue.

New ids go to a new file research/queue/YYYY-MM-DD-HHMM.txt (UTC) per run — the hand-off unit the scorer consumes
whole. A queue file is never appended to after it is written.

Corpus rows and the queue file are written only after full text and HF metadata have been fetched, so an interrupted
run (HTTP 429 → exit 75, crash, Ctrl-C) leaves no partial hand-off: recovery is rerunning the same command later.
Files already fetched are skipped on the rerun.

Reads arXiv ids from inbox files (inbox/*.jsonl, one {"arxiv": "...", ...} per line, written by the collector) or
from the command line, and prints the LLM steps that remain for each new paper (screen → assign →
judge), so a maintainer agent knows exactly what to do next.

Usage:
  python research/ingest.py inbox/2026-10-20.jsonl      # or: python research/ingest.py 2610.12345 2610.23456
"""

import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_corpus import fetch_metadata  # noqa: E402
from net import RateLimited  # noqa: E402

R = Path("research")
ARXIV = re.compile(r"(\d{4}\.\d{4,5})")
EXIT_RATE_LIMITED = 75


def requested(args: list[str]) -> list[str]:
    ids = []
    for a in args:
        p = Path(a)
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip() and (m := ARXIV.search(json.loads(line).get("arxiv", "") or json.loads(line).get("url", ""))):
                    ids.append(m.group(1))
        elif m := ARXIV.search(a):
            ids.append(m.group(1))
    return list(dict.fromkeys(ids))


def main(argv: list[str]) -> int:
    corpus_path = R / "corpus.jsonl"
    corpus = {json.loads(l)["arxiv"] for l in corpus_path.read_text().splitlines()}
    new = [i for i in requested(argv) if i not in corpus]
    if not new:
        print("nothing new")
        return 0
    meta = {}
    try:
        for i in range(0, len(new), 100):
            meta.update(fetch_metadata(new[i : i + 100]))  # net.get paces requests ≥ 3 s apart
    except RateLimited as e:
        print(f"{e}; nothing written, rerun later")
        return EXIT_RATE_LIMITED
    added = [a for a in new if a in meta]
    rows = [json.dumps({"arxiv": a, "sources": [{"list": "inbox", "section": ""}], "n_lists": 0, **meta[a]},
                       ensure_ascii=False) + "\n" for a in added]
    with tempfile.TemporaryDirectory() as tmp:
        ids_file, staged = Path(tmp) / "ids.txt", Path(tmp) / "corpus.jsonl"
        ids_file.write_text("".join(f"{a}\n" for a in added))
        staged.write_text("".join(rows))
        for cmd in (["fetch_fulltext.py", "--ids", str(ids_file), "--corpus", str(staged)],
                    ["fetch_hf_meta.py", "--ids", str(ids_file)]):
            rc = subprocess.run([sys.executable, str(R / cmd[0]), *cmd[1:]]).returncode
            if rc:
                print(f"{cmd[0]} exited {rc}; corpus and queue untouched, rerun this command later")
                return rc
    with corpus_path.open("a") as f:
        f.writelines(rows)
    queue = R / "queue" / f"{time.strftime('%Y-%m-%d-%H%M', time.gmtime())}.txt"  # one immutable hand-off file per run
    queue.parent.mkdir(exist_ok=True)
    if added:
        with queue.open("x") as q:  # "x": refuse to append to an existing file
            q.write("".join(f"{a}\n" for a in added))
    print(f"\nadded {len(added)} papers to corpus ({len(new) - len(added)} ids not found on arXiv); queued in {queue}")
    print("Remaining LLM steps per paper (see docs/PIPELINE.md):")
    for aid in added:
        print(f"  {aid}  {meta[aid]['title'][:70]}\n    1 screen → research/screen.jsonl"
              f"  2 assign → research/patterns/assign_<B>.jsonl  3 judge → research/judgments/<B>.jsonl"
              f"  (docs/agents/JUDGE_BATCH.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
