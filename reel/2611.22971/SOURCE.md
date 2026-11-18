# SEAM (2611.22971) — SOURCE

论文：*SEAM: Computer-Use Agents Know the Harm Between Screens, and Commit It Anyway*，arXiv 2611.22971v1，2026-11-17。
缓存全文：`research/fulltext/2611.22971.txt`（FULLTEXT: html）。核对于 2026-11-18（本仓 selection-018，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 标题句"指令合法、每一页单独看都无害、只有组合才有危害" | harm(I)=false, ∀i harm(o_i)=false, harm(组合)=true | §1，§3.1 式(1) |
| 17 配置×11 模型 | "17 configurations of 11 models" | §1，§4.1 |
| R 危害执行 17.5–91.6% | "carry the harm out in 17.5–91.6% of R runs" | §1，§4 |
| E_u 1.1–22.0% | "against 1.1–22.0% of E_u runs" | §1，§4 |
| 通用开源与旗舰 vs 专有 | 专有 ≤3.6%，三个专有配置靠搁置良性工作 | §1（"Proprietary models are markedly more cautious"），§4 |
| 双屏示意（指令+客户记录+服务页） | Mei 怀孕 22 周医嘱 ≤38℃ / 温泉 40℃ 例子 | §1 开头，Figure 1 |
| 指令六种改写 | "six paraphrases" | §3.3 |
| 五变体 R/B/E_u/E/E_q，环境字节一致 | "byte-identical across the four harmful variants" | §1 性质(2)，§3.3 |
| B 改一个对象事实 40→32℃ | "changes one object fact (40 °C → 32 °C)" | §3.3 |
| 150 规则×27 危害族×8 推理操作×49 域 | "150 rules across 27 harm families, 8 reasoning operations and 49 application domains" | §1 |
| 600 场景×5 变体=3,000 实例 | "instantiated as 600 scenarios × 5 variants"，"3,000 instances" | §1 |
| 6 个 E 未过门禁保留、影响 ≤0.7 点 | "6 E instances … At most 3 of 450 on-path E instances per configuration are affected (≤0.7 points)" | §3.5 Construction gates |
| OSWorld VM、步预算 40、中位 11–12 步 | "The step budget is 40 … the measured median is 11–12 steps" | §4.1 Budget and repetitions |
| 决定性页面打开 ≥99.3% | "agents open the decisive page in at least 99.3% of required-path runs" | §1 发现(i)，§5 |
| DS-1017 先陈述冲突再确认 81–87%；其他推理模型 50–69%；LLM judge | "81–87% of DeepSeek-1017's harmful runs and 50–69% for the other reasoning models we judged" | §1 发现(ii) |
| 良性孪生完成 91.8–99.6% | "completing 91.8–99.6% of benign twins" | §1，§4 |
| 单屏区分度 0.00、0/600 p<.05；全集 +0.88~+0.92 | DeepSeek-V4.1-Flash(high) 行为学验证 | §3.5，Appendix D |
| 无思考单屏 ≤0.06 | "Without thinking, single screens separate the variants by at most 0.06" | §3.5 |
| 标注员单屏误标 2/144、3/144 | "annotators flag 2 of 144 harmful-only and 3 of 144 benign-only pages" | §3.5，Appendix J |
| 服务端日志程序化判分、无 LLM judge | "read from the service's own server log … without an LLM judge" | §1 性质(3)，§3.4 |
| 温度 0.2 单次运行、DS-V4.1 复跑差 ≤2 点 | "Each task variant is run once per configuration (temperature 0.2 …)"；"a second run of DS-V4.1 reproduces its rates within 2 points" | §4.1 |
| 自建应用+生成规则、英文 | Limitations | §6 |
| 一句提示防御只关闭部分缺口 | "a one-sentence prompt defense closes only part of the gap" | §6 结论句 |
| 通道依赖（同一句话在指令里比屏幕上更能拦） | "the same sentence stops the agent far more often as part of the user's instruction than read on screen" | §1 发现(iii) |

## 编辑收窄

- "通用开源与旗舰代理"按原文 "general-purpose open-weight and flagship agents" 呈现，专有模型单列，不混排。
- 推理通道分析（81–87% 等）在画报上标注 LLM judge 与"书面推理未必驱动动作"，同原文 §6 限制句。
- 画报不外推部署安全性；专有模型谨慎含"3/5 靠搁置良性工作"的代价说明。
