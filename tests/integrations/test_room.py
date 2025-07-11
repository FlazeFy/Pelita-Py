from datetime import datetime
import sys
import os
from uuid import uuid4
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from sqlalchemy.orm import Session

# Repository
from repositories.room_repository import repository_find_all_room, repository_create_room, repository_delete_room_by_id
# Controller
from controllers.auth_controller import get_db
# Utils
from utils.converter_util import model_to_dict
# Model 
from models.room_model import SaveRoom

# Repo Find All Room
# Positive Case
def test_success_repository_find_all_room_with_no_data():
    db: Session = next(get_db()) 

    # Exec
    results = repository_find_all_room(db)

    # Assert
    assert isinstance(results, list)
    assert len(results) == 0

# Negative Case
def test_success_repository_find_all_room_with_valid_data():
    db: Session = next(get_db()) 

    # Exec
    results = repository_find_all_room(db)

    # Assert
    assert isinstance(results, list)
    assert len(results) > 0

    # Validate Model
    string_col = ['id','floor','room_name','room_dept']
    for dt in results:
        dt_dict = model_to_dict(dt)
        for col in string_col:
            print(dt_dict)
            assert isinstance(dt_dict[col], str), f"The key '{col}' should be a string"
        assert isinstance(dt_dict['created_at'], datetime), f"The key 'created_at' should be a datetime"

# Repo Create Room
# Positive Case
@pytest.mark.asyncio
async def test_success_repository_create_room_with_valid_data():
    # Test Data
    payload = SaveRoom(
        floor = "4",
        room_name = "Room A",
        room_dept = "IT"
    )

    # Exec
    result = repository_create_room(payload)

    # Assert 
    assert isinstance(result, dict)
    assert result['floor'] == payload.floor
    assert result['room_name'] == payload.room_name
    assert result['room_dept'] == payload.room_dept
    assert isinstance(result['id'], str), f"The key 'id' should be string"
    assert isinstance(result['created_at'], str), f"The key 'created_at' should be string"

# Negative Case
@pytest.mark.asyncio
async def test_failed_repository_create_room_with_invalid_data():
    # Test Data
    payload = SaveRoom(
        floor = "4",
        room_name = "Lorem ipsum dolor sit amet consectetur adipiscing elit Quisque faucibus ex sapien vitae pellentesque sem placerat",
        room_dept = "IT"
    )

    # Exec & Assert
    with pytest.raises(Exception):
        repository_create_room(payload)

# Repo Delete Room By ID
# Positive Case
@pytest.mark.asyncio
async def test_success_repository_delete_room_by_id_with_valid_id():
    payload = SaveRoom(
        floor="2",
        room_name="Temp Room",
        room_dept="QA"
    )

    # Repo Create Room
    created_room = repository_create_room(payload)
    room_id = created_room['id']

    # Repo Delete Room
    deleted = repository_delete_room_by_id(room_id)

    assert deleted is True

# Negative Case
@pytest.mark.asyncio
async def test_failed_repository_delete_room_by_id_with_invalid_id():
    random_id = str(uuid4())
    deleted = repository_delete_room_by_id(random_id)

    assert deleted is False

@pytest.mark.asyncio
async def test_failed_repository_delete_room_by_id_with_invalid_id_type():
    with pytest.raises(Exception):
        repository_delete_room_by_id(12345)

