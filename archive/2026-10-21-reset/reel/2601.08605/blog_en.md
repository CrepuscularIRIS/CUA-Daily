# ExpSeek: a search agent that asks for experience only when its own entropy is high

*A CUA Radar reading of arXiv 2601.08605v2 (Zhang, Zhang, Yu, Nie, Wu, Yue, Liu, Li). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2601.08605v2 · Code: https://github.com/WYRipple/ExpSeek*

## The problem: experience arrives once, before the task

Many agents reuse past experience: stored trajectories, distilled patterns, or memories updated online. The paper observes that most of these methods inject the experience passively, as one global context block before the task starts. While the agent works, the observations keep changing, so a block written before step one may not fit what the agent is looking at in step six. The authors also argue that timing matters: seeking at every step is costly, and seeking rarely leaves a confused agent unaided.

## What ExpSeek is

This is a web search agent, not a GUI agent. It follows the ReAct loop: each step is a thought, then a tool call or an answer. It has two tools, Search (a search engine that returns URLs with snippets) and Visit (opens a URL and returns content that a summarization model has condensed). It perceives text only and acts through tool calls and a final answer tag. The agents are Qwen3-8B and Qwen3-32B, run in non-thinking mode with temperature 1.0 and top-p 0.95, capped at 30 ReAct steps (longer episodes count as failures). Board pattern: K27, retrieve past experience into context.

Three parts make up the mechanism.

1.  **An experience base of mistake triplets.** For each training question the agent is sampled five times, and successful and failed trajectories are paired. A tool model (Qwen3-235B-A22B-Instruct-2507) compares the failed trajectory with a successful one, labels each step as correct or not, and for every incorrect step writes a triplet: Behavior (what the agent saw and did), Mistake (what went wrong), Guidance (a direction to follow, without giving the answer). Triplets are grouped into topics, with separate bases for process steps and answer steps. The training set is 25% of each WebWalkerQA difficulty level (170 questions, random seed 0); the rest of WebWalkerQA is test data.
2.  **An entropy trigger.** Each step gets a step entropy, the mean token entropy of the response. On the training steps the paper finds that correct steps have lower entropy than incorrect ones (Kolmogorov-Smirnov 0.1998 for process steps and 0.3809 for answer steps), but the separation is weak for process steps (AUC 0.6223) and better for answer steps (AUC 0.7187). A logistic regression per step type gives a decision boundary; 1000 bootstrap resamples turn it into a 95% interval. Table 1 lists the intervals, for example \[0.314, 0.413\] for 8B process steps. At inference the guidance probability is 0 below the lower bound, 1 above the upper bound, and rises linearly in between. The step after a guided step is never guided.
3.  **A guidance generator.** When the trigger fires, an experience model (again Qwen3-235B-A22B-Instruct-2507) reads the history, picks the three most relevant topics, and writes guidance for the current situation from the triplets under those topics. For a process step the guidance is appended to the tool response. For an answer step it is returned as the observation, and the agent may refine the answer or call more tools.

No weights are updated: the agent is steered by the entropy of its own output and by guidance text generated from a base of labeled failures.

## Results, as reported

All numbers are accuracy (%) from an LLM judge (Qwen3-235B-A22B-Instruct-2507, temperature 0), the mean of five independent runs, on live web tools. There is no offline step-accuracy metric in the paper. The three benchmarks other than WebWalkerQA are not used to build the experience base. Rows are the Qwen3-8B agent unless marked.

| Method (Qwen3-8B) | WebWalkerQA Avg. | GAIA | SEAL-Hard | xbench-DeepSearch | Table 2 Avg. |
|----|----|----|----|----|----|
| No Experience (ReAct) | 38.47 | 29.13 | 23.23 | 25.60 | 32.23 |
| Training-Free GRPO | 40.62 | 29.32 | 25.59 | 26.00 | 33.79 |
| ReasoningBank+ | 40.78 | 32.04 | 26.38 | 28.00 | 34.80 |
| **ExpSeek** | **48.25** | **36.89** | **30.16** | **37.20** | **41.50** |

For Qwen3-32B the same table reports ExpSeek at 51.09, 43.88, 32.76, 42.00 and 45.32 in the same columns, against 39.33 for ReasoningBank+, 38.12 for Training-Free GRPO and 37.79 for no experience in the Avg. column. The paper states average absolute improvements of 9.3% and 7.5% over vanilla ReAct for the 8B and 32B agents, and up to 14.6% (32B on xbench). The paper says the baselines stay under 3% improvement or even degrade. ReasoningBank+ is the authors’ enhanced version of ReasoningBank, using a 235B model instead of a weaker agent to generate experience.

## What the paper’s own controls say

**Process versus answer steps (Table 2).** Guiding only process steps gives 36.59 on 8B, guiding only answer steps gives 39.06, against 41.50 for full ExpSeek. On 32B the figures are 40.81 and 41.20 against 45.32. The paper reports drops of 4.91 and 2.44 (8B) and 4.51 and 4.12 (32B), and links the smaller drop for answer-only guidance to the cleaner entropy separation of answer steps.

**Trigger alternatives (Table 3, Qwen3-8B).** On GAIA, a rule that intervenes from the first step with the same experience model reaches 38.81 accuracy with 9.52 steps and 329.71 s per question; a Claude-sonnet-4 reward-model trigger reaches 39.47 with 8.55 steps and 370.82 s; the entropy trigger reaches 36.89 with 5.75 steps and 127.57 s; no experience takes 4.47 steps and 66.94 s with 29.13. The paper reads these as similar accuracy at a lower cost for the entropy trigger (the rule trigger takes 1.7 times the steps and 2.6 times the time of the entropy trigger on GAIA, in the paper’s words). On GAIA the two alternatives have the higher accuracy figure; on xbench the entropy trigger scores 37.20 against 36.40 and 36.60. Retrieving the nearest experience (text-embedding-v4) instead of generating guidance gives 30.92 on GAIA and 27.80 on xbench.

**Cost against no guidance.** ExpSeek uses more steps and time than vanilla ReAct: on xbench 5.73 steps and 143.81 s against 3.31 steps and 51.06 s. A 235B model also runs at every guided step, and no compute budget matched to the baselines is reported beyond the 30-step cap.

**Scaling and transfer.** A 4B or 30B experience model instead of 235B still helps; the 4B model improves the 32B agent by 5.2% and 9.7% points on GAIA and xbench. Swapping the 8B and 32B experience bases costs accuracy (for the 32B agent, 40.33 on GAIA and 37.20 on xbench with the 8B base, against 43.88 and 42.00). With just one experience per topic the paper says the experience model still maintains high accuracy; removing the base entirely degrades performance, but substantial accuracy remains.

**Pass@3 (Table 5).** Average Pass@3 is 61.89 (8B) and 64.96 (32B), against 48.99 and 56.21 without experience.

## Where the evidence is thinner

- Only five-run means are reported; there is no standard deviation or confidence interval, so the run-to-run spread is unknown from the paper.
- Scoring uses an LLM judge, and the paper does not report a check of that judge.
- Paper’s own limitation: “The current threshold estimation relies on the training set and the tool model’s assessment of step quality; more accurate strategies need to be investigated.”
- The experience comes from WebWalkerQA training questions, so its test split is in-distribution; only GAIA, SEAL-Hard and xbench are out of distribution.

## CUA Radar’s read

CUA Radar scores this paper **73 (★★★)**, evidence level **online**. The score reflects real-world web benchmarks, three held-out benchmarks, a stronger baseline variant, step and time cost reporting, a process/answer ablation, and released code. Budget match is marked partial, and variance and a judge check are not reported. The judgment record also flags the dependence of the thresholds on the training set and the tool model. The radar did not rerun any experiment; every number here comes from the paper (version v2).
