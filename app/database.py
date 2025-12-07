# app/database.py
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy Base для моделей
Base = declarative_base()

# PostgreSQL настройки из environment (Docker)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_DB:
    # PostgreSQL mode (Docker / production)
    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}/{POSTGRES_DB}"
    )
    connect_args = {}
else:
    # SQLite mode (local dev/tests)
    DATABASE_URL = "sqlite:///./students.db"
    # Для SQLite требуется флаг в многопоточной среде: FastAPI + TestClient
    connect_args = {"check_same_thread": False}

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
        Зависимость для FastAPI endpoints.
        Создаёт сессию базы данных и закрывает её после выполнения запроса
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
