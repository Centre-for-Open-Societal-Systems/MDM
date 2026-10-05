import importlib
import logging
from typing import Optional

from openg2p_fastapi_common.service import BaseService
from openg2p_registry_core.services import G2PRegisterDomainService

_logger = logging.getLogger("g2p-catalog-register-domain-factory")


class G2PRegisterDomainFactory(BaseService):
    """Factory to resolve domain services for catalog registers dynamically."""

    def get_domain_service(self, register_mnemonic: str) -> Optional[G2PRegisterDomainService]:
        try:
            module = importlib.import_module("openg2p_registry_catalog_extension.register_domain.services")
            register_class_prefix: str = "G2PRegisterDomainService"
            implementation_class_name: str = f"{register_class_prefix}{register_mnemonic}"
            implementation_class = getattr(module, implementation_class_name)
            _logger.info(
                f"Found specific catalog service implementation for '{register_mnemonic}': {implementation_class_name}"
            )
            g2p_register_domain_service: G2PRegisterDomainService = implementation_class.get_component()
            if not g2p_register_domain_service:
                g2p_register_domain_service = implementation_class()
            return g2p_register_domain_service
        except (AttributeError, ModuleNotFoundError) as error:
            _logger.warning(
                f"Could not find catalog implementation for register mnemonic '{register_mnemonic}': {error}."
            )
            return None
