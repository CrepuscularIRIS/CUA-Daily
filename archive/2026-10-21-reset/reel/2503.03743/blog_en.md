# CHOP: a mobile assistant whose planner may only pick from ten human basis subtasks

*A CUA Radar reading of arXiv 2503.03743v1 (Zhou, Wang, Dai, Jia, Du, Dong, Xu; Renmin University of China and Huawei Noah’s Ark Lab). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2503.03743v1 · Code: https://github.com/Yuqi-Zhou/CHOP*

## The problem: subtasks a VLM invents on its own

Mobile operating assistants built on vision-language models (VLMs) are usually hierarchical: a task (“Play Bob’s songs”) is decomposed into subtasks (“Search Bob”), which are executed as low-level actions (click, type). The paper argues the middle level is the weak one, and names two failure modes. *Ineffective subtasks*: the planner proposes something the action agent cannot execute — for “Ask Bob to attend the meeting” it may emit “Go to Bob’s office”, where “Send Bob an email” is feasible. *Inefficient subtasks*: steps that do not advance the task, such as “Wait for Bob’s feedback”. Both stem, in the authors’ words, from “the VLM’s lack of experience in decomposing subtasks within GUI scenarios in multi-agent frameworks”.

## What CHOP is

**Agent.** CHOP runs on real Android devices and is image-only: the state at step t is the current screenshot alone, with no XML or view hierarchy. The action space has six action types — CLICK (screen coordinates), SCROLL, TYPE, BACK, EXIT, WAIT — and the policy is a<sub>t</sub> = f(s<sub>t</sub>, H<sub>t</sub>) over the screenshot and accumulated history. Three modules cooperate: a **plan agent** that decomposes the instruction, an **action agent** that emits actions with observation / thought / summary narration, and the **Aria-UI** grounding model that maps symbolics like CLICK(Search Bar) to coordinates such as CLICK(200, 300). Platform: mobile (Android), evaluated in both English and Chinese app contexts.

**Board pattern.** On the CUA Radar board this is pattern C17, “decompose into a manager that plans subgoals and workers that execute them” (main pattern: agent loop context control). CHOP is a clean instance: plan agent = manager, action agent + grounding = worker, with a summary memory handed forward between subtasks.

**Mechanism.** The core idea is the *basis subtask*, by analogy with basis vectors: any task should decompose into a combination of high-frequency subtasks that humans actually perform. The basis set is mined offline from the AITZ dataset (a subset of AITW covering four apps) in four steps: verb extraction with spaCy part-of-speech tagging, synonym clustering via WordNet synsets, summarization where GPT-4 turns each cluster’s action sequences into a standardized process with boundary conditions, and frequency filtering that keeps the top 10 subtasks (Search Item, Send Text Message, Open Section, View Content, Interact, Manage Collections, Share Content, Check Notifications, Modify Settings, Create or Edit Entry). At run time the plan agent must choose each subtask from this set, generating purpose and stopping condition per subtask; if something necessary is missing, a placeholder lets the model define a custom subtask. Each basis subtask ships with documentation, which lets the action agent emit the whole action sequence for fixed-flow subtasks (like search) in a single forward pass.

**Training signal.** None — no fine-tuning anywhere. All steering is in the prompt: the constrained subtask vocabulary and the documentation. GPT-4o drives both agents; Aria-UI, spaCy, WordNet and one GPT-4 summarization pass are used as fixed tools.

## Results, as reported

All numbers are online evaluation on real devices: the agent operates a phone, and human-executed trajectories are the ground truth. Every method, including baselines, uses GPT-4o (size not stated), temperature 0.0, max output 4096; a task counts as a success only within 20 actions. Test sets: CHOP-En, 30 English instructions over 10 apps (easy / medium / hard), and CHOP-ZH, 200 Chinese instructions over 10 apps built by 10 annotators, of which 30 (3 per app) were run because of GPT-4o cost. Seeds / variance: not reported. Success rate (SR):

| SR               | En easy  | En med   | En hard  | ZH easy  | ZH med   | ZH hard |
|------------------|----------|----------|----------|----------|----------|---------|
| AppAgent         | 0.50     | 0.40     | 0.10     | 0.40     | 0.30     | 0.20    |
| Mobile Agent(v2) | 0.50     | 0.50     | 0.40     | 0.80     | 0.20     | 0.30    |
| Moba             | 0.50     | 0.30     | 0.20     | 0.40     | 0.30     | 0.10    |
| **CHOP**         | **0.80** | **0.70** | **0.60** | **1.00** | **0.80** | 0.10    |

On efficiency, the paper’s new metrics favor CHOP: Average API Cost (AAC, lower is better) is 0.76 / 0.85 / 0.93 on English easy / medium / hard against 3.62 / 3.65 / 4.42 for Mobile Agent(v2), and Mapping Efficiency (ME) exceeds 1 (1.36 / 1.20 / 1.10 English) because fixed-flow subtasks generate multiple actions per call. Completion Rate (CR) on English is 0.90 / 0.89 / 0.59 for CHOP. There are no offline step-accuracy benchmarks in the paper; everything above is online.

## What the paper’s own controls say

**Ablation (CHOP-ZH, Table 3).** Removing documentation drops SR from 0.67 to 0.47 over all 10 apps; removing the basis subtask and documentation drops it to 0.33. On the 6 out-of-domain apps (the basis was mined from AITZ’s four app types) the fall is 0.61 to 0.44 and then 0.22 — the paper’s evidence that the basis subtask generalizes rather than memorizes. In-domain SR goes 0.75 to 0.50.

**Subtask quality.** Against annotator plans, CHOP’s subtasks score higher on BLEU, ROUGE-L and an LLM-as-evaluator comparison than the same planner without the basis constraint (Figure 3; the paper gives these values only as figure labels).

**Error analysis (Table 4).** CHOP shows 0.0% hallucinations, 0.0% parse errors and 0.0% max-iteration failures, where AppAgent’s failures are 57.1% XML/output parse errors and Moba’s are 63.6% task-context misinterpretation. CHOP’s largest error category is poor graphical recognition at 54.6%.

**Honest negative.** Mobile Agent(v2) beats CHOP on the hard Chinese split (SR 0.30 vs 0.10), which the paper attributes to CHOP’s English documentation.

## Where the evidence is thinner, in the paper’s words

- Scale and scoring: “the current evaluation process relies on manual assessments, which results in a relatively small dataset” — 30 + 30 executed instructions, no seeds or variance reported.
- The LLM subtask evaluator is not validated against anything external.
- Moba “requiring additional tools to open the app, which are not available in our dataset”, the authors used Aria-UI for app launching for it.
- Only the plan/action interface is studied; “challenges between the action agent and the grounding model” are left to future work.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **transfer**. The score reflects what the paper reports: online evaluation on real devices, an in-domain / out-of-domain app split, GPT-4o for all baselines, a 20-action success budget, API-cost reporting, a component ablation, and released code and dataset. The judgment record flags as not reported: variance, and validation of the LLM judge; it also notes the loop simply runs “until the action is EXIT or the maximum number of rounds is reached”. The radar did not rerun any experiment; every number here comes from the paper (version v1).
