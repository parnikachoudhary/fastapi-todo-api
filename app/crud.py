from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Todo

app = FastAPI()

# CREATE
def create_todo(session: Session, todo: Todo):
    # FastAPI automatically reads incoming JSON request body
    # from user, validates it, and converts to Todo Python object
    session.add(todo)      # Adds object to DB session
    session.commit()       # Actually saves changes permanently
    session.refresh(todo)  # Refreshes object with auto-generated id
    return todo

# READ
def get_todos(session: Session):
    return session.exec(select(Todo)).all()

def get_todo(session: Session, todo_id: int):
    return session.get(Todo, todo_id)

# UPDATE
def update_todo(session: Session, todo_id: int, updated_todo: Todo):
    todo = session.get(Todo, todo_id)
    if not todo:
        return None
    for key, value in updated_todo.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    session.commit()
    session.refresh(todo)
    return todo

# DELETE
def delete_todo(todo_id: int, session: Session):
    todo = session.get(Todo, todo_id)  # SELECT * FROM todo WHERE id=todo_id
    if not todo:
        return {"error": "Todo not found"}
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}