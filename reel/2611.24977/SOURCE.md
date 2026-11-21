# 2611.24977 CANDID — 画报逐项来源映射

论文：Candidate-Driven Intervention for Disciplined Execution in Local CUAs（arXiv 2611.24977v1，2026-11-17）
缓存：research/fulltext/2611.24977.txt（25,965 字节，FULLTEXT: html）。核对日期 2026-11-21，执行模型 glm-5.3。

## 画报元素 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 失败双盒（32.12% / 29.79% / 7.09%） | 8B exact-action loop rate 32.12%、30B 29.79%、OpenCUA 7.09% | Table 2 |
| 失败双盒（DONE 全票率 40.8%） | OpenCUA-7B DONE unanimity 40.8%（8B 88.2/30B 78.2） | Table 2 |
| 双闸门机制（两级环检测） | 规则窗口检测 → 本地模型确认停滞 → 采样 4 候选 → 结构过滤（畸形/环模式/DONE/去重）→ 执行或选择 | §3 Method |
| 双闸门机制（DONE 全票门） | 全票通过才终止；单个 continuation 即拒绝并移除全部 DONE | §3 Method |
| 温度说明 | Qwen 默认 0.7/环恢复 1.0；OpenCUA 默认贪心 0/候选 0.7 | §3/§4 setup |
| 六行哑铃（35.31→38.80 等） | Table 3：30B s=50 +3.49、s=100 +4.26；8B +2.02/+2.01；OpenCUA-7B +3.84/+4.54，5 trials 均值 | Table 3 |
| 基线对照横杆 | GTA-1 25.19、Self-Guidance 33.30（降）、VLAA-LoopBreaker 36.98、VLAA-Verifier 34.22、VLAA-Combined 35.84、CANDID 38.80（30B） | Table 4 |
| 全票 vs 多数表 | 重定向 49.93%、假成功 241.33→171.67、Hit Max 19.33→64.67（×3.3）、准确率 26.06→30.60；作者自认 precision 56.7%/specificity 26.3%，"不构成可靠语义完成验证器" | Table 5、§4.2 |
| 逐点采样对照（23.48% vs 38.80%） | per-step dense 采样 23.48%（Hit Max 239、假成功 44.0）vs CANDID 38.80%（116.6/105.2）；Avg steps 36.89 vs 24.40 | Table 6 |
| 候选数 1→4 升、4→8 递减 | 候选芯片行注记；主实验 k=4 | Fig 6、§4.3 |
| 运营统计 | loop 触发 26.6% 步（57.1% 实际干预）、DONE 门控 4.6% 步（45.7% 干预）、selector 58.2%/77.6% 被结构过滤绕过 | Table 7 |
| 开销 KPI | prompt token +19%、359.0→396.1 s/任务（+10%）、轨迹 25.6→24.4 步 | §4.4、Table 7 |
| 边界 warnbox | 单 OSWorld、候选塌缩时无效、环检测只抓局部模式 | Limitations |

## 编辑收窄

- §2 失败分析与 Table 1 不在缓存："naively scaling merely shifts failure pattern" 仅引言断言，画报注记"§4.3 消融间接印证"，不引用其原始量化。
- WindowsAgentArena 154 任务仅在附录 B.4（不在缓存），画报未提。
- "双闸门"为编辑概括（loop 检测＋DONE 门控两条干预通道），机制描述均出自 §3。
