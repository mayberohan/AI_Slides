import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)


def ask_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    Query Gemini with a prompt and return the response text.
    """
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    return response.text
