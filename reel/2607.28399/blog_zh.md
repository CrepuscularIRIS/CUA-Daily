# 对而迟到：把解码挪出决策时刻的关键路径——预编译策略树

*CUA Radar 对 arXiv 2607.28399v1（Zihan Dong、Rui Qian、Qishi Zhan、Dongshen Peng、Kaixin Li、Yu Li）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2607.28399v1 · 板上未列代码仓库。*

## 问题：正确的动作在窗口关闭之后才到

多数 computer-use agent 都在循环：截图、调用多模态模型、执行一个动作、再观察。而 BIOS 启动提示、自动消失的对话框、瞬态 toast、反应类游戏，这些窗口的开合比一轮循环更快。论文的原话是：“the typical failure is not wrong understanding but late understanding”——agent 在窗口已经关闭之后才算出正确动作。可能有两种解释：要么 agent 没能预判事件，要么预判对了、却败在计算发生的位置。论文把模型、任务、信息全部固定，只操纵一件事：生成是否发生在决策时刻的关键路径（decision-time critical path）上。

## AAPT 是什么

方法是 Adaptive Anticipatory Policy Trees（AAPT）。感知端：30 FPS 截图经像素差 change gate（至少 0.5% 像素相差 20 个灰度级才算”变化帧”，每 500 ms 强制送入一帧探测帧，静止画面不会让 observer 失明）。动作端：allowlist 内的按键原语，树外动作一律不执行。平台是作者自建的桌面计时基准 key_prompt，外加 39 个外部 DynaCU-Bench 网页任务。在 CUA Radar 板上它属于 C17 模式：manager 规划、worker 执行——这里是从同一个冻结 checkpoint 里分出的慢 planner 和快 observer。

机制是调度而非学习。屏幕安静时，冻结模型编译一棵扁平的条件策略树：可观察 guard、预授权动作、每分支 deadline、校准 confidence、risk 级别，树的大小按规划器自身的解码延迟定：T_cover ≥ L_p95 + M（安全裕量 M = 500 ms）。事件到来时，低 token observer（输出上限 64 token，由 sweep 选出）只返回一个 JSON 对象 {branch_id, confidence, reason}；运行时检查资格、planner 置信下限、决策年龄是否超过分支 deadline，然后触发预授权动作。无匹配、歧义或过期一律回退 replanning。全程没有任何训练信号：no fine-tuning，只有 guided JSON 解码（vLLM 的 guided_json，xgrammar 后端，planner temperature 0.2），验证失败允许一次有界重采样。

## 论文报告的结果

以下全部是在线结果，服务端确定性判分：只有请求的按键在 deadline 之前到达服务器才算成功。所有对比都是 per-seed 配对——每 block 42 对，每对内隐藏调度字节级一致，条件顺序交替——用 exact two-sided McNemar 检验，模型冻结，窗口、种子、终点全部预注册。主模型是 Holo-3.1-35B-A3B；每 trial 只有一个决策，不存在步数预算，种子区间预注册且不复用。

| 对比（条件、窗口） | Reactive R0 | AAPT T2 | exact McNemar p |
|----|----|----|----|
| 争用区扫描，600 ms | 4/42 (0.095) | 29/42 (0.690) | 6.0×10⁻⁸ |
| 争用区扫描，650 ms | 12/42 (0.286) | 30/42 (0.714) | 4.0×10⁻⁵ |
| 声明主实验，650 ms | 21/42 (0.50) | 33/42 (0.79) | 1.8×10⁻³ |
| 新种子，550 ms，合并 84 对 | 0.143 | 0.619 | 1.8×10⁻¹² |
| Qwen3.6-35B-A3B，600 ms，合并 126 对 | 0.341 | 0.778 | 4.9×10⁻¹³ |
| DynaCU-Bench 迁移，39 任务 | 7/39 (0.18) | 6/39 (0.15) | 1.0（平局） |

在 500 ms（低于 reactive 地板）处，T2 28/42 对 R0 的 0/42。T2 在所有窗口的错误动作为 0；Qwen3.6 主 block 上 reactive 一侧的错误动作率为 0.57。数字背后的延迟账：reactive 往返 567 ms p50，AAPT 的路由调用约 325 ms p50，而 planner 1.81 s p50 的编译发生在事件之前。代价是真实的——T2 每 trial 生成 3.2× 于 R0 的 completion token（342.8 对 105.8；单次调用反而更便宜，59.3 对 105.8），wall time 从 1.65 s 升到 3.32 s，每次成功触发平均编译 1.27 棵树。论文没有任何离线指标，上面全部是在线数字。

## 论文自带的对照实验

- **提前动手并不够。** 开环基线 R1 和 predict-and-replan 基线 P1（TraceR1 式的 receding-horizon 控制）都在完整往返之前就开始行动，但在争用窗口双双得 0 分，因为执行期间仍在解码。
- **Oracle 路由框住 observer。** O1 用真值零延迟路由，高于 T2，但差距过不了 Holm–Bonferroni；论文把它读作 headroom——瓶颈在 observer 而非 planner。
- **尺寸规则预测了增益出现的位置。** 准备时间 sweep 中，prep 0.5–1 s 时 T2 为 0/42（事件在编译中到来），2 s 时与 R0 打平（36/42 对 37/42），4 s 时 42/42：交叉点正好落在 L_p95 + M ≈ 2.4 s。所有”饿死”失败的形态都是 miss，从不是错误动作。
- **分支预算有膝关节。** 600 ms 的 k × n sweep 里，(k=3, n=1)——每个 outcome 一条分支——42/42 全对（19/0 discordants，p = 3.8×10⁻⁶），对照共享 reactive 臂 0.548；低于 outcome 集大小的预算主要败在 planner 树有效性。observer token 上限 sweep 选出 64（合并 0.833），好于 32（0.571，截断）和 128（0.690，分支准确率低于门槛）。
- **三道能力闸门、六个模型。** 只有 observer 解码低于 1 秒、flat-tree 有效、分支准确率达到 0.85 三条全过才有增益。UI-Venus-1.5-30B-A3B 快且 schema 合法，但路由准确率 0.39，与 R0 打平（11/42 对 13/42，p = 0.625）；把它的 observer 换成真值路由，平局翻成胜利（22/42 对 12/42，p = 0.021）——这正是论文预注册了相反预测并如实报告失败的那个探针。EvoCUA-32B 的 observer 约 2.5 s，直接落败（T2 0/43 对 R0 22/43）；UI-TARS-1.5-7B 过不了有效性闸门，按协议终止。
- **是边界，不是全面胜利。** DynaCU-Bench 总体平局，但分歧胜负按任务结构干净劈开：4 个 AAPT 独有胜利全部是响应可预先枚举的 dashboard deadline（在 gated frame 之后 140–215 ms 发出）；5 个 reactive 独有胜利都需要多步序列或延迟揭示的值。把事件延迟随机化到 \[500, 1000\] ms，优势不变（15/0 discordants，p = 6.1×10⁻⁵）。

## 论文自己承认的薄弱处

正结果”is confined to two Qwen3.5-MoE checkpoints on one controlled scenario family”；三键 key_prompt 场景”was designed to isolate the mechanism, not to represent computer use broadly”。DynaCU 的解离”rests on 4 versus 5 discordant tasks”。争用窗口的成功率对种子和延迟敏感——“only paired per-seed comparisons carry evidential weight”——绝对速率不应跨种子组引用；约 100 ms 的 serving 漂移把五键 900 ms block 从争用推到天花板，得到一个 null（R0 42/42，T2 38/42，p = 0.125），论文原样报告。UI-Venus 的树覆盖在会话间漂移（outcome recall 0.22 对 0.59，配置与 compile key 相同），一次编译内核变化曾把树有效性从 88.1% 拉到 18.3%，权重不变。click_target 场景被放弃，因为两侧各自失败（reactive 一侧中位偏差 229 px 打不中 90 px 目标；树无法绑定触发时才揭示的坐标）。异步树刷新、可复用策略记忆、任何 fine-tuning 均未测试。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **online**。判定记录肯定了确定性的在线判分（“a trial succeeds only if the requested keypress reaches the server before the deadline”）、39 个确定性任务的 DynaCU-Bench 外部配对、新种子复现、完整成本账本和组件消融。它标出 AP15——把 scaffold 增益默认迁移到其他 backbone——论文用六模型闸门矩阵自己刻画了这条边界；同时记录 code 不明、基线仅部分预算对齐（T2 花 3.2× 的 completion token）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
