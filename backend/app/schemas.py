"""Pydantic schema cho request/response."""
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.models import Package

Gender = Literal["male", "female"]


class HospitalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    city: str
    address: str
    phone: str
    description: str


class PackageSummary(BaseModel):
    code: str
    name: str
    hospital_code: str
    hospital_name: str
    city: str
    price_vnd: int
    gender_scope: Literal["any", "male", "female"]
    age_min: int
    age_max: int | None
    tags: list[str]

    @classmethod
    def of(cls, p: Package) -> "PackageSummary":
        return cls(
            code=p.code, name=p.name, hospital_code=p.hospital.code, hospital_name=p.hospital.name,
            city=p.hospital.city, price_vnd=p.price_vnd, gender_scope=p.gender_scope,
            age_min=p.age_min, age_max=p.age_max, tags=list(p.tags),
        )


class HospitalDetailOut(HospitalOut):
    packages: list[PackageSummary]


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    category: str
    prep_instruction: str
    fasting_hours: int


class PackageDetailOut(PackageSummary):
    description: str
    items: list[ItemOut]

    @classmethod
    def of(cls, p: Package) -> "PackageDetailOut":
        return cls(
            **PackageSummary.of(p).model_dump(),
            description=p.description,
            items=[ItemOut.model_validate(i) for i in p.items],
        )


class CompareRow(BaseModel):
    item_code: str
    item_name: str
    category: str
    included: list[bool]


class CompareOut(BaseModel):
    packages: list[PackageSummary]
    rows: list[CompareRow]
