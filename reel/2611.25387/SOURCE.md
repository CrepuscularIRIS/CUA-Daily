# 2611.25387 TuringSpace — 画报逐项来源映射

论文：TuringSpace: Grounding Spatial Intelligence in Action with Interactive CAPTCHAs（arXiv 2611.25387v1，2026-11-19）
缓存：research/fulltext/2611.25387.txt（25,397 字节，FULLTEXT: html）。核对日期 2026-11-21，执行模型 glm-5.3。

## 画报元素 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 五类空间能力卡 | 空间关系/心理变换/闭环操作/多步规划模拟/时空推理；时空最难 Astra 52.0、人类 97.3、心理变换 Astra 85.3、闭环 Astra 85.3、多步 76.0 | §3.1、Table 1 分类别 pass@1 |
| 榜单九行 | 人类 94.1±2.6（pass³ 84.8，33.1 s/题）、GPT-6 Astra 74.1/58.4、Claude Opus 5.5 65.3、Gemini 4 Argon 57.9、Kimi K3 32.0±1.4、Qwen3.8-Max 30.7、TuringSpace-9B 33.1±6.1（1.6 基座）、UI-Venus-2-9B 3.5、UI-TARS-1.5-7B 0.5；GUI agents 全 ≤3.5（ReCAP 1.6、EvoCUA 2.9） | Table 1 |
| 时空类 Claude Opus 5.5 更高 | Astra 唯一非第一类别 | Table 1 |
| 训练馆 | 500 实例/题（时空类 200、回合 ×2.3）、共 5.5 万条验证轨迹、重放 oracle 解落盘、终态过检才保留、vision encoder 冻结、thinking-off 交叉熵 | §3.3 |
| 三重防泄漏 | 测试种子 {36,43,50} 跳过；M_train∩M_test=∅（Open Images/COCO/Poly Haven/ambientCG）；回放后空间配置哈希去重 | §3.3 |
| 建题与审查 | Claude Code＋Opus 5.5 写任务程序；每题 100 种子程序化检查（oracle 必解/random/do-nothing 几乎不过）→ Claude Sonnet 5.5 试玩查捷径 → 两作者双人试玩 | §3.2 |
| 方向性迁移 | ReCAP +17.2（56.4→73.6）、RefSpatial +19.8（38.3→58.1）、VSI-Bench +9.9（50.5→60.4）、RoboAfford +12.2（67.6→79.8）、Open CaptchaWorld +10.0、SpatialViz +6.1、VABench-Point +7.4；反向 ReCAP agent 在 TuringSpace ≤1.6% | §4.3、Table 2 |
| 机器人案例（指向指令物体 vs 动作发生处） | 基座 vs 微调后指向差异 | Fig 3 |
| 评测口径 | OSWorld 官方 computer-use 实现、1920×1080、≤50 步、pass@1=3 种子×125 任务（375 attempts）、推理档位 medium、16 模型（7 专有+4 开放+5 GUI agent） | §4.1 |
| 人类基线 | 3 名未参与建题作者、只记首次提交 | §4.1 |
| 边界 warnbox | 人工基线仅 3 作者、每题 3 实例 ±6.1 方差大；"测空间而非 GUI 灵巧度"无受控实验；"推理虚构证据辩护"失败分析章节未缓存不引用量化；OOD 上涨为旁证非因果 | Limitations、L2 biggest_gap |

## 编辑收窄

- §2 与失败分析章节不在缓存：摘要级断言（"多数失败源于误读截图""推理很少修正错误信念反而虚构证据辩护"）在画报边界卡中如实标注"方法与样本量不可核验，不引用其量化"。
- "验证馆/训练馆"为编辑比喻（程序化生成器＝无限实例供数），机制描述均出自 §3。
- Open CaptchaWorld 26.9→36.9 在 Table 2 记为 +10.0，画报取该值。
