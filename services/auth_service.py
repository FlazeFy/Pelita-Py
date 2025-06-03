from passlib.context import CryptContext
from datetime import timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Request
import jwt
# Utils
from utils.jwt import create_auth_token, decode_auth_token
# Repositories
from repositories.auth_repository import repository_check_user_exists, repository_create_user, repository_get_user_by_username
from repositories.user_repository import repository_get_user_by_username_telegram_id
# Models
from models.users_model import UserCheckAccViaTelegram

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def service_register_user(username: str, email: str, password: str, telegram_user_id:str, db: Session):
    if repository_check_user_exists(db, username=username, email=email):
        return JSONResponse(
            status_code=409,
            content={
                "message": "the email or username already been used. try using other",
                "status": "failed",
            },
        )
    hashed_password = pwd_context.hash(password)
    repository_create_user(db, username, email, telegram_user_id, hashed_password)
    return JSONResponse(
        status_code=201,
        content={"message": "user registered successfully", "status": "success"},
    )


def service_login_user(username: str, password: str, db: Session):
    db_user = repository_get_user_by_username(db, username)
    if not db_user or not pwd_context.verify(password, db_user.password):
        return JSONResponse(
            status_code=401,
            content={"message": "invalid username or password", "status": "failed"},
        )
    data = {"sub": db_user.username, "id": db_user.id}
    access_token = create_auth_token(data, expires_delta=timedelta(hours=1))
    refresh_token = create_auth_token(data, expires_delta=timedelta(hours=7))
    return JSONResponse(
        status_code=200,
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "user login successfully",
            "status": "success",
        },
    )

def service_refresh_auth_token(request: Request):
    try:
        refresh_token = request.headers.get("Authorization")
        if not refresh_token or not refresh_token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"message": "invalid refresh token", "status": "failed"},
            )
        refresh_token = refresh_token.split(" ")[1]
        payload = decode_auth_token(refresh_token)
        username = payload.get("sub")
        data = payload.get("id")
        if not username:
            return JSONResponse(
                status_code=401,
                content={"message": "invalid token", "status": "failed"},
            )
        new_access_token = create_auth_token(
            {"sub": username,  "id": data.id}, expires_delta=timedelta(hours=1)
        )
        return JSONResponse(
            status_code=200,
            content={
                "access_token": new_access_token,
                "message": "user token refresh",
                "status": "success",
            },
        )
    except (jwt.ExpiredSignatureError, jwt.PyJWTError):
        return JSONResponse(
            status_code=401,
            content={"message": "invalid token", "status": "failed"},
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"message": "something went wrong", "status": "failed"},
        )