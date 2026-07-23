# Demo 设计：Support Signal Loop

## Demo 目标

做一个轻量、可讲清楚的实际例子，展示 Loop Engineer 如何把用户反馈变成产品/工程任务。

不追求接真实客服系统，不追求完整实现产品功能。重点是展示 loop 的结构：

> tickets -> support loop -> signals -> tasks -> coding loop -> verifier -> user follow-up

## 观众应该看懂什么

1. agent 不只是回复用户，而是在提炼重复问题。
2. `signals/` 是共享状态，不是聊天记忆。
3. signal 累积后可以触发 product/coding loop。
4. loop 必须有阈值、日志、停止条件和验证。
5. 真正的价值是跨部门闭环，而不是某个单点自动化。

## 文件结构

```text
demo/
  input/
    tickets/
      ticket-001.md
      ticket-002.md
      ticket-003.md
      ticket-004.md
  artifacts/
    tickets/
    signals/
    tasks/
    followups/
  domains/
    support/
      README.md
    product/
      README.md
    coding/
      README.md
  scripts/
    support-loop.js
    product-loop.js
    coding-loop-sim.js
  log.md
```

## Mock Tickets

准备 4 条客服反馈：

1. 用户 A：想把项目导出成 Markdown，但找不到入口。
2. 用户 B：客户要求交付 Markdown 文件，目前只能复制内容。
3. 用户 C：导出 PDF 正常，但希望也支持 Markdown。
4. 用户 D：无关问题，比如账单扣费疑问。

前三条应该被归为同一个 signal：`export-markdown`。

第四条应该进入 ticket artifact，但不触发产品任务。

## Signal Schema

`artifacts/signals/export-markdown.md`

```markdown
---
id: signal-export-markdown
title: Support Markdown export
type: feature_request
status: active
severity: medium
occurrences: 3
sources:
  - ticket-001
  - ticket-002
  - ticket-003
created_at: 2026-07-09
updated_at: 2026-07-09
---

## Summary

Multiple users want a way to export project content as Markdown.

## Evidence

- ticket-001: User could not find a Markdown export option.
- ticket-002: User needs Markdown as a client deliverable.
- ticket-003: User can export PDF but wants Markdown too.

## Suggested Next Step

Create a product/engineering task to add Markdown export or expose an existing hidden export path.

## Timeline

- 2026-07-09: Created from support loop after 3 related tickets.
```

## Task Schema

`artifacts/tasks/implement-markdown-export.md`

```markdown
---
id: task-implement-markdown-export
title: Add Markdown export option
status: proposed
source_signal: signal-export-markdown
owner_loop: coding
priority: medium
---

## Goal

Add or expose a Markdown export option so users can export project content as `.md`.

## Acceptance Criteria

- Users can export project content as Markdown.
- Export option is visible in the export menu.
- Markdown output preserves headings and basic structure.
- Add or update tests for the export path.

## Context

Generated from repeated support tickets asking for Markdown export.
```

## Loop Contracts

### Support Loop

职责：

- 读取新 ticket。
- 判断是否可回复。
- 抽取用户卡点。
- 创建或更新 signal。
- 记录处理日志。
- 对已解决问题生成 follow-up 草稿。

边界：

- 不直接改代码。
- 不直接发送高风险用户通知。
- 不访问真实支付或生产数据库。

### Product Loop

职责：

- 读取 active signals。
- 根据出现次数、影响范围、业务价值排序。
- 达到阈值后创建 task。

边界：

- 不直接实现功能。
- 不绕过人工优先级策略。

### Coding Loop

Demo 中只模拟，不真实改产品代码。

职责：

- 读取 task。
- 生成实现计划。
- 输出“模拟 PR 摘要”。
- 触发 verifier 检查 acceptance criteria。

边界：

- 不连接真实 GitHub。
- 不执行真实部署。

## 视频展示方式

### 镜头 1：展示输入

打开 `demo/input/tickets/`，展示 4 条 ticket。

讲解：

> 这就是很多团队每天都会遇到的情况：用户反馈散在客服系统里，没人持续归类。

### 镜头 2：运行 support loop

展示命令：

```bash
node scripts/support-loop.js
```

输出：

- 处理 4 条 ticket。
- 识别 3 条 Markdown export 相关反馈。
- 创建 `signal-export-markdown`。
- 写入 `log.md`。

### 镜头 3：展示 signal

打开 `artifacts/signals/export-markdown.md`。

讲解：

> 这不是长期记忆的玄学，而是一份结构化证据。以后任何 loop 都能读。

### 镜头 4：运行 product loop

```bash
node scripts/product-loop.js
```

输出：

- signal occurrences >= 3。
- 创建 engineering task。

### 镜头 5：展示 task

打开 `artifacts/tasks/implement-markdown-export.md`。

讲解：

> 现在，客服反馈已经变成了工程可执行任务，而且带着来源证据和验收标准。

### 镜头 6：模拟 coding loop

```bash
node scripts/coding-loop-sim.js
```

输出：

- 生成实现计划。
- 生成模拟 PR 摘要。
- 生成 follow-up 草稿。

### 镜头 7：总结

展示最终文件：

- signal
- task
- follow-up
- log

讲解：

> 这就是 Loop Engineer 的关键：不是让 AI 一直聊天，而是让不同 loop 围绕同一套状态接力。

## 风险提示

视频里要主动讲清楚：

- 真实环境不能让 agent 随便回复用户。
- 不能让 agent 无限制访问 Stripe、数据库、生产日志。
- coding loop 必须有测试和人工 review。
- 触发 coding loop 前最好有阈值，避免一个用户一抱怨就开始改产品。
- 大模型只处理高价值判断，低价值分类可以交给规则、小模型或脚本。

## 第一阶段实施计划

先做一个无 API、无 token 成本的本地版本。

### Step 1：创建输入样例

创建 `input/tickets/`，准备 4 条 Markdown 客服工单：

- 3 条都提到 Markdown 导出或文件导出。
- 1 条是无关账单问题，用来证明 loop 不会把所有问题都合并到一个 signal。

### Step 2：创建 loop contract

创建三个 README：

- `domains/support/README.md`
- `domains/product/README.md`
- `domains/coding/README.md`

它们不需要长，但要写清楚目标、输入、输出、边界和停止条件。

### Step 3：写 support loop

`scripts/support-loop.js` 做三件事：

1. 读取 `input/tickets/*.md`。
2. 用简单关键词规则识别 Markdown export 相关 ticket。
3. 生成：
   - `artifacts/tickets/*.md`
   - `artifacts/signals/export-markdown.md`
   - `log.md`

第一版先不用 LLM，避免 demo 一开始就变复杂。

### Step 4：写 product loop

`scripts/product-loop.js` 做两件事：

1. 读取 `artifacts/signals/export-markdown.md`。
2. 如果 `occurrences >= 3`，生成 `artifacts/tasks/implement-markdown-export.md`。

这里要突出阈值逻辑：不是一个用户一提，就立刻触发工程任务。

### Step 5：写 coding loop 模拟

`scripts/coding-loop-sim.js` 不真实改代码，只生成：

- `artifacts/tasks/implement-markdown-export-plan.md`
- `artifacts/followups/ticket-001.md`
- `artifacts/followups/ticket-002.md`
- `artifacts/followups/ticket-003.md`

它模拟 coding loop 已经完成实现，并生成 support loop 可以回访用户的草稿。

### Step 6：写一键运行脚本

可以加一个：

```bash
node scripts/support-loop.js
node scripts/product-loop.js
node scripts/coding-loop-sim.js
```

或者后续再封装成：

```bash
npm run demo
```

### Step 7：录屏素材点

最终录屏重点不是代码，而是文件系统变化：

1. 跑之前：只有 4 条 tickets。
2. 跑 support loop 后：出现 signal。
3. 跑 product loop 后：出现 task。
4. 跑 coding loop 后：出现 plan 和 followups。
5. 打开 `log.md`，展示每个 loop 都留下了可追踪记录。
