from sqlalchemy.orm import Session
from typing import Union
# Models
from models.users_model import User, is_username_or_email_taken
# Utils
from utils.generator import get_UUID

def repository_check_user_exists(db: Session, username: str, email: str) -> bool:
    return is_username_or_email_taken(db, username=username, email=email)

def repository_create_user(db: Session, username: str, email: str, telegram_user_id:str, hashed_password: str) -> User:
    db_user = User(
        id=get_UUID(),
        username=username,
        email=email,
        password=hashed_password,
        telegram_user_id=telegram_user_id,
        telegram_is_valid=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def repository_get_user_by_username(db: Session, username: str) -> Union[User, None]:
    return db.query(User).filter(User.username == username).first()
