"""API danh sách và chi tiết bệnh viện."""
from fastapi import APIRouter, HTTPException

from app.db import DbSession
from app.schemas import HospitalDetailOut, HospitalOut, PackageSummary
from app.services import catalog

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.get("", response_model=list[HospitalOut])
def list_hospitals(db: DbSession, city: str | None = None):
    return catalog.list_hospitals(db, city)


@router.get("/{code}", response_model=HospitalDetailOut)
def hospital_detail(code: str, db: DbSession):
    h = catalog.get_hospital(db, code)
    if h is None:
        raise HTTPException(404, "Không tìm thấy bệnh viện")
    packages = catalog.search_packages(db, hospital_code=h.code)
    return HospitalDetailOut(
        **HospitalOut.model_validate(h).model_dump(),
        packages=[PackageSummary.of(p) for p in packages],
    )
