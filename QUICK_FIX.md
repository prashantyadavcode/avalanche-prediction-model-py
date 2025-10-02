# 🚀 **SOLUTION: How to Run Your Avalanche Prediction Web App**

## ❌ **The Problem**
You're getting a Spring Boot error because there are other applications running on ports 5000 and 8080.

## ✅ **The Solution**

### **Method 1: Use Port 3001 (Recommended)**

1. **Open Terminal and run:**
```bash
cd web-app
python -c "
import sys
sys.path.append('.')
from api import app
app.run(debug=True, host='0.0.0.0', port=3001)
"
```

2. **Open your browser and go to:**
```
http://localhost:3001
```

### **Method 2: Kill Conflicting Processes**

1. **Kill processes on ports 5000 and 8080:**
```bash
lsof -ti:5000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

2. **Then start normally:**
```bash
cd web-app
python api.py
```

3. **Open browser:**
```
http://localhost:3000
```

### **Method 3: Use the Clean Start Script**

```bash
python start_clean.py
```

This will automatically find a free port and start your app.

## 🧪 **Test Your App**

Once running, you should see:
- ✅ Interactive map of Colorado
- ✅ Color-coded avalanche risk zones
- ✅ Model metrics (92% accuracy, 86% precision, 88% recall)
- ✅ Real-time updates

## 🔧 **If Still Having Issues**

1. **Check what's running:**
```bash
lsof -i :3000
lsof -i :5000
lsof -i :8080
```

2. **Kill everything:**
```bash
pkill -f python
```

3. **Start fresh:**
```bash
cd web-app
python api.py
```

## 📱 **Test API Endpoints**

```bash
# Health check
curl http://localhost:3001/api/health

# Risk assessment
curl http://localhost:3001/api/risk-assessment

# Model metrics
curl http://localhost:3001/api/model-metrics
```

---

**Your app should now work perfectly! 🎉**
