# SOURCE · 2610.26469 VeriCUA

- 论文:VeriCUA: Learning Proactive Verification for Reliable GUI Agent Rewards(Wang, Lu et al.)
- 版本:arXiv 2610.26469v1(2026-10-19)
- 原文来源:`https://arxiv.org/html/2610.26469v1` 抓取件 `/tmp/2610.26469.html`(完整正文 + 附录 A–I,本地私有缓存,不提交);辅以 `research/fulltext/2610.26469.txt`(core 裁剪)
- 初筛记录:`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`(2610.26469 行;claim_type=component_training,G/M/X/E=4/4/4/4,evidence_level=transfer)
- 核对记录:`research/v3/runs/gui-v3-20261022-01/verify/2610.26469.md`(verify_ok,附展示收窄条件;画报按其收窄)
- 仅阅读原文,未运行代码,不构成复现。

## 数字与断言映射

| 画报位置 | 内容 | 原文出处 |
|---|---|---|
| ① 问题 | 被动奖励只能核实观察中暴露的内容;隐藏状态(如保存的文件内容)看不到 | §1 第 1 段 |
| ① 问题 | 提示式 Judge 4B→GPT-5.4 宏平均 68.13–69.62%,few-shot 至多 1.02 点 | §3.2;表1 |
| ① 截图卡注 | Done/Success/saved 等动作标签本身不算证据 | 附录 I.1 Judge 提示词第 4 条 |
| ① 截图卡(示意) | 每页备注、Presenter Console 两个例子 | 图1(b)、图6 / §3.3 的任务例子;卡片为自绘 |
| ② 上轨 | Judge 输入=任务+动作历史+最近截图;列检查项并标满足/违反/未决;全满足→成功,任一违反→失败,否则未决 | §2.1、§2.2 式(1) |
| ② 取证回合 | 只把未决项交给 Probe;K≤2 轮;每轮 ≤15 步 | §2.2;§3.1 Baselines;附录 D、表7 |
| ② 回传 | 只回传检查状态更新+选取的支持观察,Probe 全轨迹不进 Judge 上下文 | §2.2 式(2)后 |
| ② 冻结 Probe | 冻结;只检查不完成/修复任务 | §2.2 Probe 段;附录 I.2 |
| ② 下轨 | 终态是一次随机执行的产物、重放不一定复现、探查会改变它 → 每终态一次验证 | §1 第 4 段;§2.4 |
| ② 封存真值 | Y 在 Probe 交互前记录;标签对所有验证器隐藏 | §2.3;§3.1 Benchmarks;附录 G Terminal reward |
| ② p | p=是否至少调用一次 Probe(0/1) | §2.3;附录 G |
| ② 奖励表 | +1.0 / +0.7 / −0.7 / −0.3 / −1.0 | 附录 G 表9 |
| ② 训练回路 | REINFORCE++ 批内跨终态归一化,只对 Judge 新生成 token 计损失 | §2.4 式(3)(4);附录 E |
| ② 用法 B | 训练后冻结,判定→0/1 奖励,Actor 用 vanilla GRPO | §2.4 Using the trained verifier |
| ③ 结果 A | 4B:OSWorld 73.73→82.00(+8.27)、MobileWorld 73.50→77.50(+4.00)、WebArena-V 61.50→62.75(+1.25)、宏平均 69.58→74.08(+4.50) | 表1 |
| ③ 结果 A 条件 | 同 backbone/Probe/提示词/K=2;Avg@4;只训练 OSWorld;评测轨迹 414/100/100 | §3.1;§3.2 Effect of the learned verification policy |
| ③ 74.09→82.00 | 训练后 4B Judge,OSWorld,K=0→K=2;第一轮贡献大部分 | §3.3 Effect of the probing budget;图5(b) |
| ③ Probe token | 对 few-shot GPT-5.4 少 47.6–59.8% Probe token;宏平均 68.72→74.08(+5.36) | 摘要;§3.2;只计 Probe token 见附录 D |
| ④ 结果 B | Pass@4 All/ID/OOD:43.93/53.40/17.57;45.36/54.37/20.27;45.71/54.85/20.27;47.14/55.83/22.97 | 表2 |
| ④ 任务数 | ≈123/127/128/132(/280),≈13/15/15/17(/74) | **核对换算**:Pass@4×任务数(206+74=280,§3.1) |
| ④ 条件 | 同一 Qwen3-VL-4B Actor、同任务与 rollout 预算、vanilla GRPO,只换奖励源;Actor 训练集 206 单应用任务 | §3.1 Actor evaluation;附录 G 表8 |
| 限制 ① | Judge 在线 RL 训练集 "OSWorld (280 tasks)";74 MultiApp 只声明对 Actor 留出 | 附录 G 表7;§3.1;核对记录存疑点 1 |
| 限制 ② | 相对提示式 VeriCUA +4 / +2 任务;表2 无重复种子/置信区间;+3.21/+5.40 相对初始策略 | 表2;摘要;核对记录存疑点 2 |
| 限制 ③ | Mobile/Web 各 100 条;MobileWorld Probe=GUI-Owl-1.5-32B-Think;Web 仅 +1.25;Actor 在线成功只在 OSWorld | §3.1;附录 D 表5;表1;核对记录存疑点 3–4 |
| 其他条件 | 6 次重执行一致且末三帧 pHash>0.95;只计 Probe token;Avg@4/Pass@4 定义 | 附录 D;附录 A |

## 作者结果 / 阅读判断 / 示意的区分

- 作者结果:③④ 中带"作者报告"标签的数字。
- 核对换算与收窄:④ 任务数、限制栏 ①②③(虚线样式),来自核对记录。
- 我们的阅读判断:④ 下方"我们的阅读"一段。
- 自绘示意:② 双轨图、① 截图卡;未使用或仿制论文原图。
