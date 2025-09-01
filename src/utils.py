import json


def pretty_json(obj) -> str:
    """Return pretty-printed JSON string."""
    return json.dumps(obj, indent=2, ensure_ascii=False)


def clean_text(text: str) -> str:
    """Clean up text by stripping whitespace and fixing newlines."""
    if not text:
        return ""
    return " ".join(text.strip().split())
