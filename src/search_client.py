import os
import requests
from dotenv import load_dotenv

load_dotenv()


def serpapi_search(query: str, num_results: int = 5):
    """
    Return a list of dicts: {title, snippet, link}.
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("⚠️ SERPAPI_KEY not set. Returning empty results.")
        return []

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }
    res = requests.get(url, params=params)
    data = res.json()

    results = []
    if "organic_results" in data:
        for item in data["organic_results"][:num_results]:
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })
    return results
