# app/database.py
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy Base for models
Base = declarative_base()

# Read PostgreSQL settings from environment (used in Docker)
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
    # SQLite needs this flag in multithreaded environments like FastAPI + TestClient
    connect_args = {"check_same_thread": False}

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency for FastAPI endpoints.
    Creates a DB session and closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()