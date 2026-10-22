# SOURCE · 2311.18751 CompWoB（Sequential-Task Compositions）

- 版本：arXiv 2311.18751v3（HTML 版，2024-12-31）。正文 §1、§4、§6–§8 用本地缓存 `research/fulltext/2311.18751.txt`（v3 HTML，§1/§5 有截断，缺附录）；§5.1–5.4、各图注、附录 D/H/I（Table 14、15、16）由 `https://arxiv.org/html/2311.18751v3` 补读（存 /tmp，不提交）。
- 初筛记录：run `gui-pc11-20261022-01`。L1 `batches/p003.jsonl`，L2 `batches/l02.jsonl`（paper_id=2311.18751；P3 / judgment / F3 / confirmed / to_l3）；入选理由见 `selection2.md` 第 6 行，未决问题见同文件第 54 行。
- 制作：Opus 5.5，2026-10-22。没有运行论文代码，也没有复现实验。

## 数字与断言 → 原文

| 画报内容 | 原文位置 |
|---|---|
| 基本任务平均 94.0%（提示式）/ 85.4%（迁移式）；组合 24.9% / 54.8% | Abstract；§1；Table 5 |
| 提示式基本任务均值 = RCI 90.6、AdaPlanner 92.9、Synapse 98.5 的平均；HTML-T5++ 95.2；人类 93.5 | Table 1 |
| 50 个组合，每个由 2–8 个基本任务组成；分 two-way 20 / three-way 10 / n-way 5 / transition 5 / easy-medium 10；基本任务从 easy 组随机选 | §5.1 |
| 指令用 “and then” 拼接，按 A→B→C 顺序完成 | §5.1；Figure 1 图注 |
| 子任务依赖在奖励里按逻辑“与”处理 | §5.3 |
| 零样本：训练语料和示例都不提供组合任务；50 个组合 × 每个 100 回合；默认 gpt-3.5-turbo；假定最优示例检索器 | §6 Evaluation Methodology |
| 逆序指令：指令倒述，任务顺序语义不变（“solve task B, and solve task C, after solving task A”）；50 个逆序任务与 50 个组合对应 | §5.1；§5.2；Figure 1 图注；Table 14/15 行名一致 |
| 逆序：迁移式 54.8→31.0，提示式 24.9→18.0；降幅 23.8 / 6.9 点 | §6.2；Figure 3 图注；§1（“6.9% vs 23.8% drop”）；Table 5 |
| 迁移式分项 WebGUM 46.3→29.1、HTML-T5 56.6→29.7、HTML-T5++ 61.5→34.3 | Table 14、Table 15 的 Average (total) 行（三者平均分别为 54.8、31.0，已验算） |
| 提示式分项 RCI(comb) 28.7→19.2；三者平均取 RCI(comb)、Synapse(best)、AdaPlanner（Table 14：.287/.254/.206；Table 15：.192/.160/.189，平均 24.9 / 18.0，已验算） | Table 14、15；Table 5 max 列 |
| RCI + gpt-4：组合 56.0，逆序 43.5 | §6.3；Figure 4；Table 14/15 |
| 基本任务上提示式领先、组合上迁移式领先（“opposite trend”） | §6.1 |
| 失败例：“Select rJ and click Submit, after clicking on the "yes" button”，正确计划 3 步、失败计划 4 步（先点 rj、多出 type rj） | Table 4（RCI 列） |
| 作者解释：基本任务示例都是从左到右的指令，把代理绑在线性读法上 | §6.2 第 3 段（作者推测，画报已注明） |
| 组合失败常见：漏中间步骤、动作类型或 XPath 错 | §6.1；Table 3 |
| 20 个二元组合，RCI+gpt-4+oracle 示例 82.9%，逆序 71.8% | 附录 I；Figure 7 图注 |
| 与基本任务成功率乘积 R=0.691，指令 token R=−0.579，HTML 子树最大深度 R=−0.433，p<0.01 | §6.4；Figure 5 图注 |
| 迁移式为 3B 参数、只在基本任务上微调 | §4.4；Figure 2 图注 |
| 未报告方差 / 置信区间 | 全文与附录检索 std / confidence / seed / error bar 均无结果 |

## 示意内容（不是论文实验图）

- 三环链条、连环、断点位置、交叉连线和全部图标为自绘 SVG。三个任务块取自原文 Figure 1 / §5.1 的组合例（click-checkboxes-transfer + enter-password + click-dialog），中文任务名是我们的意译。
- 链条右侧的数字是 50 个组合的平均，不是这一条组合的成绩；画报没有使用这条组合的单项成绩。
- 断点画在 A–B 之间、B–C 环画成“受力”虚线，都是为讲清“平均成功率下降”的示意，不对应论文的统计。
- 失败例动作序列按原文 XPath 简写（如 `//button[text()="yes"]` → `button "yes"`）。
- 底部“阅读判断”栏是我们的解读，不是作者结论。
