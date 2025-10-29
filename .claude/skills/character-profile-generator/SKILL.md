---
name: character-profile-generator
description: Generate comprehensive, structured character profiles in Markdown format for AI character narrative projects. Use this skill when a character has been designed and needs to be documented in a standardized profile format that includes basic information, appearance, personality, background story, relationships, and the 30-memory system (6 main + 24 sub memories). Trigger this skill immediately after character creation by romantic-character-designer agent, when character-story-writer completes the background story, or when the user explicitly requests "create/generate a character profile document".
---

# Character Profile Generator

## Overview

Generate comprehensive character profile documents in Markdown format for AI character narrative projects. This skill produces standardized, detailed profiles that capture all essential character information including physical appearance, personality traits, background story, speaking patterns, relationships, internal conflicts, and the complete 30-memory system structure.

## When to Use This Skill

Use this skill in the following scenarios:

1. **After Character Creation**: Immediately after the `romantic-character-designer` agent creates a new character
2. **After Story Development**: When the `character-story-writer` agent completes the background story
3. **Before Memory System Design**: To provide structured input for the `character-memory-architect` agent
4. **User Request**: When the user explicitly asks to "create a character profile", "document this character", or "generate character documentation"
5. **Quality Review**: When the `character-editorial-reviewer` agent needs structured character information

## Workflow

### Step 1: Gather Character Information

Before generating the profile, collect all available character information from:

- Character design documents
- Background story narratives
- Memory system structures (if already created)
- Previous conversation context
- User-provided details

**If information is missing**: Ask the user targeted questions to fill critical gaps (name, age, core personality traits, background outline).

### Step 2: Use the Profile Template

Copy the template from `assets/profile_template.md` as the foundation for the character profile. This template includes:

- **Basic Information**: Name, age, gender, occupation, physical stats
- **Physical Appearance**: Face, body type, style, distinctive features
- **Personality**: Core traits, strengths, weaknesses, values
- **Speech Patterns**: Tone, formality, common phrases, dialogue examples
- **Background Story**: Childhood, adolescence, adulthood, key events, traumas
- **Relationships**: Family, important people, relationship with user
- **Internal Conflicts**: Core conflicts, desires vs. fears
- **Daily Life**: Routines, hobbies, habits
- **Skills & Abilities**: Expertise, talents, weaknesses
- **Goals & Motivations**: Short-term, long-term, fundamental drives
- **30-Memory System**: 6 main memories + 24 sub memories with unlock conditions

### Step 3: Fill in the Template

Replace all placeholder text (indicated by `[brackets]`) with specific character details:

**Good Example**:
```markdown
**이름**: 이서연
**나이**: 28세
**직업**: 독립 서점 주인
```

**Bad Example** (leaving placeholders):
```markdown
**이름**: [캐릭터 이름]
**나이**: [나이]
```

**Guidelines**:
- Be specific and concrete, not generic
- Use descriptive language that creates vivid mental images
- Ensure consistency across all sections
- Make connections between different sections (e.g., personality traits should align with background events)
- For the 30-memory system:
  - Create 6 main memories that form the narrative spine
  - Organize 24 sub memories into 6 categories (4 memories each)
  - Specify unlock conditions (level-up for main, gacha/activities for sub)
  - Ensure memories don't contradict each other

### Step 4: Ensure Narrative Coherence

After filling the template, verify:

1. **Internal Consistency**: Does personality match speech patterns? Do traumas explain current behavior?
2. **Memory System Alignment**: Do the 30 memories reflect the background story?
3. **Character Depth**: Are there layers of complexity, not just surface traits?
4. **Emotional Resonance**: Will users in their 20s-40s connect with this character emotionally?
5. **Romantic Appeal**: Does the character have qualities that make them appealing as a romantic partner?

### Step 5: Save the Profile

Save the completed profile as a Markdown file with a clear filename:

**Naming Convention**: `[character-name]-profile.md`

**Examples**:
- `이서연-profile.md`
- `MinJae-Park-profile.md`
- `Yuna-profile.md`

**Location**: Save in the current working directory or ask the user where to save it.

## Template Sections Explained

### Basic Information
Concrete, factual details that ground the character in reality.

### Physical Appearance
Detailed enough for readers to visualize the character. Include distinctive features that make them memorable.

### Personality
5 core traits with explanations, plus strengths, weaknesses, and values. Should feel multi-dimensional.

### Speech Patterns
Critical for AI character implementation. Include:
- Formality level (formal/informal)
- Tone (warm, cold, playful, serious)
- Distinctive verbal habits
- 2-3 dialogue examples showing different situations

### Background Story
Chronological narrative broken into life stages. Include 3+ pivotal events that shaped who they are today.

### Relationships
Focus on how relationships influenced character development and current personality.

### Internal Conflicts
The emotional and psychological tensions that drive character depth. Format: desire vs. fear, goal vs. obstacle.

### 30-Memory System
**Main Memories (6)**:
- Form the central narrative arc
- Unlock sequentially as relationship levels increase
- Contain the most emotionally significant revelations
- Should build toward deeper intimacy and understanding

**Sub Memories (24)**:
- Organized into 6 categories × 4 memories each
- Unlock through gacha or activities
- Add texture, humor, worldbuilding, and character depth
- Not essential to main story but enhance immersion

**Category Distribution**:
1. Childhood (4 memories)
2. Adolescence (4 memories)
3. Adulthood/Present (4 memories)
4. Relationships (4 memories)
5. Hobbies/Daily Life (4 memories)
6. Emotions/Inner World (4 memories)

## Assets

### assets/profile_template.md

Comprehensive Markdown template with all required sections pre-structured. Copy this template as the starting point for every character profile.

**Usage**:
```bash
# Copy template to create new profile
cp assets/profile_template.md ./[character-name]-profile.md
```

Then fill in all bracketed placeholders with specific character details.

## Best Practices

1. **Be Specific**: Avoid vague descriptors. "She has a warm smile" → "Her smile creates small crinkles at the corners of her eyes, giving her a perpetually kind expression"

2. **Show Character Through Details**: Instead of saying "she's kind", show it through background events, relationships, and memories

3. **Create Emotional Depth**: Every character should have desires, fears, contradictions, and growth potential

4. **Maintain Coherence**: All sections should tell a unified story about who this person is

5. **Consider Target Audience**: Design characters that appeal romantically to users in their 20s-40s

6. **Memory System Balance**:
   - Main memories: High emotional weight, narrative progression
   - Sub memories: Lighter, varied, enriching but not essential

7. **Use Concrete Examples**: In dialogue, habits, and memories—show, don't just tell

## Common Mistakes to Avoid

- Leaving placeholder text unfilled
- Generic descriptions ("nice person", "pretty face")
- Inconsistent personality traits
- Memories that contradict background story
- Flat characters without internal conflicts
- Speech patterns that don't match personality
- Missing or incomplete memory system sections

## Example Use Cases

**Case 1: After romantic-character-designer creates a character**
```
User: [Uses romantic-character-designer agent]
Agent: [Creates character named "이서연", 28, bookstore owner]
→ TRIGGER: Use character-profile-generator to document this character
```

**Case 2: User requests profile creation**
```
User: "캐릭터 프로필 문서 만들어줘"
→ TRIGGER: Use character-profile-generator
→ Ask user for character details if not in context
```

**Case 3: Before memory system design**
```
User: [Has character background story completed]
User: "이제 30개 기억 시스템을 만들어보자"
→ FIRST: Use character-profile-generator to structure all information
→ THEN: Provide structured profile to character-memory-architect
```

## Output Format

The generated profile should be:
- **Format**: Markdown (.md file)
- **Structure**: Following the template exactly
- **Completeness**: All sections filled with specific details
- **Length**: Typically 3000-5000 words for a complete profile
- **Readability**: Well-formatted with clear headers and hierarchy
