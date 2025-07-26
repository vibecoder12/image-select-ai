# GitHub Pages Deployment Instructions

## Enable GitHub Pages

1. Go to your repository: https://github.com/vibecoder12/image-select-ai
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **Deploy from a branch**
5. Select **main** branch and **/ (root)** folder
6. Click **Save**

## Access Your Frontend

Once GitHub Pages is enabled, your frontend will be available at:
**https://vibecoder12.github.io/image-select-ai**

## How to Use

1. **Start your API server** locally:
   ```bash
   python app.py
   ```

2. **Access the frontend** at the GitHub Pages URL above

3. **Enter your API endpoint**: `http://localhost:5000/api/select-image`

4. **Enter keywords** and click "Find Best Image"

## Alternative: Deploy API to Cloud

For production use, consider deploying your API to:
- **Render** (free tier available)
- **Heroku** 
- **Railway**
- **PythonAnywhere**

Then update the API URL in the frontend to point to your deployed API.

## Current Status
✅ Repository pushed to GitHub
✅ Frontend interface created
✅ Ready for GitHub Pages deployment