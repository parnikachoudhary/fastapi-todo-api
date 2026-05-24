from fastapi import APIRouter, Depends, Body
from sqlmodel import Session
from app.database import get_session
from app.models import Todo, TodoCreate, TodoPut, TodoBulkUpdateItem, TodoUpdate
from app.crud import (
    create_todo, 
    get_todos, 
    get_todo, 
    delete_todo, 
    patch_todo, 
    put_todo,
    bulk_create_todos,
    bulk_delete_todos,
    bulk_update_todos
    ) 

router = APIRouter()


# BULK UPDATE
@router.patch("/bulk")
def update_bulk_todos(items: list[TodoBulkUpdateItem], session: Session = Depends(get_session)):
    return bulk_update_todos(session, items)

# BULK DELETE
@router.delete("/bulk")
def delete_bulk_todos(ids: list[int] = Body(...), session: Session = Depends(get_session)):
    return bulk_delete_todos(session, ids)

# BULK ADD
@router.post("/bulk")
def add_bulk_todos(todos: list[TodoCreate], session: Session = Depends(get_session)):
    return bulk_create_todos(session, todos)


@router.get("/")
def read_todos(session: Session = Depends(get_session)):
    return get_todos(session)


@router.get("/{todo_id}")
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    return get_todo(session, todo_id)


@router.post("/")
def add_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    return create_todo(session, todo)

@router.put("/{todo_id}")
def replace_todo(todo_id: int, updated_todo: TodoPut, session: Session = Depends(get_session)):
    todo = put_todo(session, todo_id, updated_todo)
    if not todo:
        return {"error": "Todo not found"}
    return todo

@router.patch("/{todo_id}")
def partial_update_todo(todo_id: int, updated_todo: TodoUpdate, session: Session = Depends(get_session)):
    todo = patch_todo(session, todo_id, updated_todo)
    if not todo:
        return {"error": "Todo not found"}
    return todo

@router.delete("/{todo_id}")
def remove_todo(todo_id: int, session: Session = Depends(get_session)):
    return delete_todo(todo_id, session)


