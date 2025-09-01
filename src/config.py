# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')
CACHE_DIR = os.getenv('CACHE_DIR', './cache')
MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', '5'))