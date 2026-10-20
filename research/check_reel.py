"""Gate for Reel outputs (reel/<arxiv_id>/). Exit 1 on any problem.

Checks per paper:
  - required files exist; poster.png ≤ 3 MB;
  - SOURCE.md names the exact paper version that was read ("Read from: arXiv <version>");
  - if the license forbids figure reuse, SOURCE.md says "Paper figures shown: none";
  - every decimal number in blog_en.md / blog_zh.md occurs in the paper's full text (tables included),
    unless it is marked with ‡ (= computed by us from paper numbers, explained in SOURCE.md).
The paper text is fetched from arXiv HTML (fallback: PDF via pdftotext) into research/paper_text/ (local only).

Usage: python3 research/check_reel.py [reel/<id> ...]      # default: every reel/<id>/ directory
"""

import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from net import RateLimited, get  # noqa: E402

CACHE = Path("research/paper_text")
REQUIRED = ["poster.png", "poster.pdf", "blog_zh.md", "blog_en.md", "SOURCE.md"]
DECIMAL = re.compile(r"(?<![\w./-])(\d{1,4}\.\d{1,3})(‡?)(?![\w/])")


def paper_text(version: str) -> str:
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / f"{version}.txt"
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    text = ""
    try:
        text = html.unescape(re.sub(r"<[^>]+>", " ", get(f"https://arxiv.org/html/{version}", timeout=90).decode("utf-8", "ignore")))
    except RateLimited:
        raise
    except Exception:
        if shutil.which("pdftotext"):
            with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
                f.write(get(f"https://arxiv.org/pdf/{version}", timeout=120))
                f.flush()
                text = subprocess.run(["pdftotext", "-q", f.name, "-"], capture_output=True, text=True).stdout
    text = re.sub(r"\s+", " ", text)
    if len(text) > 5000:
        cached.write_text(text, encoding="utf-8")
    return text


def check(d: Path, cand: dict) -> list[str]:
    errs = [f"missing {f}" for f in REQUIRED if not (d / f).exists()]
    if (d / "poster.png").exists() and (d / "poster.png").stat().st_size > 3 * 1024 * 1024:
        errs.append("poster.png > 3 MB")
    if d.name not in cand:
        return errs + ["not in reel/candidates.jsonl"]
    c = cand[d.name]
    src = (d / "SOURCE.md").read_text(encoding="utf-8") if (d / "SOURCE.md").exists() else ""
    if f"Read from: arXiv {c['version']}" not in src:
        errs.append(f"SOURCE.md must contain 'Read from: arXiv {c['version']}' (the paper itself must be read)")
    if not c["figure_reuse"] and "Paper figures shown: none" not in src:
        errs.append("license forbids figure reuse: SOURCE.md must contain 'Paper figures shown: none'")
    paper = paper_text(c["version"])
    if not paper:
        return errs + [f"could not fetch the text of {c['version']} to verify numbers"]
    for blog in ("blog_en.md", "blog_zh.md"):
        if not (d / blog).exists():
            continue
        body = re.sub(r"https?://\S+", "", (d / blog).read_text(encoding="utf-8"))
        bad = sorted({n for n, mark in DECIMAL.findall(body) if not mark and not re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", paper)})
        errs += [f"{blog}: {n} is not in the paper (fix it, or mark ‡ if computed and explain in SOURCE.md)" for n in bad]
    return errs


def main(argv: list[str]) -> int:
    cand = {r["arxiv"]: r for r in map(json.loads, Path("reel/candidates.jsonl").read_text().splitlines())}
    dirs = [Path(a) for a in argv] or sorted(p for p in Path("reel").iterdir() if p.is_dir() and re.fullmatch(r"\d{4}\.\d{4,5}", p.name))
    bad = 0
    for d in dirs:
        errs = check(d, cand)
        bad += bool(errs)
        print(f"{'FAIL' if errs else 'ok  '} {d}" + "".join(f"\n     - {e}" for e in errs))
    print(f"{len(dirs)} reel dirs, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    assert DECIMAL.findall("54.5% vs 52.0‡, v3 2605.29668 4.0/") == [("54.5", ""), ("52.0", "‡")]
    sys.exit(main(sys.argv[1:]))
