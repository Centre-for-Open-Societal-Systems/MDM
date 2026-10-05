from openg2p_registry_core.services import G2PRegisterDomainService


class G2PRegisterDomainServiceCropCatalog(G2PRegisterDomainService):
    """Domain service managing Crop Catalog records."""

    def construct_record_name(self, record_dict: dict) -> str:
        """Constructs human-readable title for details view and breadcrumbs."""
        name = record_dict.get("crop_name", "")
        scientific = record_dict.get("scientific_name")
        return f"{name} ({scientific})" if scientific else str(name)

    def construct_search_text(self, record_dict: dict) -> str:
        """Constructs unified search_text corpus for full-text search."""
        fields = [
            str(record_dict.get("crop_code") or ""),
            str(record_dict.get("crop_name") or ""),
            str(record_dict.get("scientific_name") or ""),
            str(record_dict.get("crop_category") or ""),
            str(record_dict.get("preferred_ecological_zone") or ""),
            str(record_dict.get("centre") or ""),
            str(record_dict.get("known_for") or ""),
            str(record_dict.get("preferred_soil_type") or ""),
        ]
        return " ".join(f for f in fields if f).strip()

    async def validate_domain_attributes(self, records: list[dict]):
        """Validates domain attributes for Crop Catalog records."""
        for record in records:
            if not record.get("crop_code") or not str(record.get("crop_code")).strip():
                raise ValueError("Crop Code is required")
            if not record.get("crop_name") or not str(record.get("crop_name")).strip():
                raise ValueError("Crop Name is required")

