# 收录范围与证据等级

## 收录范围

**Computer-Use / GUI / Browser Agent**：在图形界面或浏览器上感知并执行操作来完成任务的系统（桌面、移动端、Web），以及它们的：

- 架构：感知与 grounding、规划、动作空间、记忆、反思与反馈；
- 训练：数据合成、SFT、RL；
- 环境模型：world model、模拟器、数字孪生；
- 评测：benchmark、verifier。

- **A 类**：论文提出新的 agent 架构、训练方法或环境模型，并在交互环境中验证。
- **B 类**：可直接用于 CUA 系统的组件或方法学，例如 grounding 数据集、judge / reward model、benchmark、评测审计方法。
- **不收录**：
  - 没有 GUI 或浏览器操作面的纯 API / function-calling agent；
  - 只生成 UI 代码、不在界面上执行操作的方法；
  - 不涉及交互的通用 VLM benchmark；
  - 机器人具身操作。

## 证据等级

| 等级 | 需要的证据 |
|---|---|
| `offline` | 只有静态的单步准确率、grounding 准确率或离线回放 |
| `online` | 在可交互环境中，任务成功由执行结果检查判定（OSWorld、AndroidWorld、WebArena、Online-Mind2Web 等） |
| `transfer` | 在构建系统时未使用过的环境、应用、网站或平台上取得 online 成功，或者跨 ≥2 个平台族（Web / 移动 / 桌面）取得 online 成功 |

判定规则：

1. **按证据判，不按自称判。** 论文自称 "generalist" 不等于 `transfer`。
2. **合成或探索用过的环境不能当留出集。** 训练数据、记忆或孪生体的校准来自哪些应用或网站，在这些应用或网站上的提升最高只能判为 `online`。
3. **学习型验证器要单独审计。** 如果成功率是由 LLM judge、reward model 或 world model 判定的，必须看它是否经过人工标注或可执行真值的校验。
4. **作者自称与我们的判定分开写。** frontmatter 里的 `evidence_level` 是我们的判定。
