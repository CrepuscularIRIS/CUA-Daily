# ANIS: synthesizing agent-friendly command interfaces for desktop applications

*A CUA Radar reading of arXiv 2610.15765v1 (Wu, Tao, Guo). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.15765v1 · Code: https://github.com/co-evolve-lab/ANIS*

*A note on scope: the agents here do not read screenshots. They drive desktop applications through programmatic interfaces (the application’s SDK, or generated shell-style commands), so this is a result about interface design rather than about GUI perception.*

## The problem: interfaces built for humans, used by agents

Desktop applications expose their functionality through GUIs, which assume a person can see and locate controls, and SDKs, which assume a developer can read documentation, learn an object model and debug low-level calls. An agent has to do that work itself, and most applications have no general command-line interface (CLI) either. The paper asks what makes an interface good for agents, and uses software evolution as a natural experiment: across releases an application’s functionality stays largely the same while its interface changes, so holding the task, agent and verifier fixed and varying only the installed release attributes differences to interface changes.

## What the paper does

**DeskIF-Bench** has 255 tasks across six applications (Writer, Impress, Inkscape, Blender, QGIS, FreeCAD) in five domains. Of these, 102 are reused from OSWorld and OpenComputer and 153 are synthesized by an authoring agent that has skills or privileged libraries the solving agent lacks. Every task has a deterministic script verifier that inspects the saved artifact, checked by confirming that it accepts a reference artifact and rejects task-relevant perturbations. Two backbones, Claude Haiku 4.5 and DeepSeek V4 Flash, run in the OpenCode scaffold on four releases of each application, with success measured as pass@3 (a task counts if any of three independent attempts passes).

**Cross-version result.** The newest release beats the oldest in all 12 model–application series. QGIS rises from 41% to 69% for DeepSeek and from 33% to 65% for Haiku; Impress rises from 40% to 58% and from 33% to 52%. Trajectory analysis points to three interface properties. **Discoverability**: operations that can be found at runtime and are clearly described (QGIS runtime descriptions grow by 20% per function between releases). **Granularity**: operations that match user goals, so fewer low-level calls are needed (for Haiku, mean QGIS operations per task fall from 30.4 to 21.2). **Observability**: being able to read back the state you wrote, which the paper finds limited in every release (581 trajectories reported completion while the saved artifact failed verification).

**ANIS (Agent-Native Interface Synthesizer)** turns those properties into a build-time and a run-time step, with no change to the application:

- **Atomic commands.** ANIS discovers capabilities inside the running application (registered operations, object introspection, menus), has an LLM build an invocation for each, executes it, and keeps only commands whose effect persists after saving and reopening the artifact. Commands are grouped by artifact object, and each writable property gets a paired read command when an accessor exists.
- **Goal-level commands.** From agent trajectories, ANIS finds command subsequences that recur in at least three requests, checks that they realize a shared artifact-level subgoal, and releases them as named commands only after a replay on a clean copy of the source artifact reproduces the saved state.

Both ANIS and the CLI-Anything baseline interfaces were generated with Claude Code using Claude Opus 4.8. On the CUA Radar board the paper sits in pattern K29, planner and grounder interface.

## Results, as reported

The expanded benchmark adds 76 Calc and 37 GIMP tasks (368 tasks, eight applications); Calc and GIMP were held out from method development. Overall success (%) and online tokens per task:

| Interface | DeepSeek V4 Flash | Tokens | Claude Haiku 4.5 | Tokens |
|----|----|----|----|----|
| Native SDK | 68.5 | 84.4K | 61.4 | 85.0K |
| CLI-Anything | 17.4 | 67.0K | 15.8 | 67.0K |
| ANIS, atomic commands | 72.3 | 22.6K | 64.9 | 23.0K |
| ANIS, with goal-level commands | 74.5 | 21.2K | 67.4 | 22.0K |

The paper reports token reductions of 73.2% and 74.9% against the native SDK with DeepSeek. Per application with DeepSeek, ANIS is above the native SDK on QGIS (77.8 and 81.5 against 68.5), Writer (89.3 against 76.8), GIMP, Calc, Impress and Inkscape, but below it on Blender (45.7 and 51.4 against 54.3) and FreeCAD (77.4 against 96.8).

## What the paper’s own controls say

**Why CLI-Anything is so low.** ANIS exposes over 20 times as many commands, and 98.7% of CLI-Anything’s failed tasks are attributed to missing commands. For ANIS’s own FreeCAD gap, 28.6% of failures lack a required command; the paper explains that FreeCAD and Blender operations depend on implicit object relationships that are harder to validate automatically.

**Observation commands.** With DeepSeek, prohibiting observation (read) commands by instruction lowers overall success from 72.3 to 60.3, a 12.0-point drop; Calc falls from 63.2 to 32.9 and Writer from 89.3 to 69.6, while GIMP, Impress and Inkscape do not change. An audit of the trajectories found no prohibited command used.

**Goal-level commands.** Ten commands were synthesized across the eight applications; they raise success by 5.7 points on Blender, 5.2 on Calc and 3.7 on QGIS and leave the other five unchanged. On a separate 7:3 split (258 training tasks, 110 held-out), 7 commands synthesized from training trajectories raise held-out successes from 64 to 67 of 110 (58.2% to 60.9%).

**Documentation.** Giving the native-SDK agents offline official documentation changes overall success by +1.4 for Kimi K2.5 and by -1.1, -1.7 and -1.9 for Haiku, DeepSeek and Claude Opus 4.6, so the paper reports no consistent gain.

## Where the evidence is thinner

- The paper reports single success rates per setting: no variance, and pass@3 is a generous criterion that rewards any of three attempts.
- Token figures count online usage by the task agent. Generating an interface took 17.1 to 36.4 hours per application with a coding agent, and that cost is not in the token comparison.
- The main goal-level result uses commands mined from the same task pool it is evaluated on; the CUA Radar record flags this overlap (anti-pattern AP5), and the held-out split shows a smaller gain (3 of 110 tasks).
- The observation ablation was run on one backbone, by instruction rather than by removing the commands.
- ANIS is below the native SDK on Blender and FreeCAD.
- Tasks, verifiers and interfaces were built with LLM assistance, which the paper acknowledges in its AI use statement.

## CUA Radar’s read

CUA Radar scores this paper **66 (★★)**, evidence level **online**. The record credits artifact-verified evaluation on live applications, two backbones, two baseline interfaces, an observation ablation, validated verifiers and released code. It flags overlap between the data used to build goal-level commands and the evaluation (AP5), records held-out evaluation and budget matching as partial, and variance as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v1).
