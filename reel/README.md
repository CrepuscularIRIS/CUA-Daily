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

---

# 第二期 — gui-pc11-20261022-01 全量(2026-10-22 · 8 篇)

基于全量 L2(1279/1331 篇过 L2)后的 584 篇候选池选题。本期补强 F0/F3/F4/F5,未入 F2(首期已覆盖 5 篇)。版式骨架与首期及互相均不相同。

| paper | 档位 | q3 / 族 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|
| 2606.12666 CAPED | P3 | capability / F4,F0 | 截图上传前遮蔽隐私内容,泄漏率降 3 倍效用不降 | 泄漏-效用对照柱 | ready |
| 2504.13936 ViMo | P3 | capability / F0,F2 | 生成的未来屏幕能实际用于选动作,在线 +7.76pp | 生成-选择闭环 | ready |
| 2602.12276 CATTS | P3 | judgment / F5,F2 | 统一加候选采样不保证更好(22.6%→15.1%) | 成本-收益反单调曲线 | ready |
| 2310.03720 SteP | P3 | judgment / F5,F0 | 同示例数下策略栈(33%)胜扁平 prompt(20-23%) | 栈式分层结构 | ready |
| 2601.22781 | P3 | judgment / F5 | 合成数据不是越难越好,α=0.5 最优(+4.3pp) | α 参数倒 U 曲线 | ready |
| 2311.18751 | P3 | judgment / F3 | 基本任务成功≠组合完成(54.8%→31%) | 组合断裂链 | ready |
| 2312.08914 CogAgent | P3 | judgment / F0,F1 | 同数据、计 FLOPs,架构净贡献约 4.5% | 双因子归因天平 | ready |
| 2609.02154 MFA | P3 | judgment / F0,F4 | MFA 完成不再能证明人在场(10/10) | 认证链攻破路径 | ready |

选择过程与 28 篇排除理由见 [selection2.md](../research/scoring/runs/gui-pc11-20261022-01/selection2.md)。两期合计 17 篇,版式 17 种互不相同。

---

# 第三期 — 重激活后选题(2026-10-22 · 2 篇)

基于重激活 L2(244 篇重核,5 篇新晋 P3)后的 591 篇候选池。只选了证据最硬的 2 篇,不凑数。

| paper | 档位 | q3 / 族 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|
| 2604.00073 | P3 | judgment / F1,F0 | 同骨干下 GUI 与终端接口成功率差 1 点,成本差 2-8 倍 | 接口成本-效果矩阵 | ready |
| 2604.04918 | P3 | judgment / F0,F2 | 138 次问题动作只拦住 29 次:有审批≠能拦住 | 人机审批漏斗 | ready |

选择过程见 [selection3.md](../research/scoring/runs/gui-pc11-20261022-01/selection3.md)。三期合计 19 篇,版式 19 种互不相同。

---

# 第四期 — gui-rolling-20261023-01 增量轮（2026-10-26 · 3 篇）

增量轮候选池 6 篇（全部 P3 confirmed）。Opus 5.5 读完三篇的完整原文与附录后制作；另 3 篇排除（同卡去重 1、编辑排除 1、证据形态 1），理由见 selection-004。本期无 correction 退回。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.30792 Trace2World | P3 | judgment / F2,F3 | calibrate_simulator_to_real（**新覆盖**） | 只把验收证据换成源轨迹回放，模拟收益留到真机 94.0% vs 54.7%（训练 app） | 双边界管线 + 哑铃图 + 保留率柱 | ready |
| 2610.31698 Malva | P3 | judgment / F1,F2 | structured_screen_observation（**新覆盖**）/ agent_loop_context_control | 工具层不核对就交状态：335 例失败、11 种模式、119 例错而不报 | 四相位环形缺陷地图 | ready |
| 2610.32536 IGG | P3 | judgment / F1 | high_resolution_target_localisation / online_evaluation_methodology | 替模型做掉显露动作，Qwen3-VL 30.8%→81.9%；只告诉动作类别仅 +3.1 | 阶段分解 + 逐级干预剥离 | ready |

选择过程见 [selection-004.md](../research/scoring/runs/gui-rolling-20261023-01/selection-004.md)。四期合计 22 篇，版式 22 种互不相同。
