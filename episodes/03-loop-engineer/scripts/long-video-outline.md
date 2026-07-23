# 长视频大纲：Loop Engineer 是什么，真的有用吗？

## 视频定位

这不是一条“新概念速通”视频，而是一条判断型内容。

主问题：

> Loop Engineer 是 AI Agent 真正自动化的下一步，还是又一个听起来很美、实际烧 token 的概念？

目标时长：12-18 分钟。

## 标题备选

1. 《Loop Engineer：AI Agent 真正自动化的下一步？》
2. 《别再手动 Prompt 了，AI Agent 开始自己找活干》
3. 《从用户反馈到自动修 Bug：Loop Engineer 到底是什么》
4. 《Loop Engineer 有多强？也有多烧钱？》

## 开头 Hook

开头不要从概念讲起，直接讲案例。

示例开头：

> 假设你的客服系统里，有 3 个用户都在问同一个问题：为什么不能导出 Markdown？  
> 过去这件事大概率会停在客服系统里。客服回复一下，产品经理有空再看，研发什么时候排期不确定。  
> 但在 Loop Engineer 的思路里，这条反馈会被 support loop 自动写进 `signals/`。如果后面越来越多用户提到同一个问题，这个 signal 的权重会变高。等上下文足够清楚，coding loop 可以直接接手修复。修复之后，support loop 还能回到原来的 ticket，告诉用户：你之前遇到的问题已经解决了。  
> 这不是 AI 客服，而是一个从用户反馈到产品改进的自动闭环。

## 结构

### 1. 先讲结论

Loop Engineer 的核心不是写更好的 prompt，而是设计一套让 agent 自动触发、共享状态、持续运行的系统。

一句话：

> Prompt Engineering 解决这次怎么问；Agent Loop 解决单个 agent 怎么跑稳；Harness Engineering 解决 agent 工作环境怎么搭；Loop Engineering 解决下一次谁来唤醒 agent，它读什么、写什么，怎么和其他 loop 形成复利。

### 2. 为什么现在会出现 Loop Engineer

不用大讲历史，只提必要背景：

- 早期大模型主要是单次文本生成，所以大家研究 prompt。
- 后来工具调用和长上下文普及，agent 可以自己调用工具、读取结果、继续行动。
- 再后来任务变长，单个 session 不够，需要跨 session、跨 agent 协作。
- 一旦跨 session，就必须有共享状态：文件、日志、任务、signals。

关键转折：

> 当 AI 不只是回答问题，而是持续做事时，真正的问题就从“怎么问”变成了“怎么组织它持续做对的事”。

### 3. Loop Engineer 和几个概念的区别

表格讲清楚，不要纠缠术语。

| 概念 | 解决的问题 |
|---|---|
| Prompt Engineering | 单次调用如何稳定输出 |
| Agent Loop | 一个 agent 如何观察、行动、反馈、停止 |
| Harness Engineering | agent 的工具、上下文、验证环境怎么搭 |
| Loop Engineering | 多个 loop 如何触发、共享状态、互相喂养 |

重点：

Agent Loop 是底层执行循环，Loop Engineer 是上层业务系统设计。

### 4. 一个真实 Loop 系统长什么样

用四个 loop 串起来：

1. support loop：每 30 分钟读客服 ticket，处理问题，写入 `signals/`。
2. SEO loop：每天读搜索和页面数据，生成内容，也发现转化缺口。
3. growth loop：读取所有 signals，判断优先级。
4. coding loop：当问题足够明确时，修 bug、实现小功能、提交 PR。

核心画面：

```
support tickets -> support loop -> signals/
SEO data -> SEO loop -> signals/
signals/ -> growth loop -> tasks/
tasks/ -> coding loop -> PR / fix
PR / fix -> support loop -> user follow-up
```

这一段要强调：

> 多个 loop 的价值不在于各自自动化，而在于它们读写同一个 shared brain。

### 5. 搭建 Loop 的四个组件

#### Trigger

谁来唤醒 agent？

- cron
- webhook
- incident
- 新 ticket
- 指标异常
- 另一个 agent 的输出

#### Shared State

agent 读写什么？

- `signals/`
- `tasks/`
- `tickets/`
- `docs/`
- `log.md`
- loop contract README

#### Tools / Connectors

agent 能操作什么？

- 客服系统
- 数据库
- 支付系统
- 日志系统
- GitHub
- 浏览器
- 数据分析工具

#### Codebase Harness

如果要让 coding loop 真干活，代码库必须：

- legible：有 `AGENTS.md`、架构文档、规则。
- executable：一条命令跑起来。
- verifiable：测试、Playwright、只读 verifier agent。

### 6. 真实使用判断：它到底有没有用

有用的地方：

- 高频重复巡检。
- 客服反馈归类。
- SEO / 增长机会发现。
- bug triage。
- 文档和测试维护。
- 小团队放大执行密度。

不适合的地方：

- 没有稳定输入。
- 错误成本高。
- 缺少验证机制。
- 数据和权限混乱。
- 业务流程本身还没跑顺。

一句判断：

> Loop Engineer 不是给混乱流程打 AI 补丁，而是把已经可观察、可记录、可验证的流程放大。

### 6.5 落地检查表：设计一个 Loop 前先问六个问题

这一段可以放在视频后半段，作为从概念走向工程实现的检查表。

不要把 Loop Engineer 讲成某个工具。它真正要解决的是六个设计问题。

#### 1. 怎么触发？

可选方式：

- 定时触发
- 用户反馈触发
- Webhook 触发
- 告警触发
- 人工按钮触发
- 另一个 loop 触发

例子：

support loop 可以每 30 分钟跑一次，也可以在用户提交反馈后触发。

incident loop 可以由线上告警触发。

coding loop 不一定定时跑，更适合在 task ready 后触发。

#### 2. 谁来处理？

不一定每一步都要大模型。

可选处理者：

- 普通脚本
- 规则系统
- 小模型
- AI agent
- Codex
- Claude Code

原则：

规则能做的用规则，脚本能做的用脚本，需要理解和判断的地方才用 agent，需要改代码时再调用 coding agent。

#### 3. 状态放哪里？

Loop Engineer 最重要的是把状态放到对话外面。

可选状态层：

- `signals/`
- `tasks/`
- `tickets/`
- `log.md`
- 数据库
- GitHub Issues
- Linear
- Notion

重点不是工具，而是状态必须可追踪、可共享、可审计。

#### 4. 什么时候进入下一步？

不能每个反馈都触发工程动作。

进入下一步可以依赖：

- 阈值
- 人工确认
- severity
- 复现步骤是否完整
- 测试结果
- verifier 是否通过

例子：

同类反馈出现 3 次以上，才生成 task。

task 被人工标记为 `ready_for_coding`，才触发 coding loop。

verifier 通过后，才生成用户回访草稿。

#### 5. 怎么验证？

Loop 不是跑完就算完成。

验证方式包括：

- 单元测试
- E2E 测试
- Playwright 浏览器检查
- verifier agent
- 人工 review
- 线上监控回看

尤其是 coding loop，不能让同一个 agent 自己说自己修好了。

#### 6. 哪些事情不能自动做？

越真实的系统，边界越重要。

通常不应该全自动的动作：

- 自动部署
- 自动发用户邮件
- 自动删数据
- 自动改支付 / 权限 / 安全逻辑
- 自动合并高风险代码

一句话总结：

> Loop Engineer 不是让 AI 一直跑，而是把触发、状态、推进、验证和人工闸门设计清楚。

### 7. 最大问题：成本和噪音

这一段要接用户直觉：“这得烧多少 token？”

核心观点：

> 成熟的 Loop Engineer 不是让 AI 一直跑，而是设计什么时候不让 AI 跑。

成本来源：

- 触发太频繁。
- 每次读太多上下文。
- 强模型用在低价值判断上。
- 多 agent 互相验证但没有硬测试。
- 产出太多低价值文档和 PR。

控制方法：

- 规则 / 脚本 / 小模型先过滤。
- 只有重复出现的问题才生成 signal。
- 只有达到阈值才触发 coding loop。
- 每个 loop 有最大轮数和预算。
- 长日志只传摘要。
- 高风险动作必须人工确认。

### 8. Demo 展示

展示本地 mock demo：

1. 几个客服 ticket。
2. support loop 读取后生成 `signals/export-markdown.md`。
3. signal 累积到 3 次，生成 `tasks/implement-markdown-export.md`。
4. coding loop 读取任务。
5. verifier 检查。
6. support loop 生成用户通知草稿。

这段重点是让观众看到：

> Loop Engineer 不是玄学记忆，而是一套很朴素的文件系统和工作流。

### 9. 结尾

结尾判断：

> Loop Engineer 真正有价值的地方，不是让 agent 更像人，而是让业务流程更像系统。  
> 它能把客服、增长、SEO、工程这些原本断开的环节连起来。  
> 但它也有门槛：数据要稳定，权限要克制，验证要可靠，成本要算清楚。  
> 未来团队的竞争力，可能不只是会不会用 AI，而是能不能把业务拆成一组可观察、可触发、可验证、可复利的 loop。
