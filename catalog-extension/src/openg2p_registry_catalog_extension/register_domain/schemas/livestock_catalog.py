from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaLivestockCatalog:
    breed_code: Optional[str] = None
    breed_name: Optional[str] = None
    species: Optional[str] = None
    breed_type: Optional[str] = "Indigenous"
    abbreviation: Optional[str] = None
    in_national_standard: Optional[bool] = True
    in_etlits_registry: Optional[bool] = False
    primary_purpose: Optional[str] = None
    origin_country: Optional[str] = None
    climate_tolerance: Optional[str] = None
    climate_adaptability: Optional[str] = None
    average_mature_weight_kg: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class G2PRegisterSchemaLivestockCatalog(G2PRegisterBaseSchema, G2PSchemaLivestockCatalog):
    """Schema for LivestockCatalog register."""
    pass


class G2PRegisterHistorySchemaLivestockCatalog(G2PRegisterHistorySchema, G2PSchemaLivestockCatalog):
    """Schema for LivestockCatalog history."""
    pass


class G2PIntakeFormSchemaLivestockCatalog(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaLivestockCatalog):
    """Schema for LivestockCatalog intake form."""
    pass


class LivestockCatalogBase(BaseModel):
    breed_code: str = Field(..., max_length=50)
    breed_name: str = Field(..., max_length=200)
    species: str = Field(..., max_length=100)
    breed_type: Optional[str] = Field("Indigenous", max_length=50)
    abbreviation: Optional[str] = Field(None, max_length=20)
    in_national_standard: Optional[bool] = True
    in_etlits_registry: Optional[bool] = False
    primary_purpose: Optional[str] = Field(None, max_length=100)
    origin_country: Optional[str] = Field(None, max_length=100)
    climate_tolerance: Optional[str] = Field(None, max_length=100)
    climate_adaptability: Optional[str] = Field(None, max_length=200)
    average_mature_weight_kg: Optional[float] = Field(None, ge=0.0)
    description: Optional[str] = None
    is_active: bool = True


class LivestockCatalogCreate(LivestockCatalogBase):
    pass


class LivestockCatalogUpdate(BaseModel):
    breed_name: Optional[str] = Field(None, max_length=200)
    species: Optional[str] = None
    breed_type: Optional[str] = None
    abbreviation: Optional[str] = None
    in_national_standard: Optional[bool] = None
    in_etlits_registry: Optional[bool] = None
    primary_purpose: Optional[str] = None
    origin_country: Optional[str] = None
    climate_tolerance: Optional[str] = None
    climate_adaptability: Optional[str] = None
    average_mature_weight_kg: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class LivestockCatalogRead(LivestockCatalogBase):
    id: str
    functional_record_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
