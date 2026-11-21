"""Fixture dùng chung: DB test thật (Postgres trong docker), TestClient."""
from collections.abc import Iterator
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.main import app
from app.models import Base

BACKEND_DIR = Path(__file__).resolve().parents[1]


def check_test_url(test_url: str | None, dev_url: str) -> sa.URL:
    """Test TRUNCATE mọi bảng, nên không được trỏ vào DB dev."""
    if not test_url:
        raise RuntimeError("Thiếu TEST_DATABASE_URL trong backend/.env")
    test, dev = sa.make_url(test_url), sa.make_url(dev_url)
    if (test.host, test.port, test.database) == (dev.host, dev.port, dev.database):
        raise RuntimeError("TEST_DATABASE_URL đang trỏ vào DB dev; test sẽ xóa sạch dữ liệu")
    return test


def _test_url() -> sa.URL:
    s = get_settings()
    try:
        return check_test_url(s.test_database_url, s.database_url)
    except RuntimeError as e:
        pytest.exit(str(e))


@pytest.fixture(scope="session")
def engine() -> Iterator[sa.Engine]:
    url = _test_url()
    admin = sa.create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.scalar(sa.text("select 1 from pg_database where datname = :n"), {"n": url.database})
        if not exists:
            conn.execute(sa.text(f'create database "{url.database}"'))
    admin.dispose()

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.attributes["url"] = url.render_as_string(hide_password=False)
    command.upgrade(cfg, "head")

    eng = sa.create_engine(url)
    yield eng
    eng.dispose()


@pytest.fixture
def db(engine) -> Iterator[Session]:
    session = Session(engine)
    yield session
    session.close()
    tables = ", ".join(t.name for t in Base.metadata.sorted_tables)
    with engine.begin() as conn:
        conn.execute(sa.text(f"truncate {tables} restart identity cascade"))


@pytest.fixture
def catalog(db) -> None:
    from scripts.seed import DATA_DIR, seed_catalog

    seed_catalog(db, DATA_DIR)


@pytest.fixture
def settings_with_seed_passwords():
    return get_settings().model_copy(
        update={"seed_consultant_password": "tvv-test-pass", "seed_customer_password": "kh-test-pass"}
    )


@pytest.fixture
def client(db) -> Iterator[TestClient]:
    def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
