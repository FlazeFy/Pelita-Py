from datetime import datetime
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session

# Configs
from configs.database import engine
# Model
from models.room_model import Room, SaveRoom
# Util
from utils.generator_util import get_UUID

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

def repository_create_room(data: SaveRoom) -> dict:
    room_id = get_UUID()
    created_at = datetime.utcnow()

    # Query
    query = insert(Room).values(
        id = room_id,
        floor = data.floor,
        room_name = data.room_name,
        room_dept = data.room_dept,
        created_at = created_at
    )

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            # Exec
            result = conn.execute(query)
            trans.commit()
            
            if result.rowcount > 0:
                response_data = data.dict()
                response_data.update({
                    "id": room_id,
                    "created_at": created_at.isoformat()
                })

                return response_data
        except Exception:
            trans.rollback()
            raise

def repository_delete_room_by_id(room_id: str) -> bool:
    query = delete(Room).where(
        Room.id == room_id
    )

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(query)
            trans.commit()
            return result.rowcount > 0
        except Exception:
            trans.rollback()
            raise
