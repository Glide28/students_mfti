# students_mfti
Backend-сервис для управления данными о студентах с аутентификацией и CRUD-операциями.

**Дисциплина:** "Язык Python для разработчиков"
**Автор:** Панклов Арсений
**Группа:** BHEMBD-25

## Функционал
- регистрация и вход пользователей (token auth);
- просмотр, добавление, изменение и удаление студентов (CRUD);
- валидация данных через Pydantic;
- хеширование паролей (bcrypt);
- модульные тесты (Pytest);
- поддержка SQLite (локально) и PostgreSQL (Docker).

## Технологии
| Компонент | Технология |
| --- | --- |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| DB | SQLite / PostgreSQL |
| Auth | Token, bcrypt, Pydantic |
| Tests | Pytest |
| Containers | Docker, Docker Compose |

## Структура проекта
```
app/
├─ database.py
├─ main.py
├─ models.py
├─ schemas.py
├─ routers/
│  ├─ auth_router.py
│  └─ students_router.py
└─ tests/
   ├─ test_auth.py
   └─ test_students.py
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## Запуск локально (SQLite)
1. git clone <репозиторий>
2. cd students_mfti
3. python -m venv .venv
4. .venv\Scripts\activate
5. pip install -r requirements.txt
6. uvicorn app.main:app --reload

Документация Swagger: http://127.0.0.1:8000/docs

## Запуск через Docker (PostgreSQL)
Создайте файл `.env`:
```
POSTGRES_DB=students_mfti_db
POSTGRES_USER=admin_ars
POSTGRES_PASSWORD=adminArs21
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Затем:
```
docker compose up -d
```

## Авторизация
| Метод | URL | Описание |
| --- | --- | --- |
| POST | /auth/register | регистрация |
| POST | /auth/login | вход и получение токена |

Передавайте токен в заголовке:
```
Authorization: Bearer <token>
```

## Методы для студентов
| Метод | URL | Описание |
| --- | --- | --- |
| GET | /students/ | список студентов |
| POST | /students/ | создать запись |
| GET | /students/{id} | получить запись |
| PATCH | /students/{id} | обновить запись |
| DELETE | /students/{id} | удалить запись |

## Тестирование
```
pytest -q
```

## Автор
Паниклов Арсений, группа BHEMBD-25. Проект выполнен в рамках курса "Язык Python для разработчиков".
