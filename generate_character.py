import os
import sys
import argparse
import json
import base64
import time
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import os
import sys
import argparse
import json
import base64
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import google.generativeai as genai

# Load environment variables
load_dotenv()

console = Console()

def configure_gemini():
    """Configure Google Generative AI."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] GOOGLE_API_KEY not found in .env file.")
        sys.exit(1)
    genai.configure(api_key=api_key)

def generate_response(system_prompt, user_input, model_name="gemini-3-pro-preview"):
    """Generate text response using Gemini."""
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        console.print(f"[bold red]Gemini Error:[/bold red] {e}")
        return ""

def generate_image(prompt, output_path):
    """Generate image using Gemini 3.0 Pro Image Preview."""
    try:
        # Try using Gemini 3.0 Pro Image model via generate_content
        model = genai.GenerativeModel("gemini-3-pro-image-preview")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "image/jpeg"}
        )
        
        if response.parts:
            for part in response.parts:
                if part.inline_data:
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    return True
        
        # Fallback to Imagen 3 if Gemini 3 Image fails or returns no image
        console.print("[yellow]Gemini 3 Image failed, falling back to Imagen 3...[/yellow]")
        return generate_imagen_fallback(prompt, output_path)

    except Exception as e:
        console.print(f"[dim]Gemini 3 Image Error: {e}[/dim]")
        return generate_imagen_fallback(prompt, output_path)

def generate_imagen_fallback(prompt, output_path):
    """Fallback: Generate image using Imagen 3 REST API."""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1}
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            predictions = response.json().get("predictions")
            if predictions:
                b64_image = predictions[0].get("bytesBase64Encoded")
                if b64_image:
                    with open(output_path, "wb") as f:
                        f.write(base64.b64decode(b64_image))
                    return True
        else:
            console.print(f"[red]Imagen Error {response.status_code}:[/red] {response.text}")
            return False
    except Exception as e:
        console.print(f"[bold red]Fallback Error:[/bold red] {e}")
        return False

def generate_video(image_path, prompt, output_path):
    """Generate video using Gemini API (Experimental)."""
    try:
        console.print(f"[yellow]Video generation via API Key is experimental.[/yellow]")
        # Currently no public endpoint for Veo via API Key is widely documented for simple usage.
        # We will attempt a generic generateContent with video model if possible, 
        # or skip.
        return False
    except Exception as e:
        console.print(f"[red]Veo Error:[/red] {e}")
        return False

def read_prompt(filename):
    prompt_path = Path("prompts") / filename
    if not prompt_path.exists():
        console.print(f"[bold red]Error:[/bold red] Prompt file {filename} not found.")
        sys.exit(1)
    return prompt_path.read_text(encoding="utf-8")

def save_output(character_name, filename, content):
    output_dir = Path("characters") / character_name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate AI Character using Google Gemini Ecosystem")
    parser.add_argument("--name", help="Character Name")
    parser.add_argument("--request", help="Character description")
    parser.add_argument("--images-only", action="store_true", help="Generate images only")
    parser.add_argument("--video", action="store_true", help="Generate videos (Experimental)")
    args = parser.parse_args()

    if not args.request and not args.images_only:
        console.print(Panel.fit("Gemini AI Character Generator", style="bold blue"))
        args.request = console.input("[bold green]Enter character description:[/bold green] ")

    configure_gemini()
    console.print("[dim]Using Google Gemini API[/dim]")

    character_name = args.name or "Unknown"
    context = {}

    # Define Steps
    steps = [
        {"name": "Character Design", "file": "01_character_designer.md", "out": "profile.md", "key": "profile", "in": args.request},
        {"name": "Visual Direction", "file": "05_visual_director.md", "out": "visual_guide.md", "key": "visual", "in_key": "profile"},
        {"name": "Story Foundation", "file": "02_story_writer.md", "out": "story_foundation.md", "key": "story", "in_key": "profile"},
        {"name": "Memory Creation", "file": "03_memory_architect.md", "out": "30_memories.md", "key": "memories", "in_key": "story"},
        {"name": "Image Prompts", "file": "06_image_generator.md", "out": "image_prompts.json", "key": "img_prompts", "in_keys": ["visual", "memories"], "json": True},
        {"name": "Video Prompts", "file": "07_video_director.md", "out": "video_prompts.json", "key": "vid_prompts", "in_keys": ["visual", "img_prompts", "memories"], "json": True, "video_only": True},
        {"name": "Quality Review", "file": "04_editorial_reviewer.md", "out": "review_report.md", "key": "review", "in_keys": ["profile", "story", "memories"]}
    ]

    # Load context if images-only
    if args.images_only:
        char_dir = Path("characters") / character_name
        try:
            context["profile"] = (char_dir / "profile.md").read_text(encoding="utf-8")
            context["visual"] = (char_dir / "visual_guide.md").read_text(encoding="utf-8")
            context["memories"] = (char_dir / "30_memories.md").read_text(encoding="utf-8")
            # Filter steps
            steps = [s for s in steps if s.get("json") or s.get("video_only")]
        except Exception as e:
            console.print(f"[red]Error loading files:[/red] {e}")
            return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        for step in steps:
            if step.get("video_only") and not args.video:
                continue

            task_id = progress.add_task(f"Running {step['name']}...", total=None)
            
            # Prepare Input
            system_prompt = read_prompt(step['file'])
            if "in" in step: user_input = step["in"]
            elif "in_key" in step: user_input = context[step["in_key"]]
            elif "in_keys" in step: user_input = "\n---\n".join([str(context.get(k,"")) for k in step["in_keys"]])
            
            # Generate Text
            response = generate_response(system_prompt, user_input)
            context[step["key"]] = response
            
            # Extract Name
            if step["name"] == "Character Design" and not args.name:
                for line in response.split('\n'):
                    if "Name:" in line or "이름:" in line:
                        character_name = line.split(":")[-1].strip().replace(" ", "_")
                        break
            
            # Save Text
            save_output(character_name, step["out"], response)
            progress.update(task_id, completed=50)
            console.print(f"[green]✓[/green] {step['name']} completed.")

            # Handle JSON/Images
            if step.get("json") and step["key"] == "img_prompts":
                try:
                    json_str = response.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_str)
                    context["img_prompts"] = json.dumps(data) # Store as string for next step
                    
                    img_dir = Path("characters") / character_name / "images"
                    img_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Generate Reference
                    if "reference_portrait" in data:
                        console.print("[dim]Generating Reference Portrait...[/dim]")
                        generate_image(data["reference_portrait"]["prompt"], img_dir / "reference.png")
                    
                    # Generate Memories
                    if "memories" in data:
                        for m in data["memories"]:
                            console.print(f"[dim]Generating Memory {m.get('memory_number')}...[/dim]")
                            generate_image(m["prompt"], img_dir / f"memory_{m.get('memory_number'):02d}.png")
                except Exception as e:
                    console.print(f"[red]Image Gen Failed:[/red] {e}")

            # Handle Video
            if step.get("json") and step["key"] == "vid_prompts" and args.video:
                try:
                    json_str = response.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_str)
                    
                    vid_dir = Path("characters") / character_name / "videos"
                    vid_dir.mkdir(parents=True, exist_ok=True)
                    img_dir = Path("characters") / character_name / "images"
                    
                    # Generate Reference Video
                    if "reference_portrait" in data:
                        console.print("[dim]Generating Reference Video...[/dim]")
                        generate_video(img_dir / "reference.png", data["reference_portrait"]["motion_prompt"], vid_dir / "reference.mp4")

                except Exception as e:
                    console.print(f"[red]Video Gen Failed:[/red] {e}")

    console.print(Panel.fit(f"Complete! Output: characters/{character_name}/", style="bold green"))

if __name__ == "__main__":
    main()
