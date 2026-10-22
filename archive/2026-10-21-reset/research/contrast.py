"""Accept-vs-reject contrast per pattern, RS anti-pattern style. Deterministic; no LLM.

Primary universe = ICLR 2025/2026 submissions only (accepted AND rejected are both fully public there,
so the base rate is fair). Awesome-list papers accepted elsewhere are curator-selected and would
inflate accept rates, so they only appear in the secondary "all labeled" view.

Writes research/patterns/contrast.json and contrast.md.
"""

import json
from collections import Counter, defaultdict
from itertools import combinations
from math import sqrt
from pathlib import Path

R = Path("research")
ACC, REJ = {"oral", "spotlight", "poster", "accept"}, {"reject", "withdrawn"}
MIN_N_PATTERN, MIN_N_COMBO, ANTI_DELTA = 10, 15, -0.12  # RS used n>=30, Δ<=-12pp on a 3x larger corpus


def jl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def or_duplicates() -> dict[str, str]:
    """OpenReview id -> arXiv id for the same paper already in the corpus (fuzzy title match ≥0.9).

    The corpus-overlap filter at pull time used exact normalized titles and missed a few
    (e.g. "Gödel" vs "Godel"). The arXiv id is canonical; the or: copy is dropped from counts.
    """
    import difflib, re
    norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    corpus = {s["arxiv"]: norm(s["title"]) for s in jl(R / "signatures.jsonl")}
    dup = {}
    for s in jl(R / "signatures_or.jsonl"):
        t = norm(s["title"])
        for aid, u in corpus.items():
            if t == u or difflib.SequenceMatcher(None, t, u).ratio() >= 0.9:
                dup[s["arxiv"]] = aid
                break
    return dup


def outcomes() -> dict[str, tuple[str, bool]]:
    """paper id -> (acc|rej, is_iclr_2025_2026). For a duplicated paper the ICLR outcome wins in the
    ICLR views (it is the decision inside that universe); its best-known label is kept for all_labeled."""
    out = {}
    for r in jl(R / "openreview.jsonl"):
        g = "acc" if r["label"] in ACC else "rej" if r["label"] in REJ else None
        if g:
            out[r["arxiv"]] = (g, r.get("venueid", "").startswith(("ICLR.cc/2025", "ICLR.cc/2026")))
    dup = or_duplicates()
    for r in jl(R / "openreview_pull.jsonl"):
        g = "acc" if r["label"] in ACC else "rej" if r["label"] in REJ else None
        oid = "or:" + r["forum"]
        if g and oid in dup:
            out[dup[oid] + "#iclr"] = (g, True)  # ICLR-view label for the canonical arXiv paper
        elif g:
            out[oid] = (g, True)
    return out


def table(groups: dict[str, list[str]], label: dict[str, str], base: float, min_n: int) -> list[dict]:
    rows = []
    for key, ids in groups.items():
        ks = [label[i] for i in ids if i in label]
        n, a = len(ks), ks.count("acc")
        if n >= min_n:
            p = a / n
            rows.append({"key": key, "n": n, "n_accept": a, "n_reject": n - a, "p_accept": round(p, 3),
                         "delta_pp": round(100 * (p - base), 1), "ci95": wilson(a, n)})
    return sorted(rows, key=lambda r: r["delta_pp"])


def main() -> None:
    tax = json.loads((R / "patterns/taxonomy.json").read_text())
    parent = {s["id"]: s["parent"] for s in tax["sub_patterns"]}
    assign = jl(R / "patterns/assignments.jsonl")
    dup = or_duplicates()
    if (R / "patterns/assignments_or.jsonl").exists():
        assign += [a for a in jl(R / "patterns/assignments_or.jsonl") if a["arxiv"] not in dup]
    raw = outcomes()
    result = {}
    views = (("iclr_2025_2026", lambda v: v[1], False), ("iclr_2025_2026_high_fit", lambda v: v[1], True),
             ("all_labeled", lambda v: True, False))
    for view, keep, high_only in views:
        label = {}
        for i, v in raw.items():  # "<arxiv>#iclr" overrides the arXiv paper's label in ICLR views only
            if i.endswith("#iclr"):
                if view.startswith("iclr"):
                    label[i[:-5]] = v[0]
            elif keep(v) and not (view.startswith("iclr") and i + "#iclr" in raw):
                label[i] = v[0]
        lab_assign = [a for a in assign if a["arxiv"] in label and (not high_only or a.get("fit") == "high")]
        base = sum(label[a["arxiv"]] == "acc" for a in lab_assign) / max(1, len(lab_assign))
        by_main, by_sub, by_combo = defaultdict(list), defaultdict(list), defaultdict(list)
        for a in lab_assign:
            main = parent[a["sub_pattern"]]
            by_main[main].append(a["arxiv"])
            by_sub[a["sub_pattern"]].append(a["arxiv"])
            for pair in combinations(sorted({main, *a.get("secondary_main", [])}), 2):
                by_combo[" + ".join(pair)].append(a["arxiv"])
        combos = table(by_combo, label, base, MIN_N_COMBO)
        result[view] = {
            "n_labeled": len(lab_assign), "base_p_accept": round(base, 3),
            "main": table(by_main, label, base, MIN_N_PATTERN),
            "sub": table(by_sub, label, base, MIN_N_PATTERN),
            "combos": combos,
            "anti_pattern_candidates": [c for c in combos if c["delta_pp"] <= 100 * ANTI_DELTA],
        }
    ev_rows = jl(R / "evidence_corpus.jsonl") if (R / "evidence_corpus.jsonl").exists() else []
    ev = defaultdict(lambda: {"acc": Counter(), "rej": Counter()})
    for r in ev_rows:
        if r["arxiv"] in raw:
            for k, v in r["evidence"].items():
                ev[k][raw[r["arxiv"]][0]][v["value"]] += 1
    result["evidence_by_outcome"] = {k: {g: dict(c) for g, c in v.items()} for k, v in ev.items()}
    (R / "patterns/contrast.json").write_text(json.dumps(result, indent=1))

    md = ["# Pattern × outcome contrast", "", "Generated by `research/contrast.py`. Δ = pattern accept rate − base rate, in percentage points. "
          "Small n: read the 95% CI before believing any Δ.", ""]
    for view, *_ in views:
        v = result[view]
        md += [f"## {view} (n={v['n_labeled']}, base accept rate {v['base_p_accept']:.0%})", "",
               "| main pattern | n | accept | reject | p_accept | Δ pp | 95% CI |", "|---|---|---|---|---|---|---|"]
        md += [f"| {r['key']} | {r['n']} | {r['n_accept']} | {r['n_reject']} | {r['p_accept']:.0%} | {r['delta_pp']:+} | {r['ci95'][0]:.0%}–{r['ci95'][1]:.0%} |" for r in v["main"]]
        md += ["", f"Anti-pattern candidates (n≥{MIN_N_COMBO}, Δ≤{int(100 * ANTI_DELTA)}pp): "
               + (", ".join(f"`{c['key']}` (n={c['n']}, Δ{c['delta_pp']:+})" for c in v["anti_pattern_candidates"]) or "none"), ""]
    (R / "patterns/contrast.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    assert wilson(5, 10)[0] < 0.5 < wilson(5, 10)[1] and wilson(0, 0) == (0.0, 0.0)
    main()
