from sqlalchemy.orm import Session
from fastapi import Request
# Configs
from configs.database import SessionLocal
# Services
from services.auth_service import service_register_user, service_login_user, service_refresh_auth_token, service_check_account_via_telegram
from models.users_model import UserCreate, UserLogin, UserCheckAccViaTelegram

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Controller
def controller_register_user(user: UserCreate, db: Session):
    return service_register_user(user.username, user.email, user.password, user.telegram_user_id, db)

def controller_login_user(user: UserLogin, db: Session):
    return service_login_user(user.username, user.password, db)

def controller_refresh_auth_token(request: Request, db: Session):
    return service_refresh_auth_token(request)
