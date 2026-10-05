from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym
from openg2p_registry_core.models import G2PGeo, G2PGeoHistory, G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services.g2p_register_domain_service_crop_catalog import G2PRegisterDomainServiceCropCatalog


class G2PCropCatalog:
    """Base domain columns for the Crop Catalog register aligned with MDM setup."""

    crop_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    crop_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    scientific_name: Mapped[str] = mapped_column(String(200), nullable=True)
    crop_category: Mapped[str] = mapped_column(String(100), nullable=True)
    preferred_ecological_zone: Mapped[str] = mapped_column(String(100), nullable=True)
    centre: Mapped[str] = mapped_column(String(100), nullable=True)
    varieties_count: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    known_for: Mapped[str] = mapped_column(Text, nullable=True)
    growth_cycle_days: Mapped[int] = mapped_column(Integer, nullable=True)
    water_requirement: Mapped[str] = mapped_column(String(50), nullable=True)
    preferred_soil_type: Mapped[str] = mapped_column(String(100), nullable=True)
    num_field_inspection_needed: Mapped[int] = mapped_column(Integer, nullable=True)
    isolation_distance: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)

    # Flattened administrative geo names for easy searching and tabular display
    region_name: Mapped[str] = mapped_column(String, nullable=True)
    zone_name: Mapped[str] = mapped_column(String, nullable=True)
    woreda_name: Mapped[str] = mapped_column(String, nullable=True)
    kebele_name: Mapped[str] = mapped_column(String, nullable=True)

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        norm = name.lower().strip()
        alias_map = {
            "crop code": "crop_code",
            "crop name": "crop_name",
            "scientific name": "scientific_name",
            "category": "crop_category",
            "crop category": "crop_category",
            "ecological zone": "preferred_ecological_zone",
            "preferred ecological zone": "preferred_ecological_zone",
            "research centre": "centre",
            "centre": "centre",
            "varieties": "varieties_count",
            "varieties count": "varieties_count",
            "growth cycle (days)": "growth_cycle_days",
            "growth cycle": "growth_cycle_days",
            "cycle (days)": "growth_cycle_days",
            "water requirement": "water_requirement",
            "water req": "water_requirement",
            "preferred soil type": "preferred_soil_type",
            "soil type": "preferred_soil_type",
            "active": "is_active",
            "status": "is_active",
            "active status": "is_active",
            "inspections needed": "num_field_inspection_needed",
            "isolation distance": "isolation_distance",
            "region": "region_name",
            "zone": "zone_name",
            "woreda": "woreda_name",
            "kebele": "kebele_name",
        }
        target = alias_map.get(norm, norm.replace(" ", "_").replace("/", "_").replace(".", ""))
        try:
            return object.__getattribute__(self, target)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


# Live Register Table
class G2PRegisterCropCatalog(G2PRegister, G2PGeo, G2PCropCatalog):
    __tablename__ = "g2p_register_crop_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceCropCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceCropCatalog().construct_record_name(self.to_dict())


# Historical Audit Table (auto-versioned on updates)
class G2PRegisterHistoryCropCatalog(G2PRegisterHistory, G2PGeoHistory, G2PCropCatalog):
    __tablename__ = "g2p_register_history_crop_catalogs"


# Intake Form Table (for Maker-Checker approval flows)
class G2PIntakeFormCropCatalog(G2PIntakeForm, G2PRegister, G2PGeo, G2PCropCatalog):
    __tablename__ = "g2p_intake_form_crop_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceCropCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceCropCatalog().construct_record_name(self.to_dict())


# Register class-level aliases for search schemas with spaces
for cls in (G2PRegisterCropCatalog, G2PRegisterHistoryCropCatalog, G2PIntakeFormCropCatalog):
    setattr(cls, "Crop Code", synonym("crop_code"))
    setattr(cls, "Crop Name", synonym("crop_name"))
    setattr(cls, "Scientific Name", synonym("scientific_name"))
    setattr(cls, "Category", synonym("crop_category"))
    setattr(cls, "Ecological Zone", synonym("preferred_ecological_zone"))
    setattr(cls, "Research Centre", synonym("centre"))
    setattr(cls, "Varieties", synonym("varieties_count"))
    setattr(cls, "Cycle (Days)", synonym("growth_cycle_days"))
    setattr(cls, "Water Req.", synonym("water_requirement"))
    setattr(cls, "Active", synonym("is_active"))
    setattr(cls, "Active Status", synonym("is_active"))
