# SOURCE — 2503.19537 Agent-Initiated Interaction in Phone UI Automation

- 论文:Agent-Initiated Interaction in Phone UI Automation,arXiv **2503.19537v1**(2025-03-25;WWW Companion ’25,DOI 10.1145/3701716.3717526)
- 阅读材料:本地 `research/fulltext/2503.19537.txt`(HTML 全文缓存,但 §4.4 后半、§4.5、§5、附录被截断);已补读 arxiv.org/html/2503.19537v1(含 §4.4–§5、脚注 3、附录 A/B),缓存在 /tmp,不提交
- 初筛记录:`research/scoring/runs/gui-pc11-20261022-01/batches/l09.jsonl`(L2,P3 confirmed,capability,F2/F4,卡 main/agent_initiated_user_interaction);入选见 `selection.md` 第 1 节 #9
- run:gui-pc11-20261022-01;规则 problem-core-v1.1

## 数字与断言映射

| 画报内容 | 原文位置 |
|---|---|
| 任务:每步判断是否需联系用户 + 生成消息;下一动作需要时才问;排除导航求助、策略性确认、建议替代任务 | §3 |
| 在 AndroidControl 演示上逐步标注;消息 + 1–5 必要性分 | §4、§4.1、Table 1 |
| 截断在首次该问处;每个 session 至多一次交互;排除开放式任务 | §4.2 Data Selection |
| 2 名专业标注员;200 条重标;κ=0.64;必要性分 Pearson 0.78 | §4.2、§4.3 |
| 772 episodes、3,605 步、250+ app;27.5% episode 含交互;约 6% 的步需交互;70% test / 30% val | §4.4 |
| 正例 5.5%;每步都问 F1=0.1;按类分布随机 F1=0.055 | §5 脚注 3 |
| 交互类型:更多信息 89% / 确认 7% / 不可行 4%(100 条抽样) | §4.4 Table 2(未上画报,仅核对“缺信息/确认/不可行”三类) |
| 所有基线为 Gemini 1.5;输入 文本(精简无障碍树)/截图/两者;1 阶段 vs 2 阶段(先列可行动作再判断);零样本/少样本 | §5 |
| audit 组件过滤假阳性,无显著改善 | §5 |
| 12 个配置的 P/R/F1;precision 0.08–0.19,recall 0.30–0.84;最高 F1 0.25(text 2-stage FS 与 scrn+text 2-stage FS) | §6 Table 3 |
| 作者解释:过于死守指令,产生多余确认与导航提问;few-shot / 2 阶段提 P 降 R;推测需微调 | §6 正文、§7 |
| 消息等价率(TP 上):text 74%/70.4%,scrn 91.3%/80.4%,scrn+text 88.3%/74.7%(人工/GPT-4o) | §6 Table 4 |
| 假阳性构成:多余确认 52%(text)/51%(text+screen);导航提问 31%(text+screen);建议后续任务 21%(text) | 附录 A |
| 漏问主因屏幕理解(如需滚动);分歧中 15%(text+screen)/26%(text)可视为可接受/主观,多见于漏问 | 附录 A |
| 示例指令 “Identify a plant using a picture taken today” 与消息 “Which picture would you like to use?” | Table 1 必要性 5 级 |
| 限制:单轮、不含用户回复与任务完成;数据量不足以训练 | §4.5、Limitations |

## 推算量(画报标“由 P/R 推算”)

论文只报告 P/R/F1,不报告计数。按“每 100 个真正该问的步”归一:问对 = recall×100,开口 = recall/precision×100,多余开口 = 开口 − 问对。

- 散点 12 点:如 text 1-stage ZS → 开口 1050 / 问对 84;scrn+text 2-stage FS → 388 / 62;scrn 2-stage FS → 158 / 30。
- 矩阵(scrn+text 2-stage FS):TP 62、FN 38、FP ≈326、TN ≈1,390(TN 按脚注 3 的 5.5% 基率:不需问的步 ≈1,718;若按 §4.4 的 6% 则 ≈1,241)。
- “每步都问”点:开口 100/0.055 ≈ 1,818,P≈0.055,F1≈0.10(与脚注 3 一致)。
- “每问 5–12.5 次问对 1 次”= 1/0.19 与 1/0.08;“每 100 次开口约 92 次不该问”= 1 − 0.08。
- 已核 Table 3 内部一致:由 P/R 计算的 F1 与表中 F1 在两位小数舍入内全部吻合。
- “88.3% → 16%”:16% 即该配置 precision 0.16,两者分母不同(前者为 TP,后者为全部开口)。

## 自绘与示意

- 顶部 episode 截断条:自绘示意,指令与消息文字取自 Table 1,手机画面不是原文截图。
- 失误矩阵与散点:按上述推算自绘,非原论文图(原文无此类图)。
- 未使用任何原论文图片。

## 作者结果 / 阅读判断的区分

- 标“作者结果”的数字与解释来自原文。
- 标“由 P/R 推算”的为核对者对原表数字的算术换算。
- 标“阅读判断”的注解带框架(高 recall、TP 上的消息正确率、相对最高 F1 都掩盖了低 precision)为核对者读法;其中“每步都问”对照来自作者脚注。
- 未运行任何代码,不构成复现。
