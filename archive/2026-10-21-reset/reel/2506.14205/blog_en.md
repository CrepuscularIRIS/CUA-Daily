# AgentSynth: computer-use tasks that are easy to generate and hard to solve

*A CUA Radar reading of arXiv 2506.14205v2 (Jingxu Xie, Dylan Xu, Xuandong Zhao, Dawn Song; UC Berkeley; ICLR 2026). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2506.14205v2 · Code: https://github.com/sunblaze-ucb/AgentSynth*

## The problem

Human curation does not scale to generalist computer-use agents. The paper’s own accounting: OSWorld took roughly 1,800 person-hours for 412 tasks (about 4.4 hours per task, \$8.8–\$110 at a \$2–\$25/hour labor rate); TheAgentCompany reports 3,000 person-hours for 175 tasks (about 17 hours, \$34–\$425); τ-bench about 2 hours, \$4–\$50. Synthetic generation exists, but it is concentrated on web environments, and asking an LLM to invent a hard long-horizon task and then solve it in one shot mostly fails: in the paper’s control, a direct-instruction generator obtains a usable ground-truth trajectory for only 64% of “easy” targets (5–10 actions), 33% for medium, and 11% for hard (Table 5). So the tasks that most need data are the ones a one-shot generator cannot produce.

## What AgentSynth is

**The agent.** Perception is a full-screen 1920×1080 screenshot (about 1k–2k tokens depending on the tokenizer). Actions are OS-level pyautogui primitives; across the released dataset the action mix is click 59.1%, write 12.1%, press 8.2%, scroll 5.4%, move 5.3%, drag 4.6%, hotkey 3.0%, double-click 1.5%, wait 0.8%. The platform is OSWorld, a Gym-compatible simulated Ubuntu desktop, and the same pipeline is ported to the InSTA web environment (194 test tasks in 61 sequences) to show generality. On the CUA Radar board the paper sits in pattern K15: propose new tasks conditioned on the agent’s history and failures.

**The mechanism: information asymmetry.** Solving a task step-by-step in the forward direction is far easier than inferring the whole solution at once. AgentSynth exploits this with six LLM roles:

1.  **Task proposer** — an initial, persona-conditioned task (personas sampled from a persona hub; tasks requiring login or email sending are prohibited), achievable in a few atomic actions.
2.  **Executor** — a ReAct-style loop where GPT-4.1 plans the next action in natural language and OpenAI’s computer-use-preview model grounds it to pixel coordinates; at most 10 steps per subtask.
3.  **Verifier** — a WebJudge-style pipeline: extract key requirements, filter the screenshots that matter (downsampled), then output a binary success label plus a completion percentage.
4.  **Reviser** — if a subtask is only partially done, rewrite the task description to match what was actually completed.
5.  **Follow-up proposer** — sees the full subtask history and the previously failed tasks, and is explicitly told to propose something simpler that builds on the current state.
6.  **Summarizer** — composes the first n completed subtasks into one long-horizon instruction; that summary **is** difficulty level n.

**The training/steering signal.** Nothing is trained here; the output is a benchmark plus trajectory dataset (6,000+ tasks). The signal that shapes it is verification: only verified subtasks are chained, and failed tasks feed back into the next proposal. Difficulty is a dial: from level 1 to 6 the average horizon grows from 5 to 45 steps, memory span from 2 to 18 steps, apps from 1.2 to 3.3, app switches from 0.5 to 4.3; level-6 tasks typically take 40–60 steps, over 60% of trajectories touch two or more apps and over 40% touch three or more.

**Cost.** \$0.60 per trajectory (a typical trajectory is 50 steps across 6 subtasks, about \$0.011 per step; GPT-4.1 at \$2 per million tokens, computer-use-preview at \$3, GPT-4.1-mini at \$0.40 for verification). Six summarized tasks come from one sequence, so \$0.1 per task. The paper’s comparators: AgentTrek \$0.55, Explorer \$0.28, InSTA \$0.27 per trajectory.

## Results, as reported

All numbers below are online task success in OSWorld, judged by the paper’s automatic verifier, 50 tasks per difficulty level, bare LLMs emitting pyautogui code with no scaffold. From Table 6, with the Agent S3 scaffold:

| Setting (eval + generator)   | L1  | L2  | L3  | L4  | L5  | L6  |
|------------------------------|-----|-----|-----|-----|-----|-----|
| GPT-4.1 + S3, GPT-4.1 gen    | 36  | 18  | 14  | 14  | 10  | 10  |
| GPT-5.1 + S3, GPT-4.1 gen    | 62  | 32  | 20  | 22  | 16  | 14  |
| GPT-5.1 + S3, GPT-5-mini gen | 60  | 34  | 18  | 20  | 18  | 16  |
| GPT-5.1 + S3, GPT-5 gen      | 58  | 28  | 18  | 16  | 14  | 14  |
| GPT-5.1 + S3, GPT-5.1 gen    | 56  | 30  | 16  | 18  | 14  | 12  |

For bare LLMs (Figure 4), the text states: o4-mini falls from 18% at level 1 to 4% at levels 5 and 6; GPT-4.1 fails to complete tasks beyond level 3; at levels 4 and 6 only o4-mini and Claude-3.7 score non-zero, around 4%. Humans achieve 70% on 20 sampled level-6 tasks. Adding the Agent S3 scaffold roughly doubles the weaker models’ level-1 success and stays above bare agents at every level; the intermediate Agent S2.5 scaffold shows similar improvements. In the InSTA web port, summarized tasks are much harder than InSTA’s own: gpt-4.1 drops from 40% to 12.9% and o4-mini from 12% to 6.45%. The paper reports no offline step or grounding accuracy; everything above is online.

## What the paper’s own controls say

**The asymmetry ablation (Table 5)** is the load-bearing control. Generation success: direct instruction 64/33/11 (easy/medium/hard) versus AgentSynth 65/57/52 (levels 1/3/6) — chaining keeps trajectories obtainable exactly where one-shot generation collapses. Evaluation success (Agent S3, GPT-5.1): direct 60/51/48 versus AgentSynth 62/20/14 — the retained direct tasks stay easy for the agent, so simply filtering one-shot outputs cannot produce a hard benchmark.

**Generator swap (Table 6).** The full pipeline re-run with GPT-5-mini, GPT-5 and GPT-5.1 as the synthesis base: conclusions are unchanged, and stronger generators yield slightly lower evaluation success, which the authors read as harder or more diverse tasks.

**Verifier validation.** A human audit of 100 instances: feasibility 91%, subtask coherence 90%, persona relevance 94%, verifier accuracy 88%, with inter-rater agreement 0.74 (Cohen’s kappa). Calibration against graded human completion scores is monotone. An adversarial stress test accepts only 12% of near-miss perturbations (subtle goal violations) while accepting 94% of benign UI perturbations.

## Where the evidence is thinner

- No seeds or repeated runs are reported for the main OSWorld results; the paper states single success rates (2-sigma bars appear only on the InSTA appendix figure).
- Tasks are generated and evaluated in the same OSWorld environment; there is no evaluation on apps or sites held out from generation.
- Success is decided by the authors’ own LLM verifier — carefully stress-tested as above, but not a ground-truth oracle.
- The bare-LLM per-level values live only in Figure 4’s printed labels; the text quotes just the endpoints summarized above.
- On the generator model, the paper itself says it “remains an open and interesting research question” how model choice affects the realism and difficulty calibration of the generated tasks.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **online**, sub-pattern K15 (history-conditioned task proposal) under exploration-driven task synthesis. The score reflects what is reported: online OSWorld evaluation, cost per trajectory, an asymmetry ablation plus a generator-swap ablation, a stress-tested validator, scaffold comparisons (Agent S3), and released code. The judgment record flags: held-out environments unclear, variance unclear, budgets only partially matched between settings, and online success judged by the paper’s own verifier. The radar did not rerun any experiment; every number here comes from the paper (version v2).
