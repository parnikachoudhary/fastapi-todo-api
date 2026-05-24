from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Todo, TodoCreate, TodoPut, TodoUpdate, TodoBulkUpdateItem

app = FastAPI()

# 1. SINGLE CREATE
def create_todo(session: Session, todo_in: TodoCreate):
    todo = Todo(**todo_in.dict())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


# 2. BULK CREATE - BY USING LIST OF OBJECTS
def bulk_create_todos(session: Session, todos_in: list[TodoCreate]):
    todos = [Todo(**todo.dict()) for todo in todos_in] 
    session.add_all(todos)
    session.commit()

    for todo in todos:
        session.refresh(todo)

    return todos


# 3. READ ALL
def get_todos(session: Session):
    return session.exec(select(Todo)).all()
# 4. READ BY ID
def get_todo(session: Session, todo_id: int):
    return session.get(Todo, todo_id)


# 5. PATCH UPDATE - PARTIAL UPDATE
def patch_todo(session: Session, todo_id: int, updated_todo: TodoUpdate):
    todo = session.get(Todo, todo_id)
    if not todo:
        return None

    update_data = updated_todo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.commit()
    session.refresh(todo)
    return todo



# 6. PUT - COMPLETE REPLACE
def put_todo(session: Session, todo_id: int, updated_todo: TodoPut):
    todo = session.get(Todo, todo_id)
    if not todo:
        return None

    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.completed = updated_todo.completed
    todo.priority = updated_todo.priority

    session.commit()
    session.refresh(todo)
    return todo


# 7. BULK UDATE
def bulk_update_todos(session: Session, items: list[TodoBulkUpdateItem]):
    updated_todos = []
    not_found_ids = []

    for item in items:
        todo = session.get(Todo, item.id) # Find row by id
        if not todo:
            not_found_ids.append(item.id)
            continue

        data = item.dict(exclude_unset=True) # Get only fields user sent
        data.pop("id", None) # remove id from dictionary, because id should not be updated

        for key, value in data.items():
            setattr(todo, key, value) # todo.title(key) = "New"(value) -> dynamically update fields

        updated_todos.append(todo)

    session.commit()

    for todo in updated_todos:
        session.refresh(todo)

    return {
        "updated": updated_todos,
        "not_found_ids": not_found_ids
    }

# 8. DELETE
def delete_todo(todo_id: int, session: Session):
    todo = session.get(Todo, todo_id)  # SELECT * FROM todo WHERE id=todo_id
    if not todo:
        return {"error": "Todo not found"}
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

# 9. BULK DELETE
def bulk_delete_todos(session: Session, ids: list[int]):
    if not ids:
        return {"deleted_ids": []}

    todos = session.exec(select(Todo).where(Todo.id.in_(ids))).all()

    deleted_ids = []
    for todo in todos:
        deleted_ids.append(todo.id)
        session.delete(todo)

    session.commit()

    return {
        "deleted_ids": deleted_ids
    }