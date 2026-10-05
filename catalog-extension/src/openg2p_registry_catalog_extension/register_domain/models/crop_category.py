from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class CropCategory(BaseORMModel):
    """Crop Category data model representing crop taxonomy categories."""

    __tablename__ = "crop_categories"

    category_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    category_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
