#!/usr/bin/env python3
"""Create a batch directory (manifest + inputs listing) for a v2.2 run.

Usage: python3 research/v2/make_batch.py <run_id> <batch_id> <id> [<id> ...]
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "research" / "v2" / "runs"


def main() -> None:
    run_id, batch_id, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    run = RUNS / run_id
    manifest = json.loads((run / "manifest.json").read_text())
    mat = {}
    for line in open(ROOT / "research" / "fulltext" / "review-runs" / run_id / "materials.jsonl"):
        r = json.loads(line)
        # later lines win; "#rN" revision ids map back to the bare id (latest revision)
        key = r["arxiv"].split("#")[0]
        cur = mat.get(key)
        rev = lambda a: int(a.split("#r")[1]) if "#r" in a else 0
        if cur is None or rev(r["arxiv"]) >= rev(cur["arxiv"]):
            mat[key] = r

    corpus = {r["arxiv"]: r for r in map(json.loads, open(ROOT / "research" / "corpus.jsonl"))}
    papers = []
    for a in ids:
        m = mat.get(a)
        if m is None:
            sys.exit(f"{a}: no material record — fetch first")
        # revision records "id#rN" live in "id.rN.txt"
        mat_file = m["arxiv"].replace("#", ".")
        papers.append({
            "paper_key": a, "arxiv": a,
            "title": corpus[a]["title"], "version": corpus[a]["latest_version"],
            "fulltext_path": f"research/fulltext/review-runs/{run_id}/fulltext/{mat_file}.txt"
            if m["status"] == "html" else None,
            "material_status": m["status"], "material_sha256": m["sha256"],
        })

    bdir = run / "batches" / batch_id
    for seat in ("sol", "son55"):
        (bdir / "seats" / seat / "attempts" / "a1").mkdir(parents=True, exist_ok=True)
    (bdir / "aggregate" / "attempts" / "a1").mkdir(parents=True, exist_ok=True)
    bm = {
        "run_id": run_id, "batch_id": batch_id, "attempt": "a1",
        "papers": papers,
        "asset_hashes": manifest["assets"],
        "model_types": manifest["model_types"],
    }
    blob = json.dumps(bm, ensure_ascii=False, sort_keys=True)
    bm["input_bundle_sha256"] = hashlib.sha256(blob.encode()).hexdigest()
    (bdir / "manifest.json").write_text(json.dumps(bm, ensure_ascii=False, indent=1))
    print(f"batch {batch_id}: {len(papers)} papers, bundle {bm['input_bundle_sha256'][:12]}")


if __name__ == "__main__":
    main()
