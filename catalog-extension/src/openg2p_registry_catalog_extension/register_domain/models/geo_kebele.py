from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class GeoKebele(BaseORMModel):
    """Administrative Kebele/Ward model (Level 4)."""

    __tablename__ = "geo_kebeles"

    kebele_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    kebele_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    kebele_name: Mapped[str] = mapped_column(String(200), nullable=False)
    pcode: Mapped[str] = mapped_column(String(50), nullable=True)
    woreda_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    woreda_name: Mapped[str] = mapped_column(String(200), nullable=False)
    zone_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    zone_name: Mapped[str] = mapped_column(String(200), nullable=False)
    region_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    region_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
