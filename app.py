import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# DEBUG: Set credentials directly for troubleshooting
os.environ["GOOGLE_API_KEY"] = "AIzaSyD25mLE5YiLQlzIpxjTBMPK6VeYDs3ZJ-s"
os.environ["GOOGLE_CX"] = "97d609ab829934caf"

app = Flask(__name__)
CORS(app)

# Load API credentials from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')
HF_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

@app.route('/api/select-image', methods=['POST'])
def select_image():
    """API endpoint using Hugging Face for semantic matching."""
    try:
        print("Raw request data:", request.data)
        data = request.get_json()
        print("Parsed JSON:", data)
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        article_text = data.get('article', keyword)
        
        # Validate API credentials
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return jsonify({
                'success': False,
                'error': 'Missing Google API credentials'
            }), 500
        
        # Get images from Google Custom Search
        images = get_images_from_google(keyword)
        
        if not images:
            return jsonify({
                'success': False,
                'error': 'No images found',
                'keyword': keyword
            }), 404
        
        # Use Hugging Face for semantic matching
        best_image = select_best_image(article_text, images)
        
        if best_image:
            return jsonify({
                'success': True,
                'image_url': best_image,
                'keyword': keyword
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No suitable image found',
                'keyword': keyword
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_images_from_google(query, num=10):
    """Get images from Google Custom Search API."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "searchType": "image",
        "num": num,
        "imgType": "photo"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    images = []
    for item in data.get("items", []):
        images.append({
            "link": item.get("link"),
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "contextLink": item.get("image", {}).get("contextLink", "")
        })
    
    return images

def select_best_image(article_text, image_items):
    """Use Hugging Face API for semantic matching."""
    if not image_items:
        return None
    
    # Prepare text for embedding
    article_text = article_text.lower()
    
    # Create metadata for each image
    best_score = -1
    best_url = None
    
    for item in image_items:
        # Create metadata text
        meta = f"{item['title']} {item['snippet']}".lower()
        
        # Use Hugging Face for similarity
        similarity = get_similarity_score(article_text, meta)
        
        if similarity > best_score:
            best_score = similarity
            best_url = item["link"]
    
    return best_url

def get_similarity_score(text1, text2):
    """Get similarity score using Hugging Face API."""
    url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": {
            "source_sentence": text1,
            "sentences": [text2]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Return the similarity score
        return result[0] if isinstance(result, list) and result else 0.5
    
    except Exception as e:
        # Fallback to simple keyword matching
        return simple_keyword_match(text1, text2)

def simple_keyword_match(text1, text2):
    """Simple keyword matching as fallback."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1.intersection(words2)
    return len(intersection) / max(len(words1), len(words2))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'image-selector-api-hf',
        'timestamp': '2025-07-26T17:38:41.150Z'
    })

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return '''
    <html>
    <head>
        <title>Hugging Face Image Selector API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #eee; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🤗 Hugging Face Image Selector API</h1>
        <p>AI-powered image selection using Google Custom Search + Hugging Face embeddings.</p>
        
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <h3>POST /api/select-image</h3>
            <p>Select the best image using Hugging Face semantic matching.</p>
            <strong>Request:</strong>
            <pre><code>{
    "keyword": "sunset beach",
    "article": "optional article text for better matching"
}</code></pre>
            <strong>Response:</strong>
            <pre><code>{
    "success": true,
    "image_url": "https://example.com/image.jpg",
    "keyword": "sunset beach"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/health</h3>
            <p>Health check endpoint.</p>
        </div>
        
        <h2>Environment Variables</h2>
        <ul>
            <li><code>GOOGLE_API_KEY</code> - Google Custom Search API key</li>
            <li><code>GOOGLE_CX</code> - Google Custom Search Engine ID</li>
            <li><code>HUGGING_FACE_API_KEY</code> - Hugging Face API key (optional, uses provided key)</li>
        </ul>
    </body>
    </html>
    '''

# Get port from environment variable
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)