"""Assemble p2/a1 aggregate final records + batch report from seat originals and decisions.py (read-only on inputs)."""
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
EXPECTED = {"2202.08137": 68.75, "2304.07061": 36.25, "2305.11854": 66.25}
SKIPPED = {"2209.08655": "skipped_a2_pending", "2303.17491": "skipped_a2_pending"}
SKIP_REASON = ("material_upgraded_a2_pending: the shared fixed full-text file was replaced by a repaired version after a1 froze; "
               "both seats' a1 records stay bound to the old sha and are retained, but no a1 aggregation is performed. "
               "The aggregator did not evaluate these papers and did not open their upgraded files.")
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
        mats = [m for m in d.get("materials", []) if pk in m["material_id"] or pk in (m.get("url") or "")]  # paper material only
        assert len(mats) == 1, (pk, s, [m["material_id"] for m in d.get("materials", [])])
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
    if "custom" in spec["rs"]:
        c = spec["rs"]["custom"]
        matches = []
        for main, seat in c["base_from"].items():
            m = dict(next(x for x in views[seat]["rs_pattern"]["matches"] if x["main_id"] == main))
            m["role"] = "primary" if main == c["primary"] else "supporting"
            m["aggregate_source_seat"] = seat
            matches.append(m)
        rs = {k: c[k] for k in ("primary", "supporting", "outside_taxonomy", "reason", "executes_pattern", "resolves_problem")}
        rs["matches"] = matches
        rs["aggregate_source_seat"] = "revised"
        pmap = []
        for seat, rs_main, dom_main in spec["rs"]["pmap"]:
            for x in views[seat]["pattern_mapping"]:
                dm = x.get("domain_main") or (x.get("domain") or {}).get("main")
                if x.get("rs_main") == rs_main and dm == dom_main:
                    pmap.append(dict(x, aggregate_source_seat=seat))
        assert len(pmap) == len(spec["rs"]["pmap"]), (spec["pk"], pmap)
        return rs, pmap
    seat, reason = spec["rs"]["seat"], spec["rs"]["reason"]
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
            "revision_proposals": son.get("revision_proposals", []) + spec.get("domain_extra_proposals", []),
            "aggregate_note": spec["domain_note"]}


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
            c["aggregate_note"] = note
        claims.append(c)

    agg_status, agg_reason = spec["status"]
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": MANIFEST["run_id"], "batch_id": "p2", "attempt_id": "a1", "seat": "aggregate",
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
        "status_reason": "Full fixed HTML text available and read (figures are not rendered in the v1 render; judgements use text, tables and captions); all eight items resolved.",
        "seat_evidence_not_verifiable": spec.get("unverifiable", {}),
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
    used: set = set()  # final decisions must not rest on seat evidence from replaced materials
    collect_ids({k: rec[k] for k in ("ratings", "resolutions", "shared_error_corrections")}, used)
    assert not (used & set(spec.get("unverifiable", {}))), pk
    unresolved = [r for r in rec["resolutions"] if r["decision"] == "unresolved"]
    assert not (unresolved and agg_status == "accepted_final")
    rec["final_record_hash"] = canonical_hash(rec)
    return rec


def main() -> None:
    report_rows = []
    records = {spec["pk"]: build_paper(spec) for spec in PAPERS}
    assert sorted([*records, *SKIPPED]) == sorted(p["paper_key"] for p in MANIFEST["papers"])
    for pk, rec in records.items():
        path = OUT_DIR / f"{pk}.json"
        write_atomic(path, rec)
        back = json.loads(path.read_text(encoding="utf-8"))
        assert canonical_hash(back) == back["final_record_hash"], pk
        assert score(back["ratings"])["raw"] == back["score"]["raw"] == EXPECTED[pk]
        confs = CONFLICTS.get(pk, [])
        report_rows.append({
            "paper_key": pk, "version": back["paper"]["version"], "aggregate_status": back["aggregate_status"],
            "claim_type": back["paper"].get("claim_type"),
            "evidence_level": back["assessment"]["evidence_level"],
            "claim_support": back["assessment"]["claim_support"],
            "raw_score": back["score"]["raw"], "display_score": back["score"]["display"],
            "seat_raw_scores": {s: (load_seat(s, pk).get("score") or {}).get("raw") for s in ("sol", "son55")},
            "n_mechanical_conflicts": len(confs),
            "n_resolutions": len(back["resolutions"]),
            "resolution_decisions": {d: sum(1 for r in back["resolutions"] if r["decision"] == d)
                                     for d in ("sol", "son55", "revised", "unresolved", "same_supported_fact")},
            "n_scoring_item_conflicts": sum(1 for c in confs if c["field"].startswith("rating.")),
            "n_shared_error_corrections": len(back["shared_error_corrections"]),
            "n_unresolved": sum(1 for r in back["resolutions"] if r["decision"] == "unresolved"),
            "seat_evidence_not_verifiable": sorted(back["seat_evidence_not_verifiable"]),
            "file": str(path.relative_to(ROOT)), "file_sha256": sha256_file(path), "final_record_hash": back["final_record_hash"],
            "input_seat_hashes": back["input_seat_hashes"],
        })
    skipped_rows = [{
        "paper_key": pk, "version": man(pk)["version"], "disposition": disp, "aggregate_status": None, "raw_score": None,
        "reason": SKIP_REASON,
        "a1_seat_files_retained": {s: {"path": str(seat_path(s, pk).relative_to(ROOT)), "sha256": sha256_file(seat_path(s, pk))}
                                   for s in ("sol", "son55")},
        "n_mechanical_conflicts_not_processed": len(CONFLICTS.get(pk, [])),
    } for pk, disp in SKIPPED.items()]
    report = {
        "schema_version": "radar-batch-report-v2.2", "kind": "aggregate-batch-report",
        "run_id": MANIFEST["run_id"], "batch_id": "p2", "attempt_id": "a1", "seat": "aggregate",
        "input_hash": MANIFEST["input_bundle_sha256"],
        "conflicts_sha256": sha256_file(BATCH_DIR / "conflicts.json"),
        **AGG_MODEL,
        "assigned_in_manifest": len(MANIFEST["papers"]),
        "in_scope_for_a1_aggregation": len(records),
        "skipped_a2_pending": len(SKIPPED),
        "accepted_final": sum(r["aggregate_status"] == "accepted_final" for r in report_rows),
        "needs_revision": sum(r["aggregate_status"] == "needs_revision" for r in report_rows),
        "needs_evidence": sum(r["aggregate_status"] == "needs_evidence" for r in report_rows),
        "needs_fulltext": sum(r["aggregate_status"] == "needs_fulltext" for r in report_rows),
        "scored": len(report_rows), "blocked": 0,
        "disposition_sum_check": f"{len(report_rows)} aggregated + {len(SKIPPED)} skipped_a2_pending = {len(MANIFEST['papers'])} in manifest",
        "outside_taxonomy_ratio_of_reviewed": f"{sum(1 for r in records.values() if r['rs_pattern'].get('outside_taxonomy') is True)}/{len(records)}",
        "totals": {"mechanical_conflicts": sum(r["n_mechanical_conflicts"] for r in report_rows),
                   "scoring_item_conflicts": sum(r["n_scoring_item_conflicts"] for r in report_rows),
                   "resolutions": sum(r["n_resolutions"] for r in report_rows),
                   "shared_error_corrections": sum(r["n_shared_error_corrections"] for r in report_rows),
                   "unresolved": sum(r["n_unresolved"] for r in report_rows)},
        "records": report_rows,
        "skipped": skipped_rows,
        "validation": {
            "aggregated_plus_skipped_equals_manifest": True,
            "seat_versions_input_hash_material_sha_checked": "both seats, 3 in-scope papers: version, input_bundle_sha256 and paper material sha match manifest; model types sol=sonnet(gpt-6.1-sol), son55=haiku(claude-sonnet-5-5 self-reported) as in manifest.model_types",
            "seat_rs_parent_and_domain_namespace_checked": "PARENTS.tsv + taxonomy.json, both seats, 3 papers: no errors",
            "seat_quote_check": "all seat quotes are substrings of their cited fixed texts except son55 2202:E028, 2304:E029, 2305:E064, which cite the replaced 2303.17491/2209.08655 files; not opened, marked not verifiable, not used in any final rating/resolution/correction (asserted)",
            "every_mechanical_conflict_has_resolution": True,
            "rating_resolutions_match_final_ratings": True,
            "final_rs_parent_and_domain_checks": True,
            "evidence_reference_integrity": "every evidence_id referenced in a final record exists in its evidence list; seat IDs namespaced sol:/son55:, own evidence agg:",
            "agg_quote_substring_check": "each agg quote is an exact substring of the cited fixed paper text",
            "score_recomputed": "S=(15G+25M+20X+10Em+10Ec+10Eh+5Es+5Ecost)/4; weights sum 100, E sum 40; recomputed after write; display=Python round to 1 decimal (as c1/a1), selection uses raw",
            "final_record_hash_recomputed_after_write": True,
            "hash_rule": "sha256 of json.dumps(record minus final_record_hash, sort_keys=True, ensure_ascii=False, separators=(',',':')) in UTF-8",
            "atomic_writes": "tmp file + os.replace",
            "limitations": [
                "Structural/arithmetic/quote checks do not establish semantic correctness or scientific validity; nothing reproduced.",
                "v1 render: figures not rendered (2202 Fig 3/5/7/8 ablation values, 2304 Fig 4 prompt example, 2305 Fig 4/7); judgements use text, tables and captions and say so.",
                "No session id or invocation receipt is available to this agent.",
            ],
        },
        "requests_to_controller": [
            "2209.08655, 2303.17491: a2 pending on upgraded materials; not aggregated here.",
            "son55 cited replaced-material evidence in 3 in-scope records (2202:E028, 2304:E029, 2305:E064); not relied on. If the a2 re-dispatch re-runs these papers, the neighbour facts can be re-cited against the new files.",
            "Optional (non-blocking): rendered figures for 2202.08137 Fig 3/5/7/8 would let E.causality be checked against numbers rather than author prose.",
            "Domain-card revision proposal (record only): gui:K29 counter-evidence from 2202.08137 Sec 3.4.",
        ],
        "boundaries": "No publication, no Reel selection, no rubric/card/seat/input edits, no git operations. Scores are draft_uncalibrated v2.2 provisional values pending controller verification.",
        "timestamp": now(),
    }
    write_atomic(OUT_DIR / "batch-report.json", report)
    for r in report_rows:
        print(r["paper_key"], r["aggregate_status"], r["raw_score"], r["display_score"], r["resolution_decisions"],
              r["n_shared_error_corrections"], r["n_unresolved"], r["final_record_hash"][:12])


if __name__ == "__main__":
    main()
