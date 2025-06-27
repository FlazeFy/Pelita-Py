from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
# Controllers
from controllers.auth_controller import controller_register_user, controller_login_user, get_db, controller_refresh_auth_token, UserCreate, UserLogin

router_auth = APIRouter()

@router_auth.post("/register",response_model=dict,summary="Register",tags=["Auth"],status_code=201,
    description="This request is used to create a new account for user using username, email, and password",
    responses={
        201: {
            "description": "Successful regist a new account",
            "content": {
                "application/json": {
                    "example": {
                        "message": "user registered successfully",
                        "status": "success",
                    }
                }
            },
        },
        409: {
            "description": "Duplicated account",
            "content": {
                "application/json": {
                    "example": {
                        "message": "the email or username already been used. try using other",
                        "status": "failed",
                    }
                }
            },
        },
        422: {
            "description": "Validation failed",
            "content": {
                "application/json": {
                    "example": {"message": "[validation message]", "status": "failed"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "error",
                    }
                }
            },
        },
    },
)
def router_register(user: UserCreate, db: Session = Depends(get_db)):
    return controller_register_user(user, db)


@router_auth.post("/login",response_model=dict,summary="User Login",tags=["Auth"],
    description="Authenticate user with username and password, returning access and refresh tokens.",
    responses={
        200: {
            "description": "User successfully logged in",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "AISKWNB123123",
                        "refresh_token": "AISKWNB123123",
                        "message": "user login successfully",
                        "status": "success",
                    }
                }
            },
        },
        401: {
            "description": "invalid username or password",
            "content": {
                "application/json": {
                    "example": {
                        "message": "invalid username or password",
                        "status": "failed",
                    }
                }
            },
        },
        422: {
            "description": "Validation failed",
            "content": {
                "application/json": {
                    "example": {"message": "[validation message]", "status": "failed"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "error",
                    }
                }
            },
        },
    },
)
def router_login(user: UserLogin, db: Session = Depends(get_db)):
    return controller_login_user(user, db)

@router_auth.post("/refresh",response_model=dict,summary="Refresh Access Token",tags=["Auth"],
    description="Use a valid refresh token from the Authorization header to get a new access token.",
    responses={
        200: {
            "description": "Access token refreshed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "AISKWNB123123",
                        "message": "user token refresh",
                        "status": "success",
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized: Missing, invalid, or expired refresh token",
            "content": {
                "application/json": {
                    "example": {"message": "invalid token", "status": "failed"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "error",
                    }
                }
            },
        },
    },
)
def router_refresh(request: Request):
    return controller_refresh_auth_token(request)
