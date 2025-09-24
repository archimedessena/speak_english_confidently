#!/usr/bin/env python3
import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    # Test home page
    try:
        response = requests.get(f"{base_url}/")
        print(f"Home page: {response.status_code}")
    except Exception as e:
        print(f"Error accessing home page: {e}")
    
    # Test API endpoints
    try:
        response = requests.post(f"{base_url}/api/start_session", json={"user_id": "test_user"})
        print(f"Start session: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Session ID: {data.get(\"session_id\")}")
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    print("Testing Speak English Confidently API...")
    test_api()
