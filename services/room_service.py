from requests import Session
from repositories.room_repository import repository_find_all_room

def service_get_all_room(db: Session):
    # Repo : Find All Room
    rooms = repository_find_all_room(db)
    
    if not rooms:
        return 404, None

    return 200, rooms
