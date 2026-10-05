from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaCropCatalog:
    crop_code: Optional[str] = None
    crop_name: Optional[str] = None
    scientific_name: Optional[str] = None
    crop_category: Optional[str] = None
    preferred_ecological_zone: Optional[str] = None
    centre: Optional[str] = None
    varieties_count: Optional[int] = 0
    known_for: Optional[str] = None
    growth_cycle_days: Optional[int] = None
    water_requirement: Optional[str] = None
    preferred_soil_type: Optional[str] = None
    num_field_inspection_needed: Optional[int] = None
    isolation_distance: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class G2PRegisterSchemaCropCatalog(G2PRegisterBaseSchema, G2PSchemaCropCatalog):
    """Schema for CropCatalog register."""
    pass


class G2PRegisterHistorySchemaCropCatalog(G2PRegisterHistorySchema, G2PSchemaCropCatalog):
    """Schema for CropCatalog history."""
    pass


class G2PIntakeFormSchemaCropCatalog(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaCropCatalog):
    """Schema for CropCatalog intake form."""
    pass


class CropCatalogBase(BaseModel):
    crop_code: str = Field(..., max_length=50, description="Unique crop identifier code")
    crop_name: str = Field(..., max_length=200, description="Common crop name")
    scientific_name: Optional[str] = Field(None, max_length=200)
    crop_category: Optional[str] = Field(None, max_length=100)
    preferred_ecological_zone: Optional[str] = Field(None, max_length=100)
    centre: Optional[str] = Field(None, max_length=100)
    varieties_count: Optional[int] = Field(0, ge=0)
    known_for: Optional[str] = None
    growth_cycle_days: Optional[int] = Field(None, ge=1, le=1000)
    water_requirement: Optional[str] = Field(None, max_length=50)
    preferred_soil_type: Optional[str] = Field(None, max_length=100)
    num_field_inspection_needed: Optional[int] = Field(None, ge=0)
    isolation_distance: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    is_active: bool = True


class CropCatalogCreate(CropCatalogBase):
    pass


class CropCatalogUpdate(BaseModel):
    crop_name: Optional[str] = Field(None, max_length=200)
    scientific_name: Optional[str] = None
    crop_category: Optional[str] = None
    preferred_ecological_zone: Optional[str] = None
    centre: Optional[str] = None
    varieties_count: Optional[int] = None
    known_for: Optional[str] = None
    growth_cycle_days: Optional[int] = None
    water_requirement: Optional[str] = None
    preferred_soil_type: Optional[str] = None
    num_field_inspection_needed: Optional[int] = None
    isolation_distance: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CropCatalogRead(CropCatalogBase):
    id: str
    functional_record_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
