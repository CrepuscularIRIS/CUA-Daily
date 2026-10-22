# SOURCE · 2504.01382

- 论文：An Illusion of Progress? Assessing the Current State of Web Agents（Tianci Xue, Weijian Qi, Tianneng Shi, Chan Hee Song, Boyu Gou, Dawn Song, Huan Sun, Yu Su；OSU / UC Berkeley）
- 版本：2504.01382v4（2025-10-08，COLM 2025），https://arxiv.org/abs/2504.01382v4
- 原文材料：`/tmp/2504.01382.html`（arxiv.org/html/2504.01382v4，sha256 前缀 4c9420ddbe81e704，含附录，未提交）；`research/fulltext/2504.01382.txt`（裁剪版，sha256 前缀 b6eedb6cec8db4c4）。数字以 HTML 为准。
- 初筛记录：`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`（G4/M4/X3/E4，screen 95，online）
- 核对记录：`research/v3/runs/gui-v3-20261022-01/verify/2504.01382.md`（verify_ok；47% 定位为 §2.2）
- 仅阅读原文，未运行代码，不构成复现。

## 数字与断言映射

| 画报位置 | 内容 | 原文出处 |
|---|---|---|
| 副标题 / 曲线红线 | WebVoyager 上报告"接近 90%"（OpenAI 2025；Müller & Žunič 2024） | §1 第 2 段（作者转述，非本文测量） |
| 问题栏 / 失效带 | 随机 650 个原 Mind2Web 任务，47% 无效或参考轨迹过时 | §2.2 |
| 问题栏 / 橙线左端 / 对照卡 | 朴素搜索 agent（Google 查询→点开链接查答案）在按网站分层抽样的 100 个 WebVoyager 任务上 51%，人工评 | §2.1；图 2 |
| 橙线右端 / 分层 / 对照卡 | 新集抽 100 任务（易/中/难 33/34/33）成功 22%，易/中/难约 50%/18%/3% | §2.2；图 2 |
| 横轴节点 | Mind2Web（Deng et al., 2023，众包并验证）；WebVoyager（He et al., 2024a，以 Mind2Web 改写任务为种子 + LM 合成，15 网站） | §2.1；§2.2 |
| 新基准区 / 关键动作 | 300 任务、136 网站；167 原任务 + 24 改写 + 34 Mind2Web-Live + 75 新建；过滤歧义/失效/CAPTCHA；难度 ≤5/6–10/≥11 步，83/143/74 | §2.2 |
| 新基准区 | 起始 URL + 提示禁用 Google 搜索 | §4.1；附录 B.2 |
| 黑点 / 六 agent 卡 | 人工评 SR：Operator 61.3、Claude CU 3.7 56.3、SeeAct 30.7、Browser Use 30.0、Claude CU 3.5 29.0、Agent-E 28.0 | 表 2 |
| 六 agent 卡 | 每任务 ≥2 名标注者，第三人仲裁 | §4.1 |
| 六 agent 卡 | 易→中平均降 31.6%、中→难再降 15.4%；CU 3.7 / Operator 易任务 90.4 / 83.1 | §4.2（图 4 描述，按原文"%"口径照录） |
| 核验环 | 三步：关键点识别；逐帧摘要 + 相关度 1–5，≥δ 保留；任务+关键点+关键截图+动作序列判定；不依赖最终回答 | §3；附录 E（δ=3） |
| 核验环中心 / 表 | WebJudge o4-mini 平均 AR 85.7、SR 差 3.8；GPT-4o 83.6 / 7.8；WebJudge-7B 87.0 / 3.9 | 表 2；§4.2 |
| 核验环表 | Autonomous Eval（只看末帧）GPT-4o 平均 AR 79.4；WebVoyager 判分（全部截图）73.9 | 表 3；§4.3 |
| 核验环注 | GPT-4o 版跑 3 次，六 agent SR 平均 std 1.1%，最大 1.8% | §4.2；图 B.1 |
| 核验环注 | AgentRewardBench 1,302 轨迹；o4-mini 版 precision 82.0；SR 平均差 10.5，偏保守 | §4.4；表 4/5 |
| 限制卡 | 开源 agent 最多 25 步；Claude CU 3.7 最多 50 步、关闭 thinking；Operator 经网页界面收集；整页 vs 可视区截图 | 附录 E |
| 限制卡 | "约 14% 不一致" = 100 − 85.7（派生） | 表 2 |
| 阅读判断 | Browser Use 允许搜索 31% / 禁止 26%，与表 2 的 30.0 口径不同 | 附录 B.2；表 2 |

## 示意与原创图形

- "任务年代 × 成功率失效曲线"为自绘示意：横轴只有三个来源节点（2023 Mind2Web、2024 WebVoyager、2025 Online-Mind2Web），非等距，中间无逐年数据；失效带的起点（创建时经验证）与曲面形状为示意，只有 47% 为论文数字；红色虚线箭头只表示"同名 agent 换任务集 + 人工评"，不是受控对照。
- 调度要求的横轴 2007→2024 在原文中无对应数据，未采用（见 QA.md）。
- 核验环为自绘机制示意，未使用、未仿制论文图 1–5。

## 作者结果 vs 阅读判断

- 作者结果：上表全部数字与标题主张（报告值被抬高、新基准上 SR 回落、WebJudge 一致率最高）。
- 我们的阅读判断（画报黄框，单独标注）：头条落差是多因素合并；47% 来自原 Mind2Web 抽样、是两类合计；B.2 与表 2 口径不同；o4-mini 版偏保守。来源：核对记录"我们的阅读判断"节。
