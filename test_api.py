#!/usr/bin/env python3
"""
Test the web API endpoints
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test risk assessment endpoint
    try:
        response = requests.get(f"{base_url}/api/risk-assessment")
        if response.status_code == 200:
            data = response.json()
            print("✅ Risk assessment endpoint working")
            print(f"   Status: {data['status']}")
            print(f"   Number of zones: {len(data['data'])}")
            print(f"   Model accuracy: {data['model_info']['accuracy']}")
        else:
            print(f"❌ Risk assessment endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Risk assessment endpoint error: {e}")
    
    # Test model metrics endpoint
    try:
        response = requests.get(f"{base_url}/api/model-metrics")
        if response.status_code == 200:
            data = response.json()
            print("✅ Model metrics endpoint working")
            print(f"   Accuracy: {data['metrics']['accuracy']}")
            print(f"   Precision: {data['metrics']['precision']}")
            print(f"   Recall: {data['metrics']['recall']}")
        else:
            print(f"❌ Model metrics endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model metrics endpoint error: {e}")

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("Make sure the Flask API is running on localhost:5000")
    print("Run: cd web-app && python api.py")
    print()
    
    # Wait a moment for user to start the API
    time.sleep(2)
    
    test_api()
