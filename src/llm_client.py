import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai


class LLMClient:
    def __init__(self):
        # ✅ Force load .env from project root
        base_dir = Path(__file__).resolve().parents[1]
        env_path = base_dir / ".env"
        load_dotenv(dotenv_path=env_path)

        # Load Gemini API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(f"GEMINI_API_KEY not found in environment variables (looked in {env_path})")

        genai.configure(api_key=api_key)

        # Choose Gemini model (can adjust if needed)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")

    def generate(self, prompt: str) -> str:
        """
        Generate raw text output from Gemini for a given prompt.
        """
        response = self.model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text.strip()
        return ""

    def synthesize(self, topic, web_results):
        """
        Calls Gemini to generate structured slide content.
        """
        prompt = f"""
        Create a structured slide outline for a PowerPoint presentation on: {topic}.
        Use around 7-8 slides maximum.
        Each slide should have:
        - title
        - 3-4 short bullet points
        Keep text concise for presentation.
        Web results for reference: {web_results}
        """

        raw_text = self.generate(prompt)

        # Gemini response is plain text, so we parse into slide structure
        slides = []
        if raw_text:
            raw = raw_text.split("\n")
            current_slide = {"title": "", "content": []}

            for line in raw:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):  # Treat headings as slide titles
                    if current_slide["title"]:
                        slides.append(current_slide)
                    current_slide = {"title": line.lstrip("#").strip(), "content": []}
                elif line.startswith("-"):
                    current_slide["content"].append(line.lstrip("-").strip())

            if current_slide["title"]:  # Add last slide
                slides.append(current_slide)

        return slides
