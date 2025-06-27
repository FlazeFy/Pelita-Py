from fastapi import FastAPI
from configs.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Pelita API",
    description="PELITA is designed as an inventory and asset management system for offices or warehouses, allowing users to store all asset data, monitor assets, create routine maintenance schedules, and perform daily checklists. Additionally, the application is integrated with Telegram Chat, enabling users to receive broadcasts easily and monitor data with just a simple click in the Telegram chat room.",
    version="1.0.0",
    contact={
        "name": "Leonardho R Sitanggang",
        "url": "https://www.linkedin.com/in/leonardho-rante-sitanggang/",  
        "email": "flazen.edu@gmail.com"
    }
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000/",
    "http://127.0.0.1:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
from routes.auth_route import router_auth
from routes.room_route import router_rooms

app.include_router(router_auth, prefix="/api/v1/auths", tags=["Auth"])
app.include_router(router_rooms, prefix="/api/v1/rooms", tags=["Room"])

# Landing
@app.get("/")
async def root():
    return {"message": "Welcome to PELITA"}

__all__ = ['app']
