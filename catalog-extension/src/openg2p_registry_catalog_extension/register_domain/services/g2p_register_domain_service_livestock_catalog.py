from openg2p_registry_core.services import G2PRegisterDomainService


class G2PRegisterDomainServiceLivestockCatalog(G2PRegisterDomainService):
    """Domain service managing Livestock Breed Catalog records."""

    def construct_record_name(self, record_dict: dict) -> str:
        breed = record_dict.get("breed_name", "")
        species = record_dict.get("species", "")
        abbr = record_dict.get("abbreviation")
        if abbr:
            return f"{breed} ({abbr}) - {species}" if species else f"{breed} ({abbr})"
        return f"{breed} ({species})" if species else str(breed)

    def construct_search_text(self, record_dict: dict) -> str:
        fields = [
            str(record_dict.get("breed_code") or ""),
            str(record_dict.get("breed_name") or ""),
            str(record_dict.get("abbreviation") or ""),
            str(record_dict.get("species") or ""),
            str(record_dict.get("breed_type") or ""),
            str(record_dict.get("primary_purpose") or ""),
            str(record_dict.get("origin_country") or ""),
        ]
        return " ".join(f for f in fields if f).strip()

    async def validate_domain_attributes(self, records: list[dict]):
        """Validates domain attributes for Livestock Breed Catalog records."""
        for record in records:
            if not record.get("breed_code") or not str(record.get("breed_code")).strip():
                raise ValueError("Breed Code is required")
            if not record.get("breed_name") or not str(record.get("breed_name")).strip():
                raise ValueError("Breed Name is required")
            if not record.get("species") or not str(record.get("species")).strip():
                raise ValueError("Species is required")

