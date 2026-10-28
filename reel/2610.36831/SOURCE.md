# SOURCE — 2610.36831 Right Click, Wrong Box: Grading GUI Grounding by What a Click Does

- 论文：arXiv **2610.36831v1**（2026-10-27）
- 阅读材料：本地 `research/fulltext/2610.36831.txt`（文件头 v1，抽取 core，§4.3 之后截断）；按钉定版本补读了 arxiv.org/html/2610.36831v1 的正文 §1–7 与附录 A–I。转换稿放在 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-06.jsonl`（L2，P3 confirmed，q3 judgment，F2；卡 main/online_evaluation_methodology；子卡 C26/K34）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-006.md` 第 1 节
- 画报源：`poster.html`（单文件，内联 CSS/SVG/JS 绘图）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome 经 Playwright 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题 | 领先 grounder 在 ScreenSpot-v2 上 93–96%；同尺寸模型差距中位 1.15 点 | 摘要；§1；§6 “Reported margins” |
| 副标题、02 | 被框拒绝的点击中达成目标结果：Gitea 17.6–20.5%，Oscar 29.7–38.1% | §4.2 Tab.3 Rescued 列 |
| 副标题、03 | ScreenSpot-v2 校正 0.2–1.8 点 | 摘要；§6 “Scoring”；App. C Tab.S5 |
| 01 示意 | 提交哈希与提交说明打开同一提交；作者名与头像打开同一主页 | §1；App. A Fig.S1(a)；**示意重画，非原图** |
| 01 研究动作 | o_b 定义、E(s,b)、E\b 与 b\E | §3.1 |
| 01 研究动作 | Chromium 1280×720；悬停 120 ms；等待 ≥250 ms、至多再 1.5 s；指纹顺序 nav/popup/非 GET/dialog/dom/noop；拦截跳转与非 GET | §3.2；App. A Tab.S1 |
| 01 研究动作 | Oscar 中间件回滚事务；数据库探测前后一致 | §3.3；App. A “Oscar” |
| 01 研究动作 | 每页约 1,000（Gitea）/ 700（Oscar）次点击 | §4.1 |
| 01 研究动作 | 重载一致 97.9/99.8%；框中心复现 98.1/98.7%；重复执行判决 98.6/98.7% | §4 Tab.1 |
| 01 出处行 | Gitea 4,970 个活目标 17.7% 不一致；Oscar 1,224 个 31.2% | §4.1 |
| 02 | 6 行：框/结果准确率、Δ 与 95% CI、被救回次数与比例 | §4.2 Tab.3 |
| 02 注 | Gitea 3,586 题、Oscar 1,147 题；模板 Click the &lt;role&gt; "&lt;text&gt;" | §3.4；§4.2 |
| 02 注 | 自然指令改写后比例 14.3% / 34.8%，框准确率降 10–16 点 | §4.2 “Natural instructions”；App. B Tab.S3 |
| 03 标尺 | 同尺寸差距中位 1.15（58 组 head-to-head）；种子极差至多 2.6；配对差 95% 半宽 1.26–1.54；校正 0.2–1.8 | §6；Fig.6；App. F Tab.S7；App. G |
| 03 右 | Web 14.4 [9.5, 21.2]（145 单元）、移动 1.0 [0.2, 5.6]（104）、桌面 0.9 [0.2, 5.2]（111） | §4.3 Tab.4 |
| 03 右 | 7–8B 强模型 20.6% [12.7, 31.6]；3B 2.9% [1.5, 5.6] | §4.4 |
| 03 右注 | 360 单元盲审；两位评审 60 单元 κ=0.95 | §3.5；Tab.1；App. C Tab.S4 |
| 03 右注 | GTA1 与 UI-Venus 差 2.9→1.7；3 对顺序反转，区间含 0 | §6 “Scoring”；App. C Tab.S6 |
| 两条做法 | 29 篇论文无一报告运行间波动；38 次领先中 21 次 ≤ 单种子效应 1.42 | §6 “Reported margins”；App. G |
| 两条做法 | 原生控件多为单一点击区，框外点击几乎都是真错 | §7 “Where equivalence comes from” |
| 训练奖励 | Qwen2.5-VL-3B + LoRA GRPO，3 种子，三种奖励；框奖励均值 85.2/89.6/80.5/86.5；结果−框 −0.18/+0.06/−0.08/+0.23 | §5 Tab.5 |
| 训练奖励 | seed 42 SSv2 p=0.03 结果奖励赢，seed 44 p=0.02 框奖励赢 | §6 “Seeds”；Fig.5a；App. E “Decision rules” |
| 训练奖励 | 193 个同结果多副本题框准确率 28.5–35.2%，结果准确率 90.7–100%；唯一 3,092 题差距小于框中心漂移 | §4.2；App. B Tab.S2 |
| 训练奖励 | 训练模型在同结果副本题上 100% 达成，点中被标注那份 27–29%；“ceiling of the test” | §5 “Why the extra credit adds little” |
| 限制 | 两个自托管 Web 应用；移动/桌面约 1% | §4.3；§7 “Scope” |
| 限制 | 拦截请求、1.5 s 等待 | §3.2；App. A “Waiting rule” |
| 限制 | 自检 30 个中 2 个假阳性 | App. A “Self-check” |
| 限制 | 3B、约 400 次更新（396） | §5 Setup；§7 “Scope” |

## 未上画报的原文内容及原因

- Mind2Web 静态分析（1.3% 步骤可见等价元素，作为下界）：只能从 label 关系恢复等价，未上画报，限制栏的“移动/桌面”已覆盖“非执行”口径。
- GUI-Libra 三种子均值差（App. E）：与结论“不稳定”一致，表中未单列。

## 示意与重绘

- 01 提交列表与点列：按 Fig.1 / Fig.S1 的现象自行绘制，标“示意”，点位不是真实探针数据。
- 02、03、训练奖励表：用作者表格数字重绘，不是原文图片。
