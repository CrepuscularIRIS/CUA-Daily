"""Shared helpers for son55/a1 builders (worker helper; not a paper record)."""
import json
import re
from pathlib import Path

ROOT = Path("/home/lingxufeng/GUI/cua-architecture-radar")
FT = ROOT / "research/fulltext/review-runs/gui-v22-20261021-01"
OUT = ROOT / "research/v2/runs/gui-v22-20261021-01/batches/p8/seats/son55/attempts/a1"

W = {"G": 15, "M": 25, "X": 20, "E.measurement": 10, "E.causality": 10,
     "E.holdout": 10, "E.statistics": 5, "E.cost": 5}
KEYS = list(W)
RUBRIC_HASH = "8e579efd92dbd5b264ce1c61f86c531cbe4300480f456baa57e47a444d42cba5"

PROV = {
    "input_hash": "f3dad3d18251340267b0256f3f2897e3cfa491c66cc114afaf952cd15960672f",
    "rubric_version": "SCORE_SPEC v2.2 draft_uncalibrated (weights frozen per controller)",
    "rubric_hash": RUBRIC_HASH,
    "rs_manifest_hash": "3fc06b621b26f2ea87aa273ee34e2a80308fd09102f1530056428662b0971e32",
    "domain_cards_hash": {
        "taxonomy": "430aa36290ecfb7a45e0c413c663085635dc1451e189d10ab86e8b4480186c21",
        "conditions": "a7501743e64eacce006fd9ad4388ad5c65684a9eeee355eac76ebaa531ef3572"},
    "expectations_hash": "4663f2b47de565c2d4d000de3228499b1de3d8a12f73d43664a0297e05452e67",
    "model_type": "haiku",
    "actual_model": "claude-sonnet-5-5[1m] (Sonnet 5.5, as named in this worker's system prompt)",
    "session_id": None,
    "receipt_ref": None,
    "session_receipt_reason": "no session id / receipt exposed to the worker; not probed",
    "timestamp": "2026-10-22T02:55:00Z",
}


def rating(status, val, reason, ev, counter=(), scope=()):
    return {"status": status, "rating": val, "reason": reason,
            "evidence_ids": list(ev), "counterevidence_ids": list(counter),
            "search_scope": list(scope)}


def score(ratings):
    tot = 0
    unknown = 0
    known_w = 0
    for k in KEYS:
        r = ratings[k]
        if r["status"] == "unknown":
            unknown += 1
            continue
        tot += W[k] * r["rating"]
        known_w += W[k]
    if unknown:
        lo = tot / 4
        hi = (tot + sum(W[k] * 4 for k in KEYS if ratings[k]["status"] == "unknown")) / 4
        return {"raw": None, "display": None, "lower": lo, "upper": hi,
                "coverage": known_w / 100, "rubric_hash": RUBRIC_HASH}
    raw = tot / 4
    return {"raw": raw, "display": round(raw, 1), "lower": raw, "upper": raw,
            "coverage": 1.0, "rubric_hash": RUBRIC_HASH}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def verify_quotes(rec, mat_texts):
    """mat_texts: material_id -> normalized text. Returns list of failures."""
    bad = []
    for e in rec["evidence"]:
        q = e.get("quote")
        if q is None:
            continue
        t = mat_texts.get(e["material_id"])
        if t is None or norm(q) not in t:
            bad.append((e["evidence_id"], q[:80]))
    return bad


def write_atomic(path, rec):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    json.loads(tmp.read_text())
    tmp.replace(path)
