import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_auth_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({
        "exp": expire
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_auth_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    return payload

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_auth_token(token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")