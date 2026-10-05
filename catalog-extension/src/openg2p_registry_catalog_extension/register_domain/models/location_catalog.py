from sqlalchemy import BigInteger, Boolean, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym
from openg2p_registry_core.models import G2PGeo, G2PGeoHistory, G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services.g2p_register_domain_service_location_catalog import G2PRegisterDomainServiceLocationCatalog


class G2PLocationCatalog:
    """Base domain columns for the single Location Catalog register with linked sub-categories."""

    location_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    location_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    admin_level: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    admin_level_code: Mapped[str] = mapped_column(String(50), nullable=True)
    parent_location_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    parent_location_name: Mapped[str] = mapped_column(String(200), nullable=True)
    capital_city: Mapped[str] = mapped_column(String(100), nullable=True)
    area_sq_km: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    population_estimate: Mapped[int] = mapped_column(BigInteger, nullable=True)
    pcode: Mapped[str] = mapped_column(String(50), nullable=True)
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
            "location code": "location_code",
            "code": "location_code",
            "location name": "location_name",
            "name": "location_name",
            "admin level": "admin_level",
            "level": "admin_level",
            "administrative level": "admin_level",
            "admin level code": "admin_level_code",
            "parent location": "parent_location_name",
            "parent location code": "parent_location_code",
            "parent location name": "parent_location_name",
            "parent": "parent_location_name",
            "capital": "capital_city",
            "capital city": "capital_city",
            "area": "area_sq_km",
            "area (sq km)": "area_sq_km",
            "population": "population_estimate",
            "population estimate": "population_estimate",
            "pcode": "pcode",
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


# Live Register Table
class G2PRegisterLocationCatalog(G2PRegister, G2PGeo, G2PLocationCatalog):
    __tablename__ = "g2p_register_location_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceLocationCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceLocationCatalog().construct_record_name(self.to_dict())


# Historical Audit Table (auto-versioned on updates)
class G2PRegisterHistoryLocationCatalog(G2PRegisterHistory, G2PGeoHistory, G2PLocationCatalog):
    __tablename__ = "g2p_register_history_location_catalogs"


# Intake Form Table (for Maker-Checker approval flows)
class G2PIntakeFormLocationCatalog(G2PIntakeForm, G2PRegister, G2PGeo, G2PLocationCatalog):
    __tablename__ = "g2p_intake_form_location_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceLocationCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceLocationCatalog().construct_record_name(self.to_dict())


# Register class-level aliases for search schemas with spaces
for cls in (G2PRegisterLocationCatalog, G2PRegisterHistoryLocationCatalog, G2PIntakeFormLocationCatalog):
    setattr(cls, "Location Code", synonym("location_code"))
    setattr(cls, "Location Name", synonym("location_name"))
    setattr(cls, "Admin Level", synonym("admin_level"))
    setattr(cls, "Parent Location", synonym("parent_location_name"))
    setattr(cls, "Capital City", synonym("capital_city"))
    setattr(cls, "Area (sq km)", synonym("area_sq_km"))
    setattr(cls, "Population", synonym("population_estimate"))
    setattr(cls, "Active", synonym("is_active"))
    setattr(cls, "Active Status", synonym("is_active"))
