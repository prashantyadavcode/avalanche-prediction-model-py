#!/usr/bin/env python3
"""
Local development server for the Avalanche Prediction Web App
"""

import os
import sys
import subprocess
import webbrowser
import time
from threading import Thread

def start_flask_server():
    """Start the Flask API server"""
    print("🚀 Starting Flask API server...")
    
    # Change to web-app directory
    os.chdir('web-app')
    
    # Start Flask server
    try:
        subprocess.run([sys.executable, 'api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Flask server stopped")
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")

def start_http_server():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting HTTP server for frontend...")
    
    # Change to web-app directory
    os.chdir('web-app')
    
    try:
        # Start Python HTTP server
        subprocess.run([sys.executable, '-m', 'http.server', '8080'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 HTTP server stopped")
    except Exception as e:
        print(f"❌ Error starting HTTP server: {e}")

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:8080')

def main():
    """Main function to start local development"""
    print("🏔️ Starting Avalanche Prediction Web App locally...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('web-app'):
        print("❌ Error: web-app directory not found!")
        print("Please run this script from the project root directory")
        return
    
    # Check if models exist
    if not os.path.exists('web-app/models/slab_model.pkl'):
        print("❌ Error: ML models not found!")
        print("Please run: python setup_web_app.py")
        return
    
    print("✅ All checks passed!")
    print()
    print("📋 Starting servers:")
    print("   - Flask API: http://localhost:5000")
    print("   - Frontend: http://localhost:8080")
    print()
    print("🛑 Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    # Start Flask server in a separate thread
    flask_thread = Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start HTTP server in a separate thread
    http_thread = Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Open browser
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("✅ Local development stopped")

if __name__ == "__main__":
    main()
