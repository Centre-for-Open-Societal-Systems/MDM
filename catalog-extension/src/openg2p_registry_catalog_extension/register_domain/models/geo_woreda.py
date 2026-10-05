from sqlalchemy import Boolean, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class GeoWoreda(BaseORMModel):
    """Administrative Woreda/District model (Level 3)."""

    __tablename__ = "geo_woredas"

    woreda_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    woreda_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    woreda_name: Mapped[str] = mapped_column(String(200), nullable=False)
    pcode: Mapped[str] = mapped_column(String(50), nullable=True)
    zone_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    zone_name: Mapped[str] = mapped_column(String(200), nullable=False)
    region_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    region_name: Mapped[str] = mapped_column(String(200), nullable=False)
    kebeles_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
