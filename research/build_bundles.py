"""Build per-main-pattern input bundles for card-writing agents → research/patterns/bundles/<main_id>.json.

Bundles join taxonomy + assignments + signatures + outcome labels + quote-grounded evidence + contrast.
They name individual papers with their outcome, so they stay local (gitignored); cards built from them
must never name a paper.
"""

import json
from pathlib import Path

R = Path("research")
ACC, REJ = {"oral", "spotlight", "poster", "accept"}, {"reject", "withdrawn"}
jl = lambda p: [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def outcome(label: str) -> str:
    return "accepted" if label in ACC else "rejected" if label in REJ else "unknown"


def main() -> None:
    tax = json.loads((R / "patterns/taxonomy.json").read_text())
    subs = {s["id"]: s for s in tax["sub_patterns"]}
    from contrast import or_duplicates  # same canonicalization as the contrast stats
    dup = or_duplicates()
    assign = jl(R / "patterns/assignments.jsonl") + [a for a in jl(R / "patterns/assignments_or.jsonl") if a["arxiv"] not in dup]
    sig = {s["arxiv"]: s for s in jl(R / "signatures.jsonl") + jl(R / "signatures_or.jsonl")}
    lab = {r["arxiv"]: outcome(r["label"]) for r in jl(R / "openreview.jsonl")}
    lab |= {"or:" + r["forum"]: outcome(r["label"]) for r in jl(R / "openreview_pull.jsonl")}
    ev = {r["arxiv"]: {k: v["value"] for k, v in r["evidence"].items()} for r in jl(R / "evidence_corpus.jsonl")}
    con = json.loads((R / "patterns/contrast.json").read_text())
    views = ("iclr_2025_2026", "all_labeled")
    by = lambda level: {v: {r["key"]: r for r in con[v][level]} for v in views}
    cs, cm = by("sub"), by("main")
    out = R / "patterns/bundles"
    out.mkdir(exist_ok=True)
    for m in tax["main_patterns"]:
        bundle = {"main": {k: m[k] for k in ("id", "name", "definition", "operational_signature", "when_to_apply", "cognitive_barrier")},
                  "main_contrast": {v: cm[v].get(m["id"]) for v in views},
                  "base_rates": {v: con[v]["base_p_accept"] for v in views}, "sub_patterns": []}
        for sid, s in subs.items():
            if s["parent"] != m["id"]:
                continue
            members = []
            for a in (a for a in assign if a["sub_pattern"] == sid):
                g = sig[a["arxiv"]]
                members.append({"outcome": lab.get(a["arxiv"], "unknown"), "fit": a["fit"], "title": g["title"],
                                **{k: g[k] for k in ("problem", "assumption_broken", "operational_signature",
                                                     "load_bearing_mechanism", "limitations_evident")},
                                **({"evidence": ev[a["arxiv"]]} if a["arxiv"] in ev else {})})
            bundle["sub_patterns"].append({**{k: s[k] for k in ("id", "name", "tactical_pattern", "differentiation_within_parent")},
                                           "contrast": {v: cs[v].get(sid) for v in views}, "members": members})
        (out / f"{m['id']}.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1))
        print(m["id"], [(s["id"], len(s["members"])) for s in bundle["sub_patterns"]])


if __name__ == "__main__":
    main()
