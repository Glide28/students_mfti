# app/routers/auth_router.py
import secrets
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import RegisterData, LoginData, UserOut

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Хэширование пароля с помощью bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Проверка пароля."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token() -> str:
    """Генерация случайного токена."""
    return secrets.token_hex(16)


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Получение текущего пользователя по токену Bearer."""
    token = creds.credentials
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@router.post("/register")
def register(
    data: RegisterData,
    db: Session = Depends(get_db),
):
    """
    Регистрация нового пользователя.
    """
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        username=data.username,
        password=hash_password(data.password),
        token=None,
    )
    db.add(user)
    db.commit()
    return {"status": "registered"}


@router.post("/login", response_model=UserOut)
def login(
    data: LoginData,
    db: Session = Depends(get_db),
):
    """
    Аутентификация пользователя.
    Возвращает id, username и токен.
    """
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_token()
    user.token = token
    db.commit()
    db.refresh(user)
    return user


@router.post("/logout")
def logout(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Logout: очищает токен у текущего пользователя.
    """
    current.token = None
    db.commit()
    return {"status": "logged out"}
