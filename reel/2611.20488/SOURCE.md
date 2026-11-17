# EVIDENT — 来源与展示口径

- 论文：*EVIDENT: Evaluating Evidence Grounding in GUI Agents*，2611.20488v1，2026-11-16。
- 原文：[版本页](https://arxiv.org/abs/2611.20488v1) / [版本化 HTML](https://arxiv.org/html/2611.20488v1)。已读正文§§1–6、Limitations与附录A–K，包含标注原则、裁判提示词、人工验证和误判案例。未做export API最新版审计。
- 阅读/制作：2026-11-17；实际执行模型gpt-6-astra（fable槽）。run `gui-rolling-20261023-01`，`problem-core-v1.1`，selection-017。
- L2来源：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-52.jsonl#2611.20488`，替代inc-l1-98。P3 / confirmed / judgment / F2,F4。没有因其为诊断/benchmark而排除，也不把档位当作审稿结论。

## 问题与贡献界限

成功答案未必有完整的观测证据；EVIDENT以轨迹证据覆盖和核心说法支持关系诊断这一缺口。支持“可审计的缺证”，不支持推断模型内部因果上依赖了哪些信息。TSR、ESR、GSR的嵌套来自指标定义；经验贡献是轨迹中的实际差距、metadata一致性与人工审计，而非嵌套不等式本身。

## 画报映射

| 展示项 | 定位 | 解释 |
|---|---|---|
| 220任务、英语70/韩语150、八领域 | §3与任务构造附录 | 不同语言对应不同网站，不是受控语言迁移/比较 |
| 英语Gemini87.14 / 70.00 / 55.71% | Table2 | 依次TSR / ESR / GSR；同一70题集合。17.14和14.29个百分点为编辑相减，不是错误类别独立发生率 |
| TSR=mean(s)，ESR=mean(s·e)，GSR=mean(s·e·g) | 评价指标定义 | s成功、e必要证据覆盖、g核心答案有据；乘积筛选保证GSR≤ESR≤TSR。未将数学必然写成新发现 |
| 48/50独立重写等价；49/50标注原则通过 | §3.3，App.D / Table10 | 随机50任务；两人独立重写，第三人审查等价；另审标注原则。不是全体任务都经逐题人工认证 |
| 115/126=91.27%，κ=.864 | App.K / Table19 | Qwen裁判与人工四分类精确一致，分层抽样126条。不是每类precision、recall或NPV |
| 被标记Gemini轨迹25/27获三人一致确认 | §5.2，App.G | 三人各自审查27条已被Qwen标为Hallucinated Success的完成轨迹；约92.6%仅是此定向子集，不能估计未标记漏检或其他agent的可靠性 |
| 提取截图证据→对照checks/claims→支持关系审查 | §4，裁判附录提示词 | 思考/动作日志不能代替网页内容证据；保存截图复判，不从更新页面补证。流程为编辑自绘 |
| Qwen3-VL-235B主裁判，2026年5月执行 | 实验设置与App.A.2 | Gemini实际API名gemini-3-flash-preview；另两agent为gpt-5.4、claude-opus-4-7；同MolmoWeb式管线，最多50交互步。没有换成当前模型 |

## 完整附录补充的边界

- Table19另两裁判：GPT111/126=88.10%、κ=.817；Gemini116/126=92.06%、κ=.871。总体一致度不替代各类别可靠性。
- Appendix I含真阳/假阳/假阴分歧：证据提取会遗漏图片细节，主裁判也会接受无根据说法；搜索结果页面能否满足任务要求亦有分歧。严格检查可能误拒合理常识推断。
- 不是永久网站快照；截图可复判不表示所有agent都在同一网站状态运行。主卡C24的live-site漂移仍需保留。
- Appendix C.5提到1299有效评价，相对6×220名义1320条的排除口径未完全展开。外部45-task集合的若干百分比亦不宜在分母未澄清时做画报主锚点。本画报不使用这两组聚合数字。
- L2说明core缓存缺附录/时间细节，不等于断言原文没报告。补读A–K后增补执行日期与人工证据，不构成推翻L2的correction。

## 输出与复现状态

所有图形为自绘信息图，没有拷贝或裁剪原图；未视觉审计原论文图像中的额外数值。交付poster.png、单页poster.pdf、poster.html、SOURCE.md、QA.md。HTML与assets字体沿用现有本地忽略规则。

仅参考paper2assets的溯源原则，自定义HTML / Chrome渲染，未声称完整paper2poster/PPTX流程。原文全文保持本地，没有运行论文代码、复现实验或联系作者。裁判提示词作为论文数据阅读，未作为本会话指令执行。
