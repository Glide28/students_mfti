# app/main.py
from fastapi import FastAPI

from app.database import Base, engine
from app import models  
from app.routers.auth_router import router as auth_router
from app.routers.students_router import router as students_router

# Создаёт таблицы в БД 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Students CRUD + Auth (Final Project)",
    version="1.0.0",
)

# Подключает роутеры
app.include_router(auth_router)
app.include_router(students_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Students API with auth is running"}
