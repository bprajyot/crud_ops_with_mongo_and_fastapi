import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URL or not DATABASE_NAME:
    raise RuntimeError("MongoDB environment variables not set")

# Create a function to get the collection instead of creating it at module level
def get_database():
    client = AsyncIOMotorClient(MONGO_URL)
    return client[DATABASE_NAME]

# For backward compatibility with existing code
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]
todo_collection = database.get_collection("todos")