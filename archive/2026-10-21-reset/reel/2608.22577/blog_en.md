# CausalCache: a GUI agent that decides which past screenshots deserve to be seen again

*A CUA Radar reading of arXiv 2608.22577v2 (Luo, Liao, Teng, Wang). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.22577v2 · Code: none linked in the paper version read.*

## The problem: text is cheap, screenshots are not

A long-horizon GUI agent accumulates screenshots, actions, text arguments and coordinates over many decisions. The complete action trace can be kept cheaply as compressed text, but keeping every screenshot in the active context is costly and distracting; the paper’s abstract puts it as “only a few historical screenshots fit in active context”. The standard answer is recency: show the latest few screenshots. The paper reframes the choice. Every past event stays in the prompt as a one-line text summary, and a fixed budget of B events additionally regains its archived screenshot. The question is which B events. Under this formulation, Recent-B gives all B slots to the latest events, and CausalCache reallocates the same B slots over the whole trace, with recent events as the default.

The authors argue that the value of restoring a screenshot depends on which images are already active: a distant frame may lack local grounding without recent images, or be redundant next to a saturated recent window. They also report that a strong frozen policy shows weak and unreliable average selectivity when old and recent frames are swapped under matched conditions, so the choice has to be learned.

## What CausalCache is

**Agent.** The policy is the frozen GUI-Owl-1.5-8B-Instruct. At each decision it sees the goal, the text summaries of all earlier events, the current screenshot and up to B restored history screenshots; it emits the next GUI action (type, arguments, coordinates). The paper evaluates on desktop (OSWorld-Verified) and mobile (MobileWorld). On the CUA Radar board the architecture pattern is C15, context control inside the agent loop.

**Two learned parts.** (1) HGKV, a history-gated key/value adapter: rank-8 low-rank residuals on the key and value projections of the last eight language-model layers, applied only to image tokens of restored history events. A mask built from the token-type sequence keeps instruction text, summaries, the current screen and action tokens untouched, and when no history image is active the policy is bitwise identical to the frozen one. (2) A budget-aware restoration selector that scores the complete summarized trace and returns an exact-B set. A distant event enters only if its predicted marginal utility beats that of the recent frame it displaces; declining every replacement recovers Recent-B exactly.

**Two-pass inference.** Pass 1 renders the default Recent-B prompt and yields a proposal action. The selector uses that proposal as a reference. Only if a recent slot is displaced is the prompt re-rendered and the same frozen weights produce the final action. Decoding is greedy, so the second pass replaces the proposal and is not best-of-n.

**Training signal.** Policy adaptation and selector training use only desktop data: successful AgentNet/OpenCUA Ubuntu trajectories (5,000 screened, 2,293 successful, 6,003 decision points). For each decision point the authors build matched-budget groups with the same summaries, screen and target: Recent-B, a relevant restore (oldest recent slot replaced by the screenshot preceding an earlier equivalent action) and a wrong restore (an age-matched screenshot whose following action is not equivalent). Group counts at B=1/2/4 are 969/764/470. The adapter is trained with a difference-of-differences objective in which every arm is anchored to its own frozen score, so uniformly amplifying all restored images earns nothing. Selector labels are policy utilities re-scored through the frozen adapted policy.

## Results as reported

All closed-loop numbers are online task success (%) at the primary budget B=4. MobileWorld is zero-shot, mean of three runs; OSWorld-Verified (361 tasks, official no-GDrive roster) is one run per arm under the official 15-step cap.

| Method | MobileWorld (117) | memory-critical (62) | single-app control (55) | OSWorld-Verified (361) |
|----|----|----|----|----|
| Frozen, summary-only (B=0) | 28.2 | 21.0 | 36.4 | 19.9 |
| Frozen + Recent-B | 29.9 | 22.6 | 38.2 | 32.7 |
| HGKV + Recent-B | 30.2 | 19.4 | 42.4 | 33.0 |
| Frozen + selector | 33.9 | 28.0 | 40.6 | 32.7 |
| **CausalCache (HGKV + selector)** | **36.8** | **30.6** | **43.6** | **33.3** |

The memory-critical stratum is the 62 MobileWorld tasks that the benchmark’s metadata marks as multi-app (information from one app is needed after switching to another); the 55 single-app tasks are controls. The paper reports +11.2 points on the memory-critical stratum (30.6 vs 19.4) and +1.2 on controls (43.6 vs 42.4), with a split-by-method interaction of +10.1 points. The paper’s own caveat about the full-roster mean: 47% of the roster is control tasks on which no restoration method should help.

On desktop under the official 15-step cap, every high-fidelity arm reaches 32.7 to 33.3, about 13 points above summary-only memory (19.9), and the allocations are statistically indistinguishable. The paper notes that 352 of 361 episodes exhaust the 15-step cap. With the cap doubled to 30 steps, Recent-4 reaches 42.4 and CausalCache 46.7, a margin of +4.3 points against +0.3 at 15 steps. This 30-step run is a diagnostic rerun of the two arms.

All of this is online evaluation. The offline numbers in the paper are teacher-forced log-likelihood margins on held-out desktop groups, discussed below, and are not success rates.

## What the paper’s own controls say

- **Same budget, same prompt.** Every compared allocation carries exactly B images with identical resolutions, summaries and structure, so the contrast isolates which events are promoted. Recent-B arms with and without the adapter (29.9 and 30.2) and the summary-only baseline (28.2) are statistically indistinguishable on MobileWorld, which the authors read as the gain coming from the allocation and not from the adapter or recency.
- **Selector on a frozen policy.** Running the selector without the adapter gives 33.9 on MobileWorld; teaching the selector from frozen-policy-scored labels gives 33.3. Both retain part of the margin, and the authors conclude the adapter contributes at deployment and as the utility teacher.
- **Chooser ladder (offline).** Log-likelihood margin over Recent-B at B=2 and B=4: learned scorer +.030 and +.017, random exact-B +.006 and +.008, RGB similarity +.006 and +.007, inverted score −.016 and −.009, no recency features +.012 and +.008. Only the learned ranking and its inversion separate from zero.
- **Adaptive spending.** At B=4 the learned scorer keeps the entire recent window on 19% of states and replaces all of it on 26%, although training supervises only single-slot replacement.
- **Pixels vs text (memory-critical split).** On the selector plus frozen deployment, pixels score 28.0. Replacing each restored frame with the verbatim recorded response gives 18.0 (task-paired p=0.006) and with an OCR transcript 24.2; the OCR margin over Recent-4 does not separate from zero, while pixel restoration’s does.
- **Cost.** CausalCache adds a median of eight policy calls per task, about 7% of median end-to-end task time. On mobile the second pass fires on 81 to 87% of audited steps, and added model time per step is 2.0, 2.3 and 2.9 s at B=1, 2 and 4.

## Where the evidence is thinner, in the paper’s words

- Under the official 15-step cap on OSWorld, “CausalCache and Recent-4 are statistically indistinguishable”; the separation appears only in the 30-step diagnostic.
- OSWorld arms are one run each, while MobileWorld uses three runs.
- “We control an active context budget, not archive capacity, and CausalCache reattaches rather than generates pixels.”
- “We claim only that some summarized events have greater conditional marginal utility than the recent realization they displace; pretraining contamination remains possible.” The word causal is used only for policy-specific effects of matched prompt interventions, not structural causal discovery.
- Full confidence intervals, per-budget tables and mining details are in a supplement that was not part of the PDF read here, so this summary uses only the main text.

## CUA Radar’s read

CUA Radar scores this paper **71 (★★★)**, evidence level **transfer**: the adapter and selector are trained on desktop trajectories and evaluated zero-shot on mobile. The judgment record credits online evaluation, a held-out environment (no mobile data touches training or selection), multiple runs on MobileWorld, strong same-budget baselines, cost reporting and a component ablation; code is not reported. No failure flags are recorded. The radar did not rerun any experiment; every number here comes from the paper (version v2).
