from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaSeedCatalog:
    seed_code: Optional[str] = None
    variety_name: Optional[str] = None
    crop_name: Optional[str] = None
    crop_code: Optional[str] = None
    breeder_source: Optional[str] = None
    release_year: Optional[int] = None
    maturity_days: Optional[int] = None
    potential_yield: Optional[str] = None
    yield_unit: Optional[str] = "Quintal/Ha"
    disease_resistance: Optional[str] = None
    match_status: Optional[str] = "UNRESOLVED"
    description: Optional[str] = None
    is_certified: Optional[bool] = True
    is_active: Optional[bool] = True


class G2PRegisterSchemaSeedCatalog(G2PRegisterBaseSchema, G2PSchemaSeedCatalog):
    """Schema for SeedCatalog register."""
    pass


class G2PRegisterHistorySchemaSeedCatalog(G2PRegisterHistorySchema, G2PSchemaSeedCatalog):
    """Schema for SeedCatalog history."""
    pass


class G2PIntakeFormSchemaSeedCatalog(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaSeedCatalog):
    """Schema for SeedCatalog intake form."""
    pass


class SeedCatalogBase(BaseModel):
    seed_code: str = Field(..., max_length=50)
    variety_name: str = Field(..., max_length=200)
    crop_name: str = Field(..., max_length=200)
    crop_code: Optional[str] = Field(None, max_length=50)
    breeder_source: Optional[str] = Field(None, max_length=200)
    release_year: Optional[int] = None
    maturity_days: Optional[int] = Field(None, ge=1)
    potential_yield: Optional[str] = Field(None, max_length=100)
    yield_unit: Optional[str] = Field("Quintal/Ha", max_length=50)
    disease_resistance: Optional[str] = None
    match_status: Optional[str] = Field("UNRESOLVED", max_length=50)
    description: Optional[str] = None
    is_certified: bool = True
    is_active: bool = True


class SeedCatalogCreate(SeedCatalogBase):
    pass


class SeedCatalogUpdate(BaseModel):
    variety_name: Optional[str] = Field(None, max_length=200)
    crop_name: Optional[str] = Field(None, max_length=200)
    crop_code: Optional[str] = None
    breeder_source: Optional[str] = None
    release_year: Optional[int] = None
    maturity_days: Optional[int] = None
    potential_yield: Optional[str] = None
    yield_unit: Optional[str] = None
    disease_resistance: Optional[str] = None
    match_status: Optional[str] = None
    description: Optional[str] = None
    is_certified: Optional[bool] = None
    is_active: Optional[bool] = None


class SeedCatalogRead(SeedCatalogBase):
    id: str
    functional_record_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
