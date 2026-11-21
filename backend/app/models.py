"""Các bảng SQLAlchemy."""
from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _enum(*values: str, name: str) -> Enum:
    # VARCHAR + CHECK thay vì enum type của Postgres, để migration thêm giá trị dễ hơn.
    return Enum(*values, name=name, native_enum=False, create_constraint=True, length=20)


class Base(DeclarativeBase):
    pass


def _pk() -> Mapped[int]:
    return mapped_column(BigInteger, Identity(always=True), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = _pk()
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(_enum("customer", "consultant", name="user_role"))
    full_name: Mapped[str] = mapped_column(String)
    birth_date: Mapped[date | None] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column(_enum("male", "female", name="user_gender"))
    phone: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[int] = _pk()
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    city_slug: Mapped[str] = mapped_column(String, index=True)
    address: Mapped[str] = mapped_column(String, default="")
    phone: Mapped[str] = mapped_column(String, default="")
    description: Mapped[str] = mapped_column(Text, default="")
    active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    packages: Mapped[list["Package"]] = relationship(back_populates="hospital", order_by="Package.price_vnd")


package_items = Table(
    "package_items",
    Base.metadata,
    Column("package_id", BigInteger, ForeignKey("packages.id", ondelete="CASCADE"), primary_key=True),
    Column("item_id", BigInteger, ForeignKey("service_items.id", ondelete="CASCADE"), primary_key=True, index=True),
)


class ServiceItem(Base):
    __tablename__ = "service_items"

    id: Mapped[int] = _pk()
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    prep_instruction: Mapped[str] = mapped_column(Text, default="")
    fasting_hours: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (CheckConstraint("fasting_hours >= 0", name="ck_service_items_fasting_hours"),)


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = _pk()
    code: Mapped[str] = mapped_column(String, unique=True)
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    price_vnd: Mapped[int] = mapped_column(Integer)
    gender_scope: Mapped[str] = mapped_column(_enum("any", "male", "female", name="package_gender_scope"))
    age_min: Mapped[int] = mapped_column(Integer, default=0)
    age_max: Mapped[int | None] = mapped_column(Integer)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, server_default="{}")
    active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    hospital: Mapped[Hospital] = relationship(back_populates="packages")
    items: Mapped[list[ServiceItem]] = relationship(secondary=package_items, order_by=ServiceItem.id)

    __table_args__ = (
        CheckConstraint("price_vnd >= 0", name="ck_packages_price"),
        CheckConstraint("age_max is null or age_max >= age_min", name="ck_packages_age_range"),
    )


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id: Mapped[int] = _pk()
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    capacity: Mapped[int] = mapped_column(Integer)
    booked_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    hospital: Mapped[Hospital] = relationship()

    __table_args__ = (
        UniqueConstraint("hospital_id", "start_at", name="uq_time_slots_hospital_start"),
        CheckConstraint("capacity > 0", name="ck_time_slots_capacity"),
        CheckConstraint("booked_count >= 0 and booked_count <= capacity", name="ck_time_slots_booked"),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = _pk()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"), index=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("time_slots.id"), index=True)
    status: Mapped[str] = mapped_column(_enum("booked", "cancelled", name="booking_status"), default="booked")
    price_snapshot_vnd: Mapped[int] = mapped_column(Integer)
    channel: Mapped[str] = mapped_column(_enum("web", "assistant", name="booking_channel"), default="web")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship()
    package: Mapped[Package] = relationship()
    slot: Mapped[TimeSlot] = relationship()

    __table_args__ = (
        # Chặn ở tầng DB việc bấm xác nhận 2 lần tạo 2 lịch hẹn trùng.
        Index(
            "uq_bookings_active",
            "user_id", "package_id", "slot_id",
            unique=True,
            postgresql_where=text("status = 'booked'"),
        ),
    )
