# ReasoningBank: a web agent that learns strategies from its own successes and failures

*A CUA Radar reading of arXiv 2509.25140v2 (Ouyang, Yan, Hsu, Chen, Jiang, Wang, Han, Le, Daruki, Tang, Tirumalashetty, Lee, Rofouei, Lin, Han, Lee, Pfister). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2509.25140v2 · Code: https://github.com/google-research/reasoning-bank*

## The problem: agents forget what they just learned

A web agent that meets a stream of tasks usually starts each one from scratch. Systems that do keep memory tend to store either raw trajectories, which are long and noisy to reuse, or routines distilled from successes only, which leave the agent’s own failures unused. The paper argues that such memory stays passive record-keeping rather than guidance that transfers to new tasks.

## What ReasoningBank is

ReasoningBank is a memory loop for a ReAct-style agent; nothing is trained. The agent sees the text accessibility tree through BrowserGym and acts with web operations (on SWE-Bench-Verified it uses bash). Tasks arrive one at a time, memory starts empty, and no ground-truth feedback is available at test time. On the CUA Radar board the paper sits in pattern C19, learning reusable knowledge from the agent’s own runs.

For each task:

1.  **Retrieve.** Embed the task query (gemini-embedding-001) and take the top-k most similar memory items by cosine similarity, with k = 1 by default; the items go into the agent’s system prompt.
2.  **Act.** Run the agent, capped at 30 steps, to get a trajectory.
3.  **Self-judge.** The same LLM, at temperature 0, reads the query, the trajectory and the final page state and labels it success or failure. This is the only correctness signal.
4.  **Extract.** From a success, distill why it worked; from a failure, distill lessons and pitfalls. Each trajectory yields at most three memory items, each a title, a one-line description and a content paragraph of strategy.
5.  **Consolidate.** New items are simply appended; there is no merging or pruning.

**MaTTS (memory-aware test-time scaling)** spends more compute per task to make better memory. In the parallel variant the agent produces k trajectories and contrasts them (self-contrast) to curate memory; in the sequential variant it refines one trajectory k times and keeps the intermediate notes as signal. Best-of-N selection is also done by an LLM.

## Results, as reported

Online WebArena, 684 tasks (the Map domain is excluded because of website issues), overall success rate (%), pass@1. The MaTTS row uses parallel scaling with k = 5.

| Method | Gemini-2.5-flash | Gemini-2.5-pro | Claude-3.7-sonnet |
|----|----|----|----|
| No Memory | 40.5 | 46.7 | 41.7 |
| Synapse (trajectory memory) | 42.1 | 47.7 | 42.6 |
| AWM (workflow memory) | 44.1 | 47.6 | 40.8 |
| **ReasoningBank** | **48.8** | **53.9** | **46.3** |
| \+ MaTTS, k = 5 | 51.8 | 56.3 | 48.8 |

The paper states gains of +8.3, +7.2 and +4.6 over the memory-free agent. On SWE-Bench-Verified, resolve rate rises from 34.2 to 38.8 with Gemini-2.5-flash and from 54.0 to 57.4 with Gemini-2.5-pro. Average steps on WebArena fall by up to 1.4 compared with no memory. Mind2Web is offline: with Gemini-2.5-flash, task-level success rises from 3.3 to 4.8 (cross-task), 1.7 to 2.3 (cross-website) and 1.0 to 1.6 (cross-domain), small in absolute terms.

## What the paper’s own controls say

**Failures as a memory source** (WebArena-Shopping, Gemini-2.5-flash). Adding failed trajectories lifts ReasoningBank from 46.5 to 49.7, while Synapse moves from 40.6 to 41.7 and AWM drops from 44.4 to 42.2.

**Scaling with memory.** With k going from 1 to 5, parallel MaTTS goes from 49.7 to 55.1 and sequential from 49.7 to 54.5. Without memory, scaling fluctuates between 39.0 and 42.2 (parallel) and between 37.4 and 40.6 (sequential). At k = 5, MaTTS reaches 55.1 against 52.4 for vanilla test-time scaling (parallel), and 54.5 against 51.9 (sequential).

**Cost.** Total tokens per task are 53054.5 for ReasoningBank against 50847.4 for no memory, versus 58514.7 for Synapse and 59372.8 for AWM; the paper describes the increase as around 4.3%.

**The judge.** On the Shopping subset the self-judge is 72.7% accurate against ground-truth labels. When the authors simulate judges of lower accuracy by flipping labels, they report similar success rates between 70% and 90% accuracy.

**Smaller models.** With Gemma-3-12B-Instruct on Shopping, success is 24.1 for ReasoningBank, 17.1 with no memory, 16.0 for Synapse and 21.4 for AWM.

## Where the evidence is thinner

- No seeds, standard deviations or intervals are reported; the main table gives single numbers.
- The MaTTS row in Table 1 uses five trajectories per task (best-of-N) while the other rows use one, so it is not compute-matched.
- The ablations and the scaling study use one subset (Shopping, 187 tasks) and one backbone; the Multi subset has 29 tasks.
- The correctness signal is the agent’s own judge, 72.7% accurate where checked, and the CUA Radar record flags this (anti-pattern AP4); the robustness check is a simulation on one subset.
- Tasks arrive sequentially from the same benchmark; the paper describes no separate held-out task split, and the CUA Radar record marks held-out evaluation as partial.
- Mind2Web gains are small in absolute terms.

## CUA Radar’s read

CUA Radar scores this paper **66 (★★)**, evidence level **online**. The record credits online WebArena evaluation, Synapse and AWM baselines, step and token reporting, a failure ablation, a judge accuracy check and released code. It flags the self-judge without two-sided validation (AP4) and records seeds, variance and held-out tasks as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v2).
