# AI 自媒体项目

这个仓库按“文档沉淀 + 可复用模板 + 最终成片”的方式整理。视频生成过程中的 HyperFrames 工程、快照、临时渲染和旧素材缓存不长期保留。

## 目录结构

- `templates/ai-video-frame-template/`：后续 AI 视频统一使用的 HyperFrames 画面模板。
- `exports/loop-engineer-segments/`：已经确认保留的最终 MP4 成片。
- `episodes/`：文档归档，包括脚本、分镜、需求、复盘和说明。
- `assets/`：文档中仍会引用的结构图素材。
- `project-memory/`：项目经验、风格记录、流程沉淀。
- `export/`：文档导出产物，例如 `.docx` 和文档封面资源。

## 新开一期视频

1. 从 `templates/ai-video-frame-template/` 复制出临时 HyperFrames 工程。
2. 制作时可以生成 `snapshots/`、`renders/`、预览工程等中间文件。
3. 确认完成后，只把最终 MP4 放入 `exports/loop-engineer-segments/`，把脚本或复盘放入 `episodes/`。
4. 收尾时删除临时工程、快照和临时渲染，避免把生成过程文件长期堆在仓库里。

## HyperFrames

后续视频优先参考：

- `/Users/zj/.codex/skills/ai-video-title-system/SKILL.md`
- `templates/ai-video-frame-template/`

项目不再长期保留 `hyperframes/` 或 `videos/` 生成工程目录。
