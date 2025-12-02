from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import time
import json
from pathlib import Path
from character_engine import CharacterEngine

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (images/videos)
# We will mount the 'characters' directory to serve generated files
CHAR_DIR = Path("characters")
CHAR_DIR.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory="characters"), name="files")

# Engine
try:
    engine = CharacterEngine()
except Exception as e:
    print(f"Failed to initialize engine: {e}")
    engine = None

class InitRequest(BaseModel):
    name: str
    description: str

class StepRequest(BaseModel):
    character_name: str
    step: str
    context: Dict[str, Any] # Previous step outputs

class RegenerateReferenceRequest(BaseModel):
    character_name: str
    current_prompt: str
    additional_instruction: str

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Gemini Character Generator API"}

@app.post("/api/init")
def init_character(req: InitRequest):
    """Initialize a new character."""
    # Create directory
    base_dir = CHAR_DIR / req.name
    base_dir.mkdir(parents=True, exist_ok=True)
    return {"status": "created", "name": req.name, "path": str(base_dir)}

@app.post("/api/generate")
def generate_step(req: StepRequest):
    """Run a generation step."""
    if not engine:
        raise HTTPException(status_code=500, detail="AI Engine not initialized")

    name = req.character_name
    step = req.step
    ctx = req.context
    
    # Load prompts (Assuming prompts are in ../prompts relative to backend)
    # Actually, let's fix the path.
    # backend/ is cwd for the server? No, usually root.
    # We will assume running from root for now, or fix paths.
    PROMPT_DIR = Path("prompts")
    
    response_content = ""
    
    try:
        if step == "profile":
            prompt = (PROMPT_DIR / "01_character_designer.md").read_text(encoding="utf-8")
            char_name = ctx.get("char_name", name)
            user_input = f"Character Name: {char_name}\nDescription: {ctx.get('request', '')}"
            response_content = engine.generate_text(prompt, user_input)
            engine.save_file(name, "profile.md", response_content)

        elif step == "visual":
            prompt = (PROMPT_DIR / "05_visual_director.md").read_text(encoding="utf-8")
            response_content = engine.generate_text(prompt, ctx.get("profile", ""))
            engine.save_file(name, "visual_guide.md", response_content)

        elif step == "story":
            prompt = (PROMPT_DIR / "02_story_writer.md").read_text(encoding="utf-8")
            response_content = engine.generate_text(prompt, ctx.get("profile", ""))
            engine.save_file(name, "story_foundation.md", response_content)
            
        elif step == "memories":
            prompt = (PROMPT_DIR / "03_memory_architect.md").read_text(encoding="utf-8")
            response_content = engine.generate_text(prompt, ctx.get("story", ""))
            engine.save_file(name, "30_memories.md", response_content)

        elif step == "image_prompts":
            prompt = (PROMPT_DIR / "06_image_generator.md").read_text(encoding="utf-8")
            # Combine visual and memories
            inp = f"{ctx.get('visual', '')}\n---\n{ctx.get('memories', '')}"
            response_content = engine.generate_text(prompt, inp)
            # Clean JSON
            response_content = response_content.replace("```json", "").replace("```", "").strip()
            engine.save_file(name, "image_prompts.json", response_content)

        elif step == "generate_reference":
            # Generate only reference image for interactive editing
            prompts_json = ctx.get("image_prompts", "{}")
            data = json.loads(prompts_json)

            if "reference_portrait" not in data:
                raise HTTPException(status_code=400, detail="No reference_portrait in image_prompts")

            reference_prompt = data["reference_portrait"]["prompt"]

            img_dir = CHAR_DIR / name / "images"
            img_dir.mkdir(parents=True, exist_ok=True)

            path = img_dir / "reference.png"
            success = engine.generate_image(reference_prompt, path)

            if success:
                return {
                    "status": "completed",
                    "image_path": f"/files/{name}/images/reference.png?t={int(time.time())}",
                    "reference_prompt": reference_prompt
                }
            else:
                raise HTTPException(status_code=500, detail="Reference image generation failed")

        elif step == "generate_memories":
            # Generate all memory images with confirmed reference prompt
            prompts_json = ctx.get("image_prompts", "{}")
            data = json.loads(prompts_json)

            # Get confirmed reference prompt (user approved)
            confirmed_prompt = ctx.get("confirmed_reference_prompt", "")
            original_prompt = data.get("reference_portrait", {}).get("prompt", "")

            # Extract character description (before scene indicators)
            def extract_char_desc(prompt):
                scene_starters = [
                    "neutral expression", "looking at camera", "portrait",
                    "sitting", "standing", "leaning", "lying", "holding",
                    "walking", "running", "looking", "gazing", "in ", "at ", "on "
                ]
                prompt_lower = prompt.lower()
                min_idx = len(prompt)
                for starter in scene_starters:
                    idx = prompt_lower.find(starter)
                    if idx > 0 and idx < min_idx:
                        min_idx = idx
                if min_idx < len(prompt):
                    last_comma = prompt.rfind(",", 0, min_idx)
                    if last_comma > 0:
                        return prompt[:last_comma].strip()
                return prompt[:min_idx].rstrip(", ").strip()

            original_char_desc = extract_char_desc(original_prompt) if original_prompt else ""
            confirmed_char_desc = extract_char_desc(confirmed_prompt) if confirmed_prompt else original_char_desc

            img_dir = CHAR_DIR / name / "images"
            img_dir.mkdir(parents=True, exist_ok=True)

            results = []

            if "memories" in data:
                for m in data["memories"]:
                    original_memory_prompt = m["prompt"]
                    # Replace character description with confirmed one
                    if original_char_desc and confirmed_char_desc:
                        updated_prompt = original_memory_prompt.replace(original_char_desc, confirmed_char_desc, 1)
                    else:
                        updated_prompt = original_memory_prompt

                    num = m.get("memory_number")
                    fname = f"memory_{num:02d}.png"
                    path = img_dir / fname
                    success = engine.generate_image(updated_prompt, path)
                    results.append({
                        "type": "memory",
                        "id": num,
                        "success": success,
                        "path": f"/files/{name}/images/{fname}"
                    })

            return {"status": "completed", "images": results}

        elif step == "generate_images":
            # Legacy: generate all images at once (kept for backwards compatibility)
            prompts_json = ctx.get("image_prompts", "{}")
            data = json.loads(prompts_json)

            img_dir = CHAR_DIR / name / "images"
            img_dir.mkdir(parents=True, exist_ok=True)

            results = []

            # Reference
            if "reference_portrait" in data:
                p = data["reference_portrait"]["prompt"]
                path = img_dir / "reference.png"
                success = engine.generate_image(p, path)
                results.append({"type": "reference", "success": success, "path": f"/files/{name}/images/reference.png"})

            # Memories
            if "memories" in data:
                for m in data["memories"]:
                    p = m["prompt"]
                    num = m.get("memory_number")
                    fname = f"memory_{num:02d}.png"
                    path = img_dir / fname
                    success = engine.generate_image(p, path)
                    results.append({"type": "memory", "id": num, "success": success, "path": f"/files/{name}/images/{fname}"})

            return {"status": "completed", "images": results}

        elif step == "video_prompts":
            prompt = (PROMPT_DIR / "07_video_director.md").read_text(encoding="utf-8")
            inp = f"{ctx.get('visual', '')}\n---\n{ctx.get('image_prompts', '')}\n---\n{ctx.get('memories', '')}"
            response_content = engine.generate_text(prompt, inp)
            response_content = response_content.replace("```json", "").replace("```", "").strip()
            engine.save_file(name, "video_prompts.json", response_content)

        elif step == "generate_videos":
            # Experimental Veo
            return {"status": "skipped", "message": "Video generation is experimental and requires Veo access."}

        else:
            raise HTTPException(status_code=400, detail=f"Unknown step: {step}")

        return {"status": "completed", "output": response_content}

    except Exception as e:
        print(f"Error in step {step}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/character/{name}")
def get_character(name: str):
    """Get character state."""
    base_dir = CHAR_DIR / name
    if not base_dir.exists():
        raise HTTPException(status_code=404, detail="Character not found")

    files = {}
    for f in base_dir.glob("*"):
        if f.is_file():
            files[f.name] = f.read_text(encoding="utf-8", errors="ignore")

    return {"name": name, "files": files}

@app.post("/api/regenerate-reference")
def regenerate_reference(req: RegenerateReferenceRequest):
    """Regenerate reference image with additional instruction."""
    if not engine:
        raise HTTPException(status_code=500, detail="AI Engine not initialized")

    name = req.character_name
    current_prompt = req.current_prompt
    instruction = req.additional_instruction

    # System prompt for modifying image prompts
    modify_system_prompt = """You are an image prompt modifier.
Given an image generation prompt and a modification instruction, output ONLY the modified prompt.
Keep the same format and structure. Apply the modification naturally.
Do not add any explanation, just output the modified prompt."""

    modify_input = f"""Original prompt:
{current_prompt}

Modification instruction:
{instruction}

Modified prompt:"""

    try:
        # Use LLM to modify prompt
        updated_prompt = engine.generate_text(modify_system_prompt, modify_input).strip()

        # Generate new image
        img_dir = CHAR_DIR / name / "images"
        img_dir.mkdir(parents=True, exist_ok=True)

        path = img_dir / "reference.png"
        success = engine.generate_image(updated_prompt, path)

        if success:
            return {
                "status": "completed",
                "image_path": f"/files/{name}/images/reference.png?t={int(time.time())}",
                "updated_prompt": updated_prompt
            }
        else:
            raise HTTPException(status_code=500, detail="Image regeneration failed")

    except Exception as e:
        print(f"Error regenerating reference: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
