# Select Actions by Simulated or Verified Lookahead
_id: `simulated_lookahead_selection` · sub-patterns: K01, K02 · 2 candidate_pattern · 0 case · domains: cua-agents (2 K / 0 C) · outcome labels: none in this build_

**Definition.** At inference time, generate several candidate actions (or whole trajectories), estimate how good each one is before committing — either by predicting its next state with a world model and scoring the imagined outcome, or by scoring it directly with a trained or agentic verifier — and execute only the best. The gain is claimed from better selection among candidates the policy already proposes, not from a better policy.

**Operational signature.** sample k candidate actions/trajectories → simulate next state (K01) or score directly with a verifier (K02) → rank → execute/submit the argmax

**When to apply.** When the target environment cannot be reset or backtracked (live websites), so real tree search is unavailable, and the policy's candidate set already contains a correct action.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K01](../sub/K01.md) | candidate_pattern | Simulate each candidate action with a world model, score the imagined outcome, execute the best | sample k candidate actions from a policy, predict each candidate's next state with a learned or prompted world model (one step), score the… |
| [K02](../sub/K02.md) | candidate_pattern | Rerank sampled actions or trajectories with a learned/agentic verifier (no simulation) | sample N candidate actions (per step) or N whole trajectories, score each with a separately trained or agentic verifier, and execute/submit… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **One-step lookahead horizon.** The simulated lookahead is one step deep, or the horizon is ablated and H=1 is chosen; H=1 is reported most effective (2411.06559#s1, 2602.09856#s2, 2602.14721#s3).
- **Trained, specialised simulator.** The world model used for lookahead is trained or specialised (abstracted next-state description or code-rendered screen) rather than a naive prompted LLM; an untrained simulator gives much smaller gains (+1.2 vs +9.5 SR on AndroidWorld; prompted 17.5% vs trained 22.0%) (2602.09856#s2, 2410.13232#s2).
- **Scorer sees the simulated next state.** The value model's input includes the predicted next state, and an ablation removing it is reported (SR 22.0 -> 18.0 without it) (2410.13232#s2).
- **Verifier accuracy measured and well above chance.** For direct reranking, the verifier's accuracy is reported and is well above 50%, ideally from a verifier trained on human labels rather than GPT-4o-labelled steps (2602.00575#s2, 2509.23738#s2).
- **Non-resettable target and cost stated.** The paper motivates simulation by an environment that cannot be reset/backtracked and reports cost/latency against tree search (~4-5x lower for simulation); trajectory-level selection keeps terminal state per rollout (2411.06559#s1, 2410.13232#s2, 2602.00575#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Multi-step simulated rollouts.** Lookahead uses horizons of 2 or more; multi-step simulation hallucinates actions unavailable in predicted states and compounds error, and horizons 2-3 lose effectiveness (2411.06559#s1, 2410.13232#s2).
- **No real-execution search baseline where reset is possible.** Absolute success remains below real-execution tree search where reset is possible (16.6 vs 19.2 WebArena; 23.6 vs 26.2 VWA); a paper that omits this comparison overstates the move (2410.13232#s2, 2411.06559#s1).
- **Gains measured only on short or offline tasks.** On short MiniWob tasks gains are small (+0.2 to +3.2) and MCTS/hybrid add little; offline SR gains from simulation are ~1.2-1.3 points (2602.14721#s3, 2602.09856#s2).
- **Candidate count scaled without compute accounting.** Best-of-N gains plateau as N grows while compute grows linearly; near-chance verifier accuracy yields negligible or negative Best-of-N gain (2509.23738#s2, 2602.00575#s2).
- **Unstable element identity between search and execution.** Large result-list state spaces (Shopping) shrink gains; element IDs change on reload, causing search/execution mismatch (2410.13232#s2).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E18 (baseline, common_practice).** For inference-time search or best-of-N (simulated lookahead, verifier reranking), report cost/latency and the number of candidates, and compare against real-execution tree search where reset is possible — _applies when_ a claim that an inference-time selection method (world-model lookahead, verifier rerank, best-of-N) improves success.
- **E31 (ablation, common_practice).** Ablate imagination / lookahead horizon, since world-model errors compound beyond 1 (lookahead) or about 5 (training) steps — _applies when_ a method that plans or trains with multi-step rollouts inside a learned GUI world model.
- **E16 (reproducibility, common_practice).** Report mean and spread over at least 3 runs (or confidence intervals) for online benchmark numbers — _applies when_ an empirical comparison on an online/live benchmark (OSWorld, AndroidWorld, WebArena, Online-Mind2Web) where LLM sampling and environment noise vary across runs.
- **E04 (dataset, common_practice).** Evaluate live-web agents on Online-Mind2Web (human-validated, start URL given, no search engine) or Mind2Web-Live rather than only WebVoyager, where a naive search-and-click agent already solves 51% of sampled tasks — _applies when_ a claim about web-agent success on real, live websites.
- **E03 (dataset, common_practice).** Report success on WebArena (self-hosted, functional-correctness checkers) for web-agent training or planning claims; if the 165-task WebArena-Lite or a per-template subset is used, say so and justify it — _applies when_ an empirical claim that a training, data-synthesis or planning method improves a web agent on self-hosted sites.

## Cognitive barriers
- "A strong world model makes inference-time search the main payoff." One member concludes world models are worth more for data synthesis than inference-time search (2602.14721#s3).
- "More candidates always help." Gains plateau with N and depend on verifier accuracy (2509.23738#s2, 2602.00575#s2).

## Related anti-patterns
[AP1](../anti-patterns.md#ap1), [AP6](../anti-patterns.md#ap6)
