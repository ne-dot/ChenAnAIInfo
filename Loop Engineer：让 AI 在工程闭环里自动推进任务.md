# Loop Engineer：让 AI 在工程闭环里自动推进任务

![Loop Engineer 封面](https://weizhenan2.tos-cn-guangzhou.volces.com/call_Z0sYgJy0BrMubLEC5ivPDDV5.jpg)

假设现在是半夜三点。

你正在睡觉，线上突然出现一个阻塞性 Bug。用户无法继续使用核心功能，客服开始反馈，监控报警也响了。过去这种情况很简单：工程师被叫醒，打开电脑，看日志，复现问题，定位代码，修改，测试，发版。

真正消耗人的，往往不是最后改的那几行代码，而是整个排查和验证过程。

最近做了一个 demo，就是模拟这个场景：线上出现阻塞性 Bug 后，不是立刻把工程师从床上叫起来，而是先让一个 AI 工程代理进入工作流。

它会读取错误信息，查看日志，找到相关代码，提出修复方案，修改代码，运行测试。如果测试失败，它会继续看失败原因，再改，再跑。直到问题被修掉，或者它明确判断当前信息不足，需要人介入。

这个过程背后，其实就是一个很火的新概念：

**Loop Engineer。**

它不是单纯的 Prompt Engineer，也不是普通的 AI Coding Assistant。它更像是一种新的工程协作方式：把 AI 放进一个可执行、可验证、可持续迭代的工作循环里。

## 什么是 Loop Engineer

Loop Engineer 的核心，不是让 AI 一次性回答一个问题，而是让 AI 在一个循环里持续推进任务。

一个典型的 loop 大概长这样：

```text
观察当前状态
读取上下文
提出下一步动作
执行动作
拿到反馈
根据反馈继续调整
产出可验证结果
```

以前我们用 AI 写代码，更多是「问一句，答一句」。

比如让 AI 帮你解释报错，帮你生成函数，帮你写一个组件。AI 给出答案以后，真正的验证和修正还是人来做。

Loop Engineer 的重点在后半段。

AI 不只是给建议，而是进入真实工程环境里。它可以读文件、改代码、跑命令、看日志、跑测试、提交结果。它不是一次性输出，而是在反馈里不断前进。

这也是「loop」这个词最关键的地方。

软件工程本来就不是一次写对。工程师平时做的事情，本质上就是循环：看现象，猜原因，改一点，跑一下，再看结果。AI 要真正参与工程，也必须进入这样的循环。

## Loop Engineer 的核心结构

一个可用的 Loop Engineer，通常由几部分组成：

![Loop Engineer 核心结构](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-core-structure.png)

这张图里，最关键的是 **Loop Contract 的位置**。

它不是流程中的一个普通步骤，而是整个 loop 的约束层。它规定 AI 要做什么、能读什么、能改什么、怎么验证、什么时候停、最后交付什么。

下面拆开看每一部分。

## Trigger：触发器

Loop 不能凭空开始，它需要一个启动信号。

这个启动信号可以是定时任务，也可以是 webhook，也可以是后台常驻进程。

比如：

```text
每 30 分钟检查一次客服工单
每天早上 9 点分析 SEO 数据
监控系统发现线上异常后自动触发
GitHub issue 被打上 bug 标签后启动修复流程
用户反馈集中出现某个问题时生成任务
```

Trigger 决定了 loop 什么时候开始。

在我的 demo 里，触发器就是线上 Bug。系统收到错误日志和用户反馈后，自动启动一次修复 loop。

## Context：上下文

AI 要做工程任务，必须能读取上下文。

上下文包括很多东西：

```text
代码
日志
文档
历史 issue
用户反馈
监控数据
测试结果
最近提交记录
```

没有上下文的 AI 只能猜。有上下文的 AI 才能定位问题。

比如线上 Bug 场景里，AI 至少需要看到：

```text
错误日志
用户反馈
相关接口
相关代码路径
最近发布记录
已有测试用例
```

这些信息决定了 AI 能不能从「看起来像错误」走到「找到真正原因」。

## Tools：工具能力

Loop Engineer 必须能执行动作。

只会分析的 AI，更像顾问。能调用工具的 AI，才有机会变成工程代理。

常见工具包括：

```text
搜索代码
读取文件
修改文件
运行测试
启动服务
查看 git diff
创建分支
生成 PR
读取监控
处理工单
调用内部接口
```

工具不是越多越好，关键是和任务匹配，并且权限边界清楚。

比如修线上 Bug 的 loop，可以允许 AI 读取日志、修改相关模块、运行测试、生成 PR，但不一定允许它直接部署生产。

这样既能让 AI 自动推进，又不会让它越过关键边界。

## Verify：验证机制

没有验证，就没有 loop。

验证决定 AI 的动作是不是有效。它可以是单元测试、集成测试、类型检查、lint，也可以是一个业务检查脚本。

比如：

```text
修 Bug 后，对应测试必须通过
改接口后，关键请求必须返回正确字段
改页面后，截图不能出现空白和错位
改数据处理逻辑后，样例输入输出必须一致
生成 PR 后，必须包含原因、修改内容和风险说明
```

Verify 是 loop 的反馈来源。

AI 每次执行完动作，都要通过验证拿到结果。通过了，进入总结和交付；失败了，读取失败原因，继续下一轮分析和修正。

## 文件结构：AI 的工作台

Loop Engineer 要稳定运行，不能只靠一段 prompt。

Prompt 更像口头交代，适合一次性任务。Loop 要反复执行，就需要一个稳定的文件结构。

一个比较清晰的结构是这样：

```text
loop-task/
├── artifacts/
│   ├── docs/
│   ├── signals/
│   ├── tasks/
│   ├── contents/
│   └── ...
├── loop-contract.md
└── LOGS.md
```

对应成结构图：

![Loop Engineer 文件结构](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-file-structure.png)

这套结构可以简单理解成三句话：

```text
artifacts/ 是资料区
loop-contract.md 是任务合同
LOGS.md 是运行记录
```

### artifacts：资料区

`artifacts/` 放所有任务材料和中间产物。

它下面可以继续拆：

```text
artifacts/
├── docs/
├── signals/
├── tasks/
├── contents/
└── ...
```

`docs/` 放背景资料，比如产品文档、接口说明、业务规则、历史决策。

`signals/` 放外部信号，比如用户反馈、客服工单、监控报警、数据异常、增长机会。

`tasks/` 放拆出来的任务，比如需要修复的 Bug、需要验证的假设、需要生成的实验。

`contents/` 放产出内容，比如文章草稿、页面文案、PR 描述、分析报告。

如果是半夜修 Bug 的场景，`signals/` 里面可以放线上报错和用户反馈，`docs/` 里面放相关接口说明，`tasks/` 里面放这次修复任务，`contents/` 里面放最后的修复摘要和 PR 描述。

这相当于给 AI 一个文件化的上下文仓库。它每一轮都可以读取这些材料，而不是依赖聊天窗口里模糊的记忆。

### loop-contract.md：任务合同

`loop-contract.md` 是整个 loop 的核心。

它不是资料，也不是日志，而是规则。

可以把它理解成一份任务合同。合同里写清楚：

```text
Goal：这次 loop 要完成什么
Inputs：AI 可以读取哪些信息
Workflow：按什么流程推进
Task：当前具体任务是什么
Timeline：执行频率和时间节奏
Permissions：允许做什么，不允许做什么
Verification：怎样判断完成
Stop Conditions：什么时候必须停下来
Output：最终交付什么
```

对应成结构图：

![Loop Contract 结构](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-contract-structure.png)

`Goal` 定义方向。比如修复线上阻塞性 Bug，或者每天发现一个产品增长机会。

`Workflow` 定义流程。比如读取信号、分析原因、生成任务、执行修改、验证结果、记录日志。

`Task` 定义当前这一轮要做的具体事情。Goal 是大方向，Task 是当前动作。

`Timeline` 定义节奏。比如每 30 分钟检查一次工单，每天早上 9 点跑一次 SEO 分析，或者监控报警后立即启动。

`Permissions` 定义权限。比如只能改指定目录，不能直接部署生产，不能读取敏感密钥。

`Verification` 定义完成标准。比如测试通过、截图通过、指标达标。

`Stop Conditions` 定义停止条件。比如连续失败、权限不足、修改范围越界时停止。

Loop Contract 的价值，是让 AI 的自动化有边界。

它不是“你自己看着办”，而是“在这份合同内循环推进”。

### LOGS.md：运行日志

`LOGS.md` 是整个 loop 的运行记录。

每一轮 AI 做了什么、看到了什么、判断了什么、失败在哪里、下一步准备做什么，都应该写进去。

一个简单的 `LOGS.md` 可以长这样：

```md
# LOGS

## 2026-07-10 03:12

Trigger:
- 线上支付接口出现大量 500 错误

Observation:
- 错误集中在 `/api/pay/confirm`
- 日志显示 `user_coupon` 字段为空

Action:
- 搜索支付确认逻辑
- 找到 `confirmPayment` 中对 `user_coupon.id` 的直接访问

Result:
- 本地复现成功

Next:
- 增加空值兼容
- 补充回归测试
```

下一轮继续追加：

```md
## 2026-07-10 03:25

Action:
- 修改空值处理逻辑
- 新增 coupon 为空时的回归测试

Result:
- 单元测试通过
- 类型检查失败

Next:
- 修复类型定义
```

这个文件很关键。

因为 loop 最怕黑箱运行。`LOGS.md` 让每一次执行都可追踪、可复盘、可接手。

工程师早上起来，不需要猜 AI 半夜到底干了什么，直接看 `LOGS.md` 就能知道整个过程。

## 一次 Loop 是怎么运行的

Loop Engineer 的运行过程，可以画成这样：

![一次 Loop 的运行流程](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-runtime-flow.png)

这里最重要的是中间这段：

```text
分析
执行
验证
反馈
再分析
```

AI 不是一次性给出答案，而是在验证结果里继续调整。

这就是 Loop Engineer 和普通 AI 编程最大的区别。

普通 AI 编程重心在生成。  
Loop Engineer 的重心在闭环。

## 半夜修 Bug 的完整例子

回到开头那个 demo。

这里有一个很重要的点：这个 demo 不是一个 loop 从头跑到尾，而是多个 loop 合作完成一件事。

一个真实的线上问题，通常不会直接变成“请 AI 修 Bug”。它会先以用户反馈、客服工单、后台异常、监控报警的形式出现。系统需要先把这些信息同步下来，再归类，再判断是否达到处理阈值，再生成任务。任务被人工批准以后，才进入 coding 阶段。

所以这套机制更像一条多 loop 协作流水线：

```text
sync -> feedback -> task -> coding -> verify -> followup
```

每个 loop 只负责一段清晰的职责。

```text
sync
从 Admin API 同步 bug 反馈，写入 artifacts/feedback

feedback
使用 DeepSeek 对 pending 反馈做归类，提炼成 signals

task
使用 DeepSeek 判断信号是否达阈值，生成 status=proposed 的 task

coding
使用 Cursor 执行修复，但必须等 task 被人工 approved

verify
使用 DeepSeek 对照 Acceptance Criteria 写验证报告

followup
使用 DeepSeek 生成用户回访草稿，但永不自动发信

serve
提供 Control Plane API，只读展示状态，并支持手动 SYNC 和批准

worker
一 loop 一 worker，通过 --loop sync|feedback|task|coding|verify|followup 调度
```

对应成流程图，大概是这样：

![多 Loop 协作修 Bug 流程](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-multi-loop-bug-flow.png)

这张图里有两个门禁非常关键。

第一个门禁在 `coding` 前面：

```text
task.status === approved
```

只有任务被人工批准以后，Cursor 才能进入修复。也就是说，AI 可以帮你发现问题、整理信号、提出任务，但不能直接因为发现一个反馈就开始改代码。

第二个门禁在 `followup` 后面：

```text
只生成草稿，永不自动发信
```

AI 可以根据修复结果生成用户回访文案，但发送动作仍然交给人。这个边界很重要，因为用户沟通不只是技术动作，也包含语气、责任和商业判断。

如果把它画成系统结构，会更清楚：

![多 Loop 系统结构](https://weizhenan2.tos-cn-guangzhou.volces.com/loop-engineer-multi-loop-system.png)

这也是为什么前面说，Loop Engineer 不只是“让 AI 自动修 Bug”。更准确的说法是：

**把一个复杂工作拆成多个有边界的 loop，让它们通过文件、状态和人工门禁协作。**

在这个 demo 里，`sync` 负责拿到事实，`feedback` 负责整理信号，`task` 负责提出任务，`coding` 负责修复，`verify` 负责验证，`followup` 负责生成沟通草稿，`serve` 负责给人一个控制面板，`worker` 负责让每个 loop 独立运行。

这样做的好处是边界非常清楚。

DeepSeek 更适合做归类、判断、总结和报告。Cursor 更适合进入代码仓库执行修复。人工负责批准任务和对外沟通。每个角色只做自己擅长、也被允许做的事情。

这时工程师早上醒来以后，看到的不是一个黑箱 AI 已经偷偷改完了线上系统，而是一条完整的处理链路：

```text
哪些反馈被同步
哪些反馈被归类成信号
哪些信号达到了任务阈值
哪个 task 被批准
Cursor 改了哪些代码
DeepSeek 如何对照 Acceptance 做验证
最后生成了什么回访草稿
```

这个体验，才是 Loop Engineer 的价值。

它不是让一个 AI 代理在生产环境里自由发挥，而是把复杂任务拆成多个可观察、可审计、可批准、可验证的小循环。

## Loop 不只用于修 Bug

修线上 Bug 是一个很容易理解的场景，但 Loop Engineer 不只适合工程故障。

它还可以放在很多业务工作流里。

比如客服支持：

```text
每 30 分钟读取新工单
自动回复简单问题
把高频摩擦点记录下来
沉淀成产品信号
如果某个问题重复出现，就生成改进建议
```

比如 SEO：

```text
每天早上分析数据
找出有机会的关键词
生成页面草稿
发布后持续监控表现
把效果好的方向继续放大
```

比如产品增长：

```text
每 2 小时读取产品分析数据
从用户行为里提炼信号
整理实验优先级
生成一个小的产品改动 PR
等待人审核和合并
```

这些场景看起来不一样，但结构是一样的：

```text
Trigger 启动任务
Artifacts 保存上下文
Loop Contract 约束边界
Tools 执行动作
Verify 验证结果
LOGS.md 记录过程
Output 交付结果
```

只要一个工作可以被持续观察、执行、反馈和改进，它就有机会被设计成 loop。

## Loop Engineer 改变的是工程组织方式

我更愿意把 Loop Engineer 看成一种新的工作组织方式。

过去我们把 AI 当成一个问答工具。人提出问题，AI 给出答案。

现在更有效的方式，是把 AI 放进一个有边界的系统里。它有输入，有工具，有任务合同，有验证标准，也有停止条件。

这个变化很重要。

因为真实工作里，最耗时间的部分往往不是想出一个答案，而是持续推进：

```text
看数据
查日志
整理上下文
尝试修复
运行验证
记录过程
提交结果
```

这些动作一旦被 loop 化，AI 就不再只是帮你写一段代码，而是可以帮你推进一个完整任务。

工程师的角色也会跟着变化。

人不再需要盯着每一个细节操作，而是更多负责设计 loop：

```text
定义目标
设计合同
准备上下文
配置工具
设置验证
控制权限
审核结果
```

这也是我觉得 Loop Engineer 值得关注的原因。

它不是一个花哨的新词，而是 AI 工程化之后很自然出现的一层能力。

## 结尾

Loop Engineer 的核心可以总结成一句话：

**让 AI 在一个有目标、有上下文、有工具、有验证、有边界的循环里持续工作。**

半夜三点的线上 Bug，只是一个最直观的例子。

真正有意思的地方在于，很多过去只能靠人反复盯、反复查、反复试的工作，都可以被重新设计成 loop。

AI 不是只负责回答问题，而是开始参与任务推进。

从 Prompt 到 Loop，这中间的变化，就是 AI 从“会说”走向“会做”的关键一步。
