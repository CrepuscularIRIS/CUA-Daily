# Calibration

`gold.jsonl` — 8 reference judgments copied from published batches (good fit, full text, 8 different main patterns,
two per band ★★★ / ★★ / ★ / —; picked with `random.seed(42)`). A new scorer model re-judges 3 of them blind and runs
`PYTHONPATH=research python3 research/calibrate.py <file>`: PASS = every paper within ±8 points and the same
evidence level.

## Runs

| date | file | papers | result |
|---|---|---|---|
| 2026-10-20 | `run1_2026-10-20.jsonl` | 2604.13318, 2509.01720, 2609.02149 | **PASS**: Δ +0 / −2 / −4 · item agreement 95% / 95% / 79% · levels identical (transfer, online, online) |
| 2026-10-21 | `run2_2026-10-21.jsonl` | same 3, dual blind seats | **FLAG, accepted by the maintainer**: Δ +0 / +6 / −11 · agreement 62% / 79% / 58% · levels identical |

Run 1 was a fresh agent of the same model family that built the board, so it measures judge self-consistency, not
cross-model agreement. Run 2 is the first cross-model panel (seats `gpt-6.1-sol` + `claude-sonnet-5-5`, arbitrator
`claude-opus-5-5`, assignment fixed). The −11 on 2609.02149 comes from three evidence-backed arbitrator reversals
(strong_baselines partial→no, AP4 no→yes, S4 yes→unclear both-seats): the panel is stricter than the single model
that built the board — the intended effect. Maintainer reviewed and accepted (2026-10-21); expect weak papers to
score lower under dual-seat re-judgment. The ±8 tolerance stays as-is for same-family re-runs; a cross-model run
beyond it needs this same human sign-off.
