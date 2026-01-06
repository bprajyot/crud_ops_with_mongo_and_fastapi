from fastapi import APIRouter, HTTPException
from bson import ObjectId

from db import todo_collection
from model import todo_helper
from schema import TodoCreate, TodoUpdate

router = APIRouter()


@router.post("/todos")
async def create_todo(todo: TodoCreate):
    new_todo = {
        "title": todo.title,
        "description": todo.description,
        "completed": False,
    }
    result = await todo_collection.insert_one(new_todo)
    return {"id": str(result.inserted_id)}


@router.get("/todos")
async def get_all_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return todos


@router.get("/todos/{todo_id}")
async def get_todo(todo_id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_helper(todo)


@router.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: TodoUpdate):
    update_data = {k: v for k, v in todo.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await todo_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo_helper(updated)


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}