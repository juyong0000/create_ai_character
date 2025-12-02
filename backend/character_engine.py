import os
import json
import base64
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class CharacterEngine:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        genai.configure(api_key=self.api_key)
        
        # Models
        self.text_model_name = "gemini-3-pro-preview"
        self.image_model_name = "gemini-3-pro-image-preview"

    def generate_text(self, system_prompt, user_input):
        """Generate text using Gemini 3.0 Pro."""
        try:
            model = genai.GenerativeModel(
                model_name=self.text_model_name,
                system_instruction=system_prompt
            )
            response = model.generate_content(user_input)
            return response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            return f"Error: {e}"

    def generate_image(self, prompt, output_path):
        """Generate image using Gemini 3.0 Pro Image (with fallback)."""
        try:
            # Try Gemini 3 Image
            model = genai.GenerativeModel(self.image_model_name)
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
            
            # Fallback
            return self._generate_imagen_fallback(prompt, output_path)
        except Exception as e:
            print(f"Gemini Image Error: {e}")
            return self._generate_imagen_fallback(prompt, output_path)

    def _generate_imagen_fallback(self, prompt, output_path):
        """Fallback to Imagen 3 REST API."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={self.api_key}"
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
            return False
        except Exception as e:
            print(f"Imagen Fallback Error: {e}")
            return False

    def generate_video(self, image_path, prompt, output_path):
        """Generate video using Veo (Placeholder/Experimental)."""
        # Note: Actual Veo API implementation depends on specific endpoint availability
        # For now, we return False or a mock if needed.
        # Ideally, this would use Vertex AI or GenAI video endpoints.
        return False

    def save_file(self, character_name, filename, content):
        """Save content to character directory."""
        base_dir = Path("characters") / character_name
        base_dir.mkdir(parents=True, exist_ok=True)
        file_path = base_dir / filename
        
        if isinstance(content, str):
            file_path.write_text(content, encoding="utf-8")
        else:
            # Assume bytes or similar if needed
            pass
        return str(file_path)

    def load_file(self, character_name, filename):
        """Load content from character directory."""
        file_path = Path("characters") / character_name / filename
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None
