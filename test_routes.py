import pytest
from bson import ObjectId


class TestTodoRoutes:
    
    @pytest.mark.asyncio
    async def test_create_todo(self, test_client):
        """Test creating a new todo"""
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo"
        }
        
        response = await test_client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert ObjectId.is_valid(data["id"])
    
    @pytest.mark.asyncio
    async def test_create_todo_without_description(self, test_client):
        """Test creating a todo without description"""
        todo_data = {
            "title": "Test Todo",
            "description": None  # Explicitly set to None
        }
        
        response = await test_client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
   
    @pytest.mark.asyncio
    async def test_get_all_todos(self, test_client):
        """Test getting all todos"""
        # Create test todos
        todos = [
            {"title": "Todo 1", "description": "Description 1"},
            {"title": "Todo 2", "description": "Description 2"}
        ]
        
        for todo in todos:
            await test_client.post("/todos", json=todo)
        
        response = await test_client.get("/todos")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Todo 1"
        assert data[1]["title"] == "Todo 2"
        assert data[0]["completed"] == False
    
    @pytest.mark.asyncio
    async def test_get_todo_by_id(self, test_client):
        """Test getting a specific todo by ID"""
        # Create a todo
        todo_data = {"title": "Test Todo", "description": "Test Description"}
        create_response = await test_client.post("/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Get the todo
        response = await test_client.get(f"/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["completed"] == False
    
    @pytest.mark.asyncio
    async def test_get_todo_not_found(self, test_client):
        """Test getting a non-existent todo"""
        fake_id = str(ObjectId())
        response = await test_client.get(f"/todos/{fake_id}")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"
    
    @pytest.mark.asyncio
    async def test_update_todo(self, test_client):
        """Test updating a todo"""
        # Create a todo
        todo_data = {"title": "Original Title", "description": "Original Description"}
        create_response = await test_client.post("/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Update the todo
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        }
        response = await test_client.put(f"/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Description"
        assert data["completed"] == True
    
    @pytest.mark.asyncio
    async def test_delete_todo(self, test_client):
        """Test deleting a todo"""
        # Create a todo
        todo_data = {"title": "Test Todo", "description": "Test Description"}
        create_response = await test_client.post("/todos", json=todo_data)
        
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]
        
        # Delete the todo
        response = await test_client.delete(f"/todos/{todo_id}")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Todo deleted successfully"
        
        # Verify it's deleted
        get_response = await test_client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404