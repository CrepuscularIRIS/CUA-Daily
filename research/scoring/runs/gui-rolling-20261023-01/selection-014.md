# selection-014 — gui-rolling-20261023-01（第十四期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-11-10，本仓第十四期（单席串行）
- 不再入选：前十三期 42 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`–`selection-013.md`，`reel/README.md`）。本期 12 篇候选均不在其中
- 依据：本 run 最新 L2 记录（回填第五波 `batches/inc-l2-40.jsonl`、`inc-l2-41.jsonl` 11 篇 + `inc-l2-39.jsonl` 的 2601.15808，各自 supersede 对应 L1）。短名单从 arxiv.org/html（2611.11971v1、2404.09911v2、2403.08140v2、2601.15808v2 结构）或 PDF 文本层（2206.11795v1，无 HTML）按版本补读。转换稿与图在 /tmp/sel14，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 候选池（总控清单 12 篇）：逐篇核对为该 paper_id 的最新记录，均为 P3 / confirmed / to_l3
- 日期：2026-11-10。之后新增的 L2 或 correction 不计入本期

## 候选池（12 篇）与处理

全部 P3，无 P2；q3 中 capability 6 篇、judgment 6 篇，不分先后。第五波以 2021–2024 年经典为主，另有两篇 2026 年近作。先按“是否直接落在 GUI 操作回路上”与问题族分组，再看证据形态，并与前十三期同题去重。

标注：C = capability，J = judgment；“读”列 = 本期读到的范围（全文 = 正文 + 可得附录；节选 = 列出的节；L2 = 只依据 L2 记录与裁剪 core，未声称读过全文）。

| ID | 简称 | tier | q3 | 族 | 主卡 | 读 | 处理 |
|---|---|---|---|---|---|---|---|
| 2611.11971 | Harness Matters / WebTrap Farm | P3 | J | F1,F2 | environmental_injection_attacks | 全文（v1 §I–VIII、附录 A–E；图 3、4 读标注） | **入选** |
| 2206.11795 | VPT | P3 | C | F0,F4 | mine_human_screen_videos | 全文（v1 PDF 正文 + 附录 A–I） | **入选** |
| 2403.08140 | BAGEL | P3 | C | F3,F2 | exploration_driven_task_synthesis | 全文（v2 §1–10、附录 A–D） | **入选** |
| 2404.09911 | ChatShop | P3 | J | F2,F4 | online_evaluation_methodology | 全文（v2 §1–7；附录只看结构） | 编辑排除（证据形态 + 偏离核心），补注不退回 |
| 2601.15808 | DeepVerifier（推理时验证扩展） | P3 | J | F2,F5 | learned_outcome_and_process_judges | L2 + 摘要 | 编辑排除（偏离核心），近同题 → 2507.11662 |
| 2208.09116 | PIRLTest | P3 | C | F3,F4 | structured_screen_observation | L2 | 编辑排除（证据形态） |
| 2110.08653 | 宏动作示范导航 | P3 | C | F0,F1 | structured_screen_observation | L2 | 编辑排除（证据形态） |
| 2203.07828 | BUI-BERT | P3 | J | F3,F0 | structured_screen_observation | L2 | 编辑排除（证据形态） |
| 2312.06147 | LLM 网页元素检索 | P3 | J | F5,F0 | structured_screen_observation | L2 | 编辑排除（证据形态） |
| 2206.10352 | GUI 感知分组 | P3 | C | F4,F0 | structured_screen_observation | L2 | 编辑排除（偏离核心：离线感知，无代理） |
| 2410.08356 | SummAct | P3 | C | F0,F4 | unassigned | L2 | 编辑排除（偏离核心：离线意图摘要） |
| 2312.11444 | Gemini 语言能力 | P3 | J | F2,F1 | online_evaluation_methodology | L2 | 编辑排除（偏离核心） |

### 粗筛 → 短名单（5 篇）

2611.11971（外壳 vs 模型的安全归因）、2206.11795（录屏挖动作，唯一空白卡）、2403.08140（无监督探索合成示范）、2404.09911（WebShop 捷径审计）、2601.15808（只读结构，判断与 SGV 是否同题）。其余 7 篇依 L2 处理。

### 2611.11971 身份核对（L2 备注）

L2 标“ID 为 2026-11 而当前日期 2026-11-10，需核对发布时间 / 版本来源”。2026-11-10 查 export.arxiv.org/api：`2611.11971v1`，published = updated = 2026-11-09T06:53:04Z，标题 “Harness Matters: Measuring and Dissecting Security Resilience in Web Agents”，作者 Wu, Chen, Dong, Hong, Pan, Dai, Liu, Yang（复旦等），cs.CR；与 corpus.jsonl、缓存文件头一致。结论：真实 arXiv v1，钉定该版本。HTML 附录 E 附有 IEEE S&P 2027 元审稿，仅作参考。

## 1. 最终入选（3 篇）

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2611.11971 Harness Matters | J / F1,F2 | environmental_injection_attacks / injection_defense_isolation / online_evaluation_methodology | 改变一个评测判断：网页代理安全常被当作后端模型的属性。6 外壳 × 7 模型、505 个攻击任务，每个配去掉攻击的可用性任务，能力失败剔出分母，网页端埋点判分。同一 GPT-4o 下 Agent-E DSR 83.79 vs Skyvern 2.0 42.89（表 VI）；GLMM 外壳 χ² 331.17、模型 437.63、交互 299.81，均显著（表 VII）；完成率最高的 Skyvern 2.0 防御率倒数第二（图 4）；朴素攻击与显式攻击得手率相当（图 3）；四组受控消融（§V-B）。限制写进画报：受控自建页、单次运行（2 模型重跑三次 σ̄ 1.73）、DSR = 1 − ASR、消融为阶段条件指标且单次、保守外壳被剔出分母 |
| 2 | 2206.11795 VPT | C / F0,F4 | mine_human_screen_videos | 消除一个数据瓶颈：操作录屏没有动作标签。1,962 h 外包录像训练非因果 IDM（键 90.6%、鼠标 R² 0.97，留出数据），给约 70k h 网络视频打伪标签，训练 20 Hz 原生键鼠策略，含合成界面光标拖放；IDM 数据 ≥10 h 出现合成、约 100 h 平台（图 9）；RL 从早期游戏模型起步铁镐 >80%、钻石镐 2.5%，随机初始化几乎为 0（图 7）。**编辑理由**：游戏题材按前期口径通常排除，本篇检验的是“无标签录屏 → 动作标签 → 可执行策略”的管线而非游戏推理，接口是原生屏幕 + 键鼠，且 mine_human_screen_videos 是 18 张主卡里最后一张没有 Reel 的卡。限制写进画报：IDM / BC / RL 各训练一次；图 8 两侧同时换数据源与标签源；“$2,000”为外推；只在 Minecraft、GUI 只是任务链几步 |
| 3 | 2403.08140 BAGEL | C / F3,F2 | exploration_driven_task_synthesis / experience_memory_retrieval | 带来一种能力：无人工示范、不知测试指令时，在同一环境里自举示范。同一 PaLM-2 来回改写轨迹与指令，自打分后入库，测试时检索 3 条。MiniWoB++ 最难 10 任务 46.8 → 61.0（表 1；图 3 为 60.5），多轮均优于一次（表 1）；choose-date 报错 1.3 → 0.1（表 3）。限制写进画报：测试任务由同一零样本代理挑出；同一任务生成器；无方差；指令—轨迹配对拆解只在 ToolQA；人工按执行结果剔错还有 +7，说明自打分漏放错误示范 |

族覆盖（本期）：F1/F2 一篇，F0/F4 一篇，F3/F2 一篇。卡覆盖：**mine_human_screen_videos 首次入 Reel**（至此 18 张主卡均有 Reel）；environmental_injection_attacks 第四次（2610.41272、2611.04879、2611.04393 均测攻击本身，本篇测外壳 vs 模型的归因与能力校准，不同题）；exploration_driven_task_synthesis 第三次（2601.22781 测合成难度、2610.33907 测教程 + 原生命令采集，本篇是无监督“先轨迹后起名”，不同题）。年代：2022、2024、2026 各一。

## 2. 排除记录

### 2.1 读过原文的短名单

| ID | 处理 | 理由 |
|---|---|---|
| 2404.09911 ChatShop | 编辑排除（证据形态 + 偏离核心），补注不退回 | 已读 v2 正文。与 CUA 直接相关的只有 §3 对 WebShop 的捷径审计：用指令原文查内置 BM25，top-50 含满奖励商品 86.8%；BERT 排序器 dev 成功率 78.3 / 奖励 87.2。证据只有这一个数加一个排序器，且**脚注 4 说明排序器不做选项选择**，78.3 与 WebShop 含选项的成功率、人类 59.6 都不是同口径比较。ChatShop 环境本身是检索 + 对话 + 选择，没有 GUI 层级；与 2503.19537、2610.34735（agent_initiated_user_interaction）同属“该问时问不问”。**补注（不退回）**：L2 facts 第 1 条应注明脚注 4 的选项排除；该审计对第十一期 GiGPO（WebShop 文本模拟站）的解读有参考价值，已在本期记录，不改画报 |
| 2601.15808 DeepVerifier | 编辑排除（偏离核心），近同题 → 2507.11662 | 只读结构与 L2。被验证对象是深度研究代理的最终答案，浏览器只用于取证；“整体判官过于认可、分解后核验更可靠”与第十一期 SGV（MLLM 轨迹验证器太爱点头、先写该怎么做再判）同属 learned_outcome_and_process_judges 的同一问题，SGV 直接验证 GUI 轨迹。依 L2 不退回 |

### 2.2 依据 L2 与裁剪 core 的编辑处理（未声称读过全文）

- **证据形态**：2208.09116 PIRLTest（L2 自述仍缺同骨干组件消融、解析成本与状态混叠审计，缓存 §4 末截断；两个平台各自训练，不是跨平台迁移）；2110.08653 宏动作示范（无应用留出，L2 自述“不等于应用留出”）；2203.07828 BUI-BERT（OCR 由 HTML span 仿真，未见任务结果多为负，属诊断但规模小）；2312.06147（124 个 Mind2Web 样本、单次，示例数效应无重复）
- **偏离核心**：2206.10352（像素控件分组，离线感知，没有代理与下游任务）；2410.08356 SummAct（离线意图摘要，文本相似度与离线预测）；2312.11444（Gemini 语言能力综合评测，WebArena 只是其中一节）

`later_work`：本期 12 条记录未据 later_work 降级。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2611.11971 | v1 全文 §I–VIII、附录 A–E；图 3、4 SVG 渲染读标注；式与 p 值取自 HTML alttext | 同意 P3/confirmed。**补注（不退回）**：DSR = 1 − ASR；模型 χ² 大于外壳；保守外壳被剔出分母；消融单次、阶段条件指标 |
| 2206.11795 | v1 PDF 正文 §1–5、附录 A–I；图 3–9 栅格化读取 | 同意 P3/confirmed 与范围收窄。**补注（不退回）**：各训练一次；图 8 对照不干净；“$2,000”外推；外包数据损失 7 轮后上升 |
| 2403.08140 | v2 全文 §1–10、附录 A–D | 同意 P3/confirmed。**补注（不退回）**：facts 第 2 条“迭代减少执行错误”应为“+BAGEL vs 零样本”（表 3）；测试任务由零样本代理挑选；表 2 只在 ToolQA；图 3 / 表 1 平均不一致 |
| 2404.09911 | v2 正文 §1–7 | 同意问题档位；编辑排除，补注见 2.1 |
| 2601.15808 | 只看结构与 L2 | 依 L2；编辑排除 |
| 其余 7 篇 | 只依 L2 与裁剪 core | 依 L2 处理，未声称读过 |

版本复核：2026-11-10 查 export.arxiv.org/api，2611.11971 最新 v1、2206.11795 最新 v1、2403.08140 最新 v2、2404.09911 最新 v2，与读取版本一致。

## 4. correction / 待补

本期**无 correction**：入选三篇与 ChatShop 的 L2 判断都在原文证据范围内，发现的问题均为措辞或边界补注，记在第 3 节，不退回 Sol。

待补清单：沿用 selection-013 第 4 节，状态未变（2609.22308、2505.13934、2609.22086 等仍待巡检班补材料）。C-013-1（2602.03798）尚未见 Sol 修订记录，本期不处理。

## 5. 漏检抽查结果

本期没有新增抽查。

## 6. Reel 成品路径

各目录含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。实际打开渲染图做视觉 QA；DOM 探针核对卡片越界、SVG 文本越框、最小有效字号与内容底边；PDF 栅格化后与 PNG 并排对照；缩到 580 px 宽检查小屏可读性。Playwright 驱动本地 Chrome，`--disable-lcd-text`。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2611.11971 | `reel/2611.11971/` | 深海军蓝页眉 + 判卷决策条 + 外壳 × 模型 6×7 热力表（同列两格加框）+ χ² 条 + TCR–DSR 散点 + 朴素 vs 显式哑铃 + 双攻击面阶段格 + 消融前后点 + 模型 × 攻击面点图 | ready（四次渲染：标题三行、整页超出约 350 px、χ² 越界、标签重叠、浮点舍入；逐次修正） |
| 2206.11795 | `reel/2206.11795/` | 米黄底草绿页眉 + 规格卡 + 左栏通高科技树阶梯（4 色可达条）+ 人类 vs RL 条 + 四段横向流程 + IDM 小时刻度尺 + 合成界面示意 + 倍数对数条 + RL 起点条 + 数据规模分区点线 + 成本账 | ready（四次渲染：标题四行、底部留白约 220 px、越界、人类基线说明不准；补成本账与人类对比并修正） |
| 2403.08140 | `reel/2403.08140/` | 横格笔记本底 + 蓝竖条 + 斜放前提印章 + 循环改写图 + 例子动作胶囊（✗✗✓）+ 一次 / 多轮配对条 + 逐任务棒棒糖 + 自打分 vs 剔错 + 报错配对条 + 同期参照表 | ready（五次渲染：JS 错误致图空白、留白约 280 px、标签互压、超出约 130 px；逐次修正） |

索引：`reel/README.md` 新增第十四期一节；`README.md` 头部统计行由 42 改为 45（滚动 run 由 23 改为 26）。poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
