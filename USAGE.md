# How to Use: AI Character Creation Workflow

This project is designed to be used with any LLM (ChatGPT, Claude, Gemini, etc.) through a process called **Prompt Chaining**.

## The Concept
You will act as the "Manager", passing the output of one step as the input to the next step along with the specific "System Prompt" for that step.

## Step-by-Step Guide

### Step 1: Create the Character Profile
**Goal**: Define who the character is.

1.  **Copy** the entire content of `prompts/01_character_designer.md`.
2.  **Paste** it into your LLM chat.
3.  **Add** your specific request at the bottom.
    > **Example Input**:
    > [Paste 01_character_designer.md content]
    >
    > ---
    > **User Request**: Create a 28-year-old male florist named Min-jun. He is very introverted and prefers writing letters because he stutters when speaking. He has a warm but shy personality.

4.  **Save** the output as `Minjun_profile.md`.

### Step 2: Create the Story Foundation
**Goal**: Design the relationship arc and memory outlines.

1.  **Start a New Chat** (Recommended to avoid context pollution).
2.  **Copy** the content of `prompts/02_story_writer.md`.
3.  **Paste** it into the chat.
4.  **Copy & Paste** the `Minjun_profile.md` you just created.
    > **Example Input**:
    > [Paste 02_story_writer.md content]
    >
    > ---
    > **Input Character Profile**:
    > [Paste Minjun_profile.md content]

5.  **Save** the output as `Minjun_story_foundation.md`.

### Step 3: Generate Memories
**Goal**: Write the actual 30 letters/memories.

1.  **Start a New Chat**.
2.  **Copy** `prompts/03_memory_architect.md`.
3.  **Paste** it.
4.  **Copy & Paste** `Minjun_story_foundation.md`.
    > **Example Input**:
    > [Paste 03_memory_architect.md content]
    >
    > ---
    > **Input Story Foundation**:
    > [Paste Minjun_story_foundation.md content]

5.  **Save** the output as `Minjun_30_memories.md`.

### Step 4: Quality Check
**Goal**: Evaluate the result.

1.  **Start a New Chat**.
2.  **Copy** `prompts/04_editorial_reviewer.md`.
3.  **Paste** it.
4.  **Copy & Paste** all three files (Profile, Story, Memories).
    > **Example Input**:
    > [Paste 04_editorial_reviewer.md content]
    >
    > ---
    > **Input Data**:
    > [Paste Minjun_profile.md]
    > [Paste Minjun_story_foundation.md]
    > [Paste Minjun_30_memories.md]

5.  Review the feedback and adjust if necessary.

## Automated Method (Python Script)

You can also run the entire workflow automatically using the provided Python script.

### Prerequisites
1.  Install Python 3.8+.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in the root directory and add your API key:
    ```
    OPENAI_API_KEY=sk-...
    # OR
    ANTHROPIC_API_KEY=sk-ant-...
    ```

### Running the Script
Run the script and follow the interactive prompts:
```bash
python generate_character.py
```

Or provide arguments directly:
```bash
python generate_character.py --name "Minjun" --request "A 28-year-old male florist who stutters"
```

The script will:
1.  Generate the profile.
2.  Create the story foundation.
3.  Write 30 memories.
4.  Generate a review report.
5.  Save everything in `characters/Minjun/`.
