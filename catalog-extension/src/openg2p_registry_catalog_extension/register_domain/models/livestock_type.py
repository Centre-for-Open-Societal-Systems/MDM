from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class LivestockType(BaseORMModel):
    """Livestock Type / Species data model (Cattle, Sheep, Goat, Camel, Beehive)."""

    __tablename__ = "livestock_types"

    type_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    type_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    type_name: Mapped[str] = mapped_column(String(200), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(200), nullable=True)
    subfamily: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    ear_tag_range: Mapped[str] = mapped_column(String(100), nullable=True)
    species_type_code: Mapped[int] = mapped_column(Integer, nullable=True)
    in_lis_population: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    in_etlits_registry: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
