# UI-NEXUS and AGENT-NEXUS: from atomic mobile tasks to compositional ones, via a GPT-4o scheduler

*A CUA Radar reading of arXiv 2506.08972v1 (Guo, Miao, Wu, Cheng, Zhou, Zhang; Shanghai Jiao Tong University and Langboat Technology). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2506.08972v1 · Project page: https://ui-nexus.github.io*

## The problem: agents pass atomic tests and stall on real instructions

Most mobile-agent research evaluates atomic tasks: short-chain execution (“look up the best rated coffee maker”) or single-screen grounding (“click the submit button”). Real user instructions compose. The paper defines three composition types by subtask dependency structure: **Simple Concatenation** (independent subtasks in sequence), **Context Transition** (a subtask consumes the output state of another), and **Deep Dive** (intermediate reasoning such as aggregation or summarization is needed between operations). On such tasks the authors observe characteristic failure modes: over-execution (redundant actions after the task is done, or fabricated values when intermediate data were never collected), under-execution (abandoning subtasks midway), context confusion (fulfilling app B’s requirement while interacting with app A), and attention drift (dropping requirements or whole subtasks).

## What the paper delivers: a benchmark plus a scheduling system

**UI-NEXUS** is an interactive Android benchmark: 100 task templates across 50 apps — 20 local utility apps plus 30 online service apps, bilingual (Chinese and English) — with an average optimal step count of 14.05, built on a modular infrastructure (agent configuration, device management, trajectory evaluation). The controllable subset **UI-NEXUS-ANCHOR** covers the 50 tasks on local utility apps, run in an Android emulator (Pixel 6, API level 33, the AndroidWorld system image) with AndroidWorld-style automatic reward signals. Online service apps run on physical devices and are scored with MLLM-as-a-Judge plus human verification. The step budget is roughly twice the human-annotated optimal steps, the same cap for every agent. Metrics pair performance (success rate; termination reason: successful, premature, budget exceeded, deemed impossible, collapse) with efficiency (USD per step, seconds per step).

**AGENT-NEXUS** is the paper’s scheduling system — on the CUA Radar board it instantiates pattern C17, a manager that plans subgoals and workers that execute them. A GPT-4o **orchestrator** decomposes the compositional instruction into a plan of self-contained atomic subtasks, each typed `act` (UI manipulation), `think` (reasoning without modifying the environment) or `tool` (a predefined operation; in this implementation the only tool is HOME). The **execution module** has three roles: an Analyst (GPT-4o) for interface analysis and static reasoning, a Navigator — any existing mobile agent, plugged in as-is; the paper tries M3A and UI-TARS-7B-SFT — and the Tool. After every subtask, its **return signal** (completion status, extracted information, execution logs) is written to a **process memory**, and the orchestrator recomputes the plan: π<sub>t+1</sub> = M(s<sub>t+1</sub>, g, P<sub>t+1</sub>). The design philosophy is context reduction: the executor sees one self-contained instruction per global step. Nothing is trained — the signal that steers the system is the return signal of each subtask.

## Results, as reported

Baseline agents: three agentic workflows on GPT-4o (M3A, Mobile-Agent-v2, Mobile-Agent-E) and two agent-as-a-model systems on Qwen2-VL-7B (OS-Atlas-7B-Pro, UI-TARS-7B-SFT, served with vLLM on one A100-SXM4-80GB). Backbone temperature is 0.0 and the input limit is 4096 tokens; UI-TARS keeps N = 5 previous screenshots.

Offline, on the 50 ANCHOR tasks (success rate %, with budget-exceeded % in parentheses):

| Agent                             | Success  | Budget exceeded |
|-----------------------------------|----------|-----------------|
| M3A                               | 50.0     | 16.0            |
| Mobile-Agent-v2                   | 30.0     | 34.0            |
| Mobile-Agent-E                    | 26.0     | 8.0             |
| OS-Atlas-7B-Pro                   | 2.0      | 72.0            |
| UI-TARS-7B-SFT                    | 6.0      | 84.0            |
| **AGENT-NEXUS w/ M3A**            | **74.0** | 10.0            |
| **AGENT-NEXUS w/ UI-TARS-7B-SFT** | **46.0** | 44.0            |

The abstract summarizes this as a 24% to 40% task success rate improvement for existing mobile agents on compositional tasks, without significantly sacrificing inference overhead. Efficiency (Table 3): AGENT-NEXUS w/ M3A costs 0.040 USD and 18.86 s per step against 0.037 USD and 14.77 s for M3A alone; AGENT-NEXUS w/ UI-TARS-7B-SFT costs 0.0063 USD and 6.53 s against 0.0025 USD and 4.35 s for UI-TARS alone.

Online, on the 30 service apps (success rate %, Table 4): English apps — M3A 32.0, Mobile-Agent-E 28.0, AGENT-NEXUS w/ UI-TARS-7B-SFT 28.0, Mobile-Agent-v2 12.0, UI-TARS-7B-SFT 8.0, OS-Atlas-7B-Pro 4.0; Chinese apps — AGENT-NEXUS w/ UI-TARS-7B-SFT 32.0, Mobile-Agent-E 24.0, Mobile-Agent-v2 12.0, UI-TARS-7B-SFT 8.0, M3A 4.0, OS-Atlas-7B-Pro 4.0. Note that on English online apps the wrapped UI-TARS configuration (28.0) sits below M3A (32.0); the scheduler’s win there is lifting the 7B executor, not beating the GPT-4o workflow. No agent exceeds 50% success on all subsets.

## What the paper’s own controls say

The central control is the **atomic-to-compositional gap analysis** (Table 5): on Simple Concatenation and Context Transition instructions from ANCHOR, each agent is run both with the full compositional instruction (“weak”) and with a manual decomposition into optimal atomic subtasks (“strong ceiling”). Manual decomposition is a major lift: M3A goes from 57.0 to 80.0 (↑87%) and UI-TARS-7B-SFT from 11.0 to 60.0 (↑452%) overall; Mobile-Agent-v2 from 34.0 to 46.0 (↑33%), Mobile-Agent-E from 31.0 to 46.0 (↑45%), OS-Atlas-7B-Pro from 3.0 to 6.0 (↑100%). Using the Weak-to-Strong-style Performance Gap Recovered (PGR) metric, AGENT-NEXUS w/ M3A reaches 77.0 overall with PGR 88.0 and AGENT-NEXUS w/ UI-TARS-7B-SFT 49.0 with PGR 76.0 — the scheduler captures most of what a human decomposer would give, without one. Baselines are reasonably matched: all three workflow baselines share the GPT-4o backbone, every agent faces the same step budget and the same app-launching convention, and the two model-based agents are quantified for cost and latency.

## Where the evidence is thinner, in the paper’s words

- No seeds or variance are reported; the tables read as single runs per agent per subset.
- The online judge is standard but unvalidated: “for online evaluation, we follow previous work to apply MLLM-as-a-Judge and human verification for accurate verification” — no check of the judge itself appears.
- Online interfaces drift: “experimental environments on applications such as RedNo and YouTube may slightly differ across time.”
- Android only: “our experiments are conducted solely on Android devices.”
- The execution module is simplified: “the only tool in HOME.”
- Task templates were expanded with GPT-4o and GPT-o1 then human-refined; a train/test app split for exploration versus evaluation is not reported (held-out apps unclear).

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**, architecture pattern **C17** (manager-worker hierarchy under agent-loop context control). The score reflects what the paper reports: interactive online evaluation, five mainstream baselines, cost and latency accounting, the atomic-versus-compositional control with PGR, and a released project page with demo, dataset and code. The judgment record also flags what is missing: no variance or seeds, held-out environments unclear, the judge untested, and budget matching only partial (the scheduler adds GPT-4o calls on top of the navigator). CUA Radar did not rerun anything; every number here comes from the paper (version v1).
