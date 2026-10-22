# 问题族映射：CUA-Daily

配合 [PROBLEM_CORE.md](PROBLEM_CORE.md) 使用，版本 `problem-core-v1`，初版映射，尚未试点。依据为各主卡“Cognitive barriers”与“Failure modes”两节；3 张卡没有认知障碍节，只用失败模式。本表只用于检索和归组；判断 Q2、Q3 时必须引用卡片原文，不能只引本表。

| 主卡 | 问题族 | 卡片中的锚点要点 |
|---|---|---|
| [agent_initiated_user_interaction](../../patterns/main/agent_initiated_user_interaction.md) | F1、F4 | 求助由真值或模拟用户回答，成功归功于 oracle；未计入提问成本 |
| [agent_loop_context_control](../../patterns/main/agent_loop_context_control.md) | F5 | 每步更多推理文本不一定有益 |
| [calibrate_simulator_to_real](../../patterns/main/calibrate_simulator_to_real.md) | F3 | 数字孪生不能直接替代真实环境；机器人 sim-to-real 技巧不能原样迁移到 GUI |
| [environmental_injection_attacks](../../patterns/main/environmental_injection_attacks.md) | F4 | 只看截图的 agent 并不免疫，渲染出的弹窗和可写文本仍能劫持 |
| [experience_memory_retrieval](../../patterns/main/experience_memory_retrieval.md) | F3 | 报告的 OOD 收益接近零 |
| [exploration_driven_task_synthesis](../../patterns/main/exploration_driven_task_synthesis.md) | F3 | 收益常在用于合成的环境上测量，跨站点迁移差 |
| [high_resolution_target_localisation](../../patterns/main/high_resolution_target_localisation.md) | F1 | 只训练动作头已能恢复大部分 grounding，坐标 SFT 未必在教感知 |
| [injection_defense_isolation](../../patterns/main/injection_defense_isolation.md) | F4、F5 | 消费被攻击输入的检查组件反而提高攻击成功率 |
| [learn_and_train_in_gui_world_model](../../patterns/main/learn_and_train_in_gui_world_model.md) | F1、F3 | 纯想象训练可低于 SFT，真实锚点承载大部分收益；理论界过松 |
| [learned_outcome_and_process_judges](../../patterns/main/learned_outcome_and_process_judges.md) | F2 | 整体准确率高不代表可安全作 reward；precision 与 NPV 不同，利用很少被测 |
| [mine_human_screen_videos](../../patterns/main/mine_human_screen_videos.md) | F2、F4 | 测试任务附带对应演示视频；VLM 推断的动作标签未经检查就用于训练 |
| [online_evaluation_methodology](../../patterns/main/online_evaluation_methodology.md) | F2、F3 | 评测方法本身的可靠性；领域随机化未改善 GUI grounding |
| [planner_grounder_interface](../../patterns/main/planner_grounder_interface.md) | F1 | 有强 grounder 时规划错误才是主要失败来源 |
| [rule_reward_single_step_rl](../../patterns/main/rule_reward_single_step_rl.md) | F1、F2 | 形状奖励被策略利用；RL 收益与数据量、骨干差异混在一起 |
| [simulated_lookahead_selection](../../patterns/main/simulated_lookahead_selection.md) | F2、F5 | 候选数增加收益饱和，并取决于验证器准确率 |
| [structured_screen_observation](../../patterns/main/structured_screen_observation.md) | F4、F5 | 结构越多不一定越安全，会继承陈旧状态和攻击者可控文本 |
| [trajectory_level_policy_training](../../patterns/main/trajectory_level_policy_training.md) | F5 | 没有 KL 或回放时，多阶段在线 RL 会退化 |
| [verifiable_execution_reward](../../patterns/main/verifiable_execution_reward.md) | F2 | 执行检查器不是真值，合法替代解被判错，假阳性未量化 |
