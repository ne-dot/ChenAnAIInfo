# Loop Engineer 完整翻译与真实使用分析

原始材料：`wtf is Loop Engineer & how to setup for real`

来源：https://www.youtube.com/watch?v=W6x-hb44C0c

---

## 一、英文文案去水整理版

这期内容的核心是 **Loop Engineer**。

作者一开始举了两个真实场景：凌晨 1 点，代码库里还在不断出现新的 PR；另一个 Go loop 已经连续跑了两天，每天自动产出 20 到 40 个 SEO 页面，并持续给公司带来流量。

这些工作不是人一直盯着做的，而是由不同的 agent loop 自动发现问题、自动接任务、自动推进。

所谓 Loop Engineer，重点不是继续手动给 coding agent 写 prompt，而是设计一套 loop，让系统在合适的时间自动唤醒 agent，并让 agent 自己找到该做的事。

### 1. 从 Prompt 到 Harness，再到 Loop

过去一年里，大模型相关概念很多，但可以简单分成几个层级。

Prompt Engineering 主要解决单次调用的问题：怎么把合适的上下文放进 prompt，让模型输出更稳定。

后来模型能力增强，上下文窗口变大，工具调用、MCP、agent workflow 开始普及。模型不再只是输出文本，而是可以调用工具、读取结果、继续思考，再调用下一个工具，直到任务完成。

这时问题变成：如何管理上下文、压缩长对话、按需加载 skill、让 agent 更好地完成一个复杂任务。

Harness Engineering 关注的就是模型之外的运行环境：prompt、上下文管理、工具、hooks、编排逻辑、文件系统、验证方式等。简单说，harness 是所有不是模型本身、但会影响 agent 工作效果的东西。

Loop Engineering 站在更外层。

它不只关心“这一次 agent 能不能把任务做好”，而是关心：

- agent 什么时候应该被唤醒？
- 它被唤醒后应该读什么状态？
- 它完成工作后应该把结果写到哪里？
- 多个 agent session 之间如何共享进度？
- 一个 loop 的发现如何变成另一个 loop 的输入？

因此，Loop Engineer 的核心是：设计触发器、共享状态、日志系统和跨 session 工作流，让 agent 不再依赖人每次手动 prompt，而是能持续运行、持续积累、持续互相喂养。

### 2. Loop Engineer 到底是什么

Loop Engineer 可以理解成 agent 外层的运行系统。

它一方面负责触发 agent runtime，另一方面负责记录状态和日志，让 agent 每次启动时都知道现在发生了什么、之前做过什么、下一步应该做什么。

agent 可以被很多东西触发：

- cron job
- webhook
- 另一个 agent
- support ticket
- 服务器 incident
- 数据指标异常

每次 agent 被唤醒后，它会调查问题、执行动作、产出 backlog 或 idea。主 agent 可以基于这些结果排序优先级，必要时再把任务分配给其他 agent。

这就是 Loop Engineer 和普通 agent 使用方式的区别：

过去是人发现任务，然后 prompt agent。

现在是系统发现信号，自动唤醒 agent，让 agent 执行、记录、再进入下一轮。

### 3. 一个客服 Loop 的例子

假设要做一个 support loop。

最简单的方式是：每 30 分钟唤醒一次 agent，让它查看所有 support tickets，自动处理能处理的问题，并把用户摩擦点、产品反馈和潜在机会记录下来。

这个 loop 本身已经有价值，因为它能持续把客服里的信息整理成产品输入。

更进一步，它还可以触发 coding agent。

比如客服里不断有人反馈“导出文件”相关问题，support loop 会把这个需求写进 `signals/`。当这个 signal 累积到一定程度后，coding loop 可以直接接手，修 bug 或实现功能。修复完成后，系统还可以继续监控是否还有用户遇到同类问题，甚至通知用户问题已经解决。

这里的关键不是“某个 agent 很聪明”，而是多个 loop 共享同一套状态。

### 4. 作者团队的真实 Loop

作者团队里有几个正在运行的 loop。

第一个是 support loop。它每 30 分钟运行一次，处理客服 ticket，并把用户摩擦点和产品想法写入 `signals/`。

`signals/` 是一个共享文件夹，用来记录产品想法、用户反馈、摩擦点和潜在机会。

例如，某次运行中 agent 发现很多用户都在问如何导出文件，它就会创建一个 signal，记录“导出为 Markdown 文件”这个需求。这个文件里会记录相关用户、来源 ticket 和后续新增案例。以后每当类似问题再次出现，agent 会继续往同一个 signal 里追加信息。

第二个是 SEO loop。它每天早上 9 点运行，拉取数据、研究话题、生成或发布 SEO 页面。

SEO loop 不只是产出页面，也会在分析中发现业务机会。比如某个页面点击很多，但转化很差，它可以创建一个 conversion gap signal，提醒增长或产品 loop 处理。

第三个是 product growth loop。它会读取不同来源的 signals，包括客服、SEO、广告、用户行为数据等，再决定哪些 bug、机会或实验应该优先处理。

第四个是 coding loop。当某个 signal 足够明确，比如一个 bug 被多次报告，或者一个需求已经有清晰上下文，它就可以触发 coding agent 去修复或实现。

这几个 loop 的价值来自同一个机制：它们读写同一个 shared brain。

support loop 写入用户反馈，growth loop 读取后排序优先级，coding loop 读取后执行，SEO loop 又可以根据 growth 或 ads loop 的发现调整内容方向。

多个 loop 不是孤立自动化，而是在同一套文件系统上互相喂养。

### 5. 搭建 Loop 的四个核心组件

要让 Loop Engineer 真的跑起来，需要四个组件。

第一是 **triggers**。

trigger 决定 agent 什么时候被唤醒。它可以是定时任务，也可以是 webhook、incident、数据异常，或者另一个 agent 的输出。

第二是 **文件和日志结构**。

这是最重要的部分。没有结构化状态，agent 每次启动都像失忆；有了共享文件系统，不同 session 才能接力工作。

第三是 **tools 和 connectors**。

agent 必须能访问真实业务工具，才能做真实工作。比如 Intercom、Stripe、Supabase、Render、GitHub、analytics 工具等。

第四是 **codebase harness**。

如果 loop 最后要触发 coding agent，那么代码库必须适合 agent 工作：能读懂、能运行、能验证、能并行。

### 6. Codebase Harness：让 Agent 能安全干活

作者强调，代码库必须具备三个特征：legible、executable、verifiable。

**Legible** 指代码库对 agent 可读。

一个好的做法是写一个简短的 `AGENTS.md`，作为索引文件，指向更详细的文档。它不需要把所有内容塞进去，而是让 agent 可以渐进式发现信息。

此外，还可以加入 custom lints。因为不能指望 agent 每次都主动找到所有规则，所以更可靠的方式是把关键约束写进 lint。

例如，如果团队不希望 agent 从 legacy folder 里 import，就可以写一个 lint 规则。一旦 agent 写错，检查工具会自动报错。

**Executable** 指代码库容易启动和测试。

理想状态是 agent 只需要运行一个 `dev-local` 脚本，就能启动完整开发环境。这样 agent 不必把大量 token 和注意力浪费在环境配置上。

代码库还应该支持 worktree。这样多个 agent 可以在不同 worktree 里并行工作，互不冲突。

最好还提供一些脚本，让 agent 快速进入特定状态，比如已登录、未登录、付费用户、空项目等，方便测试具体场景。

**Verifiable** 指 agent 能验证自己的工作。

作者推荐使用 Playwright CLI。它可以让 agent 操作浏览器、测试功能，并录制视频附在 PR 上，方便人类 review。

关键业务流程还应该有端到端测试，比如注册、升级、支付、核心产品流程等。

另外，作者认为不应该让同一个 agent 完全自我验证。更好的方式是让提交 PR 的 agent 再 spawn 一个只读 verifier agent，由另一个 agent 根据详细 spec 做检查。

### 7. 文件系统三层结构

作者认为，一个可复利的 loop 系统，应该有三类文件。

第一类是 **artifacts**。

artifacts 是 agent 工作和发现的结构化输出，相当于共享知识层。

常见 artifact 包括：

- `docs/`
- `signals/`
- `tasks/`
- `tickets/`
- `campaigns/`

每一种 artifact 都应该有自己的文件夹和 README。README 说明这个文件夹放什么、不放什么、每个 item 的 schema 是什么、如何新增和更新。

例如 `signals/` 可以记录产品反馈、用户摩擦点、增长机会、SEO 机会等。每个 signal 可以带 front matter、正文、来源链接和 timeline。

第二类是 **loop contract**。

每个 loop 都应该有自己的 folder 和 README。这个 README 就是 contract，写清楚：

- loop 的目标
- 工作流程
- 能做什么
- 不能做什么
- backlog
- timeline

每次 loop 被触发时，agent 先读这个 contract，再决定下一步动作。

第三类是 **global work log**。

虽然 artifact 和 loop contract 里都有 timeline，但还需要一个全局 `log.md`。

原因是实际工作里会有很多跨 domain 的临时信息。比如某次人工和 agent 协作做了一个复杂决策，它不一定属于某个单一 artifact，但后续 agent 需要知道。

所以每个 agent 开始工作前，应该先读最近 5 到 10 条全局日志；完成一大块工作后，也要写一条新日志。

### 8. Support Loop 的搭建流程

作者以 support loop 为例，给出了一套实际流程。

目标是：每 30 分钟拉取最近 support tickets，分析问题，在信息足够时起草或发送回复，同时记录用户摩擦点、产品想法和明确 bug。

第一步是准备 skills 和工具。

客服 agent 可能需要：

- Intercom：拉取 tickets
- Stripe：检查支付和订阅状态
- Supabase：排查用户或支付数据
- Render：查看后端日志
- triage script：辅助分类和处理 ticket

第二步是写业务上下文文件。

作者会创建一个 `CLAUDE.md`，让 agent 了解业务、产品、用户、仓库结构，以及什么时候可以 spawn engineering agent。

如果涉及代码修复，还会写清楚 worktree 规则，要求每个 coding agent 在独立 worktree 里工作。

第三步是写 `architecture.md`。

这个文件定义整体信息架构，包括有哪些 artifact types、有哪些 loop domains、日志怎么写、文件夹怎么组织。

例如系统里可以有：

- `artifacts/signals/`
- `artifacts/tickets/`
- `artifacts/tasks/`
- `artifacts/docs/`
- `domains/support/`
- `log.md`

第四步是手动跑一次 test run。

不要一开始就自动化。先让 agent 手动处理过去一小时的 tickets，观察它是否能正确分析、起草回复、保存 ticket artifact、生成 signal、识别 bug。

这个阶段的重点是校准 workflow。

第五步是创建 loop contract。

当 test run 看起来稳定后，让 agent 在 `domains/support/` 下创建 README，写清楚这个 loop 的 goal、workflow、boundaries、backlog 和 timeline。

第六步才是设置定时触发。

例如每小时触发一次当前 session，让它按 contract 继续处理 support 工作。

### 9. 这套方法真正强调什么

Loop Engineer 的重点不是某个工具，也不是某个 prompt 技巧，而是一套持续运行的工作系统。

它真正强调三件事：

第一，agent 需要被自动触发，而不是永远等人来 prompt。

第二，agent 需要读写结构化状态，而不是只依赖聊天上下文。

第三，多个 loop 要共享同一个信息层，让客服、增长、SEO、工程之间形成复利。

一句话总结：

Prompt Engineering 解决“这次怎么问”。

Harness Engineering 解决“这次怎么让 agent 做好”。

Loop Engineering 解决“下一次谁来唤醒 agent，它读什么、写什么、如何和其他 loop 一起持续变聪明”。

---

## 二、Loop Engineer 的真实使用判断

这套方法真正值得讨论的地方，不是“概念是否新”，而是它是否真的能在业务里跑起来。

我的判断是：Loop Engineer 有用，但它不是给所有人的银弹。它更像是把 agent 从“临时助手”升级成“持续运行的业务流程”。只要业务里存在重复发生、可观察、可记录、可部分自动处理的工作，它就有现实价值。反过来，如果业务本身还没有稳定流程、数据入口混乱、代码库不可验证，强行上 loop 只会制造更多噪音。

### 1. 它真正适合的场景

Loop Engineer 最适合处理三类事情。

第一类是高频、低到中风险的运营工作，比如客服 ticket 初筛、用户反馈归类、竞品监控、SEO 选题、数据日报、销售线索整理。这些事情本来就需要人周期性检查，agent loop 可以把“定期看一眼”变成自动化。

第二类是有明确输入和输出的增长工作，比如每天看搜索词、分析页面转化、生成内容草稿、记录 conversion gap。这类工作不一定要求 agent 每次都做最终决策，但它可以持续发现机会。

第三类是工程团队里的维护型任务，比如发现重复 bug、补测试、修小问题、更新文档、检查线上错误日志。前提是代码库必须可运行、可测试、可回滚。

### 2. 对行业的好处

对行业来说，Loop Engineer 的意义是让 AI agent 从“聊天界面里的工具”变成“后台持续工作的系统”。

过去的 AI 自动化大多停留在单点任务：写一段代码、总结一篇文章、生成一个回复。而 Loop Engineer 关心的是长期运行：agent 今天发现的问题，明天还能继续追踪；客服里出现的反馈，可以变成产品里的任务；SEO 里发现的机会，可以进入增长 loop。

这会推动行业从 prompt-first 转向 workflow-first。真正的竞争优势不再只是“谁会写 prompt”，而是谁能把业务流程、工具权限、状态记录、验证机制设计得更好。

它也会让小团队获得更强的杠杆。一个两三人的团队，如果能把 support、content、growth、bug triage 这些 loop 跑起来，理论上可以接近一个更大团队的运转密度。

### 3. 对使用者的好处

对个人或团队使用者来说，最大的好处是减少“主动想起要做什么”的成本。

很多工作不是不会做，而是没人持续盯。用户反馈散在客服系统里，SEO 数据没人每天看，线上日志只有出大事才查，产品想法写在不同文档里。Loop 的价值就是让 agent 定期把这些东西捞出来，归类、记录、提醒，甚至推进下一步。

第二个好处是形成组织记忆。这里的记忆不是玄学意义上的 long-term memory，而是很朴素的文件系统：signals、tickets、tasks、log。它比聊天记录更适合跨 session 使用，也更容易被人审计。

第三个好处是把 agent 的输出变成可积累资产。一次客服分析不是一次性结果，而是写入 signal；一次 SEO 分析不是一份报告，而是进入 backlog；一次 bug 修复不是单独 PR，而是和用户反馈、ticket、验证记录关联起来。

### 4. 主要坏处和风险

第一，维护成本会被低估。

很多人听到 loop 会觉得“自动跑起来就好了”，但真实情况是：你需要维护 trigger、权限、文件结构、日志规范、工具连接、失败重试、人工审核边界。如果没有人负责这套系统，它很快会变成一堆自动生成的 Markdown 垃圾。

第二，错误会复利。

好的 signal 会复利，坏的 signal 也会复利。如果 agent 错误分类了用户反馈，后续 growth loop 或 coding loop 可能会基于错误信号继续行动。loop 越自动，错误传播速度越快。

第三，权限风险更高。

当 agent 能访问 Intercom、Stripe、Supabase、Render、GitHub，它不再只是“生成文本的助手”，而是一个能触碰真实用户、真实钱、真实代码和真实生产环境的执行者。权限边界、只读模式、人工确认点必须非常清楚。

第四，容易制造假繁忙。

一个 loop 每天生成几十个页面、几十条 signals、几个 PR，看起来很热闹。但如果没有业务指标验证，很可能只是自动化地制造低价值工作。Loop Engineer 最怕的不是 agent 不工作，而是 agent 一直在工作但没有价值。

第五，对代码库和流程成熟度要求很高。

视频里强调的 legible、executable、verifiable 非常关键。如果一个项目连本地启动都困难，测试不稳定，文档混乱，agent loop 只会把这些问题放大。它不是替代工程基础设施的东西，而是建立在基础设施之上的东西。

### 5. 判断一个 Loop 是否值得做

可以用五个问题判断：

1. 这个任务是否会重复发生？
2. 是否有稳定的数据入口？
3. agent 的输出是否能被结构化记录？
4. 错误成本是否可控？
5. 是否存在明确的人工审核或验证机制？

如果五个问题里有三个以上答案是否定的，就不适合一开始做 loop。更好的方式是先手动用 agent 跑几次，观察 workflow 是否稳定，再把稳定部分自动化。

### 6. 最现实的落地路径

最现实的做法不是一上来搭四五个 loop，而是先做一个低风险 loop。

例如：

- 每天读取客服反馈，生成 `signals/`，但不自动回复用户。
- 每天读取 SEO 数据，生成机会列表，但不自动发布页面。
- 每天读取错误日志，生成 bug triage，但不自动改代码。
- 每周整理产品反馈，更新 backlog，但不自动排期。

等这个 loop 连续运行几周，确认它产生的 signals 真有价值，再逐步给它更多权限。比如从“只记录”升级到“起草回复”，再升级到“低风险场景自动回复”；从“发现 bug”升级到“创建 issue”，再升级到“spawn coding agent 修复并提交 PR”。

### 7. 内容表达建议

这篇选题最好不要包装成“下一个风口概念”，而是讲成一个更务实的问题：

AI agent 已经能做事了，但怎么让它持续做对的事？

Prompt Engineering 解决的是“这一次怎么问”。Harness Engineering 解决的是“这一次怎么让 agent 做好”。Loop Engineering 解决的是“下一次谁来唤醒它，它该读什么状态，写回什么状态，如何避免越跑越乱”。

真正的观点可以更锋利一点：

未来 AI 团队的竞争力，不只是模型能力，也不是 prompt 技巧，而是你能不能把业务变成一组可观测、可触发、可验证、可复利的 loop。

但同时也要补一句：Loop Engineer 不是让 AI 完全接管业务，而是把人从重复巡检和信息搬运中解放出来，让人负责边界、判断和最终责任。

---

## 三、补充材料：Agent Loop 工作手册怎么放进这篇内容

网上还有一条相关材料叫 **Agent Loop 工程手册 / Agent Loop 工作手册**。它和这次视频里的 Loop Engineer 很接近，但不是同一个重点。

Agent Loop 工作手册更像是在讲：**单个 agent loop 怎么稳定执行一个任务**。

Loop Engineer 更像是在讲：**多个 agent loop 怎么被自动触发、共享状态、互相喂养，并长期产生业务复利**。

可以这样区分：

| 概念 | 关注层级 | 核心问题 |
|---|---|---|
| Agent Loop | 单个 agent 的执行循环 | 如何观察、行动、接收反馈、修正下一步，并在正确时间停止 |
| Loop Engineer | 多个 loop 的系统设计 | 谁来唤醒 agent、状态存哪里、多个 loop 如何共享信号并复利 |

### 1. Agent Loop 工作手册的核心内容

Agent Loop 的基本循环是：

目标进入系统后，agent 先组装上下文，再由模型推理，选择动作，调用工具，观察工具结果，然后判断是否满足停止条件。如果没有完成，就把新反馈放进下一轮上下文继续执行；如果完成、超预算或无进展，就停止。

它解决的是一次性 prompt 的几个问题：

- 上下文不再靠人手动复制，而是由系统动态组装。
- 错误不再靠人转述，而是把日志、堆栈、测试结果放回下一轮。
- 是否完成不再只靠人的感觉，而是依赖测试、规则、检查器或明确停止条件。
- 停止不再靠“差不多了”，而是靠完成条件、预算上限或无进展检测。

一个可落地的 Agent Loop 通常包含七类组件：

| 组件 | 作用 |
|---|---|
| Automations | 自动触发循环，比如定时任务、Webhook、CI 事件 |
| Worktrees | 隔离执行环境，避免多个 agent 并行时互相覆盖 |
| Skills | 可复用操作手册，把经验沉淀成规程和命令模板 |
| Plugins / Connectors | 连接外部工具，比如 GitHub、Slack、MCP、数据库、浏览器 |
| Sub-agents | 分工或验收，比如一个生成，一个检查 |
| Memory | 外挂记忆，比如 Markdown、数据库、事件日志 |
| Guardrails | 护栏，比如最大轮数、预算上限、权限控制、无进展检测 |

### 2. Agent Loop 手册里最值得借的几个点

第一，先定义停止条件。

“把代码改好”不是好目标，因为 agent 会把“看起来合理”当成完成。更好的写法是：新增一个能复现 bug 的测试，修复后测试通过，相关测试全部通过，且不修改无关模块。

第二，context 不是写出来的，而是组装出来的。

每一轮上下文都应该根据当前状态动态生成，包括任务目标、停止条件、当前 diff 摘要、最近失败日志、相关记忆、允许调用的工具和安全约束。

第三，失败是下一轮输入。

测试失败、命令报错、页面打不开，不应该只是“失败了”。它们应该变成结构化反馈，进入下一轮。比如记录 `last_action`、`command`、`exit_code`、`error_summary`、`stack_trace`、`changed_files`。

第四，多 agent 验收不能只靠另一个 LLM。

Maker-Checker 模式有用，但如果两个 agent 用同一个底层模型，它们可能共享同样的盲区。代码正确性最好交给单元测试、静态分析、属性测试；事实真实性最好交给外部检索、HTTP 请求、白名单来源；高风险动作最好保留人工审批。

第五，必须控制成本。

Agent Loop 的成本主要来自循环轮数、上下文长度和模型数量。比较现实的做法是：简单任务用便宜模型，关键判断用强模型；只传错误摘要，不传完整日志；中间结果放文件或数据库，不要每轮都塞进 prompt；连续几轮无进展就停止。

### 3. 它和 Loop Engineer 的关系

Agent Loop 工作手册可以看作 Loop Engineer 的底层执行单元。

如果说 Agent Loop 解决的是：

> 一个 agent 被唤醒之后，怎么稳定地把一件事做完？

那 Loop Engineer 解决的是：

> 哪些 agent 应该被唤醒？什么时候唤醒？它们读写同一套什么状态？一个 loop 的发现如何变成另一个 loop 的输入？

所以这篇内容可以把 Agent Loop 工作手册作为补充，而不是主线。

主线仍然应该讲 Loop Engineer：

- 从手动 prompt 变成自动触发。
- 从单个 agent 执行变成多个 loop 协作。
- 从聊天上下文变成共享文件系统。
- 从一次性产出变成长期积累 signals、tasks、tickets 和 logs。

Agent Loop 工作手册负责解释“单个 loop 如何跑稳”；Loop Engineer 负责解释“多个 loop 如何组成一个业务系统”。

### 4. 写作时可以这样用

文章里可以用一小段承接：

> 这里要区分两个概念。Agent Loop 讲的是一个 agent 如何在观察、行动、反馈、修正中完成任务；Loop Engineer 讲的是如何设计一组能持续运行的 loop，让它们被自动触发、共享状态、互相喂养。前者是执行循环，后者是业务系统。

然后重点仍然放在 Loop Engineer 的真实问题：

- 它是不是真的有用？
- 哪些场景适合？
- 哪些场景会变成自动制造垃圾？
- 共享文件系统怎么设计？
- 哪些权限必须收紧？
- 人应该在哪些节点介入？

这样写会比单纯复述概念更有判断力。

参考资料：

- [从 Prompt 到 Agent Loop：让 AI Agent 稳定工作的循环设计方法](https://www.zhang-jian.com/archives/2026-06-16-agent-loop-engineering-design)
- [读完 Agent Loop 工程手册，我有 8 个还没想明白的问题](https://cloud.tencent.com/developer/article/2696181)
