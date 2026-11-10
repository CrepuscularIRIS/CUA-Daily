# Reel — gui-pc11-20261022-01(2026-10-22 · problem-core-v1.1)

本期 9 篇,全部经 Opus 5.5 完整原文核对后制作,版式骨架互不相同;每篇含 poster.png / poster.pdf / SOURCE.md(数字→原文定位)/ QA.md(核对结论+视觉检查)。可编辑源 poster.html 受旧 .gitignore 忽略仅存本地。画报核对共产生 5 条修订(l19–l23,run batches/),1 条降档(WebArena P3→P2 按编辑理由保留)。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2412.10840 | P3 | judgment / F1 | high_resolution_target_localisation | 注意力定位 vs 坐标生成:把"看不见"与"输出差"分开 | 双路径对照解剖 | ready |
| 2505.15810 | P3 | judgment / F2,F5 | rule_reward_single_step_rl | 框尺寸奖励被投机;推理越长定位越差(仅文字目标) | 奖励投机回路 | ready |
| 2307.13854 | P2* | judgment / F2,F3 | online_evaluation_methodology | 终态检查替代动作序列匹配(误判率未实测→P2,编辑保留) | 基准三层剖切 | ready |
| 2508.00935 | P3 | judgment / F2,F0 | verifiable_execution_reward | 聊天里拒绝 ≠ 电脑上不做:执行通道分开测量 | 双通道背离 | ready |
| 2404.06474 | P3 | capability / F2,F4 | learned_outcome_and_process_judges | 评估器与执行/人工双重校准并用于下游 | 信号校准链 | ready |
| 2409.07429 | P3 | capability / F3,F4 | experience_memory_retrieval | 只用已完成查询归纳工作流,信息边界防泄漏 | 归纳窗口时序 | ready |
| 2406.11896 | P3 | capability / F3 | trajectory_level_policy_training | 同骨干下在线 RL 逐级超过模仿(模拟器+实时网站) | 训练范式阶梯 | ready |
| 2407.01476 | P3 | capability / F0,F5 | simulated_lookahead_selection | 算力配平后搜索仍有效;前提环境可重置 | 搜索树+预算天平 | ready |
| 2503.19537 | P3 | capability / F2,F4 | agent_initiated_user_interaction | 负结果:12 种 prompting 配置问人 precision 仅 0.08–0.19 | 失误矩阵+低精确率散点 | ready |

*2307.13854 修订记录见 batches/l19-correction.jsonl;其余修订:l20(2404.06474 单位)、l21(2505.15810 边界)、l22(2409.07429 口径)、l23(2503.19537 范围)。选择过程与 43 篇排除理由见 research/scoring/runs/gui-pc11-20261022-01/selection.md;分数体系为问题档位(P0–P3),非审稿分。

---

# 第二期 — gui-pc11-20261022-01 全量(2026-10-22 · 8 篇)

基于全量 L2(1279/1331 篇过 L2)后的 584 篇候选池选题。本期补强 F0/F3/F4/F5,未入 F2(首期已覆盖 5 篇)。版式骨架与首期及互相均不相同。

| paper | 档位 | q3 / 族 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|
| 2606.12666 CAPED | P3 | capability / F4,F0 | 截图上传前遮蔽隐私内容,泄漏率降 3 倍效用不降 | 泄漏-效用对照柱 | ready |
| 2504.13936 ViMo | P3 | capability / F0,F2 | 生成的未来屏幕能实际用于选动作,在线 +7.76pp | 生成-选择闭环 | ready |
| 2602.12276 CATTS | P3 | judgment / F5,F2 | 统一加候选采样不保证更好(22.6%→15.1%) | 成本-收益反单调曲线 | ready |
| 2310.03720 SteP | P3 | judgment / F5,F0 | 同示例数下策略栈(33%)胜扁平 prompt(20-23%) | 栈式分层结构 | ready |
| 2601.22781 | P3 | judgment / F5 | 合成数据不是越难越好,α=0.5 最优(+4.3pp) | α 参数倒 U 曲线 | ready |
| 2311.18751 | P3 | judgment / F3 | 基本任务成功≠组合完成(54.8%→31%) | 组合断裂链 | ready |
| 2312.08914 CogAgent | P3 | judgment / F0,F1 | 同数据、计 FLOPs,架构净贡献约 4.5% | 双因子归因天平 | ready |
| 2609.02154 MFA | P3 | judgment / F0,F4 | MFA 完成不再能证明人在场(10/10) | 认证链攻破路径 | ready |

选择过程与 28 篇排除理由见 [selection2.md](../research/scoring/runs/gui-pc11-20261022-01/selection2.md)。两期合计 17 篇,版式 17 种互不相同。

---

# 第三期 — 重激活后选题(2026-10-22 · 2 篇)

基于重激活 L2(244 篇重核,5 篇新晋 P3)后的 591 篇候选池。只选了证据最硬的 2 篇,不凑数。

| paper | 档位 | q3 / 族 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|
| 2604.00073 | P3 | judgment / F1,F0 | 同骨干下 GUI 与终端接口成功率差 1 点,成本差 2-8 倍 | 接口成本-效果矩阵 | ready |
| 2604.04918 | P3 | judgment / F0,F2 | 138 次问题动作只拦住 29 次:有审批≠能拦住 | 人机审批漏斗 | ready |

选择过程见 [selection3.md](../research/scoring/runs/gui-pc11-20261022-01/selection3.md)。三期合计 19 篇,版式 19 种互不相同。

---

# 第四期 — gui-rolling-20261023-01 增量轮（2026-10-26 · 3 篇）

增量轮候选池 6 篇（全部 P3 confirmed）。Opus 5.5 读完三篇的完整原文与附录后制作；另 3 篇排除（同卡去重 1、编辑排除 1、证据形态 1），理由见 selection-004。本期无 correction 退回。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.30792 Trace2World | P3 | judgment / F2,F3 | calibrate_simulator_to_real（**新覆盖**） | 只把验收证据换成源轨迹回放，模拟收益留到真机 94.0% vs 54.7%（训练 app） | 双边界管线 + 哑铃图 + 保留率柱 | ready |
| 2610.31698 Malva | P3 | judgment / F1,F2 | structured_screen_observation（**新覆盖**）/ agent_loop_context_control | 工具层不核对就交状态：335 例失败、11 种模式、119 例错而不报 | 四相位环形缺陷地图 | ready |
| 2610.32536 IGG | P3 | judgment / F1 | high_resolution_target_localisation / online_evaluation_methodology | 替模型做掉显露动作，Qwen3-VL 30.8%→81.9%；只告诉动作类别仅 +3.1 | 阶段分解 + 逐级干预剥离 | ready |

选择过程见 [selection-004.md](../research/scoring/runs/gui-rolling-20261023-01/selection-004.md)。四期合计 22 篇，版式 22 种互不相同。

---

# 第五期 — gui-rolling-20261023-01 增量轮（2026-10-27 · 3 篇）

候选池 5 篇（全部 P3 confirmed）。Opus 5.5 读完 5 篇的完整原文与附录后选题：入选 3 篇；SkillShift-Bench（2610.33528）因 L2 判断超出证据写 correction 退回 Sol，本期暂停；Realtime-Bench（2610.22155）上期的单次运行顾虑未解除，再列备选。33907 与 33636 经同题判断不重复。理由见 selection-005。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.34384 AndroidFlux | P3 | judgment / F2,F5 | online_evaluation_methodology / learned_outcome_and_process_judges | 接手同一出错状态，代理排名重排（GUI-Owl-32B 53.75→26.25）；通用偏好 RM 在恢复对上 0.49–0.52 | 检查点时间轴 + 斜率重排 + 倒带/注入交叉线 + 哑铃 | ready |
| 2610.33636 Build or Adopt? | P3 | judgment / F1,F0 | agent_loop_context_control | 同工具同模型只换循环：逐步车机用例打平，开放任务上通用循环 +9~28 点，靠的是出错后补救；推理费 2.6–10.7× | 建筑剖面 + 三栏分户账 + 正确率–恢复散点 | ready |
| 2610.33907 OS-Wizard | P3 | capability / F0,F1 | exploration_driven_task_synthesis | 教程＋原生命令＋枢纽快照的采集器，同 10K 样本 36.5 vs 13.0/18.9，27B 5.9→64.1（消融混入应用构成） | 竖向采集树 + 同骨干阶梯 + 混杂标注消融 | ready |

选择过程见 [selection-005.md](../research/scoring/runs/gui-rolling-20261023-01/selection-005.md)。五期合计 25 篇，版式 25 种互不相同。

---

# 第六期 — gui-rolling-20261023-01 增量轮（2026-10-28 · 3 篇）

候选池 7 篇（全部 P3 confirmed）。Opus 5.5 读完 7 篇的完整原文与附录后选题：入选 3 篇；TAM（2610.37482）因 L2 的能力判断超出同协议证据写 correction 退回 Sol，本期暂停；Realtime-Bench（2610.22155）原文证据三期未变，不转正并移出滚动备选；36471 与 36877 编辑排除。35237/37482、36831/36471 经同题判断不重复；34735 与首期 2503.19537 同卡不同题。理由见 selection-006。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.36831 Right Click, Wrong Box | P3 | judgment / F2 | online_evaluation_methodology | 按点击结果执行判卷：被框规则拒掉的点击 17.6–38.1% 达成目标；ScreenSpot-v2 校正 0.2–1.8 点，与同尺寸模型差距同量级 | 像素结果地图 + 救回条 + 误差预算标尺 | ready |
| 2610.35237 Chart the Invisible | P3 | capability / F0 | structured_screen_observation | 目标在视口外时代理去点可见错目标（失败的 83.73%）；标出可滑动区域后 18 个滑动任务 64.8→82.7%，每题多 33–71 秒 | 手机视口剖面 + V/H/G 点阵 + 收益/耗时对账 | ready |
| 2610.34735 iPrefBench | P3 | judgment / F4,F2 | agent_initiated_user_interaction | 动作完成 91.6 而整题成功 47.7%；只能问的信息最多问到 44.2%，多问换来 precision 下降 | 来源分拣图 + 四刻度梯 + P–R 迁移箭头 + 2×2 失败象限 | ready |

选择过程见 [selection-006.md](../research/scoring/runs/gui-rolling-20261023-01/selection-006.md)。六期合计 28 篇，版式 28 种互不相同。

---

# 第七期 — gui-rolling-20261023-01 增量轮（2026-10-31 · 3 篇）

候选池 9 篇（全部 P3 confirmed）。Opus 5.5 读完 9 篇的完整原文与附录后选题：入选 3 篇；DynaRev（2610.40133）的全部结果指标来自未经校验、且同为被测代理的 DeepSeek 评审，写 correction 退回 Sol，本期暂停；WaitLens（2610.32482）与 39282 同题去重；VeriCUA、InterA11y、WebAnything、EnvOS 编辑排除（证据形态或偏离核心）。理由见 selection-007。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.39282 Stale Screenshots | P3 | judgment / F1,F3 | agent_loop_context_control | 点击过期主要来自页面加载而非规划耗时：31 个公开页面上已加载 0.4%、刚打开第一秒 17%；8/10 代理的等待规则超过 1%；“在哪”用像素检查、“发生了什么”用小模型 | 对数时间轴 + 等待条形梯 + 误报×召回平面 + 回本公式 | ready |
| 2610.39234 AgentHeal | P3 | capability / F3,F2 | online_evaluation_methodology / agent_loop_context_control | 主资源被持续阻断时找合法替代、声明版本、找不到就停：13 个模型 89.4→43.7%，激进型用冒牌页交差、谨慎型不会找；真实回放中越权更多 | 三份反事实环境 + 能力/可靠性散点 + 家族斜率 + 四道判定流程 | ready |
| 2605.29532 GUITestScape | P3 | judgment / F2,F1 | online_evaluation_methodology / learned_outcome_and_process_judges | 探索性 GUI 测试拆成 Reach/Trigger/Detect：编码代理 93.7→51.4%，GUI 专用代理 Detect 4.2%；评审器先经双标校验（Detect 97.1/94.0） | 缺陷分类树 + 评审校验条 + 三步阶梯 + 系统×故障热力图 | ready |

选择过程见 [selection-007.md](../research/scoring/runs/gui-rolling-20261023-01/selection-007.md)。七期合计 31 篇，版式 31 种互不相同。三份 poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第八期 — gui-rolling-20261023-01 增量轮（2026-11-03 · 1 篇）

候选池 3 篇（全部 P3 confirmed）。Opus 5.5 读完 3 篇的完整原文与附录后选题：入选 1 篇；跨接口授权协议（2610.41397）没有在任何实际 CUA 栈中测出问题、实验均为私有参考实现的自洽检查，SafeWebWorld（2610.40798）的决策金标单人审核、证据度量是词元重合、主实验未隔离预测接口，两篇各写 correction 退回 Sol，本期暂停。理由见 selection-008。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.41272 REEF / ANGLER | P3 | judgment / F2,F4 | environmental_injection_attacks | 攻击以“网站状态终止时仍被改”计分；同任务、每站 100 次 rollout 下自适应攻击把 8 骨干平均 ASR 15.24→20.36%（GPT-4o 占增益约四成）；弹窗被点 52.4% 而做成 17.1%；前沿骨干不点网页诱饵却仍被追加指令攻破 | 六步攻击闭环 + 增益贡献瀑布 + 72 格差值点阵 + CTA→ASR 漏斗 + 重复运行噪声条 | ready |

选择过程见 [selection-008.md](../research/scoring/runs/gui-rolling-20261023-01/selection-008.md)。八期合计 32 篇，版式 32 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第九期 — gui-rolling-20261023-01 增量轮（2026-11-04 · 2 篇）

候选池 21 篇（全部 P3 confirmed：上期之后巡检进池的 2610.41181、Awesome-CUA 回填 17 篇、inc-l2-17 新增 3 篇）。Opus 5.5 按问题族分组去重，读了 6 篇的完整原文与附录，其余 15 篇按 L2 与裁剪 core 编辑排除（未声称读过全文）。入选 2 篇；JHiMA-WebRL（2611.05263）的核心比较差距 1.7–3.8 点、无方差与多种子，主表 37.2 vs 24.0 大部分来自 SFT 数据差异，写 correction 退回 Sol，本期暂停；DIBench、Coati 列为下期备选；ScienceCUA 与 04073 同题去重。理由见 selection-009。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2611.04073 Tutorials vs world model | P3 | judgment / F1,F2 | simulated_lookahead_selection / learned_outcome_and_process_judges | 同一 policy–judge–grounder 只换判官看到的未来：无教程时真实截图前瞻 43.8→48.0，给了教程 51.7→51.6（OSWorld 360 题，Qwen3-VL-32B）；收益大头是教程，瓶颈是判官读不懂“做完没有” | 因子开关机制图 + 有/无教程分带点图 + 三组收益阶梯 + 三分支案例 + 双栏失败类型 | ready |
| 2611.04879 ScamWorld | P3 | capability / F4,F2 | environmental_injection_attacks / online_evaluation_methodology | 按用户请求在重建诈骗站上办事：6 骨干受骗 11%–35%（日志判定），合法站完成 94%–100%；受骗里 45% 事先点名了风险，付款 28% vs 凭据类 2%；单独问时认出 88%–100% | 四段结账路径 + 停法分布条 + 知道/做到点图 + 钱/秘密对比 + 收据式样例 + 干预表 | ready |

选择过程见 [selection-009.md](../research/scoring/runs/gui-rolling-20261023-01/selection-009.md)。九期合计 34 篇，版式 34 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第十期 — gui-rolling-20261023-01 增量轮（2026-11-05 · 2 篇）

候选池 4 篇（全部 P3 confirmed：selection-009 的三篇备选 + 18:17 巡检班新进池的 2611.04393），Opus 5.5 全部按 v1 补读全文与附录。入选 2 篇；DIBench（2610.06898）与 04393 同题（页面内容操纵候选选择），且最强探针本身是命令式注入、防御比较非配对，同题去重；Coati（2611.02644）的 VerifyLoop 消融仍是单次对三次均值，维持编辑排除。无 correction。理由见 selection-010。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2611.04393 Voluntary Servitude | P3 | judgment / F4,F2 | environmental_injection_attacks / injection_defense_isolation | 一条不含命令的“出过安全事故”假评论，4 个模型上选中攻击者 60.4%（指令注入 66.0%），注入检测器放行 100% / 78%；同槽位的道德失当指控只有 8.2%；“安全指控须有独立佐证”一条提示使 68.4→3.6%（非自适应）；4 个 AI 浏览器各 20 次迁移检查 | 深色页眉 + 警示斜纹 + 评论页示意 + 检测器关卡条 + 同槽位对照柱 + 排除占比条阵 + 浏览器小条 + 检索把关表 + 消融数字条 + 水平哑铃防御 | ready |
| 2610.31274 PointerBench | P3 | capability / F0 | high_resolution_target_localisation / online_evaluation_methodology | 同模型同判分下目标越细越点不中：Fable 5 单词 90.2 → 字符 70.4 → 插入点 64.7 → 区域 56.0，顶尖专用模型字符 11–19、插入点 23–34；Gemini 3.7 Flash 输出 0–1000 坐标，换算后 3.1→78.1（合成截图、单步静态） | 刻度尺页眉 + 三联目标示意 + 粒度阶梯折线 + 插入位置热力表 + 坐标换算哑铃 + 大数字格 + 全榜竖线带 | ready |

选择过程见 [selection-010.md](../research/scoring/runs/gui-rolling-20261023-01/selection-010.md)。十期合计 36 篇，版式 36 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第十一期 — gui-rolling-20261023-01 增量轮（2026-11-06 · 2 篇）

候选池 48 篇（Awesome-CUA 回填第二波 46 篇 + 近期查新 2 篇，2018–2026 年；P3 47 / P2 1）。Opus 5.5 按“主卡 × 问题”分组去重，短名单 12 篇（另补看 1 篇替补）逐篇从 arxiv.org/html 补读，两篇入选者读完全文与附录，其余按 L2 与裁剪 core 编辑处理（未声称读过全文）。入选 2 篇；2604.25235 的 CUA 相关内容只有 VQA 式判分基准中的 Mind2Web 子集，L2 的“CUA 评价组件”范围判断超出原文，写 correction C-011-1 退回 Sol；Teach it to stop、QWeb、SkillLens 等因证据形态或偏离核心编辑排除。理由见 selection-011。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2507.11662 SGV | P3 | judgment / F2,F5 | learned_outcome_and_process_judges | MLLM 轨迹验证器“太爱点头”：14 个模型失败轨迹判对率 34–78%，加思考、投票、细则都压不住；先不看轨迹写出“该怎么做”再判，Gemini 2.5 Flash 55→76；放进回路 VWA 45.0→54.0（常规验证器 46.1，token 2.2× vs 1.5×） | 深色竖栏 + 两泳道调用对比 + 14 行哑铃 + 加算力条形 + 下游柱与介入结果条 + 验证器×代理矩阵 | ready |
| 2505.10978 GiGPO | P3 | capability / F2,F1 | trajectory_level_policy_training | 同一批 rollout 里“回到同一页”就是现成对照组：不加价值网络、不加采样的逐步信用；WebShop 同超参 3 seeds，7B 66.1→75.2、1.5B 56.8→67.4，每轮多约 0.5 秒（HTML 文本观测模拟站） | 线路图机制（锚点站 + 回环箭头）+ 条件标签行 + 误差线分组柱 / 消融表 / ω 折线 + 计时与组大小条 | ready |

选择过程见 [selection-011.md](../research/scoring/runs/gui-rolling-20261023-01/selection-011.md)。十一期合计 38 篇，版式 38 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第十二期 — gui-rolling-20261023-01 增量轮（2026-11-07 · 2 篇）

候选池 13 篇（Awesome-CUA 回填第三波 8 篇 + 近期候选 5 篇）。近期 5 篇无新记录：2611.04393 已在第十期入选，DIBench、Coati、ViBench 2.0、BiGrounder 维持前期处理。回填 8 篇中 Opus 5.5 补读 5 篇原文（两篇入选者读完全文与附录），入选 2 篇；Automotive-ENV（成功率分母口径不清、安全验证器匹配推理文本）、Remote Labor Index（CUA vs CLI 只有约 2 vs 4 个项目、scaffold 不配平）、Game-TARS（无同数据接口对照、未见游戏为暂停时钟）编辑排除，lmgame-Bench / Orak / BrowseComp 依 L2 判为偏离核心。无 correction。理由见 selection-012。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2601.13142 TVWorld | P3 | capability / F3,F0 | planner_grounder_interface | 电视遥控只能移动焦点：点击式 GUI 模型在 5 张留出 Google TV 图、500 题上 1.6–15.4%；同骨干 Qwen3-VL-8B 经三类轨迹 SFT + 图命中时间奖励 RL 从 20.0 到 68.3（3 次 65.6–71.4），静态截图图回放、非真机 | 电视边框页眉 + 遥控器图 + 两屏交互对照 + 图上三类轨迹 + 分段奖励表 + 分组条形 + 两阶段表 + 变体对运行跨度点图 | ready |
| 2609.35143 Timeline-Bench | P3 | judgment / F2,F0 | online_evaluation_methodology / learned_outcome_and_process_judges | 剪辑成片“测试全过仍输”：771 个未解决运行中 562 个只差按人校准的质量门；质量门代理级 ρ=0.93、单片 κ=0.15；同一 GPT-6 Astra 改用屏幕 + 键鼠在 Resolve 里剪，解决 2/56 vs 代码 12/56（OS、工具、听觉通道同时不同） | 时间线装饰条 + 四道门漏斗 + 层级一致性条 + 16 代理散点 + 配对森林图 + 计算机使用对比表 + 行为数字卡 + 能力读数格 | ready |

选择过程见 [selection-012.md](../research/scoring/runs/gui-rolling-20261023-01/selection-012.md)。十二期合计 40 篇，版式 40 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第十三期 — gui-rolling-20261023-01 增量轮（2026-11-09 · 2 篇）

候选池 14 篇（Awesome-CUA 回填第四波 `inc-l2-34..37` 的全部 P3 confirmed）。Opus 5.5 按问题族分组、与前十二期同题去重，补读 7 篇原文（两篇入选者读完全文与可得附录），入选 2 篇；FullStack-Agent（2602.03798）的升档依据其实来自 API 判官列，GUI 判官加数据库日志要求后只降 0.9–5.4 点，且“日志有效”由同一判官 LLM 判定，写 correction C-013-1 退回 Sol；SWEeper-Bench、PPTArena、AndroidGen 与已入选论文同题去重；IChart2Code、VISTA、CUA-as-embodied 等因偏离核心或证据形态编辑排除。理由见 selection-013。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2610.37567 Gym-Anything-RT | P3 | judgment / F1,F2 | online_evaluation_methodology | 暂停式评测替模型等待：100 个截图 + 键鼠的网页小游戏，同游戏同种子只改时钟，GPT-6 Astra xHigh 暂停 75%、放慢 64× 57%、实时 9%（非实时对照 66%）；写脚本 9→31；每配置一次，暂停另给 3–6 帧 | 时钟表盘页眉 + 双时间线示意 + 一程序四时钟分叉 + 放慢倍数折线 + 六模型哑铃 + 写代码对照表 + 暂停分组条与难度表 | ready |
| 2611.08496 MobiInfer | P3 | capability / F0 | agent_loop_context_control | 手机端 GUI 代理每步重算同一段提示：按寿命复用前缀 KV、按输出阶段裁词表、只对格式与推理投机，同模型同手机推理时间快 2.11–2.78×，四设置成功 58.1→57.7%；“端到端”为推理时间合计，约 1.9% 输出与原模型不同 | 竖长手机机制图 + 步数倍数折线 + 12 组叠加条形 + 消融阶梯 + 投机方法表 + 同截图比对表与数字卡 + 难度 / 类别摘录 | ready |

选择过程见 [selection-013.md](../research/scoring/runs/gui-rolling-20261023-01/selection-013.md)。十三期合计 42 篇，版式 42 种互不相同。poster.html 受 `.gitignore` 忽略，仅存本地。

---

# 第十四期 — gui-rolling-20261023-01 增量轮（2026-11-10 · 3 篇）

候选池 12 篇（Awesome-CUA 回填第五波 11 篇 + 2601.15808，全部 P3 confirmed）。Opus 5.5 按问题族分组、与前十三期同题去重，补读 5 篇原文（三篇入选者读完全文与附录），入选 3 篇；2611.11971 的发布时间经 export.arxiv.org 核对为真实 v1（2026-11-09）。ChatShop（2404.09911）的 WebShop 捷径审计只有一个检索覆盖率和一个不含选项选择的排序器，编辑排除；DeepVerifier 与第十一期 SGV 近同题；其余 7 篇因证据形态或偏离核心编辑排除。无 correction。理由见 selection-014。

| paper | 档位 | q3 / 族 | 主卡 | 问题一句话 | 版式骨架 | QA |
|---|---|---|---|---|---|---|
| 2611.11971 Harness Matters | P3 | judgment / F1,F2 | environmental_injection_attacks / injection_defense_isolation | 配对可用性任务剔除“做不到”后，同一 GPT-4o 装进 Agent-E 防住 83.8%、装进 Skyvern 2.0 只防住 42.9%；外壳、模型、交互都显著（模型 χ² 更大）；完成率最高的外壳防御率倒数第二；受控页、单次运行，DSR = 1 − ASR | 判卷决策条 + 外壳 × 模型热力表 + χ² 条 + TCR–DSR 散点 + 朴素攻击哑铃 + 阶段格 + 消融前后点 | ready |
| 2206.11795 VPT | P3 | capability / F0,F4 | mine_human_screen_videos（**新覆盖**） | 1,962 h 带键鼠录像训练看前后帧的 IDM，给约 7 万小时网络视频补标签，训练 20 Hz 原生键鼠策略（含合成界面拖放）；IDM 约 100 h 即平台；RL 后钻石镐 2.5%；Minecraft、各训练一次 | 通高科技树阶梯 + 四段流程 + IDM 刻度尺 + 界面示意 + 倍数对数条 + 成本账 | ready |
| 2403.08140 BAGEL | P3 | capability / F3,F2 | exploration_driven_task_synthesis | 无示范、无考题：先乱点再让模型给轨迹起名、照名重做，自举示范供检索；MiniWoB++ 最难 10 任务 46.8→61.0（图 3 为 60.5）；人工按执行结果剔错还能再涨 7 点，自打分漏放错误示范 | 循环改写图 + 例子动作胶囊 + 一次 / 多轮配对条 + 逐任务棒棒糖 + 报错配对条 + 参照表 | ready |

选择过程见 [selection-014.md](../research/scoring/runs/gui-rolling-20261023-01/selection-014.md)。十四期合计 45 篇，版式 45 种互不相同；18 张主卡至此均有 Reel。poster.html 受 `.gitignore` 忽略，仅存本地。
