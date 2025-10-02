#!/usr/bin/env python3
"""
Simple script to start the Avalanche Prediction Web App on a clean port
"""

import os
import sys
import subprocess
import socket

def find_free_port():
    """Find a free port to use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def start_app():
    """Start the Flask application"""
    print("🏔️ Starting Avalanche Prediction Web App")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('web-app'):
        print("❌ Error: web-app directory not found!")
        print("Please run this script from the project root directory")
        return
    
    # Find a free port
    port = find_free_port()
    
    # Change to web-app directory
    os.chdir('web-app')
    
    print(f"🚀 Starting Flask server on port {port}...")
    print(f"🌐 Frontend: http://localhost:{port}")
    print(f"📡 API: http://localhost:{port}/api/")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Modify the port in api.py temporarily
        with open('api.py', 'r') as f:
            content = f.read()
        
        # Replace port 3000 with our free port
        content = content.replace('port=3000', f'port={port}')
        
        with open('api_temp.py', 'w') as f:
            f.write(content)
        
        # Start Flask server
        subprocess.run([sys.executable, 'api_temp.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up temp file
        if os.path.exists('api_temp.py'):
            os.remove('api_temp.py')

if __name__ == "__main__":
    start_app()
