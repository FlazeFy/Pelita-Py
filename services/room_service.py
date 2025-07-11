from requests import Session

# Model
from models.room_model import SaveRoom
# Repository
from repositories.room_repository import repository_find_all_room, repository_create_room, repository_delete_room_by_id

def service_get_all_room(db: Session):
    # Repo : Find All Room
    rooms = repository_find_all_room(db)
    
    if not rooms:
        return 404, None

    return 200, rooms

def service_create_room(data: SaveRoom):
    # Repo : Create Room
    room = repository_create_room(data)

    if not room: 
        return 500, None
    
    return 201, room

def service_delete_room_by_id(room_id: str):
    # Repo : Delete Room By Id
    return repository_delete_room_by_id(room_id)