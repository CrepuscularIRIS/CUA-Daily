# SOURCE · 2609.02154

- 论文：*WiP: Characterizing and Defending Against Mobile-Agent-Driven MFA Automation*。
- 版本：arXiv 2609.02154**v1**（2026-09-02，WiP 短文，正文 §1–§4，图 1–4）。
- 阅读材料：`research/fulltext/2609.02154.txt`（v1 HTML 提取，正文完整，缺图内数值）；图 1–3 和 §2.1 威胁模型原句由 https://arxiv.org/html/2609.02154 补看，只存 /tmp，不提交。
- 初筛记录：run `gui-pc11-20261022-01`；L1 `batches/p058.jsonl`，L2 `batches/l48.jsonl`（P3 / judgment / F0,F4 / 无主卡）；入选见 `selection2.md` 表第 8 行。

## 数字与断言 → 原文位置

| 画报内容 | 原文 |
|---|---|
| 口令式 MFA 默认由人搬运验证码；factor collapse 定义；「不是绕过，而是合法取得并提交每个因素」 | §1 第 1 段 |
| 只研究邮件 OTP 与认证器动态码 | §1「we study passcode-based MFA, including both email-delivered OTPs and authenticator-generated dynamic codes」 |
| 威胁模型：已解锁、GUI 控制权限、主凭证、邮箱/认证器已配置；不假设 OS 攻破、认证器密钥、锁屏绕过；被攻陷/误导/越权 | §2.1 Threat Model（原句「The email or is already configured」有缺词，按上下文读为邮箱或认证器） |
| Worker A（Login OTP Retriever）/ Worker B（Completion Worker）分工；只交接服务、账号、流程状态、验证码；分阶段重试 | §2.1 Modular Factor-Collapse Pipeline；图 1 |
| GPT-5 mini、MobileRun | §3.1 |
| 10 个商业网站/App，多个服务类别；每账号邮件 OTP 或认证器码 | §3.2 首段 |
| 成功 = 15 个动作内到达登录后状态；超预算或提前终止为失败；三种配置同一预算；人工核查并记录耗时 | §3.2 首段 |
| 3/10、6/10、10/10 | §3.2；摘要；§4；图 2 |
| 基础单 agent 平均 >200 s；详细指令「substantially reduces」耗时；双 worker 比详细指令「modestly increases」 | §3.2；图 3（画报未读图取数） |
| 单 agent 失败：过期码、没刷新收件箱、提前结束、谎称完成、重复操作；元素不显眼、杂乱收件箱；耗光步数 | §2.1 Single-Agent Baselines；§3.2 第 2 段 |
| 双 worker 减少上下文切换、隔离收件箱无关内容 | §3.2 第 3 段 |
| 防御 pilot：50 Hz 加速度计+陀螺仪；4 人 116 会话；五折；桌面 98.4%、手持 92.6% | §2.2；§3.3 |
| 「需要人在场的补充证据」 | 摘要末句；§4 末段 |

## 阅读判断（非作者结果）

- 结论带「MFA ≠ 人在场」与「只说明能操作这部手机的某个执行者拿齐了因素」是我们的概括，依据为 10/10 结果加威胁模型；作者原话是 factor collapse 与「physical-interaction sensing as complementary evidence of user presence」。
- 「服务端只看到验证码正确」是对口令式 MFA 机制的说明，论文未做服务端侧实验。
- 「没写每个服务跑几次、成功率无方差」「服务名单未公开」是我们对原文的缺项记录。

## 示意部分

- 认证链五层（L0–L4 + 终点）、绿色穿层路径、锁/邮件/时钟图标、读数板的 10 格均为自绘示意；层次按 §2.1 与图 1 的流程整理，不是论文原图。L0（设备锁/生物识别）画成未被攻破的前提层，对应威胁模型「unlocked device」「no lock bypass」。
- 10 格中哪几格亮只表示数量，不对应具体服务。
