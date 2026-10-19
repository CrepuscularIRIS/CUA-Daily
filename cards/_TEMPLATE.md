---
# 机器可读字段：CI 会校验这些 key 是否存在、取值是否在枚举内
id: slug-lowercase
title: "Full Paper Title"
authors: "First Author et al."
first_seen: YYYY-MM-DD          # arXiv v1 / OpenReview 首次公开日期
arxiv: "XXXX.XXXXXvN"           # 本卡实际读的版本；无则 null
openreview: null                # forum URL；无则 null
code: "https://github.com/owner/repo"   # 官方仓库；无则 null
code_commit: null               # 核查时的 SHA；未核查则 null
license: null                   # 仓库 LICENSE 原文类型；未确认则 null
venue: "arXiv preprint"         # 或 "ICLR 2027 submission" 等
tier: A                         # A=CUA 架构/训练/环境模型方法；B=可直接用于 CUA 的组件或方法学（见 docs/EVIDENCE.md）
platforms: [web]                # 子集：web|mobile|desktop|general
components: [grounding]         # 子集：perception|grounding|planning|action_space|memory|reflection|world_model|simulator|training_data|rl|reward_judge|policy|multi_agent|evaluation|safety|efficiency
evidence_level: offline         # offline|online|transfer —— 我们判定的、有证据支持的最高级
held_out: unclear               # yes|partial|no|unclear —— 评测应用/网站是否与训练、合成、探索、孪生校准所用的隔离
budget_matched: unclear         # yes|partial|no|unclear —— 与基线的比较是否预算对等
leakage_risk: unclear           # low|medium|high|unclear
code_status: released           # none|announced|released|verified_run
checked: YYYY-MM-DD
---

## 一句话
它改了感知 → 规划 → 执行 → 学习闭环里的哪一部分，属于哪个模式卡（`Kxx` / `Cxx` / `Rxx`），用什么证据支撑。

## 机制
观察表示、规划与 grounding、动作空间、记忆/反思、训练数据与奖励、环境模型，各一两句（只写论文涉及的部分）。
如果有学习型 judge、reward model、world model 或数字孪生，指出它在 agent 与真值之间的位置。

## 作者报告的证据
只转述作者的数字，并写清模型、任务、预算。不跨论文比较数值。

## 我们的诊断
- **证据等级**：为什么是 offline / online / transfer（定义见 [docs/EVIDENCE.md](../docs/EVIDENCE.md)）。
- **留出与泄漏**：训练、合成、探索或校准用了哪些应用/网站，评测又在哪些上；评测器或答案是否对系统可见。
- **验证器**：成功率若由 LLM judge / reward model / world model 判定，它是否对照人工标注或可执行真值校验过。
- **预算与失败处理**：基线是否同骨干规模、同步数/候选数/token 预算；失败或超时的任务怎么计。
- **最强的反驳**：一个最可能推翻主要结论的理由。

## 代码核查
读了哪些文件（固定 SHA）、确认了什么、没确认什么。没跑就写"未运行"。

## 相对已有工作的增量
和哪 1–3 篇最接近的工作比，真正新的部分是什么。

## 适合 / 不适合
谁今天能用它、接入代价是什么；什么场景不该用。

## 一个值得验证的问题
一个具体、可检验的后续研究问题。

## 来源
- 论文链接（含版本）
- 代码链接（含 SHA）
