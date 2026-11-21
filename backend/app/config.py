"""Cấu hình đọc từ backend/.env (pydantic-settings)."""
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
PLACEHOLDER_SECRET = "doi-gia-tri-nay"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    database_url: str
    test_database_url: str | None = None

    jwt_secret: str
    jwt_expire_minutes: int = 10080
    cookie_secure: bool = False
    guest_cookie_secret: str

    llm_provider: str = "google_genai"
    llm_model: str = "gemini-3.5-flash-lite"
    google_api_key: str | None = None
    embedding_model: str | None = None
    embedding_dim: int = 768

    chat_daily_limit_per_user: int = 50
    chat_daily_limit_per_guest: int = 10
    chat_daily_limit_all_guests: int = 200

    seed_consultant_email: str = "tuvanvien@mediflow.test"
    seed_consultant_password: str = ""
    seed_customer_email: str = "khachhang@mediflow.test"
    seed_customer_password: str = ""

    @field_validator("jwt_secret", "guest_cookie_secret")
    @classmethod
    def _strong_secret(cls, v: str) -> str:
        # Secret mẫu trong .env.example là công khai: ai biết nó sẽ ký được token giả.
        if v == PLACEHOLDER_SECRET or len(v) < 32:
            raise ValueError("Secret phải dài ít nhất 32 ký tự và không được là giá trị mẫu")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
