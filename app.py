import os
from flask import Flask, request, jsonify
from image_selector import main

app = Flask(__name__)

# Load API credentials from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyD25mLE5YiLQlzIpxjTBMPK6VeYDs3ZJ-s')
CX = os.getenv('GOOGLE_CX', '97d609ab829934caf')

@app.route('/api/select-image', methods=['POST'])
def select_image():
    """API endpoint to select the best image for a given keyword."""
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        article_text = data.get('article', keyword)  # Use keyword as fallback
        
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
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'image-selector-api'})

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return '''
    <h1>Image Selector API</h1>
    <p>POST to <code>/api/select-image</code> with JSON:</p>
    <pre>
    {
        "keyword": "your search term",
        "article": "optional article text for better matching"
    }
    </pre>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)