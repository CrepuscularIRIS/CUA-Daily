# 输出示例：全部为虚构数据

下面只演示 `rsi-v3` 的格式、算术与材料不足处理。SYNTH ID、定位和叙述均为人工构造，不是实际论文或模型评审。不能放入正式候选池。真实批次在 run.md 中记录模型、profile、材料清单与来源，逐篇来源不得使用占位内容。

## 材料足够，但只支持较窄结论

```json
{"paper_id":"SYNTH-A","version":"example","source_url":"https://example.invalid/paper-a","material_level":"core","status":"scored","claim_type":"system_method","move":"根据执行错误修改技能，并将通过门控的版本留给后续任务。","gap":"针对共享技能长期使用后质量退化的问题，增加显式替换判断。","patterns":{"rs_primary":"generative_process_redesign","rs_sub":null,"domain":["rsi:evidence_gated_retention"],"status":"matched","reason":"把固定的技能留存步骤变为可检查的选择过程；子卡材料不足，不强配。"},"ratings":{"G":3,"M":3,"X":2,"E":2},"screen_score":58.75,"reasons":{"G":"问题具体，但与其他门控方案的差别有限（示例 §2）。","M":"错误反馈到技能修订的逻辑清楚（示例 §3）。","X":"写回和调用可理解，回滚条件仍不清楚（示例 §3）。","E":"有后续任务结果，但选择与评测分离不清楚（示例 Table 1）。"},"evidence":[{"locator":"示例 §3","fact":"描述了技能候选、门控和保存流程。"},{"locator":"示例 Table 1","fact":"报告单一任务族结果，未提供足够信息判断独立留出。"}],"claim_support":"scoped","evidence_level":"task","caveat":"作者称可跨任务持续提升；所给材料仅支持单一任务族的报告结果，不能确认 retained。","needs":[]}
```

显示 58.8，内部保留 58.75。scoped 可以进入待核对候选；不是直接开始制作或确认 retained。

## 只有摘要，缺材料不等于低质量

```json
{"paper_id":"SYNTH-B","version":"example","source_url":"https://example.invalid/paper-b","material_level":"abstract","status":"needs_material","claim_type":"system_method","move":"作者提出根据反馈重写 agent 的记忆。","gap":"声称解决重复失败，但摘要没有说明最近邻区别。","patterns":{"rs_primary":null,"rs_sub":null,"domain":[],"status":"uncertain","reason":"未说明如何修改、保存和使用记忆，无法区分机制。"},"ratings":{"G":null,"M":null,"X":null,"E":null},"screen_score":null,"reasons":{"G":"摘要不足以定位具体残余瓶颈。","M":"摘要没有可重建的操作。","X":"缺方法和接口说明。","E":"缺主要实验及评测条件。"},"evidence":[{"locator":"示例摘要","fact":"只宣称记忆改善任务表现。"}],"claim_support":"unresolved","evidence_level":"unknown","caveat":"不能由摘要缺失推断论文没有实验。","needs":["方法说明和主实验表及其评测条件"]}
```

总分 null，不进入数值排序；如果机制线索有价值，可进入少量补材料清单。

## 算术对照

| G/M/X/E | RSI / Embodied | GUI |
|---|---:|---:|
| 0/0/0/0 | 0 | 0 |
| 2/2/2/2 | 50 | 50 |
| 3/3/2/2 | 58.75 | 60 |
| 4/4/4/4 | 100 | 100 |
| 任一项 null | null | null |

这些对照只验证公式，不标定真实论文质量，也不代表本版已经跑过模型或验证了选题效果。
