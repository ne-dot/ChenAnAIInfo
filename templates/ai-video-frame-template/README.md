# AI Video Frame Template

用于 `/Users/zj/Documents/AI 自媒体` 项目的 HyperFrames 模板帧。

这个模板默认带可见标注，用来说明画面结构。正式制作视频时，可以删除或隐藏 `.guide-*` 元素。

## 修改入口

- `Top Bar Label`: 修改 `.kicker`
- `Main Title`: 修改 `.title-main`
- `Subtitle`: 可选。没有副标题时保持 `<header class="title-area">`；有副标题时改成 `<header class="title-area has-subtitle">` 并填写 `.title-subtitle`
- `Right Metadata`: 修改 `.metadata`
- `Animation Area`: 只替换 `.animation-content` 内部内容
- `Subtitle Safe Area`: 底部 `125px` 保持空白，不放文字或图形
- `Guide Labels`: 标注元素使用 `.guide-label`、`.guide-note`、`.guide-outline`，正式视频可隐藏或删除

## 运行

```bash
npm run dev
npm run check
npm run snapshot
```
