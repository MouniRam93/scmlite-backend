# app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "scmlite"

    class Config:
        env_file = ".env"

settings = Settings()

# MongoDB connection
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# Collections
users_coll = db["users"]
shipments_coll = db["shipments"]
devices_coll = db["devices"]
device_streams_coll = db["device_streams"]
