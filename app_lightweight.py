import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API credentials from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

# Hugging Face API for embeddings (optional, lightweight alternative)
HF_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

@app.route('/api/select-image', methods=['POST'])
def select_image():
    """Lightweight API endpoint to select the best image for a given keyword."""
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        article_text = data.get('article', keyword)
        
        # Validate API credentials
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return jsonify({
                'success': False,
                'error': 'Server configuration error: Missing API credentials'
            }), 500
        
        # Get images from Google Custom Search
        images = get_images_from_google(keyword)
        
        if not images:
            return jsonify({
                'success': False,
                'error': 'No images found',
                'keyword': keyword
            }), 404
        
        # Simple selection based on keyword relevance
        best_image = select_best_image_simple(article_text, images)
        
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

def select_best_image_simple(article_text, images):
    """Simple selection based on keyword matching."""
    if not images:
        return None
    
    # Simple keyword matching
    keywords = article_text.lower().split()
    best_score = 0
    best_image = None
    
    for image in images:
        score = 0
        text = f"{image['title']} {image['snippet']}".lower()
        
        # Count keyword matches
        for keyword in keywords:
            if keyword in text:
                score += 1
        
        if score > best_score:
            best_score = score
            best_image = image['link']
    
    # Fallback to first image if no good match
    return best_image or images[0]['link']

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'image-selector-api-lightweight',
        'timestamp': '2025-07-26T17:27:48.966Z'
    })

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return '''
    <html>
    <head>
        <title>Lightweight Image Selector API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #eee; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🖼️ Lightweight Image Selector API</h1>
        <p>Fast, lightweight API using Google Custom Search without heavy ML libraries.</p>
        
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <h3>POST /api/select-image</h3>
            <p>Select the best image for a given keyword using simple keyword matching.</p>
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
        </ul>
    </body>
    </html>
    '''

# Get port from environment variable
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)