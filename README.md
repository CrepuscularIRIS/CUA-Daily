# CUA-Daily（原 CUA Radar — cua-architecture-radar）

`domain: GUI / computer-use agent` · `scoring: sol-batch-v3（gui-v3）` · `run: gui-v3-20261022-01` · `reel: 2026-10-22 · 9 篇` · `license: MIT`

## 高分速览（2026-10-22 · 前 30 篇 · 满分 100）

按初筛分排序的前 30 篇。paper 号链到海报的 9 篇即本期 Reel（含中文海报），其余链到 arXiv；前 15 行即 Opus 5.5 逐篇原文核对的 15 篇候选（[verify/](research/v3/runs/gui-v3-20261022-01/verify/)）。完整 1331 篇分数见 [index.jsonl](research/v3/runs/gui-v3-20261022-01/final/index.jsonl)。

| paper | 分 | G/M/X/E | 标题 | 机制一句话 | 链接 |
|---|---:|:-:|---|---|---|
| [2608.21794](reel/2608.21794/poster.png) | 100.0 | 4/4/4/4 | Lexical Coupling in GUI Element Grounding | 固定同屏候选集，对词法、语义检索器进行遮蔽、融合与簇级统计审计 | [arXiv](https://arxiv.org/abs/2608.21794) · [code](https://github.com/qijia123/lexical-coupling-release) |
| [2609.32036](reel/2609.32036/poster.png) | 100.0 | 4/4/4/4 | ScreenHaystack: Finding Blind Zones in GUI Grounding | 固定目标外观与指令遍历屏幕位置，以跨盲区迁移、区内平移和受控训练验证空间失效 | [arXiv](https://arxiv.org/abs/2609.32036) · [code](https://github.com/JigglypuffStitch/ScreenHaystack) |
| [2610.15138](reel/2610.15138/poster.png) | 100.0 | 4/4/4/4 | The Agent Clicks Approve: Injected Page Text Makes Browser Agents Authorize Access… | 用只含页面文本的注入诱导越权授权，以预先固定的任务权限包在服务端检查请求，区分尝试与真正完成 | [arXiv](https://arxiv.org/abs/2610.15138) · code — |
| [2610.26469](reel/2610.26469/poster.png) | 100.0 | 4/4/4/4 | VeriCUA: Learning Proactive Verification for Reliable GUI Agent Rewards | 训练 Judge 主动请求冻结 Probe 检查终态，以预先记录且对模型隐藏的执行真值奖励判断和取证 | [arXiv](https://arxiv.org/abs/2610.26469) · [code](https://github.com/Jeffjeno/VeriCUA) |
| [2610.26503](reel/2610.26503/poster.png) | 100.0 | 4/4/4/4 | ScopeMem: Latent Memory That Learns Where to Revise Frozen GUI Agents | 先隔离 latent prefix 的历史与修订作用，再以初答条件化前缀和正确步 KL 保留约束学习有范围的动作修订 | [arXiv](https://arxiv.org/abs/2610.26503) · code — |
| [2608.06065](reel/2608.06065/poster.png) | 96.25 | 3/4/4/4 | The Next Screenshot Knows: Gated Hindsight Distillation for Mobile GUI Agents | 训练时让教师读取下一屏，只在学生失败且教师动作与示范一致时蒸馏，部署保持因果学生 | [arXiv](https://arxiv.org/abs/2608.06065) · code — |
| [2609.05511](https://arxiv.org/abs/2609.05511) | 96.25 | 3/4/4/4 | SCAFFOLD: Self-Improving Web Agents via Recursive Parametric Skill Abstraction | 从多实例成功轨迹归纳递归技能，用 MDL 合并修剪、执行验证和守卫维护技能库，再蒸馏回策略 | [arXiv](https://arxiv.org/abs/2609.05511) · [code](https://github.com/BokwaiHo/SCAFFOLD) |
| [2610.05185](reel/2610.05185/poster.png) | 96.25 | 3/4/4/4 | Recurrent Latent Visual Search for GUI Grounding | 在一次截图编码上循环更新空间注意力，用粗到细候选框监督中间搜索，再以确定性局部峰值读出坐标 | [arXiv](https://arxiv.org/abs/2610.05185) · code — |
| [2504.01382](reel/2504.01382/poster.png) | 95.0 | 4/4/3/4 | An Illusion of Progress? Assessing the Current State of Web Agents | 审计旧任务的失效与搜索捷径，构建 Online-Mind2Web 并以关键截图 WebJudge 核验轨迹 | [arXiv](https://arxiv.org/abs/2504.01382) · [code](https://github.com/OSU-NLP-Group/Online-Mind2Web) |
| [2605.07630](reel/2605.07630/poster.png) | 95.0 | 4/4/3/4 | Safe, or Simply Incapable? Rethinking Safety Evaluation for Phone-Use Agents | 将手机风险下一动作拆成安全、危险和无有效动作，并用条件安全率剥离能力失败造成的表面安全 | [arXiv](https://arxiv.org/abs/2605.07630) · [code](https://github.com/tangzhy/PhoneSafety) |
| [2609.27273](https://arxiv.org/abs/2609.27273) | 95.0 | 4/4/3/4 | CAVEAT: Towards Robust Computer-Use Agents in Incentive-Misaligned Environments | 在九类浏览器市场构建唯一用户最优商品，固定目录和请求，仅切换八类平台引导机制做配对实验 | [arXiv](https://arxiv.org/abs/2609.27273) · [code](https://github.com/microsoft/CAVEAT) |
| [2610.07444](https://arxiv.org/abs/2610.07444) | 95.0 | 4/4/3/4 | Decoupling What from Where: How Should a Small GUI Grounding Model Receive the Action Type? | 在匹配小模型实验中拆分动作类型传递方式，并用非空间事件清理、条件干预和位置编码控制诊断表面增益 | [arXiv](https://arxiv.org/abs/2610.07444) · [code](https://github.com/aadcha/action-conditioned-gui-agent) |
| [2610.12823](https://arxiv.org/abs/2610.12823) | 95.0 | 4/4/3/4 | When Charts Deceive Web Agents: A Paired Benchmark for Misleading Visualization-Grounded Tasks | 固定网页任务和执行评分，只替换干净/误导图表形成配对，追踪陷阱一致的提交与恢复 | [arXiv](https://arxiv.org/abs/2610.12823) · code — |
| [1802.08802](https://arxiv.org/abs/1802.08802) | 90.0 | 4/4/4/3 | Reinforcement Learning on Web Interfaces Using Workflow-Guided Exploration | 从少量示范归纳工作流约束格，以环境盲探索策略发现成功回合，再回放训练 DOM 神经策略 | [arXiv](https://arxiv.org/abs/1802.08802) · [code](https://github.com/stanfordnlp/wge) |
| [2112.09332](https://arxiv.org/abs/2112.09332) | 90.0 | 4/4/4/3 | WebGPT: Browser-assisted question-answering with human feedback | 让语言模型操作文本浏览器搜寻引用，结合人工示范、偏好奖励、PPO 及最佳样本筛选生成有来源答案 | [arXiv](https://arxiv.org/abs/2112.09332) · code — |
| [2210.03347](https://arxiv.org/abs/2210.03347) | 90.0 | 4/4/4/3 | Pix2Struct: Screenshot Parsing as Pretraining for Visual Language Understanding | 以截图到可见简化 HTML 的掩码解析预训练，配合保持长宽比的可变分辨率 patch | [arXiv](https://arxiv.org/abs/2210.03347) · [code](https://github.com/google-research/pix2struct) |
| [2306.00245](https://arxiv.org/abs/2306.00245) | 90.0 | 4/4/4/3 | From Pixels to UI Actions: Learning to Follow Instructions via GUIs | Pix2Act 用截图到通用鼠标键盘动作的策略，先模仿再以 MCTS 生成轨迹继续监督训练 | [arXiv](https://arxiv.org/abs/2306.00245) · [code](https://github.com/google-deepmind/pix2act) |
| [2307.13854](https://arxiv.org/abs/2307.13854) | 90.0 | 4/4/4/3 | WebArena: A Realistic Web Environment for Building Autonomous Agents | 以自托管真实功能网站和状态检查器替代简化网页及动作串匹配 | [arXiv](https://arxiv.org/abs/2307.13854) · [code](https://github.com/web-arena-x/webarena) |
| [2310.03720](https://arxiv.org/abs/2310.03720) | 90.0 | 4/4/4/3 | SteP: Stacked LLM Policies for Web Actions | 用可递归调用的手写策略栈分解 Web 操作，子策略维护局部历史，返回后恢复父策略 | [arXiv](https://arxiv.org/abs/2310.03720) · [code](https://github.com/asappresearch/webagents-step) |
| [2402.04476](https://arxiv.org/abs/2402.04476) | 90.0 | 4/4/4/3 | Dual-View Visual Contextualization for Web Navigation | 将 DOM 候选与截图空间近邻的文本/视觉特征共同编码，分别增强元素排序与动作多选预测 | [arXiv](https://arxiv.org/abs/2402.04476) · code — |
| [2404.07972](https://arxiv.org/abs/2404.07972) | 90.0 | 4/4/4/3 | OSWorld: Benchmarking Multimodal Agents in Real Computer Environments | 将桌面任务放入可重置 VM，以初态配置和读取实际文件、应用状态的执行检查器判分 | [arXiv](https://arxiv.org/abs/2404.07972) · [code](https://github.com/xlang-ai/OSWorld) |
| [2404.16660](https://arxiv.org/abs/2404.16660) | 90.0 | 4/4/4/3 | Benchmarking Mobile Device Control Agents across Diverse Configurations | 建立带规则成功检测器的 Android 任务，随机化设备、语言、布局等配置并比较训练和测试环境 | [arXiv](https://arxiv.org/abs/2404.16660) · [code](https://github.com/jylee425/b-moca) |
| [2405.14573](https://arxiv.org/abs/2405.14573) | 90.0 | 4/4/4/3 | AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents | 把 Android 任务封装为带随机参数的初始化、执行检查和清理单元，以设备内部状态判定结果 | [arXiv](https://arxiv.org/abs/2405.14573) · [code](https://github.com/google-research/android_world) |
| [2406.07822](https://arxiv.org/abs/2406.07822) | 90.0 | 4/4/4/3 | Tell Me What's Next: Textual Foresight for Generic UI Representations | 以当前屏幕和动作框预测下一屏文字摘要的预训练目标，连接局部元素语义与全局屏幕表示 | [arXiv](https://arxiv.org/abs/2406.07822) · [code](https://github.com/aburns4/textualforesight) |
| [2407.01511](https://arxiv.org/abs/2407.01511) | 90.0 | 4/4/4/3 | CRAB: Cross-environment Agent Benchmark for Multimodal Language Model Agents | 将跨桌面/移动端任务写成带类型输入输出和状态验证器的子任务依赖图，以图进度和整任务完成评测代理 | [arXiv](https://arxiv.org/abs/2407.01511) · [code](https://github.com/camel-ai/crab) |
| [2407.05291](https://arxiv.org/abs/2407.05291) | 90.0 | 4/4/4/3 | WorkArena++: Compositional Planning and Reasoning-based Knowledge Work Tasks | 把 ServiceNow 原子任务及验证器组合为显式流程 L2 和需从工单/知识库推导流程的 L3 任务 | [arXiv](https://arxiv.org/abs/2407.05291) · [code](https://github.com/ServiceNow/WorkArena) |
| [2407.10956](https://arxiv.org/abs/2407.10956) | 90.0 | 4/4/4/3 | Spider2-V: How Far Are Multimodal Agents From Automating Data Science Workflows? | 将真实数据分析软件流程做成可快照重置的 VM 任务，以文件、API 及执行日志检查结果 | [arXiv](https://arxiv.org/abs/2407.10956) · [code](https://github.com/xlang-ai/Spider2-V) |
| [2410.05243](https://arxiv.org/abs/2410.05243) | 90.0 | 4/4/4/3 | Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents | 用 HTML 派生的多样指代表达训练高分辨率像素 grounder，再接自然语言规划接口 | [arXiv](https://arxiv.org/abs/2410.05243) · [code](https://github.com/OSU-NLP-Group/UGround) |
| [2411.02391](https://arxiv.org/abs/2411.02391) | 90.0 | 4/4/4/3 | Attacking Vision-Language Computer Agents via Pop-ups | 在代理观察中绘制含用户意图钩子和点击指令的假弹窗，改变内容与防御后分别测点击和任务结果 | [arXiv](https://arxiv.org/abs/2411.02391) · [code](https://github.com/SALT-NLP/PopupAttack) |
| [2503.15661](https://arxiv.org/abs/2503.15661) | 90.0 | 4/4/4/3 | UI-Vision: A Desktop-centric GUI Benchmark for Visual Perception and Interaction | 用密集人类演示构造元素、布局及独立步骤动作预测三层桌面评测 | [arXiv](https://arxiv.org/abs/2503.15661) · [code](https://github.com/uivision/UI-Vision) |

> 分档参考：≥95 分 13 篇 · ≥90 分 104 篇 · ≥85 分 308 篇 · ≥80 分 483 篇；中位 75.0；满分 100 共 5 篇。
> 90.0 分并列 91 篇，表中第 14–30 行是其中 arXiv 编号最早的 17 篇，并列不分先后，其余见 [index.jsonl](research/v3/runs/gui-v3-20261022-01/final/index.jsonl)。
> 分数为**选读初筛优先级，非审稿分**。2609.05511 因 transfer 证据无法核对（needs_material），未入 Reel。
> code 链接已逐个打开 repo 与论文互证；`code —` 表示未找到可确认的官方代码/项目页，不代替猜测。

## 范围与核心问题

GUI / 计算机使用 agent 雷达：在桌面、移动端或 Web 界面感知并执行动作的 agent，及其架构、grounding、训练、环境模型、benchmark 与 verifier。纯 API agent、只生成 UI 代码、具身机器人不在范围内。

核心问题：**改变了感知—规划—动作—反馈中的哪一环，在线任务是否真的完成，提升来自该环还是更强的模型/更多步骤？**

## 从这里开始

| 内容 | 入口 |
|---|---|
| 本期 Reel | [reel/README.md](reel/README.md)：9 篇海报索引，版式骨架 9 种互不相同 |
| 评分全量 | [final/index.jsonl](research/v3/runs/gui-v3-20261022-01/final/index.jsonl)：1331 篇逐篇 JSONL |
| 高分表数据 | [top30.tsv](research/v3/runs/gui-v3-20261022-01/top30.tsv)（分数/四轴/claim_support）＋[code_links.tsv](research/v3/runs/gui-v3-20261022-01/code_links.tsv) |
| 选择过程 | [selection.md](research/v3/runs/gui-v3-20261022-01/selection.md)＋[verify/](research/v3/runs/gui-v3-20261022-01/verify/)（15 篇候选核对记录） |
| 评分规则 | [SCORE_SPEC](research/v3/SCORE_SPEC.md)（`sol-batch-v3`）；本次 run 记录见 [run.md](research/v3/runs/gui-v3-20261022-01/run.md) |
| 流程文档 | [PIPELINE](docs/PIPELINE.md)；[维护规则](docs/MAINTAINING.md)；[收录范围](docs/EVIDENCE.md)；[设计依据](docs/DESIGN_BASIS.md) |
| 模式卡 | [overview](patterns/overview.md)（GUI 领域 18 主卡 / 75 子卡）；[原 15+31 冻结副本](research/reference/researchstudio-15-31/) |
| Grok 收集 | [GROK_PROMPT](docs/agents/GROK_PROMPT.md)：只收有一手证据的候选，写入 `inbox/` |

## 模型分工

| 环节 | 模型 | 做什么 |
|---|---|---|
| 收集 | **Grok** | 定时收集候选写入 `inbox/`，不打分、不做海报 |
| 初筛 | **6.1 Sol** | 单模型批量评分（`sol-batch-v3`）：四轴 G/M/X/E，gui-v3 权重 15/25/20/40，满分 100 |
| 核对＋海报 | **Opus 5.5** | top15 候选逐篇读原文核对数字与主张 → ≤9 篇制作中文海报（Reel）并视觉 QA |

| 轴 | 含义 | 权重 |
|---|---|---:|
| G | Gap 与问题位置 | 15 |
| M | 方法质量与 problem-fit | 25 |
| X | 机制执行与模式条件 | 20 |
| E | 主张的证据支撑 | 40 |

缺材料记 `needs_material`，总分为 null，不冒充低分；作者声称与材料支持分开记录（`claim_support` / `evidence_level`）。

## 本期 Reel（2026-10-22 · 9 篇 · 全部核对通过）

|  |  |  |
|---|---|---|
| [![](reel/thumbs/2608.21794.jpg)](reel/2608.21794/poster.png) | [![](reel/thumbs/2609.32036.jpg)](reel/2609.32036/poster.png) | [![](reel/thumbs/2610.15138.jpg)](reel/2610.15138/poster.png) |
| **2608.21794** 检索器文本依赖审计 | **2609.32036** 48k 探测定位空间盲区 | **2610.15138** 页面文本注入 vs 服务端权限门 |
| [![](reel/thumbs/2610.26469.jpg)](reel/2610.26469/poster.png) | [![](reel/thumbs/2610.26503.jpg)](reel/2610.26503/poster.png) | [![](reel/thumbs/2608.06065.jpg)](reel/2608.06065/poster.png) |
| **2610.26469** Judge 主动请求冻结 Probe 核验 | **2610.26503** latent prefix 隔离修订 | **2608.06065** 下一屏教师门控蒸馏 |
| [![](reel/thumbs/2610.05185.jpg)](reel/2610.05185/poster.png) | [![](reel/thumbs/2504.01382.jpg)](reel/2504.01382/poster.png) | [![](reel/thumbs/2605.07630.jpg)](reel/2605.07630/poster.png) |
| **2610.05185** 单截图循环空间注意力 | **2504.01382** 旧基准失效与捷径审计 | **2605.07630** 风险三分类＋条件安全率 |

每篇目录含 `poster.png/pdf`、`SOURCE.md`（数字→原文定位）、`QA.md`；可编辑源 `poster.html` 受旧 ignore 规则约束，仅存本地。

## 当前状态（run `gui-v3-20261022-01` · 2026-10-22）

- **覆盖 1331 篇**（A/B 档全部 1328 ＋ 当日新入库 3）：1176 scored / 93 `needs_material` / 62 `out_of_scope`；25 篇 contradicted / unresolved 列入问题清单。
- **批次**：97＋1 批，机械校验全部通过。
- **核对**：top15 候选 15/15 全核，14 篇 verify_ok、1 篇 needs_material（2609.05511 的 transfer 证据无法核对，未入 Reel）。
- **Reel**：9 篇，全部 Opus 核对通过、视觉 QA ready，版式骨架互不相同。

## 持续维护

流程：Grok 收集 → 6.1 Sol 批量初筛 → top15 候选 → Opus 5.5 逐篇原文核对 → ≤9 篇 Reel。Grok 按 [GROK_PROMPT](docs/agents/GROK_PROMPT.md) 定时把新候选写入 `inbox/`，入库后进入后续评分与 Reel 期次；评分权重、rubric 与模式卡不随日常评审改动，规则见 [MAINTAINING](docs/MAINTAINING.md)。

## 目录结构

```
inbox/                                   Grok 收集记录
patterns/overview.md                     GUI 领域模式卡（18 主卡 / 75 子卡）
research/reference/researchstudio-15-31/ 原 15+31 方法卡冻结副本
research/v3/
  ├── SCORE_SPEC.md                      sol-batch-v3 评分规则（gui-v3 权重）
  └── runs/gui-v3-20261022-01/
      ├── run.md                         规则版本、模型、输入快照
      ├── batches/                       各批评分记录
      ├── selection.md                   候选与入选理由
      ├── verify/                        15 篇候选原文核对
      ├── top30.tsv · code_links.tsv     高分速览数据与代码链接
      └── final/index.jsonl              1331 篇全量评分
reel/                                    每期海报 <paper_id>/ ＋ thumbs/ 缩略图 ＋ 索引
docs/                                    PIPELINE、MAINTAINING、EVIDENCE、DESIGN_BASIS、agents/ 提示词
```

## Related awesome lists

语料从以下列表收集 arXiv id 与章节标题（本地快照在 `refs/lists/`，不随仓库提交）。它们覆盖面比本雷达更广：

- [OSU-NLP-Group/GUI-Agents-Paper-List](https://github.com/OSU-NLP-Group/GUI-Agents-Paper-List)
- [reacher-z/Awesome-CUA](https://github.com/reacher-z/Awesome-CUA)
- [showlab/Awesome-GUI-Agent](https://github.com/showlab/Awesome-GUI-Agent)
- [ZJU-REAL/Awesome-GUI-Agents](https://github.com/ZJU-REAL/Awesome-GUI-Agents)
- [trycua/acu](https://github.com/trycua/acu)
- [ranpox/awesome-computer-use](https://github.com/ranpox/awesome-computer-use)
- [steel-dev/awesome-web-agents](https://github.com/steel-dev/awesome-web-agents)

## Credits and license

MIT（见 [LICENSE](LICENSE)）。
- **Base pipeline** 经 [HarnessRSI Daily](https://github.com/CrepuscularIRIS/HarnessRSI-Daily)，源自
  [yang3kc/daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest)（MIT）。
- **Pattern cards**：方法卡来自 ResearchStudio Idea 原 15+31（保留原 LICENSE）；领域卡借助 Open Scientist（gui domain）归纳。
