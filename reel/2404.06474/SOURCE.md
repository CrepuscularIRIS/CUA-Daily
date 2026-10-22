# SOURCE · 2404.06474 Autonomous Evaluation and Refinement of Digital Agents

- 版本：arXiv 2404.06474v3。正文 §1、§3–§5 用本地缓存 `research/fulltext/2404.06474.txt`（v3 HTML，sha256 `4363815423b5…`）。缓存缺 §2、脚注、图表数值和附录，这些由 `https://arxiv.org/html/2404.06474v3` 补读，包括 Fig.2/3/4 的 SVG（`android_compare.svg`、`reflexion_result_all.svg`、`eval_confusion.svg`）和 App. A.1–A.7。补读文件存 /tmp，不提交。
- 初筛记录：run `gui-pc11-20261022-01`。L1 见 `batches/p005.jsonl`，L2 见 `batches/l03.jsonl`（P3 / capability / F2,F4 / confirmed / to_l3）；入选理由见 `selection.md` 第 1 节第 5 行。
- 制作：Opus 5.5，2026-10-22。没有运行论文代码，也没有复现实验。

## 数字与断言 → 原文

| 画报内容 | 原文位置 |
|---|---|
| 问题：没有手写评估函数、没有额外示范时，自动评估并改进代理 | Abstract；§1 |
| 输入为指令 + 动作 + 末帧，iOS 用整条轨迹逐步打分；先输出推理再给判定 | §3、§3.1；§4「Evaluation Models」 |
| 两种实现：GPT-4V 端到端；微调 QwenVL-chat 描述截图（1,263 张，EasyOCR 辅助）→ Mixtral / GPT-4 推理；QwenVL 端到端作基线 | §3.1–3.2；App. A.2，Table 3 |
| 执行判定 = WebArena 内置手写测试用例（论文称 oracle evaluator） | §4「Environments」 |
| 人工判定 = AitW 120 个测试任务上的人工成功判定；作者自建 Android 模拟器 | §4「Environments」；App. A.4 |
| 一致率 WebArena 80.6 / 68.0 / 74.4 / 82.1，Android 90.6 / 70.2 / 92.9 / 89.8 | Table 1 |
| 混淆计数 WebArena（TP/FN/TN/FP）：GPT-4V 75/19/574/137，C+GPT-4 60/34/601/110，C+Mixtral 72/22/527/184；Android：76/25/359/20、67/34/364/15、79/22/367/12 | Fig.4（App. A.3、A.4） |
| WebArena 共 805 条（混淆计数合计），Android 共 480 条（120 任务 × 4 策略） | Fig.4；§4.1 |
| Kendall：评估器与人工 100%，动作匹配 66.7% | §4.1「Android-in-the-Wild」 |
| 约 36% 人类示范实际失败；AutoUI-large 动作匹配分 70.0 > base 67.5，按人工判定的成功率是 0.8 < 5.0 | §4.1；Fig.2 |
| iOS 逐步判定：人工同意 43/50 | §4.2「Filtered Behavior Cloning」 |
| Reflexion：基线 15.6；3 轮后执行检查 25.9，GPT-4V 20.2，C+GPT-4 19.0，C+Mixtral 18.1；中间轮次数值见折线 | Fig.3（数值读自 SVG 标注，画报为重绘） |
| 相对提升 +29%（GPT-4V）、+16%（C+Mixtral）；执行检查作为上界 | §4.2「Reflexion on WebArena」；Fig.3 图注 |
| 评估用 WebArena 发布的 GPT4-0613 + CoT-v2 轨迹；Reflexion 用 GPT-4-preview-1106 actor，成功率由执行检查判定 | App. A.3、A.5 |
| 假阴性的危害大于假阳性：FN 迫使重试成功的执行，几乎总会转为失败；FP 只是错过重试机会。作者称这是初步研究 | §4.2 |
| Android 过滤 BC：AutoUI-base，560 个训练任务，96 个测试任务；成功数 15 → 18.9±1.0 → 26.0±0.8（3 次训练），相对 +73% | §4.2；Table 2(b) |
| iOS 过滤 BC：CogAgent，80 个训练任务（737 条轨迹），52 个测试任务；成功数 8 → 11 → 14，相对 +75%；只用 C+Mixtral | §4.2；Table 2(a)；App. A.6 |
| 过滤阈值：保留逐步奖励 ≥ p 的状态-动作对；自训练 = 不过滤直接微调 | §4.2 |
| 误判归因：信息丢失 10%（模块化）/ 截图理解 5%（GPT-4V）；推理错误 50% / 70%；任务歧义 30% / 10%；判对的样本中约 10% 理由错误 | §4.3 |
| 评估器不完美；未利用语言解释 | Limitations |

## 我们据原文计算（画报标“计算”或蓝字）

- 精确率 = TP/(TP+FP)：WebArena 35.4 / 35.3 / 28.1%，Android 79.2 / 81.7 / 86.8%。数据来自 Fig.4。
- 基率与“全判失败”一致率：WebArena 94/805 = 11.7%，全判失败 711/805 = 88.3%；Android 101/480 = 21.0%，全判失败 379/480 = 79.0%。
- 占上界提升的比例：(评估器第 3 轮 − 15.6)/(25.9 − 15.6) 在 24%（C+Mixtral）到 45%（GPT-4V）之间。
- 成功数折成百分比：Android 15/96 = 15.6%，26/96 = 27.1%；iOS 8/52 = 15.4%，14/52 = 26.9%。
- “判为成功的轨迹约 2/3 实际失败”= 1 − 精确率，WebArena 三个评估器为 65–72%。

## 示意内容（不是论文实验图）

- 三个判定源节点的图标、校准链连线和下游闭环小环都是自绘示意。闭环只画信号流向，并不代表论文实际跑了多轮“训练—再评估”循环。
- Reflexion 折线用 Fig.3 的数值重绘，没有新增数据点。
- 过滤 BC 的条形按成功任务数等比例绘制。Android 和 iOS 的分母不同（96 / 52），画报已分别注明。
