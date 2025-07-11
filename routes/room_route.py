from fastapi import APIRouter, Depends, HTTPException
from requests import Session
# Controllers
from controllers.room_controller import controller_get_all_room, controller_post_create_room, controller_delete_room_by_id
from controllers.auth_controller import get_db
from models.room_model import SaveRoom

router_rooms = APIRouter()

@router_rooms.get("/",response_model=dict,summary="Get All Room",tags=["Room"],status_code=200,
    description="This request is used to get all room",
    responses={
        200: {
            "description": "success fetch room",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "f6a33efc-5321-11f0-a0c3-3216422910e7",
                                "floor": "11",
                                "room_name": "Server Room",
                                "room_dept": "IT",
                                "created_at": "2025-06-27T13:42:58"
                            }
                        ],
                        "message": "room fetched",
                        "status": "success"
                    }
                }
            },
        },
        404: {
            "description": "failed fetch not found",
            "content": {
                "application/json": {
                    "example": {"message": "room not found", "status": "failed"}
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
def router_get_all_room(db: Session = Depends(get_db)):
    try:
        return controller_get_all_room(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_rooms.post("/",response_model=dict,summary="Post Create Room",tags=["Room"],status_code=201,
    description="This request is used to create a room",
    responses={
        201: {
            "description": "success create room",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "f6a33efc-5321-11f0-a0c3-3216422910e7",
                                "floor": "11",
                                "room_name": "Server Room",
                                "room_dept": "IT",
                                "created_at": "2025-06-27T13:42:58"
                            }
                        ],
                        "message": "room created",
                        "status": "success"
                    }
                }
            },
        },
        400: {
            "description": "failed fetch not found",
            "content": {
                "application/json": {
                    "example": {"message": "invalid room_dept", "status": "failed"}
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
def router_post_create_room(data: SaveRoom):
    try:
        return controller_post_create_room(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_rooms.delete("/{room_id}",response_model=dict,summary="Delete Room By Id",tags=["Room"],status_code=200,
    description="This request is used to permanentally delete room",
    responses={
        200: {
            "description": "success delete room by id",
            "content": {
                "application/json": {
                    "example": {
                        "message": "room permanently deleted",
                        "status": "success"
                    }
                }
            },
        },
        400: {
            "description": "failed fetch not found",
            "content": {
                "application/json": {
                    "example": {"message": "invalid room_id", "status": "failed"}
                }
            },
        },
        404: {
            "description": "failed find room",
            "content": {
                "application/json": {
                    "example": {"message": "room not found", "status": "failed"}
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
def router_delete_room_by_id(room_id: str):
    try:
        return controller_delete_room_by_id(room_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))