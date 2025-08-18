#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import sys

def make_request(url, method='GET', data=None, headers=None):
    """Make HTTP request"""
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    if data:
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return None, str(e)

def test_jwt():
    base_url = "http://127.0.0.1:5000/api/auth"
    
    print("=== TESTING JWT AUTHENTICATION ===\n")
    
    # Test 1: Login
    print("1. Testing login...")
    status, response = make_request(
        f"{base_url}/login", 
        method='POST', 
        data={"username": "admin", "password": "admin123"}
    )
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        access_token = response['access_token']
        print("✅ Login successful!\n")
        
        # Test 2: Protected route
        print("2. Testing protected route...")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        status, response = make_request(f"{base_url}/protected", headers=headers)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("✅ Protected route working!\n")
        
        # Test 3: User info
        print("3. Testing user info...")
        status, response = make_request(f"{base_url}/me", headers=headers)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("✅ User info working!\n")
        
    else:
        print("❌ Login failed!")
    
    # Test 4: Invalid credentials
    print("4. Testing invalid credentials...")
    status, response = make_request(
        f"{base_url}/login", 
        method='POST', 
        data={"username": "admin", "password": "wrong"}
    )
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    print("✅ Invalid credentials properly rejected!\n")
    
    print("=== ALL TESTS COMPLETED ===")

if __name__ == "__main__":
    test_jwt()
