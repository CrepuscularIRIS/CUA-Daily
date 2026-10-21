# OS-Symphony: an orchestrator that keeps milestone screenshots and searches the web visually

*A CUA Radar reading of arXiv 2601.07779v1 (Yang, Jin, Wu, Liu, Sun, et al.). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2601.07779v1 · Code: https://github.com/OS-Copilot/OS-Symphony*

## The problem

Computer-using agents built on Vision-Language Models degrade in two situations. First, long-horizon tasks: memory modules exist, but the paper argues they lack “granular control over historical visual information curation and pruning”, so screenshots are either kept redundantly or lost, and errors such as intent drift and cyclic behavior go unnoticed. Second, novel software: retrieval-augmented approaches are either text-only — losing the visual semantics of screenshot-heavy tutorials — or built on local knowledge bases that “incur high maintenance costs and struggle to adapt to new software”. OS-Symphony targets both with a milestone-driven memory and a browsing, vision-in-the-loop searcher.

## What OS-Symphony is

The agent is a desktop CUA. It perceives screenshots (up to 8 images of 1920x1080 in context) and acts through a concise cross-platform action space mapped to PyAutoGUI primitives: click, type, scroll, drag_and_drop, hotkey, open, wait, done, fail, plus two proprietary calls, call_search_agent and call_code_agent. Platforms are Ubuntu (OSWorld), Windows (WindowsAgentArena) and macOS (MacOSArena). On the CUA Radar board its architecture pattern is C18, “verify each action’s outcome from before/after observations and feed the verdict back”, under the main pattern of structuring the prompted agent loop.

A single VLM (GPT-5, GPT-5-Mini, or Qwen3-VL 8B/32B Instruct/Thinking variants) drives four roles at temperature 0.1:

1.  **Orchestrator.** The decision core: it reads the instruction, the current screenshot, the last-K turns of short-term memory, the latest reflection, and any retrieved tutorial, and emits one thought and one action per step.
2.  **Reflection-Memory Agent (RMA).** An auxiliary VLM summarizes each completed action from pre/post screenshots and judges whether it worked. It keeps milestone screenshots plus abstract summaries in a long-term memory, and returns a structured reflection: On-track, Completed, Infeasible, or Off-track with one of four error types (GUI Error, Lack of Tutorial, Code Error, Other Error). A rule-based loop detector (perceptual hashing with Hamming distance ≤ 1, then SSIM at 0.99, window 3) supplies the Lack-of-Tutorial hint.
3.  **Multimodal Searcher.** On demand, it opens an isolated browser sandbox on the search-results page and browses with only click, type and scroll, cross-checking several pages before distilling a step-by-step tutorial, or returning fail. The unimodal ablation replaces it with SearXNG search plus Crawl4AI parsing.
4.  **Coder and Grounders.** The Coder edits files via shell/Python and is verified through GUI state checks; grounding uses UI-TARS-1.5-7B as the general grounder and an EasyOCR-based word-level grounder for text-dense apps.

There is no training: the framework is prompted, and the signals that steer it are the auxiliary VLM’s step verdicts, the rule-based loop detector, and the searcher’s tutorials.

## Results, as reported

All numbers are online success rates (%) on execution-checked desktop benchmarks. The paper reports no offline step-accuracy or grounding-accuracy numbers. The paper does not state seed counts or variance for the main tables; the board’s one-line summary records single runs. OSWorld here means OSWorld-Verified with 8 Google Drive tasks excluded (361 tasks).

| Method (steps) | OSWorld | WindowsAgentArena (154) | MacOSArena (63) |
|----|----|----|----|
| Qwen3-VL-32B-Instruct (50) | 32.40 | 31.7 | 7.94 |
| UI-TARS-2 (100) | 53.10 | 50.6 | not reported |
| Agent S3 w/ GPT-5 (100) | 62.63 | 56.6 | not reported |
| Agent S3 w/ GPT-5-Mini (50, reproduced) | 47.58 | not reported | not reported |
| OS-Symphony w/ Qwen3-VL-32B-Instruct (50) | 46.86 | 45.3 | 19.05 |
| OS-Symphony w/ GPT-5-Mini (50) | 58.05 | 62.2 | 46.03 |
| OS-Symphony w/ GPT-5 (50 / 100) | 63.61 / 65.84 | 63.5 | not run (cost) |

The paper states gains of ↑2.4% on OSWorld (65.8%), ↑6.9% on WindowsAgentArena (63.5%) and ↑38.0% on MacOSArena (46.0%) over prior bests, and says the GPT-5 100-step OSWorld score surpasses the primary baseline, 100-step Agent S3 w/ GPT-5, by about 3%. On WindowsAgentArena it reports beating the 50-step and 100-step Agent S3 baselines by 9.4% and 6.9%, with the GPT-5-Mini variant exceeding the 100-step Agent S3 (GPT-5) by 5.6%. Against its own reproduced Agent S3 runs, the framework gains 8% with Qwen3-VL-32B-Instruct and 10% with GPT-5-Mini.

## What the paper’s own controls say

**Ablation (OSWorld, GPT-5-Mini + UI-TARS-1.5-7B, 50 steps).** Removing both search and reflection scores 51.90 on average; adding unimodal search 54.81; multimodal search 58.05, a 22.1% relative gain over no search and 10.3% over unimodal in the Daily domain. For reflection: no reflection 54.38, reflection with short-term memory 54.01, the full RMA 58.05 — about 20.0% and 20.7% relative gains in the Workflow domain. Notably, naive last-K reflection falls below no reflection at all, while using ~36.5% fewer tokens. Ablating the RMA costs 3.3 extra steps per task. Removing the Coder drops OSWorld from 63.61 to 57.42 (~6.2%).

**Cost and scale.** On the Workflow domain, Claude-Sonnet-4.5 scores 57.21 at about \$500, GPT-5 54.86 at about \$150, and GPT-5-Mini 47.37 at about \$30; GPT-5-Mini “trails GPT-5 by only 5% on average while reducing costs by ~80%”. Swapping grounders barely moves the average (UI-TARS-1.5-7B 46.86, GTA1-32B 46.32, ScaleCUA-32B 45.76, Holo2-30B-A3B 43.92). A cap of 8 history images is the reported optimum (46.86).

**Reflection audit.** Of 100 steps the RMA flagged as GUI Error, human experts found about 90 real errors and about 10 hallucinations. In the message-protocol statistics, 75.0% of steps were judged normal; the Searcher was called only 35 times (0.6% of actions), and manual checks found 85% of those tutorials useful.

**Test-time scaling.** With temperature raised 0.1 per pass, Pass@2 reaches 74.14%, above the 72.4% human baseline, and Pass@5 79.40%.

## Where the evidence is thinner, in the paper’s words

- **Volatility.** “Despite strict control over prompts and temperature, we observe significant task-level volatility.” No seeds or confidence intervals are reported for the main tables.
- **Perceptual blindness.** Current VLMs “often fail to resolve fine-grained cues like highlighting or overlapping windows. This perceptual blindness leads the RMA to issue false positive errors, paradoxically allowing the w/o RMA baseline to outperform the full framework in visually complex domains.”
- **No held-out split.** All three benchmarks are standard public suites; none is held out from any exploration or tuning the paper describes, and the paper does not claim one.
- **Overhead.** The multi-agent system is heavy: the RMA and Orchestrator average about 270k tokens per task (96% prompt, 4% completion), and “our execution speed is tens of times slower than human performance”.
- **Desktop only.** “The framework’s adaptability to mobile platforms, such as Android and iOS, remains unverified.”

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**. The score reflects what the paper reports: execution-checked online evaluation on three desktop benchmarks, reproduced Agent S3 baselines under matched models, dollar cost, and component ablations with a step/token accounting. The judgment record also flags what is missing: no held-out environment, seeds/variance not reported (single runs), the RMA’s verdicts not validated against ground truth beyond the 100-step audit, and the code link unverified at review time. The radar did not rerun any experiment; every number here comes from the paper (version v1).
