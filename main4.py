from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import Body
app = FastAPI()

#Pydantic Model
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

#Service Layer
class TodoService:
    def __init__(self):
        self.todos: List[Todo] = []

    def get_all(self):
        return self.todos

    def get_by_id(self, todo_id: int):
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def add(self, todo: Todo):
        self.todos.append(todo)
        return todo
    
    def replace(self, todo_id: int, new_todo: Todo):
        for i, existing in enumerate(self.todos):
            if existing.id == todo_id:
                self.todos[i] = new_todo  
                return new_todo
        return None 
    
    def patch_data(self,todo_id: int, data: dict):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                updated_data=todo.dict()
                updated_data.update(data)
                self.todos[i]=Todo(**updated_data)
                return self.todos[i]
        return None

    def delete(self, todo_id: int):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                return self.todos.pop(i)
        return None
    
    

    


#Singleton Instance
todo_service = TodoService()

#Dependency Function
def get_service():
    return todo_service

#Routes with Dependency Injection

@app.get("/todos")
def list_todos(service: TodoService = Depends(get_service)):
    return service.get_all()

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, service: TodoService = Depends(get_service)):
    todo = service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos")
def create(todo: Todo, service: TodoService = Depends(get_service)):
    return service.add(todo)

@app.put("/todos/{todo_id}")
def replace_todo(todo_id: int, todo:Todo, service: TodoService = Depends(get_service)):
    new_todo=service.replace(todo_id,todo)
    if not new_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return new_todo

@app.patch("/todos/{todo_id}")
def patch_data(todo_id: int,data:dict= Body(...),service: TodoService = Depends(get_service)):
    todo=service.patch_data(todo_id,data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete(todo_id: int, service: TodoService = Depends(get_service)):
    todo = service.delete(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"status": "deleted", "todo": todo}
