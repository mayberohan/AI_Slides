import argparse
from dotenv import load_dotenv
import os
import re # Added import for the 're' module

# Load environment variables at the very beginning
load_dotenv()

# Correctly import all necessary components
from src.search_client import serpapi_search
from src.synthesizer import synthesize
from src.ppt_generator import create_presentation
from src.llm_client import LLMClient
from src.config import MAX_SEARCH_RESULTS
import sys

PROMPT_FILE = "prompts.md"

def _read_prompt_template(file_path, section_name):
    """Reads a specific section of the prompt template from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Use regex to find the specific section
            match = re.search(rf"{section_name}:\n(.*?)(?=\n---|\Z)", content, re.DOTALL)
            if match:
                return match.group(1).strip()
            else:
                print(f"Error: Section '{section_name}' not found in {file_path}", file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {file_path}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True, help="Presentation topic")
    parser.add_argument("--output", required=True, help="Output pptx filename")
    parser.add_argument("--template", required=True, help="PowerPoint template path")
    args = parser.parse_args()

    llm_client = LLMClient()

    print("📝 Generating optimized search query...")
    search_query_prompt_template = _read_prompt_template(PROMPT_FILE, "SEARCH_QUERY_GENERATION_PROMPT")
    search_query_prompt = search_query_prompt_template.format(topic=args.topic)
    optimized_search_query = llm_client.generate(search_query_prompt).strip()
    print(f"Generated Search Query: {optimized_search_query}")

    print("🔍 Searching web...")
    # Pass the integer MAX_SEARCH_RESULTS to the search function
    web_results = serpapi_search(optimized_search_query, num_results=MAX_SEARCH_RESULTS)
    
    # The search results are a list of dictionaries, but the synthesizer expects
    # a list of strings, so we reformat them.
    search_context = [f"{r['title']}: {r['snippet']}" for r in web_results]
    
    print("🧠 Synthesizing content via LLM...")
    structured = synthesize(args.topic, search_context, llm_client)

    print("📑 Generating PowerPoint deck...")
    create_presentation(structured, args.output, args.template)

    print(f"✅ Done! Slide deck saved to {args.output}")

if __name__ == "__main__":
    main()
