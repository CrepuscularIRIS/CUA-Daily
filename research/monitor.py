"""Hourly health check of the agent-maintained repo. Read-only: reports, never commits.

Checks every commit since the last run (state in .git/monitor_last):
  - file ownership by commit prefix (collect/ingest/maintenance = Grok, triage/score/cards = Dots, reel = Reel);
  - no agent touches the judging standards; nobody commits full texts, reviews, bundles or .env;
  - Dots edits README.md only inside the board and poster-gallery blocks;
  - new reel/<id>/ directories pass research/check_reel.py;
  - new judgment files re-verified here (quotes checked against freshly fetched full text) and scores.jsonl reproducible;
  - card checks, latest CI run, open issues, queue backlog.
Prints a report ending in "STATUS OK" or "STATUS ATTENTION".

Usage: python3 research/monitor.py [--since <sha>]
"""

import datetime as dt
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

STATE = Path(".git/monitor_last")
REPO = "CrepuscularIRIS/cua-architecture-radar"  # assumed name; confirm when the repo is published
OWN = {
    "grok": ["inbox/*", "research/corpus.jsonl", "research/hf_meta.jsonl", "research/queue/*.txt",
             "research/patterns/contrast.json", "research/patterns/contrast.md"],
    "dots": ["research/screen.jsonl", "research/signatures.jsonl", "research/patterns/assignments.jsonl",
             "research/judgments/*", "research/scores.jsonl", "papers/README.md", "README.md", "cards/*",
             "research/queue/*.txt", "research/queue/done/*", "reel/*"],
}
# Human commits must not use these prefixes (use feat:/fix:/docs:/chore:), or they are checked as agent commits.
ROLE = {"collect": "grok", "ingest": "grok", "maintenance": "grok", "triage": "dots", "score": "dots", "cards": "dots", "reel": "dots"}
PROTECTED = ["docs/EVIDENCE.md", "cards/_TEMPLATE.md", "check_cards.py", ".github/*", "research/*_SPEC.md",
             "research/*_SCHEMA.md", "research/SCREEN_RUBRIC.md", "research/score.py", "research/check_*.py",
             "research/calibrate.py", "research/patterns/taxonomy*.json", "research/patterns/conditions.json", "patterns/*",
             "research/setup_reel.sh"]
FORBIDDEN = ["research/fulltext/*", "research/reviews/*", "research/patterns/bundles/*", "research/paper_text/*", "*.env", ".env",
             "*.pptx", "*.mp3", "*.docx", "*/poster.html"]
BOARD = re.compile(r"<!-- (BOARD|REEL):START -->.*?<!-- \1:END -->", re.S)


def sh(*cmd: str, check: bool = True) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(cmd)}: {r.stderr.strip()[:300]}")
    return r.stdout


def match(path: str, pats: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, p) for p in pats)


def commit_issues(sha: str, subject: str) -> list[str]:
    role = ROLE.get(subject.split(":", 1)[0].strip())
    files = []
    for line in sh("git", "show", "--name-status", "--format=", "-M", sha).splitlines():
        parts = line.split("\t")
        files += parts[1:]  # rename lines carry old and new path
    out = [f"{sha[:7]} commits forbidden path {f}" for f in files if match(f, FORBIDDEN)]
    if role:
        out += [f"{sha[:7]} ({role}) touches protected {f}" for f in files if match(f, PROTECTED)]
        out += [f"{sha[:7]} ({role}) outside its files: {f}" for f in files if not match(f, OWN[role]) and not match(f, PROTECTED)]
        if role == "dots" and "README.md" in files:
            before = sh("git", "show", f"{sha}^:README.md", check=False)
            after = sh("git", "show", f"{sha}:README.md")
            if BOARD.sub("", before) != BOARD.sub("", after):
                out.append(f"{sha[:7]} (dots) edits README.md outside the board/gallery blocks")
    return out


def main(argv: list[str]) -> int:
    report, problems = [], []
    sh("git", "fetch", "-q", "origin")
    head = sh("git", "rev-parse", "origin/main").strip()
    since = argv[argv.index("--since") + 1] if "--since" in argv else (STATE.read_text().strip() if STATE.exists() else head)
    commits = [l.split(" ", 1) for l in sh("git", "log", "--reverse", "--format=%H %s", f"{since}..{head}").splitlines()]
    report.append(f"new commits: {len(commits)}" + "".join(f"\n  {c[:7]} {s}" for c, s in commits))
    for c, s in commits:
        problems += commit_issues(c, s)
        for f in sh("git", "show", "--name-status", "--format=", c).splitlines():  # queue files are immutable once written
            st, *paths = f.split("\t")
            if st == "M" and fnmatch.fnmatch(paths[0], "research/queue/*.txt"):
                problems.append(f"{c[:7]} modifies existing queue file {paths[0]} (queue files are write-once)")
            if st == "M" and re.fullmatch(r"research/judgments/[^/]+\.jsonl", paths[0]) and ROLE.get(s.split(":", 1)[0].strip()):
                problems.append(f"{c[:7]} rewrites published judgment batch {paths[0]} (re-judgments go in a new batch)")

    sh("git", "merge", "--ff-only", "-q", "origin/main", check=False)
    if sh("git", "rev-parse", "HEAD").strip() != head:
        problems.append("local main cannot fast-forward to origin/main; validators ran on a stale tree")

    # independent re-verification of new judgments
    changed = {f for c, _ in commits for f in sh("git", "show", "--name-only", "--format=", c).split()}
    for jf in sorted(f for f in changed if re.fullmatch(r"research/judgments/(?!ids_).+\.jsonl", f) and Path(f).exists()):
        ids = Path(jf).with_name(f"ids_{Path(jf).stem}.txt")
        if ids.exists():
            sh(sys.executable, "research/fetch_fulltext.py", "--ids", str(ids), check=False)
            r = subprocess.run([sys.executable, "research/score.py", "check", jf, str(ids)], capture_output=True, text=True,
                               env={"PYTHONPATH": "research", "PATH": "/usr/bin:/bin"})
            last = (r.stdout.strip().splitlines() or ["?"])[-1]
            report.append(f"re-verify {jf}: {last}")
            if r.returncode:
                problems.append(f"{jf} fails independent quote check: {last}")
    if any(f in changed for f in ("research/scores.jsonl",)) or any("research/judgments/" in f for f in changed):
        subprocess.run([sys.executable, "research/score.py", "build"], capture_output=True, env={"PYTHONPATH": "research", "PATH": "/usr/bin:/bin"})
        if sh("git", "diff", "--name-only", "research/scores.jsonl").strip():
            problems.append("research/scores.jsonl is not reproducible from the committed judgments")
        sh("git", "checkout", "-q", "research/scores.jsonl")

    reel_dirs = sorted({str(Path(f).parent) for f in changed if re.fullmatch(r"reel/\d{4}\.\d{4,5}/[^/]+", f) and Path(f).parent.exists()})
    if reel_dirs:
        r = subprocess.run([sys.executable, "research/check_reel.py", *reel_dirs], capture_output=True, text=True)
        report.append("reel check: " + (r.stdout.strip().splitlines() or ["?"])[-1])
        if r.returncode:
            problems.append("new posters fail research/check_reel.py: " + "; ".join(l.strip() for l in r.stdout.splitlines() if l.strip().startswith("-"))[:400])
    for cmd in (["python3", "test_check_cards.py"], ["python3", "check_cards.py"]):
        if subprocess.run(cmd, capture_output=True).returncode:
            problems.append(f"{' '.join(cmd)} fails")

    runs = json.loads(sh("gh", "run", "list", "-R", REPO, "--limit", "1", "--json", "conclusion,status,displayTitle", check=False) or "[]")
    if runs:
        report.append(f"CI: {runs[0]['status']} {runs[0]['conclusion'] or ''} — {runs[0]['displayTitle'][:60]}")
        if runs[0]["conclusion"] not in ("success", "", None):
            problems.append(f"latest CI run: {runs[0]['conclusion']}")
    issues = json.loads(sh("gh", "issue", "list", "-R", REPO, "--state", "open", "--json", "number,title", check=False) or "[]")
    report.append("open issues: " + (", ".join(f"#{i['number']} {i['title']}" for i in issues) or "none"))
    problems += [f"open issue #{i['number']}: {i['title']}" for i in issues]

    today = dt.date.today()
    for q in sorted(Path("research/queue").glob("*.txt")):
        n = len(q.read_text().split())
        age = (today - dt.date.fromisoformat(q.stem[:10])).days if re.match(r"\d{4}-\d{2}-\d{2}", q.stem) else 0
        report.append(f"queue {q.name}: {n} ids, {age} days old")
        if age >= 2 and n:
            problems.append(f"queue {q.name} unprocessed for {age} days")

    scored = sum(1 for _ in Path("research/scores.jsonl").open()) if Path("research/scores.jsonl").exists() else 0
    cand = [json.loads(l) for l in Path("reel/candidates.jsonl").open()] if Path("reel/candidates.jsonl").exists() else []
    done = sum(c.get("status") == "done" for c in cand)
    queued = sum(len(q.read_text().split()) for q in Path("research/queue").glob("*.txt"))
    report.append(f"progress: {scored} papers on the board · {queued} ids waiting in queue · posters {done}/{len(cand)}")
    STATE.write_text(head)
    print("\n".join(report))
    print("\n".join(f"! {p}" for p in problems))
    print("STATUS", "ATTENTION" if problems else "OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
