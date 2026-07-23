# 03 - Loop Engineer 内容工程

## 项目目标

围绕 **Loop Engineer** 做一组自媒体内容，而不是单篇稿子。

核心问题：

> AI Agent 已经能做事了，但怎么让它持续做对的事？Loop Engineer 到底有用，还是又一个烧 token 的概念？

本期内容要同时完成四件事：

1. 做一个长视频，发布 B 站和 YouTube。
2. 拆成多个抖音/视频号/小红书短视频。
3. 整理成公众号、掘金等平台的使用手册。
4. 做一个实际 demo，展示 Loop Engineer 如何从用户反馈进入产品/工程闭环。

## 核心观点

Loop Engineer 不是 Prompt Engineering 的新包装，也不是单个 Agent Loop 的执行技巧。

Prompt Engineering 解决“这一次怎么问”。

Agent Loop 解决“一个 agent 被唤醒后，怎么观察、行动、反馈、停止”。

Harness Engineering 解决“一个 agent 工作时，工具、上下文、文档、验证环境怎么搭”。

Loop Engineering 解决“哪些 agent 应该被唤醒，什么时候唤醒，读写什么共享状态，多个 loop 如何互相喂养，并长期产生业务复利”。

## 目标受众

- 已经用过 Cursor、Claude Code、Codex、Devin 等 AI coding 工具的人。
- 对 AI Agent 有兴趣，但还停留在手动 prompt 阶段的人。
- 做 SaaS、独立产品、自媒体工具、AI 应用的小团队。
- 想把客服、增长、内容、研发流程自动化的人。

不主要面向纯小白。可以解释基本概念，但重点要放在真实落地判断。

## 内容主线

长视频主线：

1. 开头案例：用户反复反馈“导出文件”问题，support loop 自动沉淀 signal，coding loop 修复，support loop 回头通知用户。
2. Loop Engineer 是什么：从手动 prompt 到自动触发，从单个 agent 到多个 loop。
3. 它和 Prompt Engineering、Agent Loop、Harness Engineering 的区别。
4. 一个真实系统长什么样：support loop、SEO loop、growth loop、coding loop 共享 `signals/`。
5. 搭建 Loop 的四个组件：trigger、shared state、tools/connectors、codebase harness。
6. 真实使用判断：哪些场景有用，哪些场景会变成自动烧钱和自动制造垃圾。
7. 实操 demo：用一个小型 support-to-product loop 展示完整闭环。
8. 结尾判断：Loop Engineer 的难点不是让 AI 一直跑，而是知道什么时候不让它跑。

## 关键案例

### 用户反馈到产品修复闭环

流程：

1. 多个用户在客服里反馈“导出文件不好用 / 想导出 Markdown”。
2. support loop 定期读取客服记录，把同类问题合并进 `signals/export-markdown.md`。
3. signal 记录来源用户、出现次数、原始反馈、影响范围、建议动作。
4. 当 signal 达到阈值，例如出现 3 次以上，product/growth loop 将它标记为高优先级。
5. coding loop 读取 signal 和任务说明，创建实现任务或修复 bug。
6. verifier loop 跑测试或检查结果。
7. support loop 找到相关 ticket，生成“问题已修复”的用户通知草稿。
8. 系统继续监控未来是否还有同类反馈。

这个案例是整期内容的主心骨。

它的价值在于：

> 用户反馈不再死在客服系统里，而是自动变成产品和工程系统里的待办。

## 产物清单

### 1. 长视频

目标平台：B 站、YouTube。

建议时长：12-18 分钟。

文件：

- `scripts/long-video-outline.md`
- `scripts/long-video-script.md`
- `storyboard/`
- `renders/`

视频定位：

不是纯概念科普，而是“判断 + 系统设计 + demo 展示”。

暂定标题：

- 《Loop Engineer：AI Agent 真正自动化的下一步？》
- 《别再手动 Prompt 了，AI Agent 开始自己找活干》
- 《Loop Engineer 是什么？从用户反馈到自动修 Bug 的 AI 工作流》

### 2. 短视频矩阵

目标平台：抖音、视频号、小红书、B 站竖屏切片。

建议拆 8 条：

1. 什么是 Loop Engineer？一句话讲清楚。
2. Prompt Engineering、Agent Loop、Harness Engineering、Loop Engineer 到底差在哪？
3. 最牛的案例：用户反馈如何自动变成产品修复。
4. 为什么 `signals/` 比“长期记忆”更靠谱？
5. Loop Engineer 的四个组件。
6. 真跑起来有多烧 token？怎么控制成本？
7. 哪些场景适合做 loop，哪些不适合？
8. 未来团队竞争力：不是 prompt，而是能不能把业务变成 loop。

文件：

- `shorts/01-what-is-loop-engineer.md`
- `shorts/02-concept-differences.md`
- `shorts/03-support-to-coding-loop.md`
- `shorts/04-signals-shared-memory.md`
- `shorts/05-four-components.md`
- `shorts/06-token-cost.md`
- `shorts/07-good-and-bad-use-cases.md`
- `shorts/08-business-as-loops.md`

### 3. 图文手册

目标平台：公众号、掘金、知乎、即刻长文。

建议拆成两篇：

第一篇偏认知：

《Loop Engineer 是什么：AI Agent 从工具变成系统》

结构：

1. 为什么只会 prompt 已经不够了。
2. Loop Engineer 的定义。
3. 它和 Agent Loop / Harness Engineering 的区别。
4. support loop + SEO loop + growth loop + coding loop 案例。
5. 它真正带来的变化。

第二篇偏实操：

《Loop Engineer 使用手册：如何搭一个真实可跑的 Agent Loop 系统》

结构：

1. 先判断是否值得做。
2. 设计 trigger。
3. 设计 shared state。
4. 设计 loop contract。
5. 设计 tools/connectors。
6. 设计 verifier 和人工审核点。
7. 成本控制和失败停止。
8. 一个最小可行 demo。

文件：

- `articles/01-loop-engineer-explainer.md`
- `articles/02-loop-engineer-playbook.md`

### 4. 实际 Demo

Demo 名称：

**Support Signal Loop：从用户反馈到产品任务**

目标：

不用接真实客服系统，先用本地 mock tickets 展示完整流程。

Demo 输入：

- `demo/input/tickets/*.md`：模拟客服反馈。
- 其中多条 ticket 都提到“导出 Markdown / 导出文件 / 找不到导出入口”。

Demo 输出：

- `demo/artifacts/signals/export-markdown.md`
- `demo/artifacts/tickets/*.md`
- `demo/artifacts/tasks/implement-markdown-export.md`
- `demo/log.md`

演示流程：

1. 运行 support loop，读取 mock tickets。
2. 自动归类同类问题。
3. 生成或更新 signal。
4. 如果 signal 达到阈值，生成 product/engineering task。
5. 模拟 coding loop 接收任务。
6. 生成修复完成后的用户通知草稿。

视频里可以不一定真的写完整产品功能，但要展示这个闭环的文件系统变化。

## Demo 的技术原则

为了适合内容展示，demo 要轻量：

- 不接真实 Intercom，先用本地 Markdown 模拟。
- 不直接调用真实付费 API，必要时用脚本模拟 agent 输出。
- 文件结构要清晰，能被观众一眼看懂。
- 重点展示 loop 思路，不追求复杂代码。
- 保留成本讨论：真实环境可以接客服、数据库、GitHub，但必须有权限和预算控制。

## 内容判断重点

这期不能写成“Loop Engineer 又来了，赶紧学”。

要强调：

- 它确实有用，但不是所有团队都适合。
- 它最适合高频、可观察、可记录、低到中风险的流程。
- 它最大的风险是自动烧钱、自动制造垃圾、错误信号复利。
- 成熟的 Loop Engineer 不是让 AI 一直跑，而是设计触发条件、停止条件和人工审核点。

## 落地检查表

这组问题是后续长视频和图文手册的重要框架。

### 1. 怎么触发？

定时、用户反馈、Webhook、告警、人工按钮、另一个 loop。

### 2. 谁来处理？

脚本、小模型、AI agent、Codex、Claude Code。

原则：规则能做的用规则，脚本能做的用脚本，需要理解和判断的地方才用 agent，需要改代码时再调用 coding agent。

### 3. 状态放哪里？

`signals/`、`tasks/`、数据库、GitHub Issues、Linear、Notion。

状态必须可追踪、可共享、可审计。

### 4. 什么时候进入下一步？

阈值、人工确认、severity、复现步骤、测试结果、verifier 结果。

### 5. 怎么验证？

单元测试、E2E、Playwright、verifier agent、人工 review、线上监控。

### 6. 哪些事情不能自动做？

自动部署、自动发邮件、自动删数据、自动改支付 / 权限 / 安全逻辑、高风险代码自动合并。

这部分可以作为视频里的判断金句：

> Loop Engineer 不是让 AI 一直跑，而是把触发、状态、推进、验证和人工闸门设计清楚。

## 推荐工作顺序

本项目先做 demo，再写视频和文章。

原因：

先写文案容易停留在概念解释；先把 demo 跑通，才能知道哪些地方真的有价值、哪些地方容易失控、哪些地方适合录屏展示。

调整后的顺序：

1. 做最小可用 demo：`tickets/ -> support loop -> signals/ -> tasks/ -> followups/`。
2. 录制或截图 demo 的关键过程，沉淀可展示素材。
3. 基于 demo 结果重写长视频主线，让视频从真实案例出发，而不是从概念出发。
4. 写长视频脚本初稿。
5. 制作长视频分镜和视频。
6. 从长视频中拆短视频脚本。
7. 写公众号/掘金手册，把 demo、方法论、成本和风险沉淀成图文。
8. 发布后根据评论反馈，追加短视频和第二篇文章。

## 当前第一阶段：Demo 先行

第一阶段目标：

做出一个本地可运行、可录屏、可解释的 **Support Signal Loop**。

最小闭环：

```text
mock 客服反馈 tickets
  -> support loop 归类用户卡点
  -> signals/export-markdown.md
  -> product loop 生成工程任务
  -> tasks/implement-markdown-export.md
  -> coding loop 模拟实现和验收
  -> followups/ 用户通知草稿
```

第一阶段产物：

- `demo/input/tickets/*.md`
- `demo/scripts/support-loop.js`
- `demo/scripts/product-loop.js`
- `demo/scripts/coding-loop-sim.js`
- `demo/artifacts/signals/export-markdown.md`
- `demo/artifacts/tasks/implement-markdown-export.md`
- `demo/artifacts/followups/*.md`
- `demo/log.md`

第一阶段验收：

- 可以一条命令或三条命令跑完整 demo。
- 跑完后文件系统发生清晰变化。
- 每个输出文件都适合在视频里展示。
- 不调用真实 API，不产生 token 成本。
- 能自然引出成本、权限、验证和人工审核问题。

## 当前资料

- [Loop Engineer 完整翻译与真实使用分析.md](/Users/zj/Documents/AI 自媒体/Loop Engineer 完整翻译与真实使用分析.md)
- 原始视频：https://www.youtube.com/watch?v=W6x-hb44C0c
- Agent Loop 参考：https://www.zhang-jian.com/archives/2026-06-16-agent-loop-engineering-design
- Agent Loop 讨论：https://cloud.tencent.com/developer/article/2696181
