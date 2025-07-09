from sqlalchemy import Column, String, DateTime, func
from configs.database import Base
from pydantic import BaseModel

class SaveRoom(BaseModel):
    floor: str
    room_name: str
    room_dept: str

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(36), primary_key=True, index=True)
    floor = Column(String(2), unique=True, nullable=False)
    room_name = Column(String(36), nullable=False)
    room_dept = Column(String(75), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())