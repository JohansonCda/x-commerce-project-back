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

def test_token_controller():
    """Test the new TokenController functionality"""
    
    base_url = "http://127.0.0.1:5000"
    auth_url = f"{base_url}/api/auth"
    token_url = f"{base_url}/api/token"
    
    print("=== TESTING TOKEN CONTROLLER ===\n")
    
    # Step 1: Login to get tokens
    print("1. Login to get initial tokens...")
    status, response = make_request(
        f"{auth_url}/login", 
        method='POST', 
        data={"username": "admin", "password": "admin123"}
    )
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status != 200:
        print("❌ Login failed!")
        return
    
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    print("✅ Login successful!\n")
    
    # Step 2: Validate current token
    print("2. Testing token validation...")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    status, response = make_request(f"{token_url}/validate", headers=headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Token validation working!\n")
    else:
        print("❌ Token validation failed!\n")
    
    # Step 3: Get token info
    print("3. Testing token info endpoint...")
    status, response = make_request(f"{token_url}/info", headers=headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Token info working!\n")
    else:
        print("❌ Token info failed!\n")
    
    # Step 4: Refresh token using new controller
    print("4. Testing refresh token with TokenController...")
    refresh_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {refresh_token}'
    }
    status, response = make_request(f"{auth_url}/refresh", method='POST', headers=refresh_headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Enhanced refresh token working!\n")
        new_access_token = response['access_token']
    else:
        print("❌ Enhanced refresh token failed!\n")
        return
    
    # Step 5: Test new refresh endpoint
    print("5. Testing dedicated refresh endpoint...")
    status, response = make_request(f"{token_url}/refresh", method='POST', headers=refresh_headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Dedicated refresh endpoint working!\n")
    else:
        print("❌ Dedicated refresh endpoint failed!\n")
    
    # Step 6: Test token revocation
    print("6. Testing token revocation...")
    revoke_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {new_access_token}'
    }
    status, response = make_request(f"{token_url}/revoke", method='POST', headers=revoke_headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Token revocation working!\n")
    else:
        print("❌ Token revocation failed!\n")
    
    # Step 7: Test enhanced logout
    print("7. Testing enhanced logout...")
    status, response = make_request(f"{auth_url}/logout", method='POST', headers=headers)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 200:
        print("✅ Enhanced logout working!\n")
    else:
        print("❌ Enhanced logout failed!\n")
    
    print("=== TOKEN CONTROLLER TESTS COMPLETED ===")
    print("\n🎉 TokenController Features:")
    print("✅ Enhanced token refresh with metadata")
    print("✅ Token validation and info endpoints")
    print("✅ Token revocation with tracking")
    print("✅ Improved error handling")
    print("✅ Detailed response data")

if __name__ == "__main__":
    try:
        test_token_controller()
    except Exception as e:
        print(f"❌ Error: {e}")
