# src/image_client.py
import os
import requests
import glob
from difflib import SequenceMatcher

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_existing_image(query, save_dir="images"):
    """Find an existing image that matches the query"""
    if not os.path.exists(save_dir):
        return None
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(save_dir, ext)))
    
    if not image_files:
        return None
    
    # Find the best matching image based on filename similarity
    best_match = None
    best_score = 0
    
    query_words = set(query.lower().split())
    
    for image_path in image_files:
        filename = os.path.splitext(os.path.basename(image_path))[0]
        
        # Calculate similarity score
        score = similarity(query, filename)
        
        # Bonus points for matching individual words
        filename_words = set(filename.lower().split())
        word_matches = len(query_words.intersection(filename_words))
        if word_matches > 0:
            score += word_matches * 0.2
        
        if score > best_score:
            best_score = score
            best_match = image_path
    
    # Only return if similarity is reasonable (> 0.3)
    if best_score > 0.3:
        print(f"✅ Found existing image: {best_match} (similarity: {best_score:.2f})")
        return best_match
    
    return None

def fetch_image(query, save_dir="images"):
    """Fetch image from Pexels API or use existing image"""
    
    # First, try to find an existing image
    existing_image = find_existing_image(query, save_dir)
    if existing_image:
        return existing_image
    
    # If no existing image and no API key, return None
    if not PEXELS_API_KEY:
        print("⚠️ No Pexels API key found and no matching existing image. Skipping image.")
        return None

    # Try to download from Pexels
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}

    try:
        response = requests.get(PEXELS_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["photos"]:
            url = data["photos"][0]["src"]["original"]
            os.makedirs(save_dir, exist_ok=True)
            safe_name = "".join(c for c in query if c.isalnum() or c in (" ", "_")).rstrip()
            path = os.path.join(save_dir, f"{safe_name}.jpg")
            
            with requests.get(url, stream=True, timeout=10) as img_response:
                img_response.raise_for_status()
                with open(path, "wb") as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✅ Image downloaded and saved to {path}")
            return path
        else:
            print(f"⚠️ No images found for query: {query}")
    except requests.exceptions.MissingSchema:
        print(f"⚠️ Pexels failed: The URL is invalid. Check the 'PEXELS_URL' variable.")
    except Exception as e:
        print(f"⚠️ Pexels failed for query '{query}': {e}")
    
    return None
