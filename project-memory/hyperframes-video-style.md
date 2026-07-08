# AI Explainer Series Visual Memory

## Project

Series: AI science explainer video channel

Goal: Create a repeatable visual and motion design system for a series of AI explainer videos. Each episode can discuss a different AI topic, but the whole channel should feel visually consistent and recognizable.

Current example episode:

`02 AI Native 为什么不是一次功能升级，而是一种新的软件范式`

Episode length can vary by platform, but the main style system should work for:

- 4-8 minute horizontal explainers
- 60-90 second vertical cuts
- Shorts / reels / teaser clips
- Title cards, chapter cards, thumbnails, and motion graphic inserts

Style reference image:

`/Users/zj/Documents/深度/新形象.png`

Important: this image is a visual style reference, not a required character asset. Do not assume the AI researcher must appear, speak, lip-sync, or act in every video. Use the image to guide the 2D illustrated tech aesthetic, color palette, lab atmosphere, clothing/material feel, and overall premium AI research vibe.

Current series background reference:

`/Users/zj/Documents/AI 自媒体/assets/backgrounds/ai-research-lab-dark-bg.png`

Use this as the baseline dark 2D AI research lab background. It is intentionally dark and should behave as visual space, not the main subject. Foreground nodes, text, paths, and product evidence should remain the visual focus.

## Series Core Style

Use this as the global visual style for all HyperFrames scenes:

```text
2D illustrated tech explainer, AI research lab style, dark blue AI research lab,
clean futuristic UI, anime-inspired but professional, blue neon accents,
transparent holographic panels, code interfaces, workflow diagrams,
calm intelligent educational tone, premium technology media style,
flat motion graphics, crisp Chinese title cards, high contrast lighting.
```

Short style definition:

`2D illustrated AI research lab aesthetic + professional technology motion graphic.`

The whole series should feel like advanced AI ideas are being explained inside a futuristic AI research lab. The reference character can inspire the visual identity, but the main video language should be mechanism animation, diagrams, real product evidence, and motion graphics.

## Style Reference Character

The reference image defines the style direction:

- Young female AI researcher
- Blue baseball cap with "AI"
- Black short hair
- Thin glasses
- Blue and black tech jacket
- Calm, smart, friendly expression
- Works in an AI research lab or control-room-like workspace
- Surrounded by laptops, code screens, neural network diagrams, whiteboards, and holographic UI panels

The character is optional. If used, use it only as:

- Static brand-style visual reference
- Thumbnail or cover inspiration
- Occasional non-speaking illustration
- Small title-card accent if needed

Do not create or imply a talking presenter from this single image unless the user explicitly provides or requests digital human / lip-sync assets. Do not redesign the reference into a different person, mascot, 3D avatar, photorealistic presenter, or exaggerated cartoon.

## Color System

Primary colors:

- Deep navy / near black backgrounds
- Blue-violet environmental light
- Electric blue / cyan information highlights
- Cool gray UI panels
- White text

Accent colors:

- Cyan for active AI flows
- Soft blue glow for key concepts
- Restrained violet / blue-purple as atmosphere, AI field, and glass-material depth
- Limited green only for success / verification states
- Limited red only for error / failure states

Avoid:

- Large purple SaaS gradients or generic purple-blue landing-page backgrounds
- Purple applied only to random icons without affecting the overall scene atmosphere
- Beige, tan, brown, orange-dominant palettes
- Overly colorful cartoon palettes
- Random cyberpunk pink/purple lighting

## Visual Language

Preferred visuals:

- 2D motion graphics
- Transparent UI overlays
- Flow diagrams
- Code editor panels
- Task queues
- Agent planning boards
- Nodes and connection lines
- Before/after comparison layouts
- Clean Chinese keyword cards
- Product interface reenactments or recordings when needed
- Real screenshots, web captures, or news images when they provide factual grounding

Avoid:

- Photorealistic human footage
- Generic stock footage
- Busy cyberpunk city backgrounds
- Pure PPT slides with no visual depth
- Excessive glow, lens flare, particles, or clutter
- Random 3D objects unless specifically needed

## Motion Rules

Animation should feel precise and explanatory:

- UI panels slide in lightly
- Lines connect concepts step by step
- Nodes pulse only when active
- Keywords appear with clean cuts or short fades
- Use zooms to focus attention on the current idea
- Keep movement calm and readable

Do not use:

- Fast chaotic camera movement
- Overly elastic cartoon motion
- Distracting particle explosions
- Constant background motion that competes with subtitles

## Professional Motion Graphic Rules

The animation style should follow professional technology explainer motion graphics, similar in restraint and clarity to OpenAI / Apple WWDC / Linear style references.

This is not:

- Web UI
- Dashboard
- Admin panel
- SaaS hero page
- PPT slide animation
- Decorative tech wallpaper

The goal of motion is explanation, not spectacle:

- One shot explains one core idea
- One frame has one visual focus
- The viewer should understand the mechanism even with narration muted
- Mobile readability is mandatory
- Every animation choice should help the audience understand the current AI mechanism, product shift, model behavior, workflow change, or industry concept

## Motion Spec First

Before generating or implementing any important HyperFrames / Remotion animation, create a Motion Spec first.

Required fields:

- Scene Goal: what the shot explains
- Audience Takeaway: what the viewer should understand after watching
- Script Understanding: what part of the narration this shot maps to
- Visual Metaphor: what visual mechanism explains the idea
- Layout: screen structure and subject scale
- Visual Focus: where the viewer should look first
- Node List: node names and approximate x/y/width/height
- SVG Path List: start point, end point, rounded corner radius
- Motion Type: Draw / Morph / Assemble / Converge / Slide / Flow
- Camera Direction: push in, pull out, pan, or parallax if longer than 5 seconds
- Timeline: frame-by-frame or second-by-second entrance, hold, turn, exit
- Acceptance Checklist: how to judge whether the shot is clear, professional, and restrained

Do not jump directly from a rough concept to code or final generation. First translate the concept into a shot design.

## Layout Discipline

Each scene should be composed as a motion graphic system, not a screen mockup:

- Main subject occupies 50%-70% of the canvas
- Visual center stays in the middle 50%-70% of the frame
- Important elements should be at least 180px wide
- Main Chinese text should be at least 40px where possible
- Supporting Chinese text should not be smaller than 32px
- Keep at least 48px visual spacing between key elements
- Use 8px or 12px spacing increments
- Limit major visual elements to 5 per shot; if more are needed, stage them over time or split the scene
- Empty space should strengthen focus, not make the subject feel small

## Visual System Details

Every scene should define or inherit one consistent visual system:

- Background: dark, low contrast, with subtle spatial depth
- Primary color: blue-violet environmental light for AI Core and spatial atmosphere
- Secondary color: cyan or white for supporting capabilities
- Accent color: only one accent per scene, reserved for key contrast or turning point
- Typography: maximum 3 size levels
- Radius: consistent rounded corners across nodes and panels
- Stroke: consistent line thickness
- Glow: only for visual focus and main connection path
- Materials: restrained glassmorphism, no excessive blur or glow

Avoid cheap tech effects:

- Random particle fields
- Large neon outlines everywhere
- Competing gradients
- Decorative scanning lines
- Dense HUD overlays
- Every component glowing at once
- Too many colors

## Series Visual Metaphors

AI Core can be the visual center when explaining system-level AI mechanisms, but not every episode must use the same structure. Choose the metaphor that best clarifies the current topic.

Preferred metaphors:

- Scattered signals converge into an AI Core
- User manual workflow turns into AI-organized workflow
- Many app/function entrances collapse into one goal entrance
- Feature buttons transform into system capabilities
- Responsibility moves from user to system
- Data flows through model layers
- Context enters memory / retrieval / tool-use modules
- Model reasoning path becomes a visible route
- Agents split work into planning, tool use, verification, and iteration
- Industry timeline compresses into cause-and-effect milestones
- Competing products or paradigms appear as clear side-by-side systems

These metaphors should stay consistent with the 2D illustrated tech lab style and should not become abstract dashboard UI.

For the AI Native episode specifically, prioritize:

- Scattered AI features converge into AI Core
- User manual workflow turns into AI-organized workflow
- Many app/function entrances collapse into one goal entrance
- Feature buttons transform into system capabilities
- Responsibility moves from user to system
- User expresses goal; software organizes work

## Nodes And Connectors

Nodes represent system capabilities, intelligent agents, tools, model layers, or workflow states. They should not look like ordinary web buttons or cards.

Node rules:

- Each node should contain an outline SVG-style icon and a short label
- Ordinary nodes should be at least 180x72
- Core nodes should be around 220x220 or larger when central
- Icon size should be around 28-44px
- Label size should be around 32-48px
- Nodes can have subtle glow and breathing, but only the active node should feel emphasized

Connector rules:

- Use rounded orthogonal connector paths
- Structure: horizontal segment + large rounded corner + vertical segment + large rounded corner + horizontal segment
- Avoid random Bezier curves, wave lines, ordinary sharp polylines, or Visio-like flowcharts
- Recommended stroke width: 3px
- Recommended corner radius: 64-80px
- Main path may use a soft electric blue / blue-violet glow

## Camera Rules

Any shot longer than 5 seconds should include subtle camera motion:

- Slow push in
- Slow pull out
- Gentle pan
- Parallax between background, paths, and nodes

Camera motion must guide attention:

- Define the camera purpose before generating
- Define start view and end view
- Define the final focus target
- Keep scale and translate movement restrained
- Use depth layers only to support clarity

## Preferred Motion Types

Use:

- Draw: paths are drawn to reveal connection
- Morph: function buttons transform into system capabilities
- Assemble: scattered parts assemble into AI Core
- Converge: separate tools flow toward the goal
- Slide: panels enter with purpose
- Flow: particles or light travel along the active path

Use sparingly:

- Fade
- Random rotation
- Large bouncing
- Decorative scaling

Each scene should have one dominant animation. If several things move at once, one must clearly be the primary focus.

## Typography

Chinese text should be clean, bold, and easy to read:

- Big chapter keywords
- Short phrases only
- High contrast
- No long paragraphs on screen
- Important words highlighted in electric blue or white

Preferred on-screen phrasing:

- Series-level reusable phrases:
- `模型`
- `上下文`
- `工具调用`
- `Agent`
- `记忆`
- `推理`
- `多模态`
- `工作流`
- `从功能到目标`
- `从工具到系统`
- `从提示词到任务`
- AI Native episode phrases:
- `功能入口 -> 目标入口`
- `用户表达目标`
- `软件组织工作`
- `理解目标`
- `读取上下文`
- `调用工具`
- `推进执行`
- `前台一句话，后台一整套流程`

## Narrative Framing

The series should feel like:

`Complex AI ideas explained inside a futuristic research lab using clear, premium, 2D motion graphics.`

The tone is:

- Clear
- Analytical
- Premium
- Useful
- Not hype-driven
- Not childish
- Not sensationalist
- Not marketing-heavy

Series-level editorial principle:

`把复杂 AI 概念讲成可视化机制，而不是堆术语、堆新闻、堆工具清单。`

For the current AI Native episode, preserve this conclusion:

`AI Native 不是软件多了一个 AI 功能，而是用户表达目标，软件开始组织工作。`

## Real-World Material Policy

The series can use real-world material when it improves credibility or provides factual grounding.

Use real material for:

- Product examples
- Official announcements
- News screenshots
- Public product pages
- App icons
- Interface examples
- Release demos
- Benchmark charts, if sourced clearly

Prefer generated / designed motion graphics for:

- Abstract mechanisms
- AI Core
- Model internals
- Context flow
- Agent workflow
- Capability orchestration
- Concept comparisons

Recording is optional, not mandatory at the beginning:

- First use web screenshots, official pages, product captures, or reconstructed 2D interface scenes
- Use real screen recording only when the episode needs stronger proof or when static material cannot explain the workflow
- When using real screenshots, wrap them inside the series visual system: dark lab background, subtle frame, restrained highlights, consistent captions, and no clutter

Avoid letting external material dominate the visual identity. Real assets should be evidence inside the series style, not a replacement for the style.

## HyperFrames Global Negative Prompt

Use or adapt this negative prompt in scene generation:

```text
photorealistic presenter, live action footage, 3D mascot, childish cartoon,
purple gradient SaaS landing page, generic stock footage, cluttered interface,
illegible text, random cyberpunk city, exaggerated neon, lens flare overload,
comic style, low resolution, inconsistent character, different outfit,
different face, warm brown palette, orange dominant lighting, dashboard,
admin panel, webpage card UI, SaaS hero layout, PPT slide, dense HUD,
tiny text, random particles, scanning lines, excessive glow, competing gradients,
Visio flowchart, sharp connector lines, wave connector lines
```

## Production Rule

Every scene prompt should reference this memory first, then define the specific scene. The character, color palette, UI style, and motion language should stay consistent across the full video.

## Collaboration Workflow

When the user provides a new video script, do not directly generate the full video or start implementing animations.

Use this workflow:

1. Discuss the overall video structure first
2. Clarify the narrative logic, section order, and viewer cognition path
3. Convert the script into a scene-by-scene storyboard
4. Identify which scenes need generated motion graphics, real screenshots, product captures, web material, or optional screen recordings
5. List all animations that need to be generated
6. For each animation, write a professional Motion Spec first
7. Convert each Motion Spec into a Final Animation Prompt
8. Only generate or implement animation after the prompt is clear enough and the user has confirmed the direction, unless the user explicitly says to proceed directly

The user's initial animation description may be rough. Treat it as an idea, not a finished animation brief. Help translate it into:

- Scene goal
- Visual metaphor
- Layout
- Visual focus
- Animation stages
- Timing
- Required assets
- Negative constraints

## Voiceover And Editing Workflow

The user will create the voiceover later in Jianying / CapCut. This project does not need to produce final voice narration.

However, every storyboard and animation plan must explain how voiceover should sync with visuals:

- Which narration sentence maps to which shot
- Where the visual should enter before the sentence
- Where key words should appear on screen
- Where the animation should pause for reading
- Where a transition should happen
- Which shots can be extended or shortened in editing

For each scene, provide editing notes for the user:

- Suggested duration
- Narration text
- Visual timing
- On-screen text
- Animation beat
- Cut point
- Whether the shot should hold for voiceover

Deliverables should focus on:

- Storyboard
- Shot logic
- Animation list
- Motion Specs
- Final Animation Prompts
- Generated video clips / assets when requested
- Voiceover sync notes for editing

Do not assume the final video must be fully edited here. The user will handle voiceover recording, final timeline editing, subtitles, and final assembly in Jianying / CapCut unless they ask otherwise.

Recommended prompt prefix:

```text
Follow the established style memory: 2D illustrated AI research lab aesthetic inspired by the reference image, dark blue AI research lab, clean holographic UI, electric blue accents, anime-inspired but professional illustration style, calm premium educational tone. The reference image is for style only; do not generate a talking host unless explicitly requested.
```

Recommended motion prompt prefix:

```text
Design this as a professional technology motion graphic, not a webpage, dashboard, admin UI, SaaS hero, or PPT slide. One shot explains one idea, with one visual focus. Use restrained 2D motion graphics, dark spatial background, glass-like capability nodes, rounded orthogonal SVG connector paths, subtle camera push, and clear mobile-readable Chinese labels.
```

## Final Self-Check

Before accepting a scene, verify:

- Can the viewer understand the mechanism with narration muted?
- Is there a clear visual focus within the first second?
- Does the scene have 5 or fewer major visual elements at once?
- Is all important Chinese text at least 32px?
- Is only one animation competing for primary attention?
- Does the image avoid looking like web UI, dashboard, admin panel, SaaS hero, or PPT?
- Can the shot be explained in one sentence?
- Are color, glow, font scale, radius, spacing, and connector style consistent?
