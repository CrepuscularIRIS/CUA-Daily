# SOURCE · 2605.07630

- 论文：Safe, or Simply Incapable? Rethinking Safety Evaluation for Phone-Use Agents（PhoneSafety；Tang, Zhang 等，Tencent Hunyuan / CUHK-SZ / 清华）
- 版本：2605.07630v2（2026-10-19），https://arxiv.org/abs/2605.07630v2
- 原文材料：`/tmp/2605.07630.html`（arxiv.org/html/2605.07630v2，正文与附录 A–M，sha256 前缀 e7d63558af96e642，未提交）；`research/fulltext/2605.07630.txt`（core 裁剪，sha256 前缀 368fe6f03c56d875）。数字以 HTML 为准。
- 初筛记录：`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`（G4/M4/X3/E4，screen 95，offline）
- 核对记录：`research/v3/runs/gui-v3-20261022-01/verify/2605.07630.md`（verify_ok）
- 仅阅读原文，未运行代码，不构成复现。

## 数字与断言映射

| 画报位置 | 内容 | 原文出处 |
|---|---|---|
| 问题框 / 根节点 | harmless 混淆"选择安全"与"做不到"；下载歌曲遇订阅付费页场景 | Abstract；§1；图 1（本页重绘） |
| 根节点输入 | 用户指令、近期历史、当前截图、授权协议 | §3.1；§3.6 |
| 关键动作框 | 700 个安全关键时刻，130+ 款中文 Android app；两侧参考动作；两侧都不匹配 → CFR | §3.4–3.5；附录 A；附录 D |
| 三分支定义与例 | Safe / Unsafe / 无有效动作的定义与示例动作 | §3.2；附录 A.1 |
| 终端"真安全/不安全/表面安全" | CFR 是可观察行为层面的操作类别，作者称其为能力导向信号 | §3.2–3.3；§4.4 |
| 色带 | Cond-Safe = Safe/(Safe+Unsafe)，分母为 0 时未定义；1−CFR 衡量能否做出相关动作 | §3.3 |
| 旧二分类括号 | harmless = 1 − Unsafe = Safe + CFR，比 Safe 恰多 CFR | §3.3 |
| 条形图 | 8 个模型通用 SR、Unsafe、Safe、CFR、Cond-Safe（Clean-684） | 表 1；表 10 |
| 二分类 harmless 列 | 本页按 100 − Unsafe 换算（定义见 §3.3）；AutoGLM 90.5% 为原文数字 | 表 1；§4.1 |
| Claude/MobileAgent 注 | Claude 通用第 3（53.0）Cond-Safe 第 1（88.0）；MobileAgent 3.5 通用第 4（52.8）Cond-Safe 31.4 | §4.2 |
| 脚注 | Claude 通用 SR 用 0.25 阈值；表 1 不应读成排行榜 | 表 1 注；§4.1；附录 A.2 |
| 去截图卡 | 200 例 API 子集，5 模型（含 GPT-5.5）均值：CFR 35.3→77.0%，Unsafe 13.0→4.1%，去历史 CFR 40.6% | §4.4；附录 K 表 12 |
| 相关卡 | Pearson r=0.906（通用 SR vs 1−CFR），r=0.239（vs Cond-Safe），8 个模型，描述性报告 | §4.2；§4.4；附录 G |
| 审计卡 | 2,390 条 CFR 输出中 98 条 call_user（安全参考为 grounded 动作）记为 Safe：排名不变，最大 +4.8 pp，r → 0.873 / 0.192；不界定全部参考不完整性 | §4.4；附录 B 表 3 |
| 协议卡 | 固定输出重标 CFR 不变；minimal 提示重跑 Gemini 30.0→46.5、Seed 29.5→34.5、Claude 38.0→51.5、Kimi 41.5→56.0、GPT-5.5 37.7→34.5 | §4.5；附录 F 表 8 |
| 限制栏 | 离线单步；中文 Android 生态、授权敏感动作；英文指令实验截图仍为中文（CFR −0.7~+9.5 pp，未上图）；CFR 混合多种原因 | §5；§4.4；附录 K |
| 限制栏·参考标签 | 历史核验为初始标签可见的顺序 QC，非独立事后核验；双专家 86.1%（κ=.781，158 条）针对 agent 输出 | §3.4；§3.6；附录 M |
| 阅读判断框 | AutoGLM Cond-Safe 66.7% 基于 130+65=195 个相关动作（684 例）；按 harmless 排第 2（Claude 92.1 > AutoGLM 90.5 > Gemini 89.6） | 表 10 计数；本页按表 1 换算，为本项目阅读判断 |

## 图

- 决策分解树、手机界面、色带、条形图均为自绘示意，按上表数字排布；未复制原文图 1/2/3。
