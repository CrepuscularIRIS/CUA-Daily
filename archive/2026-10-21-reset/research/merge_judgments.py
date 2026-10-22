"""Merge the two blind judgment passes of a batch into one canonical record set.

Usage (repo root):
  python3 research/merge_judgments.py <B>              # merge -> research/judgments/<B>.jsonl (+ conflicts.json)
  python3 research/merge_judgments.py <B> --apply-arb  # apply research/judgments/passes/<B>.arb.jsonl

Inputs per batch <B>:
  research/judgments/passes/<B>.sol.jsonl      seat 1 (gpt-6.1-sol)
  research/judgments/passes/<B>.son55.jsonl    seat 2 (claude-sonnet-5-5)
  research/patterns/assign_passes/assign_<B>.{sol,son55}.jsonl

Merge rules (deterministic; disagreements that change the score become FLAGs for the opus-5-5 arbitrator,
score-equivalent ones are settled deterministically without arbitration):
  - evidence / evidence_level / success / failure: equal values -> keep (quote from seat 1 if it is in the
    full text, else seat 2); `no`-vs-`unclear` -> `unclear` (both score 0, no claim made); any other
    disagreement -> placeholder `unclear`, FLAG.
  - anti: value yes|no only -> placeholder on conflict is `no` (no penalty without agreement), FLAG;
    mitigated conflict FLAGs only when the agreed value is `yes` (otherwise mitigated never affects the
    score; seat 1's value is kept silently).
  - assignment: a paper already in research/patterns/assignments.jsonl (a re-judged board paper) keeps its
    published sub_pattern — changing it would invalidate the old batch structurally in score.py build. The
    seats' own sub-patterns are recorded as proposals in research/patterns/reassign_proposals.jsonl for a
    human-review pass (applied the way wave-1 was). A paper with no published row (new papers) uses the
    dual-seat merge: same sub_pattern -> keep, differ -> FLAG for the arbitrator.
  - version_read conflict -> FLAG (placeholder seat 1). title_zh / one_line / one_line_zh: seat 1, no FLAG.
  - assignment: same sub_pattern -> keep (fit = weak if either seat says weak); differ -> FLAG. If the
    arbitrator switches a paper to seat 2's sub_pattern, that paper's record is re-based on seat 2's pass
    (different sub-pattern can mean a different main pattern and S/F id set), then its item decisions apply.

Placeholders are schema-valid for research/score.py check; the arbitrator resolves FLAGs before scoring.
Conflicts and both passes are committed with the batch (audit trail).
"""

import argparse
import json
import sys
from pathlib import Path

SEATS = ("sol", "son55")
TEXT_FIELDS = ("version_read", "title_zh", "one_line", "one_line_zh")
DICT_SECTIONS = ("evidence", "success", "failure", "anti")


def jl(p: Path) -> list[dict]:
    if not p.exists():
        sys.exit(f"missing pass file: {p}")
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def squash(s: str) -> str:
    return " ".join((s or "").split())


def load(root: Path, B: str):
    jp = root / "judgments" / "passes"
    ap = root / "patterns" / "assign_passes"
    passes = {s: {r["arxiv"]: r for r in jl(jp / f"{B}.{s}.jsonl")} for s in SEATS}
    pub = {r["arxiv"]: r for r in jl(root / "patterns" / "assignments.jsonl")} \
        if (root / "patterns" / "assignments.jsonl").exists() else {}
    assigns = {}
    for s in SEATS:  # a missing assign pass (calibration: assignment fixed) falls back to the published rows
        p = ap / f"assign_{B}.{s}.jsonl"
        assigns[s] = {r["arxiv"]: r for r in jl(p)} if p.exists() else pub
    for s in SEATS:
        if set(passes[s]) != set(passes["sol"]) and s != "sol":
            sys.exit(f"paper sets differ between seats: {sorted(set(passes[s]) ^ set(passes['sol']))}")
        if not set(passes["sol"]) <= set(assigns[s]):
            sys.exit(f"assign pass {s} misses papers: {sorted(set(passes['sol']) - set(assigns[s]))}")
    return passes, assigns


def fulltext_of(root: Path, aid: str) -> str:
    p = root / "fulltext" / f"{aid.replace(':', '_')}.txt"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def merge(root: Path, B: str) -> None:
    passes, assigns = load(root, B)
    pub = {r["arxiv"]: r for r in jl(root / "patterns" / "assignments.jsonl")} \
        if (root / "patterns" / "assignments.jsonl").exists() else {}
    out, conflicts, assign_out, proposals = [], [], [], []
    for aid in sorted(passes["sol"]):
        a, b, text = passes["sol"][aid], passes["son55"][aid], fulltext_of(root, aid)
        rec = {k: a[k] for k in TEXT_FIELDS}  # text fields: seat 1, deterministic
        if a["version_read"] != b["version_read"]:
            conflicts.append({"arxiv": aid, "field": "version_read",
                              "sol": {"value": a["version_read"]}, "son55": {"value": b["version_read"]}})
        for sec in DICT_SECTIONS:
            rec[sec] = {}
            keys = sorted(set(a.get(sec) or {}) | set(b.get(sec) or {}))
            for k in keys:
                rec[sec][k] = _merge_item(aid, f"{sec}.{k}", (a.get(sec) or {}).get(k),
                                          (b.get(sec) or {}).get(k), text, conflicts)
        rec["evidence_level"] = _merge_item(aid, "evidence_level", a.get("evidence_level"),
                                            b.get("evidence_level"), text, conflicts)
        rec = {"arxiv": aid, **rec}
        out.append(rec)
        if aid in pub:  # re-judged paper: published assignment stands, seats file proposals
            assign_out.append({k: pub[aid].get(k) for k in ("arxiv", "sub_pattern", "fit", "fit_note")})
            for s in SEATS:
                row = assigns[s].get(aid)
                if row and row.get("sub_pattern") and row["sub_pattern"] != pub[aid]["sub_pattern"]:
                    proposals.append({"arxiv": aid, "sub_pattern": row["sub_pattern"], "fit": row.get("fit"),
                                      "fit_note": row.get("fit_note", ""), "batch": B, "seat": s})
        else:
            assign_out.append(_merge_assign(aid, assigns, conflicts))
    (root / "judgments" / f"{B}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    (root / "patterns" / f"assign_{B}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in assign_out), encoding="utf-8")
    prop_path = root / "patterns" / "reassign_proposals.jsonl"
    kept = [l for l in prop_path.read_text(encoding="utf-8").splitlines()
            if l.strip() and json.loads(l).get("batch") != B] if prop_path.exists() else []
    prop_path.write_text("".join(l + "\n" for l in kept)
                         + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in proposals), encoding="utf-8")
    _write_conflicts(root, B, conflicts)
    n = len(out)
    print(f"merged {n} papers: {n * (len(out[0]['evidence']) + len(out[0]['success']) + len(out[0]['failure']) + len(out[0]['anti']) + 2) if out else 0}"
          f" items across both seats -> {len(conflicts)} FLAGs, {len(proposals)} reassign proposals")


def _merge_item(aid: str, label: str, ia: dict | None, ib: dict | None, text: str, conflicts: list) -> dict:
    ia, ib = ia or {}, ib or {}
    if label.startswith("anti."):
        item = {"value": ia.get("value"), "mitigated": ia.get("mitigated", "unclear"), "quote": ia.get("quote", "")}
        if ia.get("value") != ib.get("value"):
            item["value"] = "no"  # no penalty without 2-seat agreement; arbitrator decides
            item["quote"] = ""
            conflicts.append({"arxiv": aid, "field": f"{label}.value",
                              "sol": {"value": ia.get("value"), "quote": ia.get("quote")},
                              "son55": {"value": ib.get("value"), "quote": ib.get("quote")}})
        elif ia.get("mitigated") != ib.get("mitigated"):
            if ia.get("value") == "yes":  # only then does mitigated change the score
                item["mitigated"] = "unclear"
                conflicts.append({"arxiv": aid, "field": f"{label}.mitigated",
                                  "sol": {"value": ia.get("mitigated")}, "son55": {"value": ib.get("mitigated")}})
        return item
    va, vb = ia.get("value"), ib.get("value")
    item = {"value": va, "quote": ia.get("quote", "")}
    if va == vb:
        if text and item["quote"] and squash(item["quote"]) not in squash(text):
            item["quote"] = ib.get("quote", "")  # seat 1's quote is not verbatim; try seat 2's
    elif {va, vb} <= {"no", "unclear"}:  # score-equivalent: make no claim
        item = {"value": "unclear", "quote": ""}
    else:
        item = {"value": "unclear", "quote": ""}
        conflicts.append({"arxiv": aid, "field": label,
                          "sol": {"value": va, "quote": ia.get("quote")},
                          "son55": {"value": vb, "quote": ib.get("quote")}})
    return item


def _merge_assign(aid: str, assigns: dict, conflicts: list) -> dict:
    a, b = assigns["sol"][aid], assigns["son55"][aid]
    row = {"arxiv": aid, "sub_pattern": a["sub_pattern"],
           "fit": "weak" if "weak" in (a.get("fit"), b.get("fit")) else (a.get("fit") or "good"),
           "fit_note": a.get("fit_note", "")}
    if a["sub_pattern"] != b["sub_pattern"]:
        conflicts.append({"arxiv": aid, "field": "assign.sub_pattern",
                          "sol": {"value": a["sub_pattern"], "quote": a.get("fit_note")},
                          "son55": {"value": b["sub_pattern"], "quote": b.get("fit_note")},
                          "mains_differ_note": "if the arbitrator picks seat 2's sub_pattern the record is re-based on seat 2"})
    return row


def _write_conflicts(root: Path, B: str, conflicts: list) -> None:
    (root / "judgments" / "passes" / f"{B}.conflicts.json").write_text(
        json.dumps({"batch": B, "count": len(conflicts), "conflicts": conflicts},
                   ensure_ascii=False, indent=1), encoding="utf-8")


def apply_arb(root: Path, B: str) -> None:
    passes, assigns = load(root, B)
    arb_p = root / "judgments" / "passes" / f"{B}.arb.jsonl"
    if not arb_p.exists():
        sys.exit(f"no arbitrator file: {arb_p}")
    decisions = [json.loads(l) for l in arb_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    conflicts = json.loads((root / "judgments" / "passes" / f"{B}.conflicts.json").read_text(encoding="utf-8"))["conflicts"]
    recs = {r["arxiv"]: r for r in jl(root / "judgments" / f"{B}.jsonl")}
    assign = {r["arxiv"]: r for r in jl(root / "patterns" / f"assign_{B}.jsonl")}
    pub = {r["arxiv"] for r in jl(root / "patterns" / "assignments.jsonl")} \
        if (root / "patterns" / "assignments.jsonl").exists() else set()
    done, skipped = set(), []
    base_switch = {}
    for d in decisions:  # pass 1: assignment switches re-base the record first
        if d["field"] == "assign.sub_pattern":
            aid, v = d["arxiv"], d["value"]
            if aid in pub:
                skipped.append((aid, d["field"], "paper has a published assignment; use the proposal process"))
                continue
            seat = "son55" if v == assigns["son55"][aid]["sub_pattern"] else ("sol" if v == assigns["sol"][aid]["sub_pattern"] else None)
            if seat is None:
                skipped.append((aid, d["field"], "value matches neither seat"))
                continue
            base_switch[aid] = seat
            if seat == "son55":
                recs[aid] = {"arxiv": aid, **{k: passes[seat][aid][k] for k in TEXT_FIELDS},
                             **{sec: dict(passes[seat][aid].get(sec) or {}) for sec in DICT_SECTIONS},
                             "evidence_level": dict(passes[seat][aid]["evidence_level"])}
                assign[aid]["sub_pattern"] = v
                assign[aid]["fit_note"] = assigns[seat][aid].get("fit_note", "")
            done.add((aid, d["field"]))
    for d in decisions:  # pass 2: item-level decisions on the (possibly re-based) record
        aid, field, v = d["arxiv"], d["field"], d.get("value")
        if field == "assign.sub_pattern" or (aid, field) in done:
            continue
        rec = recs.get(aid)
        if rec is None:
            skipped.append((aid, field, "unknown paper")); continue
        q = d.get("quote", "")
        text = fulltext_of(root, aid)
        if q and text and squash(q) not in squash(text):
            skipped.append((aid, field, "quote not in fulltext")); continue
        parts = field.split(".")
        if field == "version_read":
            rec["version_read"] = v
            done.add((aid, field))
            continue
        if parts[0] == "evidence_level":
            item = rec["evidence_level"]
        elif len(parts) == 2 and parts[0] in DICT_SECTIONS:
            item = rec[parts[0]].get(parts[1])
            if item is None:
                skipped.append((aid, field, "field not in (re-based) record")); continue
        elif len(parts) == 3 and parts[0] == "anti":
            item = rec["anti"].get(parts[1])
            if item is None:
                skipped.append((aid, field, "field not in (re-based) record")); continue
            if parts[2] == "mitigated":
                item["mitigated"] = v; done.add((aid, field)); continue
        else:
            skipped.append((aid, field, "unusable field path")); continue
        item["value"] = v
        if q or v in ("unclear", "no", "na"):
            item["quote"] = q
        done.add((aid, field))
    remaining = [c for c in conflicts if (c["arxiv"], c["field"]) not in done and c["arxiv"] not in base_switch]
    remaining += [c for c in conflicts if c["arxiv"] in base_switch and c["field"] == "assign.sub_pattern" and (c["arxiv"], c["field"]) not in done]
    (root / "judgments" / f"{B}.jsonl").write_text(
        "".join(json.dumps(recs[i], ensure_ascii=False) + "\n" for i in sorted(recs)), encoding="utf-8")
    (root / "patterns" / f"assign_{B}.jsonl").write_text(
        "".join(json.dumps(assign[i], ensure_ascii=False) + "\n" for i in sorted(assign)), encoding="utf-8")
    _write_conflicts(root, B, remaining)
    print(f"arbitration: {len(done)} decisions applied, {len(skipped)} skipped, {len(remaining)} FLAGs left")
    for s in skipped:
        print("  skip:", *s)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--apply-arb", action="store_true")
    ap.add_argument("--root", default="research", type=Path, help="the research/ directory (tests point it at a temp tree)")
    a = ap.parse_args()
    apply_arb(a.root, a.batch) if a.apply_arb else merge(a.root, a.batch)


if __name__ == "__main__":
    main()
