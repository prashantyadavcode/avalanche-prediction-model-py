#!/bin/bash
# Simple script to run the web app locally

echo "🏔️ Starting Avalanche Prediction Web App locally..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "web-app" ]; then
    echo "❌ Error: web-app directory not found!"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if models exist
if [ ! -f "web-app/models/slab_model.pkl" ]; then
    echo "❌ Error: ML models not found!"
    echo "Please run: python setup_web_app.py"
    exit 1
fi

echo "✅ All checks passed!"
echo ""
echo "📋 Starting servers:"
echo "   - Flask API: http://localhost:5000"
echo "   - Frontend: http://localhost:8080"
echo ""
echo "🛑 Press Ctrl+C to stop both servers"
echo "=================================================="

# Start Flask API server in background
cd web-app
python api.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 3

# Start HTTP server for frontend
python -m http.server 8080 &
HTTP_PID=$!

# Wait for user to stop
wait

# Cleanup
echo ""
echo "🛑 Shutting down servers..."
kill $FLASK_PID 2>/dev/null
kill $HTTP_PID 2>/dev/null
echo "✅ Local development stopped"
