# Content Workflow Memory

## Purpose

This project has two content-production modes:

1. User-provided script -> analyze script -> produce video
2. Topic / direction -> write copy -> create script -> produce video

The workflow should support both. Do not assume every video starts from a finished script.

## Entry Modes

### Mode A: Existing Script

Use when the user already has a complete or mostly complete script.

Codex should:

- Analyze the script structure
- Identify core argument, audience takeaway, and emotional rhythm
- Break the script into sections, scenes, and beats
- Suggest visual metaphors, motion graphics, subtitles, pacing, and materials
- Convert the script into a production-ready storyboard or video plan

### Mode B: Topic / Direction Only

Use when the user has only a topic, point of view, trend, question, or rough direction.

Codex should:

- Clarify the target audience and video purpose when needed
- Find the strongest angle or hook
- Build the argument structure
- Write the copy / narration
- Turn the copy into a short-video or explainer script
- Then continue into script analysis and video production

### Mode C: Source Material / Notes

Use when the user provides articles, notes, research, links, transcripts, or scattered ideas.

Codex should:

- Extract key facts, claims, examples, and usable insights
- Reorganize the material into a coherent narrative
- Write or rewrite it into video copy
- Generate a production-ready script and storyboard
- Then continue into video production

## Default Conversation Contract

At the start of a new video project, determine which entry mode applies:

- "A mode" means the user has a script.
- "B mode" means the user has a topic and needs copywriting.
- "C mode" means the user has source material and needs it turned into a script.

If the user does not name a mode, infer the mode from what they provide.

The long-term goal is to build a repeatable AI media production system that covers:

- Topic selection
- Angle development
- Copywriting
- Script creation
- Script analysis
- Storyboard creation
- HyperFrames / video production
- Rendering and episode archive
