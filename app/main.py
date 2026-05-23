from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine

from app.routes.todo import router as todo_router

app = FastAPI()

app.include_router(todo_router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def home():
    return {"message": "Server Running"}