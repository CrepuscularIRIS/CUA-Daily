# Player-1: a computer-use model that learns game control from synthetic experience

*A CUA Radar reading of arXiv 2610.20584v1 (Ouyang, Wang, Hu, et al.). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.20584v1 · Code: https://github.com/TencentARC/Player-1*

## The problem: demonstrations cover few of the states an agent reaches

Computer-use agents read screens and press keys. Games are a harder test: they need precise aiming, sustained movement and several inputs at once, under fast-changing visuals. The paper argues that gameplay demonstrations “cover only a limited portion of the states an agent may encounter”, while scalable environments for interactive training are hard to obtain, and programmatic rewards for commercial games are difficult to write. Its central question is whether synthetic experience can improve game control beyond supervised initialization, and whether the gain carries over to games outside the RL training suite.

## What Player-1 is

**The agent.** At each turn the policy receives a task instruction, the current screenshot and a short history (two recent visual-action turns and two earlier action-only turns), and outputs reasoning plus an action. It is a screenshot-in, keyboard-and-mouse-out agent for games, evaluated in Minecraft, ViZDoom and browser games, and shown qualitatively in a commercial game. The base models are Qwen3.5-9B and Qwen3.5-35B-A3B. On the CUA Radar board the paper sits under pattern K13, “synthesise tasks from checkers/specs so verifiable reward exists by construction”.

**Extended action space.** Three additions to ordinary computer-use actions: relative pointer motion (normalized displacements for camera control when no pointer is visible), sustained inputs (a key or button held for one full control step), and composite actions (two or more compatible inputs executed concurrently in one step, such as holding W while tapping Space).

**Supervised initialization.** 6,044 curated gameplay trajectories (295,097 turns, 172 games, about 16.4 hours of sampled control) come from public datasets and in-house recordings. A VLM (Gemini 3.8 Flash) annotates each with a task instruction and per-turn visual reasoning. Minecraft is the largest single game, with 1,236 trajectories. Both sizes get two epochs of SFT with action-balanced sampling.

**Player-1-Gym.** Sixteen synthetic 2D and 3D environments, built on the authors’ own engines, grouped into five families by control demand: aiming (2), combat (5), driving (4), navigation (4) and UI interaction (1). Appearance, camera, scene and control response are randomized. Each environment defines a cumulative game score; the per-step score increment is the reward. The policy sees only screenshots and task text; the score is computed from privileged state, and no learned judge is used.

**RL.** Synchronous PPO with a 9B dense critic, 200 steps, 256 episodes per step spread equally over the 16 environments, at most 50 turns per episode. Because reward scales differ, advantages are normalized per environment. There is no explicit reward for composite actions.

## Results, as reported

Every evaluation below is an online game rollout; there is no offline step-accuracy benchmark in the paper. Metrics differ by benchmark, so they are kept in separate tables. Baselines keep their native preprocessing and inference procedures.

**MineDojo-300** (300 Minecraft tasks, 8 trials each; success rate %, with the paper’s 95% task-bootstrap intervals for the overall column):

| Method                       | Combat | Harvest | Overall \[95% CI\]         |
|------------------------------|--------|---------|----------------------------|
| GameWAM (strongest external) | 14.00  | 9.88    | 12.63 \[10.79, 14.54\]     |
| Qwen3.5-9B                   | 11.75  | 4.13    | 9.21 \[7.50, 11.00\]       |
| Player-1-9B-SFT              | 12.50  | 6.63    | 10.54 \[8.67, 12.50\]      |
| **Player-1-9B**              | 52.31  | 10.38   | **38.33** \[35.13, 41.58\] |
| Qwen3.5-35B-A3B              | 8.69   | 6.00    | 7.79 \[6.25, 9.46\]        |
| Player-1-35B-A3B-SFT         | 30.31  | 9.50    | 23.38 \[20.63, 26.21\]     |
| **Player-1-35B-A3B**         | 55.56  | 12.00   | **41.04** \[37.83, 44.29\] |

The paper states gains over SFT of 27.8 points for 9B and 17.7 points for 35B-A3B. Tasks solved in at least four of eight trials rise from 20 to 136 for 9B.

**ViZDoom-10** (ten maps, 50 trials per map, mean scaled return):

| Method | Precision shooting | Goal navigation | Mobile combat | Survival | Overall |
|----|----|----|----|----|----|
| GameWAM | 0.1175 | -0.1285 | 1.1860 | 0.1424 | 0.3938 |
| Player-1-9B-SFT | 0.4403 | 0.1839 | 0.5293 | 0.5423 | 0.4361 |
| Player-1-9B | 1.0772 | 0.5974 | 0.3033 | 0.7927 | 0.6922 |
| Player-1-35B-A3B | 1.0423 | 0.2628 | 0.5960 | 0.8979 | 0.7236 |

**GameWorld** (170 browser-game tasks, 34 games, 3 trials per task):

| Method           | Success (%) | Progress (%) |
|------------------|-------------|--------------|
| Qwen3.5-9B       | 10.39       | 29.22        |
| Player-1-9B-SFT  | 13.14       | 31.43        |
| Player-1-9B      | 15.88       | 34.45        |
| Qwen3.5-35B-A3B  | 13.14       | 33.49        |
| Player-1-35B-A3B | 17.25       | 38.79        |

The paper also shows Player-1-9B qualitatively in Watch Dogs 2, a commercial game unseen in SFT and RL (on-foot navigation, entering a car, driving), without a number.

## What the paper’s own controls say

**SFT versus RL.** The paper separates the stages in its tables: for 9B, SFT moves MineDojo-300 success from 9.21 to 10.54 and RL then to 38.33; for 35B-A3B, SFT alone gives 23.38 and RL 41.04.

**SFT initialization.** On Minecraft development tasks over 100 RL steps (9B), SFT then RL rises from 17.67% to 51.67%, while starting RL from the base model rises from 12.67% to 16.67%.

**Environment scaling.** With a fixed budget of 25,600 episodes over 100 RL steps, starting from the same SFT checkpoint and using 2, 4, 8 or 16 training environments, the paper’s Figure 7 shows Minecraft development-task success rising with the number of environments; the numeric labels are in the figure only, so they are not quoted here.

**Composite actions.** In in-suite validation the share of turns with composite actions rises from 64.7% at the start of RL to 85.4% after 50 steps and 93.2% after 100, with no explicit reward for it.

**Training curves.** Mean episode return and game score across the 16 environments rise over 200 steps, fastest early; the 35B-A3B curve ends slightly above the 9B curve.

## Where the evidence is thinner

- **Transfer is uneven.** On GameWorld the 9B model moves from 31.43 to 34.45 progress and from 13.14 to 15.88 success. On ViZDoom, 9B mobile combat is 0.3033 after RL against 0.5293 after SFT, and GameWAM scores 1.1860 on that category.
- **Minecraft is not unseen by SFT.** The RL suite has no Minecraft environment, but Minecraft is the largest single game in the SFT data (1,236 trajectories). The paper’s “outside the RL training suite” claim is about RL.
- **Intervals.** The 95% bootstrap intervals are given for MineDojo-300; the ViZDoom and GameWorld tables give single values.
- **Baseline handling.** External models run with their own preprocessing, resolutions and action adapters, at different sizes. The paper says it focuses on released game-control and computer-use policies rather than proprietary API models, citing the estimated cost of a full evaluation (up to 3.14 million decision turns per model).
- **Development tasks.** The ablation and scaling numbers use Minecraft development tasks; the paper does not spell out how they relate to the 300 final tasks.
- **Cost.** SFT uses 32 NVIDIA H200 GPUs for about 24 hours, and a 200-step RL run uses 64 H200 GPUs for about 36 hours.

## CUA Radar’s read

CUA Radar scores this paper **75 (three stars)**, evidence level **transfer**. The judgment record credits online evaluation, games outside the RL suite, confidence intervals on MineDojo-300, baselines that separate base, SFT and RL models, and a component ablation; budget matching and cost reporting are marked partial. It flags the anti-pattern AP2 (a synthetic environment standing in for the real target); the paper’s response is the three external benchmarks above. The radar did not rerun any experiment; every number here comes from the paper (version v1).
