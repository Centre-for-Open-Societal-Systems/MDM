from openg2p_registry_core.config import Settings as CoreSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(CoreSettings):
    model_config = SettingsConfigDict(
        env_prefix="registry_catalog_extensions_", env_file=".env", extra="allow"
    )

    openapi_title: str = "OpenG2P Registry Catalog Extension"
    openapi_description: str = """
        FastAPI Service for OpenG2P Catalog Registers
        ***********************************************
        Provides Master Reference Registers including:
        - Crop Catalog
        - Seed Variety Catalog
        - Fertilizer / Agri-Input Catalog
        - Livestock Breed Catalog
        ***********************************************
        """
    openapi_version: str = __version__
