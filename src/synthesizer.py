import json
import re
import os
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

def synthesize(topic, search_results, llm_client):
    context = "\n".join(search_results)
    
    # Read the prompt template from the file
    prompt_template = _read_prompt_template(PROMPT_FILE, "SLIDE_GENERATION_PROMPT")

    # Format the prompt with the topic and search context
    prompt = prompt_template.format(topic=topic, context=context)

    response = llm_client.generate(prompt).strip()

    # Extract JSON string from markdown code block
    json_match = re.search(r"```json\n(.*)\n```", response, re.DOTALL)
    if not json_match:
        print(f"⚠️ Failed to extract JSON from response. Raw text: {response}", file=sys.stderr)
        print("Falling back to single summary slide.", file=sys.stderr)
        return [{"title": f"Summary: {topic}", "content": response}]

    json_string = json_match.group(1).strip()

    try:
        structured_data = json.loads(json_string)
        slides = structured_data.get("slides", [])
        
        # Reformat slides to match the expected structure for ppt_generator
        # The ppt_generator expects 'content' as a single string, but the new prompt
        # generates 'bullets' as a list. We need to convert 'bullets' to 'content'.
        formatted_slides = []
        for slide in slides:
            formatted_slide = {
                "title": slide.get("title", ""),
                "subtitle": slide.get("subtitle", ""),
                "content": "\n".join([f"- {bullet}" for bullet in slide.get("bullets", [])]),
                "notes": slide.get("notes", ""),
                "sources": slide.get("sources", [])
            }
            formatted_slides.append(formatted_slide)
        
        if not formatted_slides:
            print("⚠️ No valid slides could be parsed from JSON. Falling back to single summary slide.", file=sys.stderr)
            return [{"title": f"Summary: {topic}", "content": response}]

        return formatted_slides

    except json.JSONDecodeError as e:
        print(f"⚠️ Failed to parse JSON response: {e}. Raw text: {json_string}", file=sys.stderr)
        print("Falling back to single summary slide.", file=sys.stderr)
        return [{"title": f"Summary: {topic}", "content": response}]
