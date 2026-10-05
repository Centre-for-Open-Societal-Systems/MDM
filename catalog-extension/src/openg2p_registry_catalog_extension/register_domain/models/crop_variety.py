from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class CropVariety(BaseORMModel):
    """Crop Variety data model representing individual varieties belonging to crops."""

    __tablename__ = "crop_varieties"

    variety_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    variety_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    variety_name: Mapped[str] = mapped_column(String(200), nullable=False)
    crop_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    crop_name: Mapped[str] = mapped_column(String(200), nullable=True)
    scientific_name: Mapped[str] = mapped_column(String(200), nullable=True)
    breeder_source: Mapped[str] = mapped_column(String(200), nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    maturity_days: Mapped[int] = mapped_column(Integer, nullable=True)
    potential_yield: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    yield_unit: Mapped[str] = mapped_column(String(50), nullable=True)
    is_certified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
