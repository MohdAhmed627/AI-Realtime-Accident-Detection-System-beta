#!/usr/bin/env python3
"""
Debug script to test login functionality
"""

import requests
import json

def test_login():
    print("🔍 Testing login functionality...")
    
    # Test login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                token = data.get('access_token')
                print(f"✅ Login successful!")
                print(f"Token: {token[:50]}...")
                
                # Test dashboard access
                print("\n🔍 Testing dashboard access...")
                dashboard_response = requests.get(
                    'http://localhost:5000/dashboard',
                    headers={'Authorization': f'Bearer {token}'}
                )
                print(f"Dashboard Status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    print("✅ Dashboard accessible!")
                else:
                    print(f"❌ Dashboard error: {dashboard_response.text}")
            else:
                print(f"❌ Login failed: {data.get('message')}")
        else:
            print(f"❌ Login request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
