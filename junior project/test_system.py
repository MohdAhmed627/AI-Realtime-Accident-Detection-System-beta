#!/usr/bin/env python3
"""
Test script for AI-Powered Accident Detection System
Verifies all components are working correctly
"""

import sys
import os
import requests
import json
import time
import base64
import cv2
import numpy as np
from PIL import Image
import io

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

def test_server_connection():
    """Test if the server is running"""
    print("🔍 Testing server connection...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to run 'python app.py' first")
        return False

def test_authentication():
    """Test login functionality"""
    print("🔐 Testing authentication...")
    try:
        # Test login
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Login successful")
                return data.get("access_token")
            else:
                print(f"❌ Login failed: {data.get('message')}")
                return None
        else:
            print(f"❌ Login request failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return None

def test_accident_detection(token):
    """Test accident detection API"""
    print("🤖 Testing accident detection...")
    try:
        # Create a test image (simple colored rectangle)
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        test_image[:] = (100, 150, 200)  # Blue background
        
        # Add some shapes to simulate objects
        cv2.rectangle(test_image, (100, 100), (200, 200), (0, 255, 0), -1)  # Green rectangle
        cv2.circle(test_image, (400, 300), 50, (0, 0, 255), -1)  # Red circle
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', test_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        image_data = f"data:image/jpeg;base64,{image_base64}"
        
        # Send detection request
        detection_data = {"image": image_data}
        
        response = requests.post(
            f"{BASE_URL}/detect",
            json=detection_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Detection API working")
            print(f"   - Accident detected: {data.get('accident_detected')}")
            print(f"   - Confidence: {data.get('confidence', 0):.2f}")
            print(f"   - Vehicles detected: {data.get('vehicles_detected', 0)}")
            return True
        else:
            print(f"❌ Detection API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
        return False

def test_location_update(token):
    """Test location update functionality"""
    print("📍 Testing location update...")
    try:
        location_data = {
            "lat": 28.6139,
            "lng": 77.2090
        }
        
        response = requests.post(
            f"{BASE_URL}/update_location",
            json=location_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Location update successful")
                return True
            else:
                print("❌ Location update failed")
                return False
        else:
            print(f"❌ Location update request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Location test failed: {e}")
        return False

def test_accidents_endpoint(token):
    """Test accidents history endpoint"""
    print("📊 Testing accidents endpoint...")
    try:
        response = requests.get(
            f"{BASE_URL}/accidents",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            accidents = data.get("accidents", [])
            print(f"✅ Accidents endpoint working - {len(accidents)} records found")
            return True
        else:
            print(f"❌ Accidents endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Accidents test failed: {e}")
        return False

def test_yolo_model():
    """Test YOLOv8 model loading"""
    print("🧠 Testing YOLOv8 model...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ YOLOv8 model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ YOLOv8 model test failed: {e}")
        return False

def test_opencv():
    """Test OpenCV functionality"""
    print("👁️ Testing OpenCV...")
    try:
        # Create a simple test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[:] = (255, 0, 0)  # Blue image
        
        # Test basic OpenCV operations
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        print("✅ OpenCV working correctly")
        return True
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🚗 AI Accident Detection System - Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 7
    
    # Test 1: Server connection
    if test_server_connection():
        tests_passed += 1
    else:
        print("❌ Cannot proceed without server connection")
        return
    
    # Test 2: YOLOv8 model
    if test_yolo_model():
        tests_passed += 1
    
    # Test 3: OpenCV
    if test_opencv():
        tests_passed += 1
    
    # Test 4: Authentication
    token = test_authentication()
    if token:
        tests_passed += 1
        
        # Test 5: Accident detection
        if test_accident_detection(token):
            tests_passed += 1
        
        # Test 6: Location update
        if test_location_update(token):
            tests_passed += 1
        
        # Test 7: Accidents endpoint
        if test_accidents_endpoint(token):
            tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! System is ready for demo.")
        print("\n🌐 Access the application at: http://localhost:5000")
        print("👤 Demo accounts:")
        print("   Admin: admin / admin123")
        print("   User:  user / user123")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    run_all_tests()
