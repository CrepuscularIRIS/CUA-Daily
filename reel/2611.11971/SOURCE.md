# SOURCE — 2611.11971 Harness Matters: Measuring and Dissecting Security Resilience in Web Agents

- 论文：arXiv **2611.11971v1**（2026-11-09 06:53 UTC 提交；2026-11-10 查 export.arxiv.org/api：id 2611.11971v1、published = updated = 2026-11-09，标题与作者（Wu, Chen, Dong, Hong, Pan, Dai, Liu, Yang；复旦等）与 corpus.jsonl 和本地缓存头一致）。**身份核对**：L2 备注“ID 为 2026-11 而当前日期 2026-11-10，需核对发布时间/版本来源”——已确认是真实 arXiv v1，发布在 run 日期前一天，不是伪造或误配的 ID。HTML 附录 E 为 IEEE S&P 2027 程序委员会元审稿（作者附上的录用材料），只作参考，不作为结论依据
- 阅读材料：本地 `research/fulltext/2611.11971.txt`（裁剪 core）+ arxiv.org/html/2611.11971v1 全文（§I–VIII、附录 A–E、表 I–XI）；图 3 `naive_asr.svg`、图 4 `dsr_tcr.svg` 另行下载渲染，读取柱顶标注；数学式从 HTML alttext 还原（ASR / DSR / TCR 定义，表 VII 的 p 值，κ）。转换稿与图在 /tmp/sel14，不提交。未运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-40.jsonl`（L2，supersedes inc-l1-87#2611.11971；P3 confirmed to_l3；q3 judgment；F1,F2；卡 environmental_injection_attacks、injection_defense_isolation、online_evaluation_methodology）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-014.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG/JS）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome（Playwright，`--disable-lcd-text`）渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 同一 GPT-4o：Agent-E DSR 83.79%，Skyvern 2.0 42.89%（差 40.90 点） | 表 VI；§IV-B2 第 1 段 |
| 副标题 | 6 外壳 × 7 模型；攻击任务 160 / 158 / 187；配对可用性任务；网页端埋点 | §III-B1、§III-B2、§III-C；§IV-A1–A2 |
| 01 判卷规则 | AS / DS / 能力失败三类标签 | §III-D2 |
| 01 我们核对 | DSR = 1 − ASR；TCR =（AS+DS）/ 全部 | §III-D3 式（HTML alttext）；表 IV 与表 VI 合计列逐行相加 = 100（**我们核对**） |
| 01 判官校验 | 672 / 6,720；99.26%；99.55% | §III-D1 |
| 02 热力图 | 6×7 DSR 及合计 | 表 VI（显示保留 1 位小数） |
| 02 注 | Claude-Opus-4.5 总体 77.10、Agent-E 内 75.19 < GPT-4o 83.79、Qwen3-235B 82.16 | §IV-B2；表 VI |
| 02 来源行 | 温度 0；一次执行；2 模型 × 6 外壳重跑三次，平均标准差 1.73 点 | §IV-A3 |
| 03 GLMM | χ² 331.17（df 5，p=1.97×10⁻⁶⁹）、437.63（df 6，p=2.25×10⁻⁹¹）、299.81（df 30，p=2.88×10⁻⁴⁶）；敏感性 p<10⁻³⁹ | 表 VII；§IV-B2 |
| 03 注 | “模型 χ² 大于外壳”“共同决定而非外壳更重要” | **我们的阅读**，基于表 VII |
| 04 散点 | TCR / DSR：SeeAct 50.33/57.69，BU 文本 75.77/66.16，BU 视觉 84.46/65.92，Agent-E 61.33/79.76，Skyvern 1.0 71.51/78.20，Skyvern 2.0 85.25/58.01 | 图 4 柱顶标注；§IV-B2 “Capability-Security Decoupling” |
| 05 哑铃 | 朴素 / 其他 ASR：SeeAct 50.00/49.37、50.59/55.13；BU 文本 31.19/35.89、41.27/36.30；BU 视觉 37.40/40.95、34.91/36.42；Agent-E 22.77/25.46、22.48/23.11；Skyvern 1.0 3.57/8.59、16.13/25.59；Skyvern 2.0 35.25/40.38、39.60/43.47 | 图 3 标注；§IV-B1。“12 组中 2 组朴素更高”为**我们计数** |
| 06 条件防御率 | 表 IX、表 X 全部单元与组件名 | 表 IX、X；组件归属见表 III |
| 06 注 | 300 实例、97.33%、κ=0.96、98.67% | §V-A1 Step 2 |
| 07 消融 | 75.61→53.85；73.91→43.48；92.86→69.77；56.94→50.70；70.73→54.05；19.35→43.59；GPT-4o、各 100 题 | §V-B 首段、§V-B1、§V-B2 |
| 07 注 | 受控 vs 观察的区分 | 附录 E-D 第 2 条；“抽样基线与全量不同”为**我们比对**（82.71 vs 75.61） |
| 08 模型 × 攻击面 | 表 V 全部；商用 Claude CU 9.59/16.67/22.12（总 16.85）、Gemini CU 1.45/14.29/25.51（总 15.14） | 表 IV、表 V；§IV-B1 |
| 限制 1–2、4 | 受控页、改编来源；单次运行 | §III-B1、§VI-C、§IV-A3 |
| 限制 3 | 网页侧可用性任务“明确要求点下载”导致保守外壳被剔出分母 | §III-B2 例句；推论为**我们的阅读** |
| 怎么读 | 四条设计建议；哪些有消融 | §VI-B；§V-B |

## 我们的判断（非原文）

- DSR 与 ASR 互补、两表是同一量；“模型 χ² 更大”；“12 组中 2 组朴素更高”；保守外壳被剔出分母的偏差。
- 热力图配色与描边、散点、哑铃、阶段格均按原文数值重绘，不是原图。
