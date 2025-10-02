#!/usr/bin/env python3
"""
Simple script to start the Avalanche Prediction Web App
"""

import os
import sys
import subprocess
import time

def start_app():
    """Start the Flask application"""
    print("🏔️ Starting Avalanche Prediction Web App")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('web-app'):
        print("❌ Error: web-app directory not found!")
        print("Please run this script from the project root directory")
        return
    
    # Change to web-app directory
    os.chdir('web-app')
    
    print("🚀 Starting Flask API server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start Flask server
        subprocess.run([sys.executable, 'api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_app()
