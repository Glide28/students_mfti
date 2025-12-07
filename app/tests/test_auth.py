import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base
from app.database import engine, get_db
from sqlalchemy.orm import Session

client = TestClient(app)

# Reset database before tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def register(username="user1", password="pass1"):
    return client.post("/auth/register", json={"username": username, "password": password})


def login(username="user1", password="pass1"):
    return client.post("/auth/login", json={"username": username, "password": password})


def test_register_success():
    response = register("alice", "1234")
    assert response.status_code == 200
    assert response.json() == {"status": "registered"}


def test_register_duplicate_user():
    register("bob", "123")
    response = register("bob", "456")
    assert response.status_code == 400


def test_login_success():
    register("carol", "abc")
    response = login("carol", "abc")
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_wrong_password():
    register("david", "111")
    response = login("david", "wrong")
    assert response.status_code == 401
