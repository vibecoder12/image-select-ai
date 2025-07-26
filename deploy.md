# Deploy to Render

## Quick Deploy (One-Click)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/vibecoder12/image-select-ai)

## Manual Deploy Steps

### 1. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your repository: `vibecoder12/image-select-ai`

### 2. Create Web Service
1. Click **New → Web Service**
2. Connect your GitHub repository
3. Use these settings:
   - **Name**: image-selector-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 3. Set Environment Variables
In Render dashboard, go to **Environment → Environment Variables** and add:

| Variable | Value | Description |
|----------|--------|-------------|
| `GOOGLE_API_KEY` | `your_api_key_here` | Google Custom Search API key |
| `GOOGLE_CX` | `your_cx_here` | Google Custom Search Engine ID |

### 4. Deploy
Click **Deploy** and wait for the build to complete.

## Environment Variables Setup

### Get Google API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Custom Search JSON API**
4. Create credentials (API key)

### Get Custom Search Engine ID
1. Go to [Google Custom Search Engine](https://cse.google.com/cse/)
2. Create a new search engine
3. Copy the **Search engine ID**

## API Usage

Once deployed, your API will be available at:
`https://image-selector-api.onrender.com`

### Test the deployed API:
```bash
curl -X POST https://image-selector-api.onrender.com/api/select-image \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Ormond Beach oceanfront house"}'
```

### Update frontend:
Update the API URL in `index.html` to use your Render URL:
```javascript
const apiUrl = 'https://image-selector-api.onrender.com/api/select-image';
```

## Monitoring
- **Logs**: Available in Render dashboard
- **Health check**: `/api/health`
- **Status**: Check service status in Render dashboard

## Troubleshooting
- **Build fails**: Check Python version compatibility
- **API errors**: Verify environment variables are set
- **Memory issues**: Consider upgrading Render plan