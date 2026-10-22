#!/usr/bin/env python3
"""Initialize a v2.2 scoring run: manifest + queue + calibration plan.

Usage: python3 research/v2/init_run.py <run_id>
Idempotent per run_id: refuses to overwrite an existing run directory.
"""
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "research" / "v2"
SEED = 42

# Frozen asset files recorded in the manifest (path -> role).
ASSETS = {
    "research/corpus.jsonl": "corpus",
    "research/SCORE_SPEC.md": "rubric",
    "research/PATTERN_PROTOCOL.md": "pattern_protocol",
    "research/BATCH_CONTRACT.md": "batch_contract",
    "research/REVIEW_WORKSHEET.md": "review_worksheet",
    "docs/EVIDENCE.md": "evidence_rules",
    "research/reference/researchstudio-15-31/MANIFEST.tsv": "rs_cards_manifest",
    "research/patterns/taxonomy.json": "domain_taxonomy",
    "research/patterns/conditions.json": "domain_conditions",
    ".forge/domains/cua-agents/v1/profile/expectations.json": "expectations",
}

# Agent-tool model slots as configured in this claude-kimi environment.
MODEL_TYPES = {
    "controller": "opus (glm-5.3[1m], this session)",
    "sol": "sonnet (upstream gpt-6.1-sol)",
    "son55": "haiku (upstream recorded as claude-sonnet-5-5 by the 2026-10-21 "
             "reset notes; actual upstream self-reported per worker)",
    "opus55": "fable (upstream claude-opus-5-5[1m])",
    "reel": "opus (upstream glm-5.3[1m]), selected papers only",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    run_id = sys.argv[1]
    run_dir = V2 / "runs" / run_id
    if run_dir.exists():
        sys.exit(f"run dir exists: {run_dir}")

    screen = {r["arxiv"]: r for r in map(json.loads, open(ROOT / "research/screen.jsonl"))}
    corpus = {r["arxiv"]: r for r in map(json.loads, open(ROOT / "research/corpus.jsonl"))}
    ft_dir = ROOT / "research" / "fulltext"
    indexed = {p.stem for p in ft_dir.glob("*.txt")}
    assigned = {json.loads(l)["arxiv"] for l in open(ROOT / "research/patterns/assignments.jsonl")}

    def render_status(a: str) -> str:
        head = (ft_dir / f"{a}.txt").read_text(errors="replace")[:20]
        if "FULLTEXT: html" in head:
            return "html"
        if "FULLTEXT: none" in head:
            return "none"
        return "other"

    tier_a = sorted(a for a in screen if screen[a]["tier"] == "A")
    tier_b = sorted(a for a in screen if screen[a]["tier"] == "B")
    queue_ids = tier_a + tier_b  # screen tiers are queue hints only, not judgments

    rng = random.Random(SEED)

    def pick(cands: list[str], n: int) -> list[str]:
        return sorted(rng.sample(sorted(cands), n))

    pool_ab = sorted(a for a in screen
                     if screen[a]["tier"] in "AB" and a in indexed and a in corpus)
    no_html = [a for a in pool_ab if render_status(a) == "none"]
    no_assign = [a for a in pool_ab if a not in assigned and render_status(a) == "html"]
    b_pool = [a for a in pool_ab if screen[a]["tier"] == "B" and render_status(a) == "html"]
    sys_a = [a for a in pool_ab if screen[a]["tier"] == "A"
             and screen[a]["kind"] in ("system",) and render_status(a) == "html"]
    ds_a = [a for a in pool_ab if screen[a]["tier"] == "A"
            and screen[a]["kind"] == "dataset" and render_status(a) == "html"]
    bench = [a for a in pool_ab if screen[a]["kind"] == "benchmark" and render_status(a) == "html"]
    meth_a = [a for a in pool_ab if screen[a]["tier"] == "A"
              and screen[a]["kind"] == "method" and render_status(a) == "html"]

    dev = []
    dev.append((pick(meth_a, 1)[0], "dev", "A/method anchor, html"))
    dev.append((pick(sys_a, 1)[0], "dev", "A/system anchor, html"))
    if ds_a:
        dev.append((pick(ds_a, 1)[0], "dev", "A/dataset anchor, html"))
    else:
        dev.append((pick(meth_a, 1)[0], "dev", "A/method anchor (no dataset in pool), html"))
    dev.append((pick(no_html, 1)[0], "dev", "needs_fulltext path (no html render)"))
    dev.append((pick(no_assign, 1)[0], "dev", "no old pattern assignment (matching cold-start)"))
    dev.append((pick(b_pool, 1)[0], "dev", "B-tier borderline"))

    dev_ids = {a for a, *_ in dev}
    hold = []
    # 12 holdout: full material, stratified over kind and assignment presence.
    hold_strata = [
        (meth_a, 5, "A/method"), (sys_a, 3, "A/system"),
        (ds_a + bench, 2, "dataset/benchmark"), (meth_a, 2, "A/method unassigned"),
    ]
    for cands, n, label in hold_strata:
        c = [a for a in cands if a not in dev_ids and a not in {h for h, *_ in hold}]
        for a in pick(c, n):
            hold.append((a, "holdout", f"{label}, html"))

    calib = [{"arxiv": a, "layer": layer, "stratum": s,
              "kind_hint": screen[a]["kind"], "tier_hint": screen[a]["tier"]}
             for a, layer, s in dev + hold]

    assets = {role: {"path": p, "sha256": sha256(ROOT / p)} for p, role in ASSETS.items()}
    manifest = {
        "run_id": run_id,
        "schema": "radar-run-v2.2",
        "created": "2026-10-21",
        "seed": SEED,
        "namespace": "gui",
        "scope": ("corpus snapshot 2026-10-21 (2732 ids); production queue = screen tier A (701) "
                  "then B (627); screen/assignments are queue hints only, all judgments new"),
        "assets": assets,
        "model_types": MODEL_TYPES,
        "batch_size": 5,
        "parallel_batches": 2,
        "budget_note": ("calibration 6 dev + 12 holdout, then production rounds; stop at "
                        "session budget and commit a partial checkpoint if queue remains"),
        "expectations_choice": ("cua-agents/v1 (35) — superset of cua-agents-core/v1 (22), "
                                "active card dependencies; recorded hash binds the file"),
    }

    run_dir.mkdir(parents=True)
    (run_dir / "calibration").mkdir()
    (run_dir / "batches").mkdir()
    (run_dir / "rounds").mkdir()
    (run_dir / "final").mkdir()
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    (run_dir / "calibration" / "plan.json").write_text(
        json.dumps({"seed": SEED, "papers": calib}, ensure_ascii=False, indent=1))
    with open(run_dir / "queue.jsonl", "w") as f:
        for a in queue_ids:
            s = screen[a]
            f.write(json.dumps({
                "arxiv": a, "title": corpus.get(a, {}).get("title", ""),
                "version": corpus.get(a, {}).get("latest_version"),
                "tier_hint": s["tier"], "kind_hint": s["kind"],
                "status": "queued", "attempt": None,
            }, ensure_ascii=False) + "\n")
    print(f"init {run_id}: queue={len(queue_ids)} calib={len(calib)} (dev 6, holdout {len(hold)})")


if __name__ == "__main__":
    main()
