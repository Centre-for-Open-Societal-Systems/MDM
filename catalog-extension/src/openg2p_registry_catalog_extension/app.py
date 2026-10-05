# ruff: noqa: E402
import asyncio
import logging
from sqlalchemy import text
from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_fastapi_common.context import dbengine
from openg2p_registry_core.app import Initializer as CoreInitializer

from .config import Settings
from .register_domain.factory import G2PRegisterDomainFactory
from .register_domain.models import (
    CropCategory,
    CropVariety,
    EcologicalZone,
    G2PIntakeFormCropCatalog,
    G2PIntakeFormInputCatalog,
    G2PIntakeFormLivestockCatalog,
    G2PIntakeFormLocationCatalog,
    G2PIntakeFormSeedCatalog,
    G2PRegisterCropCatalog,
    G2PRegisterHistoryCropCatalog,
    G2PRegisterHistoryInputCatalog,
    G2PRegisterHistoryLivestockCatalog,
    G2PRegisterHistoryLocationCatalog,
    G2PRegisterHistorySeedCatalog,
    G2PRegisterInputCatalog,
    G2PRegisterLivestockCatalog,
    G2PRegisterLocationCatalog,
    G2PRegisterSeedCatalog,
    GeoKebele,
    GeoRegion,
    GeoWoreda,
    GeoZone,
    LivestockBreed,
    LivestockType,
    SeedCrop,
    SeedVariety,
)
from .register_domain.services import (
    G2PRegisterDomainServiceCropCatalog,
    G2PRegisterDomainServiceInputsCatalog,
    G2PRegisterDomainServiceLivestockCatalog,
    G2PRegisterDomainServiceLocationCatalog,
    G2PRegisterDomainServiceSeedCatalog,
)
from .controllers import V1ReadOnlyCatalogController

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    """Catalog Extension runtime initializer."""

    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        self._patch_policy_builder()
        self._patch_filter_builder()

        # Initialize the domain service factory
        G2PRegisterDomainFactory()

        # Register catalog domain services with the platform component manager
        G2PRegisterDomainServiceCropCatalog()
        G2PRegisterDomainServiceSeedCatalog()
        G2PRegisterDomainServiceInputsCatalog()
        G2PRegisterDomainServiceLivestockCatalog()
        G2PRegisterDomainServiceLocationCatalog()

        # Initialize canonical read-only /v1 API endpoints
        V1ReadOnlyCatalogController().post_init()

        _logger.info("OpenG2P Catalog Extension initialized successfully with /v1 read-only API.")

    def _patch_policy_builder(self):
        """Patches G2PRegisterService._build_register_policy_condition to support both sync and async callers.

        Upstream calls 'await self._build_register_policy_condition(...)' inside get_record,
        but calls it synchronously inside search_in_a_register, get_section_records, etc.
        """
        try:
            import inspect
            from openg2p_registry_core.services.g2p_register_service import G2PRegisterService

            orig_build = G2PRegisterService._build_register_policy_condition

            def smart_build(this, *args, **kwargs):
                result = orig_build(this, *args, **kwargs)
                caller_frame = inspect.currentframe().f_back
                caller_name = caller_frame.f_code.co_name if caller_frame else ""
                if caller_name == "get_record":
                    async def _coro():
                        return result
                    return _coro()
                return result

            G2PRegisterService._build_register_policy_condition = smart_build
            _logger.info("G2PRegisterService._build_register_policy_condition smart-patched for sync/async.")
        except Exception as e:
            _logger.warning(f"Failed to patch G2PRegisterService._build_register_policy_condition: {e}")

    def _patch_filter_builder(self):
        """Patches FilterBuilder to handle string booleans cleanly."""
        try:
            from openg2p_registry_core.services.filter_builder import FilterBuilder
            from sqlalchemy import Boolean

            orig_validate = FilterBuilder._validate_value
            orig_build = FilterBuilder._build_field_conditions

            def patched_validate(this, field_config, operator, value):
                if field_config.get("filter_type") == "boolean":
                    if isinstance(value, str) and value.lower() in ("true", "false"):
                        return
                return orig_validate(this, field_config, operator, value)

            def patched_build_conditions(this, column, field_name, operators, field_config):
                is_bool_col = hasattr(column, "type") and isinstance(column.type, Boolean)
                if is_bool_col and isinstance(operators, dict):
                    converted_operators = {}
                    for op, val in operators.items():
                        if isinstance(val, str):
                            if val.lower() == "true":
                                converted_operators[op] = True
                            elif val.lower() == "false":
                                converted_operators[op] = False
                            else:
                                converted_operators[op] = val
                        elif isinstance(val, list):
                            converted_operators[op] = [
                                True if (isinstance(v, str) and v.lower() == "true") or v is True
                                else False if (isinstance(v, str) and v.lower() == "false") or v is False
                                else v
                                for v in val
                            ]
                        else:
                            converted_operators[op] = val
                    operators = converted_operators

                return orig_build(this, column, field_name, operators, field_config)

            FilterBuilder._validate_value = patched_validate
            FilterBuilder._build_field_conditions = patched_build_conditions
            _logger.info("FilterBuilder boolean handling patched successfully.")
        except Exception as e:
            _logger.warning(f"Failed to patch FilterBuilder: {e}")

    async def fastapi_app_startup(self, app):
        """FastAPI lifespan startup hook: ensures physical tables are created/migrated."""
        await self._migrate_extension_tables()

    def migrate_database(self, args):
        """CLI migration entrypoint called by 'python3 -m openg2p_registry_staff_api.main migrate'."""
        asyncio.run(self._migrate_extension_tables())

    async def _migrate_extension_tables(self):
        """Run table creation/migration using PostgreSQL advisory lock for concurrency safety."""
        try:
            async with dbengine.get().begin() as lock_conn:
                res = await lock_conn.execute(text("SELECT pg_try_advisory_lock(939392)"))
                acquired = res.scalar()
                if not acquired:
                    _logger.info("Another process is migrating catalog extension database, skipping")
                    return
        except Exception as e:
            _logger.warning(f"Could not check advisory lock for catalog migration: {e}")
            return

        try:
            await self._run_migrations()
        finally:
            try:
                async with dbengine.get().begin() as unlock_conn:
                    await unlock_conn.execute(text("SELECT pg_advisory_unlock(939392)"))
            except Exception:
                pass

    async def _run_migrations(self):
        _logger.info("Migrating catalog extension tables...")

        # 0. Lookup Tables & Taxonomies
        await CropCategory.create_migrate()
        await EcologicalZone.create_migrate()
        await CropVariety.create_migrate()
        await LivestockType.create_migrate()
        await LivestockBreed.create_migrate()
        await SeedCrop.create_migrate()
        await SeedVariety.create_migrate()

        # 1. Crop Catalog
        await G2PRegisterCropCatalog.create_migrate()
        await G2PRegisterHistoryCropCatalog.create_migrate()
        await G2PIntakeFormCropCatalog.create_migrate()

        # 2. Seed Catalog
        await G2PRegisterSeedCatalog.create_migrate()
        await G2PRegisterHistorySeedCatalog.create_migrate()
        await G2PIntakeFormSeedCatalog.create_migrate()

        # 3. Inputs Catalog (Agri-Inputs)
        await G2PRegisterInputCatalog.create_migrate()
        await G2PRegisterHistoryInputCatalog.create_migrate()
        await G2PIntakeFormInputCatalog.create_migrate()

        # 4. Livestock Breed Catalog
        await G2PRegisterLivestockCatalog.create_migrate()
        await G2PRegisterHistoryLivestockCatalog.create_migrate()
        await G2PIntakeFormLivestockCatalog.create_migrate()

        # 5. Location Catalog
        await GeoRegion.create_migrate()
        await GeoZone.create_migrate()
        await GeoWoreda.create_migrate()
        await GeoKebele.create_migrate()
        await G2PRegisterLocationCatalog.create_migrate()
        await G2PRegisterHistoryLocationCatalog.create_migrate()
        await G2PIntakeFormLocationCatalog.create_migrate()

        _logger.info("Catalog extension tables migrated successfully.")
