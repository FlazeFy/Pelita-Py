import requests

base_url = "http://localhost:8000/api/v1" 

# Dummy test user
test_user = {
    "username": "testuser3454",
    "email": "testuser3454@example.com",
    "password": "test123"
}

# Positive Case
def test_register_user_success_with_valid_data():
    # Exec
    response = requests.post(f"{base_url}/auths/register", json=test_user)
    data = response.json()

    # Check Default Response
    assert response.status_code == 201
    assert data['status'] == 'success'

    # Check String Object
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'user registered successfully'

def test_login_user_success_with_valid_data():
    # Test Data
    payload = {
        "username": test_user["username"],
        "password": test_user["password"]
    }

    # Exec
    response = requests.post(f"{base_url}/auths/login", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 200
    assert data['status'] == 'success'

    # Check String Object
    list_string_object = ['message','status','refresh_token','access_token']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'user login successfully'

def test_refresh_auth_token_success_with_valid_data():
    # Test Data
    payload = {
        "username": test_user["username"],
        "password": test_user["password"]
    }

    # Exec - Login
    response = requests.post(f"{base_url}/auths/login", json=payload)
    data_login = response.json()

    # Test Data
    refresh_token = data_login['refresh_token']
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    # Exec - Login
    response = requests.post(f"{base_url}/auths/refresh", headers=headers)
    data = response.json()

    # Check String Object
    list_string_object = ['message','status','access_token']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'user token refresh'

# Negative Case
def test_register_user_failed_with_invalid_data():
    # Exec
    response = requests.post(f"{base_url}/auths/register", json= {
        "username": "tes",
        "email": "testuser@example.com",
        "password": "test123"
    })
    data = response.json()

    # Check Default Response
    assert response.status_code == 422
    assert data['status'] == 'failed'

    # Check String Object
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'invalid username'

def test_login_user_failed_with_invalid_data():
    # Exec
    response = requests.post(f"{base_url}/auths/login", json= {
        "username": "tes",
        "password": "test123"
    })
    data = response.json()

    # Check Default Response
    assert response.status_code == 422
    assert data['status'] == 'failed'

    # Check String Object
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'invalid username'

def test_refresh_auth_token_failed_with_missing_token():
    # Exec
    response = requests.post(f"{base_url}/auths/refresh")
    data = response.json()

    # Check Default Response
    assert response.status_code == 401
    assert data['status'] == 'failed'

    # Check String Object
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data
        assert isinstance(data[col], str), f"The key '{col}' should be a string"
    assert data['message'] == 'invalid refresh token'