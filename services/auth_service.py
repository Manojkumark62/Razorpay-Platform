from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.config import settings
from models.user_model import User
from models.role_model import Role
from models.refresh_token_model import RefreshToken
from models.password_reset_model import PasswordReset

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def register_user(db: Session, username: str, email: str, password: str, role_id: int):
    existing_user = (db.query(User).filter(User.email == email).first())
    if existing_user:
        raise Exception("Email already exists")
    user = User(username=username, email=email, hashed_password=hash_password(password), role_id=role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = (db.query(User).filter(User.email == email).first())
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    access_token = (create_access_token({"sub": str(user.id)}))
    refresh_token = (create_refresh_token({"sub": str(user.id)}))
    token_record = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(token_record)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_exists = (db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first())
        if not token_exists:
            return None
        return create_access_token({"sub": user_id})
    except JWTError:
        return None

def get_user_by_id(db: Session, user_id: int):
    return (db.query(User).filter(User.id == user_id).first())

def get_user_by_email(db: Session, email: str):
    return (db.query(User).filter(User.email == email).first())

def forgot_password(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    reset_token = (create_access_token({"sub": str(user.id)}))
    record = PasswordReset(email=email, reset_token=reset_token)
    db.add(record)
    db.commit()
    return reset_token

def reset_password(db: Session, token: str, new_password: str):
    reset_record = (db.query(PasswordReset).filter(PasswordReset.reset_token == token).first())
    if not reset_record:
        return False
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("sub")
    user = get_user_by_id(db, int(user_id))
    user.hashed_password = (hash_password(new_password))
    db.commit()
    return True

def change_password(db: Session, user_id: int, old_password: str, new_password: str):
    user = get_user_by_id(db, user_id)
    if not verify_password(old_password, user.hashed_password):
        return False
    user.hashed_password = (hash_password(new_password))
    db.commit()
    return True