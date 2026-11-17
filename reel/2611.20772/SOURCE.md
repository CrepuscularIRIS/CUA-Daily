# DroidPrefill — 来源与展示口径

- 论文：*Building Fully On-Device GUI Agents with Mobile NPUs*，2611.20772v1，2026-11-16。
- 原文：[版本页](https://arxiv.org/abs/2611.20772v1) / [版本化HTML](https://arxiv.org/html/2611.20772v1)。读完整正文§§1–7、Tables1–2与limitations；该HTML没有独立附录。未做export API最新版审计。
- 阅读/制作：2026-11-17；实际执行gpt-6-astra（fable槽）。run `gui-rolling-20261023-01`，`problem-core-v1.1`，selection-017。
- L2：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-52.jsonl#2611.20772`，替代inc-l1-98。P3 / confirmed / capability / F0,F5。保持限定的判断，不改L1/L2。

## 确认的问题

商用手机NPU上，prefill/decode吞吐不对称和静态上下文profile给GUI决策带来实际瓶颈。用有限候选、候选相关UI压缩、有界状态账本与短输出接口重塑工作负载，在A11y可见界面和测试硬件上有价值。不是候选动作或历史压缩本身首次出现；也不证明困难任务、所有手机或纯视觉界面已解决。

## 数字与机制来源

| 画报项 | 原文定位 | 口径 |
|---|---|---|
| Xiaomi17、Snapdragon8 Elite Gen5、Qwen3-4B-Instruct-2507 | §4.1 | 同released checkpoint无任务特调；QAIRT/QNN HTP W4A16与GenieX llama.cpp Q4_0都运行Hexagon NPU，不是NPU与CPU对比 |
| QAIRT prefill1473 / decode17.9 tok/s；82.3倍 | §2.2 / Figure2正文解释 | 128-token测量点；1473÷17.9≈82.3为编辑计算，非任意请求长度恒定吞吐，非整步加速 |
| A11y→有限候选→CGUC+BSL→固定前缀/动态后缀→派发或SDR | §3 | 单token标签映射当前node/action payload；有界状态账本包含进度/转移/无效动作，无额外LLM摘要；Type/Speak值另行填充；自绘机制 |
| QAIRT Easy10.7→23.0%；Medium/Hard0.0→3.6% | Table1 | 各runtime内T3A+→DroidPrefill；A11y-only，不与视觉基线混同 |
| llama.cpp Easy13.1→37.7%；Medium/Hard5.5→7.3% | Table1 | Easy增加24.6个百分点，而非相对24.6%；仅简单任务有较大改善 |
| llama.cpp34.8→5.2秒/步 | Table1 | 整个任务集按交互步微平均推理关键路径，不是Easy-only，也非含观察/执行/传输的整步wall-clock。全系统行不能充作独立SPAD在线复跑 |
| 24.7% fast-path覆盖，95.5%与SDR一致 | §4.4 | 在固定轨迹上回放；95.5%不是动作真值准确率；不一致均在原失败轨迹中，成功轨迹保持 |
| 5.6→4.4秒、SR37.7%不变 | Table2及§4.4 | Easy的trajectory-preserving replay投影，不是独立在线fast-path实验。输出tokens32.4→22.2亦同此口径；画报用单独虚线框显著隔开 |
| logit margin≥0.6；排除Complete/destructive/answer-returning | §4.4 | eligible动作包括OpenApp/Wait/Type/Tap；不是任意高置信动作都可提前派发；同KV缓存继续有界SDR |
| 主机管emulator/reset/execution/checker，手机做完整决策 | §4.1 | 无主机规划或远程推理，但不是整个AndroidWorld原生在手机运行 |

## 不得混用的证据

1. 主系统结果、Easy消融、SPAD回放各有不同汇总口径。派发后的后台继续计算不计入关键路径；不能写等比例总计算或节能。
2. §4.5另有物理手机RealMobile代表性任务的5.0秒端到端步时延；缺基准规模成功率/样本细节，不拿它替换Table1或背书全流程普适性。
3. Table2的CGUC替换使Easy37.7→31.1%，BSL换近期动作历史使37.7→21.3%；说明表示/状态不只是在减少token。未建立被删目标覆盖率、长流程遗忘或陈旧结构专项安全结论。
4. 512×512输入限制视觉基线，不能据此宣称视觉无用。A11y未暴露的canvas/自绘控件仍缺覆盖；单硬件家族、手调阈值、未见长期热稳态/能耗与充分重复运行。

## L2引用定位勘误（非判断退回）

`inc-l2-52#2611.20772 facts[1].loc`合并写“§4.1–4.4，表2及SPAD Analysis”。其中24.2→4.6秒、34.8→5.2秒和13.1→37.7%的全系统比较实际在**Table1**；SPAD分析与Easy消融才对应§4.4 / Table2。数字和已限定的P3判断正确，属于引用定位错误，不是需要暂停制作的L2判断错误。本期在selection-017的C-017-E1记载并交回Sol/总控修正定位；原记录不覆盖，未假称Sol已修订。

## 制作与复现

原图不复用；机制/条形图为编辑自绘。仅参考paper2assets目录与溯源原则，以自定义HTML + 本地Chrome制作，不声称完整paper2poster或PPTX产物。交付poster.png、单页poster.pdf、poster.html、SOURCE.md、QA.md；HTML和assets字体仅本地，原文全文不纳入交付。未运行论文代码、做实验复现或联系作者。
