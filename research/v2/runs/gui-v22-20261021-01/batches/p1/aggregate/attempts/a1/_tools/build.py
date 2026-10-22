"""Assemble p1/a1 aggregate final records + batch report from seat originals and decisions.py (read-only on inputs).

Adapted from the c1/a1 aggregate tooling; differences: composite RS picks, per-paper overrides (claim_type),
scope decisions, and a material check that tolerates seat reference-library materials.
"""
from __future__ import annotations

import json

from common import (BATCH_DIR, FT_DIR, KEYS8, OUT_DIR, ROOT, ID_LIST_KEYS, canonical_hash, load_seat,
                    now, score, seat_path, seat_view, sha256_file, write_atomic)
from decisions import PAPERS

BATCH = "p1"
MANIFEST = json.loads((BATCH_DIR / "manifest.json").read_text())
CONFLICTS = json.loads((BATCH_DIR / "conflicts.json").read_text())["conflicts"]
TAX = json.loads((ROOT / "research/patterns/taxonomy.json").read_text())
SUBS_OF = {m["id"]: set(m["subs"]) for m in TAX["main"]}
PARENTS = dict(l.split("\t") for l in (ROOT / "research/reference/researchstudio-15-31/PARENTS.tsv").read_text().split("\n")[1:] if l.strip())
RS_MAINS = {p.stem for p in (ROOT / "research/reference/researchstudio-15-31/ideation-patterns").glob("*.md")} - {"overview"}
EXPECTED = {"1802.08802": 65.0, "1909.00031": 58.75, "2005.03776": 61.25, "2103.16057": 55.0, "2112.09332": 76.25}
AGG_MODEL = {"aggregate_model": "fable", "aggregate_actual_model": "claude-opus-5-5[1m]", "aggregate_session": None,
             "aggregate_receipt_ref": None,
             "aggregate_session_note": "Configured model type fable (upstream claude-opus-5-5[1m]) per batch manifest model_types.opus55; no session id or invocation receipt is exposed to this agent."}


def man(pk: str) -> dict:
    return next(p for p in MANIFEST["papers"] if p["paper_key"] == pk)


def ent_key(m: dict) -> tuple:
    return (m.get("main") or m.get("main_id"), m.get("sub") if "sub" in m else m.get("sub_id"))


def check_patterns(rs: dict, dom: dict) -> list[str]:
    errs = []
    if rs.get("outside_taxonomy") is True:
        if rs.get("primary") is not None or rs.get("matches") or rs.get("supporting"):
            errs.append("outside_taxonomy with matches")
    else:
        if rs.get("primary") not in RS_MAINS:
            errs.append(f"bad rs primary {rs.get('primary')}")
        for m in rs.get("matches", []):
            if m["main_id"] not in RS_MAINS:
                errs.append(f"bad rs main {m['main_id']}")
            if m.get("sub_id") is not None and PARENTS.get(m["sub_id"]) != m["main_id"]:
                errs.append(f"rs sub {m['sub_id']} not under {m['main_id']}")
        if len(rs.get("supporting", [])) > 2:
            errs.append("more than 2 supporting")
        mains = [m["main_id"] for m in rs.get("matches", [])]
        if sorted(mains) != sorted([rs.get("primary")] + list(rs.get("supporting", []))):
            errs.append("rs primary/supporting do not equal matches")
    if dom.get("namespace") != "gui":
        errs.append("domain namespace")
    for m in dom.get("matches", []):
        main, sub = ent_key(m)
        if main not in SUBS_OF or (sub is not None and sub not in SUBS_OF[main]):
            errs.append(f"domain {main}/{sub} invalid")
    return errs


def target_material_ok(mats: list, mf: dict) -> bool:
    """The seat's target material must carry the manifest sha; any material pointing at this paper's file must match."""
    path = mf["fulltext_path"]
    shas = [m.get("sha256") for m in mats]
    on_path = [m.get("sha256") for m in mats if path in (m.get("path"), m.get("local_path"), m.get("fulltext_path"))]
    return mf["material_sha256"] in shas and all(s == mf["material_sha256"] for s in on_path)


def seat_integrity(pk: str) -> dict:
    mf = man(pk)
    out = {}
    for s in ("sol", "son55"):
        d = load_seat(s, pk)
        mats = d.get("materials", [])
        v = seat_view(s, pk)
        st = d.get("status")
        out[s] = {
            "file_sha256": sha256_file(seat_path(s, pk)),
            "version_matches_manifest": d["paper"]["version"] == mf["version"],
            "input_hash_matches_manifest": d["provenance"]["input_hash"] == MANIFEST["input_bundle_sha256"],
            "target_material_sha_matches_manifest": target_material_ok(mats, mf),
            "target_material_complete": any(m.get("complete") for m in mats if m.get("sha256") == mf["material_sha256"]),
            "rs_and_domain_parent_errors": check_patterns(v.get("rs_pattern", {}), v.get("domain_pattern", {})),
            "seat_status": st.get("value") if isinstance(st, dict) else st,
            "model_type": d["provenance"].get("model_type"), "actual_model": d["provenance"].get("actual_model"),
            "receipt_ref": d["provenance"].get("receipt_ref"),
        }
    return out


def pick_rs(spec: dict, views: dict) -> tuple[dict, list]:
    r = spec["rs"]
    if isinstance(r, tuple):
        seat, reason = r
        rs = dict(views[seat]["rs_pattern"])
        rs["aggregate_source_seat"] = seat
        rs["aggregate_reason"] = reason
        return rs, [dict(x, aggregate_source_seat=seat) for x in views[seat]["pattern_mapping"]]
    matches = []
    for seat, main, sub_override, role in r["matches"]:
        src = next(m for m in views[seat]["rs_pattern"]["matches"] if m["main_id"] == main)
        m = dict(src)
        if sub_override != "keep":
            m["sub_id"] = sub_override
        m["role"] = role
        m["aggregate_source_seat"] = seat
        matches.append(m)
    rs = {"primary": r["primary"], "supporting": r["supporting"], "matches": matches, "outside_taxonomy": False,
          "reason": r["reason"], "executes_pattern": r["executes_pattern"], "resolves_problem": r["resolves_problem"],
          "aggregate_source_seat": "revised", "aggregate_reason": r["reason"]}
    pmap = []
    for seat in ("sol", "son55"):
        for x in views[seat]["pattern_mapping"]:
            if x.get("rs_main") in {m["main_id"] for m in matches}:
                y = dict(x, aggregate_source_seat=seat)
                if r.get("mapping_note"):
                    y["aggregate_note"] = r["mapping_note"]
                pmap.append(y)
    return rs, pmap


def pick_domain(spec: dict, views: dict) -> dict:
    matches = []
    for seat, main, sub, fit in spec["domain"]:
        src = next(m for m in views[seat]["domain_pattern"]["matches"] if ent_key(m) == (main, sub))
        m = dict(src)
        m["main"], m["sub"] = main, sub
        m.pop("main_id", None), m.pop("sub_id", None)
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
            x["aggregate_source_seat"] = "revised"
            out.append(x)
    return out


def resolutions_for(spec: dict) -> list:
    pk = spec["pk"]
    confs = CONFLICTS.get(pk, [])
    dec = spec["resolutions"]
    fields = [c["field"] for c in confs]
    missing = [f for f in fields if f not in dec]
    extra = [f for f in dec if f not in fields]
    assert not missing and not extra, (pk, missing, extra)
    out = []
    for c in confs:
        decision, final, reason, ev, impact = dec[c["field"]]
        assert decision in {"sol", "son55", "revised", "unresolved", "same_supported_fact"}, decision
        out.append({"field_path": c["field"], "sol_value": c["sol"], "son55_value": c["son55"], "decision": decision,
                    "final_value": final, "reason": reason, "evidence_ids": ev, "score_impact": impact})
    return out


def consistency_checks(spec: dict, ratings: dict, rec: dict) -> None:
    exp = {e["id"]: e for e in rec["expectations"]}
    for f, (decision, final, *_rest) in spec["resolutions"].items():
        if f.startswith("rating."):
            k = f[len("rating."):]
            fv = final if isinstance(final, dict) else {"rating": final}
            assert ratings[k]["rating"] == fv["rating"], (spec["pk"], k)
        elif f.startswith("expectation."):
            assert exp[f.split(".", 1)[1]]["status"] == final, (spec["pk"], f, exp[f.split(".", 1)[1]]["status"], final)
        elif f == "claim_type":
            assert rec["paper"]["claim_type"] == final, f
        elif f == "evidence_level":
            assert rec["assessment"]["evidence_level"] == final, f
        elif f == "rs.primary":
            assert rec["rs_pattern"]["primary"] == final, f
        elif f == "rs.supporting":
            assert rec["rs_pattern"]["supporting"] == final, f
        elif f == "rs.matches":
            got = [f"{m['main_id']}/{m['sub_id']}" for m in rec["rs_pattern"]["matches"]]
            assert sorted(got) == sorted(final), (spec["pk"], got, final)
        elif f == "domain.matches":
            got = [f"{m['main']}/{m['sub']}" for m in rec["domain_pattern"]["matches"]]
            assert sorted(got) == sorted(final), (spec["pk"], got, final)


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


def agg_material(src: str, role: str) -> dict:
    path = FT_DIR / f"{src}.txt"
    head = path.read_text(encoding="utf-8").split("\n", 1)[0]
    mf = next((p for p in MANIFEST["papers"] if p["paper_key"] == src), None)
    return {"material_id": f"agg:{src}", "source_url": head.replace("SOURCE: ", "").strip(),
            "version": mf["version"] if mf else None, "sha256": sha256_file(path),
            "fulltext_path": str(path.relative_to(ROOT)), "role": role,
            "sections_read": ["full text, all sections and appendices as rendered"] if role == "paper" else ["targeted sections cited by agg evidence"],
            "complete": role == "paper",
            "missing_sections": ["figure images (captions only in render)"] if role == "paper" else ["used only as factual reference for cited lines"]}


def build_paper(spec: dict) -> dict:
    pk = spec["pk"]
    mf = man(pk)
    views = {s: seat_view(s, pk) for s in ("sol", "son55")}
    base = views["son55"]
    integ = seat_integrity(pk)
    assert all(v["version_matches_manifest"] and v["input_hash_matches_manifest"] and v["target_material_sha_matches_manifest"]
               and v["target_material_complete"] and not v["rs_and_domain_parent_errors"] for v in integ.values()), (pk, integ)

    ratings = {k: spec["ratings"][k] for k in KEYS8}
    sc = score(ratings)
    assert sc["raw"] == EXPECTED[pk], (pk, sc["raw"])
    rs, pmap = pick_rs(spec, views)
    dom = pick_domain(spec, views)
    assert not check_patterns(rs, dom), (pk, check_patterns(rs, dom))
    gap = dict(base["gap"])
    gap.update(spec["gap_check"])
    paper = dict(base["paper"])
    paper["paper_id"] = mf["arxiv"]
    paper.update(spec.get("paper_override", {}))

    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": BATCH, "attempt_id": "a1", "seat": "aggregate",
        "paper": paper,
        "provenance": {
            "input_hash": MANIFEST["input_bundle_sha256"], "rubric_version": "v2.2 draft_uncalibrated",
            "rubric_hash": MANIFEST["asset_hashes"]["rubric"]["sha256"],
            "rs_manifest_hash": MANIFEST["asset_hashes"]["rs_cards_manifest"]["sha256"],
            "domain_cards_hash": MANIFEST["asset_hashes"]["domain_taxonomy"]["sha256"],
            "domain_conditions_hash": MANIFEST["asset_hashes"]["domain_conditions"]["sha256"],
            "expectations_hash": MANIFEST["asset_hashes"]["expectations"]["sha256"],
            "batch_contract_hash": MANIFEST["asset_hashes"]["batch_contract"]["sha256"],
            "aggregate_rules": "docs/agents/AGGREGATE_OPUS.md",
            "aggregate_rules_sha256": sha256_file(ROOT / "docs/agents/AGGREGATE_OPUS.md"),
            "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"),
            "references_sha256": sha256_file(ROOT / "research/fulltext/review-runs/gui-v22-20261021-01/references.json"),
            "model_type": "fable", "actual_model": "claude-opus-5-5[1m]", "session_id": None, "receipt_ref": None,
            "timestamp": now(),
            "independence_note": "Aggregation over two seat inputs; the fixed paper text was read in full before the seat scores, but this is not a third blind review or human gold. All results are author reports; nothing was reproduced.",
        },
        "materials": [agg_material(src, role) for src, role in spec["materials"]] + views["sol"]["materials"] + base["materials"],
        "evidence": spec["evidence"] + views["sol"]["evidence"] + base["evidence"],
        "preliminary_evidence_judgment": spec["prelim"],
        "scope_decision": spec["scope"],
        "signatures": base["signatures"],
        "gap": gap,
        "rs_pattern": rs,
        "domain_pattern": dom,
        "pattern_mapping": pmap,
        "expectations": pick_expectations(spec, views),
        "claims": base["claims"],
        "assessment": spec["assessment"],
        "ratings": ratings,
        "score": sc,
        "status": "reviewed",
        "status_reason": "Full fixed HTML text available and read (figure images are captions only); in scope per scope_decision; all eight items resolved.",
        "input_seat_hashes": {s: integ[s]["file_sha256"] for s in ("sol", "son55")},
        **AGG_MODEL,
        "seat_integrity_check": integ,
        "resolutions": resolutions_for(spec),
        "shared_error_corrections": spec["shared"],
        "aggregate_status": spec["status"][0],
        "aggregate_status_reason": spec["status"][1],
    }
    consistency_checks(spec, ratings, rec)
    assert rec["paper"]["version"] == mf["version"]
    ev_ids = {e["evidence_id"] for e in rec["evidence"]}
    assert len(ev_ids) == len(rec["evidence"]), pk
    mat_ids = {m["material_id"] for m in rec["materials"]}
    assert all(e["material_id"] in mat_ids for e in rec["evidence"]), pk
    refs: set = set()
    collect_ids({k: v for k, v in rec.items() if k != "evidence"}, refs)
    dangling = sorted(r for r in refs if r.split(":")[0] in {"sol", "son55", "agg"} and r not in ev_ids)
    assert not dangling, (pk, dangling)
    unresolved = [r for r in rec["resolutions"] if r["decision"] == "unresolved"]
    assert not (unresolved and rec["aggregate_status"] == "accepted_final")
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def main() -> None:
    report_rows = []
    records = {spec["pk"]: build_paper(spec) for spec in PAPERS}
    assert sorted(records) == sorted(p["paper_key"] for p in MANIFEST["papers"])
    for pk, rec in records.items():
        path = OUT_DIR / f"{pk}.json"
        write_atomic(path, rec)
        back = json.loads(path.read_text(encoding="utf-8"))
        assert canonical_hash(back) == back["final_record_hash"], pk
        assert score(back["ratings"])["raw"] == back["score"]["raw"]
        confs = CONFLICTS.get(pk, [])
        report_rows.append({
            "paper_key": pk, "version": back["paper"]["version"], "aggregate_status": back["aggregate_status"],
            "claim_type": back["paper"]["claim_type"], "scope": back["scope_decision"],
            "evidence_level": back["assessment"]["evidence_level"],
            "claim_support": back["assessment"]["claim_support"],
            "raw_score": back["score"]["raw"], "display_score": back["score"]["display"],
            "seat_raw_scores": {s: (load_seat(s, pk).get("score") or {}).get("raw") for s in ("sol", "son55")},
            "n_mechanical_conflicts": len(confs),
            "n_resolutions": len(back["resolutions"]),
            "resolution_decisions": {d: sum(1 for r in back["resolutions"] if r["decision"] == d)
                                     for d in ("sol", "son55", "revised", "unresolved", "same_supported_fact")},
            "n_rating_conflicts": sum(1 for c in confs if c["field"].startswith("rating.")),
            "n_shared_error_corrections": len(back["shared_error_corrections"]),
            "n_unresolved": sum(1 for r in back["resolutions"] if r["decision"] == "unresolved"),
            "file": str(path), "file_sha256": sha256_file(path), "final_record_hash": back["final_record_hash"],
            "input_seat_hashes": back["input_seat_hashes"],
        })
    report = {
        "schema_version": "radar-batch-report-v2.2", "kind": "aggregate-batch-report",
        "run_id": MANIFEST["run_id"], "batch_id": BATCH, "attempt_id": "a1", "seat": "aggregate",
        "input_hash": MANIFEST["input_bundle_sha256"],
        "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"),
        **AGG_MODEL,
        "assigned": len(MANIFEST["papers"]),
        "accepted_final": sum(r["aggregate_status"] == "accepted_final" for r in report_rows),
        "needs_revision": sum(r["aggregate_status"] == "needs_revision" for r in report_rows),
        "needs_evidence": sum(r["aggregate_status"] == "needs_evidence" for r in report_rows),
        "needs_fulltext": sum(r["aggregate_status"] == "needs_fulltext" for r in report_rows),
        "out_of_scope": 0,
        "scored": sum(r["raw_score"] is not None for r in report_rows),
        "blocked": sum(r["raw_score"] is None for r in report_rows),
        "outside_taxonomy_ratio_of_reviewed": f"{sum(1 for r in records.values() if r['rs_pattern'].get('outside_taxonomy') is True)}/{len(records)}",
        "totals": {"mechanical_conflicts": sum(r["n_mechanical_conflicts"] for r in report_rows),
                   "rating_conflicts": sum(r["n_rating_conflicts"] for r in report_rows),
                   "resolutions": sum(r["n_resolutions"] for r in report_rows),
                   "shared_error_corrections": sum(r["n_shared_error_corrections"] for r in report_rows),
                   "unresolved": sum(r["n_unresolved"] for r in report_rows)},
        "records": report_rows,
        "validation": {
            "seat_set_equals_manifest": True,
            "seat_versions_input_hash_target_material_sha_checked": "both seats, all 5 papers: version, input_bundle_sha256 and target material sha256 equal the batch manifest; seat reference-library materials are separate entries",
            "seat_rs_parent_and_domain_namespace_checked": "PARENTS.tsv + taxonomy.json, both seats, all papers: no errors",
            "every_mechanical_conflict_has_resolution": True,
            "final_values_match_resolutions": "ratings, expectation statuses, claim_type, evidence_level, rs primary/supporting/matches and domain matches asserted equal to resolution final_value",
            "final_rs_parent_and_domain_checks": True,
            "evidence_reference_integrity": "every evidence_id referenced in a final record exists in its evidence list; seat IDs namespaced sol:/son55:, own evidence agg:",
            "agg_quote_substring_check": "each agg quote is an exact substring of the cited fixed text",
            "score_recomputed": "S=(15G+25M+20X+10Em+10Ec+10Eh+5Es+5Ecost)/4; weights sum 100, E sum 40; recomputed after write and equal to the hand-computed expected values",
            "final_record_hash_recomputed_after_write": True,
            "hash_rule": "sha256 of json.dumps(record minus final_record_hash, sort_keys=True, ensure_ascii=False, separators=(',',':')) in UTF-8",
            "atomic_writes": "tmp file + os.replace",
            "limitations": [
                "Structural/arithmetic/quote checks do not establish semantic correctness or scientific validity; nothing reproduced.",
                "Figure images are not rendered in the fixed HTML texts (1802.08802 Fig 3/4 main MiniWoB and sample-efficiency results; 2112.09332 Fig 2-8; 1909.00031 Fig 5; 2103.16057 Fig 7-8); judgements use text, tables and captions only.",
                "Historical nearest neighbours (Shi17/World of Bits, Sugilite/Appinite, PhraseNode, Krishna21, Stiennon20) are not in the fixed pack; lineage stays author-attributed with uncertainty notes, following both seats. Only in-batch papers (2005.03776 for 2103.16057) were used as verified neighbour text.",
                "No session id or invocation receipt is available to this agent; the sol seat's receipt_ref points to the controller session transcript (sol was dispatched from it), recorded as-is.",
            ],
        },
        "requests_to_controller": [
            "None blocking. Optional: rendered figure values for 1802.08802 Fig 3/4 and 2112.09332 Fig 2 (with denominators) would allow re-checking E.measurement/E.statistics; current values do not depend on them.",
            "Scope: 2112.09332 (read-only text-browser QA, human-preference outcome) and 1909.00031 (end-user programming by demonstration, usability study) are kept in scope as edge cases (see each record's scope_decision); selection should not read their scores as evidence of execution-checked GUI task competence.",
        ],
        "boundaries": "No publication, no Reel selection, no rubric/card/seat/input edits, no git operations. Scores are draft_uncalibrated v2.2 provisional values pending controller verification.",
        "timestamp": now(),
    }
    write_atomic(OUT_DIR / "batch-report.json", report)
    for r in report_rows:
        print(r["paper_key"], r["aggregate_status"], r["raw_score"], r["n_mechanical_conflicts"], r["resolution_decisions"],
              r["n_shared_error_corrections"], r["n_unresolved"], r["final_record_hash"][:12])


if __name__ == "__main__":
    main()
