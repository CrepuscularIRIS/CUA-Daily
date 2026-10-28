# SOURCE — 2610.34735 iPrefBench: A User-Centric Benchmark for Personalized Mobile Use Agents

- 论文：arXiv **2610.34735v1**（2026-10-26）
- 阅读材料：本地 `research/fulltext/2610.34735.txt`（文件头 v1，裁剪 core，未含附录）；按钉定版本补读了 arxiv.org/html/2610.34735v1 的正文 §1–5 与附录 A–G（G 为提示词，只看了结构）。转换稿放在 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-05.jsonl`（L2，P3 confirmed，q3 judgment，F4/F2；卡 main/agent_initiated_user_interaction；子卡 R02）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-006.md` 第 1 节
- 画报源：`poster.html`（单文件，内联 CSS/SVG/JS 绘图）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome 经 Playwright 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | Claude Opus 5 动作完成 91.6、整题成功 47.7%；只能问的信息 recall 最高 44.2%（正文 §1 写作 44.3%，画报取表值并写“44%”） | §4 Tab.1；§1 |
| 副标题 | 26 个 mock app、iOSWorld 模拟器；3,051 条活动事件；ask_user | §3.2；App. B.1、B.2；Tab.D.1 |
| 副标题 | 每个省略信息由构造规定为可推断或只能问 | §3.1、§3.3 |
| 副标题 | 130 任务、7 个模型同一 harness；动作完成 77.5–91.6、SR 26.2–47.7 | §4.1；§4.2；Tab.1 |
| 副标题、01 | 平均每题 0.89 个只能问、1.98 个可推断；每题 ask_user 0.08–0.35 次 | §3.5；Tab.D.1；§4.2 |
| 01 示意 | “book me my usual restaurant for tomorrow” 的三个省略值及来源 | §1；§3.3 Task Design；**示意转述** |
| 01 | 只能问的值尽量不同于 app 默认值 | §3.3；App. D.1 Stage 2 |
| 01 | 评分三层与整题成功定义；recall / precision 定义 | §3.4；App. E.2–E.3 |
| 01 | 扰动题 11/10/13 | §3.5；Tab.D.1 |
| 01 | 两轮人工审核；证据不足时改写种子数据 | §3.3；App. D.1 |
| 01 | 用户画像 13 维 92 条，对代理隐藏；模拟用户只答所问 | §3.2；App. C.2、C.3 |
| 02 左 | 7 个模型的 Action / Infer / Ask / SR | Tab.1 |
| 02 左注 | 动作与个性化分按任务宏平均，SR 按任务计 | §3.4；App. E.2 |
| 02 右 | 7 个模型的 recall / precision；Claude Sonnet 5 与 Qwen3.8-Flash-Next 均为 25.7 / 60.4 | Tab.1 |
| 02 右 | 执行前澄清：Sonnet 39.2→53.8、recall 25.7→85.0、precision 60.4→42.5、#Ask 0.24→1.37；Qwen3.8-27B 26.2→35.4、21.2→69.0、70.6→60.9、0.21→0.84 | §4.4 Tab.2 |
| 失败象限 | 四种错误类型的定义与例子（打车 5 人、往返默认日期、旧晨练习惯、吧台位） | §4.3；Fig.F.1–F.4 说明；**示意转述** |
| 失败象限注 | Sonnet 79、Qwen 96 个失败任务；89% / 84% 含个性化错误；Qwen “should I ask?” 后自说自话去猜 | §4.3；App. F.2 |
| 多给历史 | Qwen3.8-27B 推断类个性化 35%→63%（前 50 条），全量不再提高；询问类几乎不动；recall 33.6→21.2 | §4.4 “Effect of User History Exposure”；Fig.4 |
| 多给历史 | 首选项缺货扰动下提问 2.3 倍、询问类个性化对每个代理提高 | §4.2；Fig.2 |
| 校验 | 评分条目 95.7% κ0.89；整题 97.0% κ0.94；recall 95.2% κ0.90；多余提问 93.9% κ0.82；模拟用户 86/89=96.6%；Gemini 3.7 Flash 整题 96.4% κ0.92 | §4.5；App. C.4；App. E.4 |
| 限制 | 单一用户 Jordan Avery；模拟用户与评分器均为 Claude Sonnet 5 | App. C；§4.1；App. C.3 |
| 限制 | 专用 GUI 代理未纳入 | §4.1；App. F.1 |
| 我们的阅读 | 2503.19537 的 precision 0.08–0.19 | `reel/2503.19537/SOURCE.md`（本仓首期） |

## 未上画报的原文内容及原因

- 消息格式质量（App. E.1 Tab.E.1，几乎满分）：说明问题在“是否问”而不在“怎么问”，画报文字已涵盖，未单列。
- 个性化总分（Tab.1 Overall 列）：画报拆成推断类与询问类两项，没有再列总分。
- Fig.3 四种错误类型的具体比例：正文未给数值，画报只列类型与例子。

## 示意与重绘

- 01 分拣图与失败象限中的例子：按原文文字转述，标“示意”。
- 四刻度图、P–R 平面、校验条：用作者表格数字重绘，不是原文图片。
