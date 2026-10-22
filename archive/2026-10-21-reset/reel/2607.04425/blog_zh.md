# UI-MOPD：一个 8B GUI 智能体，两个平台教师，按平台路由的在策略蒸馏

*CUA Radar 对 arXiv 2607.04425v2（Lian、Chen、Yu、Duan、Liu、Liu、Fu、Luan、Qu、Xia、Wang；清华深圳国际研究生院、小米、哈工大深圳、浙江大学、鹏城实验室）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2607.04425v2 · 代码：https://github.com/EliSpectre/UI-MOPD*

## 问题：平台共享能力，但交互约定互相冲突

一个同时操作电脑和手机的 GUI 智能体，必须同时保住两套交互词汇。论文的表述是：桌面与移动端”share transferable capabilities but differ in action semantics and interaction conventions”——同样是”返回”，在电脑上是关窗口，在手机上是按返回键。论文的初步分析发现，混合监督微调和静态模型合并”tend to average away or overwrite platform-specific behaviors”。在 8B 基座上，仅桌面 SFT 把 OSWorld 从 33.9% 提到 35.8%，却让 MobileWorld 从 7.7% 崩到 0%；把两个平台模型做 TIES 合并，MobileWorld 同样是 0%。

## UI-MOPD 是什么

**智能体。** 一个以截图为输入的跨平台 GUI 智能体，覆盖桌面与移动。感知是截图（训练时只看当前截图；推理时看 4 张历史截图 + 当前截图 + 完整文本动作历史），动作以 tool-call JSON 输出、带坐标。桌面走 `computer_use` 接口（key、type、各类鼠标点击、scroll、wait、terminate），移动走 `mobile_use`（click、long_press、swipe、type、answer、system_button、wait、ask_user、terminate）。它在 CUA Radar 板上的架构模式是 R01，属于 rule-reward single-step RL 一族。

**数据。** Uni-GUI，用统一跨平台采集 harness 构建：近 1 万条高质量可执行轨迹，最终过滤前约 160K 步、11.5K 条轨迹，混合自采数据（桌面用 Kimi-K2.6、移动用 Gemini-3.1-Pro 采集，后者还负责清洗）与清洗后的 OpenCUA、OpenMobile 数据。超过 40 步的轨迹被丢弃，再由 Gemini-3.1-Pro 按子任务逐项判定成功后才保留。

**机制。** 两个阶段。Stage 1 在 Uni-GUI 的桌面、移动两个分区上分别 SFT 出两个 Qwen3-VL-32B-Thinking 专家教师。Stage 2 从 Qwen3-VL-8B-Thinking 初始化一个共享学生，用基于 GRPO 的 DAPO 目标在自己的 rollout 上做强化学习——新东西在这里：多教师在线策略蒸馏（MOPD），论文称这是该技术首次进入 GUI 智能体训练。每条 rollout 按平台标签路由到对应教师，教师作为”platform-conditioned behavioral anchor”，通过 token 级反向 KL（K3 估计器，系数 0.01）约束学生；一个组级自适应 mask 会在该组任务奖励已足够时去掉 KL 惩罚。教师只在训练期存在，部署只需要单个 8B 学生。

**训练信号。** 每个动作的规则奖励：所有维度匹配（动作类型、坐标落入目标框、滚动方向、按键集合、大小写不敏感文本）得 1.0，部分有效得 −0.5，无法解析得 −1.0。训练每阶段 1 个 epoch，每个 prompt 采 8 条 rollout，用 64 张 H100。

## 论文报告的结果

在线任务成功率；下列集成方法各行的学生同为 8B 规模。

| 方法（未注明即 8B 学生）            | OSWorld   | MobileWorld | H-Mean    |
|-------------------------------------|-----------|-------------|-----------|
| Qwen3-VL-8B-Thinking（基座）        | 33.9%     | 7.7%        | 12.5%     |
| Mixed-SFT (8B)                      | 35.0%     | 6.4%        | 10.8%     |
| Mixed-RL (8B)                       | 35.9%     | 9.4%        | 14.9%     |
| Unified-Teacher OPD（32B 混合教师） | 35.9%     | 8.7%        | 14.0%     |
| Mobile-Only OPD（32B 教师）         | 34.9%     | 10.3%       | 15.9%     |
| MOPD（8B 教师）                     | 36.2%     | 9.4%        | 14.9%     |
| **UI-MOPD**                         | **38.2%** | **12.0%**   | **18.3%** |

论文报告相对基座分别提升 12.7% 与 55.8%，两个平台各涨 4.3 个点（MinGain 4.3，为其消融表最大值）。H-Mean 18.3% 与 Qwen3-VL-235B-A22B-Thinking（38.1% / 12.0% / 18.3%）持平。作为参照，论文列出 SeedVL-1.5 在 OSWorld 34.1%、GUI-Owl-7B 34.9% / 4.5%、GELab-Zero-4B 31.9% / 10.9%；“Controlled Training References” 里还有两个 32B 教师（桌面 46.3%，移动 16.2%）与 32B Mixed-SFT 的 44.4% / 16.2%，并明确说后者是容量参考、不是参数对齐基线。

离线静态能力只作为对照：AndroidControl⋆ 准确率从基座 78.73% 到 80.05%，OSWorld-G 从 52.13% 到 52.84%，ScreenSpot-Pro（43.71% 到 43.14%）与 ScreenSpotV2（91.27% 到 90.88%）与基座相差不超过 0.6 个点；TIES 合并把 AndroidControl⋆ 拉到 74.01%。以上所有数字，论文均未报告种子、运行次数或方差。

## 论文自带的对照实验

- **教师专精，而非规模。** 固定 8B 学生与 Stage-2 数据，把 32B 专家换成 8B 教师得 36.2% / 9.4%，换成混合数据训练的统一 32B 教师得 35.9% / 8.7%——“the advantage of UI-MOPD cannot be explained by ordinary OPD or teacher scale alone”。
- **路由有效。** 两个教师随机选（MinGain 1.7，完整方法 4.3）“removes the platform–expert correspondence and substantially reduces the balanced gain”。
- **自适应 mask 有效。** 对所有组施加 KL 得 37.1% / 10.3%；当某组奖励已足够时继续模仿”can unnecessarily restrict policy improvement”。
- **监督用在哪里。** 对学生访问状态上的师生动作分歧分析呈对角形态——每个专家在本平台给出更多有用纠错，且集中在低奖励组（Figure 4；百分比只出现在图内标签，本文不引用）。
- **集成基线。** 顺序 RL 依赖训练顺序（先移动 36.6% / 9.4%，先桌面 33.7% / 11.1%）；权重平均 36.5% / 6.8%；TIES 合并 36.8% / 0%。“All parameter-matched integration baselines underperform UI-MOPD on at least one platform.”

## 论文自己承认或未覆盖的薄弱处

- 全文没有任何种子、运行次数或方差报告，所有表格都没有误差线。
- 评测环境同时是采集环境：附录 B 写明功能点提取自”the original initialized OSWorld environments”与”the original initialized MobileWorld and AndroidWorld environments”。论文没有报告留出的应用或网站划分。
- 轨迹判定器与移动端采集器是同一个模型（Gemini-3.1-Pro）；判定记录未找到对该判定器的单独验证。
- 代码有链接，但判定记录把代码可得性标为 unclear；CUA Radar 没有运行过它。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **transfer**，子模式 R01。判定记录认可：OSWorld 与 MobileWorld 的在线评测、参数对齐的 8B 集成基线、以及固定学生与 Stage-2 数据的组件消融；预算对齐与成本报告记为 partial（给了硬件：8 节点共 64 张 H100）。标为 unclear 的证据项：留出环境、方差、代码。反模式未命中（AP7: no）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
