"""Nạp dữ liệu mô phỏng vào DB: bệnh viện, gói, khung giờ, tài khoản mẫu.

Chạy: uv run python -m scripts.seed  (chạy lại nhiều lần được)
"""
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path

import yaml
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Hospital, Package, ServiceItem, TimeSlot
from app.textnorm import VN_TZ, slug_vi

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SLOT_HOURS = (7, 8, 9, 10)
SLOT_CAPACITY = 5


def _load(data_dir: Path, name: str) -> list[dict]:
    return yaml.safe_load((data_dir / name).read_text(encoding="utf-8"))


def _upsert(db: Session, model, code: str):
    obj = db.scalar(select(model).where(model.code == code))
    if obj is None:
        obj = model(code=code)
        db.add(obj)
    return obj


def seed_catalog(db: Session, data_dir: Path = DATA_DIR) -> None:
    hospitals = {}
    for row in _load(data_dir, "hospitals.yaml"):
        h = _upsert(db, Hospital, row["code"])
        h.name, h.city, h.city_slug = row["name"], row["city"], slug_vi(row["city"])
        h.address, h.phone, h.description = row["address"], row["phone"], row["description"]
        h.active = True
        hospitals[h.code] = h

    items = {}
    for row in _load(data_dir, "service_items.yaml"):
        it = _upsert(db, ServiceItem, row["code"])
        it.name, it.category = row["name"], row["category"]
        it.prep_instruction, it.fasting_hours = row["prep_instruction"], row["fasting_hours"]
        items[it.code] = it

    for row in _load(data_dir, "packages.yaml"):
        p = _upsert(db, Package, row["code"])
        p.hospital = hospitals[row["hospital"]]
        p.name, p.description, p.price_vnd = row["name"], row["description"], row["price_vnd"]
        p.gender_scope, p.age_min, p.age_max = row["gender_scope"], row["age_min"], row["age_max"]
        p.tags, p.active = row["tags"], True
        p.items = [items[c] for c in row["items"]]

    db.commit()


def seed_slots(db: Session, start: date, days: int = 14) -> None:
    """Khung 07–10h giờ Việt Nam, Thứ 2–Thứ 7, cho mọi bệnh viện; bỏ qua khung đã có."""
    rows = [
        {"hospital_id": hid, "start_at": datetime.combine(day, time(h), VN_TZ),
         "capacity": SLOT_CAPACITY, "booked_count": 0}
        for hid in db.scalars(select(Hospital.id).where(Hospital.active))
        for day in (start + timedelta(days=i) for i in range(days))
        if day.weekday() < 6
        for h in SLOT_HOURS
    ]
    if rows:
        db.execute(insert(TimeSlot).values(rows).on_conflict_do_nothing(index_elements=["hospital_id", "start_at"]))
    db.commit()


def main() -> None:
    from app.db import SessionLocal

    sys.stdout.reconfigure(encoding="utf-8")  # Windows: pipe mặc định cp1252, in tiếng Việt bị lỗi
    with SessionLocal() as db:
        seed_catalog(db)
        seed_slots(db, datetime.now(VN_TZ).date())
        print("Đã seed danh mục và khung giờ 14 ngày tới.")


if __name__ == "__main__":
    main()
