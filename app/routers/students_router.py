# app/routers/students_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student, User
from app.schemas import StudentCreate, StudentUpdate, StudentOut
from app.routers.auth_router import get_current_user

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


@router.post("/", response_model=StudentOut)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    """
        Создание студента (только для авторизованных пользователей).
    """
    obj = Student(
        name=student.name,
        faculty=student.faculty,
        course=student.course,
        score=student.score,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[StudentOut])
def read_students(
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    """
        Получение списка всех студентов.
    """
    objs = db.query(Student).all()
    return objs


@router.get("/{student_id}", response_model=StudentOut)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    """
        Получение одного студента по id.
    """
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.patch("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    """
        Частичное обновление данных студента.
    """
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in data.dict(exclude_none=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    """
        Удаление студента.
    """
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(obj)
    db.commit()
    return {"status": "deleted"}
