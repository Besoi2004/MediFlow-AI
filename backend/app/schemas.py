"""Pydantic schema cho request/response."""
import re
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, field_validator

from app.models import Booking, Package
from app.textnorm import today_vn

Gender = Literal["male", "female"]

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_email(v: str) -> str:
    # Không dùng EmailStr: email-validator từ chối tên miền .test của tài khoản mẫu.
    v = v.strip().lower()
    if not _EMAIL_RE.match(v):
        raise ValueError("Email không hợp lệ")
    return v


Email = Annotated[str, AfterValidator(_normalize_email)]


class RegisterIn(BaseModel):
    email: Email
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=100)
    birth_date: date
    gender: Gender
    phone: str = Field(pattern=r"^\+?\d{8,15}$")

    @field_validator("phone", mode="before")
    @classmethod
    def _compact_phone(cls, v: object) -> object:
        return re.sub(r"[\s.\-]", "", v) if isinstance(v, str) else v

    @field_validator("full_name")
    @classmethod
    def _strip_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Họ tên không được để trống")
        return v.strip()

    @field_validator("birth_date")
    @classmethod
    def _past_birth_date(cls, v: date) -> date:
        if not date(1900, 1, 1) <= v < today_vn():
            raise ValueError("Ngày sinh không hợp lệ")
        return v


class LoginIn(BaseModel):
    email: Email
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: Literal["customer", "consultant"]
    birth_date: date | None
    gender: Gender | None
    phone: str | None


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


class SlotOut(BaseModel):
    id: int
    start_at: datetime
    remaining: int


class BookingIn(BaseModel):
    package_code: str
    slot_id: int


class BookingOut(BaseModel):
    id: int
    status: Literal["booked", "cancelled"]
    channel: Literal["web", "assistant"]
    package_code: str
    package_name: str
    hospital_code: str
    hospital_name: str
    start_at: datetime
    price_snapshot_vnd: int
    created_at: datetime

    @classmethod
    def of(cls, b: Booking) -> "BookingOut":
        return cls(
            id=b.id, status=b.status, channel=b.channel,
            package_code=b.package.code, package_name=b.package.name,
            hospital_code=b.package.hospital.code, hospital_name=b.package.hospital.name,
            start_at=b.slot.start_at, price_snapshot_vnd=b.price_snapshot_vnd, created_at=b.created_at,
        )


class ConsultantBookingOut(BookingOut):
    customer_name: str
    customer_phone: str | None
    customer_email: str

    @classmethod
    def of(cls, b: Booking) -> "ConsultantBookingOut":
        return cls(
            **BookingOut.of(b).model_dump(),
            customer_name=b.user.full_name, customer_phone=b.user.phone, customer_email=b.user.email,
        )


class ChecklistItem(BaseModel):
    text: str
    items: list[str]
