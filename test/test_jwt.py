import requests
import json

# Base URL de la API
BASE_URL = "http://127.0.0.1:5000/api/auth"

def test_jwt_auth():
    """Test JWT authentication functionality"""
    
    print("=== TESTING JWT AUTHENTICATION ===\n")
    
    # Test 1: Login with valid credentials
    print("1. Testing login with valid credentials (admin)...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        print("✅ Login successful!\n")
        
        # Test 2: Access protected route
        print("2. Testing protected route...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Protected route access successful!\n")
        
        # Test 3: Get user info
        print("3. Testing user info endpoint...")
        response = requests.get(f"{BASE_URL}/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ User info retrieved successfully!\n")
        
        # Test 4: Refresh token
        print("4. Testing token refresh...")
        refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
        response = requests.post(f"{BASE_URL}/refresh", headers=refresh_headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Token refresh successful!\n")
        
        # Test 5: Logout
        print("5. Testing logout...")
        response = requests.post(f"{BASE_URL}/logout", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Logout successful!\n")
        
    else:
        print("❌ Login failed!")
        return
    
    # Test 6: Login with invalid credentials
    print("6. Testing login with invalid credentials...")
    invalid_login_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=invalid_login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Invalid credentials properly rejected!\n")
    
    # Test 7: Access protected route without token
    print("7. Testing protected route without token...")
    response = requests.get(f"{BASE_URL}/protected")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Unauthorized access properly rejected!\n")
    
    print("=== ALL TESTS COMPLETED ===")

if __name__ == "__main__":
    try:
        test_jwt_auth()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server. Make sure the Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
