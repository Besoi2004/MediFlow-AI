"""API đặt, xem, hủy lịch hẹn và checklist chuẩn bị của khách hàng."""
from typing import Annotated, NoReturn

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_role
from app.db import DbSession
from app.models import Booking, User
from app.schemas import BookingIn, BookingOut, ChecklistItem
from app.services.booking import BookingError, cancel_booking, create_booking, list_bookings
from app.services.prep import prep_checklist

router = APIRouter(prefix="/bookings", tags=["bookings"])

Customer = Annotated[User, Depends(require_role("customer"))]

_ERRORS = {
    "package_not_found": (404, "Không tìm thấy gói khám"),
    "slot_not_found": (404, "Không tìm thấy khung giờ"),
    "booking_not_found": (404, "Không tìm thấy lịch hẹn"),
    "slot_wrong_hospital": (400, "Khung giờ không thuộc bệnh viện của gói này"),
    "slot_in_past": (400, "Khung giờ đã qua"),
    "slot_full": (409, "Khung giờ đã hết chỗ"),
    "duplicate_booking": (409, "Bạn đã đặt gói này vào khung giờ này rồi"),
    "already_cancelled": (409, "Lịch hẹn đã được hủy trước đó"),
}


def raise_http(e: BookingError) -> NoReturn:
    status, message = _ERRORS[e.code]
    raise HTTPException(status, message) from e


@router.post("", response_model=BookingOut, status_code=201)
def book(body: BookingIn, user: Customer, db: DbSession):
    try:
        b = create_booking(db, user_id=user.id, package_code=body.package_code, slot_id=body.slot_id)
    except BookingError as e:
        raise_http(e)
    return BookingOut.of(b)


@router.get("", response_model=list[BookingOut])
def my_bookings(user: Customer, db: DbSession):
    return [BookingOut.of(b) for b in list_bookings(db, user_id=user.id)]


@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel(booking_id: int, user: Customer, db: DbSession):
    try:
        b = cancel_booking(db, booking_id=booking_id, actor=user)
    except BookingError as e:
        raise_http(e)
    return BookingOut.of(b)


@router.get("/{booking_id}/checklist", response_model=list[ChecklistItem])
def checklist(booking_id: int, user: Customer, db: DbSession):
    b = db.get(Booking, booking_id)
    if b is None or b.user_id != user.id:
        raise HTTPException(404, "Không tìm thấy lịch hẹn")
    return prep_checklist(b.package)
