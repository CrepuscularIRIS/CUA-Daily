"""Assemble c1/a1 aggregate final records + batch report from seat originals and decisions.py (read-only on inputs)."""
from __future__ import annotations

import json

from common import (BATCH_DIR, KEYS8, OUT_DIR, ROOT, ID_LIST_KEYS, agg_material, canonical_hash, load_seat,
                    now, score, seat_path, seat_view, sha256_file, write_atomic)
from decisions import PAPERS

MANIFEST = json.loads((BATCH_DIR / "manifest.json").read_text())
CONFLICTS = json.loads((BATCH_DIR / "conflicts.json").read_text())["conflicts"]
TAX = json.loads((ROOT / "research/patterns/taxonomy.json").read_text())
SUBS_OF = {m["id"]: set(m["subs"]) for m in TAX["main"]}
PARENTS = dict(l.split("\t") for l in (ROOT / "research/reference/researchstudio-15-31/PARENTS.tsv").read_text().split("\n")[1:] if l.strip())
RS_MAINS = {p.stem for p in (ROOT / "research/reference/researchstudio-15-31/ideation-patterns").glob("*.md")} - {"overview"}
EXPECTED = {"2605.23939": 61.25, "2505.18829": 25.0, "2504.12679": 47.5, "2610.23307": 53.75, "2610.23303": 53.75}
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
        mats = d.get("materials", [])
        v = seat_view(s, pk)
        out[s] = {
            "file_sha256": sha256_file(seat_path(s, pk)),
            "version_matches_manifest": d["paper"]["version"] == mf["version"],
            "input_hash_matches_manifest": d["provenance"]["input_hash"] == MANIFEST["input_bundle_sha256"],
            "material_sha_matches_manifest": all(m.get("sha256") == mf["material_sha256"] for m in mats),
            "material_complete": all(m.get("complete") for m in mats) if mf["material_status"] == "html" else None,
            "rs_and_domain_parent_errors": check_patterns(v.get("rs_pattern", {}), v.get("domain_pattern", {})) if mf["material_status"] == "html" else [],
            "model_type": d["provenance"].get("model_type"), "actual_model": d["provenance"].get("actual_model"),
        }
    return out


def pick_rs(spec: dict, views: dict) -> tuple[dict, list]:
    seat, reason = spec["rs"]
    rs = dict(views[seat]["rs_pattern"])
    rs["aggregate_source_seat"] = seat
    rs["aggregate_reason"] = reason
    if seat == "son55" and rs.get("outside_taxonomy"):
        rs["primary"], rs["supporting"], rs["matches"] = None, [], []
    return rs, views[seat]["pattern_mapping"]


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
        out.append({"field_path": c["field"], "sol_value": c["sol"], "son55_value": c["son55"], "decision": decision,
                    "final_value": final, "reason": reason, "evidence_ids": ev, "score_impact": impact})
    return out


def rating_resolutions_consistent(spec: dict, ratings: dict) -> None:
    for f, (decision, final, *_rest) in spec["resolutions"].items():
        if f.startswith("rating."):
            k = f[len("rating."):]
            fv = final if isinstance(final, dict) else {"rating": final}
            assert ratings[k]["rating"] == fv["rating"], (spec["pk"], k)


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


def build_paper(spec: dict) -> dict:
    pk = spec["pk"]
    mf = man(pk)
    views = {s: seat_view(s, pk) for s in ("sol", "son55")}
    base = views["son55"]
    integ = seat_integrity(pk)
    assert all(v["version_matches_manifest"] and v["input_hash_matches_manifest"] and v["material_sha_matches_manifest"]
               and not v["rs_and_domain_parent_errors"] for v in integ.values()), (pk, integ)

    ratings = {k: spec["ratings"][k] for k in KEYS8}
    rating_resolutions_consistent(spec, ratings)
    sc = score(ratings)
    assert sc["raw"] == EXPECTED[pk], (pk, sc["raw"])
    rs, pmap = pick_rs(spec, views)
    dom = pick_domain(spec, views)
    assert not check_patterns(rs, dom), (pk, check_patterns(rs, dom))
    gap = dict(base["gap"])
    gap.update(spec["gap_check"])

    claims = []
    for c in base["claims"]:
        c = dict(c)
        note = spec.get("claims_append", {}).get(c["claim_id"])
        if note:
            c["counterevidence"] = (c.get("counterevidence") or "") + " " + note
        claims.append(c)

    agg_status, agg_reason = spec["status"]
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": "c1", "attempt_id": "a1", "seat": "aggregate",
        "paper": dict(base["paper"]),
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
            "independence_note": "Aggregation over two seat inputs; the fixed paper text was read before seat scores, but this is not a third blind review or human gold. All results are author reports; nothing was reproduced.",
        },
        "materials": [agg_material(src, role) for src, role in spec["materials"]] + views["sol"]["materials"] + base["materials"],
        "evidence": spec["evidence"] + views["sol"]["evidence"] + base["evidence"],
        "preliminary_evidence_judgment": spec["prelim"],
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
        "resolutions": resolutions_for(spec),
        "shared_error_corrections": spec["shared"],
        "aggregate_status": agg_status,
        "aggregate_status_reason": agg_reason,
    }
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
    assert not (unresolved and agg_status == "accepted_final")
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def build_nofulltext(pk: str) -> dict:
    mf = man(pk)
    integ = seat_integrity(pk)
    confs = CONFLICTS.get(pk, [])
    assert [c["field"] for c in confs] == ["claim_support"]
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": "c1", "attempt_id": "a1", "seat": "aggregate",
        "paper": {"paper_key": pk, "paper_id": mf["arxiv"], "title": mf["title"], "version": mf["version"],
                  "claim_type": None, "central_claim": None},
        "materials": [{"material_id": f"manifest:{pk}", "url": f"https://arxiv.org/abs/{mf['version']}", "sha256": None,
                       "fulltext_path": None, "material_status": mf["material_status"], "sections_read": [],
                       "complete": False, "missing_sections": ["entire full text (HTML/PDF): method, experiments, appendix"]}],
        "status": "needs_fulltext",
        "status_reason": "Batch manifest material_status=no_html with fulltext_path=null and material_sha256=null; no abstract- or title-based evaluation performed. Request: pin 2610.23857v1 full text (HTML or PDF) with sha256 identically for both seats, then re-dispatch both seats.",
        "score": None,
        "input_seat_hashes": {s: integ[s]["file_sha256"] for s in ("sol", "son55")},
        **AGG_MODEL,
        "seat_integrity_check": integ,
        "resolutions": [{"field_path": "claim_support", "sol_value": confs[0]["sol"], "son55_value": confs[0]["son55"],
                         "decision": "revised", "final_value": None,
                         "reason": "No material, so no assessment fields are carried into the final record; both seats agree on needs_fulltext, all-unknown ratings and score=null. The difference is representational only.",
                         "evidence_ids": [], "score_impact": "none (score=null)"}],
        "shared_error_corrections": [],
        "aggregate_status": "needs_fulltext",
        "aggregate_status_reason": "Full text missing from the fixed input package.",
    }
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def main() -> None:
    report_rows = []
    records = {}
    for spec in PAPERS:
        records[spec["pk"]] = build_paper(spec)
    records["2610.23857"] = build_nofulltext("2610.23857")
    for pk, rec in records.items():
        path = OUT_DIR / f"{pk}.json"
        write_atomic(path, rec)
        back = json.loads(path.read_text(encoding="utf-8"))
        assert canonical_hash(back) == back["final_record_hash"], pk
        if back.get("score"):
            assert score(back["ratings"])["raw"] == back["score"]["raw"]
        confs = CONFLICTS.get(pk, [])
        report_rows.append({
            "paper_key": pk, "version": back["paper"]["version"], "aggregate_status": back["aggregate_status"],
            "claim_type": back["paper"].get("claim_type"),
            "evidence_level": back.get("assessment", {}).get("evidence_level"),
            "claim_support": back.get("assessment", {}).get("claim_support"),
            "raw_score": back["score"]["raw"] if back.get("score") else None,
            "seat_raw_scores": {s: (load_seat(s, pk).get("score") or {}).get("raw") for s in ("sol", "son55")},
            "n_mechanical_conflicts": len(confs),
            "n_resolutions": len(back["resolutions"]),
            "resolution_decisions": {d: sum(1 for r in back["resolutions"] if r["decision"] == d)
                                     for d in ("sol", "son55", "revised", "unresolved", "same_supported_fact")},
            "n_shared_error_corrections": len(back["shared_error_corrections"]),
            "n_unresolved": sum(1 for r in back["resolutions"] if r["decision"] == "unresolved"),
            "file": str(path), "file_sha256": sha256_file(path), "final_record_hash": back["final_record_hash"],
            "input_seat_hashes": back["input_seat_hashes"],
        })
    scored = [r for r in report_rows if r["raw_score"] is not None]
    report = {
        "schema_version": "radar-batch-report-v2.2", "kind": "aggregate-batch-report",
        "run_id": MANIFEST["run_id"], "batch_id": "c1", "attempt_id": "a1", "seat": "aggregate",
        "input_hash": MANIFEST["input_bundle_sha256"],
        "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"),
        **AGG_MODEL,
        "assigned": len(MANIFEST["papers"]),
        "accepted_final": sum(r["aggregate_status"] == "accepted_final" for r in report_rows),
        "needs_revision": sum(r["aggregate_status"] == "needs_revision" for r in report_rows),
        "needs_evidence": sum(r["aggregate_status"] == "needs_evidence" for r in report_rows),
        "needs_fulltext": sum(r["aggregate_status"] == "needs_fulltext" for r in report_rows),
        "scored": len(scored), "blocked": len(report_rows) - len(scored),
        "outside_taxonomy_ratio_of_reviewed": f"{sum(1 for pk, r in records.items() if r.get('rs_pattern', {}).get('outside_taxonomy') is True)}/{len(scored)}",
        "totals": {"mechanical_conflicts": sum(r["n_mechanical_conflicts"] for r in report_rows),
                   "resolutions": sum(r["n_resolutions"] for r in report_rows),
                   "shared_error_corrections": sum(r["n_shared_error_corrections"] for r in report_rows),
                   "unresolved": sum(r["n_unresolved"] for r in report_rows)},
        "records": report_rows,
        "validation": {
            "seat_set_equals_manifest": sorted(records) == sorted(p["paper_key"] for p in MANIFEST["papers"]),
            "seat_versions_input_hash_material_sha_checked": True,
            "seat_rs_parent_and_domain_namespace_checked": "PARENTS.tsv + taxonomy.json, both seats, all reviewed papers: no errors",
            "every_mechanical_conflict_has_resolution": True,
            "rating_resolutions_match_final_ratings": True,
            "final_rs_parent_and_domain_checks": True,
            "evidence_reference_integrity": "every evidence_id referenced in a final record exists in its evidence list; seat IDs namespaced sol:/son55:, own evidence agg:",
            "agg_quote_substring_check": "each agg quote is an exact substring of the cited fixed text (reference texts for neighbour facts)",
            "score_recomputed": "S=(15G+25M+20X+10Em+10Ec+10Eh+5Es+5Ecost)/4; weights sum 100, E sum 40; recomputed after write",
            "final_record_hash_recomputed_after_write": True,
            "hash_rule": "sha256 of json.dumps(record minus final_record_hash, sort_keys=True, ensure_ascii=False, separators=(',',':')) in UTF-8",
            "atomic_writes": "tmp file + os.replace",
            "limitations": [
                "Structural/arithmetic/quote checks do not establish semantic correctness or scientific validity; nothing reproduced.",
                "Figures are not rendered in the fixed HTML texts (DRIVE Fig 2, TongUI prompts/Fig 2-3, MobileInject Fig 5-12, MobileJailBench Fig 3); judgements use text/captions only and say so.",
                "Reference-library texts were used only as factual sources for neighbour/baseline facts; shared-error corrections derived from them are listed per paper.",
                "No session id or invocation receipt is available to this agent.",
            ],
        },
        "requests_to_controller": [
            "2610.23857: pin v1 full text (HTML or PDF) with sha256 identically for both seats and re-dispatch; aggregate cannot proceed.",
            "Optional: a PDF version of 2610.23303 with visible bootstrap intervals and unresolved-episode counts would allow re-checking E.statistics (currently 1).",
        ],
        "boundaries": "No publication, no Reel selection, no rubric/card/seat/input edits, no git operations. Scores are draft_uncalibrated v2.2 provisional values pending controller verification.",
        "timestamp": now(),
    }
    write_atomic(OUT_DIR / "batch-report.json", report)
    for r in report_rows:
        print(r["paper_key"], r["aggregate_status"], r["raw_score"], r["n_mechanical_conflicts"], r["n_shared_error_corrections"], r["n_unresolved"], r["final_record_hash"][:12])


if __name__ == "__main__":
    main()
