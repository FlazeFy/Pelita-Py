from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from configs.database import Base
from sqlalchemy.orm import Session

# Auth Schema
class UserCreate(BaseModel):
    username: str
    password: str
    telegram_user_id: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str
    
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telegram_user_id = Column(String(36), unique=True, nullable=True)
    telegram_is_valid = Column(Boolean, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

def is_username_or_email_taken(db: Session, username: str = None, email: str = None) -> bool:
    if not username and not email:
        return True

    if username:
        if db.query(User).filter(User.username == username).first():
            return True

    if email:
        if db.query(User).filter(User.email == email).first():
            return True

    return False
