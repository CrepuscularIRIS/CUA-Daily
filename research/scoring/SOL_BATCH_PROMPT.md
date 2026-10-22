# 给 6.1 Sol 的批量评价提示词

规则版本 `problem-core-v1.1`。三个项目共用本文件，内容逐字相同。评价规则只看 [PROBLEM_CORE.md](PROBLEM_CORE.md)；本文件只规定怎样派发和交接。**不计算 G/M/X/E 四轴或 `screen_score`**；[SCORE_SPEC.md](SCORE_SPEC.md) 已停用。

你是当前 **CC 交互会话中的总控**。直接使用 CC 内置的 Subagent 功能派发，评价 Subagent 的 **model type 选择用户已经配置的 6.1 Sol**。若配置使用别名，沿用现有映射，不自行猜测或覆盖配置键。总控自己的模型无需更换。

**执行方式限定为 CC 内置 Subagent。不得另起无头 Claude：不调用 `claude -p` / `cc -p`，不使用 subprocess、tmux、shell 循环或 SDK 启动额外 Claude 会话，不创建模型 API 客户端、代理、调度器或适配器。** 若当前会话无法派发指定 model type，报告具体阻塞，不能静默换通道或换模型。

## 一次加载

总控读取 PROBLEM_CORE.md、本项目 PROBLEM_MAP.md、PROFILE.md（收录范围与证据等级）、仓库 docs/EVIDENCE.md 和 PATTERN_INDEX.md。评价依据是本项目 patterns/main、patterns/sub 的领域卡；不加载原 ResearchStudio 15＋31，不重建领域卡，不做新 idea 生成、全网 scoop 检索或完整 Open Scientist 循环。

用户会给出论文范围和材料目录。未给范围时，先固定当前待处理清单；不自动重跑全历史语料。旧 run 的数值、状态和提示词一律不作输入。

为本次建立独立 `research/scoring/runs/<run_id>/`，写 `run.md`：规则版本、当前 Git HEAD、卡片版本、模型实际可得身份、输入清单及材料位置/hash、L1 批大小、**L2 篇数与 token 上限**（PROBLEM_CORE 第 5 节）、实际并发。

完整原文、调用日志和私有材料放已有忽略目录；不要提交密钥或全文。没有用户正式授权开始执行时，只交付配置和提示词，不把文档准备写成评价完成。

## 材料准备

- **L1**：用脚本从已缓存原文切出摘要＋引言，保留章节定位；切不出则只给摘要，标 `material=abstract`。不另派模型给论文写摘要，不为全量重新下载。
- **L2**：给方法与主要实验的关键段，附章节/表号/页码。裁剪文本标 `core`，不能冒充 `full`。

## 派发

- 默认 **4 个 Subagent 并发**，每个负责一批，批次互不重叠。L1 每批 20 篇起；L2 每批 10–20 篇。按实际输入量调整，接近上下文或输出上限就拆批，不静默截断。
- **滚动补位**：任一批完成即核对、保存进度并补派下一批，不等整组完成。每个 paper ID/version 同时只属于一个活动批次；失败/超时的批次确认不再写入后才重派。
- 只重试失败或缺失的记录。持续限流时降低并发并按提示退避；额度和槽位允许且无持续限流时可逐步升至 6–8。三个项目共用额度时由用户分配总并发，不把各自默认值叠加。
- 不一篇一个 Subagent，不让 Subagent 再派子代理。总控只把本批需要的输入、规则和相关卡片交给 worker；不复制整个对话或其他批次的输出。

L1 任务正文：

> 你是 6.1 Sol 评价 Subagent，处理 run=<run_id>、batch=<batch_id>、stage=L1。读取 PROBLEM_CORE.md、本项目 PROBLEM_MAP.md 与本批输入，按机制打开相关主卡的“Cognitive barriers”“Failure modes”等章节。按 PROBLEM_CORE 第 3、4、7 节为每篇写一条 JSONL 到 `batches/<batch_id>.jsonl`。Q2 必须排除本文及其所有版本，只与本文首版之前的同题同条件工作比较。材料未知不降低 priority；无法判断记 null 或 needs_material，不记 P0。你只拥有这个输出文件，不写其他批次或共享文件，不操作 git，不再派 Subagent，不启动无头 Claude 或模型 API 调用。完成后只返回输出路径、覆盖数量和阻塞项。

L2 任务正文：

> 你是 6.1 Sol 评价 Subagent，处理 run=<run_id>、batch=<batch_id>、stage=L2。读取 PROBLEM_CORE.md、本批每篇的 L1 记录与方法/实验材料，并打开对应子卡。确认 q1_basis 与 q4_fit，按第 4 节更新 problem_tier、evidence_status、priority、next_action；按第 6 节填 subcard_checks：检查机制依赖的条件是否成立、关键失败是否排除，不检查论文是否照卡片步骤实现。每篇写一条 stage=L2 的新记录，supersedes 指向 L1 记录，不改 L1 原行。权限限制同 L1。

同一批中同一张卡只需读取一次；每篇仍逐篇核对证据。不强制档位分布，不设优秀比例，不因前面出现强论文而压低后面的论文。

## 总控核对与进度

- 保存 `batches/<batch_id>-inputs.tsv`。收到结果后核对：输入与输出 ID 一一对应、无重复漏行、枚举取值合法、封顶规则被遵守、`facts` 定位能在输入中找到。可用现有工具或小脚本；结构通过不等于科学判断正确。
- 更新 `progress.md`：L1 已处理、各档位数、`needs_material`、`out_of_scope`；L2 已用篇数与预算余量；**漏检抽查数及其中被改判的数量**。
- L1 全部完成后，总控按 PROBLEM_CORE 第 5 节排 L2 队列：先 `high` 再 `medium`，在预算内截断；另外固定 10% 预算从 P0/P1、F0、`needs_material`、`park` 中随机抽取，记录随机种子，抽中记录标 `audit_sample=true`。

## 交接

L2 完成或到达明确停止点后，按 [SELECTION.md](SELECTION.md) 产出候选名单，交 Opus 5.5 核对原文和制作 Reel。Opus 发现判断错误时写 correction 并退回该篇给 Sol 单篇修订，不直接改原记录。

只有总控按用户当次授权提交/推送，Subagent 不操作 git。只包含本次明确产物，不包含他人未提交文件。总结写覆盖、未完成、候选数、漏检抽查结果和文件位置；不虚报全量完成、准确率、用量或加速倍数。
