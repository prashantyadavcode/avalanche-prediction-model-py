# AI Avalanche Predictor - Render Deployment Guide

## 🚀 Deploy to Render

### Quick Deploy Steps

1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub
   - Click "New +" → "Web Service"

2. **Configure Deployment**
   - **Repository**: `prashantyadavcode/avalanche-prediction-model-py`
   - **Branch**: `main`
   - **Root Directory**: Leave empty (uses root)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Environment Variables** (Optional)
   - No environment variables required for basic functionality

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy

### 📁 Project Structure for Render

```
avalanche-prediction-model-py/
├── app.py                   # Main Flask application
├── Procfile                # Render process configuration
├── requirements.txt        # Python dependencies
├── index.html              # Main application page
├── styles.css              # Styling
├── app.js                  # Frontend JavaScript
└── README.md               # Documentation
```

### 🌐 Access Your App

After deployment, your app will be available at:
- **Main App**: `https://your-app-name.onrender.com/`
- **API Health**: `https://your-app-name.onrender.com/api/health`
- **Risk Data**: `https://your-app-name.onrender.com/api/risk-assessment`

### 🔧 Render Configuration

- **Runtime**: Python 3.9+
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Port**: Automatically assigned by Render
- **Auto-deploy**: Enabled (deploys on every push to main)

### 📊 Features

- ✅ Interactive map with Colorado backcountry zones
- ✅ Real-time avalanche risk assessment
- ✅ Machine learning model metrics (94.2% accuracy)
- ✅ Responsive design matching AI Stock Predictor
- ✅ Auto-refresh functionality
- ✅ Mobile-optimized interface

### 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5000
```

### 🔍 Troubleshooting

If deployment fails:
1. Check build logs in Render dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify `app.py` is the main Flask application
4. Check that `Procfile` contains correct start command

### 📞 Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Project Repository**: [github.com/prashantyadavcode/avalanche-prediction-model-py](https://github.com/prashantyadavcode/avalanche-prediction-model-py)
