# Reel — gui-pc11-20261022-01(2026-10-22 · problem-core-v1.1)

本期 9 篇,全部经 Opus 5.5 完整原文核对后制作,版式骨架互不相同;每篇含 poster.png / poster.pdf / SOURCE.md(数字→原文定位)/ QA.md(核对结论+视觉检查)。可编辑源 poster.html 受旧 .gitignore 忽略仅存本地。画报核对共产生 5 条修订(l19–l23,run batches/),1 条降档(WebArena P3→P2 按编辑理由保留)。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2412.10840 | P3 | judgment / F1 | high_resolution_target_localisation | 注意力定位 vs 坐标生成:把"看不见"与"输出差"分开 | 双路径对照解剖 | ready |
| 2505.15810 | P3 | judgment / F2,F5 | rule_reward_single_step_rl | 框尺寸奖励被投机;推理越长定位越差(仅文字目标) | 奖励投机回路 | ready |
| 2307.13854 | P2* | judgment / F2,F3 | online_evaluation_methodology | 终态检查替代动作序列匹配(误判率未实测→P2,编辑保留) | 基准三层剖切 | ready |
| 2508.00935 | P3 | judgment / F2,F0 | verifiable_execution_reward | 聊天里拒绝 ≠ 电脑上不做:执行通道分开测量 | 双通道背离 | ready |
| 2404.06474 | P3 | capability / F2,F4 | learned_outcome_and_process_judges | 评估器与执行/人工双重校准并用于下游 | 信号校准链 | ready |
| 2409.07429 | P3 | capability / F3,F4 | experience_memory_retrieval | 只用已完成查询归纳工作流,信息边界防泄漏 | 归纳窗口时序 | ready |
| 2406.11896 | P3 | capability / F3 | trajectory_level_policy_training | 同骨干下在线 RL 逐级超过模仿(模拟器+实时网站) | 训练范式阶梯 | ready |
| 2407.01476 | P3 | capability / F0,F5 | simulated_lookahead_selection | 算力配平后搜索仍有效;前提环境可重置 | 搜索树+预算天平 | ready |
| 2503.19537 | P3 | capability / F2,F4 | agent_initiated_user_interaction | 负结果:12 种 prompting 配置问人 precision 仅 0.08–0.19 | 失误矩阵+低精确率散点 | ready |

*2307.13854 修订记录见 batches/l19-correction.jsonl;其余修订:l20(2404.06474 单位)、l21(2505.15810 边界)、l22(2409.07429 口径)、l23(2503.19537 范围)。选择过程与 43 篇排除理由见 research/scoring/runs/gui-pc11-20261022-01/selection.md;分数体系为问题档位(P0–P3),非审稿分。
