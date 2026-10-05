from openg2p_registry_core.services import G2PRegisterDomainService


class G2PRegisterDomainServiceSeedCatalog(G2PRegisterDomainService):
    """Domain service managing Seed Variety Catalog records."""

    def construct_record_name(self, record_dict: dict) -> str:
        variety = record_dict.get("variety_name", "")
        crop = record_dict.get("crop_name", "")
        return f"{variety} - {crop}" if crop else str(variety)

    def construct_search_text(self, record_dict: dict) -> str:
        fields = [
            str(record_dict.get("seed_code") or ""),
            str(record_dict.get("variety_name") or ""),
            str(record_dict.get("crop_code") or ""),
            str(record_dict.get("crop_name") or ""),
            str(record_dict.get("breeder_source") or ""),
            str(record_dict.get("match_status") or ""),
            str(record_dict.get("potential_yield") or ""),
        ]
        return " ".join(f for f in fields if f).strip()

    async def validate_domain_attributes(self, records: list[dict]):
        """Validates domain attributes for Seed Variety Catalog records."""
        for record in records:
            if not record.get("seed_code") or not str(record.get("seed_code")).strip():
                raise ValueError("Seed Code is required")
            if not record.get("variety_name") or not str(record.get("variety_name")).strip():
                raise ValueError("Variety Name is required")
            if not record.get("crop_name") or not str(record.get("crop_name")).strip():
                raise ValueError("Parent Crop Name is required")

