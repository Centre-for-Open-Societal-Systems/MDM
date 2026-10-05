from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaInputCatalog:
    input_code: Optional[str] = None
    trade_name: Optional[str] = None
    input_category: Optional[str] = None
    nutrient_composition: Optional[str] = None
    manufacturer: Optional[str] = None
    application_method: Optional[str] = None
    recommended_crops: Optional[str] = None
    recommended_dosage: Optional[str] = None
    license_number: Optional[str] = None
    safety_precautions: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class G2PRegisterSchemaInputCatalog(G2PRegisterBaseSchema, G2PSchemaInputCatalog):
    """Schema for InputsCatalog register."""
    pass


class G2PRegisterHistorySchemaInputCatalog(G2PRegisterHistorySchema, G2PSchemaInputCatalog):
    """Schema for InputsCatalog history."""
    pass


class G2PIntakeFormSchemaInputCatalog(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaInputCatalog):
    """Schema for InputsCatalog intake form."""
    pass


class InputCatalogBase(BaseModel):
    input_code: str = Field(..., max_length=50, description="Unique input identifier code")
    trade_name: str = Field(..., max_length=200, description="Brand or trade name of the agro-input")
    input_category: str = Field(..., max_length=100, description="Agro-input classification category")
    nutrient_composition: Optional[str] = Field(None, max_length=200, description="Active ingredient or chemical/nutrient composition")
    manufacturer: Optional[str] = Field(None, max_length=200, description="Manufacturer, formulator or licensed importer")
    application_method: Optional[str] = Field(None, max_length=100, description="Method of application")
    recommended_crops: Optional[str] = Field(None, description="Crops for which this input is recommended")
    recommended_dosage: Optional[str] = Field(None, max_length=200, description="Standard recommended application rate or dosage")
    license_number: Optional[str] = Field(None, max_length=100, description="Registration or regulatory license number")
    safety_precautions: Optional[str] = Field(None, description="Pre-harvest interval and safety instructions")
    description: Optional[str] = None
    is_active: bool = True


class InputCatalogCreate(InputCatalogBase):
    pass


class InputCatalogUpdate(BaseModel):
    trade_name: Optional[str] = Field(None, max_length=200)
    input_category: Optional[str] = Field(None, max_length=100)
    nutrient_composition: Optional[str] = None
    manufacturer: Optional[str] = None
    application_method: Optional[str] = None
    recommended_crops: Optional[str] = None
    recommended_dosage: Optional[str] = None
    license_number: Optional[str] = None
    safety_precautions: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class InputCatalogRead(InputCatalogBase):
    id: str
    uuid: Optional[str] = None
    functional_record_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Backward-compatibility aliases
G2PSchemaFertilizerCatalog = G2PSchemaInputCatalog
G2PRegisterSchemaFertilizerCatalog = G2PRegisterSchemaInputCatalog
G2PRegisterHistorySchemaFertilizerCatalog = G2PRegisterHistorySchemaInputCatalog
G2PIntakeFormSchemaFertilizerCatalog = G2PIntakeFormSchemaInputCatalog
FertilizerCatalogBase = InputCatalogBase
FertilizerCatalogRead = InputCatalogRead
