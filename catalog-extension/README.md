# OpenG2P Registry Catalog Extension

An installable **Catalog Extension** for the OpenG2P Registry Platform.

This extension implements authoritative master reference catalogues (Agricultural Crops, Seed Varieties, Agro-Inputs & Fertilizers, Livestock Breeds, and Administrative Geolocation) as native registers within OpenG2P, backed by PostgreSQL `uuid-ossp` identifiers and exposed via high-performance, cached, read-only `/v1` REST APIs.

---

## What this Extension Contains

| Component | Path | Purpose |
|---|---|---|
| **Packaging** | `pyproject.toml` | Hatchling-based Python package definition |
| **App Initializer** | `src/openg2p_registry_catalog_extension/app.py` | Discovered by the platform via `REGISTRY_EXTENSION_MODULE` |
| **Read-Only /v1 API** | `src/openg2p_registry_catalog_extension/controllers/` | Canonical `/v1` REST endpoints (Crops, Seeds, Inputs, Livestock, Locations) |
| **Domain Models** | `register_domain/models/` | SQLAlchemy models for live (`G2PRegister*`), history (`G2PRegisterHistory*`), and intake (`G2PIntakeForm*`) |
| **Pydantic Schemas** | `register_domain/schemas/` | Request/Response validation schemas |
| **Domain Services** | `register_domain/services/` | Search text indexation and display title formatters |
| **Factory** | `register_domain/factory/` | Runtime service resolution per register mnemonic |
| **UI Metadata** | `meta_data/register-metadata/` | SQL definitions for dynamic Next.js Staff Portal rendering (Forms, Tables, Filters) |
| **Seed & Migration** | `scripts/` | Deployment scripts (`deploy_catalog_data.sh`), table DDLs, and metadata seeders |
| **Full Technical Manual** | `CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md` | Comprehensive architectural and operational guide |

---

## Master Registers Defined

All records are identified by both a **business code** and a **UUIDv4** (`public.uuid_generate_v4()`) for clean joins across external modules:

| Register ID | Mnemonic | Subject | Total Live Records | Domain Key / Unique Identifier |
|---|---|---|:---:|---|
| `c1000000-0000-4000-8000-000000000001` | `CropCatalog` | Agricultural Crops | **156** | `crop_code`, `uuid` |
| `c1000000-0000-4000-8000-000000000002` | `SeedCatalog` | Seed Varieties | **1,206** | `seed_code`, `uuid` |
| `c1000000-0000-4000-8000-000000000003` | `InputsCatalog` | Agro-Inputs & Fertilizers | **11** (extensible) | `input_code`, `uuid` |
| `c1000000-0000-4000-8000-000000000004` | `LivestockCatalog` | Livestock Breeds | **94** | `breed_code`, `uuid` |
| `c1000000-0000-4000-8000-000000000005` | `LocationCatalog` | Location Catalog | **21,053** | `location_code`, `pcode`, `uuid` |

### Standard Agro-Input Categories (`InputsCatalog`)
The Inputs Catalog supports 11 standardized agro-input categories (`InputCategoryEnum`):
1. `INORGANIC_FERTILIZER` (NPSB, Urea, DAP)
2. `ORGANIC_FERTILIZER` (Vermicompost, Bio-slurry)
3. `BIO_FERTILIZER` (Rhizobium inoculants)
4. `MICRONUTRIENT` (Zinc Sulphate, Boron)
5. `SOIL_AMENDMENT` (Agricultural Dolomitic Lime, Gypsum)
6. `PESTICIDE` (Broad-spectrum chemical pesticides)
7. `INSECTICIDE` (Deltamethrin, Malathion)
8. `HERBICIDE` (2,4-D Amine, Glyphosate)
9. `FUNGICIDE` (Mancozeb, Propiconazole)
10. `SEED_TREATMENT` (Apron Star, Thiram)
11. `GROWTH_REGULATOR` (Ethephon, Gibberellic acid)
12. `OTHER`

---

## Canonical Read-Only `/v1` REST API

The `/v1` API is strictly **read-only (`GET` only)**. Mutations (`POST`, `PUT`, `DELETE`) are blocked with `HTTP 405 Method Not Allowed`. All responses support **ETag hashing**, `Cache-Control: public, max-age=300`, and `HTTP 304 Not Modified` on `If-None-Match`.

| Endpoint | Method | Key Query Parameters | Description |
|:---|:---:|:---|:---|
| `GET /v1/releases/current` | `GET` | — | Active release metadata and checksum |
| `GET /v1/catalogues` | `GET` | — | Summary list and record counts of all 5 catalogues |
| `GET /v1/catalogues/{code}/values` | `GET` | `search`, `category`, `status`, `page`, `page_size` | Unified router across any catalogue |
| `GET /v1/catalogue-values` | `GET` | `catalogue_code`, `limit` | Compact option tuples (`code`, `display_name`, `uuid`) for UI widgets |
| `GET /v1/inputs` | `GET` | `category`, `manufacturer`, `crops`, `search`, `page`, `page_size` | Search agro-inputs and fertilizers |
| `GET /v1/inputs/{code_or_uuid}` | `GET` | — | Single agro-input by code or UUID |
| `GET /v1/crops` | `GET` | `category`, `ecological_zone`, `search`, `page`, `page_size` | Search agricultural crops |
| `GET /v1/crops/{code_or_uuid}` | `GET` | — | Single crop by code or UUID |
| `GET /v1/seed-varieties` | `GET` | `crop_name`, `is_certified`, `release_year`, `search`, `page`, `page_size` | Search registered seed varieties |
| `GET /v1/seed-varieties/{code_or_uuid}` | `GET` | — | Single seed variety by code or UUID |
| `GET /v1/crop-varieties/{code_or_uuid}` | `GET` | — | Alias for seed variety lookup |
| `GET /v1/livestock/species` | `GET` | — | Distinct species list (`CATTLE`, `SHEEP`, `GOAT`, etc.) |
| `GET /v1/livestock/breeds` | `GET` | `species`, `breed_type`, `primary_purpose`, `search`, `page`, `page_size` | Search livestock breeds |
| `GET /v1/livestock/breeds/{code_or_uuid}` | `GET` | — | Single breed by code or UUID |
| `GET /v1/livestock/reference-data` | `GET` | — | Standard sets: gender, production types, and record statuses |
| `GET /v1/geography/levels` | `GET` | — | Administrative hierarchy levels (Region, Zone, Woreda, Kebele) |
| `GET /v1/geography/units` | `GET` | `level`, `parent_code`, `search`, `page`, `page_size` | Search administrative locations |
| `GET /v1/geography/units/{code_or_uuid}` | `GET` | — | Single location by code, pcode, or UUID |
| `GET /v1/snapshots/current` | `GET` | — | Complete registry snapshot summary |

---

## DevOps & Server Deployment Setup Guide

This section outlines everything required from the **DevOps / SysAdmin / SRE** side to provision, configure, and maintain the Catalog subsystem in production or staging.

### 1. Prerequisites
- **PostgreSQL 14+**: Must have `uuid-ossp` available.
- **Docker & Docker Compose**: Engine 20.10+ / Compose V2.
- **Network Ports**:
  - `8002`: Staff API & public `/v1` read-only API
  - `3002`: OpenG2P Staff UI Portal
  - `5432` / `5445`: PostgreSQL database

### 2. Database Provisioning (Mandatory First Step)
Before launching the API container or running migrations, the PostgreSQL database must have the `"uuid-ossp"` extension enabled:

```sql
-- Connect to Postgres as superuser:
CREATE DATABASE catalog_registry_db;
\c catalog_registry_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 3. Master Data & Metadata Deployment
Run the idempotent master deployment script to create all 22 tables, register OpenG2P UI metadata, and load all 21,053 locations, 1,206 seeds, 156 crops, 94 livestock breeds, and 11 agro-inputs:

```bash
cd catalog-extension

# Option A: Run automated script
PGHOST=your-postgres-host PGPORT=5432 PGDATABASE=catalog_registry_db PGUSER=postgres PGPASSWORD=your-password ./scripts/deploy_catalog_data.sh

# Option B: Manual SQL execution via psql
psql -h $PGHOST -U $PGUSER -d catalog_registry_db -f scripts/init_catalog_tables.sql
psql -h $PGHOST -U $PGUSER -d catalog_registry_db -f scripts/init_location_tables.sql
psql -h $PGHOST -U $PGUSER -d catalog_registry_db -f scripts/init_location_metadata.sql
psql -h $PGHOST -U $PGUSER -d catalog_registry_db -f scripts/seed_all_catalogs_data.sql
python3 scripts/seed_catalog_metadata.py
```

### 4. Docker Compose Reference Service
Add the following service to your `docker-compose.yml`:

```yaml
services:
  catalog-registry-staff-api:
    image: registry.gitlab.com/openg2p/registry/registry-platform/staff-api:0.0.0-develop.384
    container_name: catalog-registry-staff-api
    restart: unless-stopped
    ports:
      - "8002:8000"
    environment:
      - DB_DATASOURCE=postgresql+asyncpg://postgres:postgres@farmer-registry-postgres:5432/catalog_registry_db
      - REGISTRY_EXTENSION_MODULE=openg2p_registry_catalog_extension
      - OPENAPI_COMMON_API_PREFIX=
      - CORS_ALLOW_ORIGINS=["*"]
      - CORS_ALLOW_CREDENTIALS=true
      - NO_OF_WORKERS=2
      - WORKER_TYPE=uvicorn
    volumes:
      - ./catalog-extension/src/openg2p_registry_catalog_extension:/usr/local/lib/python3.12/site-packages/openg2p_registry_catalog_extension:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v1/releases/current"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 20s
    networks:
      - openagri-network
```

### 5. Verification Smoke Tests
Run these curl commands to verify service health immediately after deployment:

```bash
# 1. Health check & current release metadata
curl -s http://localhost:8002/v1/releases/current | jq .

# 2. Verify all 5 catalogues and record counts
curl -s http://localhost:8002/v1/catalogues | jq .

# 3. Verify agro-inputs with UUIDv4
curl -s "http://localhost:8002/v1/inputs?category=INSECTICIDE" | jq .

# 4. Verify crops search
curl -s "http://localhost:8002/v1/crops?search=Teff" | jq .

# 5. Verify HTTP 304 ETag caching
curl -i -s -H 'If-None-Match: "032e9a22bb86acf8b694b41866203a27"' http://localhost:8002/v1/releases/current

# 6. Verify mutation prevention (Must return 405 Method Not Allowed)
curl -i -s -X POST http://localhost:8002/v1/inputs -d '{"test":"forbidden"}'
```

### 6. DevOps Troubleshooting Runbook
- **`function public.uuid_generate_v4() does not exist`**: The `"uuid-ossp"` extension was not created in PostgreSQL. Run `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` in `catalog_registry_db`.
- **Database lock on startup (`pg_try_advisory_lock`)**: If a previous container was abruptly killed, clear the advisory lock by executing `SELECT pg_advisory_unlock_all();` in PostgreSQL.
- **Data masking in UI**: Ensure `_patch_policy_builder()` in `app.py` is loaded. It bypasses sync/async caller evaluation issues in the OpenG2P core library.

---

## Detailed Technical Documentation

For complete schema details, architectural designs, cross-registry joins, and full API payloads, refer to:
- [CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md](file:///home/megha/Videos/gen%202%20last%20aug%2018/catalog-extension/CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md)
