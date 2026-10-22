# GUI Agents：先研究分析与评分，再精选 Reel

当前：旧分数/Reel 已归档；已有模式卡保留；v2.2 是待校准设计，尚无新分数或新画报。
[设计依据](DESIGN_BASIS.md) → [评分规则](../research/SCORE_SPEC.md) → [逐篇工作表](../research/REVIEW_WORKSHEET.md)。

## 一次性准备与按证据更新

先核既有语料、签名、Harness 模式卡和 reviewer expectations 的来源/适用范围。
从实际研究操作及成功/失败条件逆向形成卡片；没有真实审稿就使用有来源的审稿期望。
现有卡片已完成，先复用；只有资料缺口或新反证触发定向补读、修订建议和版本更新。
再将期望映射到评分轴，做开发/留出校准、冻结 rubric。Open Scientist 建议安装到 CC，用 study 支持缺口诊断与独立审阅。
不把安装完成、卡片存在或结构检查通过当作评分已经可靠。

## 每批流程

1. **Grok 收集**：[GROK_PROMPT](agents/GROK_PROMPT.md)。一手来源、明确操作/实验的候选写 inbox，保留当前统一格式；不打分、不生成 Reel。
2. **核对与入库**：检查 ID/title/version、原始来源与重复。`python3 research/ingest.py inbox/<batch>.jsonl` 只处理新 arXiv ID；
   已有 ID 的版本更新单独处理，无 arXiv ID 的正式材料保留 inbox 独立核对。确认逐行有处理结果后才移动到 processed。
3. **完整阅读与签名**：固定全文/附录及 hash。旧裁剪全文只可作索引；缺材料标 needs_fulltext。先提取改了什么、怎么选择与留存、信息权限、对照和结果，不评分。
4. **Gap identify 与谱系**：核作者 gap、最近邻、祖先/前沿残余与代价；说明本文机制如何回应它，以及还剩什么。不是每篇强行生成一个新 idea。
5. **模式与审稿期望**：严格按原15+31做识别，再记录本领域卡与逐篇映射；按真实操作选卡或有理由的 outside_taxonomy，逐项核生效条件、失败边界和适用 expectation；无真实 review 不跳过此步。
6. **双席证据判定与评分**：6.1 Sol 与 Sonnet 5.5 独立初评，Opus 5.5 逐篇聚合。[LOCAL_SCORING_PROMPT](agents/LOCAL_SCORING_PROMPT.md)。核主张-证据矩阵，尤其留存改动在之后任务上是否有效；
   写独立的 evidence_level 与 claim_support，再按冻结权重计算 G/M/X/E；独立语义审核通过才成为有效分数。
7. **动态选题**：[REEL_SELECTION](REEL_SELECTION.md)。先过质量底线，再按数量上限/可选机制限额挑选；默认最多 9 篇，不凑数量。
8. **GLM 5.3 / Reel 画报**：[REEL_PROMPT](agents/REEL_PROMPT.md)。只处理有效 selection；paper2assets → 内容策划 → paper2poster → 图文核验与渲染 QA → 精选入口。

证据不足返回阅读/检索；机制条件冲突返回审阅；Reel 发现新反证返回判定。不是走完步骤就自动通过。
日常改阈值只重选题，改论文判断须重审，改 rubric/卡片须新版本并复核受影响分数。

## 数据与边界

| 资产 | 位置 / 状态 |
|---|---|
| 原始语料/全文 | research/corpus.jsonl、research/fulltext/（本地；旧缓存可能裁剪） |
| 既有逆向模式卡 | patterns/、research/patterns/；保持原件 |
| 历史线索 | research/screen.jsonl、research/patterns/assignments.jsonl；不能直接当新判断 |
| 新版阅读、校准、判断、选题 | research/v2/；当前只有说明，拟分开 readings/calibration/judgments/selections |
| 旧分数/Reel/运行记录 | archive/2026-10-21-reset/；不进入新评分输入 |
| 对外画报 | reel/；只容纳选中且完成 QA 的新成品 |

旧 scorer、board、merge/batch、monitor 与 Reel 批量入口继续返回退役错误。
新版 scorer/selector/publisher 尚未实现；本次没有批量评审、抓取、启动 Grok Bot 或运行研究实验。

## 大语料执行入口

直接把 [LOCAL_SCORING_PROMPT](agents/LOCAL_SCORING_PROMPT.md) 交给 claude-kimi（Claude Code）；model type 已配置，直接沿用。默认每批5篇、每轮并行2批，双席独立初评后 Opus 逐篇聚合、总控验收并开下一轮。
只有总控写共享索引和最终提交，worker 各写独立 attempt；断点恢复依赖材料/规则/输出 hash，不靠文件存在。格式与检查见 [BATCH_CONTRACT](../research/BATCH_CONTRACT.md)。
本轮只准备了完整提示词与原卡参考包；没有启动这些模型，也没有新增批量评分结果。
