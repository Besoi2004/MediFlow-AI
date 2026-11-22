"""Khung giờ, đặt/hủy lịch có khóa hàng."""
from datetime import UTC, date, datetime, time, timedelta
from typing import Literal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models import Booking, Hospital, Package, TimeSlot, User
from app.services import catalog
from app.textnorm import VN_TZ


class BookingError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _now() -> datetime:
    return datetime.now(UTC)


def _lock(db: Session, model: type[TimeSlot] | type[Booking], row_id: int):
    # populate_existing: đọc lại hàng vừa khóa, không dùng bản cũ đang nằm sẵn trong session.
    q = select(model).where(model.id == row_id).with_for_update().execution_options(populate_existing=True)
    return db.scalar(q)


def _local_day_start(d: date) -> datetime:
    return datetime.combine(d, time(0), VN_TZ)


def list_available_slots(db: Session, package_code: str, date_from: date, days: int = 14) -> list[TimeSlot]:
    package = catalog.get_package(db, package_code)
    if package is None:
        raise BookingError("package_not_found")
    start = _local_day_start(date_from)
    q = (
        select(TimeSlot)
        .where(
            TimeSlot.hospital_id == package.hospital_id,
            TimeSlot.start_at >= start,
            TimeSlot.start_at < start + timedelta(days=days),
            TimeSlot.start_at > _now(),
            TimeSlot.booked_count < TimeSlot.capacity,
        )
        .order_by(TimeSlot.start_at)
    )
    return list(db.scalars(q))


def create_booking(
    db: Session,
    *,
    user_id: int,
    package_code: str,
    slot_id: int,
    channel: Literal["web", "assistant"] = "web",
) -> Booking:
    try:
        package = catalog.get_package(db, package_code)
        if package is None:
            raise BookingError("package_not_found")
        slot = _lock(db, TimeSlot, slot_id)  # hai người không cùng lấy được chỗ cuối
        if slot is None:
            raise BookingError("slot_not_found")
        if slot.hospital_id != package.hospital_id:
            raise BookingError("slot_wrong_hospital")
        if slot.start_at <= _now():
            raise BookingError("slot_in_past")
        duplicate = db.scalar(
            select(Booking.id).where(
                Booking.user_id == user_id, Booking.package_id == package.id,
                Booking.slot_id == slot.id, Booking.status == "booked",
            )
        )
        if duplicate:
            raise BookingError("duplicate_booking")
        if slot.booked_count >= slot.capacity:
            raise BookingError("slot_full")

        slot.booked_count += 1
        booking = Booking(
            user_id=user_id, package_id=package.id, slot_id=slot.id,
            price_snapshot_vnd=package.price_vnd, channel=channel,
        )
        db.add(booking)
        db.commit()
    except BookingError:
        db.rollback()
        raise
    except IntegrityError as e:
        db.rollback()
        if e.orig.diag.constraint_name == "uq_bookings_active":  # chỉ mục chặn bản trùng
            raise BookingError("duplicate_booking") from e
        raise
    return booking


def cancel_booking(db: Session, *, booking_id: int, actor: User) -> Booking:
    try:
        booking = _lock(db, Booking, booking_id)
        if booking is None or (actor.role != "consultant" and booking.user_id != actor.id):
            raise BookingError("booking_not_found")  # không cho biết lịch của người khác có tồn tại
        if booking.status == "cancelled":
            raise BookingError("already_cancelled")
        slot = _lock(db, TimeSlot, booking.slot_id)
        if slot.start_at <= _now():
            raise BookingError("slot_in_past")
        slot.booked_count -= 1
        booking.status = "cancelled"
        db.commit()
    except BookingError:
        db.rollback()
        raise
    return booking


def list_bookings(
    db: Session,
    *,
    user_id: int | None = None,
    hospital_code: str | None = None,
    status: str | None = None,
    on_date: date | None = None,
) -> list[Booking]:
    q = (
        select(Booking)
        .join(Booking.slot)
        .join(Booking.package)
        .join(Package.hospital)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.slot),
            joinedload(Booking.package).joinedload(Package.hospital),
        )
    )
    if user_id is not None:
        q = q.where(Booking.user_id == user_id)
    if hospital_code:
        q = q.where(Hospital.code == hospital_code.upper())
    if status:
        q = q.where(Booking.status == status)
    if on_date:
        start = _local_day_start(on_date)
        q = q.where(TimeSlot.start_at >= start, TimeSlot.start_at < start + timedelta(days=1))
    return list(db.scalars(q.order_by(TimeSlot.start_at, Booking.id)))
