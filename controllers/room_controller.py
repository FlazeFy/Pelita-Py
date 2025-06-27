from requests import Session
from services.room_service import service_get_all_room
from utils.converter_util import format_list_of_dict_with_datetime, model_to_dict
from utils.response_util import build_response

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