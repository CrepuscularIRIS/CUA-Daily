# gui-v3.1 — CUA-Daily / GUI Agents

权重：G=15、M=25、X=20、E=40。正式范围以仓库 `docs/EVIDENCE.md` 为准。


核心问题：**改变了感知—规划—动作—反馈中的哪一环，任务是否真的完成，提升是否来自该环？**

收录桌面、移动端和 Web 上执行图形界面操作的 agent，以及 grounding、训练、记忆、环境模型、benchmark 和 verifier。纯 API agent、只生成 UI 代码而不操作界面、机器人工作分流到其他项目。

| 轴 | 本领域的具体判断 |
|---|---|
| G | 瓶颈是看不清、定位错误、长程状态丢失、动作不可执行，还是完成判断不准？区分静态单步与真实交互。 |
| M | 改变了哪条 observe–act–feedback 路径或训练信号？为何对准瓶颈，而非只加模型、角色和步骤？ |
| X | 信息可见性、动作接口、历史/上下文、恢复与验证的必要条件是否清楚？只检查本文相关环节。 |
| E | 用什么执行结果判成功？基座、环境、步数/时间预算是否可比？训练/探索见过的网站不能当未见迁移。 |

grounding 组件按定位任务的主张评价，不因没有完整在线 agent 一律扣分；但不能将静态准确率宣传成在线任务成功。评测审计和负结果也可高分。

证据等级沿用 offline / online / transfer，材料不够则 unknown。LLM judge 或 learned verifier 需要注明是否有可执行真值或人工校验；初步材料不足就留下疑点，不编造验证。

可按机制查现有领域卡：

- `patterns/main/structured_screen_observation.md`：组织屏幕观测。
- `patterns/main/agent_loop_context_control.md`：控制交互循环上下文。
- `patterns/main/learned_outcome_and_process_judges.md`：结果/过程判断器。
- `patterns/main/trajectory_level_policy_training.md`：轨迹级策略训练。

这里的 Cxx 是 GUI 领域卡编号，只记录 gui:<card-id>；不再输出原 ResearchStudio Cxx。依据领域卡具体判据评分，匹配标签本身不加分。
