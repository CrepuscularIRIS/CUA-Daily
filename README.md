# CUA-Daily

从论文中识别具体的研究方法和可信证据，积累可复用的领域 pattern，挑出少数值得深入阅读的工作。

核心问题：**改变了感知—规划—动作—反馈中的哪一环，在线任务是否真的完成，提升来自哪里？** 收录边界见 [EVIDENCE](docs/EVIDENCE.md)。

> 2026-10-22：现有评分、排名、选题与 Reel 已统一撤下。原文和已归纳领域卡保留；当前没有新版有效榜单或 Reel。此次维护未启动重评分，详情见 [重置核查](docs/RESET_2026-10-22.md)。

## 使用流程

Grok 收集候选 → 6.1 Sol 按已有领域 pattern 批量评分 → 少量候选 → Opus 5.5 核对原文并制作 Reel。

| 内容 | 入口 |
|---|---|
| 领域模式卡 | [patterns/overview](patterns/overview.md)；评分依据是这些卡的机制、条件、失败模式和审稿期望 |
| 新版评分 | [规则](research/scoring/SCORE_SPEC.md) · [本领域配置](research/scoring/PROFILE.md) |
| CC 执行 | [启动提示词](docs/agents/START_CC.md) · [完整批量提示词](research/scoring/SOL_BATCH_PROMPT.md) |
| 精选 Reel | [选题](research/scoring/SELECTION.md) · [Opus 制作](research/scoring/OPUS_REEL_PROMPT.md) · [成品入口](reel/README.md) |
| 候选收集 | [Grok 提示词](docs/agents/GROK_PROMPT.md) · [inbox](inbox/README.md) |

默认 CC 内置 4 个评分 Subagent 并行，model type 使用已配置的 6.1 Sol，每批通常 10–20 篇，完成一批立即补派；不另起无头 Claude。Opus 只负责少量候选核对与 Reel。

评分顺序是论文操作 → 相关领域卡 → 适用判据 → 论文证据 → 得分。G/M/X/E 只汇总这些判断。原 ResearchStudio 15＋31 保留为方法来源，不是逐篇评分 taxonomy；匹配卡数、录用率、代码链接和名气不加分。

初步材料足够即可简评，缺材料不冒充低分。通常每期不到 10 篇 Reel；先核对、后制作，不把全部论文做成海报墙。

维护说明：[PIPELINE](docs/PIPELINE.md) · [MAINTAINING](docs/MAINTAINING.md)。`make check` 只验证本地结构，不代表科学结论正确。

## Credits and license

MIT（见 [LICENSE](LICENSE)）。
- **Base pipeline** 经 [HarnessRSI Daily](https://github.com/CrepuscularIRIS/HarnessRSI-Daily)，源自
  [yang3kc/daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest)（MIT）。
- **Pattern cards**：方法卡来自 ResearchStudio Idea 原 15+31（保留原 LICENSE）；领域卡借助 Open Scientist（gui domain）归纳。
