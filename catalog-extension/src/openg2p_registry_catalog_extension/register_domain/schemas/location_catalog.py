from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaLocationCatalog:
    location_code: Optional[str] = None
    location_name: Optional[str] = None
    admin_level: Optional[str] = None
    admin_level_code: Optional[str] = None
    parent_location_code: Optional[str] = None
    parent_location_name: Optional[str] = None
    capital_city: Optional[str] = None
    area_sq_km: Optional[float] = None
    population_estimate: Optional[int] = None
    pcode: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class G2PRegisterSchemaLocationCatalog(G2PRegisterBaseSchema, G2PSchemaLocationCatalog):
    """Schema for LocationCatalog register."""
    pass


class G2PRegisterHistorySchemaLocationCatalog(G2PRegisterHistorySchema, G2PSchemaLocationCatalog):
    """Schema for LocationCatalog history."""
    pass


class G2PIntakeFormSchemaLocationCatalog(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaLocationCatalog):
    """Schema for LocationCatalog intake form."""
    pass


class LocationCatalogBase(BaseModel):
    location_code: str = Field(..., max_length=50, description="Unique location identifier code")
    location_name: str = Field(..., max_length=200, description="Name of the administrative location")
    admin_level: str = Field(..., max_length=50, description="Administrative level (Region, Zone, Woreda, Kebele)")
    admin_level_code: Optional[str] = Field(None, max_length=50)
    parent_location_code: Optional[str] = Field(None, max_length=50)
    parent_location_name: Optional[str] = Field(None, max_length=200)
    capital_city: Optional[str] = Field(None, max_length=100)
    area_sq_km: Optional[float] = None
    population_estimate: Optional[int] = None
    pcode: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    is_active: bool = True


class LocationCatalogCreate(LocationCatalogBase):
    pass


class LocationCatalogUpdate(BaseModel):
    location_name: Optional[str] = Field(None, max_length=200)
    admin_level: Optional[str] = Field(None, max_length=50)
    admin_level_code: Optional[str] = None
    parent_location_code: Optional[str] = None
    parent_location_name: Optional[str] = None
    capital_city: Optional[str] = None
    area_sq_km: Optional[float] = None
    population_estimate: Optional[int] = None
    pcode: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class LocationCatalogRead(LocationCatalogBase):
    id: str
    functional_record_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
