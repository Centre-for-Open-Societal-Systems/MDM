from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym
from openg2p_registry_core.models import G2PGeo, G2PGeoHistory, G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services.g2p_register_domain_service_livestock_catalog import (
    G2PRegisterDomainServiceLivestockCatalog,
)


class G2PLivestockCatalog:
    """Base domain columns for the Livestock Breed Catalog register aligned with MDM."""

    breed_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    breed_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    species: Mapped[str] = mapped_column(String(100), index=True, nullable=True)  # Cattle, Sheep, Goat, etc.
    breed_type: Mapped[str] = mapped_column(String(50), default="Indigenous", nullable=True)  # Indigenous, Exotic, Cross
    abbreviation: Mapped[str] = mapped_column(String(20), nullable=True)
    in_national_standard: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    in_etlits_registry: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    primary_purpose: Mapped[str] = mapped_column(String(100), nullable=True)  # DAIRY, MEAT, DUAL_PURPOSE, etc.
    origin_country: Mapped[str] = mapped_column(String(100), nullable=True)
    climate_tolerance: Mapped[str] = mapped_column(String(100), nullable=True)
    climate_adaptability: Mapped[str] = mapped_column(String(200), nullable=True)
    average_mature_weight_kg: Mapped[float] = mapped_column(Float, nullable=True)
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
            "breed code": "breed_code",
            "code": "breed_code",
            "breed name": "breed_name",
            "name": "breed_name",
            "species": "species",
            "breed type": "breed_type",
            "type": "breed_type",
            "abbreviation": "abbreviation",
            "national standard": "in_national_standard",
            "in national standard": "in_national_standard",
            "et-lits": "in_etlits_registry",
            "in etlits registry": "in_etlits_registry",
            "primary purpose": "primary_purpose",
            "purpose": "primary_purpose",
            "origin country": "origin_country",
            "origin": "origin_country",
            "climate tolerance": "climate_tolerance",
            "active": "is_active",
            "status": "is_active",
            "active status": "is_active",
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


class G2PRegisterLivestockCatalog(G2PRegister, G2PGeo, G2PLivestockCatalog):
    __tablename__ = "g2p_register_livestock_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceLivestockCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceLivestockCatalog().construct_record_name(self.to_dict())


class G2PRegisterHistoryLivestockCatalog(G2PRegisterHistory, G2PGeoHistory, G2PLivestockCatalog):
    __tablename__ = "g2p_register_history_livestock_catalogs"


class G2PIntakeFormLivestockCatalog(G2PIntakeForm, G2PRegister, G2PGeo, G2PLivestockCatalog):
    __tablename__ = "g2p_intake_form_livestock_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceLivestockCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceLivestockCatalog().construct_record_name(self.to_dict())


for cls in (G2PRegisterLivestockCatalog, G2PRegisterHistoryLivestockCatalog, G2PIntakeFormLivestockCatalog):
    setattr(cls, "Breed Code", synonym("breed_code"))
    setattr(cls, "Breed Name", synonym("breed_name"))
    setattr(cls, "Species", synonym("species"))
    setattr(cls, "Breed Type", synonym("breed_type"))
    setattr(cls, "Abbreviation", synonym("abbreviation"))
    setattr(cls, "Primary Purpose", synonym("primary_purpose"))
    setattr(cls, "National Standard", synonym("in_national_standard"))
    setattr(cls, "ET-LITS", synonym("in_etlits_registry"))
    setattr(cls, "Active Status", synonym("is_active"))
