# OMA — 来源与口径

- Paper: **Outcome-Mass Alignment: Controlling Length-Dependent Trajectory Influence in Multi-Turn LLM Agent Reinforcement Learning**，2611.16816v1，2026-11-12。
- 原文：https://arxiv.org/html/2611.16816v1 。读完正文 §§1–6、limitations、附录 A–G；引用按此版本，不声称做过最新版本 API 审计。
- 最新 L2：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-45.jsonl`。
- 编辑：selection-016，2026-11-16；本会话 gpt-6-astra（fable 槽，依总控确认的 2026-11-16 配置），不是 Opus 5.5。
- 仅文献核对，未执行论文代码、未复现结果。图表为中文自绘/数据重排，没有裁剪或使用未经核对的原图像素。使用 HTML + 本地 Chrome；参考 paper2assets 的溯源原则，未完整执行该插件或 paper2poster，不声称 PPTX 产出。

## 逐项来源

| 画报元素 | 原文位置 | 核对与限定 |
|---|---|---|
| 轨迹展开导致隐式长度权重 | §§3–4；Fig. 1 | 行扩展 outcome 均值为 Σ nᵢyᵢ / Σ nᵢ，唯一轨迹均值为 Σ yᵢ/K；两者差为 Cov(n,y)/E[n]。token-mean 的外层质量为 Dᵢ/ΣD。不是动作内部信用分配 |
| 14 vs 50 turns；1,663 vs 6,446 tokens | Fig. 1 的作者 ALFWorld 同任务/同 checkpoint 实例 | 失败行份额 50/64=78.125%，token 份额 6446/8109=79.492%；均四舍五入一位小数。源轨迹各 50%。自绘条长度依此比例，不是总体样本分布 |
| OA：只统计一次再广播 | §3.2 | 指指定的 outcome statistics；本已唯一轨迹归一化的实现中 OA 是 identity，不把所有实现都称为有 bug |
| MA：先轨迹内均值再组内均值 | §3.3 目标定义；Appendix B | 画报以 t 合并原文有效 row/token 索引，仅对有效 response tokens 求和，Dᵢ 为其数量。保留 native advantages、ratio、detach、clipping。等质量只在完整组归约成立；各自归一化的 microbatch 不具任意分割不变性 |
| 普通 WebShop 3B：64.8→57.0% | Table 2，final success | Base vs OMA，−7.8 个百分点。不是 score，也不是 nAUC。对应 score 81.4→71.4；success nAUC 32.4→34.4，不拿 endpoint 代表全曲线 |
| WebShop-SOL 3B：64.8→73.4% | Table 2，final success | +8.6 个百分点。SOL 修改训练 reward 与 successful-only termination；不是普通 WebShop 单变量对照。success nAUC 39.9→51.1 |
| 主表协议 | §4.1；Appendix C | Qwen2.5-Instruct，seed 0，150 trainer updates，16 groups/update、8 trajectories/group、1 PPO epoch；原 validation temperature .4。update-matched 不是 token/interaction/compute/time matched；不同 A800/H20 host/software 家族，不支持效率因果结论 |
| 额外两 seed 的终点与曲线差异 | Appendix A | greedy validation temperature 0、env seed 1000；WebShop 1.5B Base endpoint success 47.27±.55 → OMA 58.20±2.76；nAUC 30.29±2.66 → 29.15±6.58（两个 seed 的均值±样本 SD）。与主表不拼成同协议 n=3，不作显著性结论 |
| OA 单用可能损伤结果 | Tables 2–3 | ALFWorld 3B endpoint Base74.2 / OA61.7 / MA77.3 / OMA81.2；1.5B Base73.4 / OA38.3。支持“不是普适最优”而非所有环境必然有害 |
| 冻结梯度审计不是实际更新复现 | gradient audit 正文及附录 B–G | 选定完整8轨迹组；ratio=1，old probs 为 detached current，clip inactive，无 optimizer step。归档 retokenization 检查 token count，不是历史 minibatch replay |

## 领域对应与边界

- 主卡 `main/trajectory_level_policy_training`；直接“外层统计/质量归约”子卡未收录，不强塞 K20。
- K20 是邻近条件：短任务、少重复与跨规模限制仍重要。主卡 E16 的多次运行期望未由单 seed 主表满足；额外 n=2 只给描述性补证。
- 与 GiGPO Reel 不同：GiGPO 审计轨迹内 anchor-state 信用，OMA 问整条源轨迹如何计票；native GiGPO 机制在 OMA 中可以保留。
- 不宣称新 SOTA、通用 GUI 能力提升、显著优势、计算预算公平或等轨迹质量必然正确。
