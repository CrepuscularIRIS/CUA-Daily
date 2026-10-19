# Calibration

`gold.jsonl` — 8 reference judgments copied from published batches (good fit, full text, 8 different main patterns,
two per band ★★★ / ★★ / ★ / —; picked with `random.seed(42)`). A new scorer model re-judges 3 of them blind and runs
`PYTHONPATH=research python3 research/calibrate.py <file>`: PASS = every paper within ±8 points and the same
evidence level.

## Runs

| date | file | papers | result |
|---|---|---|---|
| 2026-10-20 | `run1_2026-10-20.jsonl` | 2604.13318, 2509.01720, 2609.02149 | **PASS**: Δ +0 / −2 / −4 · item agreement 95% / 95% / 79% · levels identical (transfer, online, online) |

Run 1 was a fresh agent of the same model family that built the board, so it measures judge self-consistency, not
cross-model agreement. Run it again when the scorer model changes.
