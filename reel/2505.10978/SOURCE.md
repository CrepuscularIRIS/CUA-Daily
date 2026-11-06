# SOURCE — 2505.10978 Group-in-Group Policy Optimization for LLM Agent Training (GiGPO)

- 论文：arXiv **2505.10978v3**（v1 2025-05-16、v2 2025-09-03、v3 2025-10-28；2026-11-06 查 export.arxiv.org/abs，最新为 v3，与本地缓存版本一致）。第一作者 Lang Feng
- 阅读材料：本地 `research/fulltext/2505.10978.txt`（文件头 v3，裁剪 core）；按钉定版本补读 arxiv.org/html/2505.10978v3 全文 §1–6 与附录 A–F（表 1–5；图 4 消融雷达、图 5 组大小、图 6 计时为原文 SVG，图 4 由 SVG 多边形坐标换算读数；附录 F 推理样例只读说明）。转换稿与 SVG 在 /tmp/sel11，不提交。没有运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-23.jsonl`（L2，supersedes inc-l1-32#2505.10978；P3 confirmed，q1 measured_own，q2 open_failure，q3 capability，q4 fits；F2/F1；卡 main/trajectory_level_policy_training、main/verifiable_execution_reward；子卡 K20、K30）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-011.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 不加价值网络、不加采样的逐步信用分配 | 摘要；§1 第 4–5 段；§4.2 “Anchor state grouping” |
| 副标题 | GRPO 每步同一优势 | §4 首段；图 1 左 |
| 副标题 | 8 条 rollout、回到相同页面 | §4.1（N 条同任务同初始状态）；§5.1 “rollout group size N … 8” |
| 副标题 / 票根 | 7B 66.1 ±3.7 → 75.2 ±3.8（不除 std），72.8 ±3.2（除 std）；1.5B 56.8 → 67.4 | §5.2 表 1（WebShop Succ.，3 seeds） |
| 副标题 | rollout 与显存不变，每轮多约 0.5 秒 | §5.6；图 6（0.01 s + 0.53 s，ALFWorld、1.5B） |
| 票根 | WebShop 为 HTML 文本观测模拟站 | §5.1 “WebShop … simulated HTML-based shopping website”；附录 E.2 图 9 提示模板 |
| 01 示意 | 三条轨迹交汇于同一搜索结果页；点第 2 件→返回、点第 1 件→成功、下一页→失败 | §4.2 图 3 及 “How does step-level group work?” 段。**示意重画，非原图** |
| 01 右框 | A^E 组均值归一；A^S 同锚点组；γ=0.95；A = A^E + ω·A^S，ω=1；哈希表；无重复时退化为 GRPO | §4.1 式 (3)；§4.2 式 (4)–(7)；§4.3 式 (8)；附录 E.1（γ、ω）；§6（退化为 GRPO） |
| 01 排序条 | A^S(第1件) > A^S(第2件) > A^S(下一页) | §4.2 图 3 说明段 |
| 对照条件 | 同超参；组 8×16；WebShop ≤15 步；奖励 10/0/−0.1；lr 1e-6；KL 0.01；150 轮；历史 2 步 | 附录 E.1 “Hyperparameters for WebShop”“Computing Details”；E.2（history length 2） |
| 02 柱 | PPO 51.5/68.7、RLOO 52.1/65.7、GRPO 56.8/66.1、GiGPO 65.0/72.8（除 std）、67.4/75.2（不除 std），均带 ± | 表 1 |
| 02 参考线 | GPT-4o 23.7、Gemini-2.5-Pro 35.9（提示式） | 表 1 闭源行 |
| 02 注 | ALFWorld All：GRPO 72.8/77.6；GiGPO 86.7/86.1、90.8/90.2 | 表 1 |
| 02 标题 | 拉开 7–11 点 | 表 1：1.5B +8.2/+10.6，7B +6.7/+9.1（我们复算） |
| 02 消融表 | 完整不除 std 67.4/76.5/79.5/71.7；除 std 65.0/67.5/76.4/79.8；去 A^S 56.8/55.3/54.6/61.0；去 A^E 62.5/60.1/63.2/66.0（WebShop/Look/Pick2/Cool） | 图 4（ablation.svg）。我们按 SVG 多边形顶点到圆心距离换算（中心 = 20，外圈 = 100）；两“完整”变体换算值与表 1 1.5B 行逐格一致，作为校验 |
| 02 消融注 | 任一层拿掉掉 5–25 点；去 A^S 的 WebShop 与 GRPO 同为 56.8 | 图 4 换算值 vs 表 1（我们复算） |
| 02 ω 曲线 | 56.6/63.1/65.8/67.2/68.3/67.4/66.5/56.3 | 附录 E.5 表 5（Success Rate 行） |
| 03 计时 | 362.83 s；0.01 s；0.53 s；≈0.15% | §5.6；图 6。0.54/362.83 = 0.149%（我们复算） |
| 03 计时注 | 原文“<0.002%” | §5.6 末句；摘要同义表述“little to no additional time cost” |
| 03 计时注 | 128 个环境；PPO 128 个独立环境 | 附录 E.1 |
| 03 组大小 | 第 10 轮 10–49：16.2%、≥50：5.6%；第 75 轮 12.1%、3.1%；第 140 轮集中 6–8；组大小 1 始终 <35% | §5.5 正文与图 5 |
| 03 叠加 | GRPO 56.8、DAPO 66.1、GiGPO+DAPO 75.0（WebShop 1.5B） | 附录 E.4 表 4 |
| 03 叠加 | Sokoban GRPO 67.1 → 81.0（Qwen2.5-VL-3B） | 附录 E.3 表 3 |
| 限制 | 文本观测、search/click 动作 | §5.1；附录 E.2 |
| 限制 | 相似度匹配阈值 0.9 只用于搜索问答 | §5.1 “Training details” |
| 限制 | 同观测 ≠ 同状态 | L2 biggest_gap；论文 §6 只谈“噪声或细微差异导致难以匹配”，未讨论部分可观测的误合并。为我们的阅读 |
| 限制 | 7B：不除 std +9.1，除 std +6.7 | 表 1（我们复算） |
| 限制 | 消融、ω 扫描未注明种子数；图 5 只有 ALFWorld | §5.4、§5.5；附录 E.5 |
| 我们的阅读 | 循环变对照组；对齐决定适用范围；收敛后组内趋同；与 2406.11896 互补 | 我们的归纳；图 5 的“组大小集中 6–8”与 §5.5 末段作者解读（8 条行为一致） |

## 原文内部出入与口径

- §5.6 写新增计算占每轮时间“< 0.002%”，按其给出的 0.01 s + 0.53 s 与 362.83 s 计算为约 0.15%（应为 < 0.2%）。结论“几乎不增加时间”不变；画报按复算值写并注明。
- 摘要与 §5.2 的“> 9% on WebShop”取不除 std 变体；另一变体 7B 为 +6.7。画报两个变体都画。
- 图 4 消融为雷达图、无误差线，未注明是单次还是多种子；“去掉 A^S”在 WebShop 上与表 1 GRPO 同为 56.8，ALFWorld 各子任务与 GRPO 相差 0–1.7 点。

## 示意与自绘

- 01 线路图为按图 3 文字与图 2 结构重画的示意，商品与页面为占位。
- 02 消融表数值由我们从原文 SVG 坐标换算，非原文表格；其余条形、折线由我们按原文表格数值绘制。
