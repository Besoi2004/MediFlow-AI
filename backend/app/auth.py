"""Băm mật khẩu, JWT trong cookie, current_user, require_role."""
from datetime import UTC, datetime, timedelta
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException, Request, Response
from pwdlib import PasswordHash

from app.config import get_settings
from app.db import DbSession
from app.models import User

COOKIE_NAME = "access_token"
_hasher = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _hasher.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    s = get_settings()
    exp = datetime.now(UTC) + timedelta(minutes=s.jwt_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": exp}, s.jwt_secret, algorithm="HS256")


def set_auth_cookie(response: Response, token: str) -> None:
    s = get_settings()
    response.set_cookie(
        COOKIE_NAME, token, httponly=True, samesite="lax", secure=s.cookie_secure,
        max_age=s.jwt_expire_minutes * 60, path="/",
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME, path="/", httponly=True, samesite="lax", secure=get_settings().cookie_secure)


def optional_user(request: Request, db: DbSession) -> User | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        payload = jwt.decode(token, get_settings().jwt_secret, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None
    return db.get(User, user_id)


def current_user(user: Annotated[User | None, Depends(optional_user)]) -> User:
    if user is None:
        raise HTTPException(401, "Vui lòng đăng nhập")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def require_role(role: Literal["customer", "consultant"]):
    def dependency(user: CurrentUser) -> User:
        if user.role != role:
            raise HTTPException(403, "Không có quyền truy cập")
        return user

    return dependency
