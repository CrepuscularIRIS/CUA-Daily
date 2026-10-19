"""Validate a signatures JSONL file against research/SIGNATURE_SCHEMA.md enums.

Usage: python research/check_signatures.py <signatures.jsonl> [<expected_ids.txt>]
Exit 1 on any error; prints one line per problem.
"""

import json
import sys

TARGET = {"prompt", "skill", "tool", "workflow", "memory", "code", "evaluator", "config", "weights"}
PROPOSER = {"reflective_rewrite", "evolutionary_mutation", "recombination", "coding_agent_edit", "retrieval_reuse",
            "textual_gradient", "trained_proposer", "search_over_space", "other"}
SOURCE = {"ground_truth", "llm_judge", "execution", "self_critique", "human", "peer_consensus"}
SELECTION = {"strict_improvement", "pareto", "archive_open_ended", "tournament_or_bandit", "llm_select",
             "noise_band_regularized", "none", "other"}
RETENTION = {"single_incumbent", "archive", "library", "memory_store", "population", "none"}
TRANSFER = {"same_task_unseen_instances", "cross_task", "cross_domain", "cross_model", "none"}
YPNU = {"yes", "partial", "no", "unclear"}
YNU = {"yes", "no", "unclear"}
EVIDENCE = {
    "held_out_separate_from_selection": YPNU, "ood_or_cross_task_eval": YNU, "multiple_seeds_with_variance": YNU,
    "budget_matched_baselines": YPNU, "optimizer_cost_reported": YPNU, "failures_in_denominator": YNU,
    "leakage_guard": {"tested", "untested", "none", "unclear"}, "retained_artifact_ablation": YNU,
    "improver_level_comparison": YNU, "code_released": {"yes", "announced", "no", "unclear"},
}
TEXT = ["problem", "assumption_broken", "operational_signature", "load_bearing_mechanism", "title", "version_read"]


def check(r: dict) -> list[str]:
    e = [f"empty {k}" for k in TEXT if not isinstance(r.get(k), str) or not r[k].strip()]
    subset = lambda k, allowed, v: e.append(f"{k}={v!r}") if not isinstance(v, list) or set(v) - allowed else None
    subset("target", TARGET, r.get("target"))
    subset("transfer_claimed", TRANSFER, r.get("transfer_claimed"))
    subset("signal.source", SOURCE, (r.get("signal") or {}).get("source"))
    for k, allowed in (("proposer", PROPOSER), ("selection", SELECTION), ("retention", RETENTION)):
        if r.get(k) not in allowed:
            e.append(f"{k}={r.get(k)!r}")
    if (r.get("signal") or {}).get("form") not in {"scalar", "text", "both", "unclear"}:
        e.append("signal.form")
    if not isinstance((r.get("improver_modified") or {}).get("value"), bool):
        e.append("improver_modified.value")
    ev = r.get("evidence") or {}
    e += [f"evidence.{k}={ev.get(k)!r}" for k, allowed in EVIDENCE.items() if ev.get(k) not in allowed]
    for k in ("limitations_evident", "closest_prior"):
        if not isinstance(r.get(k), list) or len(r[k]) > 3:
            e.append(f"{k} must be a list of ≤3")
    return e


def main(argv: list[str]) -> int:
    rows = [json.loads(l) for l in open(argv[0], encoding="utf-8") if l.strip()]
    bad = 0
    for r in rows:
        for err in check(r):
            bad += 1
            print(f"{r.get('arxiv')}: {err}")
    if len(argv) > 1:
        want = set(open(argv[1]).read().split())
        got = [r.get("arxiv") for r in rows]
        if set(got) != want or len(got) != len(set(got)):
            bad += 1
            print(f"id mismatch: missing={sorted(want - set(got))[:10]} extra={sorted(set(got) - want)[:10]} dup={len(got) - len(set(got))}")
    print(f"{len(rows)} rows, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
