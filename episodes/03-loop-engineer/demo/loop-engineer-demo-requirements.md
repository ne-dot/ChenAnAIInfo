# Loop Engineer Demo 需求文档

## 1. 项目目标

在一个小型 Web 项目里演示 Loop Engineer 的真实工作方式：

> 前台用户提交意见反馈后，后台通过 agent loop 自动收集、归类、沉淀 signal，并在满足条件时生成修复任务，最终辅助开发者修复问题、验证结果、生成用户回访内容。

这个 demo 的重点不是展示“AI 自动改完所有代码”，而是展示一个更可信的闭环：

```text
用户反馈
  -> feedback loop 收集和归类
  -> signals 沉淀重复问题
  -> task loop 生成修复任务
  -> coding loop 辅助修复
  -> verifier loop 验证
  -> followup loop 生成用户回访草稿
```

## 2. Demo 要证明什么

这个 demo 要让观众看懂四件事：

1. Loop Engineer 不是单次 prompt，而是一套持续运行的业务闭环。
2. 用户反馈不会停在后台列表里，而是会被整理成可追踪的 `signals`。
3. 当同类反馈重复出现，系统可以自动生成工程任务。
4. 修复不是无脑自动上线，而是要经过测试、验证和人工确认。

## 3. 角色定义

### 前台用户

用户在 Web 页面里提交反馈，例如：

- “导出按钮点了没反应。”
- “我想把内容导出成 Markdown。”
- “移动端页面里的反馈按钮挡住了内容。”
- “登录后刷新页面会退出。”

### 产品/运营人员

查看后台整理出的 signals 和 tasks，决定哪些可以进入修复。

### 开发者

查看 Loop Engineer 生成的任务说明、复现步骤和验收标准，决定是否让 coding agent 处理。

### Loop Engineer 系统

负责定时或事件触发地处理反馈、归类问题、生成任务、辅助修复和记录状态。

## 4. 核心功能范围

### 4.1 前台反馈入口

前台需要一个简单的反馈入口。

用户可以提交：

- 反馈类型：bug / feature request / usability issue / other
- 反馈内容
- 当前页面路径
- 浏览器信息
- 用户邮箱，可选
- 截图，可选，第一版可以不做

提交后，反馈进入后台存储。

第一版可以用本地 JSON / SQLite / Markdown 文件存储，不一定需要接真实数据库。

### 4.2 Feedback Inbox

后台需要有一个原始反馈池，类似：

```text
feedback/
  feedback-001.md
  feedback-002.md
  feedback-003.md
```

每条反馈包含：

```markdown
---
id: feedback-001
type: bug
status: new
source: web_form
page: /export
user_email: user@example.com
created_at: 2026-07-09T10:00:00+08:00
---

## Content

导出按钮点了没反应，我想导出 Markdown 文件。
```

### 4.3 Feedback Loop

Feedback Loop 是第一个 loop。

触发方式：

- Demo 第一版：手动运行脚本。
- 真实版本：定时任务，例如每 30 分钟运行一次；或者新反馈提交后触发 webhook。

它要做的事情：

1. 读取新增反馈。
2. 判断反馈类型：bug、功能需求、使用卡点、无关反馈。
3. 抽取关键词和问题主题。
4. 判断是否和已有 signal 相关。
5. 如果相关，追加到已有 signal。
6. 如果不相关，创建新 signal。
7. 记录本次处理日志。

第一版可以先用规则和关键词完成，不强依赖 LLM。

示例：

用户多次提到：

- “导出 Markdown”
- “导出按钮没反应”
- “想导出 md 文件”

系统生成或更新：

```text
artifacts/signals/export-markdown.md
```

### 4.4 Signals

Signal 是 Loop Engineer 的共享状态核心。

每个 signal 代表一个被反复观察到的问题、需求或机会。

Signal 文件结构：

```markdown
---
id: signal-export-markdown
title: Markdown export problem
type: feature_request
status: active
severity: medium
occurrences: 3
sources:
  - feedback-001
  - feedback-002
  - feedback-003
created_at: 2026-07-09T10:10:00+08:00
updated_at: 2026-07-09T10:30:00+08:00
---

## Summary

多个用户反馈希望支持 Markdown 导出，或者反馈当前导出入口不可用。

## Evidence

- feedback-001：用户希望导出 Markdown。
- feedback-002：用户表示导出按钮没有反应。
- feedback-003：用户需要交付 md 文件给客户。

## Impact

影响需要把内容交付给客户、迁移到其他工具或归档项目的用户。

## Suggested Next Step

检查当前导出功能，确认是否已有 Markdown 导出能力。如果没有，创建工程任务；如果已有，修复入口或文案。

## Timeline

- 2026-07-09 10:10：首次创建。
- 2026-07-09 10:30：追加 feedback-003，occurrences 增加到 3。
```

### 4.5 Task Loop

Task Loop 负责把成熟的 signal 变成工程任务。

触发条件示例：

- `occurrences >= 3`
- 或 `severity = high`
- 或人工把 signal 标记为 `ready_for_task`

它要做的事情：

1. 读取 active signals。
2. 判断是否达到任务生成阈值。
3. 生成工程任务。
4. 写入 `artifacts/tasks/`。
5. 更新 signal 状态，例如 `task_created`。

任务文件示例：

```markdown
---
id: task-fix-export-markdown
title: Fix or add Markdown export
status: proposed
source_signal: signal-export-markdown
priority: medium
owner_loop: coding
created_at: 2026-07-09T10:40:00+08:00
---

## Problem

多个用户反馈希望导出 Markdown，或反馈导出入口不可用。

## Evidence

来自 signal-export-markdown，当前累计 3 条相关反馈。

## Reproduction

1. 打开项目页面。
2. 点击导出按钮。
3. 查看是否存在 Markdown 导出选项。
4. 如果存在，确认点击后是否能生成 `.md` 文件。

## Acceptance Criteria

- 用户能看到 Markdown 导出入口。
- 点击后可以生成 `.md` 文件。
- 导出内容保留标题、段落和列表结构。
- 增加或更新对应测试。
- 不影响现有 PDF / HTML 导出。

## Human Approval

第一版 demo 中，该任务需要人工确认后才进入 coding loop。
```

### 4.6 Coding Loop

Coding Loop 负责根据 task 辅助修复问题。

Demo 第一版可以分两种模式：

#### 模式 A：模拟 coding loop

不真的改代码，只生成：

- 修复计划
- 可能影响文件
- 测试建议
- 模拟 PR 摘要

适合第一版内容展示，成本低、风险小。

#### 模式 B：真实 coding loop

如果小项目足够简单，可以让 coding agent 实际修改代码。

要求：

- 必须在独立分支或 worktree 中运行。
- 必须先写或更新测试。
- 必须运行测试。
- 必须生成变更摘要。
- 必须等待人工 review，不能自动部署。

### 4.7 Verifier Loop

Verifier Loop 负责检查 coding loop 的结果。

它要做的事情：

1. 读取 task 的验收标准。
2. 检查代码 diff 或模拟 PR。
3. 运行测试。
4. 如果是前端问题，运行浏览器检查或截图。
5. 输出验证报告。

验证报告示例：

```markdown
---
id: verify-task-fix-export-markdown
task: task-fix-export-markdown
status: passed
created_at: 2026-07-09T11:20:00+08:00
---

## Checks

- Markdown export button exists: passed
- `.md` file can be generated: passed
- Existing PDF export still works: passed
- Tests passed: passed

## Notes

建议人工检查一次真实导出内容格式。
```

### 4.8 Followup Loop

Followup Loop 负责在问题修复后，生成用户回访草稿。

它要做的事情：

1. 找到 signal 关联的原始 feedback。
2. 找到留下邮箱的用户。
3. 根据修复结果生成回复草稿。
4. 写入 `artifacts/followups/`。
5. 不自动发送，第一版必须人工确认。

回访草稿示例：

```markdown
---
feedback_id: feedback-001
signal: signal-export-markdown
status: draft
recipient: user@example.com
---

你好，我们已经根据你之前反馈的导出问题，新增了 Markdown 导出入口。

现在你可以在项目页面点击“导出”，选择 Markdown 格式，下载 `.md` 文件。

感谢你的反馈，它帮助我们改进了这个功能。
```

## 5. 文件结构建议

```text
demo-app/
  app/
    feedback-form/
    admin/
  loop-engineer/
    artifacts/
      feedback/
      signals/
      tasks/
      verifications/
      followups/
    domains/
      feedback/
        README.md
      product/
        README.md
      coding/
        README.md
      verifier/
        README.md
      followup/
        README.md
    scripts/
      feedback-loop.js
      task-loop.js
      coding-loop-sim.js
      verifier-loop.js
      followup-loop.js
    log.md
```

## 6. Loop Contract 要求

每个 loop 都要有 README，写清楚：

- 目标
- 输入
- 输出
- 工作步骤
- 能做什么
- 不能做什么
- 停止条件
- 失败时怎么记录

例如 feedback loop 的边界：

- 可以读取用户反馈。
- 可以创建和更新 signals。
- 不可以修改代码。
- 不可以直接回复用户。
- 不可以删除原始反馈。

## 7. 权限和风险控制

这个 demo 必须主动展示边界感。

### 必须限制

- 不自动部署。
- 不自动发送用户邮件。
- 不直接访问生产数据库。
- 不把用户隐私信息发送给不必要的模型。
- 不因为一条反馈就触发 coding loop。

### 必须保留

- 人工确认任务是否值得做。
- 人工 review coding loop 的结果。
- verifier loop 的验证报告。
- 全局 `log.md` 记录每一步。

## 8. 第一版 MVP 范围

第一版只做最小闭环。

必须有：

- 前台反馈表单，或用本地 mock feedback 文件模拟。
- feedback loop：生成 signal。
- task loop：signal 达到阈值后生成 task。
- coding loop sim：生成修复计划，不一定真改代码。
- verifier loop sim：生成验证报告。
- followup loop：生成用户回访草稿。
- `log.md`：记录每个 loop 做了什么。

可以暂时不做：

- 真实客服系统接入。
- 真实邮件发送。
- 真实 GitHub PR。
- 真实自动部署。
- 多模型调度。
- 复杂后台 UI。

## 9. Demo 验收标准

Demo 跑完后，应该能展示：

1. 用户提交了几条反馈。
2. 系统自动把相似反馈合并成一个 signal。
3. signal 累积到阈值后自动生成 task。
4. task 有清楚的问题描述、证据、复现步骤和验收标准。
5. coding loop 生成修复计划。
6. verifier loop 生成验证报告。
7. followup loop 生成用户回访草稿。
8. `log.md` 能串起整个过程。

## 10. 视频展示脚本思路

演示时可以按这个顺序：

1. 先展示一个普通小项目，用户可以提交反馈。
2. 连续提交三条和“导出 Markdown”相关的反馈。
3. 运行 feedback loop，展示 `signals/export-markdown.md` 被创建。
4. 运行 task loop，展示 `tasks/fix-export-markdown.md` 被创建。
5. 运行 coding loop，展示修复计划或真实代码改动。
6. 运行 verifier loop，展示验证报告。
7. 运行 followup loop，展示给用户的回复草稿。
8. 总结：这就是 Loop Engineer 和普通 AI 客服的区别。

核心旁白：

> AI 客服只是在回答用户。Loop Engineer 是把用户反馈变成产品和工程系统的一部分。

