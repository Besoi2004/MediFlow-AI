"""API lọc, chi tiết, so sánh gói khám và khung giờ."""
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.db import DbSession
from app.schemas import CompareOut, Gender, PackageDetailOut, PackageSummary, SlotOut
from app.services import booking, catalog
from app.textnorm import VN_TZ

router = APIRouter(prefix="/packages", tags=["packages"])


@router.get("", response_model=list[PackageSummary])
def search_packages(
    db: DbSession,
    hospital: str | None = None,
    city: str | None = None,
    tag: str | None = None,
    gender: Gender | None = None,
    age: Annotated[int | None, Query(ge=0, le=130)] = None,
    price_max: Annotated[int | None, Query(ge=0)] = None,
):
    found = catalog.search_packages(
        db, hospital_code=hospital, city=city, tag=tag, gender=gender, age=age, price_max=price_max
    )
    return [PackageSummary.of(p) for p in found]


@router.get("/compare", response_model=CompareOut)
def compare_packages(db: DbSession, codes: str):
    try:
        return catalog.compare_packages(db, codes.split(","))
    except catalog.CatalogError as e:
        if e.code == "compare_count":
            raise HTTPException(400, "Chỉ so sánh được 2–3 gói") from e
        raise HTTPException(404, f"Không tìm thấy gói khám {e.detail}") from e


@router.get("/{code}/slots", response_model=list[SlotOut])
def package_slots(code: str, db: DbSession, date_from: date | None = None):
    try:
        slots = booking.list_available_slots(db, code, date_from or datetime.now(VN_TZ).date())
    except booking.BookingError as e:
        raise HTTPException(404, "Không tìm thấy gói khám") from e
    return [SlotOut(id=s.id, start_at=s.start_at, remaining=s.capacity - s.booked_count) for s in slots]


@router.get("/{code}", response_model=PackageDetailOut)
def package_detail(code: str, db: DbSession):
    p = catalog.get_package(db, code)
    if p is None:
        raise HTTPException(404, "Không tìm thấy gói khám")
    return PackageDetailOut.of(p)
