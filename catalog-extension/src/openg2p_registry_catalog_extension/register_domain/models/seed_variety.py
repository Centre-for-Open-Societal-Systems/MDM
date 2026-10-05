from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class SeedVariety(BaseORMModel):
    """Seed Variety lookup data model representing registered seed varieties."""

    __tablename__ = "seed_varieties"

    variety_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    variety_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    variety_name: Mapped[str] = mapped_column(String(200), nullable=False)
    seed_crop_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    seed_crop_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    breeder_source: Mapped[str] = mapped_column(String(200), nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    maturity_days: Mapped[int] = mapped_column(Integer, nullable=True)
    potential_yield: Mapped[str] = mapped_column(String(100), nullable=True)
    yield_unit: Mapped[str] = mapped_column(String(50), default="Quintal/Ha", nullable=True)
    match_status: Mapped[str] = mapped_column(String(50), default="UNRESOLVED", nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_certified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
