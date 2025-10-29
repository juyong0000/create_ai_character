---
name: character-project-manager
description: Orchestrate the complete AI character creation workflow by managing directory structure, coordinating multiple specialized agents (romantic-character-designer, character-story-writer, character-memory-architect, character-editorial-reviewer), and organizing output files systematically. Use this skill when the user requests to create a new AI character, start a character project, or needs to organize an existing character's files. This skill automatically triggers at the beginning of any character creation workflow.
---

# Character Project Manager

## Overview

Orchestrate the complete AI character creation workflow from initial concept to final deliverable. This skill manages the entire project lifecycle by creating organized directory structures, coordinating specialized agents, tracking progress, and ensuring all outputs are saved to the correct locations in a standardized format.

## When to Use This Skill

Use this skill automatically in the following scenarios:

1. **New Character Creation**: When the user says "create a new character", "make a character", "새 캐릭터 만들어줘"
2. **Character Project Setup**: When starting any character design workflow
3. **File Organization**: When organizing existing character files into the proper structure
4. **Workflow Coordination**: When multiple character agents need to work together sequentially

**Trigger Keywords**: "새 캐릭터", "create character", "character project", "캐릭터 만들어"

## Complete Workflow

### Phase 1: Project Initialization

**Goal**: Set up the project structure and prepare the workspace.

#### Step 1.1: Gather Basic Information

Ask the user for essential starting information:
- Character name (required)
- Any initial concept or inspiration (optional)
- Target demographic preferences (optional - default: 20s-40s for romantic AI)

**Example Questions**:
```
"새로운 캐릭터를 만들어드리겠습니다. 캐릭터의 이름은 무엇으로 하시겠어요?"

"캐릭터에 대한 초기 아이디어나 컨셉이 있으시면 알려주세요.
(예: '조용하고 지적인 서점 주인', '밝고 활발한 카페 바리스타' 등)
없으시면 제가 추천해드릴게요."
```

#### Step 1.2: Create Directory Structure

Use the `scripts/setup_character_directory.py` script to create the organized project structure:

```bash
python scripts/setup_character_directory.py "<character_name>" --base-dir ./characters
```

This creates:
```
characters/
└── character-XXX-<name>/
    ├── 01-profile.md           # Character profile
    ├── 02-background-story.md  # Detailed backstory
    ├── 03-memory-system.md     # 30-memory system
    ├── 04-review-notes.md      # Review feedback
    ├── README.md               # Project overview
    └── assets/                 # Images, references
```

#### Step 1.3: Confirm Setup

Inform the user:
```
"✅ 캐릭터 프로젝트 디렉토리를 생성했습니다!
📁 위치: characters/character-XXX-<name>/

이제 캐릭터 디자인을 시작하겠습니다."
```

---

### Phase 2: Character Design

**Goal**: Create the initial character concept with physical appearance and basic background.

#### Step 2.1: Launch romantic-character-designer Agent

Use the Task tool to invoke the romantic-character-designer agent with the user's initial concept:

```
Prompt: Create a romantic AI character design with the following details:
- Name: <character_name>
- Initial concept: <user_concept>
- Target audience: 20s-40s seeking romantic connection

Include detailed physical appearance, personality traits, speaking style, and basic background story.
```

#### Step 2.2: Save Design Output

When the agent completes, extract the character design and prepare for profile generation.

---

### Phase 3: Profile Documentation

**Goal**: Create a structured, comprehensive character profile document.

#### Step 3.1: Trigger character-profile-generator Skill

The character-profile-generator skill should automatically activate (or manually trigger it) to create the standardized profile using the template.

#### Step 3.2: Save Profile

Write the completed profile to:
```
characters/character-XXX-<name>/01-profile.md
```

Update the README.md checklist:
```markdown
- [x] 캐릭터 디자인 (romantic-character-designer)
- [x] 프로필 생성 (character-profile-generator)
- [ ] 백스토리 작성 (character-story-writer)
...
```

---

### Phase 4: Background Story Development

**Goal**: Develop a deep, emotionally resonant background story with concrete narrative events.

#### Step 4.1: Launch character-story-writer Agent

Use the Task tool with the completed profile:

```
Prompt: Develop a detailed background story for this character based on the profile:
[Include the 01-profile.md content]

Create concrete narrative events, relationships, traumas, and emotional arcs that will serve as the foundation for the 30-memory system.
```

#### Step 4.2: Save Background Story

Write the detailed backstory to:
```
characters/character-XXX-<name>/02-background-story.md
```

Update README.md progress.

---

### Phase 5: Memory System Architecture

**Goal**: Transform the background story into the 30-memory system structure.

#### Step 5.1: Launch character-memory-architect Agent

Use the Task tool with both profile and backstory:

```
Prompt: Design the 30-memory system for this character:

Profile: [Include 01-profile.md]
Background Story: [Include 02-background-story.md]

Create 6 main memories (unlock via relationship levels) and 24 sub memories (unlock via gacha/activities) organized into 6 categories.
```

#### Step 5.2: Save Memory System

Write the memory structure to:
```
characters/character-XXX-<name>/03-memory-system.md
```

Update README.md progress.

---

### Phase 6: Editorial Review

**Goal**: Quality assurance and improvement recommendations.

#### Step 6.1: Launch character-editorial-reviewer Agent

Use the Task tool with all completed materials:

```
Prompt: Review this complete character design for quality, appeal, and commercial viability:

Profile: [Include 01-profile.md]
Background Story: [Include 02-background-story.md]
Memory System: [Include 03-memory-system.md]

Provide feedback on:
- Overall appeal to target demographic (20s-40s)
- Narrative coherence and depth
- Memory system balance
- Areas for improvement
```

#### Step 6.2: Save Review Notes

Write the review feedback to:
```
characters/character-XXX-<name>/04-review-notes.md
```

Append to existing content with timestamp.

---

### Phase 7: Iteration (If Needed)

**Goal**: Refine the character based on editorial feedback or user requests.

#### Step 7.1: Analyze Feedback

Review the editorial notes and identify areas requiring revision.

#### Step 7.2: Selective Re-execution

Re-run specific agents for sections that need improvement:
- Profile updates → Edit 01-profile.md directly or use character-profile-generator
- Story improvements → Re-run character-story-writer
- Memory rebalancing → Re-run character-memory-architect

#### Step 7.3: Track Iterations

Add iteration notes to 04-review-notes.md with timestamps.

---

### Phase 8: Project Completion

**Goal**: Finalize the character and mark project as complete.

#### Step 8.1: Final Checklist

Verify all files are complete:
- ✅ 01-profile.md (filled, no placeholders)
- ✅ 02-background-story.md (detailed narrative)
- ✅ 03-memory-system.md (6 main + 24 sub memories)
- ✅ 04-review-notes.md (editorial feedback)

#### Step 8.2: Update README

Mark all tasks complete in README.md:
```markdown
- [x] 캐릭터 디자인 (romantic-character-designer)
- [x] 프로필 생성 (character-profile-generator)
- [x] 백스토리 작성 (character-story-writer)
- [x] 기억 시스템 설계 (character-memory-architect)
- [x] 검수 (character-editorial-reviewer)
- [x] 최종 완성
```

#### Step 8.3: Summary Report

Provide the user with a completion summary:
```
"🎉 캐릭터 '<name>' 생성이 완료되었습니다!

📁 프로젝트 위치: characters/character-XXX-<name>/

📄 생성된 파일:
✅ 01-profile.md - 캐릭터 프로필
✅ 02-background-story.md - 백그라운드 스토리
✅ 03-memory-system.md - 30개 기억 시스템
✅ 04-review-notes.md - 검수 및 피드백

다음 단계: [제안사항]
"
```

---

## File Management Rules

### File Naming Conventions

- **Profile**: `01-profile.md`
- **Background**: `02-background-story.md`
- **Memories**: `03-memory-system.md`
- **Reviews**: `04-review-notes.md`
- **Project Info**: `README.md`

### Directory Naming

Format: `character-XXX-<sanitized_name>`
- XXX: 3-digit incremental number (001, 002, 003...)
- sanitized_name: Name with spaces removed, special chars cleaned
- Examples: `character-001-이서연`, `character-002-MinJaePark`

### Update Strategy

- **Append**: 04-review-notes.md (add new reviews with timestamps)
- **Replace**: Other files (overwrite with improved versions)
- **Never Delete**: Keep all versions in git history if using version control

---

## Progress Tracking

Use TodoWrite tool to track the workflow progress in real-time:

```
Todos:
1. [in_progress] Set up character project directory
2. [pending] Run romantic-character-designer agent
3. [pending] Generate character profile document
4. [pending] Develop background story
5. [pending] Design 30-memory system
6. [pending] Editorial review
7. [pending] Final completion
```

Update todo status as each phase completes.

---

## Scripts

### scripts/setup_character_directory.py

Creates the standardized directory structure for a new character project.

**Usage**:
```bash
python scripts/setup_character_directory.py "<character_name>"
python scripts/setup_character_directory.py "<character_name>" --base-dir /custom/path
```

**What it does**:
- Creates `characters/` base directory if needed
- Generates unique character directory with incremental numbering
- Creates all placeholder .md files with timestamps
- Sets up assets/ subdirectory
- Generates README.md with checklist

**Output**: Returns the path to the created character directory

---

## Agent Coordination

### Agent Invocation Order

1. **romantic-character-designer** → Initial design
2. **character-profile-generator** (skill) → Structured documentation
3. **character-story-writer** → Deep narrative
4. **character-memory-architect** → Memory system
5. **character-editorial-reviewer** → Quality check

### Data Flow

```
User Input
    ↓
[romantic-character-designer] → Character concept
    ↓
[character-profile-generator] → 01-profile.md
    ↓
[character-story-writer] → 02-background-story.md
    ↓
[character-memory-architect] → 03-memory-system.md
    ↓
[character-editorial-reviewer] → 04-review-notes.md
    ↓
Final Character Package
```

### Error Handling

If any agent fails or produces insufficient output:
1. Log the issue in 04-review-notes.md
2. Ask user if they want to retry or provide additional guidance
3. Re-run the failed agent with more specific instructions
4. Continue from the point of failure

---

## Best Practices

1. **Always Create Directory First**: Before launching any agents, set up the directory structure
2. **Save Incrementally**: Don't wait until the end - save each output as it's generated
3. **Track Progress Visibly**: Update README.md and use TodoWrite so users see progress
4. **Preserve Context**: When launching agents, provide all previously generated content
5. **Atomic Updates**: Update one file completely before moving to the next phase
6. **User Communication**: Keep user informed at each phase transition
7. **Flexible Workflow**: Allow users to skip or repeat phases if desired

---

## Common User Requests

### "Create a new character"
→ Execute full workflow from Phase 1 to Phase 8

### "Make a character like X"
→ Pass the inspiration to romantic-character-designer in Phase 2

### "Review this character"
→ Skip to Phase 6 with existing files

### "Reorganize my character files"
→ Create directory structure and move files to correct locations

### "Continue working on [character name]"
→ Check which phase was last completed and resume from next phase

---

## Example Workflow Execution

```
User: "20대 후반 서점 주인 컨셉으로 캐릭터 만들어줘"

Claude (using character-project-manager):
1. ✅ Ask for character name → "이서연"
2. ✅ Run setup_character_directory.py
3. ✅ Launch romantic-character-designer with "20대 후반 서점 주인"
4. ✅ Trigger character-profile-generator, save to 01-profile.md
5. ✅ Launch character-story-writer, save to 02-background-story.md
6. ✅ Launch character-memory-architect, save to 03-memory-system.md
7. ✅ Launch character-editorial-reviewer, save to 04-review-notes.md
8. ✅ Update README.md, provide summary to user

Result: Complete character package in characters/character-001-이서연/
```

---

## Integration with Other Skills

- **character-profile-generator**: Automatically triggered in Phase 3
- **theme-factory**: Can be used to style final documentation
- **docx/pptx**: Can convert final outputs to presentation formats if requested

---

## Troubleshooting

### Issue: Directory already exists
**Solution**: Script auto-increments number, won't overwrite

### Issue: Agent produces incomplete output
**Solution**: Save what's available, note gaps in review file, ask user if should retry

### Issue: User wants to change character mid-workflow
**Solution**: Save current state, ask if should start new project or modify existing

### Issue: Files not saving to correct location
**Solution**: Always use absolute paths constructed from the character directory path returned by setup script
