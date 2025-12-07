import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base
from app.database import engine

client = TestClient(app)

# Полный сброс и пересоздание схемы БД перед тестами
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def register_login(username="тест", password="1234"):
    """
        Вспомогательная функция:
        - регистрирует пользователя
        - логинит его
        - возвращает заголовок Authorization с токеном
    """
    client.post("/auth/register", json={"username": username, "password": password})
    resp = client.post("/auth/login", json={"username": username, "password": password})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_student_authorized():
    headers = register_login()
    data = {
        "name": "Иван Иванов",
        "faculty": "ФКН",
        "course": "Python",
        "score": 5,
    }
    resp = client.post("/students/", json=data, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Иван Иванов"
    assert body["faculty"] == "ФКН"
    assert body["course"] == "Python"
    assert body["score"] == 5


def test_create_student_unauthorized():
    data = {
        "name": "Мария Петрова",
        "faculty": "ФКН",
        "course": "Python",
        "score": 5,
    }
    resp = client.post("/students/", json=data)
    # без токена доступ запрещён
    assert resp.status_code == 401


def test_get_students_list():
    headers = register_login("пользователь2", "2222")

    # создаём одного студента перед запросом списка
    client.post(
        "/students/",
        json={
            "name": "Алексей Смирнов",
            "faculty": "ФКН",
            "course": "ML",
            "score": 4,
        },
        headers=headers,
    )

    resp = client.get("/students/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    names = [s["name"] for s in data]
    assert "Алексей Смирнов" in names
