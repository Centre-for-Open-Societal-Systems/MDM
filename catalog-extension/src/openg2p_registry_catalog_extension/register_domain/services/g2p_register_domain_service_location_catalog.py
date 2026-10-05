from openg2p_registry_core.services import G2PRegisterDomainService


class G2PRegisterDomainServiceLocationCatalog(G2PRegisterDomainService):
    """Domain service managing Location Catalog records."""

    def construct_record_name(self, record_dict: dict) -> str:
        """Constructs human-readable title for details view and breadcrumbs."""
        name = record_dict.get("location_name", "")
        level = record_dict.get("admin_level")
        return f"{name} ({level})" if level else str(name)

    def construct_search_text(self, record_dict: dict) -> str:
        """Constructs unified search_text corpus for full-text search."""
        fields = [
            str(record_dict.get("location_code") or ""),
            str(record_dict.get("location_name") or ""),
            str(record_dict.get("admin_level") or ""),
            str(record_dict.get("parent_location_name") or ""),
            str(record_dict.get("parent_location_code") or ""),
            str(record_dict.get("capital_city") or ""),
            str(record_dict.get("pcode") or ""),
            str(record_dict.get("region_name") or ""),
            str(record_dict.get("zone_name") or ""),
            str(record_dict.get("woreda_name") or ""),
            str(record_dict.get("kebele_name") or ""),
            str(record_dict.get("description") or ""),
        ]
        return " ".join(f for f in fields if f).strip()

    async def validate_domain_attributes(self, records: list[dict]):
        """Validates domain attributes for Location Catalog records."""
        for record in records:
            if not record.get("location_code") or not str(record.get("location_code")).strip():
                raise ValueError("Location Code is required")
            if not record.get("location_name") or not str(record.get("location_name")).strip():
                raise ValueError("Location Name is required")
            if not record.get("admin_level") or not str(record.get("admin_level")).strip():
                raise ValueError("Admin Level is required (Region, Zone, Woreda, or Kebele)")
