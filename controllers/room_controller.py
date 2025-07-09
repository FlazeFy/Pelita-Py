from requests import Session

# Config
from configs.const import ROOM_DEPT_RULES
# Model
from models.room_model import SaveRoom
# Services
from services.room_service import service_get_all_room, service_create_room
# Utils
from utils.converter_util import format_list_of_dict_with_datetime, model_to_dict
from utils.response_util import build_response
from utils.validator_util import validate_target_in_rules, validate_char_length

def controller_get_all_room(db: Session):
    # Service : Get All Room
    status_code, data = service_get_all_room(db)
    list_datetime_col = ['created_at']
    data_list_final = format_list_of_dict_with_datetime(data, list_datetime_col)

    return build_response(
        status_code, 
        "success" if status_code == 200 else "failed", 
        "room", 
        "get" if status_code == 200 else "not found", 
        data_list_final
    )

def controller_post_create_room(data: SaveRoom):
    # Validator Lenght
    if not validate_char_length(data.floor, 1, 2):
        return build_response(422, "failed", "floor", "invalid", None)
    if not validate_char_length(data.room_name, 2, 36):
        return build_response(422, "failed", "room_name", "invalid", None)
    if not validate_char_length(data.room_dept, 2, 75):
        return build_response(422, "failed", "room_dept", "invalid", None)

    # Validator Rules
    if not validate_target_in_rules(data.room_dept, ROOM_DEPT_RULES):
        return build_response(422, "failed", "room_dept", "invalid", None)
    
    # Service : Create Room
    status_code, data = service_create_room(data)
    list_datetime_col = ['created_at']
    data_final = format_list_of_dict_with_datetime(data, list_datetime_col)

    return build_response(
        status_code,
        "success" if status_code == 201 else "failed", 
        "room",
        "post",
        data_final
    )