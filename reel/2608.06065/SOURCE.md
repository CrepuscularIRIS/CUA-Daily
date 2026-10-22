# SOURCE · 2608.06065 Gated Hindsight Distillation (GHD)

- 论文：*The Next Screenshot Knows: Gated Hindsight Distillation for Mobile GUI Agents*，arXiv **2608.06065v1**（2026-08-06）
- 材料：`research/fulltext/2608.06065.txt`（sha256 前缀 4558fe1332e5faf9，贡献列表处有裁剪）；`/tmp/2608.06065.html`（arxiv.org/html/2608.06065v1，sha256 前缀 10df2a1a40d1f0ef，本地私有，不提交）
- 初筛记录：`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`（screen_score 96.25，claim_support=supported_in_material）
- 核对：`research/v3/runs/gui-v3-20261022-01/verify/2608.06065.md`（verify_ok）
- 原文无章节编号，以下按节名 / 公式号 / 表号定位。

## 数字与断言

| 画报内容 | 原文定位 | 类型 |
|---|---|---|
| 离线训练切成前缀-动作对、丢弃下一屏；Soft Wrap 例子 | Abstract；Method › Motivation | 作者表述 |
| 教师 = 同参数、停止梯度，输入 x̃_t=(x_t, o_{t+1})；不单独训练、不自回归生成 | Method › Privileged Hindsight Distillation，Eq.5 | 作者方法 |
| 教师不给示范动作 / 理由文本（"Ours" 仅下一屏） | Experiments › Privileged Information and Transfer Mechanism（表 4 相关段） | 作者方法 |
| 广义 JSD，α=0.5；学生 top-K=100 + 余量桶；覆盖推理与工具调用全部 token；梯度只经学生 | Eq.6–7 及其后文字 | 作者方法 |
| 门控 M(y)=[R(y)<τ_succ]·[match_δ(â_T, a*)]；教师逐位 top-1 拼出动作；同动作名，坐标 δ=20（1000×1000 网格），文本精确或编辑相似，解析失败拒 | Method › Gating，Eq.8–9；Reinforcement Learning（1000×1000 网格，Eq.3） | 作者方法 |
| τ_succ = 1.45；G=8；λ=0.1；K=100；δ=20；200 步 | Experiments › GHD Implementation Details；Eq.10 | 作者超参 |
| 动态采样最多 3 组、评估门控时不更新模型；全程平均 2.69 次 | Method › Dynamic sampling；Experiments › Efficiency and Sampling Overhead | 作者报告 |
| 动态采样规则两处不一："stop at the first attempt containing at least one accepted response" vs "retains the attempt containing the most useful gated supervision" | Method › Dynamic sampling；表 5 图注 | 原文呈现（核对确认歧义） |
| 部署移除教师、下一屏、门控，无额外推理模块；训练时间"未明显增加"但非受控对比 | Experiments › Efficiency and Sampling Overhead 末段 | 作者报告 |
| **表 2（7B, AndroidWorld Pass@1）：GRPO 47.13 → +Gate(无特权) 47.84 → +DS(无特权) 49.56 → GHD 52.73；+3.17 来自下一屏** | Ablation Studies，表 2 及其后段落（"further 3.17-point improvement"） | 作者报告；画报按核对口径以 49.56→52.73（同采样次数对照）表述 |
| 表 2 全部从同一 SFT-7B 起点；两个对照均不接触未来信息 | 表 2 图注 | 作者报告 |
| 表 3（7B）GHD 52.73±1.51（三次运行） | 表 3 | 作者报告 |
| 表 3（8B）：SFT 59.05/39.13；GRPO 61.35±1.08 / 37.43±0.42；GHD 66.47±0.68 / 54.11±1.11 | 表 3（AW / AL，三次运行均值±std） | 作者报告 |
| 表 5（8B）：GHD 无 DS 63.64±2.04 / 51.93±0.84，与 GRPO 同 rollout 预算 | 表 5 及图注 | 作者报告 |
| 训练集为 SFT 一次未解出的难子集：27,360 → 7B 6,968 / 8B 5,982；截图 420×896，SFT 起点低于官方 OpenMobile | Experiments › Models and Initialization；GHD Implementation Details | 作者报告 |
| Pass@1 为交互式模拟器成功率；训练为离线轨迹 + 步级 verifier | Benchmarks and Metrics；Method › Reinforcement Learning | 作者报告 / 核对结论 |

## 阅读判断（非作者主张，画报中以红色虚线 / "阅读判断"标出）

- 门控只检查动作一致，放行后蒸馏覆盖推理 token（Eq.7），因此动作一致不能证明教师理由真实（承 Sol caveat 与核对）。
- 表 2 未报标准差与运行次数；参照表 3 同配置 std 1.51，+3.17 约为两倍标准差，宜读作方向性证据。
- 8B 上 GRPO 在 AL 低于 SFT（37.43 vs 39.13），AL 大增益需结合这一弱基线理解（核对"阅读判断"节）。

## 自绘示意

- 手机屏（o_t / o_{t+1} Soft Wrap 菜单）、人物节点、管道、门控阀、剪刀、回路箭头均为自绘，非原论文图 1/2；未使用原文实验图。
- 未复现任何实验。
