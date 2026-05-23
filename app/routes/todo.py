from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Todo
from app.crud import create_todo, get_todos, get_todo, update_todo, delete_todo

router = APIRouter()

@router.post("/")
def add_todo(todo: Todo, session: Session = Depends(get_session)):
    return create_todo(session, todo)

@router.get("/")
def read_todos(session: Session = Depends(get_session)):
    return get_todos(session)


@router.get("/{todo_id}")
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    return get_todo(session, todo_id)

@router.put("/{todo_id}")
def update_todo_endpoint(todo_id: int, updated_todo: Todo, 
                         session: Session = Depends(get_session)):
    todo = update_todo(session, todo_id, updated_todo)
    if not todo:
        return {"error": "Todo not found"}
    return todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: int, session: Session = Depends(get_session)):
    return delete_todo(todo_id, session)