# AI 自媒体项目

这个仓库按“项目级制作工具 + 每期视频独立归档”的方式整理。

## 目录结构

- `hyperframes/`：项目级 HyperFrames 工程。后续视频复用这一套预览、校验、渲染命令和通用素材引用。
- `episodes/`：每期视频一个单独文件夹，存放脚本、分镜、原型、导出成片和复盘。
- `assets/`：跨视频可复用素材库。
- `project-memory/`：项目经验、风格记录、流程沉淀。

## 新开一期视频

1. 在 `episodes/` 下创建新文件夹，例如 `episodes/03-topic-name/`。
2. 建议保留这些子目录：
   - `storyboard/`：分镜、旁白、时间轴。
   - `prototype/`：快速验证用的临时代码或实验。
   - `renders/`：该期导出的 MP4、截图、阶段版本。
   - `notes/`：复盘、素材来源、发布记录。
3. 在 `hyperframes/` 中制作或复制对应 composition；最终导出后，把成片归档到该期 `renders/`。

## HyperFrames

进入项目级工程后运行：

```bash
cd hyperframes
npm run dev
npm run check
npm run render
```

`hyperframes/renders/` 是临时渲染输出目录；收尾时把确认要保留的版本移动到对应 `episodes/<episode>/renders/`。
