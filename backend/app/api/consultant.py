"""API cho tư vấn viên: lịch hẹn (cảnh báo và hội thoại ở Kế hoạch 4)."""
from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query

from app.api.bookings import raise_http
from app.auth import require_role
from app.db import DbSession
from app.models import User
from app.schemas import ConsultantBookingOut
from app.services.booking import BookingError, cancel_booking, list_bookings

router = APIRouter(prefix="/consultant", tags=["consultant"])

Consultant = Annotated[User, Depends(require_role("consultant"))]


@router.get("/bookings", response_model=list[ConsultantBookingOut])
def all_bookings(
    _: Consultant,
    db: DbSession,
    hospital: str | None = None,
    status: Literal["booked", "cancelled"] | None = None,
    on_date: Annotated[date | None, Query(alias="date")] = None,
):
    found = list_bookings(db, hospital_code=hospital, status=status, on_date=on_date)
    return [ConsultantBookingOut.of(b) for b in found]


@router.post("/bookings/{booking_id}/cancel", response_model=ConsultantBookingOut)
def cancel(booking_id: int, user: Consultant, db: DbSession):
    try:
        b = cancel_booking(db, booking_id=booking_id, actor=user)
    except BookingError as e:
        raise_http(e)
    return ConsultantBookingOut.of(b)
