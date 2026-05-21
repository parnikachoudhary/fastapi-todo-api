from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="TODO App API")

#Data Model
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None #This field is optional
    completed: bool = True
    priority: str = "medium" #Default values


#In-memory storage >> create a list of objects
todos: List[Todo] = []


#Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to TODO API App"}


#Get all TODOS
@app.get("/todos", response_model=List[Todo]) # That only response in the Todo list form allowed
def get_all_todos():
    return todos

#GET a single todo by ID
@app.get("/todos/{todo_id}", response_model=Todo) # Response will be Object Todo type
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


#POST - Create a new Todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    # Check if id already exists, because no two todos have same id
    for existing in todos:
        if existing.id == todo.id:
            raise HTTPException(status_code=400, detail="Todo with this ID already exists")
    todos.append(todo)
    return todo


#PUT - Update existing Todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
        raise HTTPException(status_code=404, detail="Todo not found")
    

#DELETE a Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted = todos.pop(index)
            return {"message": "Succesfully deleted", "todo": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")


#Mark todo as complete
@app.patch("/todos/{todo_id}/complete")
def mark_complete(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return {"message": "Toda marked as completed", "todo": todo}
        
    raise HTTPException(status_code=404, detail="Todo not found")






