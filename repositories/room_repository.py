from sqlalchemy import select
from sqlalchemy.orm import Session
from models.room_model import Room

def repository_find_all_room(db: Session):
    # Query
    query = (
        select(Room).order_by(
            Room.created_at.desc()
        )
    )

    # Exec
    result = db.execute(query).scalars().all()
    return result

def repository_create_room(data: Room) -> dict:
    result = None

    return result
