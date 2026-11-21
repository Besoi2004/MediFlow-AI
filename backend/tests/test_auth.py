from sqlalchemy import select

from app.auth import verify_password
from app.models import User
from scripts.seed import seed_users

NEW = {"email": "An@Mail.test", "password": "matkhau123", "full_name": "Nguyễn An",
       "birth_date": "1991-05-02", "gender": "male", "phone": "0900000001"}


def test_register_sets_httponly_cookie_and_customer_role(client, db):
    r = client.post("/api/auth/register", json=NEW)
    assert r.status_code == 201 and r.json()["role"] == "customer"
    assert "httponly" in r.headers["set-cookie"].lower()
    assert client.get("/api/auth/me").json()["email"] == "an@mail.test"
    u = db.scalar(select(User))
    assert u.password_hash != NEW["password"] and verify_password(NEW["password"], u.password_hash)


def test_register_ignores_role_field(client):
    r = client.post("/api/auth/register", json={**NEW, "role": "consultant"})
    assert r.status_code == 201 and r.json()["role"] == "customer"


def test_email_case_insensitive(client):  # Review Focus 5
    client.post("/api/auth/register", json=NEW)
    assert client.post("/api/auth/register", json={**NEW, "email": "an@mail.test"}).status_code == 409
    client.post("/api/auth/logout")
    r = client.post("/api/auth/login", json={"email": "AN@MAIL.TEST", "password": "matkhau123"})
    assert r.status_code == 200


def test_wrong_password_401(client):
    client.post("/api/auth/register", json=NEW)
    client.post("/api/auth/logout")
    r = client.post("/api/auth/login", json={"email": NEW["email"], "password": "sai12345"})
    assert r.status_code == 401


def test_short_password_422(client):
    assert client.post("/api/auth/register", json={**NEW, "password": "123"}).status_code == 422


def test_invalid_email_and_future_birth_date_422(client):
    assert client.post("/api/auth/register", json={**NEW, "email": "khong-phai-email"}).status_code == 422
    assert client.post("/api/auth/register", json={**NEW, "birth_date": "2999-01-01"}).status_code == 422


def test_logout_then_me_401(client):
    client.post("/api/auth/register", json=NEW)
    assert client.post("/api/auth/logout").status_code == 204
    assert client.get("/api/auth/me").status_code == 401


def test_tampered_token_401(client):
    client.cookies.set("access_token", "khong.phai.jwt")
    assert client.get("/api/auth/me").status_code == 401


def test_seed_users_creates_consultant(db, settings_with_seed_passwords):
    seed_users(db, settings_with_seed_passwords)
    seed_users(db, settings_with_seed_passwords)
    roles = sorted(db.scalars(select(User.role)).all())
    assert roles == ["consultant", "customer"]
