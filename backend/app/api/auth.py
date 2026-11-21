"""API đăng ký, đăng nhập, đăng xuất, thông tin tài khoản."""
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth import (
    CurrentUser,
    clear_auth_cookie,
    create_access_token,
    hash_password,
    set_auth_cookie,
    verify_password,
)
from app.db import DbSession
from app.models import User
from app.schemas import LoginIn, RegisterIn, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

_EMAIL_TAKEN = "Email đã được đăng ký"


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterIn, response: Response, db: DbSession):
    if db.scalar(select(User.id).where(User.email == body.email)):
        raise HTTPException(409, _EMAIL_TAKEN)
    user = User(
        email=body.email, password_hash=hash_password(body.password), role="customer",
        full_name=body.full_name, birth_date=body.birth_date, gender=body.gender, phone=body.phone,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:  # hai người đăng ký cùng email cùng lúc
        db.rollback()
        raise HTTPException(409, _EMAIL_TAKEN) from e
    set_auth_cookie(response, create_access_token(user.id))
    return user


@router.post("/login", response_model=UserOut)
def login(body: LoginIn, response: Response, db: DbSession):
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Email hoặc mật khẩu không đúng")
    set_auth_cookie(response, create_access_token(user.id))
    return user


@router.post("/logout", status_code=204)
def logout():
    response = Response(status_code=204)
    clear_auth_cookie(response)
    return response


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
