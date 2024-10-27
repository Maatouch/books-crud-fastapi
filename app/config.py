from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://mongo:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "books_db")

@lru_cache
def get_database():
    client = AsyncIOMotorClient(DATABASE_URL)
    return client[DATABASE_NAME]