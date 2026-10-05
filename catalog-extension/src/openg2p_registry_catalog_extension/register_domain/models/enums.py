from enum import Enum


class CatalogStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DRAFT = "DRAFT"
    RETIRED = "RETIRED"


class CropCategoryEnum(str, Enum):
    CEREAL = "Cereal Crops"
    PULSE = "Pulse Crops"
    OIL = "Oil Crops"
    TUBERS_ROOTS_VEGETABLE = "Tubers, Roots & Vegetable Crops"
    FRUIT = "Fruit Crops"
    FORAGE_PASTURE = "Forage and Pasture Crops"
    OTHER = "Other Crops"


class EcologicalZoneEnum(str, Enum):
    KOLLA = "Kolla"
    WEYNA_DEGA = "Weyna Dega"
    DEGA = "Dega"


class WaterRequirementEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class InputCategoryEnum(str, Enum):
    INORGANIC_FERTILIZER = "INORGANIC_FERTILIZER"
    ORGANIC_FERTILIZER = "ORGANIC_FERTILIZER"
    BIO_FERTILIZER = "BIO_FERTILIZER"
    MICRONUTRIENT = "MICRONUTRIENT"
    SOIL_AMENDMENT = "SOIL_AMENDMENT"
    PESTICIDE = "PESTICIDE"
    INSECTICIDE = "INSECTICIDE"
    HERBICIDE = "HERBICIDE"
    FUNGICIDE = "FUNGICIDE"
    SEED_TREATMENT = "SEED_TREATMENT"
    GROWTH_REGULATOR = "GROWTH_REGULATOR"
    OTHER = "OTHER"


class FertilizerTypeEnum(str, Enum):
    INORGANIC_FERTILIZER = "INORGANIC_FERTILIZER"
    ORGANIC_FERTILIZER = "ORGANIC_FERTILIZER"
    BIO_FERTILIZER = "BIO_FERTILIZER"
    SOIL_AMENDMENT = "SOIL_AMENDMENT"
    MICRONUTRIENT = "MICRONUTRIENT"
    INORGANIC = "INORGANIC"
    ORGANIC = "ORGANIC"


class LivestockSpeciesEnum(str, Enum):
    CATTLE = "CATTLE"
    SHEEP = "SHEEP"
    GOAT = "GOAT"
    POULTRY = "POULTRY"
    CAMEL = "CAMEL"
    EQUINE = "EQUINE"
    SWINE = "SWINE"
    BEE = "BEE"
    OTHER = "OTHER"


class LivestockPurposeEnum(str, Enum):
    DAIRY = "DAIRY"
    MEAT = "MEAT"
    DUAL_PURPOSE = "DUAL_PURPOSE"
    WOOL = "WOOL"
    DRAUGHT = "DRAUGHT"
    EGG = "EGG"
    OTHER = "OTHER"
