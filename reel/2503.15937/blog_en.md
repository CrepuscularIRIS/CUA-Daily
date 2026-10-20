# V-Droid: a mobile GUI agent that verifies candidate actions instead of generating them

*A CUA Radar reading of arXiv 2503.15937v5 (Dai, Jiang, Cao, Li, Yang, Tan, Li, Qiu; MobiCom ’26). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2503.15937v5 · Code: https://github.com/V-Droid-Agent/V-Droid*

## The problem: generation is slow and error-prone

Most mobile GUI agents use an LLM as a generator: at every step the model reads the screen and autoregressively decodes a decision, often with Chain-of-Thought on top. The paper reports two consequences on AndroidWorld: the highest success rate achieved by existing agents is 54.3%, “significantly lower than the human performance of 80%”, and latency is poor — Agent-S2, powered by GPT-4o and UI-TARS-72B, “takes over 25 seconds for a single step”, and most existing agents need more than 10 seconds per step. Prompt engineering and GUI fine-tuning sharpen instruction-following but, in the paper’s words, “fail to adequately address task-specific, multi-step decision-making challenges”.

## What V-Droid is

**The agent.** V-Droid is a text-only mobile GUI task automation agent for Android. It perceives the UI as an XML description extracted via the Android Accessibility Service (no screenshots in the current design), plus a working memory of past steps; it acts through discrete operations — click, long-press, scroll, type text, clear text — executed via Android commands (ADB), supplemented by default actions that are not visible on screen: open app, wait, navigate home, navigate back, complete task, answer user. Board pattern: K02, “rerank sampled actions with a learned verifier” — enumerate, score, run the top one; no next-state simulation.

**The mechanism.** Instead of generating an action, a fine-tuned Llama-3.1-8B-Instruct (4-bit) verifier scores every extracted candidate: each action is wrapped in a prompt (“Is the action X helpful for completing the given user task?”; the model must answer Yes or No), and the score is read from the probability of the “Yes” first token. This is prefilling-only — no autoregressive decoding — so all candidates are verified in one batched pass with prefix caching (vLLM’s Automatic Prefix Caching), with same-type actions grouped to maximize the shared prefix. On average 50.3 actions are verified per step, taking 0.44 s on the default 2× RTX 4090 server. An MLP head on top of the LLM projects token logits into action scores.

**The training signal.** The Pair-wise Process Preference (P³) loss trains the verifier so the labeled correct action outscores every other candidate at each step: contrastive positive-negative pairs are built from fine-grained labeled trajectories (from 100 task traces the paper derives around 55K step-wise labels; pairwise construction yields 50× more training samples than one-per-step). Erroneous states are also used: a predefined reverse-action mapping (click → navigate back, type → clear, open app → navigate home, scroll → reverse scroll, long-click → navigate back) creates self-correcting pairs, sampled to about 2.5% of the training set. Data comes from human-agent joint annotation: the current verifier annotates first, its score-distribution entropy flags uncertain steps for humans to correct, and four iterative rounds grow the dataset from 9K human-labeled pairs (about four minutes per task, five hours total) to 27K, 55K and 110K, with human fixing time dropping to around one minute per task. The dataset spans more than 90 applications in seven categories. Final training: Q-LoRA rank 16, learning rate 1e-4 decayed to 1e-6, 20 epochs, 90 hours on 16× A100 40G.

## Results, as reported

All numbers below are online task success rates on real-execution Android environments (live emulators); the paper reports no offline grounding/step-accuracy benchmark. Seeds, runs and variance are not reported. Verifier backbone: Llama-3.1-8B (4-bit) with an MLP scoring head; latency measured on 20 randomly sampled tasks, default serving on 2× RTX 4090.

| Benchmark (online) | V-Droid | Margin over prior best (as reported) |
|----|----|----|
| AndroidWorld (20 apps, 116 tasks, in-domain) | 59.5% | +5.2 pts (prior best 54.3%) |
| AndroidLab (138 tasks, out-of-domain) | 38.3% | +2.1 pts |
| MobileAgentBench (100 tasks, out-of-domain) | 49% | +9.0 pts |

Latency: 4.3 s per step overall — a 6.1× speedup over prior agents — and 0.74 s per decision (32.1× faster than grounding-based agents that split reasoning and grounding; 25.1× vs UI-TARS and 112.2× vs DeepSeek-R1 with System-2 reasoning). The step budget: 0.44 s verification, 0.30 s action completion (needed in only 12.4% of steps), 3.03 s working-memory update written by GPT-4, plus 0.54 s average page transition; action-space extraction takes under 1 ms. GPU footprint is about 16 GB including the KV cache.

Versus specific baseline families, the paper reports: 25.0% and 7.13% higher SR than cloud-LLM agents on AndroidWorld and AndroidLab; 14.3% over reasoning+grounding decompositions (UI-TARS, Aria-UI, UGround, Aguvis) on AndroidWorld; 14.3% over fine-tuned SLMs on AndroidLab; over 36.2%, 21.0% and 18.0% over memory-driven agents (AutoDroid, MobileGPT) on the three benchmarks.

## What the paper’s own controls say

**Same-base alternatives (Table 3, AndroidWorld, 1.1K task steps of training data each).** The same Llama-3.1-8B fine-tuned as a selector (output the correct action number) reaches 35.8%, and as a T3A-style generator 27.4%, against 47.4% for V-Droid’s P³ verifier. Untrained judges collapse: Llama-3.1-8B as LLM-as-a-Judge scores 0%, GPT-4 as judge 34.5% (still above GPT-4 as generator, 29.6%). Verification only helps after preference training.

**CoT on/off (Table 2, AndroidWorld).** GPT-4o: 41.3% with CoT at 6.70 s decision latency, 39.2% without at 5.74 s; UI-TARS-7B: 33.2% at 10.6 s, 29.3% at 0.97 s. V-Droid, which has no CoT stage, sits at 59.5% with 0.74 s and 2.6K input / 54.3 output tokens.

**Self-correction and memory.** Removing self-correcting pairs drops AndroidWorld from 59.5% to 52.2% (average trajectory length grows from 10.3 to 11.6 steps with them). Replacing the GPT-4 working-memory writer with rule-based summaries gives 46.1% (near-zero latency), action history alone 40.0%.

**Scaling and annotation.** AndroidWorld SR grows 15.0% → 37.5% → 47.4% → 59.5% as training pairs grow 9K → 27K → 55K → 110K; MobileAgentBench from 17.0% to 49.0%. The verifier-as-annotator check: entropy predicts step correctness with AUC improving from 0.55 (iteration 2) to approximately 0.8; annotation accuracy improves from 0.51 to over 0.70, and on out-of-domain data prediction accuracy reaches 76%. Prefix caching gives a 10× decision-latency speedup.

## Where the evidence is thinner, in the paper’s words

- Baseline numbers are not rerun: “We directly adopt the SR number reported in the respective baseline papers on the corresponding benchmarks.” So cross-paper comparisons are not budget-matched.
- AndroidWorld is in-domain: “AndroidWorld is designated as the in-the-domain test set”; only the other two benchmarks’ apps were excluded from training-data collection.
- The working memory is written by GPT-4 and dominates step time (3.03 s); the paper explores but does not fully close this bottleneck.
- Failure study over 300+ tasks: hallucinated decisions remain the largest V-Droid failure category, and there is “an incomplete action space caused by inaccurate information from the accessibility service” — the a11y enumeration can miss actions. Text-only operation leaves “modality limitations” (tasks demanding vision).
- No seeds or variance are reported for any success rate.

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **transfer**, sub-pattern K02 (verifier reranks enumerated candidates). The score reflects what the paper reports: online evaluation on three public benchmarks, held-out applications for two of them, strong baselines, latency and cost reporting, a component ablation against same-base selector/generator alternatives, a validated verifier-as-annotator check (AUC), and released code. The judgment record flags that AndroidWorld is in-domain while the training data overlapped its apps (AP5), that baseline SRs come from their original papers rather than matched reruns, and that variance is not reported; AP14 (binding actions to a possibly incomplete structural element list) is flagged unclear. The radar did not rerun any experiment; every number here comes from the paper (version v5).
