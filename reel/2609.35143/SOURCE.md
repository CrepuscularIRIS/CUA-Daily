# SOURCE — 2609.35143 Timeline-Bench: Evaluating Agents on Realistic Video-Editing Tasks, from Raw Footage to Final Cut

- 论文：arXiv **2609.35143v1**（2026-09-28；2026-11-07 查 export.arxiv.org/abs，最新仍为 v1，与本地缓存版本一致）
- 阅读材料：本地 `research/fulltext/2609.35143.txt`（文件头 v1，裁剪 core）；按钉定版本补读 arxiv.org/html/2609.35143v1 全文 §1–9、Reproducibility / Ethics / AI Use 声明与附录 A–N（表 1–11；图 1、4、5、8、9 为位图，只读说明与正文数字）。转换稿在 /tmp/sel12，不提交。没有运行代码，没有访问任务媒体
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-31.jsonl`（L2，supersedes inc-l1-47#2609.35143；P3 confirmed，q1 measured_own，q2 open_failure，q3 judgment，q4 fits；F2/F0；卡 main/online_evaluation_methodology、main/learned_outcome_and_process_judges、main/verifiable_execution_reward；子卡 K30、C24、K16）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-012.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题 | 56 个任务；16 个代理各 1 次；43 位剪辑师、2,582 次可评判断 | 摘要；§3.2；§4 |
| 副标题 / 右框 | 771 个未解决中 562 个只输在质量门（73%）；15/16 个代理 61–90% | §6 第 2 段；图 4a |
| 副标题 / 02 | 代理级 ρ=0.93（留一代理阈值）；单片 κ=0.15 | §5 “Human preference” 段；附录 D.4 |
| 副标题 / 05 | GPT-6 Astra 计算机使用 2/56，Codex CLI 12/56 | 表 1（3.6% / 21.4%）；附录 I.1 表 9 “Resolved 2 vs 12” |
| 01 漏斗 | 896 → 863 交出 → 857 合规格 → 687 过全部非质量测试 → 125 解决（14.0%，CI 11.7–16.4） | §4（896 runs）；附录 J.1（863 delivered、857 meet spec / 6 fail delivery、762 pass every brief test）；表 1 “Tests” 列合计 687、“All agents 14.0”；§5（125 of 896）。687 − 125 = 562 为我们复算，与 §6 一致 |
| 01 门说明 | 交付 4 项；内容 6 项（附录 C 表 4）；简报 180 项 = 153 程序化（帧/声匹配、OCR、Whisper）+ 27 项三判官 2/3 多数 | §3.1；附录 C；附录 E |
| 01 质量门 | 三判官 1–10 分、各自 z 分、平均；不看简报；须高于参考剪辑合集阈值；冻结阈值 0.30/0.52/0.21/1.54 | §3.3；附录 D.2–D.3 |
| 02 条形 | α=0.10（单票，ordinal）；κ=0.15（面板 vs 人类多数）、0.14（单个剪辑师 vs 其余多数）；ρ=0.32（每题通过率 vs 人类每题率）；信度 0.84；ρ=0.93 | 附录 G.1；附录 D.4；§5 |
| 02 注 | 阈值“通过率尽量接近但不超过人类胜/平率”；限制节“valid per agent, not per edit”；GPT-6 Astra 是判官之一 | §3.3；§7；§3.3 判官名单与 §4.1 代理名单 |
| 03 散点 | 16 个代理（解决率，人类胜/平率），按 harness 分形状 | 表 1 / 表 8 |
| 03 注 | 35 题无人解决（随机约 5）；Rasch 题难度方差 2.6 倍 | §6 “Difficulty belongs to tasks”；附录 J.3、K.2 |
| 04 森林图 | 6 组配对：−4.2 [−13.2,+4.7]、+0.9 [−7.5,+9.4]、+0.6 [−9.6,+10.8]、+5.9 [−2.9,+14.7]、+0.6 [−8.4,+9.6]、−16.4 [−24.0,−8.7]；解决数 5/10、12/12、10/10、13/10、15/12、2/12；p&lt;0.001、McNemar 0.038；n=53 | 附录 I.1 表 9 |
| 04 注 | 编辑指南 1,909 字 | §4.1 “Curated guidance” |
| 05 表 | 解决 / 胜平 2/56·8.2% vs 12/56·23.8%；漏台词 41.5% vs 5.9%（代码代理）；场记板 / 现场对话 / 重拍 18.5% vs 1.4%（人评前 6）；重复素材 18.5% vs 3.6%；时长中位 52.7 vs 19.6 min；成本 $41.61* vs $8.71* | 表 1；附录 J.1、J.2；附录 H.3 表 7 |
| 05 注 | macOS + DaVinci Resolve 免费版、项目与素材已导入、无 shell；代码代理 Linux 容器 + FFmpeg / Remotion / 转写命令；“cannot hear” | §4.1 “Computer use”；§4.2；附录 H.2 表 6；附录 J.1 |
| 06 卡 1 | 54% 感知 / 17% 验证 / 9% 构建；98% 感知在首次渲染前；首次渲染在 72–90%；83% 读取为帧或联系表；111,636 个动作 | §6 “Agents look first” 段；附录 K.3 |
| 06 卡 2 | 5.5% vs 66%；14/15 代码代理 86–100% 运行自查 | §6 同段；图 5d |
| 06 卡 3 | 93% 声称成功，含 95.5% 未过测试者；由 Claude Opus 5.5 标注、作者核对 | §6 同段；附录 K.3 “Self-reports” |
| 06 卡 4 | 换镜 0.72×、最长静止 1.5×；每减半 −6.6（CI 3.2–10.0）；更快不扣分 | §6 “Human editors prefer” 段；附录 J.2 |
| 07 能力条 | 八项读数与证据 | §6 表 2（作者归纳）；证据数字来自表 2、附录 J.1–J.2、§6 |
| 限制 | 每题 1 次、CI 约 ±11；阈值下移 0.1 多 27 个、ρ=0.96；剪辑师不看简报；参考非认证真值 | §5；§6；§3.2；§7 |
| 顶部条 | 装饰性时间线 | **非数据** |

## 我们的判断（非原文）

- “改变的是反馈 / 评价这一环”“自查只覆盖代理看得到的通道”“计算机使用臂差别不能归为 GUI 操作本身”为阅读判断（后者与 L2 一致，并由 §4.1、附录 H.2 的环境差异支撑）。
- 所有图形为我们按原文表格绘制；散点与森林图坐标按表 1、表 9 数值换算。
