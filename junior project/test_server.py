#!/usr/bin/env python3
"""
Test if the server is running and responding
"""

import requests
import time

def test_server():
    print("🧪 Testing if server is running...")
    
    # Wait a moment for server to start
    time.sleep(3)
    
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding!")
            print("🌐 Open http://localhost:5000 in your browser")
            print("👤 Login with: admin / admin123")
            return True
        else:
            print(f"⚠️ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running")
        return False

if __name__ == "__main__":
    test_server()
