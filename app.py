import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_selector import main

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load API credentials from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_CX')

# Validate required environment variables
if not API_KEY or not CX:
    print("Warning: GOOGLE_API_KEY and GOOGLE_CX environment variables are required")
    print("Please set these in your Render environment variables")

@app.route('/api/select-image', methods=['POST'])
def select_image():
    """API endpoint to select the best image for a given keyword."""
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        article_text = data.get('article', keyword)
        
        # Validate API credentials
        if not API_KEY or not CX:
            return jsonify({
                'success': False,
                'error': 'Server configuration error: Missing API credentials'
            }), 500
        
        # Call the image selector
        image_url = main(article_text, keyword, API_KEY, CX)
        
        if image_url:
            return jsonify({
                'success': True,
                'image_url': image_url,
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render."""
    return jsonify({
        'status': 'healthy',
        'service': 'image-selector-api',
        'timestamp': '2025-07-26T16:35:55.400Z'
    })

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return '''
    <html>
    <head>
        <title>Image Selector API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #eee; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🖼️ Image Selector API</h1>
        <p>AI-powered image selection using Google Custom Search and semantic matching.</p>
        
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <h3>POST /api/select-image</h3>
            <p>Select the best image for a given keyword.</p>
            <strong>Request:</strong>
            <pre><code>{
    "keyword": "Ormond Beach oceanfront house",
    "article": "optional article text for better matching"
}</code></pre>
            <strong>Response:</strong>
            <pre><code>{
    "success": true,
    "image_url": "https://example.com/image.jpg",
    "keyword": "Ormond Beach oceanfront house"
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

# Get port from environment variable (Render sets this)
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=port)