import threading
from datetime import date, datetime, time, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.auth import COOKIE_NAME, create_access_token, hash_password
from app.main import app
from app.models import Booking, Hospital, Package, TimeSlot, User
from app.services.booking import BookingError, cancel_booking, create_booking
from app.textnorm import VN_TZ
from scripts.seed import seed_slots


def today_vn() -> date:
    return datetime.now(VN_TZ).date()


def tomorrow_at(hour: int, minute: int = 0) -> datetime:
    return datetime.combine(today_vn() + timedelta(days=1), time(hour, minute), VN_TZ)


def _user(db, email, role="customer", phone="0900000009") -> User:
    u = User(email=email, password_hash=hash_password("matkhau123"), role=role,
             full_name=f"Người dùng {email}", phone=phone)
    db.add(u)
    db.commit()
    return u


def _client_for(user: User) -> TestClient:
    c = TestClient(app)
    c.cookies.set(COOKIE_NAME, create_access_token(user.id))
    return c


@pytest.fixture
def slots(db, catalog):
    seed_slots(db, today_vn() + timedelta(days=1), days=7)


@pytest.fixture
def customer(db) -> User:
    return _user(db, "a@kh.test", phone="0911111111")


@pytest.fixture
def customer_client(client, customer) -> TestClient:
    return _client_for(customer)


@pytest.fixture
def other_client(client, db) -> TestClient:
    return _client_for(_user(db, "b@kh.test", phone="0922222222"))


@pytest.fixture
def consultant_client(client, db) -> TestClient:
    return _client_for(_user(db, "tvv@mf.test", role="consultant"))


@pytest.fixture
def make_slot(db):
    def _make(hospital_code: str, start_at: datetime, capacity: int = 5, booked_count: int = 0) -> TimeSlot:
        hid = db.scalar(select(Hospital.id).where(Hospital.code == hospital_code))
        s = TimeSlot(hospital_id=hid, start_at=start_at, capacity=capacity, booked_count=booked_count)
        db.add(s)
        db.commit()
        return s
    return _make


@pytest.fixture
def two_customer_ids(db) -> tuple[int, int]:
    return _user(db, "c1@kh.test").id, _user(db, "c2@kh.test").id


@pytest.fixture
def past_booking_id(db, catalog, customer, make_slot) -> int:
    slot = make_slot("ALP", datetime.combine(today_vn() - timedelta(days=1), time(8), VN_TZ), booked_count=1)
    pkg = db.scalar(select(Package).where(Package.code == "ALP-CB01"))
    b = Booking(user_id=customer.id, package_id=pkg.id, slot_id=slot.id, price_snapshot_vnd=pkg.price_vnd)
    db.add(b)
    db.commit()
    return b.id


def first_slot(client, code="ALP-CB01") -> dict:
    return client.get(f"/api/packages/{code}/slots").json()[0]


def book(client, code="ALP-CB01") -> int:
    r = client.post("/api/bookings", json={"package_code": code, "slot_id": first_slot(client, code)["id"]})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_slots_only_from_package_hospital(client, slots, db):
    ids = [s["id"] for s in client.get("/api/packages/GAM-CB01/slots").json()]
    assert ids and {db.get(TimeSlot, i).hospital.code for i in ids} == {"GAM"}


def test_slots_unknown_package_404(client, catalog):
    assert client.get("/api/packages/KHONG-CO/slots").status_code == 404


def test_date_from_is_vietnam_local_day(client, catalog, make_slot):  # Review Focus 2
    d = today_vn() + timedelta(days=3)
    early = make_slot("ALP", datetime.combine(d, time(6, 30), VN_TZ))  # 23:30 UTC hôm trước
    prev_night = make_slot("ALP", datetime.combine(d - timedelta(days=1), time(23, 30), VN_TZ))
    ids = [s["id"] for s in client.get("/api/packages/ALP-CB01/slots", params={"date_from": d.isoformat()}).json()]
    assert early.id in ids and prev_night.id not in ids


def test_full_slot_not_listed(client, catalog, make_slot):
    full = make_slot("ALP", tomorrow_at(9), capacity=2, booked_count=2)
    ids = [s["id"] for s in client.get("/api/packages/ALP-CB01/slots").json()]
    assert full.id not in ids


def test_book_and_price_snapshot(customer_client, slots, db):
    s = first_slot(customer_client)
    r = customer_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": s["id"]})
    assert r.status_code == 201 and r.json()["price_snapshot_vnd"] == 1_200_000
    assert r.json()["channel"] == "web" and r.json()["hospital_code"] == "ALP"
    db.expire_all()
    assert db.get(TimeSlot, s["id"]).booked_count == 1


def test_double_confirm_rejected(customer_client, slots):  # Review Focus 3
    body = {"package_code": "ALP-CB01", "slot_id": first_slot(customer_client)["id"]}
    assert customer_client.post("/api/bookings", json=body).status_code == 201
    assert customer_client.post("/api/bookings", json=body).status_code == 409


@pytest.mark.parametrize("case,status", [("full", 409), ("wrong_hospital", 400), ("past", 400), ("inactive", 404)])
def test_booking_rejections(customer_client, catalog, make_slot, db, two_customer_ids, case, status):
    if case == "full":
        slot = make_slot("ALP", tomorrow_at(7), capacity=1)
        create_booking(db, user_id=two_customer_ids[0], package_code="ALP-CB01", slot_id=slot.id)
    elif case == "wrong_hospital":
        slot = make_slot("GAM", tomorrow_at(7))
    elif case == "past":
        slot = make_slot("ALP", datetime.combine(today_vn() - timedelta(days=1), time(7), VN_TZ))
    else:
        slot = make_slot("ALP", tomorrow_at(7))
        db.execute(update(Package).where(Package.code == "ALP-CB01").values(active=False))
        db.commit()
    r = customer_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": slot.id})
    assert r.status_code == status, r.text


def test_last_spot_concurrency(catalog, make_slot, engine, two_customer_ids, db):
    slot = make_slot("ALP", tomorrow_at(7), capacity=1)
    barrier = threading.Barrier(2)
    results: list[str] = []

    def worker(user_id: int) -> None:
        with Session(engine) as s:
            barrier.wait()
            try:
                create_booking(s, user_id=user_id, package_code="ALP-CB01", slot_id=slot.id)
                results.append("ok")
            except BookingError as e:
                results.append(e.code)

    threads = [threading.Thread(target=worker, args=(uid,)) for uid in two_customer_ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == ["ok", "slot_full"]
    db.expire_all()
    assert db.get(TimeSlot, slot.id).booked_count == 1


def test_create_booking_reads_fresh_slot_under_lock(catalog, make_slot, db, engine, two_customer_ids):
    slot = make_slot("ALP", tomorrow_at(7), capacity=2)
    assert slot.booked_count == 0  # slot nằm sẵn trong session `db`
    with Session(engine) as other:
        create_booking(other, user_id=two_customer_ids[0], package_code="ALP-CB01", slot_id=slot.id)
    create_booking(db, user_id=two_customer_ids[1], package_code="ALP-CB01", slot_id=slot.id)
    db.expire_all()
    assert db.get(TimeSlot, slot.id).booked_count == 2


def test_cancel_booking_reads_fresh_status_under_lock(catalog, make_slot, db, engine, customer):
    slot = make_slot("ALP", tomorrow_at(8), capacity=2)
    b = create_booking(db, user_id=customer.id, package_code="ALP-CB01", slot_id=slot.id)
    assert b.status == "booked"  # booking nằm sẵn trong session `db`
    with Session(engine) as other:
        cancel_booking(other, booking_id=b.id, actor=other.get(User, customer.id))
    with pytest.raises(BookingError) as exc:
        cancel_booking(db, booking_id=b.id, actor=customer)
    assert exc.value.code == "already_cancelled"


def test_cancel_rules(customer_client, other_client, consultant_client, slots, db):
    bid = book(customer_client)
    slot_id = db.get(Booking, bid).slot_id
    assert other_client.post(f"/api/bookings/{bid}/cancel").status_code == 404
    assert customer_client.post(f"/api/bookings/{bid}/cancel").json()["status"] == "cancelled"
    db.expire_all()
    assert db.get(TimeSlot, slot_id).booked_count == 0
    assert customer_client.post(f"/api/bookings/{bid}/cancel").status_code == 409
    bid2 = book(customer_client)
    assert consultant_client.post(f"/api/consultant/bookings/{bid2}/cancel").status_code == 200


def test_rebook_after_cancel_allowed(customer_client, slots):
    bid = book(customer_client)
    customer_client.post(f"/api/bookings/{bid}/cancel")
    book(customer_client)


def test_cannot_cancel_past_booking(customer_client, past_booking_id, db):  # Review Focus 4
    before = db.get(Booking, past_booking_id).slot.booked_count
    assert customer_client.post(f"/api/bookings/{past_booking_id}/cancel").status_code == 400
    db.expire_all()
    assert db.get(Booking, past_booking_id).slot.booked_count == before
    assert db.get(Booking, past_booking_id).status == "booked"


def test_lists_are_scoped(customer_client, other_client, consultant_client, slots):
    book(customer_client)
    book(other_client, "GAM-CB01")
    assert len(customer_client.get("/api/bookings").json()) == 1
    rows = consultant_client.get("/api/consultant/bookings").json()
    assert len(rows) == 2 and all(r["customer_phone"] for r in rows)
    gam = consultant_client.get("/api/consultant/bookings", params={"hospital": "GAM"}).json()
    assert [r["hospital_code"] for r in gam] == ["GAM"]


def test_consultant_filter_by_date_and_status(customer_client, consultant_client, slots, db):
    bid = book(customer_client)
    day = db.get(Booking, bid).slot.start_at.astimezone(VN_TZ).date()
    assert len(consultant_client.get("/api/consultant/bookings", params={"date": day.isoformat()}).json()) == 1
    other_day = (day + timedelta(days=1)).isoformat()
    assert consultant_client.get("/api/consultant/bookings", params={"date": other_day}).json() == []
    customer_client.post(f"/api/bookings/{bid}/cancel")
    assert consultant_client.get("/api/consultant/bookings", params={"status": "booked"}).json() == []


def test_checklist(customer_client, other_client, slots):
    bid = book(customer_client)
    items = customer_client.get(f"/api/bookings/{bid}/checklist").json()
    assert items[0]["text"].startswith("Nhịn ăn ít nhất 8 tiếng")
    assert items[-2]["text"] == "Mang theo CCCD hoặc giấy tờ tùy thân"
    assert items[-1]["text"] == "Đến trước giờ hẹn 15 phút để làm thủ tục"
    texts = [i["text"] for i in items]
    assert len(texts) == len(set(texts))
    assert other_client.get(f"/api/bookings/{bid}/checklist").status_code == 404


def test_role_guards(client, customer_client, consultant_client, slots):
    assert client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": 1}).status_code == 401
    assert client.get("/api/consultant/bookings").status_code == 401
    assert customer_client.get("/api/consultant/bookings").status_code == 403
    assert consultant_client.post("/api/bookings", json={"package_code": "ALP-CB01", "slot_id": 1}).status_code == 403
