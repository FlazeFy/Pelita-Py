from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.converter_util import model_to_dict
from controllers.auth_controller import get_db
from sqlalchemy.orm import Session
from repositories.room_repository import repository_find_all_room

def test_success_repository_find_all_room_with_no_data():
    db: Session = next(get_db()) 

    # Exec
    results = repository_find_all_room(db)

    # Assert
    assert isinstance(results, list)
    assert len(results) == 0

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
