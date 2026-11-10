# SOURCE — 2403.08140 BAGEL: Bootstrapping Agents by Guiding Exploration with Language

- 论文：arXiv **2403.08140v2**（v1 2024-03-12，v2 2024-06-09；2026-11-10 查 export.arxiv.org/api，最新为 v2，与 corpus.jsonl `latest_version` 一致）
- 阅读材料：本地 `research/fulltext/2403.08140.txt`（裁剪 core）+ arxiv.org/html/2403.08140v2 全文（§1–10、附录 A–D，含全部提示词与表 5）。图 3 为 pgfplots SVG，读到平均标注 46.8 / 60.5（MiniWoB）、40.9 / 43.3（ToolQA）；逐任务零样本柱值未能读出。转换稿在 /tmp/sel14，不提交。未运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-40.jsonl`（L2，supersedes inc-l1-81#2403.08140；P3 confirmed；q1 measured_own、q2 open_failure、q3 capability、q4 fits；F3,F2；卡 exploration_driven_task_synthesis、experience_memory_retrieval；子卡 K14、C19：2 holds、5 partial）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-014.md` 第 1 节
- 画报源：`poster.html`；`poster.png`（1400×2000）、`poster.pdf`（1 页，1050×1500 pt），本地 Chrome（Playwright）渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题 | 同一 PaLM-2、五个提示角色；检索 3 条；46.8 → 60.5 | §3.1；附录 A.1；图 3 |
| 前提框 | 无人工示范、无测试指令、只做上下文学习；可预探索；环境报错 | §1；§4；§6.2；影响声明 |
| 1 循环图 | 轨迹优先 / 指令优先；标注器看首末页面与变化；最多 5 轮；打分 1–5 | §3.1–3.2；§6.2；附录 B 列表 4–7 |
| 1 循环图 | 版面 | **示意**（依原文图 1 重绘） |
| 2 例子 | choose-date 三轮动作与标签、✗✗✓ | 图 2（原文示例，中文转述） |
| 2 报错 | 1.3 → 0.1；3.0 → 0.6 | 表 3；§8.2 |
| 2 检索 / 执行 | T5-XXL、余弦、top-3；动作字符串由另一 LM 映射元素 id，调用 Selenium | 附录 A.1；§5.1；附录 C |
| 2 示范摘录 | Reply / Forward / Like, Share 三条 | 表 4 |
| 3 | MiniWoB 46.8 / 52.0 / 56.0 / 53.0 / 61.0；ToolQA 40.9 / 38.8 / 43.3 / 40.9 / 42.2 | 表 1；§7 |
| 3 来源行 | 10 任务 × 50 种子、映射到 0–1；图 3 为 60.5 | §5.1；图 3（与表 1 差异为**我们比对**；表 5 十项平均 = 0.605，**我们复算**） |
| 4 | 10 任务 BAGEL 分数 | 附录 D 表 5 |
| 4 注 | +20（choose-date、tic-tac-toe、use-autocomplete）；book-flight 5 → 15；search-engine +5 | §7；§8.5 |
| 5 | 打分器为 LM 1–5 分；人工按执行结果剔错 +7 个百分点 | 附录 B 列表 7；§8.3 |
| 5 第三条 | 60.5 + 7 的条长 | **示意**（原文未给具体平均） |
| 6 | 40.9 / 38.0 / 41.4 / 42.2（ToolQA） | 表 2；§8.1 |
| 7 | 1.3 → 0.1；3.0 → 0.6；3.0 → 1.9 | 表 3 |
| 8 | BAGEL / Flat / SteP / RCI 分数与底座模型 | 附录 D 表 5 |
| 限制 | 最难 10 个（<0.95）；同一任务生成器（随机种子）；温度 1.0；PaLM-2；60 条；book-flight 全为十二月；SciRex 全错 | §5.1；§6.2；§8.5 |
| 怎么读 | 与 OS-Wizard、AWM 不同题；7 点空间 | **我们的阅读** |

## 我们的判断（非原文）

- “测试任务由同一零样本代理挑出”“自打分放过错误示范”“+7 用到标准答案、不属无监督”；“未报告重复运行或方差”（原文只给单值）。
- 原文“13× reduction”对应 choose-date 1.3 → 0.1 为**我们对应**。
