import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base
from app.database import engine

client = TestClient(app)

# Reset DB
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def register_login(username="test", password="1234"):
    client.post("/auth/register", json={"username": username, "password": password})
    resp = client.post("/auth/login", json={"username": username, "password": password})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_student_authorized():
    headers = register_login()
    data = {"name": "John Doe", "faculty": "CS", "course": "Python", "score": 5}
    resp = client.post("/students/", json=data, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "John Doe"


def test_create_student_unauthorized():
    data = {"name": "Jane Doe", "faculty": "CS", "course": "Python", "score": 5}
    resp = client.post("/students/", json=data)
    assert resp.status_code == 401


def test_get_students_list():
    headers = register_login("user2", "2222")
    client.post("/students/", json={"name": "X", "faculty": "CS", "course": "ML", "score": 4}, headers=headers)
    resp = client.get("/students/", headers=headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
