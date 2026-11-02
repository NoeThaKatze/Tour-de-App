from sqlalchemy import Boolean, Float, ForeignKey, String, false
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Product(Base):
    __tablename__: str = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)


class Team(Base):
    __tablename__: str = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Member(Base):
    __tablename__: str = "member"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Stop(Base):
    __tablename__: str = "stop"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    x: Mapped[float | None] = mapped_column(Float, nullable=True)
    y: Mapped[float | None] = mapped_column(Float, nullable=True)
    wheelchair_accessible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    has_shelter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    has_bench: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    has_ticket_machine: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    has_display: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
