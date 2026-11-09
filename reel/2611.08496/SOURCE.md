# SOURCE — 2611.08496 MobiInfer: Accelerating On-Device GUI Agents with Workload-Aware Inference

- 论文：arXiv **2611.08496v1**（2026-08-11；2026-11-09 查 export.arxiv.org/abs，最新仍为 v1，与本地缓存版本一致）
- 阅读材料：本地 `research/fulltext/2611.08496.txt`（文件头 v1，裁剪 core）；按钉定版本补读 arxiv.org/html/2611.08496v1 全文（摘要、引言、§2 动机、§3 方法与算法 1、§4 实验全部小节、相关工作、结论；表 1–4）；图 4–7 为位图，实际打开读取标注值。原文多处指向“supplementary material”（硬件细节、完整任务清单、分设置成功率），arXiv 版未附，**未读到**。转换稿与图片在 /tmp/sel13，不提交。没有运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-34.jsonl`（L2，supersedes inc-l1-70#2611.08496；P3 confirmed，q1 measured_own，q2 new_bottleneck，q3 capability，q4 fits；F0；卡 main/agent_loop_context_control、main/online_evaluation_methodology；子卡 C24 + unassigned）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-013.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome（Playwright 驱动，`--disable-lcd-text`）渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题 | 平均快 2.4×；成功 58.1% → 57.7%，最多降 0.9 点；不重训、不改动作接口 | 摘要；§1；§4 “Main Results and Task Quality” |
| 页眉规格 | MAI-UI-2B、GELab-Zero-4B；INT8 GPTQ（AutoRound）；MNN；OnePlus 13 / OPPO Find X8 / Redmi K50；AndroidWorld 116 模板 / 20 应用，自建 RealWorld 111 题；基线 = MNN 原模板，同权重、分词器、量化、动作格式、种子 | §4 “Experimental Setup” |
| 1 问题 | 每步重新预填充、全词表投影 | §1 第 2–3 段；§2 |
| 1 数字 | 基线 85.8 s / 困难 283 s / 购物 833 s | 表 1（MAI-UI-2B） |
| 1 数字 | 词嵌入与输出头占 34.3% 权重 | §4 “Memory and Storage Footprint” |
| 1 小图 | 14,162 / 151,669；209 / 349 / 580 种覆盖 80 / 90 / 95%；3-token 69.1%、4-token 57.6% | 图 3 标题；§2 “Phase-Structured Outputs” 末段；图 2 |
| 2 输入 | 固定 / 半固定 / 动态三段及其内容；固定段离线存盘并核对模型与模板；半固定段每任务一次、换目标重建；无法安全归类放动态段；同 token / 位置 / 权重 / 内核下恢复等价于重算；增量预填充 | §3 “Prompt canonicalization”“Prefix materialization and restoration”；式 (1) |
| 2 输出 | 自动机状态：结构、推理、动作、坐标、其他参数、完成；可投机 = 结构、推理；受保护 = 动作、坐标、参数；n-gram 离线表 + 任务内缓存；批量验证、最长匹配前缀；SafePrefix | §3 “Schema-Guided Speculative Decoding”；式 (4)–(5)；算法 1 |
| 2 词表 | 全局裁剪保留出现过的行 + 格式所需 + 特殊符号 + 256 字节 token；按状态选阶段输出头；映射回原 token ID；裁剪是近似 | §3 “Phase-Indexed Vocabulary Specialization”；式 (2)–(3)；§3 末段 “vocabulary specialization itself is approximate” |
| 2 词表宽度 | 各阶段词表大小 | **示意**：原文未给 |
| 2 下卡 | 1 步 11.47 → 6.83 s，5 步 96.53 → 42.39 s；1.68 / 1.78 / 1.97 / 2.10 / 2.28× | §4 “Scaling with Agent Steps”；图 6 标注 |
| 3 大图 | 12 组每题推理时间（基线 / MobiInfer）：AW OnePlus 85.8/39.9、137.0/56.9；Find X8 89.2/41.0、142.9/58.8；K50 113.6/49.8、182.5/71.5；RW OnePlus 118.3/50.8、189.4/72.4；Find X8 156.9/74.3、197.5/74.8；K50 197.1/91.4、252.4/90.9 | 图 5 柱顶标注。倍数与“平均 2.39×”为**我们复算** |
| 3 注 | AndroidWorld 模板化任务重复结构更多；视觉段不变 | §4 “Main Results” 第 2 段；图 5 |
| 3 消融 | 1.00 / 1.12 / 1.27 / 1.33 / 1.69 / 1.90 / 2.20 / 2.33×；每配置 3 次；K / D / P 含义；P 主要省输出头计算、内存与存储 | 图 7 标注与标题；§4 “Ablation Study” |
| 3 投机对比 | 118.3 / 103.4 / 126.5 / 93.2 s；1.00 / 1.23 / 1.15 / 1.84×；42.3 / 41.4 / 39.6 / 41.4% | 表 3；§4 “Speculation Strategy Comparison” |
| 4 表 | 0.782/76.4/91.8/100.0；0.780/76.1/91.7/98.9；0.779/75.8/91.5/98.5；0.777/75.5/91.3/98.1 | 表 2；§4 “Quality Preservation” |
| 4 KPI | 58.1 → 57.7、最大降 0.9 | §4 “Main Results” 末段；图 4 |
| 4 KPI | PSS 3,769.98 → 2,570.26 MiB（−31.82%），Find X8 −31.89%，K50 −31.33% | 表 4 |
| 4 KPI | 部署 3,279.83 → 2,297.01 MB（−29.97%），含 27.48 MB n-gram 表与 108.27 MB KV | 表 4 及标题 |
| 4 表 1 摘录 | AW 简单 / 中等 / 困难 49.25→26.71（1.84×）、96.23→43.46（2.21×）、283.28→88.72（3.19×）；RW 导航 / 系统 / 搜索 / 购物 21.30→12.19、70.09→34.40、86.57→39.87、832.71→185.78（1.75/2.04/2.17/4.48×） | 表 1（MAI-UI-2B） |
| 3 注 | GELab 困难 3.60×、购物 5.38× | 表 1（GELab-Zero-4B） |
| 限制 1 | 表 1 “E2E latency” = 推理时间（视觉 + 预填充 + 解码）；对应 OnePlus 13 | 表 1 的 85.81 / 136.99 / 118.32 / 189.38 与图 5 OnePlus 13 柱顶、图 7 基线 ≈118 s 相同（**我们比对**）；图 5 纵轴为 “Absolute inference latency” |
| 限制 2 | 约 1.9% 输出不同；投机只对裁剪后策略无损 | 表 2 “MNN agree.” 98.1%；§3 末段 |
| 限制 3 | 词表、n-gram 表来自 7,000+ 条采集轨迹，与测试任务的划分未说明；补充材料未附 | 图 3 标题；§3；§4 “Experimental Setup”（指向 supplementary）。“未说明”为我们核对正文的结论 |
| 限制 4 | 误差线重叠；两个 INT8 小模型、三台手机 | 图 4（误差线未定义）；§4 |
| 怎么读 | 困难题加速后仍 88.7 / 126.7 s | 表 1 |

## 我们的判断（非原文）

- “改变的是循环的推理成本这一环”“与 agent_loop_context_control 既有卡片的关系”为阅读判断。
- 12 组倍数与平均 2.39× 由图 5 标注复算；“表 1 对应 OnePlus 13”“端到端 = 推理时间合计”由表 1 与图 5、图 7 数值比对得出。
- 机制图（手机外形、三段条、阶段胶囊、词表宽度）为示意；数值图按原文数值重绘，不是原图。
