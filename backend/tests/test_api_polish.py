"""API cho giao diện: lỗi nhập liệu tiếng Việt, giới hạn ngày, lỗi IntegrityError không bị che."""
from datetime import datetime, time, timedelta

import pytest
from conftest import tomorrow_at
from sqlalchemy.exc import IntegrityError

from app.services.booking import create_booking
from app.textnorm import VN_TZ, today_vn


def test_422_is_vietnamese_with_field(client):
    r = client.post("/api/auth/register", json={"email": "x@y.test", "password": "123", "full_name": "A",
                                                "birth_date": "1990-01-01", "gender": "male", "phone": "0900000001"})
    body = r.json()
    assert r.status_code == 422 and body["detail"] == "Dữ liệu không hợp lệ"
    assert {"field": "password", "message": "Cần ít nhất 8 ký tự"} in body["errors"]


def test_422_missing_field(client):
    errors = client.post("/api/auth/login", json={"email": "a@b.test"}).json()["errors"]
    assert {"field": "password", "message": "Bắt buộc"} in errors


def test_422_value_error_message_kept(client):
    errors = client.post("/api/auth/login", json={"email": "sai", "password": "x"}).json()["errors"]
    assert {"field": "email", "message": "Email không hợp lệ"} in errors


@pytest.mark.parametrize("path,param", [("/api/packages/ALP-CB01/slots", "date_from")])
def test_far_dates_rejected(client, catalog, path, param):
    r = client.get(path, params={param: "9999-12-31"})
    assert r.status_code == 422 and r.json()["errors"][0]["field"] == param


def test_consultant_far_date_rejected(consultant_client):
    assert consultant_client.get("/api/consultant/bookings", params={"date": "9999-12-31"}).status_code == 422


def test_birth_date_too_old_rejected(client):
    r = client.post("/api/auth/register", json={"email": "o@y.test", "password": "matkhau123", "full_name": "A",
                                                "birth_date": "1800-01-01", "gender": "male", "phone": "0900000001"})
    assert {"field": "birth_date", "message": "Ngày sinh không hợp lệ"} in r.json()["errors"]


def test_non_duplicate_integrity_error_not_masked(db, catalog, make_slot):
    slot = make_slot("ALP", tomorrow_at(7))
    with pytest.raises(IntegrityError):
        create_booking(db, user_id=999_999, package_code="ALP-CB01", slot_id=slot.id)  # khóa ngoại sai


def test_date_from_window_end_is_vn_local(client, catalog, make_slot):
    d = today_vn() + timedelta(days=2)
    last_in = make_slot("ALP", datetime.combine(d + timedelta(days=13), time(23, 30), VN_TZ))
    first_out = make_slot("ALP", datetime.combine(d + timedelta(days=14), time(6, 30), VN_TZ))
    ids = [s["id"] for s in client.get("/api/packages/ALP-CB01/slots", params={"date_from": d.isoformat()}).json()]
    assert last_in.id in ids and first_out.id not in ids


def test_consultant_date_filter_at_0630_vn(customer_client, consultant_client, catalog, make_slot, db):
    d = today_vn() + timedelta(days=3)
    slot = make_slot("ALP", datetime.combine(d, time(6, 30), VN_TZ))  # 23:30 UTC ngày hôm trước
    customer_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": slot.id})
    rows = consultant_client.get("/api/consultant/bookings", params={"date": d.isoformat()}).json()
    assert len(rows) == 1
