#!/usr/bin/env python3
"""Mechanical acceptance check for a dual-seat batch (BATCH_CONTRACT items 1-5).

Verifies seat coverage against the batch manifest, required fields, rs-card
ids/namespaces, rating legality; writes field-level diffs to conflicts.json.
Semantic checking stays with the Opus aggregator — this is structure only.

Usage: python3 research/v2/check_batch.py <run_id> <batch_id> [attempt=a1]
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = Path(os.environ.get("CUA_RADAR_RUNS", ROOT / "research" / "v2" / "runs"))

MAIN_CARDS = {
    "adapt_via_conditioning", "algebraic_equivalence_unification",
    "architectural_operator_substitution", "assumption_audit_and_pivot",
    "characterize_limit_then_surpass", "controlled_diagnostic_design",
    "decompose_and_delegate", "generative_process_redesign",
    "heterogeneous_decomposition", "reframe_as_solvable_object",
    "relax_discrete_search_to_continuous", "self_supervised_signal_engineering",
    "structural_prior_encoding", "targeted_self_supervised_objective",
    "unify_into_shared_representation",
}
PARENTS = {}
for line in open(ROOT / "research/reference/researchstudio-15-31/PARENTS.tsv"):
    sub, parent = line.strip().split("\t")
    if sub != "sub_id":
        PARENTS[sub] = parent

RATING_KEYS = ["G", "M", "X", "E.measurement", "E.causality", "E.holdout",
               "E.statistics", "E.cost"]
E_SUBS = RATING_KEYS[3:]


def rating(rec: dict, key: str):
    ratings = rec.get("ratings", {})
    if key in ratings:  # flat form: "E.measurement" (contract literal)
        return ratings[key]
    if key.startswith("E."):
        return (ratings.get("E") or {}).get(key[2:])
    return ratings.get(key)


def load_seat(bdir: Path, seat: str, attempt: str) -> dict[str, dict]:
    d = {}
    adir = bdir / "seats" / seat / "attempts" / attempt
    for f in adir.glob("*.json"):
        if f.name == "batch-report.json" or f.name.startswith("_"):
            continue  # worker helper files (quote caches, build scripts) are not paper records
        try:
            d[f.stem] = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            d[f.stem] = {"_schema_error": f"unparseable JSON: {e}"}
    return d


def check_record(rec: dict, key: str, errors: list) -> None:
    def err(m):
        errors.append(f"{key}: {m}")
    for field in ("schema_version", "run_id", "batch_id", "seat", "paper",
                  "provenance", "materials", "ratings", "status"):
        if field not in rec:
            err(f"missing field {field}")
    if rec.get("schema_version") != "radar-review-v2.2":
        err(f"schema_version={rec.get('schema_version')!r}")
    st = rec.get("status")
    if isinstance(st, dict):  # {state|value, reason} forms
        st = st.get("state", st.get("value"))
    if st not in ("reviewed", "needs_fulltext", "needs_evidence", "out_of_scope"):
        err(f"status={st!r}")
    if st == "reviewed":
        if not rec.get("rs_pattern"):
            err("reviewed without rs_pattern block")
        if not rec.get("assessment"):
            err("reviewed without assessment block")
    rsp = rec.get("rs_pattern") or {}
    for m in (rsp.get("matches") or []):
        main = m.get("main_id")
        if main not in MAIN_CARDS:
            err(f"rs main_id {main!r} not one of the 15 cards")
        sub = m.get("sub_id")
        if sub is not None:
            # protocol form is `rs:C08`; PARENTS.tsv keys are bare C08
            bare = sub[3:] if sub.startswith("rs:") else sub
            if PARENTS.get(bare) != main:
                err(f"rs sub {sub!r} not under parent {main!r} (PARENTS.tsv says {PARENTS.get(bare)!r})")
    if rsp.get("outside_taxonomy") and rsp.get("primary") is not None:
        err("outside_taxonomy=true but primary is set")
    dp = rec.get("domain_pattern") or {}
    if dp and dp.get("namespace") != "gui":
        err(f"domain namespace={dp.get('namespace')!r}")
    # ratings legality
    n_unknown = 0
    for k in RATING_KEYS:
        r = rating(rec, k)
        if not isinstance(r, dict):
            err(f"rating {k} missing/not dict")
            continue
        val, stat = r.get("rating"), r.get("status")
        if stat == "unknown":
            if val is not None:
                err(f"{k} unknown but rating={val}")
            n_unknown += 1
        elif stat in ("resolved", "not_reported"):
            if not isinstance(val, int) or not 0 <= val <= 4:
                err(f"{k} rating={val!r} not int 0..4 (status {stat})")
            if stat == "not_reported" and not r.get("search_scope"):
                err(f"{k} not_reported without search_scope")
        else:
            err(f"{k} status={stat!r}")
    if st == "reviewed":
        sc = rec.get("score")
        if not isinstance(sc, dict):
            err("score block missing")
        elif n_unknown and sc.get("raw") is not None:
            err(f"{n_unknown} unknown ratings but score.raw is not null")


def diff_records(sol: dict, son: dict, key: str) -> list[dict]:
    """Field-level diffs on judgment-bearing fields (no averaging, no threshold)."""
    out = []
    def state_of(r):
        st = r.get("status")
        return st.get("state", st.get("value")) if isinstance(st, dict) else st
    pairs = [
        ("claim_type", lambda r: r.get("paper", {}).get("claim_type")),
        ("evidence_level", lambda r: r.get("assessment", {}).get("evidence_level")),
        ("claim_support", lambda r: r.get("assessment", {}).get("claim_support")),
        ("status", state_of),
        ("rs.primary", lambda r: (r.get("rs_pattern") or {}).get("primary")),
        ("rs.supporting", lambda r: (r.get("rs_pattern") or {}).get("supporting")),
        ("rs.outside", lambda r: (r.get("rs_pattern") or {}).get("outside_taxonomy")),
        ("rs.matches", lambda r: sorted(
            f"{m.get('main_id')}/{m.get('sub_id')}" for m in (r.get("rs_pattern") or {}).get("matches") or [])),
        ("domain.matches", lambda r: sorted(
            f"{m.get('main')}/{m.get('sub')}" for m in (r.get("domain_pattern") or {}).get("matches") or [])),
    ]
    for name, get in pairs:
        a, b = get(sol), get(son)
        if a != b:
            out.append({"field": name, "sol": a, "son55": b})
    for k in RATING_KEYS:
        a, b = rating(sol, k), rating(son, k)
        av = (a or {}).get("rating"); bv = (b or {}).get("rating")
        ast = (a or {}).get("status"); bst = (b or {}).get("status")
        if av != bv or ast != bst:
            out.append({"field": f"rating.{k}", "sol": {"status": ast, "rating": av},
                        "son55": {"status": bst, "rating": bv}})
    exp_a = {e.get("id"): e.get("status") for e in sol.get("expectations") or []}
    exp_b = {e.get("id"): e.get("status") for e in son.get("expectations") or []}
    for eid in sorted(set(exp_a) | set(exp_b)):
        if exp_a.get(eid) != exp_b.get(eid):
            out.append({"field": f"expectation.{eid}", "sol": exp_a.get(eid), "son55": exp_b.get(eid)})
    return out


def main() -> None:
    run_id, batch_id = sys.argv[1], sys.argv[2]
    attempt = sys.argv[3].split("=")[1] if len(sys.argv) > 3 else "a1"
    bdir = RUNS / run_id / "batches" / batch_id
    bm = json.loads((bdir / "manifest.json").read_text())
    want = {p["paper_key"] for p in bm["papers"]}

    seats = {}
    all_errors = []
    for seat in ("sol", "son55"):
        recs = load_seat(bdir, seat, attempt)
        missing, extra = want - set(recs), set(recs) - want
        if missing:
            all_errors.append(f"seat {seat}: missing papers {sorted(missing)}")
        if extra:
            all_errors.append(f"seat {seat}: extra papers {sorted(extra)}")
        for key, rec in recs.items():
            check_record(rec, f"{seat}/{key}", all_errors)
        seats[seat] = recs

    conflicts = {}
    for key in sorted(want & set(seats["sol"]) & set(seats["son55"])):
        d = diff_records(seats["sol"][key], seats["son55"][key], key)
        if d:
            conflicts[key] = d

    out = {
        "batch": batch_id, "attempt": attempt,
        "coverage_ok": not all_errors,
        "errors": all_errors,
        "n_conflict_papers": len(conflicts),
        "conflicts": conflicts,
    }
    (bdir / "conflicts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "conflicts"}, ensure_ascii=False, indent=1))
    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
