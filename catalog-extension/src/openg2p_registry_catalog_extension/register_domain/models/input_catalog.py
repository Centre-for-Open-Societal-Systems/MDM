from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, synonym
from openg2p_registry_core.models import G2PGeo, G2PGeoHistory, G2PRegister, G2PRegisterHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm

from ..services.g2p_register_domain_service_inputs_catalog import G2PRegisterDomainServiceInputsCatalog


class G2PInputCatalog:
    """Base domain columns for the Inputs Catalog register covering all agro-inputs."""

    input_code: Mapped[str] = mapped_column(String(50), index=True, nullable=True)
    trade_name: Mapped[str] = mapped_column(String(200), index=True, nullable=True)
    input_category: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    nutrient_composition: Mapped[str] = mapped_column(String(200), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=True)
    application_method: Mapped[str] = mapped_column(String(100), nullable=True)
    recommended_crops: Mapped[str] = mapped_column(Text, nullable=True)
    recommended_dosage: Mapped[str] = mapped_column(String(200), nullable=True)
    license_number: Mapped[str] = mapped_column(String(100), nullable=True)
    safety_precautions: Mapped[str] = mapped_column(Text, nullable=True)
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
            "input code": "input_code",
            "code": "input_code",
            "trade name": "trade_name",
            "product name": "trade_name",
            "category": "input_category",
            "input category": "input_category",
            "fertilizer type": "input_category",
            "type": "input_category",
            "nutrient composition": "nutrient_composition",
            "composition": "nutrient_composition",
            "active ingredient": "nutrient_composition",
            "manufacturer": "manufacturer",
            "producer": "manufacturer",
            "supplier": "manufacturer",
            "application method": "application_method",
            "method": "application_method",
            "recommended crops": "recommended_crops",
            "crops": "recommended_crops",
            "recommended dosage": "recommended_dosage",
            "dosage": "recommended_dosage",
            "application rate": "recommended_dosage",
            "license number": "license_number",
            "registration number": "license_number",
            "safety precautions": "safety_precautions",
            "precautions": "safety_precautions",
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
class G2PRegisterInputCatalog(G2PRegister, G2PGeo, G2PInputCatalog):
    __tablename__ = "g2p_register_input_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceInputsCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceInputsCatalog().construct_record_name(self.to_dict())


# Historical Audit Table (auto-versioned on updates)
class G2PRegisterHistoryInputCatalog(G2PRegisterHistory, G2PGeoHistory, G2PInputCatalog):
    __tablename__ = "g2p_register_history_input_catalogs"


# Intake Form Table (for Maker-Checker approval flows)
class G2PIntakeFormInputCatalog(G2PIntakeForm, G2PRegister, G2PGeo, G2PInputCatalog):
    __tablename__ = "g2p_intake_form_input_catalogs"

    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceInputsCatalog().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceInputsCatalog().construct_record_name(self.to_dict())


# Register class-level aliases for UI search and display schemas
for cls in (G2PRegisterInputCatalog, G2PRegisterHistoryInputCatalog, G2PIntakeFormInputCatalog):
    setattr(cls, "Input Code", synonym("input_code"))
    setattr(cls, "Trade Name", synonym("trade_name"))
    setattr(cls, "Category", synonym("input_category"))
    setattr(cls, "Input Category", synonym("input_category"))
    setattr(cls, "Composition", synonym("nutrient_composition"))
    setattr(cls, "Nutrient / Chemical Composition", synonym("nutrient_composition"))
    setattr(cls, "Manufacturer", synonym("manufacturer"))
    setattr(cls, "Application Method", synonym("application_method"))
    setattr(cls, "Recommended Crops", synonym("recommended_crops"))
    setattr(cls, "Dosage", synonym("recommended_dosage"))
    setattr(cls, "License / Reg No", synonym("license_number"))
    setattr(cls, "Active", synonym("is_active"))
    setattr(cls, "Active Status", synonym("is_active"))
    setattr(cls, "fertilizer_type", synonym("input_category"))


# Backward-compatibility and mnemonic aliases (InputsCatalog and InputCatalog)
G2PRegisterInputsCatalog = G2PRegisterInputCatalog
G2PRegisterHistoryInputsCatalog = G2PRegisterHistoryInputCatalog
G2PIntakeFormInputsCatalog = G2PIntakeFormInputCatalog

G2PRegisterFertilizerCatalog = G2PRegisterInputCatalog
G2PRegisterHistoryFertilizerCatalog = G2PRegisterHistoryInputCatalog
G2PIntakeFormFertilizerCatalog = G2PIntakeFormInputCatalog
