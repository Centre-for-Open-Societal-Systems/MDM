from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class LivestockBreed(BaseORMModel):
    """Livestock Breed lookup data model representing standard Ethiopian livestock breeds."""

    __tablename__ = "livestock_breeds"

    breed_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    breed_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    breed_name: Mapped[str] = mapped_column(String(200), nullable=False)
    species_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    species_name: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    breed_type: Mapped[str] = mapped_column(String(50), default="Indigenous", nullable=True)
    abbreviation: Mapped[str] = mapped_column(String(20), nullable=True)
    primary_purpose: Mapped[str] = mapped_column(String(100), nullable=True)
    origin_country: Mapped[str] = mapped_column(String(100), default="Ethiopia", nullable=True)
    climate_adaptability: Mapped[str] = mapped_column(String(200), nullable=True)
    in_national_standard: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    in_etlits_registry: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
