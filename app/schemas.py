# app/schemas.py
from typing import Optional
from pydantic import BaseModel


# ====== Student схемы ======
class StudentBase(BaseModel):
    name: str
    faculty: str
    course: str
    score: int

class StudentCreate(StudentBase):
    """Схема для создания студента."""
    pass

class StudentUpdate(BaseModel):
    """Схема для частичного обновления студента."""
    name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[str] = None
    score: Optional[int] = None

class StudentOut(StudentBase):
    """Схема для возврата студента клиенту."""
    id: int
    class Config:
        from_attributes = True

# ====== Auth схемы ======
class RegisterData(BaseModel):
    username: str
    password: str

class LoginData(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    token: str
    class Config:
        from_attributes = True
