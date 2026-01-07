import pytest
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch

# Import your app
from main import app

# Get MongoDB connection details from environment
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "test_todo_db")


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """Create a fresh test database connection for each test"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    yield db
    # Clean up after test
    await db.todos.delete_many({})
    client.close()


@pytest.fixture(scope="function")
async def test_client(test_db):
    """Create a test client with mocked database"""
    # Patch the db module to use our test database
    with patch('db.database', test_db):
        with patch('db.todo_collection', test_db.todos):
            # Also patch routes.py if it imports directly
            with patch('routes.todo_collection', test_db.todos):
                transport = ASGITransport(app=app)
                async with AsyncClient(transport=transport, base_url="http://test") as client:
                    yield client