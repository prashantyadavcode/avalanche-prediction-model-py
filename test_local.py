#!/usr/bin/env python3
"""
Simple local testing script for the Avalanche Prediction Web App
This script will work even if the ML models can't be loaded due to version issues
"""

import os
import subprocess
import sys
import time
import webbrowser
from threading import Thread

def check_setup():
    """Check if everything is set up correctly"""
    print("🔍 Checking setup...")
    
    # Check if web-app directory exists
    if not os.path.exists('web-app'):
        print("❌ web-app directory not found!")
        return False
    
    # Check if models exist
    if not os.path.exists('web-app/models/slab_model.pkl'):
        print("⚠️ ML models not found - will use demo mode")
    else:
        print("✅ ML models found")
    
    # Check if main files exist
    required_files = ['web-app/index.html', 'web-app/styles.css', 'web-app/script.js', 'web-app/api.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            return False
    
    print("✅ All required files found")
    return True

def start_flask_api():
    """Start the Flask API server"""
    print("🚀 Starting Flask API server on http://localhost:5000")
    
    try:
        os.chdir('web-app')
        subprocess.run([sys.executable, 'api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Flask API server stopped")
    except Exception as e:
        print(f"❌ Error starting Flask API: {e}")

def start_frontend_server():
    """Start the frontend HTTP server"""
    print("🌐 Starting frontend server on http://localhost:8080")
    
    try:
        os.chdir('web-app')
        subprocess.run([sys.executable, '-m', 'http.server', '8080'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")

def open_browser():
    """Open browser after servers start"""
    time.sleep(5)  # Wait for servers to start
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:8080')

def main():
    """Main function"""
    print("🏔️ Avalanche Prediction Web App - Local Testing")
    print("=" * 60)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup check failed. Please fix the issues above.")
        return
    
    print("\n📋 Starting local development servers...")
    print("   - Flask API: http://localhost:5000")
    print("   - Frontend: http://localhost:8080")
    print("\n🛑 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    # Start Flask API in background thread
    flask_thread = Thread(target=start_flask_api, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    # Start frontend server in background thread
    frontend_thread = Thread(target=start_frontend_server, daemon=True)
    frontend_thread.start()
    
    # Open browser
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("✅ Local testing stopped")

if __name__ == "__main__":
    main()
