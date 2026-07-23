# Coding Loop 实现方案

## 1. Coding Loop 是什么

在这个 demo 里，coding loop 不是“AI 自动上线代码”。

它的职责是：

> 读取已经成熟的工程任务，根据任务上下文生成修复方案，必要时修改代码，运行验证，并把结果写回 artifacts。

它位于整个闭环的中后段：

```text
feedback
  -> signal
  -> task
  -> coding loop
  -> verification
  -> followup
```

也就是说，coding loop 不直接读取所有用户反馈。它只处理已经被整理过、达到阈值、并生成明确验收标准的 task。

## 2. 为什么不能一上来全自动

真实环境里，coding loop 风险最高。

它可能：

- 改错代码。
- 修了一个问题，引入另一个问题。
- 理解错用户反馈。
- 没跑测试就以为完成。
- 生成一堆低价值 PR。
- 因为一个弱 signal 就开始乱改产品。

所以第一版 demo 不建议直接做“自动改代码 + 自动提交 PR”。

更稳的路线是三阶段：

| 阶段 | 能力 | 适合用途 |
|---|---|---|
| V1 演示版 | 不改代码，只生成修复计划、影响文件、验收清单、模拟 PR 摘要 | 视频 demo |
| V2 半自动版 | 生成 patch 或修改本地代码，但不提交、不部署 | 技术文章 / 掘金 |
| V3 真实版 | 独立 worktree 中修复、跑测试、生成 PR，等待人工 review | 真正业务落地 |

## 3. V1：演示版 Coding Loop

V1 目标：

让观众看懂 coding loop 怎么接收 task，并把产品问题转成工程执行计划。

### 输入

读取：

```text
artifacts/tasks/fix-export-markdown.md
artifacts/signals/export-markdown.md
domains/coding/README.md
log.md
```

### 输出

生成：

```text
artifacts/tasks/fix-export-markdown-plan.md
artifacts/verifications/fix-export-markdown-checklist.md
artifacts/followups/feedback-001.md
artifacts/followups/feedback-002.md
artifacts/followups/feedback-003.md
log.md
```

### 它做什么

1. 读取 task。
2. 读取 source signal，理解为什么要修。
3. 读取 coding loop contract，确认边界。
4. 生成修复计划。
5. 生成可能影响的文件列表。
6. 生成验收清单。
7. 生成模拟 PR 摘要。
8. 把结果写回 log。

### 它不做什么

- 不直接改代码。
- 不提交 Git。
- 不部署。
- 不通知用户。
- 不绕过人工确认。

### V1 脚本逻辑

`scripts/coding-loop-sim.js`

伪代码：

```js
const task = readMarkdown("artifacts/tasks/fix-export-markdown.md")
const signal = readMarkdown("artifacts/signals/export-markdown.md")
const contract = readMarkdown("domains/coding/README.md")

if (!task.includes("status: proposed")) {
  stop("No proposed task found")
}

const plan = buildPlan(task, signal, contract)
writeMarkdown("artifacts/tasks/fix-export-markdown-plan.md", plan)

const verification = buildVerificationChecklist(task)
writeMarkdown("artifacts/verifications/fix-export-markdown-checklist.md", verification)

const followups = buildFollowupDrafts(signal)
writeFollowupDrafts(followups)

appendLog("coding-loop", "Generated implementation plan, verification checklist, and followup drafts.")
```

这个版本可以完全不用 LLM，用模板生成。视频里可以强调：

> 第一版 demo 不追求 AI 真写代码，而是先展示 loop 的状态流转。真实场景里，coding loop 可以换成 Claude Code、Codex 或 CI agent。

## 4. V2：半自动 Coding Loop

V2 可以让 agent 真正修改本地代码，但仍然不提交、不部署。

### 输入

除了 V1 的输入，还需要：

```text
AGENTS.md
package.json
src/
tests/
```

### 工作流程

1. 读取 task 和 acceptance criteria。
2. 搜索相关代码。
3. 先写一个失败测试，复现问题。
4. 修改代码。
5. 跑测试。
6. 生成 diff summary。
7. 写 verification report。
8. 等人工 review。

### 输出

```text
artifacts/coding-runs/run-001.md
artifacts/verifications/fix-export-markdown-report.md
```

### 半自动版的关键要求

- 必须先读 `AGENTS.md`。
- 必须记录改了哪些文件。
- 必须运行测试。
- 测试失败时不能标记完成。
- 不能自动 commit。
- 不能自动部署。

## 5. V3：真实 Coding Loop

V3 才接近真正的 Loop Engineer。

### 推荐架构

```text
task-loop
  -> create task
  -> human approval
  -> create worktree
  -> spawn coding agent
  -> coding agent modifies code
  -> run tests
  -> spawn verifier agent
  -> create PR
  -> human review
```

### 真实版必须有的护栏

#### 1. Worktree 隔离

每个 coding loop 都在独立 worktree 或分支里工作。

避免多个 agent 同时改同一个目录。

#### 2. 权限分级

coding loop 可以：

- 读 task。
- 读代码。
- 修改本地文件。
- 跑测试。
- 生成 PR 草稿。

coding loop 不可以：

- 直接部署生产。
- 删除数据库。
- 自动给用户发邮件。
- 修改账单、权限、支付相关逻辑，除非人工批准。

#### 3. 测试优先

每个 task 都必须有 acceptance criteria。

coding loop 的完成条件不是“我觉得改好了”，而是：

- 相关测试通过。
- 验收标准满足。
- verifier loop 通过。
- 人工 review 通过。

#### 4. Verifier 独立

不要让同一个 agent 完全自我验证。

coding agent 完成后，应该由 verifier loop 读取 task 和 diff，做只读检查。

#### 5. 成本限制

必须设置：

- 最大轮数。
- 最大运行时间。
- 最大 token 预算。
- 连续失败停止。
- 同一 task 不重复触发。

## 6. Demo 第一版建议怎么做

建议第一版这样实现：

### Step 1：用本地 Web 项目制造一个真实小 bug

例如项目里有一个导出按钮，但没有 Markdown 导出能力。

用户反馈：

> 我想导出 Markdown，但现在只能复制内容。

### Step 2：feedback loop 生成 signal

`signals/export-markdown.md`

### Step 3：task loop 生成 task

`tasks/fix-export-markdown.md`

### Step 4：coding loop sim 生成修复计划

`tasks/fix-export-markdown-plan.md`

内容包括：

```markdown
## Implementation Plan

1. Locate export menu component.
2. Add Markdown option.
3. Implement markdown serializer.
4. Add a basic export test.
5. Verify PDF export still works.

## Likely Files

- src/components/export-menu.tsx
- src/lib/export/markdown.ts
- tests/export-markdown.test.ts

## PR Summary

Adds Markdown export option based on repeated user feedback.
```

### Step 5：视频里再展示“如果是真实版”

可以在旁白里说：

> 到这里，第一版 demo 只是生成了修复计划。真实业务里，下一步可以把这个 task 交给 Claude Code 或 Codex，让它在独立 worktree 中实现，然后由 verifier loop 检查，最后人工 review。

这样最稳。

## 7. 后续如果要真改代码

如果你想让 demo 更有冲击力，可以在 V2 做一个真实修复。

前提是小项目足够简单。

推荐做法：

1. 人工确认 task。
2. 让 Codex 读取 task。
3. Codex 修改本地代码。
4. Codex 跑测试。
5. verifier loop 生成报告。
6. 人工展示 diff。

不要第一版就自动 commit 或自动 PR。

## 8. 一句话总结

Coding loop 的正确实现方式不是“用户一反馈，AI 马上改代码”。

更合理的是：

> 用户反馈先沉淀成 signal，signal 达到阈值后生成 task，task 有明确验收标准后，coding loop 才能在受控环境里修复，并由 verifier loop 和人工 review 兜底。

