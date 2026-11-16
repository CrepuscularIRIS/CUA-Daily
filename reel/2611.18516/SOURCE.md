# StreamEmbed — 来源与口径

- Paper: **StreamEmbed: Real-Time Indexing from Pixels for Screenshot Retrieval**，2611.18516v1，2026-11-13。
- 原文：https://arxiv.org/html/2611.18516v1 。读完正文 §§1–8、附录 A–H；未声称最新版本 API 审计。
- 最新 L2：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-50.jsonl`。遵循其收窄范围：指定硬件下的视觉索引吞吐瓶颈，不是代理任务效果。
- 编辑：selection-016，2026-11-16；本会话 gpt-6-astra（fable 槽，依总控确认的 2026-11-16 配置），不是 Opus 5.5。
- 所有数值为作者报告，未运行论文代码、未独立复现。像素网格为自行绘制的机制示意，不是原始截图；条形图是 Table 6 的数据重排。未使用原图像素。HTML + 本地 Chrome 制作；仅参考 paper2assets 的溯源原则，不声称完整执行 paper2assets/paper2poster 或提供 PPTX。

## 逐项来源

| 画报元素 | 原文位置 | 核对与限定 |
|---|---|---|
| 空间剪枝 | 方法章节（§4），实现附录 | 比较左/上邻块，最大 RGB 差阈值8/255；保留位置编码，每3×3 tile 为 uniform region 保留覆盖。原1280×720截图内部1280×704、880个32×32块。画报网格不按真实块数绘制 |
| 时间复用与刷新 | 方法章节及实现附录 | 比较当前像素与上次计算该块KV时像素；未变块复用 ViT/LM KV，变化/新增块与输出后缀重算。changed ratio>.9 或10帧刷新。未变像素的上下文仍可能改变，因此不是严格等价推理 |
| 一致性 LoRA | 方法/训练章节 | 完整图像 FT embedding 教师；cosine + KL ranking distribution + margin MSE 对齐剪枝学生，权重合并无额外推理开销。query embedding 仍用原 FT 模型 |
| H1耗时阶梯 2.33→1.65→1.00→.66→.66秒 | Table 6 | released full FT→equivalent linear patch→spatial→temporal→consistency。对应 R@10 83.4→83.4→82.8→81.8→82.1。横条共用0–2.33秒尺度。Conv3d→linear 优化是总增益的一部分，不全部归功剪枝/缓存 |
| H1/H2/Agent GPU时延与 R@10 | Table 5 | full FT→StreamEmbed：H1 2.33→.66秒、83.4→82.1%；H2 2.34→.84、84.5→83.3%；Agent 2.34→.63、58.2→57.6%。两者相同H1微调数据；质量损失1.3/1.2/.6个百分点 |
| 2.8–3.7× GPU加速 | Table 5，计算2.33/.66、2.34/.84、2.34/.63 | 四舍五入范围，基线为发布版完整编码；已经线性patch优化的基线为1.65/1.64/1.66秒，剪枝/复用相对其仅约2.0–2.6× |
| M2 Pro、32GB、空闲机、5秒采样 | 实验实现及延迟测量章节/附录 | EC2 mac2-m2pro，GPU MPS fp16；CPU fp32/8threads。输入历史每5秒一帧；30 H1/30 H2/20 Agent recordings，每段最多前50帧，起点cache空，计时读取图像到embedding。不是持续1Hz在后台负载下的服务测量 |
| p99 1.47–1.77秒；CPU均值1.87–2.61秒 | Appendix E；Table 5 | GPU均值<1秒不等于每帧<1秒；CPU三历史1.97/2.61/1.87秒，不支持1Hz |
| 10,426测试问题、184小时 | ScreenMemEval 数据章节及统计表 | H1 5,111题/88h，H2 3,507题/18h，Agent 1,808题/78h。另1,000 train/315 val，不加到测试分母。两个人类Windows历史与一个Ubuntu agent历史 |
| recording-level R@10 | 评估定义；Appendix A | 每个相关 recording/证据集合被任一检索截图命中即可；不是回答准确率或严格证据帧准确率。Agent appendix说明keyframes，但未找到可独立支撑更强证据帧主张的专门数值表 |
| 标签与留出局限 | 数据制作章节；Appendix A | 主要LLM生成/校验，未见独立人工相关性校准。全历史索引后查询，是回溯检索；H1有train/val recordings进入索引，54个test questions相关，移除后R@10变动≤.03。不能写成整段时间严格留出 |
| 多年索引非真实多年部署 | Table 4及对应附录 | 高斯噪声扩充真实embedding来模拟2.1M截图/年；RAM数字只计二值索引，不含全部截图、模型。五年56ms索引搜索另有52ms query encoding；本画报不采用这个次要headline |

## 领域对应与边界

- `main/experience_memory_retrieval` 的 B 类组件；直接像素索引子卡未收录，不声称已跑完K27“取回经验→规划执行”链条。
- K27的检索可靠性与迁移条件提醒：H2/Agent只说明检索来源变化，不说明跨应用任务完成率收益；LLM相关性标签未人工校准。
- 与 MobiInfer 不同：后者降低自回归决策推理延迟，本篇降低截图入库编码成本；与AWM不同，未证明跨任务工作流记忆增益。
- “本地”不等于经过隐私/安全审计；“real-time”只按上述硬件、平均耗时解释。不是无损、硬实时、全年持续运行或通用代理能力结论。
