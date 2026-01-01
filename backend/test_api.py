#!/usr/bin/env python3
"""
Test script for BTEC Assessment Engine FastAPI backend
"""

import requests
import json

BASE_URL = "http://localhost:10000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

def test_register():
    """Test user registration"""
    print("📝 Testing user registration...")
    data = {
        "email": "test@example.com",
        "password": "test123456",
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()
    return response.json()

def test_login(email, password):
    """Test user login"""
    print("🔐 Testing user login...")
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    print()
    return result

def test_get_me(access_token):
    """Test getting current user info"""
    print("👤 Testing /me endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("BTEC Assessment Engine - API Tests")
    print("=" * 50)
    print()
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Register user
        try:
            user = test_register()
        except Exception as e:
            print(f"   ⚠️  Registration failed (user may already exist): {e}")
            print()
        
        # Test 3: Login
        login_result = test_login("test@example.com", "test123456")
        access_token = login_result.get("access_token")
        
        # Test 4: Get current user
        if access_token:
            test_get_me(access_token)
        
        print("=" * 50)
        print("✅ All tests completed!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Make sure the server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 10000")
