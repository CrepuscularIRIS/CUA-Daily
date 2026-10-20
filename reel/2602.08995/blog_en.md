# DeAction: a pre-execution guardrail that catches off-task computer-use actions and sends feedback

*A CUA Radar reading of arXiv 2602.08995v2 (Ning, Jones, Zhang, Ye, Ruan, Li, Gupta, Sun). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2602.08995v2 · Code: https://github.com/OSU-NLP-Group/Misaligned-Action-Detection*

## The problem: actions that drift from what the user asked

Computer-use agents sometimes take actions that deviate from the user’s original intent. The paper separates three kinds: following malicious instructions injected into the environment, causing harmful side effects through the agent’s own mistakes, and doing other task-irrelevant things such as opening unrelated apps. It names three gaps in existing defenses: many are tied to fixed policies or known attack types, existing benchmarks label whole trajectories rather than single actions, and simply blocking an action stalls the task instead of helping the agent recover.

## What DeAction is

DeAction is a guardrail that sits between a computer-use agent and the machine. It is not trained: it is a set of LLM prompts that work with any agent without access to its internals. When the agent proposes an action (the agents here act through pyautogui code), DeAction holds it and judges it against the user’s task before anything executes.

1.  **Narrative summary.** After each executed step, the observation-action-observation triple is turned into a short text description. These summaries replace raw screenshots as history and are built in parallel with execution.
2.  **Fast check.** One LLM call returns a one-sentence reason and either approves a clearly aligned action or sends it on. It is meant as a conservative filter for routine steps.
3.  **Systematic analysis.** Four parts: injection analysis (does the screenshot contain instructions that could redirect the agent), action understanding, outcome prediction and a misalignment judgment with a readable rationale.
4.  **Iterative correction.** A misaligned action is not just blocked. The agent gets structured feedback saying why (for example an injection, a harmful outcome or an intent mismatch) and proposes a revision, which is re-checked, for at most 3 rounds.

On the CUA Radar board the paper sits in pattern C34, injection defense and isolation.

## Results, as reported

**Offline detection on MisActBench**, the authors’ benchmark of 558 trajectories and 2,264 human-annotated action steps, of which 1,264 are aligned. It combines trajectories from attacks on OS-Harm, DoomArena, RedTeamCUA and RiOSWorld with synthesized unintended behaviors in benign tasks. F1 with misaligned actions as the positive class:

| Backbone          | Task Shield | InferAct | DeAction |
|-------------------|-------------|----------|----------|
| Qwen3-VL-32B      | 58.4        | 61.6     | 70.7     |
| Claude Sonnet 4.5 | 66.6        | 64.3     | 80.4     |
| GPT-5.1 Instant   | 65.1        | 64.7     | 79.4     |
| GPT-5.1 Thinking  | 66.9        | 62.3     | 82.8     |

The paper notes that Task Shield and InferAct often reach high recall but with precision around 50%, while DeAction’s precision reaches up to 89.9%.

**Online evaluation.** RedTeamCUA (50 high-risk end-to-end tasks, indirect prompt injections, 50-step cap) gives attack success rate (ASR, lower is better) and utility under attack (UA, higher is better); OSWorld (15-step cap) gives task success rate (SR). The guard uses GPT-5.1 Instant and at most 3 corrections.

| Agent             | Defense                | ASR         | UA          | OSWorld SR  |
|-------------------|------------------------|-------------|-------------|-------------|
| Claude Sonnet 4.5 | none                   | 60.0        | 44.0        | 42.9        |
| Claude Sonnet 4.5 | DeAction               | 6.0         | 76.0        | 40.7        |
| OpenAI CUA        | none                   | 42.0        | 82.0        | 26.0        |
| OpenAI CUA        | DeAction               | 4.0         | 84.0        | 30.7        |
| OpenCUA-72B       | none                   | 32.0        | 48.0        | 39.0        |
| OpenCUA-72B       | DSP / PromptArmor      | 24.0 / 26.0 | 52.0 / 44.0 | 38.3 / 35.2 |
| OpenCUA-72B       | Task Shield / InferAct | 22.0 / 22.0 | 58.0 / 70.0 | 36.6 / 36.5 |
| OpenCUA-72B       | DeAction               | 2.0         | 60.0        | 39.6        |

The paper reports ASR reduced by over 90% for every agent, with OSWorld success “comparable or sometimes improved”. InferAct has the higher UA on OpenCUA-72B (70.0 against 60.0), with higher latency.

## What the paper’s own controls say

**Cost and routing.** Guardrail reasoning takes 7.2 s of a 28.1 s average step (25%). The fast check approves 45% of actions directly, at 3.2 s each. 16% of steps are flagged as misaligned, 78% of those end up corrected, and 62% are fixed in a single revision.

**Ablations** (a 566-step subset of MisActBench, GPT-5.1 Thinking). Fast check only: F1 77.8 at 4.2 s; systematic analysis only: 80.1 at 13.1 s; the default two-stage design: 79.9 at 11.3 s. Downgrading the systematic analysis model to GPT-5 mini drops F1 to 70.8, while GPT-5 mini for the fast check and the summarizer together gives 80.4 at 65% lower cost. Narrative summaries use 41 tokens per step against over 1K tokens per screenshot, and about 11 s latency per step against 18 s with screenshots. With the cheaper configuration online, ASR is 8.0 for all three agents.

**Failure modes.** The paper lists well-disguised malicious instructions that fool the fast check, weak grounding when reading coordinate-based actions, and overly narrow notions of task relevance. Malicious instruction following is the easiest category to detect; the two internally arising categories are harder to detect and classify.

## Where the evidence is thinner

- The 50 RedTeamCUA tasks are those with the highest attack success rates in the original benchmark, so ASR is measured on the hardest cases. Each task is 2 percentage points; no repeats or seeds are reported.
- Competing defenses were run online only on OpenCUA-72B.
- The OSWorld no-defense numbers are taken from the OSWorld leaderboard without re-running, while DeAction runs used a 15-step cap, so the SR comparison is not matched.
- MisActBench is built by the same authors, with a balanced label mix; the paper says real traffic with mostly aligned actions would let the fast check bypass more steps.
- The CUA Radar record marks held-out evaluation, variance and code as unclear; the paper’s first page links a project page.

## CUA Radar’s read

CUA Radar scores this paper **67 (★★)**, evidence level **online**. The record credits online evaluation on two benchmarks, four baselines, a matched maximum of 3 corrections, runtime cost, a component ablation and a human-labelled detection benchmark; it records no flags. The radar did not rerun any experiment; every number here comes from the paper (version v2).
