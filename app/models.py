# app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # хэш пароля
    token = Column(String, nullable=True)      # текущий токен авторизации


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)      # ФИО (фамилия + имя)
    faculty = Column(String, nullable=False)   # факультет
    course = Column(String, nullable=False)    # курс / предмет
    score = Column(Integer, nullable=False)    # оценка
