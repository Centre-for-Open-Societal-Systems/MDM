# OpenAgriNet Master Data Management (MDM)

[![OpenG2P](https://img.shields.io/badge/Platform-OpenG2P-blue.svg)](https://openg2p.org)
[![FastAPI](https://img.shields.io/badge/API-FastAPI%20v1-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2014%2B-blue.svg)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Authoritative **Master Data Management (MDM)** and Reference Catalogues for the Ethiopian Agricultural Registry ecosystem (Ministry of Agriculture, Agricultural Transformation Institute - ATI, Ethio-Seed, and LITS).

This repository builds the complete Catalog Registry platform from scratch, including:
1. **OpenG2P Catalog Extension (`catalog-extension`)**: Custom registers, data models, schemas, and dynamic Next.js UI metadata for OpenG2P Staff Portal.
2. **Canonical Read-Only `/v1` REST APIs**: High-performance, cached, strictly read-only public endpoints with enforced pagination, search, category filtering, and ETag hashing.
3. **Database Architecture & UUIDv4 Integration**: Fully normalized tables carrying `public.uuid_generate_v4()` identifiers across all tables for stable cross-registry joins.
4. **DevOps & Docker Deployment**: Unified multi-stage Docker build and compose orchestration for server and Kubernetes publishing.

---

## 1. Master Data Catalogues

All catalog records carry both a human-readable **business code** and a canonical **UUIDv4** (`public.uuid_generate_v4()`):

| Catalogue Code | Register Mnemonic | Subject | Records | Key Identifier | Description |
|:---|:---|:---|:---:|:---|:---|
| `crops` | `CropCatalog` | Agricultural Crops | **156** | `crop_code`, `uuid` | National crop master data with growth cycles, ecological zones, and water requirements. |
| `seeds` | `SeedCatalog` | Seed Varieties | **1,206** | `seed_code`, `uuid` | Officially released & registered seed varieties with breeder source, certification, and yields. |
| `inputs` | `InputsCatalog` | Agro-Inputs & Fertilizers | **11** | `input_code`, `uuid` | Standardized agro-inputs covering inorganic/organic fertilizers, pesticides, herbicides, etc. |
| `livestock` | `LivestockCatalog` | Livestock Breeds | **94** | `breed_code`, `uuid` | Cattle, sheep, goat, camel, and beehive breeds aligned with National Standards and ET-LITS. |
| `locations` | `LocationCatalog` | Administrative Geolocation | **21,053** | `location_code`, `uuid` | Standardized Ethiopian administrative hierarchy: 14 Regions, 125 Zones, 1,379 Woredas, 19,535 Kebeles. |

### Standard Agro-Input Categories (`InputsCatalog`)
The generalized `InputsCatalog` schema supports 11 standardized agro-input categories (`InputCategoryEnum`):
- `INORGANIC_FERTILIZER` (NPSB, Urea 46-0-0, DAP)
- `ORGANIC_FERTILIZER` (Bio-Green Vermicompost, Compost)
- `BIO_FERTILIZER` (Legume Bio-Rhizobium)
- `MICRONUTRIENT` (Zinc Sulphate, Boron)
- `SOIL_AMENDMENT` (Agricultural Dolomitic Lime, Gypsum)
- `PESTICIDE` (Broad-spectrum chemical crop protection)
- `INSECTICIDE` (Decis Deltamethrin, Malathion)
- `HERBICIDE` (2,4-D Amine, Glyphosate)
- `FUNGICIDE` (Mancozeb, Propiconazole)
- `SEED_TREATMENT` (Apron Star, Thiram dressing)
- `GROWTH_REGULATOR` (Plant growth regulators)
- `OTHER` (General agro-inputs)

---

## 2. Canonical Read-Only `/v1` REST API

The `/v1` API is strictly **read-only (`GET` only)**. All mutation requests (`POST`, `PUT`, `DELETE`) are blocked with `HTTP 405 Method Not Allowed`. Responses feature **ETag hashing** and return `HTTP 304 Not Modified` on `If-None-Match` polls.

| Endpoint | Method | Filters & Query Parameters | Description |
|:---|:---:|:---|:---|
| `/v1/releases/current` | `GET` | — | Current release metadata, schema version, and checksum. |
| `/v1/catalogues` | `GET` | — | Summary list and record counts of all 5 catalogues. |
| `/v1/catalogues/{code}/values` | `GET` | `search`, `category`, `status`, `page`, `page_size` | Unified query router across any catalogue. |
| `/v1/catalogue-values` | `GET` | `catalogue_code`, `limit` | Compact option tuples (`code`, `display_name`, `uuid`) for UI dropdowns. |
| `/v1/inputs` | `GET` | `category`, `manufacturer`, `crops`, `search`, `page`, `page_size` | List and search agro-inputs and fertilizers. |
| `/v1/inputs/{code_or_uuid}` | `GET` | — | Single agro-input by code or UUID. |
| `/v1/crops` | `GET` | `category`, `ecological_zone`, `search`, `page`, `page_size` | List and search agricultural crops. |
| `/v1/crops/{code_or_uuid}` | `GET` | — | Single crop by code or UUID. |
| `/v1/seed-varieties` | `GET` | `crop_name`, `is_certified`, `release_year`, `search`, `page`, `page_size` | List and search seed varieties. |
| `/v1/seed-varieties/{code_or_uuid}` | `GET` | — | Single seed variety by code or UUID. |
| `/v1/crop-varieties/{code_or_uuid}` | `GET` | — | Alias for seed variety lookup. |
| `/v1/livestock/species` | `GET` | — | Distinct species list (`CATTLE`, `SHEEP`, `GOAT`, `CAMEL`, `BEEHIVE`). |
| `/v1/livestock/breeds` | `GET` | `species`, `breed_type`, `primary_purpose`, `search`, `page`, `page_size` | List and search livestock breeds. |
| `/v1/livestock/breeds/{code_or_uuid}` | `GET` | — | Single breed by code or UUID. |
| `/v1/livestock/reference-data` | `GET` | — | Reference sets: gender, production types, and record statuses. |
| `/v1/geography/levels` | `GET` | — | Administrative levels definition (Region, Zone, Woreda, Kebele). |
| `/v1/geography/units` | `GET` | `level`, `parent_code`, `search`, `page`, `page_size` | List and search administrative locations. |
| `/v1/geography/units/{code_or_uuid}` | `GET` | — | Single location by code, pcode, or UUID. |
| `/v1/snapshots/current` | `GET` | — | Complete registry snapshot summary. |

### Quick API Examples
```bash
# Get catalogue overview
curl -s http://localhost:8002/v1/catalogues | jq .

# Search inputs by category (e.g. INSECTICIDE)
curl -s "http://localhost:8002/v1/inputs?category=INSECTICIDE" | jq .

# Lookup by UUID
curl -s "http://localhost:8002/v1/inputs/94f46e61-d060-4956-afaa-23dfbe3b4ac8" | jq .

# Search crops
curl -s "http://localhost:8002/v1/crops?search=Teff" | jq .

# Compact dropdown values for UI widgets
curl -s "http://localhost:8002/v1/catalogue-values?catalogue_code=input_categories" | jq .

# Verify ETag 304 response
curl -i -s -H 'If-None-Match: "032e9a22bb86acf8b694b41866203a27"' http://localhost:8002/v1/releases/current
```

---

## 3. DevOps & Server Deployment Setup Guide

This section is for **DevOps Engineers and SREs** publishing this repository on a new server or Kubernetes environment.

### Step 1: System Prerequisites
- **PostgreSQL 14+**: Must have `uuid-ossp` extension available.
- **Docker 20.10+ & Docker Compose V2**
- **Ports Required**:
  - `8002`: Staff API & Read-Only `/v1` REST API
  - `3002`: OpenG2P Staff UI Portal
  - `5432` / `5445`: PostgreSQL database

### Step 2: Database Provisioning (Mandatory)
Connect to PostgreSQL as a superuser and ensure `catalog_registry_db` and the `"uuid-ossp"` extension exist:
```sql
CREATE DATABASE catalog_registry_db;
\c catalog_registry_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Step 3: Run Master Data Deployment
Run the automated, idempotent deployment script to create all 22 physical tables, register OpenG2P UI metadata, populate all 21,053 locations, 1,206 seeds, 156 crops, 94 livestock breeds, 11 agro-inputs, and backfill UUIDv4 keys:

```bash
# From repository root:
PGHOST=your-db-host PGPORT=5432 PGDATABASE=catalog_registry_db PGUSER=postgres PGPASSWORD=your-password \
  ./catalog-extension/scripts/deploy_catalog_data.sh
```

### Step 4: Configure Environment & Launch Docker Compose
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Adjust database credentials in .env
nano .env

# 3. Build and launch services
docker compose up -d --build
```

### Step 5: Post-Deployment Smoke Tests
Execute the following verification checklist:
```bash
# 1. Check container health
docker compose ps

# 2. Test Staff API / v1 releases
curl -s http://localhost:8002/v1/releases/current | jq .

# 3. Test Staff UI
curl -I http://localhost:3002

# 4. Verify mutation rejection (Must return 405 Method Not Allowed)
curl -i -s -X POST http://localhost:8002/v1/inputs -d '{}'
```

---

## 4. Repository Layout

```
MDM/
├── .env.example                                   # Environment configuration template
├── .gitignore                                     # Clean Git ignore rules (no caches/binaries)
├── Dockerfile                                     # Unified multi-stage Docker build
├── docker-compose.yml                             # Container orchestration definition
├── README.md                                      # Repository overview & quickstart
├── docs/
│   ├── CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md  # Comprehensive technical manual
│   ├── EAON_PLAN_SOW_Master Data Management_D1.docx   # Scope of Work specification
│   └── MDM_via_Registry_Platform - System design.docx # Architectural design document
└── catalog-extension/                             # OpenG2P Catalog Extension Python package
    ├── pyproject.toml                             # Hatchling build configuration
    ├── README.md                                  # Extension documentation
    ├── scripts/
    │   ├── deploy_catalog_data.sh                 # Idempotent master database deployer
    │   ├── init_catalog_tables.sql                # DDL for master catalog tables
    │   ├── init_location_tables.sql               # DDL for location hierarchy
    │   ├── init_location_metadata.sql             # OpenG2P UI metadata for LocationCatalog
    │   ├── seed_all_catalogs_data.sql             # Seed SQL for all catalogues
    │   └── seed_catalog_metadata.py               # Metadata loader for OpenG2P registers
    └── src/openg2p_registry_catalog_extension/
        ├── __init__.py
        ├── app.py                                 # Extension Initializer & DB migrations
        ├── config.py                              # Configuration & settings
        ├── controllers/
        │   ├── __init__.py
        │   └── v1_readonly_controller.py          # Read-only /v1 REST API controller
        ├── register_domain/
        │   ├── factory/                           # Domain service resolver
        │   ├── models/                            # SQLAlchemy models (Crops, Seeds, Inputs, etc.)
        │   ├── schemas/                           # Pydantic validation schemas
        │   └── services/                          # Domain services & search indexers
        └── meta_data/
            ├── register-metadata/                 # 9 UI metadata SQL definitions
            └── registry-configurations/           # Themes & language configurations
```

---

## 5. Further Documentation

For full architectural deep-dives, entity relationship diagrams, database schemas, and SRE runbooks, see:
- [docs/CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md](file:///home/megha/Videos/gen%202%20last%20aug%2018/MDM/docs/CATALOG_MASTER_DATA_DEVELOPER_DEVOPS_GUIDE.md)
