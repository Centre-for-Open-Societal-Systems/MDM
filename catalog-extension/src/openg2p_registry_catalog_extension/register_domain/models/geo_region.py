from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class GeoRegion(BaseORMModel):
    """Administrative Region model (Level 1)."""

    __tablename__ = "geo_regions"

    region_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    region_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    region_name: Mapped[str] = mapped_column(String(200), nullable=False)
    pcode: Mapped[str] = mapped_column(String(50), nullable=True)
    capital: Mapped[str] = mapped_column(String(100), nullable=True)
    area_sq_km: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    zones_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    woredas_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    kebeles_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
