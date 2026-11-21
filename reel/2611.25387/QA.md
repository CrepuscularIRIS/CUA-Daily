# QA 记录 — 2611.25387 TuringSpace

**结论：ready（0 重做 / 0 fail）。**

流程：
1. 渲染（reel/render_poster.py，google-chrome headless）：1500×2820，render-check.json = contentBottom 2730 ≤ 2820、overflow []、fontOK true（PosterCN 400/700 loaded）、pdfPages 1 → pass。
2. 画布预检一次即达标（初稿即 2820，未加高），不占重做额度。
3. 视觉 QA：read_image 实开 poster.png 全图 + 4 段全分辨率裁图（0–765/705–1470/1410–2175/2115–2820）逐段目检：无溢出、无裁切、无重叠；五类空间卡第三卡"时空推理"红色顶边完整、2×3 网格无挤压；九行榜单哑铃与数值列对齐；方向性迁移双段条（基座浅/增益深）底部平齐；三重防泄漏 check 行换行正常；footer 完整落画布内。
4. 字体：本地 Noto Sans CJK SC woff2 子集（reel/2611.25387/assets/fonts/），渲染无远程请求。
5. 数字核对：画报全部数值与 research/fulltext/2611.25387.txt 及 SOURCE.md 映射一致；§2/失败分析未缓存小节未引用（边界卡注明）。

遗留观察：无。
