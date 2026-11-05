# SOURCE — 2610.31274 PointerBench: A Diagnostic Benchmark for Fine-Grained GUI Grounding

- 论文：arXiv **2610.31274v1**（2026-10-22；2nd Workshop on Agentic AI Benchmarks and Applications for Enterprise Tasks；2026-11-05 查 export.arxiv.org/abs 只有 v1）
- 阅读材料：本地 `research/fulltext/2610.31274.txt`（文件头 v1，裁剪 core）；按钉定版本补读 arxiv.org/html/2610.31274v1 全文 §1–4 与 App. A–H（表 1–15；图 2 从原文 SVG 取柱高换算，图 1 与图 3–5 只读图与说明）。转换稿在 /tmp/sel10，不提交。没有下载基准数据或评测代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-02.jsonl`（L2，supersedes inc-l1-01#2610.31274v1；P3 confirmed，q1 measured_own，q2 open_failure，q3 capability，q4 fits；F0；卡 main/high_resolution_target_localisation、main/online_evaluation_methodology；子卡 C26）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-010.md` 第 1 节（selection-004 起的备选）
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | Fable 5 单词 90.2 → 字符 70.4 / 插入点 64.7 / 区域 56.0 | §3.3 表 3 |
| 标题 | 专用模型一到三成 | 表 3：顶尖专用模型字符 11.1–18.5、插入点 22.5–34.2；§3.3 |
| 副标题 | 1,500 张 1024×768、像素精确、三套各 500 | 摘要；§1；§3 “Task design” |
| 副标题 | Pro 界面也是生成的 | App. A “PointerBench-Pro”（generated professional-application interfaces）；App. H |
| 副标题 | 37 个通用模型同一提示；39 个专用配置原生提示与坐标约定 | App. C “Prompt”；App. F 表 14；§3.2；App. G |
| 副标题 | 单步静态、不执行 | §1；§2；App. H |
| 01 左图 | 列边线 1–3 px、两字形间插入点、专业软件图标 | 图 1(a)(b)(c)；§3 “Task design”（1–3 px dividers）。**示意重画，非原图** |
| 01 左图 | 面积中位数 0.215% / 0.0286% / 0.129%，约 1/7.5 | App. B “Spatial and geometric coverage” |
| 01 右 | 点在区域内；框覆盖 ≥0.90 且精确率 ≥0.70；畸形算错；不重试 | §3 “Task design”；App. C 式 (1) 与 “Inference settings” |
| 01 右 | Text 构成 187/134/112/27/23/17 | App. B 表 5 |
| 02 图 | Fable、Opus、Sol、MVP-32B、GTA1-32B、UI-Venus-2-9B 在单词/字符/插入点/区域 | 表 3（标点、界面文字两列未画） |
| 02 图 | 三个专用模型只出点 → 区域记 0 | §3.3（point-only 在 134 题上 0.0）；表 3 Region 列 |
| 02 右 | UI-Venus-Ground-7B 11.2、GUI-G2-7B 12.7 | §3.3 |
| 02 右 | 框失败：Fable/Opus 偏大 26.1%；Sol/Luna 裁掉 39.6%/41.8% | App. E 表 12 |
| 02 右注 | 字符 27、标点 23；英语/非英语各 250，Fable 69.6/69.6 | App. B 表 5；App. E 表 11 |
| 03 热力表 | 9 种插入位置 × 6 模型的成功率 | 图 2（caret_success_by_objective_four_models.svg）：按柱高 ÷（100% 网格线 − 基线）换算，四舍五入；与各类 n 的 k/n 吻合（如 Fable 词间 10/22=45.5、字间 26/36=72.2），加权总和复现表 3 Caret 列（Fable 121/187=64.7）。GTA1-32B 句子边界无柱，记 0。“空行”n=1 未列 |
| 03 右 | 词前/词后/词间前沿 ≤50%、专用 <24% | §3.3 图 2 说明段；热力表 |
| 03 右 | 段首、段尾专用 64–91%；字间 Fable 72、专用 17–28 | 热力表（我们按图 2 读数归纳） |
| 03 右 | 面积最大四分之一比最小高 10.7 点，只部分解释 | App. B “Area alone can obscure…” |
| 03 右 | 插入点总分 64.7/62.6/51.9/34.2/22.5/25.7 | 表 3 Caret 列 |
| 03 右 | 键盘替代路径未测 | **我们的阅读**；原文未讨论 |
| 04 左 | 3.1→78.1、2.8→55.4、1.5→31.9；输出 0–1000；换算不计排名 | §3.3 “Coordinate-frame compliance”；App. E 表 13 |
| 04 左注 | 37 个系统中 22 个平均 ≤10.2%；只核了 3 个 | App. F 表 14（第 16–37 名，我们计数）；App. E 表 13 |
| 04 中 | Fable 单元格/表头/颜色 100；行高拖柄 78.1；UI-Venus-2-9B 单元格/表头 89.0–100、边线/拖柄 31.6–55.8、相对偏移 3.0；前沿四模型边线 81.0–98.3 | App. E 表 9；§3.3 “PointerBench-Sheets” 与 “PointerBench-Text” 段 |
| 04 右 | 图标 190 / 文字 154 / 其他 156；375 次失败中图标 215（57.3%）；图标 70.0–75.3、文字 89.0–92.9 | App. A “PointerBench-Pro”；App. E 表 10；§3.3 |
| 04 右 | 低推理对关闭：Luna +19.2、Sol +9.8、Sonnet −1.8（p=0.00182），配对 McNemar | App. D 表 8 |
| 全榜一瞥 | 37 个通用系统平均值、39 个专用配置平均值；中心点击 0.3% | App. F 表 14；App. G 表 15。竖线由我们按两表“Avg.”列绘制 |
| 全榜一瞥 | Gemini 3.7 Flash 换算后 78.1，不计排名 | 表 13 |
| 限制 | 单步静态；合成截图；两榜协议不同；单次运行；样本小；无人类基线与标注误差审计 | App. H；App. A；App. C；App. G；表 5 |
| 我们的阅读 | 把总分拆成操作原语；低分可能有不少是坐标约定；需在线任务回答阻塞性 | 我们的归纳，依据 §4、表 13–14 |

## 原文内部出入与口径

- 没有发现与 L2 facts 冲突的数字。L2 引用的 UI-Venus-2-9B 字符 11.1 / 插入点 25.7 / 单词 52.7、Gemini 3.7 Flash 与 Qwen3.8 Max 的 3.1/2.8 → 78.1/55.4 均与表 3、表 13 一致。
- 摘要与表 1 只列代表性模型；“37 个通用系统”取自 App. F 表 14 的行数（不含中心点击基线）。

## 示意与自绘

- 01 左图三联为按原文图 1 重画的示意，不是原文截图。
- 粒度阶梯、热力表、哑铃图与全榜竖线由我们按原文表格与图 2 SVG 数值绘制。
