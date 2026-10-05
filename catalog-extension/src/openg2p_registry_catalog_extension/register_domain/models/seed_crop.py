from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class SeedCrop(BaseORMModel):
    """Seed Crop taxonomy data model representing crops from which seeds and varieties are derived."""

    __tablename__ = "seed_crops"

    crop_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    crop_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    crop_name: Mapped[str] = mapped_column(String(200), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
