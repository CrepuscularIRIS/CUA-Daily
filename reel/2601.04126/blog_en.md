# InfiniteWeb: synthesize the whole training gym — functional websites with dense evaluators, at scale

*A CUA Radar reading of arXiv 2601.04126v3 (Zhang, Wang, Zhang, Guo, Li, Li, Lu; Peking University, Nanjing University, Microsoft Research Asia). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2601.04126v3 · Code (as listed in the paper’s abstract): https://github.com/microsoft/FIVE-UI-Evol*

## The problem: environments, not tasks, are the bottleneck

RL-trained GUI agents need interactive environments to train on, and the existing ones — Mini-WoB++, WebArena, OSWorld — are hand-built: tens to hundreds of applications, each needing someone to design the site or install the app, define tasks and write evaluation criteria. Recent synthesis work generates tasks or trajectories, but still inside those same benchmark environments. The paper asks whether the environments themselves can be generated automatically, and identifies three reasons naive LLM generation fails: **consistency** (independently generated pages disagree on data formats, interface signatures and state management, breaking cross-page interactions), **correctness** (functional bugs compound over long-horizon tasks and produce wrong reward signals that “destabilize reinforcement learning”), and **diversity** (repetitive task patterns and homogeneous visual styles risk overfitting).

## What InfiniteWeb is

Two agents appear in this paper. The **generator** is an agentic pipeline built on GPT-5 (reasoning effort “high”). Its inputs are a website seed (a short description) and a reference design image, both sampled from Common Crawl. Four stages follow, with backend and frontend running in parallel:

1.  **Unified Specification.** Generate 8–10 realistic user tasks for the seed, then derive shared data models and user-facing interfaces from those tasks. Every page implements the same specification; system-managed parameters (userId, sessionId) are hidden and state lives in localStorage, which “enables data persistence across pages without a backend server.”
2.  **Task-Centric Backend (TCTDD).** Concrete data is generated to be consistent with the tasks; test cases are derived from task specifications, and implementation code is iteratively refined until all task-relevant tests pass (at most 8 iterations; 1.5% of sites remain unfixed). Correctness is required only on the task-induced subspace, not the whole website.
3.  **Design-Guided Frontend.** A vision-language model extracts the color system, typography, spacing and component styling from the design image; a shared page framework and then each page’s HTML/CSS/JS are generated against that style, calling the backend SDK.
4.  **Automatic Evaluator Generation.** Instrumentation checkpoints are written to localStorage when key functions execute; a generated JavaScript evaluator combines weighted checkpoints (e.g. 0.35 / 0.30 / 0.35) and returns a dense 0.0–1.0 score with partial credit.

The **trainee** is UI-TARS-1.5-7B: a screenshot goes in, low-level GUI actions come out. It is trained with GRPO on the generated sites using the dense reward (600 tasks, 8 trajectories per task, max 15 steps per episode, 128 parallel environments). On the CUA Radar board this is sub-pattern K13 — synthesize tasks from checkers/specs so that a verifiable reward exists by construction — under the main pattern “ground reward in executable checkers”.

## Results, as reported

All agent numbers below are **online** success rates. Every row uses the same trainee, UI-TARS-1.5-7B; OSWorld numbers are OSWorld-Verified under a 15-step cap; standard deviations are over three runs where reported.

| Training data | Online-Mind2Web (live web) | OSWorld (desktop) | MobileWorld (mobile) |
|----|----|----|----|
| original UI-TARS-1.5-7B | 23.0 ± 0.9 | 24.5 ± 1.2 | 6.4 |
| Claude-Code sites, 600 tasks | 23.7 | 25.2 | 5.1 |
| InfiniteWeb, 200 tasks | 25.3 ± 1.0 | 27.3 ± 0.9 | — |
| InfiniteWeb, 400 tasks | 27.3 ± 1.4 | 29.7 ± 1.1 | — |
| InfiniteWeb, 600 tasks | 28.7 ± 1.2 | 31.4 ± 1.0 | 10.3 |

The paper reports improvements of +6.9 on OSWorld, +5.7 on Online-Mind2Web and +3.9 on MobileWorld. Table 2 also lists, under the same 15-step cap, Claude-4-Sonnet at 31.2, Doubao-1.5-thinking-0428 at 28.1 and OpenCUA-32B at 29.7 ± 1.1. The paper describes Online-Mind2Web as in-domain generalization (real websites never seen in training), OSWorld as out-of-domain transfer, MobileWorld as mobile transfer.

A separate axis measures the generated websites, not the trainee. On WebGen-Bench (101 sites; an LLM agent executes predefined tasks on each generated site), task completion over three runs is: InfiniteWeb 85.6 ± 1.2, Codex 80.8 ± 0.4, Claude-Code 75.8 ± 2.4, Bolt.diy 67.1 ± 1.8, all baselines using GPT-5. In LLM-as-judge visual comparisons, InfiniteWeb wins 85.4 ± 0.5 against Claude-Code, 84.2 ± 0.8 against Bolt.diy and 69.3 ± 0.7 against Codex. On the generated environments themselves, UI-TARS-1.5-7B scores 7.4 and Agent S2 14.1, versus 24.5 and 27.3 on OSWorld, which the paper reads as higher difficulty and better discriminability between agents.

## What the paper’s own controls say

- **Quality vs quantity.** With the same 600-task GRPO budget on Claude-Code-generated websites, gains are marginal or negative (+0.7 Online-Mind2Web, +0.7 OSWorld, −1.3 MobileWorld); the paper concludes “data quality, not quantity, drives the improvement.” Claude-Code sites average 4.9 pages per website versus 12.6.
- **Ablations.** On WebGen-Bench, removing the TCTDD loop gives 82.6 ± 1.4 and swapping GPT-5 for GPT-4.1 gives 77.4 ± 1.4, against 85.6 ± 1.2 full. Note a paper-internal inconsistency: the text quotes the TCTDD drop as 5.0 points (to 80.6), while Table 6 lists 82.6 ± 1.4; the backbone drop is quoted as 8.2 points.
- **Dense vs binary reward.** Over 4,000 tasks with 4 trajectories each, 767 tasks are discriminative for GRPO with the dense reward versus 174 with binary reward — a 4.4× increase in usable training signal.
- **Statistics.** Welch’s t-tests confirm the WebGen-Bench gaps against all three baselines, and the Online-Mind2Web gains for each task count.
- **Cost.** A website costs about 0.36M input and 0.34M output tokens — \$1.93 at GPT-5 batch pricing, median 20 minutes; 600 sites generate in about 125 minutes in parallel, and generation accounts for 6.9% of total training time. The paper contrasts this with OSWorld’s roughly 1,800 person-hours for 369 tasks.
- **Human checks.** Human evaluators agree with the GPT-5 visual judge in 91% of 100 sampled comparisons, and 95 of 100 sampled tasks pass human verification of task description and automatic evaluator.

## Where the evidence is thinner, in the paper’s words

- “Our current tasks operate within individual websites. Cross-website tasks, such as comparing prices across multiple shopping sites … represent an important real-world scenario not yet covered.” (Multi-application tasks in OSWorld did improve, 3.8 to 9.7.)
- “our current system only generates web environments” — native mobile application generation is future work despite the MobileWorld transfer.
- Generation cost and latency “remains an engineering direction”, at \$1.93 per site and a 20-minute median.
- The radar’s record additionally notes that the generated evaluator is validated only by the 100-task human check, and that the training mixture contains no real environments.

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **transfer**. The score reflects what the paper reports: online evaluation on three real benchmarks, held-out environments, three-run variance with t-tests, cost reporting and a component ablation. The judgment record flags: a synthetic-only training mixture (anti-pattern AP2, a generated environment without a real anchor in training); the generated evaluator recorded as untested as a judge (validator check “untested”, against the paper’s own 95/100 human verification of a sample); strong-baseline and budget matching recorded as partial; and code recorded as announced rather than released, although the paper’s abstract links github.com/microsoft/FIVE-UI-Evol. CUA Radar did not rerun any experiment; every number here comes from the paper (version v3).
