import hashlib
import json
from typing import Any, Dict, List, Optional
from fastapi import Query, Request, Response
from fastapi.responses import JSONResponse
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_common.context import dbengine
from sqlalchemy import text


def _generate_etag(data: Any) -> str:
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:32]


def _format_row(row_dict: dict) -> dict:
    """Ensure UUID and date types are JSON serializable."""
    res = {}
    for k, v in row_dict.items():
        if v is not None and hasattr(v, "isoformat"):
            res[k] = v.isoformat()
        elif v is not None and hasattr(v, "hex"):  # UUID
            res[k] = str(v)
        else:
            res[k] = v
    return res


class V1ReadOnlyCatalogController(BaseController):
    """FastAPI Read-Only Controller exposing canonical /v1 endpoints.

    Strictly GET-only operations for external consumers, registries, and lookups:
    - Pagination, search, and category filtering
    - OpenAgriNet UUIDs (public.uuid_generate_v4()) on every record
    - ETag and Cache-Control headers with 304 Not Modified support
    - Zero POST/PUT/DELETE mutations allowed
    """

    def __init__(self, name="v1-readonly-catalog-controller", **kwargs):
        super().__init__(name, **kwargs)
        self.router.tags += ["Master Data Catalogues - Read-Only API (v1)"]
        self.router.prefix = "/v1"

        # 1. Catalogues and releases
        self.router.add_api_route("/releases/current", self.get_current_release, methods=["GET"])
        self.router.add_api_route("/catalogues", self.get_catalogues, methods=["GET"])
        self.router.add_api_route("/catalogues/{catalogue_code}/values", self.get_catalogue_values, methods=["GET"])
        self.router.add_api_route("/catalogue-values", self.get_catalogue_options, methods=["GET"])

        # 2. Agri-Inputs Catalog (Fertilizers, Pesticides, Herbicides, etc.)
        self.router.add_api_route("/inputs", self.get_inputs, methods=["GET"])
        self.router.add_api_route("/inputs/{code_or_uuid}", self.get_input_by_id, methods=["GET"])

        # 3. Crops Catalog
        self.router.add_api_route("/crops", self.get_crops, methods=["GET"])
        self.router.add_api_route("/crops/{code_or_uuid}", self.get_crop_by_id, methods=["GET"])
        self.router.add_api_route("/crop-varieties/{code_or_uuid}", self.get_seed_variety_by_id, methods=["GET"])

        # 4. Seed Varieties Catalog
        self.router.add_api_route("/seed-varieties", self.get_seed_varieties, methods=["GET"])
        self.router.add_api_route("/seed-varieties/{code_or_uuid}", self.get_seed_variety_by_id, methods=["GET"])

        # 5. Livestock Catalog
        self.router.add_api_route("/livestock/species", self.get_livestock_species, methods=["GET"])
        self.router.add_api_route("/livestock/breeds", self.get_livestock_breeds, methods=["GET"])
        self.router.add_api_route("/livestock/breeds/{code_or_uuid}", self.get_livestock_breed_by_id, methods=["GET"])
        self.router.add_api_route("/livestock/reference-data", self.get_livestock_reference_data, methods=["GET"])

        # 6. Geography & Location Catalog
        self.router.add_api_route("/geography/levels", self.get_geography_levels, methods=["GET"])
        self.router.add_api_route("/geography/units", self.get_geography_units, methods=["GET"])
        self.router.add_api_route("/geography/units/{code_or_uuid}", self.get_geography_unit_by_id, methods=["GET"])

        # 7. Snapshots
        self.router.add_api_route("/snapshots/current", self.get_snapshot_summary, methods=["GET"])

    # --------------------------------------------------------------------------
    # Helper: Apply ETag and Cache Headers
    # --------------------------------------------------------------------------
    def _respond_with_cache(self, request: Request, payload: dict, max_age: int = 300) -> Response:
        etag = _generate_etag(payload)
        if_none_match = request.headers.get("if-none-match", "").strip('"')
        if if_none_match and if_none_match == etag:
            return Response(status_code=304)

        headers = {
            "ETag": f'"{etag}"',
            "Cache-Control": f"public, max-age={max_age}",
            "X-Catalogue-Release": "ETH-master-catalog-v1",
        }
        return JSONResponse(content=payload, headers=headers)

    # --------------------------------------------------------------------------
    # 1. Releases & Catalogues
    # --------------------------------------------------------------------------
    async def get_current_release(self, request: Request):
        """Returns the current active release metadata."""
        release = {
            "country_code": "ETH",
            "version": "ETH-master-catalog-v1",
            "schema_version": "1.0",
            "checksum": "sha256:d8b2e10697920abce6fbc1f83",
            "source": "OpenAgriNet Master Data Management (MoA / ATI / Ethio-Seed / LITS)",
            "status": "ACTIVE",
            "capabilities": ["uuid_generate_v4", "read_only", "etag_caching"],
        }
        return self._respond_with_cache(request, {"release": release})

    async def get_catalogues(self, request: Request):
        """Lists all 5 canonical master catalogues."""
        async with dbengine.get().connect() as conn:
            counts = {
                "crops": (await conn.execute(text("SELECT count(*) FROM g2p_register_crop_catalogs"))).scalar() or 0,
                "seeds": (await conn.execute(text("SELECT count(*) FROM g2p_register_seed_catalogs"))).scalar() or 0,
                "inputs": (await conn.execute(text("SELECT count(*) FROM g2p_register_input_catalogs"))).scalar() or 0,
                "livestock": (await conn.execute(text("SELECT count(*) FROM g2p_register_livestock_catalogs"))).scalar() or 0,
                "locations": (await conn.execute(text("SELECT count(*) FROM g2p_register_location_catalogs"))).scalar() or 0,
            }

        catalogues = [
            {
                "code": "crops",
                "domain": "agriculture",
                "display_name": "Agricultural Crops",
                "description": "National Crop Master Catalog with ecological zones, growth cycle, water requirements",
                "total_records": counts["crops"],
                "status": "ACTIVE",
            },
            {
                "code": "seeds",
                "domain": "agriculture",
                "display_name": "Seed Varieties",
                "description": "Officially released & registered seed varieties with breeder source and certification",
                "total_records": counts["seeds"],
                "status": "ACTIVE",
            },
            {
                "code": "inputs",
                "domain": "agriculture",
                "display_name": "Agri-Inputs",
                "description": "Agro-Inputs master catalog covering inorganic/organic fertilizers, pesticides, herbicides, fungicides, soil amendments, seed treatments",
                "total_records": counts["inputs"],
                "status": "ACTIVE",
            },
            {
                "code": "livestock",
                "domain": "livestock",
                "display_name": "Livestock Breeds",
                "description": "Indigenous and exotic livestock breeds aligned with national standard and ET-LITS",
                "total_records": counts["livestock"],
                "status": "ACTIVE",
            },
            {
                "code": "locations",
                "domain": "geography",
                "display_name": "Administrative Geolocation",
                "description": "Standardized Ethiopian administrative boundaries: Regions, Zones, Woredas, and Kebeles",
                "total_records": counts["locations"],
                "status": "ACTIVE",
            },
        ]
        return self._respond_with_cache(request, {"catalogues": catalogues, "total": len(catalogues)})

    async def get_catalogue_values(
        self,
        request: Request,
        catalogue_code: str,
        search: Optional[str] = Query(None, description="Search query string"),
        category: Optional[str] = Query(None, description="Filter by category"),
        status: str = Query("ACTIVE", description="Filter by status"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(50, ge=1, le=1000, description="Items per page (max 1000)"),
    ):
        """Unified generic search/lookup for items in any catalogue."""
        c = catalogue_code.lower()
        if c in ("crops", "crop"):
            return await self.get_crops(request, search=search, category=category, page=page, page_size=page_size)
        elif c in ("seeds", "seed", "seed-varieties", "seed_varieties"):
            return await self.get_seed_varieties(request, search=search, page=page, page_size=page_size)
        elif c in ("inputs", "input", "fertilizers", "fertilizer"):
            return await self.get_inputs(request, search=search, category=category, page=page, page_size=page_size)
        elif c in ("livestock", "breeds", "livestock-breeds", "livestock_breeds"):
            return await self.get_livestock_breeds(request, search=search, page=page, page_size=page_size)
        elif c in ("locations", "location", "geography", "units"):
            return await self.get_geography_units(request, search=search, page=page, page_size=page_size)
        else:
            return JSONResponse(
                status_code=404,
                content={"error": f"Unknown catalogue '{catalogue_code}'. Available: crops, seeds, inputs, livestock, locations."},
            )

    async def get_catalogue_options(
        self,
        request: Request,
        catalogue_code: str = Query(..., description="Catalogue code: crops, seeds, inputs, livestock, locations, crop_categories, input_categories"),
        search: Optional[str] = Query(None),
        limit: int = Query(100, ge=1, le=500),
    ):
        """Compact options list for dropdown widgets (code, display_name, uuid)."""
        c = catalogue_code.lower()
        options = []
        async with dbengine.get().connect() as conn:
            if c in ("crop_categories", "crop_category"):
                q = text("SELECT category_code AS code, category_name AS display_name, uuid FROM crop_categories ORDER BY category_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]
            elif c in ("input_categories", "input_category"):
                q = text("SELECT value_code AS code, value_display AS display_name FROM g2p_attribute_values WHERE attribute_id = 'INPUT_CATEGORY' ORDER BY sort_order")
                rows = (await conn.execute(q)).mappings().all()
                options = [{"code": r["code"], "display_name": r["display_name"]} for r in rows]
            elif c in ("crops", "crop"):
                q = text("SELECT crop_code AS code, crop_name AS display_name, uuid FROM g2p_register_crop_catalogs WHERE is_active = TRUE ORDER BY crop_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]
            elif c in ("inputs", "input", "fertilizers", "fertilizer"):
                q = text("SELECT input_code AS code, trade_name AS display_name, uuid FROM g2p_register_input_catalogs WHERE is_active = TRUE ORDER BY trade_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]
            elif c in ("seeds", "seed"):
                q = text("SELECT seed_code AS code, variety_name AS display_name, uuid FROM g2p_register_seed_catalogs WHERE is_active = TRUE ORDER BY variety_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]
            elif c in ("livestock", "breeds"):
                q = text("SELECT breed_code AS code, breed_name AS display_name, uuid FROM g2p_register_livestock_catalogs WHERE is_active = TRUE ORDER BY breed_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]
            elif c in ("locations", "regions"):
                q = text("SELECT location_code AS code, location_name AS display_name, uuid FROM g2p_register_location_catalogs WHERE admin_level = 'Region' ORDER BY location_name LIMIT :limit")
                rows = (await conn.execute(q, {"limit": limit})).mappings().all()
                options = [_format_row(dict(r)) for r in rows]

        return self._respond_with_cache(request, {"catalogue_code": catalogue_code, "options": options, "total": len(options)})

    # --------------------------------------------------------------------------
    # 2. Agri-Inputs Endpoints (Fertilizers, Pesticides, Herbicides, etc.)
    # --------------------------------------------------------------------------
    async def get_inputs(
        self,
        request: Request,
        category: Optional[str] = Query(None, description="Agri-input category (e.g. INORGANIC_FERTILIZER, PESTICIDE, HERBICIDE)"),
        manufacturer: Optional[str] = Query(None, description="Manufacturer/supplier name filter"),
        crops: Optional[str] = Query(None, description="Recommended crops filter"),
        search: Optional[str] = Query(None, description="Text search query"),
        is_active: bool = Query(True, description="Active status"),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=1000),
    ):
        """Search and list Agri-Inputs with full agro-input categories, UUIDs, and pagination."""
        offset = (page - 1) * page_size
        where_clauses = ["is_active = :is_active"]
        params = {"is_active": is_active, "limit": page_size, "offset": offset}

        if category:
            where_clauses.append("input_category ILIKE :category")
            params["category"] = f"%{category}%"
        if manufacturer:
            where_clauses.append("manufacturer ILIKE :manufacturer")
            params["manufacturer"] = f"%{manufacturer}%"
        if crops:
            where_clauses.append("recommended_crops ILIKE :crops")
            params["crops"] = f"%{crops}%"
        if search:
            where_clauses.append("(trade_name ILIKE :search OR input_code ILIKE :search OR nutrient_composition ILIKE :search OR manufacturer ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        async with dbengine.get().connect() as conn:
            count_q = text(f"SELECT count(*) FROM g2p_register_input_catalogs WHERE {where_sql}")
            total = (await conn.execute(count_q, params)).scalar() or 0

            data_q = text(f"""
                SELECT 
                    uuid, input_code, trade_name, input_category, nutrient_composition,
                    manufacturer, application_method, recommended_crops, recommended_dosage,
                    license_number, safety_precautions, description, is_active,
                    created_at, record_status
                FROM g2p_register_input_catalogs
                WHERE {where_sql}
                ORDER BY input_code
                LIMIT :limit OFFSET :offset
            """)
            rows = (await conn.execute(data_q, params)).mappings().all()

        items = [_format_row(dict(r)) for r in rows]
        payload = {
            "catalogue": "inputs",
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
        return self._respond_with_cache(request, payload)

    async def get_input_by_id(self, request: Request, code_or_uuid: str):
        """Fetch a single input record by input_code or UUID."""
        async with dbengine.get().connect() as conn:
            q = text("""
                SELECT 
                    uuid, input_code, trade_name, input_category, nutrient_composition,
                    manufacturer, application_method, recommended_crops, recommended_dosage,
                    license_number, safety_precautions, description, is_active,
                    created_at, record_status
                FROM g2p_register_input_catalogs
                WHERE input_code = :val OR uuid::text = :val
                LIMIT 1
            """)
            row = (await conn.execute(q, {"val": code_or_uuid})).mappings().first()

        if not row:
            return JSONResponse(status_code=404, content={"error": f"Input '{code_or_uuid}' not found"})
        return self._respond_with_cache(request, {"input": _format_row(dict(row))})

    # --------------------------------------------------------------------------
    # 3. Crops Endpoints
    # --------------------------------------------------------------------------
    async def get_crops(
        self,
        request: Request,
        category: Optional[str] = Query(None, description="Crop category"),
        ecological_zone: Optional[str] = Query(None, description="Preferred ecological zone"),
        search: Optional[str] = Query(None, description="Search query"),
        is_active: bool = Query(True),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=1000),
    ):
        """Search and list Agricultural Crops with UUIDs and pagination."""
        offset = (page - 1) * page_size
        where_clauses = ["is_active = :is_active"]
        params = {"is_active": is_active, "limit": page_size, "offset": offset}

        if category:
            where_clauses.append("crop_category ILIKE :category")
            params["category"] = f"%{category}%"
        if ecological_zone:
            where_clauses.append("preferred_ecological_zone ILIKE :ecological_zone")
            params["ecological_zone"] = f"%{ecological_zone}%"
        if search:
            where_clauses.append("(crop_name ILIKE :search OR crop_code ILIKE :search OR scientific_name ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        async with dbengine.get().connect() as conn:
            count_q = text(f"SELECT count(*) FROM g2p_register_crop_catalogs WHERE {where_sql}")
            total = (await conn.execute(count_q, params)).scalar() or 0

            data_q = text(f"""
                SELECT 
                    uuid, crop_code, crop_name, scientific_name, crop_category,
                    preferred_ecological_zone, centre, varieties_count, growth_cycle_days,
                    water_requirement, preferred_soil_type, known_for, description, is_active
                FROM g2p_register_crop_catalogs
                WHERE {where_sql}
                ORDER BY crop_code
                LIMIT :limit OFFSET :offset
            """)
            rows = (await conn.execute(data_q, params)).mappings().all()

        items = [_format_row(dict(r)) for r in rows]
        payload = {
            "catalogue": "crops",
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
        return self._respond_with_cache(request, payload)

    async def get_crop_by_id(self, request: Request, code_or_uuid: str):
        """Fetch a single crop record by crop_code or UUID."""
        async with dbengine.get().connect() as conn:
            q = text("""
                SELECT 
                    uuid, crop_code, crop_name, scientific_name, crop_category,
                    preferred_ecological_zone, centre, varieties_count, growth_cycle_days,
                    water_requirement, preferred_soil_type, known_for, description, is_active
                FROM g2p_register_crop_catalogs
                WHERE crop_code = :val OR uuid::text = :val
                LIMIT 1
            """)
            row = (await conn.execute(q, {"val": code_or_uuid})).mappings().first()

        if not row:
            return JSONResponse(status_code=404, content={"error": f"Crop '{code_or_uuid}' not found"})
        return self._respond_with_cache(request, {"crop": _format_row(dict(row))})

    # --------------------------------------------------------------------------
    # 4. Seed Varieties Endpoints
    # --------------------------------------------------------------------------
    async def get_seed_varieties(
        self,
        request: Request,
        crop_name: Optional[str] = Query(None, description="Parent crop name"),
        is_certified: Optional[bool] = Query(None, description="Certification status"),
        release_year: Optional[int] = Query(None, description="Year of release"),
        search: Optional[str] = Query(None, description="Search query"),
        is_active: bool = Query(True),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=1000),
    ):
        """Search and list Seed Varieties with UUIDs and pagination."""
        offset = (page - 1) * page_size
        where_clauses = ["is_active = :is_active"]
        params = {"is_active": is_active, "limit": page_size, "offset": offset}

        if crop_name:
            where_clauses.append("crop_name ILIKE :crop_name")
            params["crop_name"] = f"%{crop_name}%"
        if is_certified is not None:
            where_clauses.append("is_certified = :is_certified")
            params["is_certified"] = is_certified
        if release_year:
            where_clauses.append("release_year = :release_year")
            params["release_year"] = release_year
        if search:
            where_clauses.append("(variety_name ILIKE :search OR seed_code ILIKE :search OR crop_name ILIKE :search OR breeder_source ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        async with dbengine.get().connect() as conn:
            count_q = text(f"SELECT count(*) FROM g2p_register_seed_catalogs WHERE {where_sql}")
            total = (await conn.execute(count_q, params)).scalar() or 0

            data_q = text(f"""
                SELECT 
                    uuid, seed_code, variety_name, crop_name, breeder_source,
                    release_year, maturity_days, potential_yield, yield_unit,
                    disease_resistance, match_status, description, is_certified, is_active
                FROM g2p_register_seed_catalogs
                WHERE {where_sql}
                ORDER BY seed_code
                LIMIT :limit OFFSET :offset
            """)
            rows = (await conn.execute(data_q, params)).mappings().all()

        items = [_format_row(dict(r)) for r in rows]
        payload = {
            "catalogue": "seed_varieties",
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
        return self._respond_with_cache(request, payload)

    async def get_seed_variety_by_id(self, request: Request, code_or_uuid: str):
        """Fetch a single seed variety by seed_code or UUID."""
        async with dbengine.get().connect() as conn:
            q = text("""
                SELECT 
                    uuid, seed_code, variety_name, crop_name, breeder_source,
                    release_year, maturity_days, potential_yield, yield_unit,
                    disease_resistance, match_status, description, is_certified, is_active
                FROM g2p_register_seed_catalogs
                WHERE seed_code = :val OR uuid::text = :val
                LIMIT 1
            """)
            row = (await conn.execute(q, {"val": code_or_uuid})).mappings().first()

        if not row:
            return JSONResponse(status_code=404, content={"error": f"Seed variety '{code_or_uuid}' not found"})
        return self._respond_with_cache(request, {"seed_variety": _format_row(dict(row))})

    # --------------------------------------------------------------------------
    # 5. Livestock Endpoints
    # --------------------------------------------------------------------------
    async def get_livestock_species(self, request: Request):
        """Lists canonical livestock species."""
        async with dbengine.get().connect() as conn:
            q = text("SELECT DISTINCT species FROM g2p_register_livestock_catalogs WHERE is_active = TRUE ORDER BY species")
            species = [r[0] for r in (await conn.execute(q)).all()]
        return self._respond_with_cache(request, {"species": species, "total": len(species)})

    async def get_livestock_breeds(
        self,
        request: Request,
        species: Optional[str] = Query(None, description="Species filter (e.g. CATTLE, SHEEP, GOAT)"),
        breed_type: Optional[str] = Query(None, description="Breed type (Indigenous, Exotic, Cross)"),
        primary_purpose: Optional[str] = Query(None, description="Primary purpose (DAIRY, MEAT, DUAL_PURPOSE)"),
        search: Optional[str] = Query(None, description="Search query"),
        is_active: bool = Query(True),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=1000),
    ):
        """Search and list Livestock Breeds with UUIDs and pagination."""
        offset = (page - 1) * page_size
        where_clauses = ["is_active = :is_active"]
        params = {"is_active": is_active, "limit": page_size, "offset": offset}

        if species:
            where_clauses.append("species ILIKE :species")
            params["species"] = f"%{species}%"
        if breed_type:
            where_clauses.append("breed_type ILIKE :breed_type")
            params["breed_type"] = f"%{breed_type}%"
        if primary_purpose:
            where_clauses.append("primary_purpose ILIKE :primary_purpose")
            params["primary_purpose"] = f"%{primary_purpose}%"
        if search:
            where_clauses.append("(breed_name ILIKE :search OR breed_code ILIKE :search OR abbreviation ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        async with dbengine.get().connect() as conn:
            count_q = text(f"SELECT count(*) FROM g2p_register_livestock_catalogs WHERE {where_sql}")
            total = (await conn.execute(count_q, params)).scalar() or 0

            data_q = text(f"""
                SELECT 
                    uuid, breed_code, breed_name, species, breed_type, abbreviation,
                    primary_purpose, origin_country, in_national_standard, in_etlits_registry,
                    climate_adaptability, average_mature_weight_kg, description, is_active
                FROM g2p_register_livestock_catalogs
                WHERE {where_sql}
                ORDER BY breed_code
                LIMIT :limit OFFSET :offset
            """)
            rows = (await conn.execute(data_q, params)).mappings().all()

        items = [_format_row(dict(r)) for r in rows]
        payload = {
            "catalogue": "livestock_breeds",
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
        return self._respond_with_cache(request, payload)

    async def get_livestock_breed_by_id(self, request: Request, code_or_uuid: str):
        """Fetch a single livestock breed by breed_code or UUID."""
        async with dbengine.get().connect() as conn:
            q = text("""
                SELECT 
                    uuid, breed_code, breed_name, species, breed_type, abbreviation,
                    primary_purpose, origin_country, in_national_standard, in_etlits_registry,
                    climate_adaptability, average_mature_weight_kg, description, is_active
                FROM g2p_register_livestock_catalogs
                WHERE breed_code = :val OR uuid::text = :val
                LIMIT 1
            """)
            row = (await conn.execute(q, {"val": code_or_uuid})).mappings().first()

        if not row:
            return JSONResponse(status_code=404, content={"error": f"Livestock breed '{code_or_uuid}' not found"})
        return self._respond_with_cache(request, {"breed": _format_row(dict(row))})

    async def get_livestock_reference_data(self, request: Request):
        """Returns standard livestock reference sets: gender, production types, and record statuses."""
        payload = {
            "country_code": "ETH",
            "release": "ETH-master-catalog-v1",
            "gender_types": [
                {"code": "FEMALE", "display_name": "Female"},
                {"code": "MALE", "display_name": "Male"},
                {"code": "CASTRATED", "display_name": "Castrated / Neutered"},
            ],
            "production_types": [
                {"code": "DAIRY", "display_name": "Dairy / Milk", "valid_species": ["CATTLE", "CAMEL", "GOAT"]},
                {"code": "MEAT", "display_name": "Meat / Beef / Mutton", "valid_species": ["CATTLE", "SHEEP", "GOAT", "CAMEL"]},
                {"code": "DUAL_PURPOSE", "display_name": "Dual Purpose (Milk & Meat)", "valid_species": ["CATTLE", "GOAT", "SHEEP", "CAMEL"]},
                {"code": "DRAFT_POWER", "display_name": "Draft Power / Ploughing", "valid_species": ["CATTLE", "CAMEL"]},
                {"code": "BREEDING", "display_name": "Breeding Stock", "valid_species": ["CATTLE", "SHEEP", "GOAT", "CAMEL"]},
                {"code": "WOOL", "display_name": "Wool", "valid_species": ["SHEEP"]},
                {"code": "HONEY", "display_name": "Honey Production", "valid_species": ["BEEHIVE"]},
                {"code": "HIDE_SKIN", "display_name": "Hide or Skin", "valid_species": ["CATTLE", "GOAT", "SHEEP"]},
            ],
            "record_statuses": [
                {"code": "ACTIVE", "display_name": "Active / Approved", "is_live": True},
                {"code": "INACTIVE", "display_name": "Inactive / Retired", "is_live": False},
                {"code": "PENDING", "display_name": "Pending Approval", "is_live": False},
            ],
        }
        return self._respond_with_cache(request, payload)

    # --------------------------------------------------------------------------
    # 6. Geography & Administrative Location Endpoints
    # --------------------------------------------------------------------------
    async def get_geography_levels(self, request: Request):
        """Lists Ethiopian administrative levels."""
        levels = [
            {"level": 1, "name": "Region", "description": "Regional State (Level 1)", "count_estimate": 14},
            {"level": 2, "name": "Zone", "description": "Administrative Zone (Level 2)", "count_estimate": 125},
            {"level": 3, "name": "Woreda", "description": "District / Woreda (Level 3)", "count_estimate": 1379},
            {"level": 4, "name": "Kebele", "description": "Ward / Kebele (Level 4)", "count_estimate": 19535},
        ]
        return self._respond_with_cache(request, {"levels": levels})

    async def get_geography_units(
        self,
        request: Request,
        level: Optional[str] = Query(None, description="Administrative level (Region, Zone, Woreda, Kebele)"),
        parent_code: Optional[str] = Query(None, description="Parent location code"),
        search: Optional[str] = Query(None, description="Search query string"),
        is_active: bool = Query(True),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=1000),
    ):
        """Search and list Administrative Geography units with UUIDs and pagination."""
        offset = (page - 1) * page_size
        where_clauses = ["is_active = :is_active"]
        params = {"is_active": is_active, "limit": page_size, "offset": offset}

        if level:
            where_clauses.append("admin_level ILIKE :level")
            params["level"] = level
        if parent_code:
            where_clauses.append("parent_location_code = :parent_code")
            params["parent_code"] = parent_code
        if search:
            where_clauses.append("(location_name ILIKE :search OR location_code ILIKE :search OR pcode ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        async with dbengine.get().connect() as conn:
            count_q = text(f"SELECT count(*) FROM g2p_register_location_catalogs WHERE {where_sql}")
            total = (await conn.execute(count_q, params)).scalar() or 0

            data_q = text(f"""
                SELECT 
                    uuid, location_code, location_name, admin_level,
                    parent_location_code, parent_location_name, pcode,
                    capital_city, area_sq_km, population_estimate, is_active
                FROM g2p_register_location_catalogs
                WHERE {where_sql}
                ORDER BY location_code
                LIMIT :limit OFFSET :offset
            """)
            rows = (await conn.execute(data_q, params)).mappings().all()

        items = [_format_row(dict(r)) for r in rows]
        payload = {
            "catalogue": "geography_units",
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
        return self._respond_with_cache(request, payload)

    async def get_geography_unit_by_id(self, request: Request, code_or_uuid: str):
        """Fetch a single location unit by location_code or UUID."""
        async with dbengine.get().connect() as conn:
            q = text("""
                SELECT 
                    uuid, location_code, location_name, admin_level,
                    parent_location_code, parent_location_name, pcode,
                    capital_city, area_sq_km, population_estimate, is_active
                FROM g2p_register_location_catalogs
                WHERE location_code = :val OR uuid::text = :val
                LIMIT 1
            """)
            row = (await conn.execute(q, {"val": code_or_uuid})).mappings().first()

        if not row:
            return JSONResponse(status_code=404, content={"error": f"Geography unit '{code_or_uuid}' not found"})
        return self._respond_with_cache(request, {"unit": _format_row(dict(row))})

    # --------------------------------------------------------------------------
    # 7. Snapshots
    # --------------------------------------------------------------------------
    async def get_snapshot_summary(self, request: Request):
        """Complete projection snapshot summary across all catalogues."""
        async with dbengine.get().connect() as conn:
            res = {
                "release": "ETH-master-catalog-v1",
                "counts": {
                    "crops": (await conn.execute(text("SELECT count(*) FROM g2p_register_crop_catalogs"))).scalar() or 0,
                    "seed_varieties": (await conn.execute(text("SELECT count(*) FROM g2p_register_seed_catalogs"))).scalar() or 0,
                    "inputs": (await conn.execute(text("SELECT count(*) FROM g2p_register_input_catalogs"))).scalar() or 0,
                    "livestock_breeds": (await conn.execute(text("SELECT count(*) FROM g2p_register_livestock_catalogs"))).scalar() or 0,
                    "geography_units": (await conn.execute(text("SELECT count(*) FROM g2p_register_location_catalogs"))).scalar() or 0,
                },
                "status": "READY",
            }
        return self._respond_with_cache(request, res)
