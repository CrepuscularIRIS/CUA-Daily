"""Assemble c3/a1 aggregate final records + batch report from seat originals and decisions.py (read-only on inputs)."""
from __future__ import annotations

import json

from common import (BATCH, BATCH_DIR, ID_LIST_KEYS, KEYS8, OUT_DIR, REFS, ROOT, agg_material, bare, canonical_hash,
                    load_seat, now, score, seat_path, seat_status, seat_view, sha256_file, write_atomic)
from decisions import PAPERS, QP

MANIFEST = json.loads((BATCH_DIR / "manifest.json").read_text())
CONFLICTS = json.loads((BATCH_DIR / "conflicts.json").read_text())["conflicts"]
TAX = json.loads((ROOT / "research/patterns/taxonomy.json").read_text())
SUBS_OF = {m["id"]: set(m["subs"]) for m in TAX["main"]}
PARENTS = dict(l.split("\t") for l in (ROOT / "research/reference/researchstudio-15-31/PARENTS.tsv").read_text().split("\n")[1:] if l.strip())
RS_MAINS = {p.stem for p in (ROOT / "research/reference/researchstudio-15-31/ideation-patterns").glob("*.md")} - {"overview"}
AGG_MODEL = {"aggregate_model": "fable", "aggregate_actual_model": "claude-opus-5-5[1m]", "aggregate_session": None,
             "aggregate_receipt_ref": None,
             "aggregate_session_note": "Configured model type fable (upstream claude-opus-5-5[1m]) per batch manifest model_types.opus55; no session id or invocation receipt is exposed to this agent."}


def man(pk: str) -> dict:
    return next(p for p in MANIFEST["papers"] if p["paper_key"] == pk)


def ent_key(m: dict) -> tuple:
    main = m.get("main") or m.get("main_id")
    sub = m["sub"] if "sub" in m else m.get("sub_id")
    return (main, bare(sub))


def check_patterns(rs: dict, dom: dict) -> list[str]:
    errs = []
    if rs.get("outside_taxonomy") is True:
        if rs.get("primary") is not None or rs.get("matches") or rs.get("supporting"):
            errs.append("outside_taxonomy with matches")
    elif rs:
        if rs.get("primary") not in RS_MAINS:
            errs.append(f"bad rs primary {rs.get('primary')}")
        for m in rs.get("matches", []):
            if m["main_id"] not in RS_MAINS:
                errs.append(f"bad rs main {m['main_id']}")
            if m.get("sub_id") is not None and PARENTS.get(bare(m["sub_id"])) != m["main_id"]:
                errs.append(f"rs sub {m['sub_id']} not under {m['main_id']}")
        if len(rs.get("supporting", [])) > 2:
            errs.append("more than 2 supporting")
    if dom:
        if dom.get("namespace") != "gui":
            errs.append("domain namespace")
        for m in dom.get("matches", []):
            main, sub = ent_key(m)
            if main not in SUBS_OF or (sub is not None and sub not in SUBS_OF[main]):
                errs.append(f"domain {main}/{sub} invalid")
    return errs


def seat_integrity(pk: str) -> dict:
    mf = man(pk)
    out = {}
    for s in ("sol", "son55"):
        d = load_seat(s, pk)
        v = seat_view(s, pk)
        out[s] = {
            "file_sha256": sha256_file(seat_path(s, pk)),
            "status": seat_status(d),
            "status_field_shape": type(d["status"]).__name__ + ("" if isinstance(d["status"], str) else " (contract expects string; value read from .state)"),
            "version_matches_manifest": d["paper"]["version"] == mf["version"],
            "input_hash_matches_manifest": d["provenance"]["input_hash"] == MANIFEST["input_bundle_sha256"],
            "material_sha_matches_manifest": mf["material_sha256"] in [m.get("sha256") for m in d.get("materials", [])],
            "rs_and_domain_parent_errors": check_patterns(v.get("rs_pattern") or {}, v.get("domain_pattern") or {}),
            "model_type": d["provenance"].get("model_type"), "actual_model": d["provenance"].get("actual_model"),
        }
    return out


def pick_rs(spec: dict, views: dict) -> tuple[dict, list]:
    seat, reason = spec["rs"]
    rs = dict(views[seat]["rs_pattern"])
    rs["aggregate_source_seat"] = seat
    rs["aggregate_reason"] = reason
    return rs, views[seat]["pattern_mapping"]


def pick_domain(spec: dict, views: dict) -> dict:
    matches = []
    for seat, main, sub, fit in spec["domain"]:
        src = next(m for m in views[seat]["domain_pattern"]["matches"] if ent_key(m) == (main, sub))
        m = dict(src)
        m.pop("main_id", None), m.pop("sub_id", None)
        m["namespace"], m["main"], m["sub"] = "gui", main, (f"gui:{sub}" if sub else None)
        if fit:
            m["fit"] = fit
        m["aggregate_source_seat"] = seat
        matches.append(m)
    son = views["son55"]["domain_pattern"]
    return {"namespace": "gui", "matches": matches, "unassigned": son.get("unassigned", []),
            "revision_proposals": son.get("revision_proposals", []), "aggregate_note": spec["domain_note"]}


def pick_expectations(spec: dict, views: dict) -> list:
    by = {s: {e["id"]: e for e in views[s]["expectations"]} for s in ("sol", "son55")}
    out = []
    for e in views["son55"]["expectations"]:
        choice = spec["expectations"].get(e["id"])
        if choice is None:
            out.append(e)
        elif isinstance(choice, str):
            x = dict(by[choice][e["id"]])
            x["aggregate_source_seat"] = choice
            out.append(x)
        else:
            x = dict(e)
            x.update(choice)
            x["aggregate_source_seat"] = "son55_value_reason_replaced"
            out.append(x)
    return out


def resolutions_for(pk: str, dec: dict) -> list:
    confs = CONFLICTS.get(pk, [])
    fields = [c["field"] for c in confs]
    missing = [f for f in fields if f not in dec]
    extra = [f for f in dec if f not in fields]
    assert not missing and not extra, (pk, missing, extra)
    out = []
    for c in confs:
        decision, final, reason, ev, impact = dec[c["field"]]
        out.append({"field_path": c["field"], "sol_value": c["sol"], "son55_value": c["son55"], "decision": decision,
                    "final_value": final, "reason": reason, "evidence_ids": ev, "score_impact": impact})
    return out


def collect_ids(obj, acc: set) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ID_LIST_KEYS and isinstance(v, list):
                acc.update(x for x in v if isinstance(x, str) and ":" in x)
            else:
                collect_ids(v, acc)
    elif isinstance(obj, list):
        for x in obj:
            collect_ids(x, acc)


def provenance() -> dict:
    a = MANIFEST["asset_hashes"]
    return {
        "input_hash": MANIFEST["input_bundle_sha256"], "rubric_version": "v2.2 draft_uncalibrated",
        "rubric_hash": a["rubric"]["sha256"], "rs_manifest_hash": a["rs_cards_manifest"]["sha256"],
        "domain_cards_hash": a["domain_taxonomy"]["sha256"], "domain_conditions_hash": a["domain_conditions"]["sha256"],
        "expectations_hash": a["expectations"]["sha256"], "batch_contract_hash": a["batch_contract"]["sha256"],
        "aggregate_rules": "docs/agents/AGGREGATE_OPUS.md", "aggregate_rules_sha256": sha256_file(ROOT / "docs/agents/AGGREGATE_OPUS.md"),
        "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"), "references_sha256": sha256_file(REFS),
        "model_type": "fable", "actual_model": "claude-opus-5-5[1m]", "session_id": None, "receipt_ref": None,
        "timestamp": now(),
        "independence_note": "Aggregation over two seat inputs; each fixed paper text was read before the seat scores, but this is not a third blind review or human gold. All results are author reports; nothing was reproduced.",
    }


def check_refs(rec: dict, pk: str) -> None:
    ev_ids = {e["evidence_id"] for e in rec["evidence"]}
    assert len(ev_ids) == len(rec["evidence"]), pk
    mat_ids = {m["material_id"] for m in rec["materials"]}
    assert all(e["material_id"] in mat_ids for e in rec["evidence"]), pk
    refs: set = set()
    collect_ids({k: v for k, v in rec.items() if k != "evidence"}, refs)
    dangling = sorted(r for r in refs if r.split(":")[0] in {"sol", "son55", "agg"} and r not in ev_ids)
    assert not dangling, (pk, dangling)


def build_paper(spec: dict) -> dict:
    pk = spec["pk"]
    mf = man(pk)
    views = {s: seat_view(s, pk) for s in ("sol", "son55")}
    base = views["son55"]
    integ = seat_integrity(pk)
    assert all(v["version_matches_manifest"] and v["input_hash_matches_manifest"] and v["material_sha_matches_manifest"]
               and not v["rs_and_domain_parent_errors"] for v in integ.values()), (pk, integ)

    ratings = {k: spec["ratings"][k] for k in KEYS8}
    for f, (_d, final, *_r) in spec["resolutions"].items():
        if f.startswith("rating."):
            assert ratings[f[len("rating."):]]["rating"] == final["rating"], (pk, f)
    sc = score(ratings)
    assert sc["raw"] == spec["expected_score"], (pk, sc["raw"])
    rs, pmap = pick_rs(spec, views)
    if pk == "2604.11784":  # son55 rs already carries supporting controlled_diagnostic_design
        assert rs["supporting"] == ["controlled_diagnostic_design"]
    dom = pick_domain(spec, views)
    assert not check_patterns(rs, dom), (pk, check_patterns(rs, dom))
    gap = dict(base["gap"])
    gap.update(spec["gap_check"])

    paper = dict(base["paper"])
    paper["paper_id"] = mf["arxiv"]
    if "claim_type" in spec["resolutions"]:
        paper["claim_type"] = spec["resolutions"]["claim_type"][1]
    claims = []
    known_claims = {c["claim_id"] for c in base["claims"]}
    assert set(spec.get("claims_append", {})) <= known_claims, pk
    for c in base["claims"]:
        c = dict(c)
        add = spec.get("claims_append", {}).get(c["claim_id"])
        if add:
            ids, note = add
            c["counterevidence"] = list(c.get("counterevidence") or []) + ids
            c["aggregate_note"] = note
        claims.append(c)

    agg_status, agg_reason = spec["status"]
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": BATCH, "attempt_id": "a1", "seat": "aggregate",
        "paper": paper,
        "provenance": provenance(),
        "materials": [agg_material(src, role) for src, role in spec["materials"]] + views["sol"]["materials"] + base["materials"],
        "evidence": spec["evidence"] + views["sol"]["evidence"] + base["evidence"],
        "preliminary_evidence_judgment": spec["prelim"],
        "agreed_items_review": spec["agreed_review"],
        "signatures": base["signatures"],
        "gap": gap,
        "rs_pattern": rs,
        "domain_pattern": dom,
        "pattern_mapping": pmap,
        "expectations": pick_expectations(spec, views),
        "claims": claims,
        "assessment": spec["assessment"],
        "ratings": ratings,
        "score": sc,
        "status": "reviewed",
        "status_reason": "Full fixed HTML text available and read; all eight items resolved.",
        "input_seat_hashes": {s: integ[s]["file_sha256"] for s in ("sol", "son55")},
        **AGG_MODEL,
        "seat_integrity_check": integ,
        "resolutions": resolutions_for(pk, spec["resolutions"]),
        "shared_error_corrections": spec["shared"],
        "aggregate_status": agg_status,
        "aggregate_status_reason": agg_reason,
    }
    assert rec["paper"]["version"] == mf["version"]
    check_refs(rec, pk)
    assert not ([r for r in rec["resolutions"] if r["decision"] == "unresolved"] and agg_status == "accepted_final")
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def build_out_of_scope(spec: dict) -> dict:
    pk = spec["pk"]
    mf = man(pk)
    integ = seat_integrity(pk)
    assert all(v["status"] == "out_of_scope" for v in integ.values()), integ
    confs = CONFLICTS.get(pk, [])
    assert len(confs) == spec["expected_conflicts"]
    son = load_seat("son55", pk)
    note = ("Both seats independently disposed of the paper as out_of_scope; son55 additionally kept provisional analysis fields "
            "(status object reason: 'temporary analysis retained'). An out-of-scope final record carries no assessment, pattern, "
            "expectation or rating judgement, so the sol value (null/empty) is kept. son55's provisional content is not adopted "
            "and is not judged here; it remains in the seat original (hash in input_seat_hashes).")
    resolutions = [{"field_path": c["field"], "sol_value": c["sol"], "son55_value": c["son55"], "decision": "sol",
                    "final_value": c["sol"], "reason": note, "evidence_ids": ["agg:QP-A01"],
                    "score_impact": "none (out_of_scope, score=null)"} for c in confs]
    unscored = {k: {"status": "unknown", "rating": None, "reason": "Not scored: out_of_scope disposition (not a quality judgement).",
                    "evidence_ids": [], "counterevidence_ids": [], "search_scope": []} for k in KEYS8}
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": BATCH, "attempt_id": "a1", "seat": "aggregate",
        "paper": {"paper_key": pk, "paper_id": mf["arxiv"], "title": mf["title"], "version": mf["version"],
                  "claim_type": None, "central_claim": son["paper"]["central_claim"]},
        "provenance": provenance(),
        "materials": [agg_material(pk, "paper")],
        "evidence": spec["evidence"],
        "ratings": unscored,
        "score": None,
        "status": "out_of_scope",
        "status_reason": spec["reason"],
        "input_seat_hashes": {s: integ[s]["file_sha256"] for s in ("sol", "son55")},
        **AGG_MODEL,
        "seat_integrity_check": integ,
        "resolutions": resolutions,
        "shared_error_corrections": [],
        "aggregate_status": "out_of_scope",
        "aggregate_status_reason": "Scope exclusion confirmed from the fixed full text (typed tool-call planner; no GUI operation surface). Disposition, not an error state and not a completed scoring review; score=null.",
    }
    check_refs(rec, pk)
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def main() -> None:
    records = {spec["pk"]: build_paper(spec) for spec in PAPERS}
    records[QP["pk"]] = build_out_of_scope(QP)
    assert sorted(records) == sorted(p["paper_key"] for p in MANIFEST["papers"])
    rows = []
    for p in MANIFEST["papers"]:
        pk = p["paper_key"]
        path = OUT_DIR / f"{pk}.json"
        write_atomic(path, records[pk])
        back = json.loads(path.read_text(encoding="utf-8"))
        assert canonical_hash(back) == back["final_record_hash"], pk
        if back.get("score"):
            assert score(back["ratings"])["raw"] == back["score"]["raw"]
        res = back["resolutions"]
        rows.append({
            "paper_key": pk, "version": back["paper"]["version"], "aggregate_status": back["aggregate_status"],
            "claim_type": back["paper"].get("claim_type"),
            "evidence_level": (back.get("assessment") or {}).get("evidence_level"),
            "claim_support": (back.get("assessment") or {}).get("claim_support"),
            "raw_score": back["score"]["raw"] if back.get("score") else None,
            "display_score": back["score"]["display"] if back.get("score") else None,
            "ratings": {k: back["ratings"][k]["rating"] for k in KEYS8},
            "seat_raw_scores": {s: (load_seat(s, pk).get("score") or {}).get("raw") for s in ("sol", "son55")},
            "seat_status": {s: seat_status(load_seat(s, pk)) for s in ("sol", "son55")},
            "n_mechanical_conflicts": len(CONFLICTS.get(pk, [])),
            "n_resolutions": len(res),
            "resolution_decisions": {d: sum(1 for r in res if r["decision"] == d)
                                     for d in ("sol", "son55", "revised", "unresolved", "same_supported_fact")},
            "n_rating_conflicts": sum(1 for r in res if r["field_path"].startswith("rating.")),
            "n_shared_error_corrections": len(back["shared_error_corrections"]),
            "n_unresolved": sum(1 for r in res if r["decision"] == "unresolved"),
            "file": str(path), "file_sha256": sha256_file(path), "final_record_hash": back["final_record_hash"],
            "input_seat_hashes": back["input_seat_hashes"],
        })
    scored = [r for r in rows if r["raw_score"] is not None]
    reviewed = [pk for pk, r in records.items() if r["status"] == "reviewed"]
    report = {
        "schema_version": "radar-batch-report-v2.2", "kind": "aggregate-batch-report",
        "run_id": MANIFEST["run_id"], "batch_id": BATCH, "attempt_id": "a1", "seat": "aggregate",
        "input_hash": MANIFEST["input_bundle_sha256"],
        "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"), "references_sha256": sha256_file(REFS),
        **AGG_MODEL,
        "assigned": len(MANIFEST["papers"]),
        "dispositions": {st: sum(r["aggregate_status"] == st for r in rows)
                         for st in ("accepted_final", "needs_revision", "needs_evidence", "needs_fulltext", "out_of_scope")},
        "scored": len(scored), "blocked": sum(r["aggregate_status"] in ("needs_revision", "needs_evidence", "needs_fulltext") for r in rows),
        "outside_taxonomy_ratio_of_reviewed": f"{sum(1 for pk in reviewed if records[pk]['rs_pattern'].get('outside_taxonomy') is True)}/{len(reviewed)}",
        "totals": {"mechanical_conflicts": sum(r["n_mechanical_conflicts"] for r in rows),
                   "resolutions": sum(r["n_resolutions"] for r in rows),
                   "rating_conflicts": sum(r["n_rating_conflicts"] for r in rows),
                   "shared_error_corrections": sum(r["n_shared_error_corrections"] for r in rows),
                   "unresolved": sum(r["n_unresolved"] for r in rows)},
        "records": rows,
        "validation": {
            "seat_set_equals_manifest": True,
            "seat_versions_input_hash_material_sha_checked": True,
            "seat_quote_substring_check": "all seat evidence quotes (both seats, 6 papers) found in the cited fixed texts after whitespace normalisation",
            "seat_rs_parent_and_domain_namespace_checked": "PARENTS.tsv + taxonomy.json with rs:/gui: prefixes normalised; no errors in either seat",
            "seat_schema_note": "son55 writes status as an object {state, reason} in all six records (contract: string + reason); value read from .state, no effect on judgements. sol uses bare domain sub IDs (e.g. C17) vs son55 gui:C17; final records use gui: prefixes.",
            "every_mechanical_conflict_has_resolution": True,
            "rating_resolutions_match_final_ratings": True,
            "final_rs_parent_and_domain_checks": True,
            "evidence_reference_integrity": "every evidence_id referenced in a final record exists in its evidence list; seat IDs namespaced sol:/son55:, own evidence agg:",
            "agg_quote_substring_check": "each agg quote asserted as an exact substring of the cited fixed text (paper or frozen reference)",
            "score_recomputed": "S=(15G+25M+20X+10Em+10Ec+10Eh+5Es+5Ecost)/4; weights sum 100, E sum 40; recomputed after write and asserted against hand-computed values",
            "final_record_hash_recomputed_after_write": True,
            "hash_rule": "sha256 of json.dumps(record minus final_record_hash, sort_keys=True, ensure_ascii=False, separators=(',',':')) in UTF-8",
            "atomic_writes": "tmp file + os.replace",
            "limitations": [
                "Structural/arithmetic/quote checks do not establish semantic correctness or scientific validity; nothing reproduced.",
                "MAI-UI (2512.22047) entered references.json after c3 seats ran; it was used only as a shared factual check for 2604.11784 and every use is listed in that record's shared_error_corrections.",
                "Figures are not rendered in the fixed HTML texts (e.g. MobileSteward Fig 5-6, MONDAY Fig 3-5, GUIrilla Fig 5-9, ClawGUI Fig 1-4); judgements use text/tables/captions only.",
                "No session id or invocation receipt is available to this agent.",
            ],
        },
        "requests_to_controller": [
            "None blocking. Optional for 2604.11784: if a later version states the MobileWorld settings used for the MAI-UI-2B/8B re-runs and the training-task source, E.measurement/E.causality/E.holdout could be re-checked (re-dispatch both seats on the new version).",
        ],
        "boundaries": "No publication, no Reel selection, no rubric/card/seat/input edits, no git operations. Scores are draft_uncalibrated v2.2 values pending controller verification.",
        "timestamp": now(),
    }
    write_atomic(OUT_DIR / "batch-report.json", report)
    for r in rows:
        print(r["paper_key"], r["aggregate_status"], r["raw_score"], "conf", r["n_mechanical_conflicts"],
              r["resolution_decisions"], "shared", r["n_shared_error_corrections"], "unres", r["n_unresolved"], r["final_record_hash"][:12])


if __name__ == "__main__":
    main()
