#!/usr/bin/env bash
# ==============================================================================
# OpenG2P Catalog Extension - Master Database Deployment & Data Import Script
# ==============================================================================
# This script sets up the database schema, registers OpenG2P metadata,
# and imports all catalog data (Crop, Seed, Livestock, and Location)
# on any server, Kubernetes pod, or local docker environment.
#
# Usage:
#   ./scripts/deploy_catalog_data.sh
#   Or with custom connection parameters:
#   PGHOST=localhost PGPORT=5445 PGDATABASE=catalog_registry_db PGUSER=postgres PGPASSWORD=postgres ./scripts/deploy_catalog_data.sh
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Database Connection Settings (with fallback defaults)
export PGHOST="${PGHOST:-${REGISTRY_EXTENSIONS_DB_HOSTNAME:-${COMMON_DB_HOSTNAME:-localhost}}}"
export PGPORT="${PGPORT:-${REGISTRY_EXTENSIONS_DB_PORT:-${COMMON_DB_PORT:-5432}}}"
export PGDATABASE="${PGDATABASE:-${REGISTRY_EXTENSIONS_DB_DBNAME:-${COMMON_DB_DBNAME:-catalog_registry_db}}}"
export PGUSER="${PGUSER:-${REGISTRY_EXTENSIONS_DB_USERNAME:-${COMMON_DB_USERNAME:-postgres}}}"
export PGPASSWORD="${PGPASSWORD:-${REGISTRY_EXTENSIONS_DB_PASSWORD:-${COMMON_DB_PASSWORD:-postgres}}}"

# Check for psql client
PSQL_CMD="psql"
if ! command -v psql &> /dev/null; then
    # Check if docker is available to run via container
    if command -v docker &> /dev/null && docker ps | grep -q "postgres"; then
        PG_CONTAINER=$(docker ps --format '{{.Names}}' | grep "postgres" | head -n 1)
        echo "[INFO] Local psql not found, using docker exec on container: ${PG_CONTAINER}"
        PSQL_CMD="docker exec -i ${PG_CONTAINER} psql -U ${PGUSER} -d ${PGDATABASE}"
    else
        echo "[ERROR] 'psql' client not found on PATH. Please install postgresql-client or run inside container."
        exit 1
    fi
else
    PSQL_CMD="psql -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${PGDATABASE} -v ON_ERROR_STOP=1"
fi

echo "=============================================================================="
echo " OpenG2P Catalog Registry - Deployment & Data Ingestion"
echo " Target: ${PGUSER}@${PGHOST}:${PGPORT}/${PGDATABASE}"
echo "=============================================================================="

# 1. Test Connection
echo "[1/5] Testing database connectivity..."
${PSQL_CMD} -c "SELECT 1;" > /dev/null
echo "      Database connection OK."

# 2. Initialize Catalog and Location Tables
echo "[2/5] Creating catalog and location physical tables (DDL)..."
if [ -f "${SCRIPT_DIR}/init_catalog_tables.sql" ]; then
    ${PSQL_CMD} -f "${SCRIPT_DIR}/init_catalog_tables.sql" > /dev/null
fi
if [ -f "${SCRIPT_DIR}/init_location_tables.sql" ]; then
    ${PSQL_CMD} -f "${SCRIPT_DIR}/init_location_tables.sql" > /dev/null
fi
echo "      Physical tables and search indexes created."

# 3. Initialize OpenG2P Metadata
echo "[3/5] Registering OpenG2P catalog metadata, schemas, tabs, and intake forms..."
if [ -d "${BASE_DIR}/src/openg2p_registry_catalog_extension/meta_data/register-metadata" ]; then
    for f in "${BASE_DIR}/src/openg2p_registry_catalog_extension/meta_data/register-metadata/"*.sql; do
        if [ -f "$f" ]; then
            ${PSQL_CMD} -f "$f" > /dev/null
        fi
    done
fi
if [ -f "${SCRIPT_DIR}/init_location_metadata.sql" ]; then
    ${PSQL_CMD} -f "${SCRIPT_DIR}/init_location_metadata.sql" > /dev/null
fi
echo "      Metadata definitions in place."

# 4. Ingest Catalog & Location Data
echo "[4/5] Ingesting catalog and location data..."

# Check if standalone dump is available
if [ -f "${SCRIPT_DIR}/seed_all_catalogs_data.sql" ]; then
    echo "      Loading all catalog & location data from seed_all_catalogs_data.sql..."
    ${PSQL_CMD} -f "${SCRIPT_DIR}/seed_all_catalogs_data.sql" > /dev/null
    echo "      Seed data loaded successfully."
elif [ -f "${SCRIPT_DIR}/seed_reference_catalogs.sql" ]; then
    echo "      Loading reference catalogs from seed_reference_catalogs.sql..."
    ${PSQL_CMD} -f "${SCRIPT_DIR}/seed_reference_catalogs.sql" > /dev/null
fi

# If live ETL ingestion from master data is requested or needed
if [ "${LIVE_ETL:-false}" = "true" ] && [ -f "${SCRIPT_DIR}/ingest_location_baseline.py" ]; then
    echo "      Running live ETL ingestion from master data..."
    python3 "${SCRIPT_DIR}/ingest_location_baseline.py" \
        --src-host "${MASTER_DATA_DB_HOSTNAME:-${COMMON_DB_HOSTNAME:-farmer-registry-postgres}}" \
        --src-db "${MASTER_DATA_DB_DBNAME:-farmer_master_data_db}" \
        --tgt-host "${PGHOST}" \
        --tgt-port "${PGPORT}" \
        --tgt-user "${PGUSER}" \
        --tgt-pass "${PGPASSWORD}" \
        --tgt-db "${PGDATABASE}"
fi

echo "[4b/5] Ensuring public.uuid_generate_v4() identifiers are populated..."
${PSQL_CMD} <<'EOF' > /dev/null
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DO $$
DECLARE
    tbl text;
    catalog_tables text[] := ARRAY[
        'crop_categories', 'crop_catalog', 'crop_varieties', 'ecological_zones',
        'seed_crops', 'seed_varieties', 'seed_catalog', 'livestock_types',
        'livestock_breeds', 'livestock_catalog', 'geo_regions', 'geo_zones',
        'geo_woredas', 'geo_kebeles', 'g2p_register_crop_catalogs',
        'g2p_register_seed_catalogs', 'g2p_register_input_catalogs',
        'g2p_register_livestock_catalogs', 'g2p_register_location_catalogs'
    ];
BEGIN
    FOREACH tbl IN ARRAY catalog_tables LOOP
        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = tbl) THEN
            EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS uuid UUID DEFAULT public.uuid_generate_v4();', tbl);
            EXECUTE format('UPDATE public.%I SET uuid = public.uuid_generate_v4() WHERE uuid IS NULL;', tbl);
            EXECUTE format('ALTER TABLE public.%I ALTER COLUMN uuid SET NOT NULL;', tbl);
            EXECUTE format('CREATE UNIQUE INDEX IF NOT EXISTS %I ON public.%I (uuid);', 'ix_' || tbl || '_uuid', tbl);
        END IF;
    END LOOP;
END $$;
EOF
echo "      UUID identifiers verified and backfilled."

# 5. Verification & Summary
echo "[5/5] Verifying catalog counts..."
echo "------------------------------------------------------------------------------"
${PSQL_CMD} -t -A -c "
SELECT 'Crop Catalog Register:      ' || count(*) FROM g2p_register_crop_catalogs
UNION ALL SELECT 'Seed Catalog Register:      ' || count(*) FROM g2p_register_seed_catalogs
UNION ALL SELECT 'Inputs Catalog Register:    ' || count(*) FROM g2p_register_input_catalogs
UNION ALL SELECT 'Livestock Catalog Register: ' || count(*) FROM g2p_register_livestock_catalogs
UNION ALL SELECT 'Location Catalog Register:  ' || count(*) FROM g2p_register_location_catalogs
UNION ALL SELECT '-------------------------------------------'
UNION ALL SELECT 'Geo Regions (Level 1):      ' || count(*) FROM geo_regions
UNION ALL SELECT 'Geo Zones (Level 2):        ' || count(*) FROM geo_zones
UNION ALL SELECT 'Geo Woredas (Level 3):      ' || count(*) FROM geo_woredas
UNION ALL SELECT 'Geo Kebeles (Level 4):      ' || count(*) FROM geo_kebeles;
"
echo "------------------------------------------------------------------------------"
echo " [SUCCESS] Catalog extension database deployment & data import completed!"
echo "=============================================================================="
