"""Bệnh viện, lọc/chi tiết/so sánh gói."""
from typing import Literal

from sqlalchemy import any_, literal, or_, select
from sqlalchemy.orm import Session, contains_eager, selectinload

from app.models import Hospital, Package
from app.schemas import CompareOut, CompareRow, PackageSummary
from app.textnorm import slug_vi


class CatalogError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code)
        self.code = code
        self.detail = detail


def list_hospitals(db: Session, city: str | None = None) -> list[Hospital]:
    q = select(Hospital).where(Hospital.active).order_by(Hospital.name)
    if city:
        q = q.where(Hospital.city_slug == slug_vi(city))
    return list(db.scalars(q))


def get_hospital(db: Session, code: str) -> Hospital | None:
    return db.scalar(select(Hospital).where(Hospital.code == code.upper(), Hospital.active))


def _active_packages():
    return (
        select(Package)
        .join(Package.hospital)
        .where(Package.active, Hospital.active)
        .options(contains_eager(Package.hospital))
    )


def search_packages(
    db: Session,
    *,
    hospital_code: str | None = None,
    city: str | None = None,
    tag: str | None = None,
    gender: Literal["male", "female"] | None = None,
    age: int | None = None,
    price_max: int | None = None,
) -> list[Package]:
    q = _active_packages()
    if hospital_code:
        q = q.where(Hospital.code == hospital_code.upper())
    if city:
        q = q.where(Hospital.city_slug == slug_vi(city))
    if tag:
        q = q.where(literal(tag) == any_(Package.tags))
    if gender:
        q = q.where(Package.gender_scope.in_(("any", gender)))
    if age is not None:
        q = q.where(Package.age_min <= age, or_(Package.age_max.is_(None), Package.age_max >= age))
    if price_max is not None:
        q = q.where(Package.price_vnd <= price_max)
    return list(db.scalars(q.order_by(Package.price_vnd, Package.code)))


def get_package(db: Session, code: str) -> Package | None:
    q = _active_packages().where(Package.code == code.upper()).options(selectinload(Package.items))
    return db.scalar(q)


def compare_packages(db: Session, codes: list[str]) -> CompareOut:
    codes = list(dict.fromkeys(c.strip().upper() for c in codes if c.strip()))
    if not 2 <= len(codes) <= 3:
        raise CatalogError("compare_count")
    packages = []
    for code in codes:
        p = get_package(db, code)
        if p is None:
            raise CatalogError("package_not_found", code)
        packages.append(p)

    items = {i.code: i for p in packages for i in p.items}
    owned = [{i.code for i in p.items} for p in packages]
    rows = [
        CompareRow(item_code=i.code, item_name=i.name, category=i.category,
                   included=[i.code in s for s in owned])
        for i in sorted(items.values(), key=lambda i: (i.category, i.name))
    ]
    return CompareOut(packages=[PackageSummary.of(p) for p in packages], rows=rows)
