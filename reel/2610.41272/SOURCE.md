# SOURCE — 2610.41272 ANGLER: Verifier-Grounded Benchmarking with an Adaptive Attacker for Web Agents

- 论文：arXiv **2610.41272v1**（2026-10-30；2026-11-03 查 arxiv.org/abs 仍只有 v1）。基准名 REEF，攻击框架名 ANGLER
- 阅读材料：本地 `research/fulltext/2610.41272.txt`（文件头 v1，裁剪 core，§5 截断、无附录）；按钉定版本补读了 arxiv.org/html/2610.41272v1 全文 §1–7 与 App. A–B（A.1–A.2、B.1–B.6）。本文没有局限性一节。转换稿放在 /tmp/sel8，不提交。没有下载或运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-11.jsonl`（L2，supersedes inc-l1-12#2610.41272；P3 confirmed，q3 judgment，F2/F4；卡 main/environmental_injection_attacks；子卡 C29、C30、C33）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-008.md` 第 1 节
- 画报源：`poster.html`（由本地生成脚本把四张 SVG 填入模板后得到的静态文件，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 同任务、每站 100 次 rollout；8 骨干平均 ASR 15.24% → 20.36% | 摘要；§6.2 “Main Results”；Tab.3 Avg. 行 |
| 标题 | ASR = 恶意目标终止时仍成立 | §3.2 “Adversarial Goal”；§4.3 “Verifier-Grounded Measurement” |
| 副标题 | 9 个 AutoWebWorld 站点、5 个领域、合成用户与内容、8,316 个可执行用例、326 个恶意实例 | §4.1；Fig.1 说明；App. A.2；§7 |
| 副标题 | 5 种攻击：DPI（追加到用户指令）；IPI / 弹窗 / 干扰 / 广告 | §3.2 “Capabilities”；§4.2；App. A.1 |
| 副标题 | V_a 在重置态须为假；不靠自述与 LLM 评审 | §4.3 |
| 01 ① 调度 | 覆盖阶段配额；自适应阶段任务模板均匀、攻击层级与结果无关 | §5.1 |
| 01 ② 种子 | 四类经验记录与近失定义；低证据/精化两种权重 | §5.2；Tab.2；App. B.2 Tab.9 |
| 01 ③ 变异 | Qwen3.5-9B；按失败阶段路由；白名单字段（显示时机 1–3、颜色/字号/字体） | §5.2 “Candidate Generation”；§6.1；App. B.3–B.4 Tab.10 |
| 01 ④ 选择 | 用户级 logistic Thompson 采样；环境级门控×完成 | §5.3 式 (5)(6) |
| 01 ⑤ 执行 | VisualWebArena 脚手架、多模态 a11y 树+截图、10 种按 id 动作、只在本站导航 | §3.1；App. B.1 Tab.8 |
| 01 ⑥ 验证器 | V_u / V_a / V_r 与 CTA | §4.3 式 (3) |
| 01 NA 对照 | 同任务上下文、编译器过滤后均匀随机；另跑无攻击 | §6.1 “Evaluation Protocol” |
| 02 瀑布 | 各骨干 NA→ANGLER 平均与增益 | Tab.3 Avg. 行；**贡献 = 增益/8，排序与 39%、去掉 GPT-4o 后 +3.6 为我们计算** |
| 02 “8 个骨干、9 个网站平均都上升” | 作者原文 | §6.2 |
| 02 点阵 | 72 格 ANGLER−NA；52 升 / 18 降 / 2 平 | Tab.3 逐格；**计数为我们计算** |
| 02 来源注 | 预算 50 时 713 vs 545 次成功 | §6.2 “Discovery Efficiency”；Fig.3 |
| 03 漏斗 | IPI 25.8/15.9、弹窗 52.4/17.1、干扰 47.0/17.8、广告 34.6/13.9（CTA/ASR）；DPI ASR 31.5 | App. B.5 Tab.11 Aggregate 行；§6.5 |
| 03 说明 | 两阶段投放；作者认为 CTA 是曝光指标 | §4.2 “Environment-level”；§6.5 “Engagement May Not Imply…” |
| 04 表 | 8 骨干 × 5 种送达的 ASR/CTA | App. B.5 Tab.11（逐格照录） |
| 04 说明 | Sol、Sonnet 5.5 环境级 CTA 不超过 5.4% / 2.3%，DPI 仍有三成以上做成 | §6.5；Tab.11。正文与表的 Sonnet 5.5 DPI 值不一致，见下“出入” |
| 04 “我们的阅读” | DPI 威胁模型更强，两列不可直接比 | §3.2 两类能力定义；**判断为我们的** |
| 05 BSR | 无攻击 61.9、NA 46.4、ANGLER 44.4；Sonnet 4.5 44.9→46.8、Qwen3-VL 50.2→51.9 | §6.2 “Attack-Free…”；Tab.4 |
| 06 噪声条 | Qwen3-VL NA 11.6（Tab.3）；三次运行 14.6/12.1/11.0（12.6±1.8）；去 bandit 10.3、去经验 11.3、去变异 12.0；Full 14.6/41.1/51.9 | Tab.3；§6.3 Tab.5；§6.4 Tab.6 |
| 06 “我们的阅读” | Full 行与 Run 1 相同、消融差异落在三次运行波动内 | **我们对 Tab.5 与 Tab.6 的比对**；作者在 §6.4 称三个组件都有贡献 |
| 限制 1 | 合成网站与账户 | §4.1；Ethics |
| 限制 2 | 每骨干每站 100 次；只 Qwen3-VL 重复 | §6.2；§6.3 |
| 限制 3 | 运行时不含候选生成 | App. B.6 |
| 限制 4 | 验证器只有构建期人工审计 | §4.2 “Quality Control” |
| 限制 5 | CTA 只记注册诱饵的交互事件 | §4.3 |
| 限制 6 | ASR 是 rollout 命中率；无局限性一节 | §6.1 指标定义；全文结构 |
| 限制 7 | MUZZLE、SIR、AgentVigil 已有自适应，多为单一注入类型 | Tab.1；§2 |

## 原文内部出入（画报取表值）

- §6.5 写 “direct prompt injection still achieves ASRs of 32.5% and 32.9% against these two models”，App. B.5 Tab.11 中 Claude Sonnet 5.5 的 DPI 为 39.8。画报 04 表照录 Tab.11，文字只写“三成以上”，两者都成立。

## 示意与自绘

- 01 流程图为我们按 §5 重画的示意，不是原文 Fig.2。
- 02、03、06 的图形为我们按原文表格数值绘制；原文 Fig.3/Fig.4 的曲线没有使用。
