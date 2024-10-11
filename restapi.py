from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for todo items
todo_items = []
next_id = 1

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Get all todo items
@app.get("/todos/", response_model=List[TodoItem])
async def get_todos():
    return todo_items

# Get a specific todo item by ID
@app.get("/todos/{item_id}", response_model=TodoItem)
async def get_todo(item_id: int):
    for item in todo_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Todo item not found")

# Create a new todo item
@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    global next_id
    todo.id = next_id
    next_id += 1
    todo_items.append(todo)
    return todo

# Update an existing todo item
@app.put("/todos/{item_id}", response_model=TodoItem)
async def update_todo(item_id: int, updated_todo: TodoItem):
    for index, item in enumerate(todo_items):
        if item.id == item_id:
            todo_items[index] = updated_todo
            updated_todo.id = item_id  # Maintain the original ID
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo item not found")

# Delete a todo item
@app.delete("/todos/{item_id}", response_model=dict)
async def delete_todo(item_id: int):
    for index, item in enumerate(todo_items):
        if item.id == item_id:
            todo_items.pop(index)
            return {"detail": "Todo item deleted"}
    raise HTTPException(status_code=404, detail="Todo item not found")

