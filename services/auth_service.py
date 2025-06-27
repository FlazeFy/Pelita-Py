import bcrypt
from passlib.context import CryptContext
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Request
import jwt
# Repositories
from repositories.auth_repository import repository_find_user_by_email_username, repository_create_user, repository_find_user_by_username
# Utils
from utils.jwt_util import create_auth_token, decode_auth_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def service_register_user(username: str, email: str, password: str, telegram_user_id:str, db: Session):
    try:
        # Repo : Find User By Email and Username
        if repository_find_user_by_email_username(db, username=username, email=email):
            return 409, "the email or username already been used. try using other"
        
        # Hash Password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Repo : Create User
        repository_create_user(db, username, email, telegram_user_id, hashed_password)
        
        return 201, "user registered successfully"
    except Exception as err:
        return 500, "something went wrong"

def service_login_user(username: str, password: str, db: Session):
    try:
        # Repo : Find User By Username
        db_user = repository_find_user_by_username(db, username)

        # Validate Password
        if not db_user or not bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')):
            return 401, "invalid username or password", None, None
        
        # Create Auth Token
        data = {"sub": db_user.username, "id": db_user.id}
        access_token = create_auth_token(data, expires_delta=timedelta(hours=24))
        refresh_token = create_auth_token(data, expires_delta=timedelta(days=7))

        return 200, "user login successfully", access_token, refresh_token
    except Exception as err:
        return 500, err.args, None, None

def service_refresh_auth_token(refresh_token: str):
    try:
        # Decode Token
        refresh_token = refresh_token.split(" ")[1]
        payload = decode_auth_token(refresh_token)
        username = payload.get("sub")
        data = payload.get("id")

        if not username:
            return 401, "invalid token", None
        
        # Create Auth Token
        new_access_token = create_auth_token(
            {"sub": username,  "id": data}, expires_delta=timedelta(days=7)
        )

        return 200, "user token refresh", new_access_token
    except (jwt.ExpiredSignatureError, jwt.PyJWTError):
        return 401, "invalid token", None
    except Exception as err:
        return 500, "something went wrong", None