from openg2p_registry_core.services import G2PRegisterDomainService


class G2PRegisterDomainServiceInputsCatalog(G2PRegisterDomainService):
    """Domain service managing Inputs Catalog (Agri-Inputs) records."""

    def construct_record_name(self, record_dict: dict) -> str:
        """Constructs human-readable title for details view and breadcrumbs."""
        name = record_dict.get("trade_name") or record_dict.get("record_name") or ""
        category = record_dict.get("input_category") or record_dict.get("fertilizer_type")
        return f"{name} ({category})" if category else str(name)

    def construct_search_text(self, record_dict: dict) -> str:
        """Constructs unified search_text corpus for full-text search."""
        fields = [
            str(record_dict.get("input_code") or ""),
            str(record_dict.get("trade_name") or ""),
            str(record_dict.get("input_category") or record_dict.get("fertilizer_type") or ""),
            str(record_dict.get("nutrient_composition") or ""),
            str(record_dict.get("manufacturer") or ""),
            str(record_dict.get("application_method") or ""),
            str(record_dict.get("recommended_crops") or ""),
            str(record_dict.get("license_number") or ""),
            str(record_dict.get("description") or ""),
        ]
        return " ".join(f for f in fields if f).strip()

    async def validate_domain_attributes(self, records: list[dict]):
        """Validates domain attributes for Inputs Catalog records."""
        for record in records:
            if not record.get("input_code") or not str(record.get("input_code")).strip():
                raise ValueError("Input Code is required")
            if not record.get("trade_name") or not str(record.get("trade_name")).strip():
                raise ValueError("Trade Name is required")


# Backward-compatibility alias
G2PRegisterDomainServiceFertilizerCatalog = G2PRegisterDomainServiceInputsCatalog
