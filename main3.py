from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for input and output
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

# In-memory "database"
todos: List[Todo] = []

# Create a new todo
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

# Get all todos
@app.get("/todos")
def get_all():
    return todos

# Get one todo by ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Delete a todo
@app.delete("/todos/{todo_id}")
def delete(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(i)
    raise HTTPException(status_code=404, detail="Todo not found")
