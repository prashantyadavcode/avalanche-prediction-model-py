# 🏔️ Local Testing Guide for Avalanche Prediction Web App

## 🚀 Quick Start (Easiest Method)

### Option 1: Using the Python Script
```bash
python run_local.py
```

### Option 2: Using the Bash Script
```bash
./run_local.sh
```

### Option 3: Manual Setup (Step by Step)

## 📋 Manual Setup Instructions

### Step 1: Install Dependencies
```bash
cd web-app
pip install -r requirements.txt
```

### Step 2: Start the Flask API Server
```bash
# In terminal 1
cd web-app
python api.py
```
The API will be available at: `http://localhost:5000`

### Step 3: Start the Frontend Server
```bash
# In terminal 2 (new terminal window)
cd web-app
python -m http.server 8080
```
The frontend will be available at: `http://localhost:8080`

### Step 4: Open Your Browser
Navigate to: `http://localhost:8080`

## 🧪 Testing the Application

### Test API Endpoints
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test risk assessment
curl http://localhost:5000/api/risk-assessment

# Test model metrics
curl http://localhost:5000/api/model-metrics
```

### Test Frontend
1. Open `http://localhost:8080` in your browser
2. You should see:
   - Interactive map with Colorado zones
   - Color-coded risk levels
   - Model metrics (Accuracy: 92%, Precision: 86%, Recall: 88%)
   - Real-time updates every 30 seconds

## 🔧 Troubleshooting

### Common Issues:

#### 1. "Module not found" errors
```bash
# Install missing dependencies
pip install flask flask-cors pandas numpy scikit-learn
```

#### 2. "Models not found" error
```bash
# Run the setup script
python setup_web_app.py
```

#### 3. CORS errors in browser
- Make sure Flask-CORS is installed
- Check that the API is running on port 5000
- Verify the frontend is running on port 8080

#### 4. Port already in use
```bash
# Kill processes using the ports
lsof -ti:5000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

## 📊 What You Should See

### Frontend Features:
- ✅ Interactive map with 10 Colorado zones
- ✅ Color-coded risk levels (Green → Purple)
- ✅ Clickable zones with detailed popups
- ✅ Model performance metrics
- ✅ Real-time timestamp updates
- ✅ Refresh button functionality
- ✅ Professional disclaimer

### API Responses:
- ✅ Health check: `{"status": "healthy"}`
- ✅ Risk data: Array of zones with risk levels
- ✅ Model metrics: Accuracy, precision, recall

## 🎯 Expected Behavior

1. **Map Loading**: Map should load with Colorado zones
2. **Risk Colors**: Zones should be colored based on risk levels
3. **Click Interactions**: Clicking zones should show detailed information
4. **Real-time Updates**: Risk levels should update every 30 seconds
5. **Model Metrics**: Should display your actual model performance

## 🚀 Ready for Vercel Deployment

Once local testing is successful:
```bash
cd web-app
vercel --prod
```

## 📱 Testing on Mobile

The app is responsive and works on mobile devices:
- Open `http://localhost:8080` on your phone
- Test touch interactions on the map
- Verify responsive design

## 🔍 Debugging Tips

### Check Console Logs:
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API call failures

### Check Server Logs:
- Flask server logs will show in terminal
- Look for model loading messages
- Check for prediction errors

### Test Individual Components:
- Test API endpoints with curl
- Test frontend without API (will use demo data)
- Test models separately with test_models.py

---

**Happy Testing! 🎉**

Your avalanche prediction model should now be running locally with real ML predictions!
