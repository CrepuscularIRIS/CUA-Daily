"""Shared helpers for the c2/a1 Opus aggregate (adapted from c3/a1 tooling): seat loading, ID namespacing, scoring, hashing."""
from __future__ import annotations

import copy
from decimal import ROUND_HALF_UP, Decimal
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/lingxufeng/GUI/cua-architecture-radar")
RUN = "gui-v22-20261021-01"
BATCH = "c2"
BATCH_DIR = ROOT / f"research/v2/runs/{RUN}/batches/{BATCH}"
OUT_DIR = BATCH_DIR / "aggregate/attempts/a1"
FT_DIR = ROOT / f"research/fulltext/review-runs/{RUN}/fulltext"
REFS = ROOT / f"research/fulltext/review-runs/{RUN}/references.json"
KEYS8 = ["G", "M", "X", "E.measurement", "E.causality", "E.holdout", "E.statistics", "E.cost"]
WEIGHTS = {"G": 15, "M": 25, "X": 20, "E.measurement": 10, "E.causality": 10,
           "E.holdout": 10, "E.statistics": 5, "E.cost": 5}
RUBRIC_HASH = "8e579efd92dbd5b264ce1c61f86c531cbe4300480f456baa57e47a444d42cba5"
ID_LIST_KEYS = {"evidence_ids", "counterevidence_ids", "counterevidence"}

assert sum(WEIGHTS.values()) == 100
assert sum(v for k, v in WEIGHTS.items() if k.startswith("E.")) == 40


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def seat_path(seat: str, pk: str) -> Path:
    return BATCH_DIR / f"seats/{seat}/attempts/a1/{pk}.json"


def load_seat(seat: str, pk: str) -> dict:
    return json.loads(seat_path(seat, pk).read_text(encoding="utf-8"))


def seat_status(d: dict) -> str:
    """son55 writes status as {value|state, reason}; contract says a string."""
    s = d["status"]
    return (s.get("value") or s.get("state")) if isinstance(s, dict) else s


def bare(x):
    """'gui:C17' / 'rs:C26' -> 'C17' / 'C26'; None stays None."""
    return x.split(":", 1)[1] if isinstance(x, str) and ":" in x else x


def remap_ids(obj, seat: str, known: set[str]):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ID_LIST_KEYS and isinstance(v, list):
                out[k] = [f"{seat}:{x}" if isinstance(x, str) and x in known else remap_ids(x, seat, known) for x in v]
            else:
                out[k] = remap_ids(v, seat, known)
        return out
    if isinstance(obj, list):
        return [remap_ids(x, seat, known) for x in obj]
    return copy.deepcopy(obj)


def seat_view(seat: str, pk: str) -> dict:
    """Seat record with namespaced evidence/material IDs and flat ratings."""
    d = load_seat(seat, pk)
    known = {e["evidence_id"] for e in d.get("evidence", [])}
    v = remap_ids(d, seat, known)
    for e in v.get("evidence", []):
        e["evidence_id"] = f"{seat}:{e['evidence_id']}"
        e["material_id"] = f"{seat}:{e['material_id']}"
    for m in v.get("materials", []):
        m["material_id"] = f"{seat}:{m['material_id']}"
    r = v.get("ratings", {})
    if "E" in r:
        for k, val in r.pop("E").items():
            r[f"E.{k}"] = val
    v["ratings"] = {k: r[k] for k in KEYS8}
    return v


def score(ratings: dict) -> dict:
    lo = hi = 0.0
    cov = 0
    unknown = False
    for k in KEYS8:
        r = ratings[k]
        w = WEIGHTS[k]
        if r["status"] == "unknown":
            assert r["rating"] is None
            unknown = True
            hi += w * 4
        else:
            assert isinstance(r["rating"], int) and 0 <= r["rating"] <= 4, (k, r)
            if r["status"] == "not_reported":
                assert r["rating"] == 0 and r.get("search_scope"), k
            lo += w * r["rating"]
            hi += w * r["rating"]
            cov += w
    lo, hi = lo / 4, hi / 4
    raw = None if unknown else lo
    disp = None if raw is None else float(Decimal(str(raw)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    return {"raw": raw, "display": disp, "lower": lo, "upper": hi,
            "coverage": cov / 100, "rubric_hash": RUBRIC_HASH,
            "formula": "S=(15G+25M+20X+10Emeas+10Ecaus+10Ehold+5Estat+5Ecost)/4; unknown -> L uses 0, U uses 4; raw=null while any unknown"}


def canonical_hash(record: dict) -> str:
    body = {k: v for k, v in record.items() if k != "final_record_hash"}
    s = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_atomic(path: Path, record: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def agg_evidence(eid: str, src: str, locator: str, quote: str, expl: str, kind: str = "author_report") -> dict:
    """Aggregator evidence; quote must be a contiguous substring of the fixed text (checked here)."""
    path = FT_DIR / f"{src}.txt"
    text = path.read_text(encoding="utf-8")
    assert text.count(quote) >= 1, (src, quote[:80])
    return {"evidence_id": f"agg:{eid}", "material_id": f"agg:{src}", "material_sha256": sha256_file(path),
            "locator": locator, "quote": quote, "support_explanation": expl, "kind": kind}


def agg_material(src: str, role: str, note: str | None = None, manifest_sha: str | None = None) -> dict:
    path = FT_DIR / f"{src}.txt"
    sha = sha256_file(path)
    pdf = src.endswith(".pdf-supplement")
    aid = src.split(".pdf")[0]
    m = {"material_id": f"agg:{src}", "url": f"https://arxiv.org/{'pdf' if pdf else 'html'}/{aid}", "sha256": sha,
         "fulltext_path": str(path.relative_to(ROOT)), "role": role,
         "sections_read": ["full text"] if role == "paper" else (["prompt boxes / appendix listings cited by agg evidence"] if pdf else ["targeted sections cited by agg evidence"]),
         "complete": role in ("paper", "pdf_supplement"),
         "missing_sections": [] if role in ("paper", "pdf_supplement") else ["not read in full; used only as shared factual reference"]}
    if manifest_sha is not None:
        m["manifest_sha256"] = manifest_sha
        m["matches_manifest_pin"] = sha == manifest_sha
    if note:
        m["note"] = note
    return m
