# InfiniteWeb：把整个训练场馆一起合成——带稠密评估器的功能性网站，可规模化生成

*CUA Radar 对 arXiv 2601.04126v3（Zhang、Wang、Zhang、Guo、Li、Li、Lu；北京大学、南京大学、微软亚洲研究院）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2601.04126v3 · 代码（论文摘要所列）：https://github.com/microsoft/FIVE-UI-Evol*

## 问题：瓶颈是环境，不是任务

用 RL 训练 GUI agent 需要可交互的环境，而现有基准——Mini-WoB++、WebArena、OSWorld——都是人工搭建的：只有几十到几百个应用，每个都要人来设计网站或安装应用、定义任务、编写评估标准。近期的合成工作生成的是任务或轨迹，但仍然在这些基准环境内部打转。论文追问：环境本身能否自动生成？并指出让 LLM 朴素地生成完整网站有三个障碍：**consistency**（各页面独立生成会在数据格式、接口签名和状态管理上互相矛盾，破坏跨页交互）、**correctness**（功能 bug 在长程任务里复利累积，产生错误奖励信号，“destabilize reinforcement learning”）、**diversity**（任务模式和视觉风格同质化，有过拟合风险）。

## InfiniteWeb 是什么

论文里有两个角色。**生成器**是一条以 GPT-5（reasoning effort 为 “high”）为骨干的 agent 流水线，输入是网站种子（一段简短描述）和参考设计图，两者都采样自 Common Crawl。随后是四个阶段，后端与前端并行：

1.  **Unified Specification。** 先为种子生成 8–10 个真实用户任务，再从任务推导出共享的数据模型和面向用户的接口。所有页面实现同一份规范；userId、sessionId 等系统参数被隐藏，状态存放在 localStorage，“It enables data persistence across pages without a backend server”。
2.  **Task-Centric Backend（TCTDD）。** 生成与任务一致的具体数据；从任务规范导出测试用例，然后迭代修复实现代码直到所有任务相关测试通过（最多 8 轮；1.5% 的网站未能修复）。正确性只要求覆盖任务诱导的子空间，而非整站。
3.  **Design-Guided Frontend。** 视觉语言模型从设计图提取色彩体系、字体、间距与组件样式；先生成统一页面框架，再生成各页面的 HTML/CSS/JS，调用后端 SDK。
4.  **Automatic Evaluator Generation。** 关键函数执行时向 localStorage 写入 instrumentation 检查点；生成的 JavaScript evaluator 以加权检查点（如 0.35 / 0.30 / 0.35）合成 0.0–1.0 的稠密分数，允许部分得分。

**受训者**是 UI-TARS-1.5-7B：输入 screenshot，输出底层 GUI 动作。它在生成的网站上用 GRPO 以稠密奖励训练（600 个任务、每任务 8 条轨迹、每 episode 最多 15 步、128 个并行环境）。在 CUA Radar 板上这属于子模式 K13——从 checker/规范出发合成任务，让可验证奖励由构造保证——挂在主模式 “ground reward in executable checkers” 之下。

## 论文报告的结果

以下 agent 数字全部是**在线**成功率。每一行都是同一个受训模型 UI-TARS-1.5-7B；OSWorld 用 OSWorld-Verified、15 步上限；标准差为三次运行的值（论文给出处）。

| 训练数据 | Online-Mind2Web（真实网站） | OSWorld（桌面） | MobileWorld（移动） |
|----|----|----|----|
| 原始 UI-TARS-1.5-7B | 23.0 ± 0.9 | 24.5 ± 1.2 | 6.4 |
| Claude-Code 网站，600 任务 | 23.7 | 25.2 | 5.1 |
| InfiniteWeb，200 任务 | 25.3 ± 1.0 | 27.3 ± 0.9 | — |
| InfiniteWeb，400 任务 | 27.3 ± 1.4 | 29.7 ± 1.1 | — |
| InfiniteWeb，600 任务 | 28.7 ± 1.2 | 31.4 ± 1.0 | 10.3 |

论文报告提升 +6.9（OSWorld）、+5.7（Online-Mind2Web）、+3.9（MobileWorld）。同一 15 步上限下，Table 2 还列出 Claude-4-Sonnet 31.2、Doubao-1.5-thinking-0428 28.1、OpenCUA-32B 29.7 ± 1.1。论文把 Online-Mind2Web 称为 in-domain 泛化（训练中从未见过的真实网站）、OSWorld 为 out-of-domain 迁移、MobileWorld 为移动迁移。

另一条轴衡量的是生成网站本身，而非受训 agent。在 WebGen-Bench（101 个网站；由 LLM agent 在每个生成站点上执行预定义任务）上，三次运行的任务完成率为：InfiniteWeb 85.6 ± 1.2、Codex 80.8 ± 0.4、Claude-Code 75.8 ± 2.4、Bolt.diy 67.1 ± 1.8，所有基线都用 GPT-5。LLM-as-judge 视觉对比中，InfiniteWeb 对 Claude-Code 胜率 85.4 ± 0.5、对 Bolt.diy 84.2 ± 0.8、对 Codex 69.3 ± 0.7。在生成的环境上，UI-TARS-1.5-7B 得 7.4、Agent S2 得 14.1，而在 OSWorld 上分别是 24.5 和 27.3，论文据此认为生成环境难度更高、对 agent 能力差异更敏感。

## 论文自带的对照实验

- **质量 vs 数量。** 同样的 600 任务 GRPO 预算换成 Claude-Code 生成的网站，提升边际甚至为负（Online-Mind2Web +0.7、OSWorld +0.7、MobileWorld −1.3）；论文结论是 “data quality, not quantity, drives the improvement”。Claude-Code 网站平均 4.9 页，InfiniteWeb 为 12.6 页。
- **消融。** WebGen-Bench 上，去掉 TCTDD 循环为 82.6 ± 1.4，把 GPT-5 换成 GPT-4.1 为 77.4 ± 1.4，完整系统 85.6 ± 1.2。注意论文内部有一处不一致：正文把 TCTDD 的损失写作 5.0 个点（降到 80.6），而 Table 6 列的是 82.6 ± 1.4；骨干模型的损失正文写为 8.2 个点。
- **稠密 vs 二值奖励。** 在 4,000 个任务、每任务 4 条轨迹上，稠密奖励下有 767 个任务对 GRPO 可判别，二值奖励下只有 174 个——可用训练信号扩大 4.4×。
- **统计检验。** Welch’s t-tests 确认了 WebGen-Bench 上对三个基线的差距，以及 Online-Mind2Web 上各任务数量档的增益。
- **成本。** 生成一个网站约消耗 0.36M 输入与 0.34M 输出 token——按 GPT-5 batch 定价约 \$1.93，中位耗时 20 分钟；600 个网站并行约 125 分钟生成完毕，生成只占总训练时间的 6.9%。论文对照 OSWorld 约 1,800 人时建 369 个任务。
- **人工抽查。** 100 个抽样视觉对比中，人类评估者与 GPT-5 judge 的一致率为 91%；100 个抽样任务中 95 个通过了对任务描述与自动评估器的人工核验。

## 论文自己承认的薄弱处

- “Our current tasks operate within individual websites. Cross-website tasks, such as comparing prices across multiple shopping sites … represent an important real-world scenario not yet covered.”（OSWorld 的多应用任务确有提升：3.8 到 9.7。）
- “our current system only generates web environments”——尽管有 MobileWorld 迁移，原生移动应用环境的生成仍是未来工作。
- 生成成本与延迟 “remains an engineering direction”：每站 \$1.93、中位 20 分钟。
- CUA Radar 的记录另指出：生成的评估器只经过 100 个任务的人工抽查；训练混合中不包含任何真实环境。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **transfer**。分数反映论文所报告的证据：三个真实基准上的在线评测、held-out 环境、三次运行的方差加 t 检验、成本报告、组件消融。判定记录同时标出：训练混合纯合成（反模式 AP2，生成环境没有真实锚点）；生成的评估器被记录为未作为 judge 验证（validator check “untested”，对应论文自身 95/100 的抽样人工核验）；strong-baseline 与 budget matching 记录为 partial；代码记录为 announced 而非已发布，尽管论文摘要给出了 github.com/microsoft/FIVE-UI-Evol 链接。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v3）。
