from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from schemas.auth_schema import (
    RegisterSchema, LoginSchema, RefreshSchema,
    ForgotPasswordSchema, ResetPasswordSchema
)
from models.user_model import User
from models.role_model import Role
from models.refresh_token_model import RefreshToken
from models.password_reset_model import PasswordReset
from core.database import get_db
from jose import jwt, JWTError
from core.config import settings
from core.permission import require_roles
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token, create_refresh_token
from dependencies.dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_user(payload: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        # FIX: 400 instead of 200 error message
        raise HTTPException(status_code=400, detail="Email already exists")

    role_name = payload.role or "EMPLOYEE"
    role = db.query(Role).filter(Role.name == role_name).first()
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role_id=role.id if role else None,
    )
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    db.add(RefreshToken(user_id=user.id, token=refresh_token))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/token")
def login_for_access_token(
    username: str | None = Form(default=None),
    email: str | None = Form(default=None),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_value = email or username
    if not login_value:
        raise HTTPException(status_code=422, detail="Email or username is required")

    user = db.query(User).filter(
        (User.email == login_value) | (User.username == login_value)
    ).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    db.add(RefreshToken(user_id=user.id, token=refresh_token))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@router.post("/refresh")
def refresh_access_token(payload: RefreshSchema, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = decoded.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # FIX: verify token exists in DB
        token_record = db.query(RefreshToken).filter(
            RefreshToken.token == payload.refresh_token
        ).first()
        if not token_record:
            raise HTTPException(status_code=401, detail="Refresh token revoked")
        return {"access_token": create_access_token({"sub": user_id})}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return {"message": "If that email exists, a reset link has been sent"}

    reset_token = create_access_token({"sub": str(user.id)})
    db.add(PasswordReset(email=user.email, reset_token=reset_token))
    db.commit()
    return {"message": "Reset token generated", "reset_token": reset_token}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    token_record = db.query(PasswordReset).filter(
        PasswordReset.reset_token == payload.reset_token
    ).first()
    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    try:
        decoded = jwt.decode(
            payload.reset_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = decoded.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token expired or invalid")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(payload.new_password)
    # FIX: delete the used reset token
    db.delete(token_record)
    db.commit()
    return {"message": "Password updated successfully"}