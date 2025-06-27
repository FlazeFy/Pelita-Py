from fastapi import Request

base_url = "http://localhost:8000/api/v1" 

# Negative Case
def test_failed_get_all_room_with_empty_data():
    # Exec
    response = Request.get(f"{base_url}/rooms")
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
    response = Request.get(f"{base_url}/rooms")
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
