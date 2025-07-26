import requests
from sentence_transformers import SentenceTransformer, util

def get_image_results(api_key, cx, query, num=10):
    """
    Query Google Custom Search API for images.
    Returns a list of image result dicts.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image",
        "num": num,
        "imgType": "photo"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("items", [])

def filter_image_urls(items):
    """
    Filter image results to only include direct image URLs with valid extensions.
    """
    valid_exts = (".jpg", ".jpeg", ".png", ".webp")
    filtered = []
    for item in items:
        link = item.get("link", "")
        if link.lower().endswith(valid_exts):
            filtered.append(item)
    return filtered

def select_best_image(article_text, image_items):
    """
    Select the image whose metadata is most semantically similar to the article.
    Uses sentence-transformers for embeddings and cosine similarity.
    """
    if not image_items:
        return None

    model = SentenceTransformer("all-MiniLM-L6-v2")
    article_emb = model.encode(article_text, convert_to_tensor=True)

    best_score = -1
    best_url = None

    for item in image_items:
        meta = " ".join([
            item.get("title", ""),
            item.get("snippet", ""),
            item.get("image", {}).get("contextLink", "")
        ])
        meta_emb = model.encode(meta, convert_to_tensor=True)
        score = util.pytorch_cos_sim(article_emb, meta_emb).item()
        if score > best_score:
            best_score = score
            best_url = item["link"]

    return best_url

def main(article_text, keyword, api_key, cx):
    image_items = get_image_results(api_key, cx, keyword)
    filtered_items = filter_image_urls(image_items)
    best_image_url = select_best_image(article_text, filtered_items)
    return best_image_url

if __name__ == "__main__":
    # Using provided credentials and keyword
    ARTICLE = "Ormond Beach oceanfront house"
    KEYWORD = "Ormond Beach oceanfront house"
    API_KEY = "AIzaSyD25mLE5YiLQlzIpxjTBMPK6VeYDs3ZJ-s"
    CX = "97d609ab829934caf"
    print(main(ARTICLE, KEYWORD, API_KEY, CX))
