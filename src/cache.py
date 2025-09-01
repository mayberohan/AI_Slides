import os
import json
import hashlib

CACHE_DIR = ".cache"


def _get_cache_path(key: str) -> str:
    """Generate a unique cache file path based on the key."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    hashed = hashlib.sha256(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hashed}.json")


def load_cache(key: str):
    """Load cached result if it exists."""
    path = _get_cache_path(key)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_cache(key: str, data):
    """Save result to cache."""
    path = _get_cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
