from _common import PROV, rating, score

M1, M2, M3, M4, M5 = "M1", "M2", "M3", "M4", "M5"
SHA = {
    M1: "293bb7190ce5e7130b67136aba5c5df4803da0e9d1fc3f86212525b804fe1ac0",
    M2: "6bb91bd3ce3d84f5e4c903e386c4cb42d0a6dc52a7b19f3cfe70ffabab07c7dd|e31c69029e713bf2cb3e16bc29250b8e894247853be8fd4065e74115c248e39f|cd295431b918a9ffd6c2bacdd9620f9b9a8a8ebf94d4d9a25653207d6475c94c",
    M3: "97d5b3d6fb473c80d134464bcbc5a946259c73de13c6b7b0780851dc422f953a|d87599b8d61e7218b0624b4b211208e182b02c3b9fa9c62508c8fe3b6edbeadf",
    M4: "87feadb8e33d1f4624ea6b05aa980306a60da2a1b03cb2b44da6f1cf8b753fc9",
    M5: "896882a2c125ec2595dc2ed78f638950bc0b0a7c04c187bafa82c8174d7ecc62",
}


def ev(i, mat, loc, quote, why, kind="author_report"):
    return {"evidence_id": i, "material_id": mat, "material_sha256": SHA[mat], "locator": loc,
            "quote": quote, "support_explanation": why, "kind": kind}


EVIDENCE = [
    ev("W01", M1, "Abstract", "We show that WebVoyager achieves a 59.1% task success rate on our benchmark, significantly surpassing the performance of both GPT-4 (All Tools) and the WebVoyager (text-only) setups", "作者中心主张(agent 成功率)。"),
    ev("W02", M1, "Abstract", "The proposed automatic evaluation metric achieves 85.3% agreement with human judgment,", "作者次要主张:GPT-4V 自动评测与人工一致 85.3%。"),
    ev("W03", M1, "Abstract", "Existing web agents typically only handle one input modality and are evaluated only in simplified web simulators or static web snapshots, greatly limiting their applicability in real-world scenarios.", "作者 gap。"),
    ev("W04", M1, "Sec 1", "This approach, however, may not fully account for the variety of viable strategies to accomplish a task, as it only reflects one possible plan.", "对离线单参考(golden trajectory)评测的批评。"),
    ev("W05", M1, "Sec 3.1", "Unlike WebArena Zhou et al. (2023) , we do not host any websites locally and allow the agent to explore the open web instead", "与自托管 WebArena 对比:开放网页环境(漂移)。"),
    ev("W06", M1, "Sec 3.2", "we perform context clipping to remove outdated web page information and only keep the three most recent observations in the inputs, and we keep the entire history of thoughts and actions to better guide the agent.", "上下文:最近 3 个观测+全部 thought/action 历史。"),
    ev("W07", M1, "Sec 3.3", "GPT-4V-Act is efficient since it is rule-based without incorporating any object detection model.", "元素标注靠规则化 JS 抽取交互元素并叠加编号框(Set-of-Mark 式),非检测器。"),
    ev("W08", M1, "Sec 3.3", "We observe that using a single black color yields higher success rates than using multiple colors.", "标注颜色的设计选择只有断言,无数字/消融。"),
    ev("W09", M1, "Sec 3.3", "We also provide the agent with auxiliary text as inputs, including the textual content embedded within the interactive element, the type of the element, and possibly some comment text in the aria-label attribute.", "辅助文本输入。"),
    ev("W10", M1, "Sec 3.3", "Note that each error correction attempt also consumes one step from the total exploration budget.", "仅有执行异常的报错重试,并占用步数预算;无结果验证/反思。"),
    ev("W11", M1, "Sec 5 Experimental Details", "We set the temperature to 1 during generation and allow the agent to explore at most 15 steps.", "温度 1,最多 15 步。"),
    ev("W12", M1, "Sec 5 Experimental Details", "We employ GPT-4 Turbo with vision (gpt-4-vision-preview) as the backbone model of our agent", "主骨干 gpt-4-vision-preview。"),
    ev("W13", M1, "Sec 5 Experimental Details", "We include the GPT-4 (All Tools) for baselines, which integrates vision, web browsing, code analysis, and various plugins in one model. Additionally, we consider a text-only baseline where the agent only receives the websites’ accessibility tree as input to prediction actions.", "基线:GPT-4 (All Tools) 产品与 a11y-tree 文本-only。"),
    ev("W14", M1, "Sec 5.2", "their performance is significantly better than the Text-only setting (with GPT-4 as the backbone).", "文本-only 基线骨干为 GPT-4,与视觉版 GPT-4V 不同:模态与骨干混杂。"),
    ev("W15", M1, "Table 1", "WebVoyager 65.1% 61.9% 59.5% 70.7% 76.7% 44.2% 63.0% 59.1%", "人工判定整体 59.1%(与 GPT-4 All Tools 30.8%、text-only 40.1% 对照)。"),
    ev("W16", M1, "Table 1", "GPT-4 (All Tools) 25.6% 9.5% 2.4% 53.7% 60.5% 37.2% 52.2% 30.8%", "GPT-4 (All Tools) 整体 30.8%。"),
    ev("W17", M1, "Table 1", "WebVoyager ∗ 71.3% ±1.3% 60.3% ±2.8% 51.6% ±1.4% 64.3% ±2.8% 77.5% ±2.7% 55.8% ±2.3% 60.9% ±2.2% 57.1% ±0.2%", "GPT-4V 自动评测整体 57.1% ±0.2:± 来自评测器 3 次运行,不是 agent 重复运行。"),
    ev("W18", M1, "Table 1 caption", "For each automatic evaluation, we run GPT-4V evaluator three times to calculate the performance mean and standard deviation.", "方差仅覆盖评测器重复。"),
    ev("W19", M1, "Sec 5.1", "We adopt human evaluation as our main evaluation metric since most of the questions in our benchmark have open-ended answers.", "主指标=人工判定完整轨迹。"),
    ev("W20", M1, "Sec 5.1", "For a subset of 300 tasks, we invite three annotators to judge each trajectory to understand the agreement among human annotators.", "人工一致性仅在 300 任务子集;其余任务的评判者数量/流程未述。"),
    ev("W21", M1, "Table 2", "Full 58.3% 85.3% 0.70", "GPT-4V 与人工在完整轨迹上一致 85.3%,κ=0.70(k=1 时 75.3%/0.51)。"),
    ev("W22", M1, "Sec 5.2", "Claude-3-Opus, on the other hand, demonstrates a clear preference for its own results, believing that GPT-4V and GPT-4o are similar but considers itself to have the best performance.", "评测器存在自偏好,未校正。"),
    ev("W23", M1, "Table 3", "GPT-4V 57.1 55.1 63.0 Claude-3-Opus 52.8 61.6 55.4 GPT-4o 55.5 54.9 64.1", "骨干×评测器矩阵:对角线(自评)最高,评测器改变绝对成功率 ~55-64。"),
    ev("W24", M1, "Sec 4.2", "Initially, we manually sample and rewrite some tasks from Mind2Web ( Yin et al., 2023 ; Deng et al., 2023 ) for websites including Google Flights, Google Map, Google Search, Booking, and Wolfram Alpha.", "种子任务改写自 Mind2Web(5 个站点)。"),
    ev("W25", M1, "Sec 4.2", "prompt GPT-4 Turbo to generate approximately 100 new tasks (20 iterations).", "self-instruct 生成任务,随后人工核验可答性与重复度。"),
    ev("W26", M1, "Sec 4.2", "In total, we collected 40+ tasks per website, resulting in a total of 643 tasks.", "643 任务/15 站点。"),
    ev("W27", M1, "Sec 4.3", "In total, 22.3% of questions are annotated with golden responses, and the rest only have possible answers.", "仅 22.3% 有 golden 答案,其余为‘可能答案’(开放/实时)。"),
    ev("W28", M1, "Sec 4.1", "Due to technical limitations, we regretfully omit websites requiring login or CAPTCHA to access their content.", "范围排除登录/CAPTCHA 站点。"),
    ev("W29", M1, "Sec 5.2", "Finally, WebVoyager has a success rate of 30% on the SeeAct online test set whereas the best SeeAct autonomous agent has 26%, showing the efficacy of our proposed agent.", "外部 50 任务集:30% vs 26%(差 4 点,n=50,无方差)。"),
    ev("W30", M1, "Sec 5 Dataset and Metrics", "we also evaluated on 90 web browsing tasks (Level 1 and Level 2) from the GAIA dataset", "外部集 GAIA 90 任务;结果在 Fig 5(图未提供,数值 unknown)。"),
    ev("W31", M1, "Table 4", "Navigation Stuck 44.4% Visual Grounding Issue 24.8% Hallucination 21.8% Prompt Misalignment 9.0%", "失败分布(300 任务抽样人工标注)。"),
    ev("W32", M1, "Sec 5.4", "The agent also tends to repeat its previous mistakes due to the input clipping, as mentioned in section 3.2 .", "作者承认截图裁剪导致重复犯错(C15 失败模式)。"),
    ev("W33", M1, "Sec 5.2", "This is primarily because these websites are more text-heavy than others.", "文本密集站点上视觉模式不占优。"),
    ev("W34", M1, "Sec 5.3", "we observe that the text-only agent demonstrates significantly poorer performance on websites with complex visual elements, such as Booking and Flights", "文本-only 在 Booking/Flights 显著更差(与 Table 1:2.3%/7.1% vs 43.2%/59.5% 一致)。"),
    ev("W35", M1, "Sec 5.3", "the primary limitation of GPT-4 (All Tools)’s performance is rooted in its reliance on Bing search for web browsing", "GPT-4 (All Tools) 受限于 Bing 取页,不能直接操作站点:基线机制不同。"),
    ev("W36", M1, "Sec 5.3", "most open-sourced LMMs such as LLaVA ( Liu et al., 2024 ) reduce the image resolution to 224x224 or 336x336", "未测开源模型,理由是分辨率/上下文。"),
    ev("W37", M1, "Limitations", "First, we haven’t supported all possible actions in our environment compared to actions a human user might take when browsing the web. e.g. the Drag action on web pages.", "动作空间局限。"),
    ev("W38", M1, "Sec 5.4", "Prematurely terminating the process using the ANSWER action, though agent knows that the task is not yet complete", "自宣告终止;无完成验证器,提前 ANSWER 属 prompt 对齐失败。"),
    ev("W39", M1, "Sec 3.1 footnote 4", "Regarding CAPTCHAs (Completely Automated Public Turing test to tell Computers and Humans Apart) challenges, we believe it is important to respect the rules of these websites and prompt the agent to retrieve information from alternative sources.", "CAPTCHA 策略(绕道换源),并非报告阻塞比例。"),
    ev("W40", M1, "Sec 5.4", "We sampled 300 tasks from our benchmark and manually labeled the error category for each failed case", "失败标注覆盖 300 任务抽样。"),
    ev("W41", M1, "App E", "SeeClick Cheng et al. (2024) focused on finetuning an LMM to solely leverage screenshots as inputs to interact with websites.", "同期最近邻:SeeClick(微调 LVLM,screenshot-only)。"),
    ev("W42", M1, "Sec 2", "However, the best SeeAct agent still relies on a finetuned cross-encoder model to select candidate elements for interaction.", "最近邻:SeeAct 依赖微调 cross-encoder 候选筛选;SeeAct 原文不在共享引用集。"),
    ev("W43", M1, "Sec 5.3", "In our case, the agent needs to handle trajectories as long as 15 steps, and it requires approximately 7000+ tokens", "成本仅此一句:15 步约 7000+ token,无金额/延迟。"),
    ev("W44", M2, "Fig 7 (PDF page 14 render, image)", None, "图读取:系统提示=‘像人类一样浏览网页’,观测=带编号标签的截图+文本;列出 Click/Type/Scroll/Wait/GoBack/Google/ANSWER 格式;含 Action 与 Web Browsing guidelines(原文以 ‘...’ 截断,全文不可得);要求输出 Thought 与 Action。", "our_inference"),
    ev("W49", M2, "Fig 8 (pdfpage15-fig8-evaluator.png, image)", None, "图读取:评测器提示=给定任务指令、结果截图、结果文本回答;不得交互、不得据截图之外信息假设;多子任务缺一即不成功;回答与截图矛盾时以截图为准;需先写判断依据再给 'SUCCESS' 或 'NOT SUCCESS'。未向评测器提供 Golden/Possible 参考答案。", "our_inference"),
    ev("W45", M3, "Fig 6 (page_complexity.png, image)", None, "图读取(近似):平均轨迹长度约 3(Wolfram)–10(Google Flights/Booking)步;每步平均元素数约 14(Allrecipes)–73(ESPN);颜色=成功率。仅作定性使用。", "our_inference"),
    ev("W46", M4, "Mind2Web Sec 4 metrics", "Each step of the task is evaluated independently with the ground truth action history provided.", "参考文献 Mind2Web:离线逐步评测带真值历史,支持 WebVoyager 对其批评。"),
    ev("W47", M5, "WebArena Sec 2.3", "a screenshot, a pixel-based representation that represents the current web page as an RGB array and (3) the accessibility tree of the web page.", "WebArena 观测空间已含截图与 a11y tree 选项:WebVoyager 对其‘只是初步’的定位需限定为‘未系统探索视觉 agent’。"),
    ev("W48", M1, "Sec 1", "Particularly, vision capability is crucial for utilizing tools such as web browsers, as rendered web pages are inherently designed with user experience (UX), emphasizing intuitive information and structured presentation.", "方法假设(视觉比冗长 HTML 更有效),由 Table 1 的站点级差异部分检验。"),
]

R = {}
R["G"] = rating("resolved", 3,
    "gap 具体:现有 web agent 多为单模态(HTML)且在简化模拟器/静态快照上评测(W03),离线单参考评测不容多种可行路径(W04,配合 Mind2Web 原文的带真值历史逐步评测 W46),WebArena 为自托管(W05)。"
    "残余瓶颈与代价已落实:文本密集站点、视觉 grounding(24.8%)、导航卡住(44.4%)(W31/W33)。"
    "不足:最近邻 SeeAct、Set-of-Mark、AppAgent 原文不在共享引用集,SeeAct 差别只凭作者描述(W42)、同期 SeeClick 只在附录一句带过(W41);‘WebArena 只是初步探索视觉’的措辞与 WebArena 已含截图观测选项(W47)不完全吻合。边界较清楚故为 3。",
    ["W03", "W04", "W05", "W31", "W33", "W46"], ["W41", "W42", "W47"])
R["M"] = rating("resolved", 3,
    "操作与假设可重建:规则化 JS 在截图上叠加数字标签(W07)+辅助文本(W09)+ReAct thought→action(W06)+3 张截图上下文裁剪(W06)+执行异常重试(W10)。"
    "站点级差异支持其机制预测——复杂视觉站点(Booking/Flights)文本-only 明显更差(W34),文本密集站点无增益(W33)。"
    "不足:机制主要是 Set-of-Mark/ReAct/ GPT-4V 的组合,没有对标记、辅助文本、裁剪窗口、报错重试的单项机制检验(W08 仅断言);文本-only 对照骨干不同(W14)。",
    ["W06", "W07", "W09", "W10", "W33", "W34", "W48"], ["W08", "W14"])
R["X"] = rating("resolved", 3,
    "agent 循环、观测、动作空间与格式(Appendix C)、上下文裁剪、步数/温度、窗口大小均可重建(W06/W11/W44),报错重试占用步数(W10)。"
    "不足:无完成验证/反思/恢复机制,自宣告 ANSWER 导致提前终止(W38);无状态保存;系统提示中的 guidelines 在论文里以‘...’截断(W44),评测器提示 Fig 8 已由补证页核读(W49);动作空间缺拖拽(W37);限定非登录/非 CAPTCHA 站点(W28);裁剪导致重复错误(W32)。生效条件与失败模式写得较清楚,但恢复/验证接口缺位。",
    ["W06", "W10", "W11", "W44"], ["W32", "W37", "W38"])
R["E.measurement"] = rating("resolved", 3,
    "以人工判定完整轨迹为主指标(W19),并报告 GPT-4V 自动评测的一致性(Table 2:85.3%/κ=0.70,W21),换三种评测器检验了偏差并披露自偏好(W22/W23),对照基线也由同一人工流程评判(W15/W16)。"
    "不足:开放网页无可执行判据,约 77.7% 任务只有‘可能答案’(W27);人工评判者数量与盲评流程只在 300 子集写明(W20);未报告评测器对‘成功/失败’判定的分别精确率/NPV;评测器与被测 agent 同族(GPT-4V 判 GPT-4V,W22);验证只用 WebVoyager 自身轨迹,未用其他 agent 的轨迹验证评测器;评测器提示(Fig 8,W49)规则合理(截图优先、多子任务缺一即失败),但不给它参考答案,答案是否正确只能凭截图可见内容判断。",
    ["W15", "W16", "W19", "W21", "W23", "W49"], ["W20", "W22", "W27"])
R["E.causality"] = rating("resolved", 1,
    "有两项对照:GPT-4 (All Tools) 与 a11y-tree 文本-only(W13)。但前者是不同机制的商业产品且受 Bing 取页限制(W35),后者骨干为 GPT-4 而非 GPT-4V(W14),模态与骨干混杂;"
    "核心设计(数字标签颜色、辅助文本、3 张截图裁剪、报错重试、Google 跳转动作)均无单项消融(W08 仅断言),裁剪还被作者承认引发重复错误(W32)。站点级差异只提供间接证据(W34/W33),‘视觉+文本都必要’的结论依赖混杂对照。",
    ["W13", "W34", "W33"], ["W14", "W35", "W08", "W32"])
R["E.holdout"] = rating("resolved", 2,
    "全程为提示式 agent,无训练数据污染路径;在 15 个未登录站点之外还报告了 GAIA 90 任务与 SeeAct 50 任务两个外部集(W30/W29:30% vs 26%),并有中文/西班牙语定性示例。"
    "不足:基准由作者自建,种子取自 Mind2Web 的 5 个站点(W24);系统提示开发是否见过测试任务未述;骨干预训练污染未讨论;GAIA 结果在 Fig 5(未提供,unknown);SeeAct 外部集 n=50 差距 4 点无方差;范围限定非登录站点(W28),‘真实世界网站’主张宜降为这些站点。",
    ["W29", "W30", "W24"], ["W28"])
R["E.statistics"] = rating("resolved", 1,
    "主表每站仅 40-45 任务(W26),Table 1 的 ± 来自评测器 3 次重复而非 agent 重复(W17/W18);agent 在温度 1 下采样(W11)却未见多次运行均值/置信区间;"
    "κ 与一致率只给点估计(W21)。有 300 任务的失败分类分布(W31/W40),但没有每站失败分母。故仅部分满足。",
    ["W17", "W18", "W21", "W31"], ["W11"])
R["E.cost"] = rating("resolved", 1,
    "报告步数上限 15、温度、窗口大小(W11),指出 15 步约 7000+ token(W43),并给出因步数耗尽而‘导航卡住’占失败 44.4%(W31),Fig 6 近似给出各站平均轨迹长度 3-10 步(W45,近似读图)。"
    "不足:无美元成本/延迟/调用数;基线 GPT-4 (All Tools) 的预算与步数上限未披露,无法判断预算公平。",
    ["W11", "W31", "W43", "W45"], [])

RATINGS = R

SIGNATURES = [
    {"sig_id": "S1", "object": "提示式浏览器 agent 循环(Selenium + GPT-4V 类 LMM;亦测 Claude 3 Opus、GPT-4o)",
     "information": "每步:带数字标签与黑框的页面截图(规则 JS 提取交互元素)+辅助文本(元素文本/类型/aria-label);历史=最近 3 个观测+全部 thought/action;无多标签页;不可见:DOM 全树、真值答案",
     "operation": "ReAct 式 Thought→Action;7 个动作(Click/Type/Scroll/Wait/GoBack/Google/ANSWER);PDF 自动解析入观测;动作异常→回传错误信息重试(占步数)",
     "output": "格式化动作字符串;ANSWER 返回任务答案",
     "conditions": "窗口 1024×768,温度 1,最多 15 步;非登录、非 CAPTCHA 站点",
     "feedback": "页面渲染截图与执行异常信息;无结果验证/反思",
     "selection_rule_data": "无选择/拒绝规则;无训练",
     "persistence": "无跨任务保存", "later_use": "none",
     "claimed_effect": "人工评判整体成功率 59.1%(GPT-4 All Tools 30.8%,text-only 40.1%)",
     "failure_boundary": "导航卡住 44.4%、视觉 grounding 24.8%、幻觉 21.8%、提示对齐 9.0%;文本密集站点弱;无拖拽",
     "evidence_ids": ["W06", "W07", "W09", "W10", "W11", "W15", "W31", "W38", "W44"]},
    {"sig_id": "S2", "object": "WebVoyager 评测集(15 个真实站点、643 任务)",
     "information": "种子:Mind2Web 改写+人工;GPT-4 Turbo self-instruct 迭代;人工核验答案可在站点找到;答案标注 Golden(22.3%)/Possible",
     "operation": "语义相似度审计(all-mpnet-base-v2,全部 206,403 对中 49 对>0.8)",
     "output": "任务集与参考答案", "conditions": "仅非登录站点;实时信息答案会漂移",
     "feedback": "none", "selection_rule_data": "人工核验/改写,低重复检查",
     "persistence": "公开基准", "later_use": "后续评测(非本文证据)",
     "claimed_effect": "覆盖多样真实站点的端到端评测",
     "failure_boundary": "Possible 答案非严格真值;站点漂移",
     "evidence_ids": ["W24", "W25", "W26", "W27", "W28"]},
    {"sig_id": "S3", "object": "GPT-4V 自动评测协议",
     "information": "任务+agent 回答+最后 k 张截图(或完整轨迹);温度 0;提示见 Fig 8(W49):截图优先于回答、不得假设截图外信息、多子任务缺一即失败;不提供 Golden/Possible 参考答案",
     "operation": "二分类判成功/不成功;与人工在 300 子集比一致率/κ;交叉评测骨干×评测器",
     "output": "成功/失败标签", "conditions": "k 越大一致越高(k=1 75.3%,full 85.3%)",
     "feedback": "none", "selection_rule_data": "k 作为超参数(选择数据未述)",
     "persistence": "none", "later_use": "none",
     "claimed_effect": "κ=0.70 与人工一致,GPT-4V 可作为在线 agent 的自动评测器",
     "failure_boundary": "自偏好(Claude/GPT-4o/GPT-4V 各自偏爱自己);评测器与被测同族;无分类别精确率/NPV;只能核对截图里可见的内容,未用参考答案核对答案内容",
     "evidence_ids": ["W18", "W19", "W20", "W21", "W22", "W23", "W49"]},
]

GAP = {
    "author_gap": "既有 web agent 只处理单模态(HTML/文本)且只在简化模拟器或静态快照上评测,难以用于真实网站。",
    "checked_gap": "gap 成立:Mind2Web 逐步离线评测带真值历史(W46)、WebArena 自托管(W05);视觉 agent 在真实站点上的端到端评测当时稀缺(同期有 SeeAct、SeeClick)。‘WebArena 只做初步视觉探索’需限定(W47:WebArena 已提供截图观测选项)。",
    "lineage": [
        {"ancestor": "ReAct 提示范式", "relation": "祖先", "source": "WebVoyager Sec 3.2;原文在共享引用集(2210.03629)", "version": "n/a", "availability": "paper-only"},
        {"ancestor": "Set-of-Mark prompting", "relation": "祖先(标记)", "source": "WebVoyager Sec 3.3 自述;原文不在共享引用集", "version": "n/a", "availability": "unresolved"},
        {"ancestor": "WebArena(a11y tree / 截图观测、自托管)", "relation": "最近邻环境", "source": "共享引用 2307.13854", "version": "n/a", "availability": "verified"},
        {"ancestor": "Mind2Web(离线逐步)", "relation": "最近邻评测/种子来源", "source": "共享引用 2306.06070", "version": "n/a", "availability": "verified"},
        {"ancestor": "SeeAct(同期,cross-encoder 候选筛选)", "relation": "最近邻(同期)", "source": "WebVoyager Sec 2/Sec 5.2 自述;原文不在共享引用集", "version": "n/a", "availability": "unresolved"},
        {"ancestor": "SeeClick(同期,微调 LVLM 的 screenshot-only)", "relation": "最近邻(同期)", "source": "WebVoyager App E 一句话;原文在共享引用集 2401.10935", "version": "v2", "availability": "verified"}],
    "closest_adjacent": "SeeAct:同为 GPT-4V 在真实网站,但依赖微调 cross-encoder 筛选候选;SeeClick:微调 LVLM 输出坐标,无需 DOM;WebVoyager 用规则抽取的元素编号标签,不需训练,在作者的 50 任务集上高 4 点。",
    "residue": "文本密集页面上截图识别弱(W33)、视觉 grounding 误差(24.8%)、步数耗尽(44.4%)、缺少完成验证/恢复;评测依赖人工/LLM 判定。",
    "stakes": "真实网站任务的端到端成功率决定可用性;评测方式决定结论可信度。",
    "method_response": "规则化数字标签截图+文本辅助+ReAct+上下文裁剪构成端到端 agent;自建真实站点基准与 GPT-4V 评测器配套。",
    "remaining_gap": "各设计成分的单独贡献、跨站点/跨时间的稳定性、评测器偏差、需登录站点、效率与成本。",
    "current_relevance": "后续在线基准与评测器审计工作(本批材料外)可能修正该基准的区分度;不用于反推发表时的问题位置。",
    "evidence_ids": ["W03", "W04", "W05", "W41", "W42", "W46", "W47"],
    "unresolved": ["SeeAct/Set-of-Mark/AppAgent 原文不在共享引用集;谱系仅凭作者描述;空检索不代表新颖性。"],
}

RS = {
    "primary": None, "supporting": [], "matches": [], "outside_taxonomy": True,
    "reason": "逐篇阅读后判定无单一原卡的实际操作与本文执行的操作签名吻合:(1)agent 是不训练的提示式浏览器循环(规则叠加标签+ReAct+上下文裁剪),原 15 卡的操作签名围绕假设/证明/目标/表示变换,不描述这类 harness;"
              "(2)评测基准+GPT-4V 评测器与 controlled_diagnostic_design/C02 部分相邻,但没有‘一次只改变一个混杂变量的受控实例’或独立真值(评测器校验使用人工判定而非受控构造),故不套用;"
              "(3)self-instruct 生成任务+人工核验形似 self_supervised_signal_engineering/C08 的‘生成+过滤’,但产物用作评测集而非训练信号;(4)‘截图替代 HTML’形似 architectural_operator_substitution,但其卡要求证明保持关键性质,本文只做经验比较。"
              "仍完整评价该论文;outside_taxonomy 不扣分。",
    "considered_not_selected": [
        {"main_id": "controlled_diagnostic_design", "sub": "rs:C02", "why": "无单变量受控构造;真值为人工判定,但评测集由 LLM 生成且开放答案(W27),不是 C02 的 oracle-independent 控制实例。"},
        {"main_id": "self_supervised_signal_engineering", "sub": "rs:C08", "why": "生成+人工过滤的对象是评测任务而非训练信号。"},
        {"main_id": "architectural_operator_substitution", "sub": None, "why": "无保持性质的证明;经验比较的骨干也不同(W14)。"},
        {"main_id": "adapt_via_conditioning", "sub": "rs:C03", "why": "零样本提示,无统一条件化格式的跨任务留出验证。"}],
    "executes_pattern": {"value": "not_applicable", "reason": "outside_taxonomy。", "evidence_ids": []},
    "resolves_problem": {"value": "partial", "reason": "在作者基准上人工判定 59.1% 优于文本-only 与 All Tools,支持‘视觉+文本 agent 在真实站点可行’;评测可靠性与成分归因未闭合,不能称真实网页 agent 问题已解决。", "evidence_ids": ["W15", "W16", "W31"]},
}

DOMAIN = {
    "namespace": "gui",
    "matches": [
        {"main": "structured_screen_observation", "sub": "C01", "version": "taxonomy_sha256:430aa362…", "fit": "strong",
         "condition_checks": [
             {"id": "S1", "kind": "success", "name": "Targets exposed by the structural view", "status": "met", "evidence_ids": ["W07", "W28"], "note": "仅评测可由 DOM 元素枚举的非登录网页;排除登录/CAPTCHA 站点。"},
             {"id": "S4", "kind": "success", "name": "Observation modalities compared under one backbone", "status": "partial", "evidence_ids": ["W13", "W14"], "note": "有 a11y-only 对照,但骨干为 GPT-4 vs GPT-4V,非同骨干。"},
             {"id": "F3", "kind": "failure", "name": "Marks drawn on dense text-heavy pages", "status": "observed", "evidence_ids": ["W31", "W33"], "note": "视觉 grounding 占失败 24.8%,文本密集站点无增益。"},
             {"id": "F2", "kind": "failure", "name": "Duplicate or text-less elements", "status": "observed", "evidence_ids": ["W31"], "note": "文中提到相邻元素混淆、日历数字被当作标签。"},
             {"id": "F4", "kind": "failure", "name": "Mark reading assumed for any backbone", "status": "partial", "evidence_ids": ["W36", "W23"], "note": "测了 GPT-4V/Claude 3 Opus/GPT-4o,三者均为前沿模型;开源 LMM 因分辨率/上下文未测。"},
             {"id": "F5", "kind": "failure", "name": "Actions bound to structure inherit structure errors", "status": "observed", "evidence_ids": ["W31"], "note": "‘向错误文本框输入仍然有效且无报错’属 Hallucination 类(Sec 5.4)。"},
             {"id": "F6", "kind": "failure", "name": "Parsing cost and per-site pruning losses unreported", "status": "observed", "evidence_ids": ["W07"], "note": "规则 JS 抽取的成本/逐站点损失未报告。"}],
         "evidence_ids": ["W06", "W07", "W09", "W13", "W14", "W34"],
         "reason": "操作与 C01 完全对应:从 DOM 枚举交互元素、画数字标记并要求以标签编号执行动作。"},
        {"main": "agent_loop_context_control", "sub": "C20", "version": "taxonomy_sha256:430aa362…", "fit": "strong",
         "condition_checks": [
             {"id": "S2", "kind": "success", "name": "Recent steps at full fidelity, older steps as text, with the window ablated", "status": "partial", "evidence_ids": ["W06", "W32"], "note": "保留 3 张最近截图+全部 thought/action 文本(对应 C15 的一部分),窗口大小未消融。"},
             {"id": "F2", "kind": "failure", "name": "Summaries hide errors over long horizons", "status": "observed", "evidence_ids": ["W32"], "note": "作者自述裁剪导致重复犯错。"},
             {"id": "F4", "kind": "failure", "name": "No role-removal ablation and unreported per-step cost", "status": "observed", "evidence_ids": ["W08", "W43"], "note": "未对标签/辅助文本/裁剪/报错重试做单项消融,也无成本。"},
             {"id": "F1", "kind": "failure", "name": "Reflector and self-check accuracy unmeasured", "status": "not_applicable", "evidence_ids": ["W10", "W38"], "note": "无反思器;完成判定为自宣告 ANSWER,提前终止属提示失败。"}],
         "evidence_ids": ["W06", "W10", "W11", "W38", "W44"],
         "reason": "每步 thought→action 的固定 schema 与自宣告终止对应 C20;上下文裁剪对应 C15 的一部分(见 secondary_candidates)。"},
        {"main": "learned_outcome_and_process_judges", "sub": "C25", "version": "taxonomy_sha256:430aa362…", "fit": "strong",
         "condition_checks": [
             {"id": "S1", "kind": "success", "name": "Judge agreement with humans reported", "status": "met", "evidence_ids": ["W21", "W19"], "note": "300 子集 85.3%/κ=0.70;但无分类别精确率/NPV。"},
             {"id": "S2", "kind": "success", "name": "Completion visible in the judged state", "status": "partial", "evidence_ids": ["W21"], "note": "k=1 仅 75.3% 一致;完整轨迹才达 85.3%。"},
             {"id": "F3", "kind": "failure", "name": "Systematic bias treated as noise", "status": "observed", "evidence_ids": ["W22", "W23"], "note": "自偏好被披露但未修正。"},
             {"id": "F2", "kind": "failure", "name": "Disagreement with humans on free-form tasks", "status": "observed", "evidence_ids": ["W21", "W27"], "note": "约 14.7% 不一致;77.7% 任务仅有‘可能答案’。"}],
         "evidence_ids": ["W02", "W19", "W21", "W22", "W23", "W49"],
         "reason": "GPT-4V 以任务+回答+截图判定轨迹成功并与人工对齐,正是 C25 的操作(提示见 W49);本文用作评测而非 RL 奖励。"}],
    "unassigned": [],
    "secondary_candidates": [
        {"main": "online_evaluation_methodology", "sub": "C24", "why": "真实站点+人工判定评测;与 C25 同属评测设计,主匹配取 C25 以避免重复计。"},
        {"main": "agent_loop_context_control", "sub": "C15", "why": "上下文裁剪:最近 3 张截图完整、更早仅保留 thought/action 文本。"}],
    "revision_proposals": [{"note": "领域卡 C01/C25 的 sources 含本文(2401.13919#s1-#s3),卡片由本文推导,匹配度高有循环性;本席按自己的阅读复核,未采信卡片内的数值。", "status": "proposal_unchecked"}],
}

MAPPING = [
    {"rs_main": None, "rs_sub": None, "domain": {"namespace": "gui", "main": "structured_screen_observation", "sub": "C01"},
     "operation_correspondence": "无对应原卡:规则叠加元素标签的观测表示属 harness 设计;最近的 architectural_operator_substitution 要求证明保持性质而本文仅经验比较。",
     "required_conditions_and_differences": "领域卡匹配强,原卡层 outside_taxonomy;两层不互相替代。", "evidence_ids": ["W07", "W14"]},
    {"rs_main": None, "rs_sub": None, "domain": {"namespace": "gui", "main": "learned_outcome_and_process_judges", "sub": "C25"},
     "operation_correspondence": "与 controlled_diagnostic_design/C02 只部分相邻(评测仪器),缺少单变量受控实例与独立真值,故不映射。",
     "required_conditions_and_differences": "评测器真值来自人工判定,且仅为 300 子集抽样。", "evidence_ids": ["W19", "W21"]},
]

EXPECTATIONS = [
    {"id": "E04", "version": "profile expectations.json sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E04"],
     "applies_when": "a claim about web-agent success on real, live websites", "applicable": True, "status": "partial",
     "reason": "有独立外部实时集(GAIA 90、SeeAct 50:30% vs 26%,W29/W30)但无期望所指的 Online-Mind2Web/Mind2Web-Live,我无法据固定材料确定其时间先后,不据此扣分;自建基准的难度/可被简单基线解决程度未检验。", "evidence_ids": ["W29", "W30", "W24"], "score_item": "E.holdout"},
    {"id": "E10", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E10"],
     "applies_when": "a method that uses an LLM/VLM judge to label trajectory success for evaluation", "applicable": True, "status": "partial",
     "reason": "评测器与人工在 300 子集校验(W21),并换评测器检验(W23);但只验证了 WebVoyager 自身轨迹,没有用未参与构建评测器的其他 agent 轨迹验证,也未给成功率差距。", "evidence_ids": ["W20", "W21", "W23"], "score_item": "E.measurement"},
    {"id": "E11", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E11"],
     "applies_when": "a claim that a GUI-agent judge is reliable enough to serve as evaluator", "applicable": True, "status": "unmet",
     "reason": "只报告总体一致率与 κ,未分正/负判定报告精确率与 NPV。", "evidence_ids": ["W21"], "score_item": "E.measurement"},
    {"id": "E16", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E16"],
     "applies_when": "an empirical comparison on a live benchmark where sampling and environment noise vary across runs", "applicable": True, "status": "unmet",
     "reason": "± 仅为评测器 3 次运行,agent 在温度 1 下的重复运行未报告。", "evidence_ids": ["W11", "W17", "W18"], "score_item": "E.statistics"},
    {"id": "E17", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E17"],
     "applies_when": "a comparison of agent success where methods or baselines may run with different step caps", "applicable": True, "status": "partial",
     "reason": "WebVoyager 与变体用 15 步上限,并给出步数耗尽占失败 44.4%;GPT-4 All Tools 的步数上限未述。", "evidence_ids": ["W11", "W31", "W13"], "score_item": "E.cost"},
    {"id": "E20", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E20"],
     "applies_when": "a claim measured on live websites", "applicable": True, "status": "partial",
     "reason": "用 Golden/Possible 标注应对实时漂移并排除登录/CAPTCHA(W27/W28/W39);文中未给出评测日期,也未报告被封锁/失效任务数。", "evidence_ids": ["W27", "W28", "W39"], "score_item": "E.holdout"},
    {"id": "E21", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E21"],
     "applies_when": "a comparison of GUI agents whose observation spaces may differ", "applicable": True, "status": "partial",
     "reason": "分别报告截图+标签与 a11y-tree-only,但骨干不同(GPT-4V vs GPT-4),且未做‘截图+a11y’增强。", "evidence_ids": ["W13", "W14", "W15"], "score_item": "E.causality"},
    {"id": "E23", "version": "profile sha 4663f2b4…", "source_strength": "single_source", "source_refs": ["profile E23"],
     "applies_when": "a new benchmark or a claim about long-horizon GUI task capability", "applicable": True, "status": "partial",
     "reason": "有 300 任务失败原因分布与站点级轨迹长度/元素数 vs 成功率图(W31/W45,图为近似读图),无按人类参考步数分层。", "evidence_ids": ["W31", "W45"], "score_item": "E.statistics"},
    {"id": "core-E10", "version": "patterns card text (not in profile file)", "source_strength": "common_practice", "source_refs": ["patterns/main/structured_screen_observation.md"],
     "applies_when": "a claim that a particular perception input improves an agent", "applicable": True, "status": "partial",
     "reason": "同骨干对照缺失(W14),无 a11y+截图混合或仅截图(无标签)消融。", "evidence_ids": ["W13", "W14"], "score_item": "E.causality"},
    {"id": "core-E11", "version": "patterns card text (not in profile file)", "source_strength": "common_practice", "source_refs": ["patterns/main/structured_screen_observation.md"],
     "applies_when": "a claim that an element-marking scheme helps GUI agents in general", "applicable": True, "status": "partial",
     "reason": "测了 Claude 3 Opus、GPT-4o,开源 LMM 因分辨率/上下文被排除(W36),主张宜限定为前沿多模态模型。", "evidence_ids": ["W23", "W36"], "score_item": "E.holdout"},
    {"id": "E15", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E15"],
     "applies_when": "a claim measured with offline teacher-forced step metrics", "applicable": False, "status": "not_applicable",
     "reason": "本文为在线端到端评测,没有以离线 step 指标支撑能力主张。", "evidence_ids": ["W15"], "score_item": None},
    {"id": "E22", "version": "profile sha 4663f2b4…", "source_strength": "common_practice", "source_refs": ["profile E22"],
     "applies_when": "a claim that a training recipe generalises across policy backbones", "applicable": False, "status": "not_applicable",
     "reason": "无训练 recipe;跨三种前沿骨干的结果已在 E.holdout/core-E11 中记录。", "evidence_ids": ["W23"], "score_item": None},
]

CLAIMS = [
    {"claim_id": "C1", "text": "WebVoyager 在自建 643 任务、15 站点基准上人工判定成功率 59.1%,显著高于 GPT-4 (All Tools) 30.8% 与文本-only 40.1%。",
     "setting": "gpt-4-vision-preview,温度 1,≤15 步,1024×768,非登录站点;人工评判完整轨迹", "baseline_control": "GPT-4 (All Tools) 产品;a11y-tree 文本-only(GPT-4 骨干)",
     "selection_vs_test": "无训练;系统提示/标注颜色等设计选择是否见过测试任务未述", "result_denominator": "643 任务,每站 40-45;agent 单次运行(未报告重复)",
     "evidence_ids": ["W01", "W13", "W15", "W16", "W26"], "counterevidence": ["W14", "W35", "W08"],
     "allowed_conclusion": "在作者构建的实时站点任务集上,单次运行的 GPT-4V+标签截图 agent 的人工判定成功率高于所列两种基线;视觉模态与骨干混杂,不能把差距全部归因于视觉设计。"},
    {"claim_id": "C2", "text": "GPT-4V 自动评测与人工一致(85.3%,κ=0.70),可作可靠评测器。",
     "setting": "300 任务子集;完整轨迹截图;温度 0", "baseline_control": "三名人工(κ 0.7)、Claude 3 Opus(κ 0.6)、GPT-4o(κ 0.72)",
     "selection_vs_test": "k 作为超参数选择;未说明在哪份数据上选 k", "result_denominator": "300 任务;无分正负类指标",
     "evidence_ids": ["W02", "W19", "W20", "W21", "W22"], "counterevidence": ["W22", "W23", "W27"],
     "allowed_conclusion": "在 300 个 WebVoyager 轨迹上,完整轨迹的 GPT-4V 评测器与共识人工标签的一致性与人际一致相当;对其他 agent、其他类型任务及正/负判定的可靠性未验证,自偏好存在。"},
    {"claim_id": "C3", "text": "方法在不同骨干(Claude 3 Opus、GPT-4o)上同样明显优于文本-only。",
     "setting": "GPT-4V 评测器;单次运行", "baseline_control": "文本-only 44.3% (GPT-4V 评测)",
     "selection_vs_test": "—", "result_denominator": "52.8% / 55.5% vs 44.3%;评测器改变绝对值(Table 3)", "evidence_ids": ["W14", "W17", "W23"],
     "counterevidence": ["W22", "W23"], "allowed_conclusion": "三种前沿多模态骨干的数值较接近且高于文本-only 基线(骨干不同的混杂依旧);GPT-4o 作评测器会给出更高数值。"},
    {"claim_id": "C4", "text": "在 SeeAct 的 50 个在线任务上优于其最佳自治 agent(30% vs 26%);GAIA 90 任务上优于两基线。",
     "setting": "外部任务集;GAIA 从 Google Search 起步", "baseline_control": "SeeAct 的结果(取自其论文);GAIA 上同两基线",
     "selection_vs_test": "—", "result_denominator": "n=50 / n=90;GAIA 数值在 Fig 5(未提供)", "evidence_ids": ["W29", "W30"],
     "counterevidence": [], "allowed_conclusion": "SeeAct 集上 4 点差距(n=50,无方差,基线取自论文)不足以排除噪声;GAIA 结论无法核对。"},
    {"claim_id": "C5", "text": "视觉与文本信号对通用 web agent 都必要。",
     "setting": "站点级对比与错误分析", "baseline_control": "文本-only vs 视觉",
     "selection_vs_test": "—", "result_denominator": "站点 40-45 任务", "evidence_ids": ["W33", "W34", "W31"],
     "counterevidence": ["W14"], "allowed_conclusion": "站点级模式与‘复杂视觉页面更需截图,文本密集页面更需文本’一致,但没有同骨干消融,也未证明‘文本增强截图’能弥补。"},
]

ASSESSMENT = {
    "evidence_level": "online",
    "evidence_level_note": "真实实时网站上的在线交互;成功由人工/LLM 判定轨迹而非可执行检查,评测器经 300 子集人工核验但存在自偏好;无未见环境专门留出(不构成 transfer)。",
    "claim_support": "scoped",
    "author_claim": "WebVoyager 是端到端、可在真实网站完成任务的 LMM web agent,成功率 59.1%,显著优于基线;自动评测器与人工 85.3% 一致。",
    "strongest_supported_claim": "在作者自建的 15 站点(非登录)、643 任务集上,单次运行的 GPT-4V+数字标签截图 agent 的人工判定成功率为 59.1%,高于 GPT-4 (All Tools) 30.8% 与 GPT-4 a11y-tree 文本-only 40.1%;GPT-4V 评测器在 300 个 WebVoyager 轨迹子集上与人工一致 85.3%(κ=0.70)。",
    "still_unsupported": ["视觉标签/辅助文本/裁剪/报错重试各自的贡献", "对其他 agent、其他站点、其他时间的稳定性", "评测器对正/负判定分别的可靠性", "GAIA 上的优势(Fig 5 未读)", "真实世界网站的泛化"],
    "unresolved": ["Fig 5(GAIA)数值未提供;Fig 7 系统提示被论文截断(以 ‘...’ 省略部分 guidelines)"],
    "reproduction": "作者报告,非我们复现。",
}

RETENTION = {"applicable": False, "reason": "提示式 agent,无持久化改动/选择/留存闭环;不编造 retained 链。"}

PAPER = {
    "paper_key": "2401.13919", "paper_id": "arXiv:2401.13919",
    "title": "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models", "version": "2401.13919v4",
    "claim_type": "system_method",
    "claim_type_note": "主体是 agent 系统;同时贡献 643 任务基准与 GPT-4V 评测器(次要评测资源主张),按 system_method 评价并把评测器作为 E.measurement 的一部分。",
    "central_claim": "WebVoyager 是由大型多模态模型驱动、可通过与真实网站交互端到端完成用户指令的 web agent;在自建 15 站点 643 任务基准上任务成功率 59.1%,显著优于 GPT-4 (All Tools) 与文本-only;提出的 GPT-4V 自动评测与人工判断一致率 85.3%。",
}

MATERIALS = [
    {"material_id": M1, "url": "https://arxiv.org/html/2401.13919v4", "path": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2401.13919.txt", "sha256": SHA[M1],
     "sections_read": ["Abstract", "1-6", "Limitations", "Ethics", "References(skim)", "App A-F", "Tables 1-4"], "complete": True,
     "missing_sections": ["Fig 5(GAIA 成功率)数值——图未在总控补证中", "Figs 9-28 轨迹截图(定性)未逐张读"],
     "note": "文件后半为同一正文的第二份渲染,已核对重复。"},
    {"material_id": M2, "url": "n/a (figs: pdfpage13/14)", "path": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext-figs/2401.13919/pdfpage13-fig78.png|pdfpage14-fig78.png", "sha256": SHA[M2],
     "sections_read": ["Fig 7 系统提示(page 14)", "Appendix A-C 页(page 13)", "Fig 8 评测器提示(page 15)"], "complete": False, "missing_sections": [], "note": "总控补证(含 pdfpage15 的 Fig 8 评测器提示);sha 为 figs.json 记录。"},
    {"material_id": M3, "url": "n/a (figs)", "path": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext-figs/2401.13919/page_complexity.png|episode_h_large.png", "sha256": SHA[M3],
     "sections_read": ["Fig 6", "Fig 4"], "complete": True, "missing_sections": [], "note": "Fig 6 数值仅近似读图,不作为评分数字依据。"},
    {"material_id": M4, "url": "https://arxiv.org/html/2306.06070", "path": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2306.06070.txt", "sha256": SHA[M4],
     "sections_read": ["metrics"], "complete": False, "missing_sections": ["仅核对指标定义"], "note": "共享引用集成员。"},
    {"material_id": M5, "url": "https://arxiv.org/html/2307.13854", "path": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2307.13854.txt", "sha256": SHA[M5],
     "sections_read": ["Sec 2.3 observation space"], "complete": False, "missing_sections": ["仅核对观测空间"], "note": "共享引用集成员。"},
]


def build(meta):
    rec = {
        "schema_version": "radar-review-v2.2",
        "run_id": meta["run_id"], "batch_id": meta["batch_id"], "attempt_id": meta["attempt"], "seat": "son55",
        "paper": PAPER, "provenance": PROV, "materials": MATERIALS, "evidence": EVIDENCE,
        "signatures": SIGNATURES, "retention_trace": RETENTION, "gap": GAP, "rs_pattern": RS,
        "domain_pattern": DOMAIN, "pattern_mapping": MAPPING, "expectations": EXPECTATIONS,
        "claims": CLAIMS, "assessment": ASSESSMENT, "ratings": RATINGS, "score": score(RATINGS),
        "status": "reviewed",
        "status_reason": "全文(含附录)已通读,另读总控补证的 Fig 4/6/7 页;Fig 5(GAIA)未提供;Fig 8 评测器提示已核读。",
        "contamination": "未读另一席/Opus/旧分数/旧 Reel/archive;领域卡 sources 含本文自身(循环性已在 revision_proposals 标注)。",
    }
    return rec
