from datetime import date

import pytest
from sqlalchemy import func, select

from app.models import Hospital, Package, TimeSlot
from app.textnorm import VN_TZ, slug_vi
from scripts.seed import DATA_DIR, seed_catalog, seed_slots


@pytest.mark.parametrize("raw,slug", [
    ("Hà Nội", "ha-noi"), ("HÀ NỘI", "ha-noi"), ("ha noi", "ha-noi"),
    ("TP. Hồ Chí Minh", "tp-ho-chi-minh"), ("Đà Nẵng", "da-nang"),
])
def test_slug_vi(raw, slug):
    assert slug_vi(raw) == slug


def test_seed_catalog_is_idempotent(db):
    seed_catalog(db, DATA_DIR)
    seed_catalog(db, DATA_DIR)
    assert db.scalar(select(func.count(Hospital.id))) == 3
    assert db.scalar(select(func.count(Package.id))) == 15
    pkg = db.scalar(select(Package).where(Package.code == "GAM-TIM"))
    assert pkg.price_vnd == 4_600_000 and pkg.hospital.code == "GAM" and pkg.age_min == 40


def test_seed_hospitals_marked_simulated(db):
    seed_catalog(db, DATA_DIR)
    names = db.scalars(select(Hospital.name)).all()
    assert all(n.endswith("(mô phỏng)") for n in names)


def test_seed_slots_local_time_and_weekdays(db):
    seed_catalog(db, DATA_DIR)
    monday = date(2026, 11, 23)  # Thứ 2
    seed_slots(db, monday, days=7)
    seed_slots(db, monday, days=7)
    slots = db.scalars(select(TimeSlot)).all()
    assert len(slots) == 3 * 6 * 4  # 3 BV × T2–T7 × 4 khung
    local = [s.start_at.astimezone(VN_TZ) for s in slots]
    assert {t.hour for t in local} == {7, 8, 9, 10}
    assert all(t.weekday() < 6 for t in local)
