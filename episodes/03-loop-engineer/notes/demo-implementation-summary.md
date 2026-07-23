# Demo 实现总结：Parrot Loop Engineer

来源：

- `/Users/zj/Desktop/ai-parrot/parrot/技术方案2.2.1-Loop-Engineer反馈修Bug.md`
- `/Users/zj/Desktop/ai-parrot/parrot/技术方案2.2.2-Loop-Engineer自动化与可视化.md`

## 一句话总结

这个 demo 已经从“模拟用户反馈文件”升级成了一个真实的 Loop Engineer 系统：

> 前台用户反馈进入 SiteKit 后，后台通过 `loop-engineer/` 把反馈同步成工件，再由多个 agent loop 归类 signal、生成 task、人工批准、触发 coding、验证修复、生成回访草稿，并通过 Mission Console 可视化整个事件链。

## 当前实现的核心闭环

```text
SiteKit 用户反馈
  -> sync-feedback
  -> artifacts/feedback
  -> feedback loop
  -> artifacts/signals
  -> task loop
  -> tasks status=proposed
  -> 人工批准 approved
  -> coding loop
  -> Cursor Agent / Codex
  -> verifier loop
  -> verifications
  -> followup loop
  -> followups 草稿
  -> 人工合入 / 发信 / Admin 结案
```

## 关键实现判断

### 1. 每个 loop 都是 agent，但不是所有动作都全自动

方案明确写了：

> 每个 loop 是 AI agent，读 `domains/*/README.md`。

但系统不是全自动，而是保留多个人工闸门：

- task 从 `proposed` 到 `approved` 需要人工。
- coding 需要人工触发。
- 合入 main 需要人工。
- 发用户回访需要人工。
- Admin 标记 resolved 需要人工。
- 生产部署需要人工。

这正好能支撑视频里的一个重要观点：

> Loop Engineer 不是全自动，而是自动推进 + 人工闸门。

### 2. sync 不是 agent，而是确定性脚本

方案里很重要的一点：

> CLI 只做启动与门禁；sync 是唯一确定性 HTTP 同步脚本。

也就是说：

- `sync-feedback` 负责从 `GET /api/admin/feedback` 拉数据。
- 它不做智能判断。
- 它只把真实反馈同步成 `artifacts/feedback/*.md`。

这个设计很适合讲：

> 规则能做的交给代码，语义判断再交给 agent。

### 3. feedback / task / verifier / followup 用 DeepSeek

运行时分流：

- feedback loop：DeepSeek
- task loop：DeepSeek
- verifier loop：DeepSeek
- followup loop：DeepSeek
- coding loop：Cursor Agent CLI，也可以替换为 Codex

这说明 Loop Engineer 不绑定一个模型或工具。

它是一个调度系统：

```text
确定性同步：普通脚本
语义归类：DeepSeek
代码修复：Cursor / Codex
验证报告：DeepSeek + 测试命令
回访草稿：DeepSeek
```

### 4. coding loop 是最高风险环节

方案里对 coding 的边界非常清楚：

- 需要人工批准 task。
- 需要人工触发 coding。
- coding 走 `loop/*` 分支。
- 禁止自动合入 main。
- 禁止自动部署。

这比“AI 自动修 bug”更可信。

视频里可以这么讲：

> 真正落地时，coding loop 不是用户一反馈就开始改代码，而是 signal 先沉淀，task 先生成，人工批准后才进入 coding。AI 可以修，但不能替你合并和部署。

## 文件系统设计

可运行目录是工作区根：

```text
loop-engineer/
  artifacts/
    feedback/
    signals/
    tasks/
    verifications/
    followups/
  domains/
    feedback/README.md
    product/README.md
    coding/README.md
    verifier/README.md
    followup/README.md
  scripts/
  state/
  log.md
```

这个结构非常适合录屏展示：

- `artifacts/feedback`：原始用户反馈工件。
- `artifacts/signals`：重复问题 / 产品信号。
- `artifacts/tasks`：工程任务。
- `artifacts/verifications`：验证报告。
- `artifacts/followups`：用户回访草稿。
- `domains/*/README.md`：每个 loop 的 Loop Contract。
- `log.md`：全局可审计日志。

## CLI 命令

已有命令：

```bash
loop-engineer hello
loop-engineer sync
loop-engineer feedback
loop-engineer task
loop-engineer run-to-task
loop-engineer coding
loop-engineer verify
loop-engineer followup
```

这些命令很适合视频里做逐步演示：

```text
sync -> feedback -> task -> approve -> coding -> verify -> followup
```

也可以用 `run-to-task` 展示“一键跑到待批准 task”。

## 2.2.2 的升级：事件驱动和可视化

2.2.2 把 2.2.1 的手动 CLI 链路升级成：

```text
serve / Web / CLI
  -> publish event
  -> Redis events
  -> one loop one worker
  -> artifacts + log.md
  -> Mission Console
```

事件链：

```text
sync.requested
  -> sync.completed
  -> feedback.completed
  -> task.proposed
  -> task.approved
  -> coding.completed
  -> verify.passed
  -> followup.completed
```

这部分特别适合讲“Loop Engineer 怎么触发”：

- P0：人工 CLI 触发。
- P1：事件驱动触发。
- 后续：可选定时 sync、Webhook、告警触发。

## Mission Console 的内容价值

控制台不是普通后台列表，而是用来展示：

> 哪个 loop 被哪条事件唤起。

关键视图：

- Mission：workers + SYNC NOW + 事件流。
- Problems：Needs Approve / Fixed / In Flight。
- Contracts：展示 `domains/*/README`。
- Events：事件表。
- Gate：非 high task 的批准抽屉。

这很适合做视频视觉主体。

观众能看到 Loop Engineer 不只是命令行，而是一个可观察、可审计、可批准的控制台。

## 内容里最值得强调的点

### 1. Loop Engineer 不绑定 Claude Code

原视频偏 Claude Code + Skills。

这个 demo 是：

```text
TypeScript CLI
  + DeepSeek
  + Cursor Agent / Codex
  + Markdown artifacts
  + Redis event bus
  + Mission Console
```

说明 Loop Engineer 是架构思想，不是某个工具。

### 2. 自动化不是一步到位

2.2.1 是人工触发为主：

```text
sync / feedback / task / coding / verify / followup
```

2.2.2 才引入事件驱动：

```text
event -> worker -> next event
```

这可以作为视频里的成熟路径：

```text
先 CLI 手动跑通
再事件驱动串联
最后才考虑定时 / webhook / 高 severity 自动批准
```

### 3. 高风险节点必须有 Gate

方案里最清晰的边界：

- 不自动 merge。
- 不自动 deploy。
- 不自动发信。
- 不自动 Admin resolved。
- 不默认全量 auto approve。

这比单纯吹自动化更有可信度。

### 4. AI 和代码分工明确

这个 demo 可以直接证明：

> Loop Engineer 不是每一步都用 AI。确定性的事用脚本，语义判断用模型，代码修复用 coding agent，高风险决策交给人。

## 视频可用主线

建议长视频 demo 部分按这个顺序讲：

1. 展示前台反馈入口或 SiteKit feedback。
2. 展示 `loop-engineer sync`：真实反馈变成 `artifacts/feedback`。
3. 展示 `feedback loop`：DeepSeek 把反馈归成 signal。
4. 展示 `task loop`：signal 达阈值后生成 proposed task。
5. 展示人工 Gate：task 必须 approved。
6. 展示 `coding loop`：Cursor / Codex 开始修复，但不自动合并。
7. 展示 `verifier loop`：验证报告。
8. 展示 `followup loop`：生成用户回访草稿。
9. 展示 Mission Console：事件流和 worker 状态。
10. 总结：这就是“自动推进 + 人工闸门”的 Loop Engineer。

## 可以直接用于视频的表达

> 我做这个 demo 之后，最大的感受是：Loop Engineer 不是让 AI 完全接管系统，而是把用户反馈到产品修复这条链路拆成多个可触发、可观察、可审计的 loop。

> 每个 loop 都可以是 agent，但不是每一步都应该交给大模型。拉数据这种确定性动作，用脚本；归类反馈这种语义判断，用模型；修代码，用 Cursor 或 Codex；合并、部署、发信，留给人。

> 所以真正成熟的 Loop Engineer，不是全自动，而是自动推进加人工闸门。

## 后续文案需要更新的地方

- 原本 demo 文档里说“本地 mock tickets”，现在要改成“真实 SiteKit feedback + sync 工件化”。
- 原本 coding loop 只是模拟，现在可以讲 Cursor Agent / Codex 调起。
- 原本触发方式只讲 CLI，现在要加事件驱动 worker 和 Redis。
- 原本没有可视化，现在要加入 Mission Console。
- “怎么触发、谁处理、状态放哪、什么时候进入下一步、怎么验证、哪些不能自动做”这六个问题，可以用这个 demo 一一回答。
