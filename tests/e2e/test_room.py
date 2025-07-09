import requests

base_url = "http://localhost:8000/api/v1" 

# API GET : Get All Room
# Negative Case
def test_failed_get_all_room_with_empty_data():
    # Exec
    response = requests.get(f"{base_url}/rooms")
    data = response.json()

    # Check Default Response
    assert response.status_code == 404
    assert data['status'] == 'failed'
    assert data['message'] == 'room not found'
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data

    # Check Data
    assert 'data' not in data 

# Positive Case
def test_success_get_all_room_with_valid_data():
    # Exec
    response = requests.get(f"{base_url}/rooms")
    data = response.json()

    # Check Default Response
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'room fetched'
    list_string_object = ['message','status']
    for col in list_string_object:
        assert col in data

    # Check Data
    assert 'data' in data 
    assert isinstance(data['data'], list), f"The key 'data' should be a list"

    string_col = ['id','floor','room_name','room_dept','created_at']
    for dt in data['data']:
        for col in string_col:
            assert isinstance(dt[col], str), f"The key '{col}' should be a string"

# API Post : Create Room
# Negative Case
def test_failed_post_create_room_with_empty_room_name():
    # Payload
    payload = {
        'floor' : '9A',
        'room_name' : '',
        'room_dept' : 'IT'
    }

    # Exec
    response = requests.post(f"{base_url}/rooms", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 422
    assert data['status'] == 'failed'

    # Check Validation Message
    assert data['message'] == 'room_name invalid'

def test_failed_post_create_room_with_invalid_char_length_room_name():
    # Payload
    payload = {
        'floor' : '9A',
        'room_name' : 'Lorem ipsum dolor sit amet consectetur adipiscing elit Quisque faucibus ex sapien vitae pellentesque sem placerat',
        'room_dept' : 'IT'
    }
    
    # Exec
    response = requests.post(f"{base_url}/rooms", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 422
    assert data['status'] == 'failed'

    # Check Validation Message
    assert data['message'] == 'room_name invalid'

def test_failed_post_create_room_with_invalid_rules_room_dept():
    # Payload
    payload = {
        'floor' : '9A',
        'room_name' : 'Room A',
        'room_dept' : 'Room B'
    }

    # Exec
    response = requests.post(f"{base_url}/rooms", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 422
    assert data['status'] == 'failed'

    # Check Validation Message
    assert data['message'] == 'room_dept invalid'

# Positive Case
def test_success_post_create_room_with_valid_data():
    # Payload
    payload = {
        'floor' : '9A',
        'room_name' : 'Pantry',
        'room_dept' : 'IT'
    }

    # Exec
    response = requests.post(f"{base_url}/rooms", json=payload)
    data = response.json()

    # Check Default Response
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert isinstance(data['data'], object), f"The key 'data' should be a object"

    # Check Data
    assert data['data']['floor'] == payload['floor']
    assert data['data']['room_name'] == payload['room_name']
    assert data['data']['room_dept'] == payload['room_dept']
    assert isinstance(data['data']['id'], str), f"The key 'id' should be string"
    assert isinstance(data['data']['created_at'], str), f"The key 'created_at' should be string"
    

