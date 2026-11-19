# MemCredit (2611.15600) — SOURCE

论文：*MemCredit: Decision-Utility Memory for Long-Horizon Agents*（缓存正文标题段），arXiv 2611.15600，2026-11 提交（v1）。
缓存全文：`research/fulltext/2611.15600.txt`（FULLTEXT: html，含 §1–§5 正文与 Tables 1–5；附录 A.1 不在缓存中）。核对于 2026-11-19（本仓 selection-019，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 核心问句"缺了这条记忆，代理会不会做出更差的决策" | "would the agent make a worse decision if a particular memory were unavailable?" | §1 |
| 相关性 vs 效用定义（检索匹配状态 / 决策改善） | "semantic relevance measures whether a memory matches the current state, whereas decision utility measures whether it improves the agent's decision" | §1 |
| 效用定义式 U_π(m;s,S)=E[Q\|s,S∪{m},π]−E[Q\|s,S,π] | 式(1) | §1 |
| 500-token 预算 ALFWorld SR@50：MemCredit 86.57 vs BM25 65.67 | Table 1（Overall 列），"outperforming BM25 retrieval by 20.90 percentage points" | 摘要，§1，§4.2，Table 1 |
| 750-token：90.30 vs BM25 81.34，差 20.90→8.96 | Table 1；"decreases from 20.90 points at 500 tokens to 8.96 points at 750" | §4.2 |
| 基线系列 Flat Recency 57.46 / BM25 65.67 / Failure-Aware 70.15 / State-Aware 76.12 / MemArbiter 82.84 | Table 1 Overall 列（500-token 段） | Table 1 |
| 柱状图六根（57.5/65.7/70.2/76.1/82.8/86.6） | 同上，四舍五入到一位小数 | Table 1 |
| 失败后恢复 75.9 / 失败动作重复 16.4（最优） | Table 1 Recovery / Failed Rep. 列 | §4.2，Table 1 |
| 对 BM25 优势最大类 Pick Two +35.30 | "improves over BM25 by 30.43, 28.57, and 35.30 points … on Heat, Cool, and Pick Two" | §4.2 |
| WebShop：0.612 / 152.1；MemArbiter 0.586 / 427.6；State-Aware 0.524 / 578.4；BM25 0.407 / 597.0；Full History 0.356 / 599.1 | Table 2 全表 | §4.2，Table 2 |
| 少用 64.4%（vs MemArbiter）/ 74.5%（vs BM25）记忆 token | "reductions of 64.4% and 74.5%" | §4.2 |
| 重复搜索 0.227→0.213、无效动作 0.324→0.316、步数 12.3→12.0 | Table 2；"repeated searches decrease from 0.227 to 0.213, invalid actions from 0.324 to 0.316, and average trajectory length from 12.3 to 12.0" | §4.2 |
| "Score 为 WebShop 官方分（非成功率）" | "Score denotes the official WebShop task score" | Table 2 注 |
| 1041 次干预 / 45 任务 / 86.9% 零效用 | "Across 1,041 context-conditional interventions from 45 ALFWorld tasks, 86.9% produce no measurable behavioral change" | §1，§4.3，Table 3 |
| 失败上下文 +0.176 vs 非失败 +0.029 | Table 3；§4.3 | 
| 相关性-效用合并 Spearman −0.011；dense 子集 −0.191；broad +0.135 | Table 3（画报主面用合并值，dense/broad 未上画报） | §4.3，Table 3 |
| 平均 credit +0.054 | Table 3 | §4.3 |
| 效用预测：full +0.220 Spearman / 0.270 AUPRC / 0.744 AUROC；relevance-only −0.031/0.097/0.483；failure-only AUROC 0.658；shuffled +0.048 | Table 4 | §4.4 |
| "秩相关中等：当排序信号用" | "its moderate rank correlation shows that fine-grained utility prediction remains challenging … a practical ranking signal rather than an exact regressor" | §4.4 |
| 消融：BM25 排序 65.67 / 失败启发式 70.15 / λ=0.5 混合 78.36 / utility-only 84.33 / 去显式 failure+state 特征 86.57 | Table 5 | §4.5 |
| λ=0.5 比 utility-only 低 5.97 点 | "5.97 points below utility-only ranking" | §4.5 |
| 相关性只做召回不进最终打分 | "Relevance limits the search space; it is not interpolated into the final utility score" | §3.4 |
| 主模型 Qwen3.6-27B-FP8、vLLM、确定性解码 | "All main experiments use Qwen3.6-27B-FP8 with deterministic decoding … served with vLLM" | §4.1 |
| 跨模型 Qwen2.5-7B / DeepSeek-V3 / GPT-5.4 近乎全胜，例外 GPT-5.4 下 BM25 略高 | "the single exception is SR@50 under GPT-5.4, where BM25 scores marginally higher" | §4.2 Cross-model |
| 原子记忆五型 Goal/State/Constraint/Episodic/Reference（沿用 MemArbiter） | "Following MemArbiter … functional types are Goal, State, Constraint, Episodic, and Reference" | §3.1 |
| α∈{0,¼,½,¾,1} 占用层级采样参考上下文 | 式(6) 及其说明 | §3.2 |
| 同一环境快照起跑、两支只差 m 的渲染 | "both branches start from the same verified environment snapshot and differ only in the rendered inclusion of m_i" | §3.2 Paired environment replay |
| ExtraTrees 回归器、特征两组（状态-记忆 + 上下文覆盖/Jaccard/预算占用） | 式(13)(14)；"We retain an ExtraTrees regressor" | §3.3 |
| 在线贪心：credit per added token 最大、阈值 δ、分数随 S 重算、预算是上限 | 式(16)(17)；"the budget is a ceiling rather than a requirement" | §3.4 |
| ALFWorld 依赖确定性动力学（含重构状态校验） | "Its deterministic dynamics allow factual and counterfactual decisions to be replayed from the same reconstructed environment state"；"every retained sample passes the reconstruction check" | §4.1，§4.3 |
| 边界：干预/重放次数与置信区间未在正文给出（WebShop） | 正文仅 Table 3 给 ALFWorld 干预的 task-clustered bootstrap CI；WebShop 干预数量与重复次数未见 | §4.1–§4.3（缺失事实，按"未给出"陈述） |
| 贪心不保证全局最优、可能漏互补记忆对 | "does not assume additive utilities or guarantee a globally optimal subset … may miss complementary memories that are useful only jointly" | §3.4 |

## 编辑收窄

- 画报不呈现 dense/broad 子集相关性（−0.191/+0.135）分野，只引合并 ρ=−0.011 与"相关≠有用"结论；子集分歧属原文细节，未上画报不构成误导。
- WebShop 边界按事实写"干预/重放次数与置信区间未在正文给出"，同时保留分数与 token 数对照表；selection-016 提出的"协议细节缺失"在本缓存仍未完全补齐（附录 A.1 不在缓存），画报如实标注。
- "策略冻结"是方法设计（不加环境交互），画报边界区不将其夸大为部署安全声明。
- 86.9% 零效用与 0.176/0.029 均为 ALFWorld 干预统计，画报同句注明"1041 次干预（45 个 ALFWorld 任务）"，不外推到 WebShop。
