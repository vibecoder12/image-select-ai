# Image Selector API

A Flask-based REST API that uses Google Custom Search and sentence transformers to find the most relevant image for a given keyword.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)
```bash
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_custom_search_engine_id"
```

### 3. Start the API Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Test the API

#### Using curl:
```bash
curl -X POST http://localhost:5000/api/select-image \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Ormond Beach oceanfront house"}'
```

#### Using Python:
```python
import requests

response = requests.post('http://localhost:5000/api/select-image', 
                        json={'keyword': 'Ormond Beach oceanfront house'})
print(response.json())
```

#### Using the test script:
```bash
python test_api.py "your search keyword"
```

## API Endpoints

### POST /api/select-image
Select the best image for a given keyword.

**Request Body:**
```json
{
  "keyword": "search term",
  "article": "optional article text for better matching"
}
```

**Response:**
```json
{
  "success": true,
  "image_url": "https://example.com/image.jpg",
  "keyword": "search term"
}
```

### GET /api/health
Health check endpoint.

### GET /
API documentation and usage examples.

## Environment Variables
- `GOOGLE_API_KEY`: Google Custom Search API key (defaults to provided key)
- `GOOGLE_CX`: Google Custom Search Engine ID (defaults to provided CX)
- `PORT`: Server port (defaults to 5000)

## Files
- `app.py`: Flask API server
- `image_selector.py`: Core image selection logic
- `test_api.py`: Test script for API
- `requirements.txt`: Python dependencies