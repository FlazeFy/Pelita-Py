import requests

base_url = "http://localhost:8000/api/v1" 

def helper_test_login(username: str, password: str):
    # Test Data
    payload = {
        "username": username,
        "password": password
    }

    # Exec
    response = requests.post(f"{base_url}/auth/login", json=payload)
    data = response.json()
    return data['access_token']