from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym
from openg2p_registry_core.models import G2PGeo, G2PGeoHistory, G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services.g2p_register_domain_service_seed_catalog import G2PRegisterDomainServiceSeedCatalog


class G2PSeedCatalog:
    """Base domain columns for the Seed Variety Catalog register aligned with MDM."""

    seed_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    variety_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    crop_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    crop_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    breeder_source: Mapped[str] = mapped_column(String(200), nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    maturity_days: Mapped[int] = mapped_column(Integer, nullable=True)
    potential_yield: Mapped[str] = mapped_column(String(100), nullable=True)
    yield_unit: Mapped[str] = mapped_column(String(50), default="Quintal/Ha", nullable=True)
    disease_resistance: Mapped[str] = mapped_column(Text, nullable=True)
    match_status: Mapped[str] = mapped_column(String(50), default="UNRESOLVED", nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_certified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
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
            "seed code": "seed_code",
            "variety name": "variety_name",
            "variety": "variety_name",
            "parent crop": "crop_name",
            "crop name": "crop_name",
            "crop": "crop_name",
            "seed crop": "crop_name",
            "breeder / source": "breeder_source",
            "breeder": "breeder_source",
            "maintainer": "breeder_source",
            "release year": "release_year",
            "release": "release_year",
            "maturity (days)": "maturity_days",
            "maturity": "maturity_days",
            "match status": "match_status",
            "match": "match_status",
            "potential yield": "potential_yield",
            "yield": "potential_yield",
            "yield unit": "yield_unit",
            "disease resistance": "disease_resistance",
            "certified": "is_certified",
            "is certified": "is_certified",
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


class G2PRegisterSeedCatalog(G2PRegister, G2PGeo, G2PSeedCatalog):
    __tablename__ = "g2p_register_seed_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSeedCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSeedCatalog().construct_record_name(self.to_dict())


class G2PRegisterHistorySeedCatalog(G2PRegisterHistory, G2PGeoHistory, G2PSeedCatalog):
    __tablename__ = "g2p_register_history_seed_catalogs"


class G2PIntakeFormSeedCatalog(G2PIntakeForm, G2PRegister, G2PGeo, G2PSeedCatalog):
    __tablename__ = "g2p_intake_form_seed_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceSeedCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceSeedCatalog().construct_record_name(self.to_dict())


for cls in (G2PRegisterSeedCatalog, G2PRegisterHistorySeedCatalog, G2PIntakeFormSeedCatalog):
    setattr(cls, "Seed Code", synonym("seed_code"))
    setattr(cls, "Variety Name", synonym("variety_name"))
    setattr(cls, "Parent Crop", synonym("crop_name"))
    setattr(cls, "Crop Name", synonym("crop_name"))
    setattr(cls, "Breeder / Source", synonym("breeder_source"))
    setattr(cls, "Release Year", synonym("release_year"))
    setattr(cls, "Match Status", synonym("match_status"))
    setattr(cls, "Maturity (Days)", synonym("maturity_days"))
    setattr(cls, "Potential Yield", synonym("potential_yield"))
    setattr(cls, "Certified", synonym("is_certified"))
    setattr(cls, "Active Status", synonym("is_active"))
