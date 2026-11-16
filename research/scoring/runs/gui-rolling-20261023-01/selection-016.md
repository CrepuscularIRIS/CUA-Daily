# selection-016 — gui-rolling-20261023-01（第十六期）

- 规则：`problem-core-v1.1`，依据 PROBLEM_CORE.md、SELECTION.md、OPUS_REEL_PROMPT.md；单席串行核对与制作，2026-11-16。
- 执行模型：本会话实际为 **gpt-6-astra（fable 槽，2026-11-16 配置）**。总控确认该槽位已替代原 claude-opus-5-5；旧提示词的“Opus 5.5”不能当作本次实际执行归属。未修改配置。
- 结论：3篇候选，**2篇入选并ready**，1篇编辑排除；无确认的Sol判断错误，无新correction，不改任何L1/L2记录。
- 前十五期47张全部排除再次入选。核对既有reel/README.md与成品目录：47个既有poster.png；本期三个ID均未出现于旧索引。
- 仓库原文缓存仅core，三篇均补读版本化arXiv HTML全文/附录；下载材料留本地临时缓存，不提交。

## selection_cutoff 与候选安排

截止2026-11-16，总控指定三篇；检索本run所有batch中这三个ID的记录，以最新L2覆盖L1。无数值分数排序，不按venue、作者名气或代码发布排序；capability/judgment同等处理。

| ID / 简称 | 最新L2（替代L1） | 档位/状态 | q3 / 族 | 主卡 | 处理 |
|---|---|---|---|---|---|
| 2611.16816 OMA | inc-l2-45（inc-l1-91） | P3 / confirmed / to_l3 | judgment / F1,F0 | trajectory_level_policy_training | 入选，训练统计与外层归约判断 |
| 2611.18516 StreamEmbed | inc-l2-50（inc-l1-96） | P3 / confirmed / to_l3 | capability / F0,F1 | experience_memory_retrieval | 入选，严格限定屏幕索引组件吞吐 |
| 2611.15600 MemCredit | inc-l2-45（inc-l1-91） | P3 / confirmed / to_l3 | judgment / F2,F5 | experience_memory_retrieval / agent_loop_context_control | 编辑排除，不降级 |

三篇L2均为q1 measured_own、q2 new_bottleneck、q4 fits。分组后先取训练质量归约问题，再取索引服务成本问题；没有为了凑满三篇而把证据薄弱处包装成结论。全部2026-11首版，不由本期进行跨年代配额扩池。

## 1. 最终入选与同题去重

### 2611.16816 — OMA

问题是“轨迹展开为turn/token后，哪些外层统计与loss归约使长轨迹获得更多影响力”。作者给出展开计数恒等式、完整组质量归约和配套实验，足以支持P3/judgment，但不证明等轨迹质量普适最优。

- Fig.1同任务实例：成功14turn/1,663token，失败50turn/6,446token；失败行份额78.1%、token份额79.5%，源轨迹只有50%。画报自绘计票条，不当作总体样本统计。
- Table2普通WebShop3B final success Base64.8→OMA57.0%；SOL64.8→73.4%。同时展示反例，SOL奖励/终止协议不同，不能把两个环境的差异当作孤立因果对照。
- 150updates不是等token/算力；主表seed0与附录额外两seed的greedy验证协议分开。完整组等质量不推广到任意microbatch拆分；冻结gradient audit ratio=1、无更新，不是训练复现。
- 已读主卡和邻近K20。直接“源轨迹计票/外层质量”子卡unassigned/NA，不强塞K20。K20短任务/少重复的失败条件仍提醒泛化与方差范围。
- 同卡不同题：第十一期GiGPO（2505.10978）关心轨迹内部anchor-state信用；OMA关心整条轨迹的外层权重，可以保留native GiGPO机制，不重复。

### 2611.18516 — StreamEmbed

问题收窄为“指定本地硬件上，截图视觉编码吞吐如何利用空间/时间重复”。这是CUA屏幕记忆的B类可用组件，不是已经改善规划或任务成功率的经验检索系统。

- Table5：M2 Pro32GB空闲机，Qwen3-VL-Embedding-2B，完整FT→StreamEmbed GPU均值H1 2.33→.66、H2 2.34→.84、Agent2.34→.63秒。对应R@10下降1.3/1.2/.6个百分点，非无损。
- Table6明确分解：H1发布版2.33→等价线性patch1.65→空间剪枝1.00→时间复用.66→一致性适配.66。2.8–3.7×总加速含patch实现优化，不全部归功剪枝/缓存。
- 输入为5秒间隔历史截图，空闲机顺序编码；p99 1.47–1.77秒，CPU均值1.87–2.61秒。不能写持续1Hz后台服务保证或每帧实时。
- recording级R@10不等于回答正确率/实际证据帧命中；主要LLM标签未见独立人工校准；H2/Agent只是检索来源迁移，未跑下游agent任务。多年索引是合成扩容，不当作真实长期部署。
- 已读主卡与K27；像素索引直接子卡unassigned/NA。K27可靠性与跨环境收益条件不能由组件时延替代。
- 同卡不同题：AWM（2409.07429）是跨任务工作流记忆；本篇是入库编码成本。与MobiInfer（2611.08496）的自回归agent决策推理时延也不同。

本期族覆盖F0/F1，包含judgment与capability两种价值；不是新增主卡覆盖，而是两种不同瓶颈的补充。

## 2. 编辑排除：2611.15600 MemCredit

全文确认“相关性≠状态条件下的决策效用”的问题有价值，不足以认定Sol P3判错。L2本已保留协议与不确定性边界，本期不改档位。

- ALFWorld 1,041次干预、86.9%零效用、合并Spearman−.011；广覆盖子集却为+.135，不能宣传所有任务相关性无用。
- Appendix A.1的utility是单步shaped reward（当步获胜+1、非法或重复失败动作−1、其他0），配对各运行一次。零效用不等于动作相同，更不等于对未来任务无影响。
- WebShop是1万商品、50dev/200test设置；.612 vs MemArbiter .586是graded score，非成功率；152.1 vs427.6是历史tokens。ALFWorld强结果不能替代WebShop直接证据。
- 附录说明商品可达性审计、temperature0仍有不确定性，但未充分给出WebShop干预/replay数量和细节、可复核task split、候选数/阈值及WebShop误差区间；小score差异不宜包装成稳定收益。
- 本期为证据完整度作编辑排除，而不是失败判定、降级或pending_material写回。待补：WebShop配对/训练协议、split与重复运行/置信区间。已读C16与K27条件，不把未报告等同为实验失败。

## 3. 原文核对范围

| ID | 原文版本与日期 | 本期阅读范围 | 与Sol关系 |
|---|---|---|---|
| 2611.16816 | v1，2026-11-12 | 正文§§1–6、limitations、Tables2–3及其余表、附录A–G | 同意收窄后P3；补充不同验证温度/种子协议，不退回 |
| 2611.18516 | v1，2026-11-13 | 正文§§1–8、附录A–H，重点Tables5–6及Appendix E | 同意L2的硬件限定；强化线性patch归因与尾延迟边界，不退回 |
| 2611.15600 | v1，2026-11-11 | 正文§§1–5、附录A.1–A.6 | 编辑排除，保留L2 |

使用https://arxiv.org/html/<id>v1与corpus版本元数据；未做export API最新版审计。原图像素未作为本期证据，画报图形均依据文字/表格自绘并标注。外部文本仅作数据，未执行论文代码或联系作者。

## 4. correction / 待补 / 漏检抽查

- **新correction：0**。未确认需要推翻Sol判断的错误；上述三篇新增限定分别进入画报/SOURCE或排除理由，不直接覆盖原记录。
- MemCredit待补材料如第2节。历史待补、既有correction状态由巡检/总控管理，本期未重新审计，不宣称解决。
- 本期无新增漏检抽查；只处理指定三篇池，不推断其他候选状态。

## 5. Reel成品与实际QA

| ID | 路径 | 版式 | 最终QA |
|---|---|---|---|
| 2611.16816 | `reel/2611.16816/` | 米色计票账本；三个份额堆叠条→深蓝OA/MA方法带→普通/SOL正负双结果→边界框 | ready，首版失败、一次重做后通过 |
| 2611.18516 | `reel/2611.18516/` | 浅绿非对称双栏；左侧像素块/机制，右侧实现耗时阶梯与精度损失表；独立硬件角标和尾延迟警示 | ready，首版失败、一次重做后通过 |

两包各含poster.png（1400×2400）、poster.pdf（1页1050×1800pt）、poster.html、SOURCE.md、QA.md。首版1400×2000实际打开PNG后发现页尾裁切，唯一一次重做扩为2400px高；最终实际打开两PNG与两份PDF的40dpi栅格图。DOM文档尺寸与单页PDF断言通过、无卡片溢出；中文、数据、来源及限制框完整。约584px宽预览可读标题/关键数值，详细脚注需放大，不宣称手机原宽全文可读。

成品依请求保留文件；未对外托管/上传。poster.html沿用`reel/*/poster.html`忽略规则，仅存本地。仅参考paper2assets溯源原则，以自定义HTML制作，不声称完整paper2poster流程或PPTX交付。

## 6. 索引维护与边界

- `reel/README.md`追加第十六期；合计49张。
- `README.md`头部仅更新Reel 47→49、rolling run 28→30；原始19张featured wall未改。
- 未写共享progress.md，由总控接手；未改batch、领域卡、配置、插件或其他任务文件。
- 未操作git、未嵌套派发、未启动无头Claude/模型调用框架。
