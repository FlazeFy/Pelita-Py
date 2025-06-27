from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Union
# Models
from models.user_model import User, is_username_or_email_taken
# Utils
from utils.generator_util import get_UUID

def repository_find_user_by_email_username(db: Session, username: str, email: str) -> bool:
    return is_username_or_email_taken(db, username=username, email=email)

def repository_create_user(db: Session, username: str, email: str, telegram_user_id:str, hashed_password: str) -> User:
    # Query
    db_user = User(
        id=get_UUID(),
        username=username,
        email=email,
        password=hashed_password,
        telegram_user_id=telegram_user_id,
        telegram_is_valid=False,
        created_at=datetime.utcnow()
    )

    # Exec
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def repository_find_user_by_username(db: Session, username: str) -> Union[User, None]:
    # Query
    query = select(User).where(User.username == username)

    # Exec
    result = db.execute(query).scalars()
    return result.first()
