# VeriEnv: train web agents inside cloned websites, with rewards read from the database

*A CUA Radar reading of arXiv 2603.10505v1 (Chae, Park, Ritter). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2603.10505v1 · Code: https://github.com/kyle8581/VeriEnv (the paper says code and resources will be released upon acceptance)*

## The problem: real websites are a poor training ground

Self-evolving web agents generate tasks, try them, and learn from the outcome. The paper lists three obstacles when this happens on live sites. Exploration can be unsafe or restricted: actions may affect other users, violate platform policies, or be blocked by Cloudflare and CAPTCHAs. Self-generated tasks are often underspecified, with several valid answers. And the reward usually comes from an LLM acting as judge, which the authors describe as error-prone compared with verification-based rewards. VeriEnv’s answer is to move training off the real site: clone it, and use the clone’s own database to decide whether a task was solved.

## What VeriEnv is

The agent being trained is a web agent that interacts with a cloned website through browser actions and observations (the paper’s overview figure names a BrowserGym interface; the text does not spell out whether observations are screenshots, accessibility trees or DOM). The platform is the web only. On the CUA Radar board the paper sits under sub-pattern K13, “synthesise tasks from checkers/specs so verifiable reward exists by construction”, part of the main pattern “ground reward in executable checkers”.

The mechanism has three parts.

1.  **Environment cloning.** A coding agent (GPT-5.2, driven through Cursor CLI) receives screenshots of a real site and builds a synthetic environment (C, D, P): application code C, a database D, and a Python SDK P that gives controlled internal access for querying and verifying state. It also writes start-up and reset scripts. The agent then tests the deployed clone with Playwright MCP, files bug reports and patches them, in a loop. The authors say the clone is not identical to the original site but keeps the functional structure needed for training.
2.  **Verifiable tasks and judges.** An LLM writes about 50 tasks per site. Each comes with a validation program that uses the SDK. Running the program both checks that the task is executable and yields the expected answer, which becomes a rule-based judge (for example, `must_include` of a listing name and price). At the end of an episode the judge queries the database state and returns a binary reward.
3.  **Training.** The paper uses reward-based rejection fine-tuning as its example method: sample trajectories for each task and keep only those that pass the validator, then fine-tune on them. New tasks and trajectories are folded back in over time. Training uses LLaMA-Factory for two epochs on two NVIDIA A40 GPUs. The SDK is used only by the validator and is never accessible to the agent; environments run sandboxed with external network access disabled.

Scale as reported: 149 websites (chosen by reference to the Mind2Web and Mind2Web-Online site lists), 7,400 tasks in total, of which 2,972 (40.2%) are easy, 2,900 (39.2%) medium and 1,528 (20.6%) hard. Building a site takes 83.5 minutes and \$3.6 on average, including debugging and task generation. The training runs use 97 of the websites.

## Results as reported

All results are **online** success rates; the paper has no offline step-accuracy numbers. Two base models are trained: Qwen3-4B and LLaMA-3.2-3B-Instruct. Synatra (synthetic trajectories from tutorials) and ADP (the Agent Data Protocol, a unified collection of agent datasets) are the open-source comparisons, trained on the same base models. Sites overlapping the test splits of the evaluation benchmarks were excluded from cloning and training.

**WebArena-Lite** (5 sites, Table 4):

| Model                 | Shopping | CMS   | Reddit | GitLab | Map   | Total |
|-----------------------|----------|-------|--------|--------|-------|-------|
| GPT-4o\*              | 23.91    | 31.43 | 28.57  | 56.25  | 19.35 | 31.52 |
| Qwen3-4B              | 3.77     | 6.67  | 4.17   | 13.89  | 14.29 | 7.88  |
| \+ Synatra            | 0.00     | 0.00  | 12.50  | 8.33   | 0.00  | 3.64  |
| \+ ADP                | 4.35     | 5.71  | 9.52   | 3.13   | 9.68  | 6.06  |
| \+ VeriEnv            | 4.35     | 20.00 | 23.81  | 12.50  | 16.13 | 13.94 |
| LLaMA-3.2-3B-Instruct | 0.00     | 2.86  | 9.52   | 3.13   | 3.23  | 3.03  |
| \+ Synatra            | 2.17     | 2.86  | 14.29  | 9.38   | 6.45  | 6.06  |
| \+ ADP                | 4.35     | 11.43 | 14.29  | 12.50  | 6.45  | 9.09  |
| \+ VeriEnv            | 4.35     | 17.14 | 19.05  | 15.63  | 12.90 | 12.73 |

**Mind2Web-Online** (220 of the 300 tasks, after removing tasks on sites that block agents; scored with WebJudge-7B; Table 5):

| Model                 | Easy  | Medium | Hard  | Total |
|-----------------------|-------|--------|-------|-------|
| Browser-Use-GPT-4o\*  | 55.40 | 26.60  | 8.10  | 30.00 |
| Claude-3.5-Sonnet\*   | 56.60 | 26.60  | 6.80  | 28.80 |
| Qwen3-4B              | 26.32 | 9.41   | 11.63 | 13.18 |
| \+ Synatra            | 35.09 | 5.88   | 9.30  | 14.55 |
| \+ ADP                | 26.32 | 7.06   | 6.98  | 11.36 |
| \+ VeriEnv            | 29.82 | 23.53  | 6.98  | 20.45 |
| LLaMA-3.2-3B-Instruct | 19.30 | 12.94  | 0.00  | 11.36 |
| \+ Synatra            | 24.56 | 15.29  | 6.98  | 14.55 |
| \+ ADP                | 42.11 | 24.71  | 11.63 | 24.09 |
| \+ VeriEnv            | 40.35 | 29.41  | 13.95 | 24.55 |

Rows marked \* are numbers taken from other papers, not runs under the same setup. The paper’s own delta column gives +6.06 (Qwen3-4B) on WebArena-Lite and +7.27 on Mind2Web-Online, and +13.19 for LLaMA on Mind2Web-Online. One inconsistency to note: the text (Section 4.1 and the Introduction) states +9.09 for LLaMA-3.2-3B on WebArena, while Table 4’s delta column lists +9.70.

## What the paper’s own controls say

- **Same base model, same fine-tuning style.** Within each group the baselines start from the same base model, so the comparison is against other training data, not other models. On Qwen3-4B, both Synatra and ADP end below or close to the base on WebArena-Lite (3.64 and 6.06 against 7.88), and the authors report that ADP’s mixed data hurt action formats for Qwen. On LLaMA, ADP reaches 24.09 on Mind2Web-Online against VeriEnv’s 24.55; the authors attribute ADP’s gain there to dataset overlap between its training data and the evaluation distribution.
- **Held-out sites.** Overlapping sites are excluded, so WebArena-Lite is described as fully out-of-domain for the cloned training sites.
- **Environment quality, checked by humans.** Four graduate-student annotators rated generated sites and tasks. Average functional correctness was 90.3% (navigation and forms 100%, search 81%), visual quality 4.7 out of 5, task executability 90% and judge correctness 76%, with mean Cohen’s κ = 0.61. The most common judge errors came from database resets that did not preserve the random seeds; the authors say re-running the validation programs detects and resolves these.
- **Site-specific training against PAE** (Figure 4, no numbers in the text). Training inside a clone of a single website (the WebArena sites, used only through their clones) is compared with PAE, which uses real sites and a VLM judge. The authors report larger and more stable gains for VeriEnv, strongest in CMS and Shopping.
- **Scaling** (Figure 5, no numbers in the text). Performance generally rises as the share of training environments grows, on both benchmarks, while the fixed-data baselines stay roughly flat.

## Where the evidence is thinner

- There is **no component ablation**. The PAE comparison changes several things at once (real versus cloned site, non-verifiable versus verifiable tasks, VLM versus rule-based judge), so it does not isolate which part matters.
- **No seeds, standard deviations or confidence intervals** are reported; each cell is a single number.
- Absolute rates stay low: the best Qwen3-4B result on WebArena-Lite is 13.94 against 31.52 reported for GPT-4o. Per-site numbers are mixed: Qwen3-4B with VeriEnv scores 12.50 on GitLab, below the base model’s 13.89, and 6.98 on Mind2Web-Online hard tasks, below the base’s 11.63.
- Mind2Web-Online is scored by WebJudge-7B, a model judge, so the evaluation side is not rule-verified even though training rewards are. The paper does not say which model samples the trajectories for rejection fine-tuning beyond the description above.
- Judge correctness of 76% means some training rewards may be wrong. The sim-to-real gap is argued (“much smaller” than in robotics) rather than measured, and the authors say cloned sites are not identical to the originals. Site counts differ between sections (149 in Table 1; 136 candidates and 97 validated sites in the filtering figure).
- Only rejection fine-tuning is tried; reinforcement learning on these environments is left to future work.

## CUA Radar’s read

CUA Radar scores this paper **74 (★★★)**, evidence level **transfer**. The record credits online evaluation, held-out sites, open-source baselines, cost reporting and a tested validator check (task executability 90%, judge correctness 76%). It marks variance and budget matching as unclear, the component ablation as not reported, and code as announced but not yet released. The judgment flags one anti-pattern, AP2: a synthetic environment used as the training world without a measured gap to the real one. The radar did not rerun any experiment; every number here comes from the paper (version v1).
