-- OpenG2P Location Catalog DDL Script
-- Single Location Register with linked sub-category tables for Regions, Zones, Woredas, Kebeles

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. LINKED SUB-CATEGORY TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.geo_regions (
    region_id VARCHAR(50) PRIMARY KEY,
    region_code VARCHAR(50) UNIQUE NOT NULL,
    region_name VARCHAR(200) NOT NULL,
    pcode VARCHAR(50),
    capital VARCHAR(100),
    area_sq_km NUMERIC(12, 2),
    zones_count INTEGER DEFAULT 0,
    woredas_count INTEGER DEFAULT 0,
    kebeles_count INTEGER DEFAULT 0,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE IF NOT EXISTS public.geo_zones (
    zone_id VARCHAR(50) PRIMARY KEY,
    zone_code VARCHAR(50) UNIQUE NOT NULL,
    zone_name VARCHAR(200) NOT NULL,
    pcode VARCHAR(50),
    region_code VARCHAR(50) NOT NULL,
    region_name VARCHAR(200) NOT NULL,
    capital VARCHAR(100),
    area_sq_km NUMERIC(12, 2),
    woredas_count INTEGER DEFAULT 0,
    kebeles_count INTEGER DEFAULT 0,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE IF NOT EXISTS public.geo_woredas (
    woreda_id VARCHAR(50) PRIMARY KEY,
    woreda_code VARCHAR(50) UNIQUE NOT NULL,
    woreda_name VARCHAR(200) NOT NULL,
    pcode VARCHAR(50),
    zone_code VARCHAR(50),
    zone_name VARCHAR(200),
    region_code VARCHAR(50) NOT NULL,
    region_name VARCHAR(200) NOT NULL,
    kebeles_count INTEGER DEFAULT 0,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE IF NOT EXISTS public.geo_kebeles (
    kebele_id VARCHAR(50) PRIMARY KEY,
    kebele_code VARCHAR(50) UNIQUE NOT NULL,
    kebele_name VARCHAR(200) NOT NULL,
    pcode VARCHAR(50),
    woreda_code VARCHAR(50) NOT NULL,
    woreda_name VARCHAR(200) NOT NULL,
    zone_code VARCHAR(50),
    zone_name VARCHAR(200),
    region_code VARCHAR(50) NOT NULL,
    region_name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);

-- Indexes on sub-category tables
CREATE INDEX IF NOT EXISTS ix_geo_zones_region_code ON public.geo_zones (region_code);
CREATE INDEX IF NOT EXISTS ix_geo_woredas_zone_code ON public.geo_woredas (zone_code);
CREATE INDEX IF NOT EXISTS ix_geo_woredas_region_code ON public.geo_woredas (region_code);
CREATE INDEX IF NOT EXISTS ix_geo_kebeles_woreda_code ON public.geo_kebeles (woreda_code);
CREATE INDEX IF NOT EXISTS ix_geo_kebeles_zone_code ON public.geo_kebeles (zone_code);
CREATE INDEX IF NOT EXISTS ix_geo_kebeles_region_code ON public.geo_kebeles (region_code);

-- ============================================================================
-- 2. MAIN LOCATION REGISTER TABLES (Maker-Checker & Staff UI)
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.g2p_register_location_catalogs (
    internal_record_id VARCHAR PRIMARY KEY,
    functional_record_id VARCHAR,
    link_internal_record_id VARCHAR,
    link_foundational_id VARCHAR,
    record_name VARCHAR,
    record_image_document_id VARCHAR,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    last_approved_at TIMESTAMP WITHOUT TIME ZONE,
    last_approved_by VARCHAR,
    search_text TEXT,
    record_status VARCHAR DEFAULT 'ACTIVE',
    record_status_reason VARCHAR,
    location_code VARCHAR(50) UNIQUE NOT NULL,
    location_name VARCHAR(200) NOT NULL,
    admin_level VARCHAR(50) NOT NULL,
    admin_level_code VARCHAR(50),
    parent_location_code VARCHAR(50),
    parent_location_name VARCHAR(200),
    capital_city VARCHAR(100),
    area_sq_km NUMERIC(12, 2),
    population_estimate BIGINT,
    pcode VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    geo_lowest_level_value_id VARCHAR,
    geo_code_hierarchy_json JSONB,
    region_name VARCHAR,
    zone_name VARCHAR,
    woreda_name VARCHAR,
    kebele_name VARCHAR,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    altitude NUMERIC(10, 2),
    plus_code VARCHAR,
    address_line_1 VARCHAR,
    address_line_2 VARCHAR,
    postal_code VARCHAR,
    country_code VARCHAR
);

CREATE TABLE IF NOT EXISTS public.g2p_register_history_location_catalogs (
    history_record_id VARCHAR PRIMARY KEY,
    internal_record_id VARCHAR NOT NULL,
    tab_id VARCHAR NOT NULL,
    section_id VARCHAR NOT NULL,
    change_request_id VARCHAR,
    submission_id VARCHAR,
    change_request_source VARCHAR NOT NULL,
    is_primary_section BOOLEAN NOT NULL,
    functional_record_id VARCHAR,
    link_internal_record_id VARCHAR,
    subject_internal_record_id VARCHAR,
    link_foundational_id VARCHAR,
    record_name VARCHAR,
    record_image_document_id TEXT,
    record_status VARCHAR NOT NULL,
    record_status_reason VARCHAR,
    created_by VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    approved_by VARCHAR NOT NULL,
    approved_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    location_code VARCHAR(50),
    location_name VARCHAR(200),
    admin_level VARCHAR(50),
    admin_level_code VARCHAR(50),
    parent_location_code VARCHAR(50),
    parent_location_name VARCHAR(200),
    capital_city VARCHAR(100),
    area_sq_km NUMERIC(12, 2),
    population_estimate BIGINT,
    pcode VARCHAR(50),
    description TEXT,
    is_active BOOLEAN,
    geo_lowest_level_value_id VARCHAR,
    geo_code_hierarchy_json JSONB,
    region_name VARCHAR,
    zone_name VARCHAR,
    woreda_name VARCHAR,
    kebele_name VARCHAR,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    altitude NUMERIC(10, 2),
    plus_code VARCHAR,
    address_line_1 VARCHAR,
    address_line_2 VARCHAR,
    postal_code VARCHAR,
    country_code VARCHAR
);

CREATE TABLE IF NOT EXISTS public.g2p_intake_form_location_catalogs (
    submission_id UUID NOT NULL,
    application_reference VARCHAR(255),
    internal_record_id VARCHAR NOT NULL,
    action_type VARCHAR,
    is_approved BOOLEAN,
    approval_status VARCHAR,
    rejection_reason VARCHAR,
    functional_record_id VARCHAR,
    link_internal_record_id VARCHAR,
    link_foundational_id VARCHAR,
    record_name VARCHAR,
    record_image_document_id VARCHAR,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    last_approved_at TIMESTAMP WITHOUT TIME ZONE,
    last_approved_by VARCHAR,
    search_text TEXT,
    record_status VARCHAR DEFAULT 'ACTIVE',
    record_status_reason VARCHAR,
    location_code VARCHAR(50),
    location_name VARCHAR(200),
    admin_level VARCHAR(50),
    admin_level_code VARCHAR(50),
    parent_location_code VARCHAR(50),
    parent_location_name VARCHAR(200),
    capital_city VARCHAR(100),
    area_sq_km NUMERIC(12, 2),
    population_estimate BIGINT,
    pcode VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    geo_lowest_level_value_id VARCHAR,
    geo_code_hierarchy_json JSONB,
    region_name VARCHAR,
    zone_name VARCHAR,
    woreda_name VARCHAR,
    kebele_name VARCHAR,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    altitude NUMERIC(10, 2),
    plus_code VARCHAR,
    address_line_1 VARCHAR,
    address_line_2 VARCHAR,
    postal_code VARCHAR,
    country_code VARCHAR,
    PRIMARY KEY (submission_id, internal_record_id)
);

-- ============================================================================
-- 3. INDEXES
-- ============================================================================
CREATE INDEX IF NOT EXISTS ix_location_catalog_admin_level ON public.g2p_register_location_catalogs (admin_level);
CREATE INDEX IF NOT EXISTS ix_location_catalog_parent_code ON public.g2p_register_location_catalogs (parent_location_code);
CREATE INDEX IF NOT EXISTS ix_location_catalog_search_text ON public.g2p_register_location_catalogs USING gin (search_text gin_trgm_ops);
