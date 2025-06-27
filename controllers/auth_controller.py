from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request
# Configs
from configs.database import SessionLocal
# Services
from services.auth_service import service_register_user, service_login_user, service_refresh_auth_token
from models.user_model import UserCreate, UserLogin

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Controller
def controller_register_user(user: UserCreate, db: Session):
    # Validator Field
    if not isinstance(user.username, str) or not (6 < len(user.username) <= 50):
        return JSONResponse(status_code=422, content={"message": "invalid username", "status": "failed"})
    if not isinstance(user.email, str) or not (10 < len(user.email) <= 100):
        return JSONResponse(status_code=422, content={"message": "invalid email", "status": "failed"})
    if not isinstance(user.password, str) or not 6 < len(user.password):
        return JSONResponse(status_code=422, content={"message": "invalid password", "status": "failed"})

    # Service
    status_code, message = service_register_user(user.username, user.email, user.password, user.telegram_user_id, db)
    
    if status_code == 201:
        return JSONResponse(
            status_code=201,
            content={
                "message": message,
                "status": "success",
            },
        )
    else:
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "status": "failed"
            },
        )

def controller_login_user(user: UserLogin, db: Session):
    # Validator Field
    if not isinstance(user.username, str) or not (6 < len(user.username) <= 50):
        return JSONResponse(status_code=422, content={"message": "invalid username", "status": "failed"})
    if not isinstance(user.password, str) or not 6 < len(user.password):
        return JSONResponse(status_code=422, content={"message": "invalid password", "status": "failed"})
    
    # Service
    status_code, message, access_token, refresh_token = service_login_user(user.username, user.password, db)

    if status_code == 200:
        return JSONResponse(
            status_code=200,
            content={
                "message": message,
                "status": "success",
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )
    else:
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "status": "failed"
            },
        )

def controller_refresh_auth_token(request: Request):
    # Get Auth Token
    refresh_token = request.headers.get("Authorization")
    if not refresh_token or not refresh_token.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={
                "message": "invalid refresh token",
                "status": "failed",
            },
        )
    
    # Service
    status_code, message, data = service_refresh_auth_token(refresh_token)

    if status_code == 200:
        return JSONResponse(
            status_code=200,
            content={
                "message": message,
                "status": "success",
                "access_token": data
            },
        )
    else:
        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "status": "failed"
            },
        )