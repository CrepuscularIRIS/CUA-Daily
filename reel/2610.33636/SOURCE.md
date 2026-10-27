# SOURCE — 2610.33636 Build or Adopt? Custom-Built vs. General-Purpose LLM Agent Harnesses for Automotive GUI Testing

- 论文：arXiv **2610.33636v1**（2026-10-24）
- 阅读材料：本地 `research/fulltext/2610.33636.txt`（文件头 v1，core，有 4 处 [...] 裁剪）；按钉定版本补读了 arxiv.org/html/2610.33636v1 的全文（本文没有附录）。Fig. 2 是 SVG（`2610.33636v1/effectiveness.svg`），渲染后读出柱顶数值。转换稿和渲染图放在 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-04.jsonl`（L2，P3 confirmed，q3 judgment，F1/F0；卡 agent_loop_context_control、online_evaluation_methodology；子卡 C20/C25）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-005.md` 第 1 节
- 画报源：`poster.html`（单文件，内联 CSS/SVG/JS 绘图）；`poster.png`（1400×2000）和 `poster.pdf`（1 页）由 headless Chrome 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题 | 车机成功率 55–61%；同模型 B−A −4.5 到 −0.8，p≥0.17 | §IV-B “Volvo IVI benchmark” |
| 副标题 | Maps 上 B 高 9–28 点；工具正确率更低 | §IV-B；Table I |
| 副标题 | 同模型车机推理费 2.6–10.7× | §IV-D RQ3 findings；Table II（0.92/0.35 = 2.6；4.97/0.46 = 10.8，原文写 10.7） |
| 剖面 · A | 固定四步 ReAct（观察、推理+清单、校验、执行），每轮一个动作；每步重建 prompt；历史 = 步骤日志 + 清单；截图只留上一个动作前后 | §III-A |
| 剖面 · B | 通用循环；上下文累积并由 harness 压缩；一份通用指令模板；动作工具返回动作前后层级 | §III-B |
| 剖面 · 地基 | 共享工具层（设备工具 + 子代理），A 本地调用，B 经 MCP；uiautomator2 → ADB | §III-C；Fig. 1 |
| 剖面 · 维护分工 | A 全栈自维护；B 循环由厂商维护，Volvo 维护模板、MCP、工具 | §III-D |
| 分户账 · 柱 | IVI：GPT-5.1 A 59；GPT-5.4 A 61/OC 57；Sonnet A 58/CC 58/OC 55。Booking：10；27/31；29/42/31。Maps：53；53/80；68/84/87；Opus 73/83/84 | Fig. 2（SVG 读数，整数百分比） |
| 分户账 · 题量与轮数 | IVI 66 题 × 2 轮；AMEX 56 题（Maps 40、Booking 16）× 3 轮 | §IV-A2、§IV-A3 |
| 分户账 · 显著性 | Maps GPT-5.4 +28、Sonnet +17~19（p≤0.01）；Opus +9~11（p=0.04/0.06）；Booking 不显著；里程碑 72–78% vs 56–59% | §IV-B |
| 分户账 · flaky | IVI A 0.02–0.03 / B 0.05–0.09；Booking A 0.06–0.38 / B 0.19–0.50；Maps A 0.35–0.48 / B 0.13–0.25 | Table I |
| 分户账 · 费用 | 各场景每题美元区间 | Table II |
| 散点 | 21 个配置的（工具正确率，故障恢复） | Table I |
| 散点注 | 作者把恢复优势归因于累积上下文 | §IV-B “Recovery rather than precision” |
| 总账 | 0.5 → 0.1 FTE；每晚 60 个车机用例；多出的推理费 = 0.06–0.39 FTE；月总成本低 3–66%；OpenCode 省得最多，Claude Code 最少 | §VI “Trading engineering effort for inference cost” |
| 总账 | 工程投入由团队经理估计 | §V-A2 末句 |
| 总账 | B 同模型每题平均快 3–57 s | §IV-D “Latency” |
| 总账 | 生产配置 GPT-5.1 每题 $0.13 | Table II；§IV-D |
| 访谈 F1–F4 | 生态带来的技术债；维护转向集成；失去上下文控制、成本评分最差；可见性与守流程 | §V-B F1–F4 |
| 限制 | judge 为 GPT-5.6-sol；Booking 一轮人工核对，无歧义的 88% 全部一致；κ=0.85 | §IV-A3 |
| 限制 | 换应用同时换了用例风格和设备 | §IV-C “Application change” |
| 限制 | D2–D4 是作者 | §VII Internal validity |

## 示意与重绘

- 剖面图按 §III 和 Fig. 1 自行绘制，标“示意”。
- 柱图、散点图和总账条按原文表图数字重绘，不是原文图片。
