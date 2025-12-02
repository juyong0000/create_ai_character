# AI Character Creation Workflow

## Overview
This document outlines the workflow for creating high-quality AI characters using **LLM Prompt Chaining**. Instead of relying on a specific tool, we use a series of specialized System Prompts to guide any LLM (GPT-4, Claude, etc.) through the creation process.

## The Process

The workflow consists of 4 sequential steps. The output of one step becomes the input for the next.

### Step 1: Character Design
## Workflow Overview

The character creation process follows a **9-step LLM prompt chaining** workflow using the **Google Gemini Ecosystem**:

1.  **Character Designer** (`prompts/01_character_designer.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: User's initial character request
    *   **Output**: `profile.md` - Character profile with appearance, personality, background
    
2.  **Visual Director** (`prompts/05_visual_director.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `profile.md`
    *   **Output**: `visual_guide.md` - Master prompts and visual consistency guide

3.  **Story Writer** (`prompts/02_story_writer.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `profile.md`
    *   **Output**: `story_foundation.md` - Story arc and 30 memory outlines

4.  **Memory Architect** (`prompts/03_memory_architect.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `story_foundation.md`
    *   **Output**: `30_memories.md` - Full narrative content for all 30 memories

5.  **Image Prompt Generation** (`prompts/06_image_generator.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `visual_guide.md`, `30_memories.md`
    *   **Output**: `image_prompts.json` - Structured prompts for image generation

6.  **Image Generation** (Automated)
    *   **Model**: **Imagen 3** (via Google GenAI REST API)
    *   **Input**: `image_prompts.json`
    *   **Output**: `.png` files in `images/` directory (Reference + 30 Memories)

7.  **Video Prompt Generation** (`prompts/07_video_director.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `visual_guide.md`, `image_prompts.json`
    *   **Output**: `video_prompts.json` - Motion prompts for video generation

8.  **Video Generation** (Automated - Experimental)
    *   **Model**: **Veo** (via Google GenAI/Vertex AI)
    *   **Input**: `video_prompts.json` + Generated Images
    *   **Output**: `.mp4` files in `videos/` directory

9.  **Editorial Reviewer** (`prompts/04_editorial_reviewer.md`)
    *   **Model**: Gemini 1.5 Pro / Flash
    *   **Input**: `profile.md`, `story_foundation.md`, `30_memories.md`
    *   **Output**: `review_report.md` - Quality assessment and approval

## Directory Structure
```
.
├── GUIDELINES.md       # Core project rules
├── WORKFLOW.md         # This file
├── prompts/            # System prompts for each step
│   ├── 01_character_designer.md
│   ├── 02_story_writer.md
│   ├── 03_memory_architect.md
│   ├── 04_editorial_reviewer.md
│   ├── 05_visual_director.md
│   ├── 06_image_generator.md
│   └── 07_video_director.md
└── characters/         # Output directory
    └── [Character Name]/
        ├── profile.md
        ├── visual_guide.md
        ├── story_foundation.md
        ├── 30_memories.md
        ├── image_prompts.json
        ├── video_prompts.json
        ├── review_report.md
        ├── images/             # Generated Images
        │   ├── reference.png
        │   └── memory_01.png...
        └── videos/             # Generated Videos
            └── reference.mp4...
```
