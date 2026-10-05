#!/usr/bin/env python3
"""OpenG2P Catalog Extension - Sync from Reference Server
Syncs live reference data from Ethiopian National Catalogue Console (http://3.110.195.9)
into PostgreSQL database tables and generates reproducible SQL seed scripts:
- Crop: Categories, Ecological Zones, Crops (150)
- Seed: Seed Crops (129), Seed Varieties (902)
- Livestock: Livestock Types (5), Livestock Breeds (94)
"""

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE_URL = os.getenv("REFERENCE_SERVER_URL", "http://3.110.195.9")
DB_CONTAINER = os.getenv("PGCONTAINER", "farmer-registry-postgres")
DB_NAME = os.getenv("PGDATABASE", "catalog_registry_db")
DB_USER = os.getenv("PGUSER", "postgres")


def fetch_json(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Fetching from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "OpenG2P-Catalog-Sync/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def sql_escape(val):
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val).replace("'", "''")
    return f"'{s}'"


def sync_all():
    print(f"=== Starting Sync from Reference Server: {BASE_URL} ===")
    sql_statements = []

    # =========================================================================
    # 1. CROP CATEGORIES
    # =========================================================================
    cat_data = fetch_json("/v1/catalogues/crop_category/values?page_size=100")
    cat_values = cat_data.get("values", [])
    print(f"Fetched {len(cat_values)} crop categories.")

    sql_statements.append("-- 1. CROP CATEGORIES")
    for cat in cat_values:
        cid = f"cat-{cat['code']}"
        code = cat['code']
        name = cat['display_name']
        meta = cat.get("metadata") or {}
        desc = meta.get("description") or f"Category for {name}"
        status = cat.get("status", "ACTIVE")
        sql = f"""INSERT INTO public.crop_categories (category_id, category_code, category_name, description, status, is_active)
VALUES ({sql_escape(cid)}, {sql_escape(code)}, {sql_escape(name)}, {sql_escape(desc)}, {sql_escape(status)}, TRUE)
ON CONFLICT (category_code) DO UPDATE SET
    category_name = EXCLUDED.category_name,
    description = EXCLUDED.description,
    status = EXCLUDED.status;"""
        sql_statements.append(sql)

    # =========================================================================
    # 2. ECOLOGICAL ZONES
    # =========================================================================
    eco_data = fetch_json("/v1/catalogues/ecological_zone/values?page_size=100")
    eco_values = eco_data.get("values", [])
    print(f"Fetched {len(eco_values)} ecological zones.")

    sql_statements.append("\n-- 2. ECOLOGICAL ZONES")
    for eco in eco_values:
        zid = f"eco-{eco['code']}"
        code = eco['code']
        name = eco['display_name']
        meta = eco.get("metadata") or {}
        desc = meta.get("description") or f"Zone for {name}"
        status = eco.get("status", "ACTIVE")
        sql = f"""INSERT INTO public.ecological_zones (zone_id, zone_code, zone_name, description, status, is_active)
VALUES ({sql_escape(zid)}, {sql_escape(code)}, {sql_escape(name)}, {sql_escape(desc)}, {sql_escape(status)}, TRUE)
ON CONFLICT (zone_code) DO UPDATE SET
    zone_name = EXCLUDED.zone_name,
    description = EXCLUDED.description,
    status = EXCLUDED.status;"""
        sql_statements.append(sql)

    # =========================================================================
    # 3. CROPS (All 150 crops)
    # =========================================================================
    crop_data = fetch_json("/v1/catalogues/crop/values?page_size=250")
    crop_values = crop_data.get("values", [])
    print(f"Fetched {len(crop_values)} crops.")

    sql_statements.append("\n-- 3. CROP CATALOG MASTER (150 CROPS)")
    for c in crop_values:
        code = str(c['code'])
        display_name = c['display_name']
        meta = c.get("metadata") or {}
        relations = c.get("relations") or []

        category_name = None
        eco_zone_name = None
        for r in relations:
            if r.get("type") == "category":
                category_name = r.get("target_display_name")
            elif r.get("type") == "preferred_ecological_zone":
                eco_zone_name = r.get("target_display_name")

        sci_name = meta.get("scientific_name") or ""
        centre = meta.get("centre") or ""
        varieties_count = meta.get("varieties_count") or 0
        known_for = meta.get("known_for") or ""
        desc = meta.get("description") or ""
        inspections = meta.get("num_field_inspection_needed") or 0
        isolation = meta.get("isolation_distance") or 0
        status = c.get("status", "ACTIVE")

        internal_id = f"crop-catalog-{code}"
        search_text = f"{code} {display_name} {sci_name} {category_name or ''} {centre or ''}".strip()

        sql = f"""INSERT INTO public.g2p_register_crop_catalogs (
    internal_record_id, record_name, crop_code, crop_name, scientific_name,
    crop_category, preferred_ecological_zone, centre, varieties_count, known_for,
    num_field_inspection_needed, isolation_distance, description, is_active, search_text, record_status
) VALUES (
    {sql_escape(internal_id)}, {sql_escape(display_name)}, {sql_escape(code)}, {sql_escape(display_name)}, {sql_escape(sci_name)},
    {sql_escape(category_name)}, {sql_escape(eco_zone_name)}, {sql_escape(centre)}, {sql_escape(varieties_count)}, {sql_escape(known_for)},
    {sql_escape(inspections)}, {sql_escape(isolation)}, {sql_escape(desc)}, TRUE, {sql_escape(search_text)}, {sql_escape(status)}
)
ON CONFLICT (crop_code) DO UPDATE SET
    crop_name = EXCLUDED.crop_name,
    scientific_name = EXCLUDED.scientific_name,
    crop_category = EXCLUDED.crop_category,
    preferred_ecological_zone = EXCLUDED.preferred_ecological_zone,
    centre = EXCLUDED.centre,
    varieties_count = EXCLUDED.varieties_count,
    known_for = EXCLUDED.known_for,
    num_field_inspection_needed = EXCLUDED.num_field_inspection_needed,
    isolation_distance = EXCLUDED.isolation_distance,
    description = EXCLUDED.description,
    search_text = EXCLUDED.search_text,
    record_status = EXCLUDED.record_status;"""
        sql_statements.append(sql)

    # =========================================================================
    # 4. CROP VARIETIES (Top 300 varieties)
    # =========================================================================
    var_data = fetch_json("/v1/catalogues/crop_variety/values?page_size=300")
    var_values = var_data.get("values", [])
    print(f"Fetched {len(var_values)} crop varieties.")

    sql_statements.append("\n-- 4. CROP VARIETIES")
    for v in var_values:
        v_code = str(v['code'])
        v_name = v['display_name']
        v_id = f"var-{v_code}"[:100]
        status = v.get("status", "ACTIVE")

        crop_code = None
        crop_name = None
        for r in v.get("relations") or []:
            if r.get("type") == "crop":
                crop_code = str(r.get("target_code"))
                crop_name = r.get("target_display_name")
                break

        sql = f"""INSERT INTO public.crop_varieties (
    variety_id, variety_code, variety_name, crop_code, crop_name, status, is_active
) VALUES (
    {sql_escape(v_id)}, {sql_escape(v_code[:100])}, {sql_escape(v_name)}, {sql_escape(crop_code)}, {sql_escape(crop_name)}, {sql_escape(status)}, TRUE
)
ON CONFLICT (variety_code) DO UPDATE SET
    variety_name = EXCLUDED.variety_name,
    crop_code = EXCLUDED.crop_code,
    crop_name = EXCLUDED.crop_name,
    status = EXCLUDED.status;"""
        sql_statements.append(sql)

    # =========================================================================
    # 5. LIVESTOCK TYPES (5 Species: Cattle, Sheep, Goat, Camel, Beehive)
    # =========================================================================
    lst_data = fetch_json("/v1/catalogues/livestock_type/values?page_size=50")
    lst_values = lst_data.get("values", [])
    print(f"Fetched {len(lst_values)} livestock types.")

    sql_statements.append("\n-- 5. LIVESTOCK TYPES (SPECIES)")
    for lt in lst_values:
        code = lt['code']
        name = lt['display_name']
        tid = f"lst-{code}"
        meta = lt.get("metadata") or {}
        sci_name = meta.get("scientific_name") or ""
        subfamily = meta.get("subfamily") or ""
        desc = meta.get("description") or f"Livestock type {name}"
        tag_range = meta.get("ear_tag_range") or ""
        species_code = meta.get("species_type_code")
        in_lis = meta.get("in_lis_population", True)
        in_etlits = meta.get("in_etlits_registry", True)
        status = lt.get("status", "ACTIVE")

        sql = f"""INSERT INTO public.livestock_types (
    type_id, type_code, type_name, scientific_name, subfamily, description,
    ear_tag_range, species_type_code, in_lis_population, in_etlits_registry, status, is_active
) VALUES (
    {sql_escape(tid)}, {sql_escape(code)}, {sql_escape(name)}, {sql_escape(sci_name)}, {sql_escape(subfamily)}, {sql_escape(desc)},
    {sql_escape(tag_range)}, {sql_escape(species_code)}, {sql_escape(in_lis)}, {sql_escape(in_etlits)}, {sql_escape(status)}, TRUE
)
ON CONFLICT (type_code) DO UPDATE SET
    type_name = EXCLUDED.type_name,
    scientific_name = EXCLUDED.scientific_name,
    subfamily = EXCLUDED.subfamily,
    description = EXCLUDED.description,
    ear_tag_range = EXCLUDED.ear_tag_range,
    species_type_code = EXCLUDED.species_type_code,
    in_lis_population = EXCLUDED.in_lis_population,
    in_etlits_registry = EXCLUDED.in_etlits_registry,
    status = EXCLUDED.status;"""
        sql_statements.append(sql)

    # =========================================================================
    # 6. LIVESTOCK BREEDS (94 Breeds into livestock_breeds & g2p_register_livestock_catalogs)
    # =========================================================================
    lbr_data = fetch_json("/v1/catalogues/livestock_breed/values?page_size=200")
    lbr_values = lbr_data.get("values", [])
    print(f"Fetched {len(lbr_values)} livestock breeds.")

    sql_statements.append("\n-- 6. LIVESTOCK BREEDS & MASTER REGISTER (94 BREEDS)")
    for lb in lbr_values:
        code = str(lb['code'])
        display_name = lb['display_name']
        meta = lb.get("metadata") or {}
        relations = lb.get("relations") or []

        species_code = None
        species_name = "Cattle"
        for r in relations:
            if r.get("type") == "species":
                species_code = r.get("target_code")
                species_name = r.get("target_display_name") or "Cattle"
                break

        breed_type = meta.get("breed_type") or "Indigenous"
        abbreviation = meta.get("abbreviation") or ""
        in_std = meta.get("in_national_standard", True)
        in_etlits = meta.get("in_etlits_registry", False)
        status = lb.get("status", "ACTIVE")
        desc = meta.get("description") or f"Standard {breed_type} {display_name} ({species_name}) breed in Ethiopia."

        # Purpose heuristic based on species and type
        purpose = "DUAL_PURPOSE"
        if species_name and "cattle" in species_name.lower():
            purpose = "DAIRY" if "holstein" in display_name.lower() or "jersey" in display_name.lower() else "DUAL_PURPOSE"
        elif species_name and "sheep" in species_name.lower():
            purpose = "MEAT"
        elif species_name and "goat" in species_name.lower():
            purpose = "MEAT"
        elif species_name and "beehive" in species_name.lower():
            purpose = "HONEY_POLLINATION"

        bid = f"lbr-{code}"
        b_sql = f"""INSERT INTO public.livestock_breeds (
    breed_id, breed_code, breed_name, species_code, species_name, breed_type,
    abbreviation, primary_purpose, origin_country, in_national_standard, in_etlits_registry,
    description, status, is_active
) VALUES (
    {sql_escape(bid)}, {sql_escape(code)}, {sql_escape(display_name)}, {sql_escape(species_code)}, {sql_escape(species_name)}, {sql_escape(breed_type)},
    {sql_escape(abbreviation)}, {sql_escape(purpose)}, 'Ethiopia', {sql_escape(in_std)}, {sql_escape(in_etlits)},
    {sql_escape(desc)}, {sql_escape(status)}, TRUE
)
ON CONFLICT (breed_code) DO UPDATE SET
    breed_name = EXCLUDED.breed_name,
    species_code = EXCLUDED.species_code,
    species_name = EXCLUDED.species_name,
    breed_type = EXCLUDED.breed_type,
    abbreviation = EXCLUDED.abbreviation,
    primary_purpose = EXCLUDED.primary_purpose,
    in_national_standard = EXCLUDED.in_national_standard,
    in_etlits_registry = EXCLUDED.in_etlits_registry,
    description = EXCLUDED.description,
    status = EXCLUDED.status;"""
        sql_statements.append(b_sql)

        reg_id = f"lstk-reg-{code}"
        search_text = f"{code} {display_name} {species_name} {breed_type} {abbreviation}".strip()
        reg_sql = f"""INSERT INTO public.g2p_register_livestock_catalogs (
    internal_record_id, record_name, breed_code, breed_name, species, breed_type,
    abbreviation, primary_purpose, origin_country, in_national_standard, in_etlits_registry,
    description, is_active, search_text, record_status
) VALUES (
    {sql_escape(reg_id)}, {sql_escape(display_name)}, {sql_escape(code)}, {sql_escape(display_name)}, {sql_escape(species_name.upper())}, {sql_escape(breed_type)},
    {sql_escape(abbreviation)}, {sql_escape(purpose)}, 'Ethiopia', {sql_escape(in_std)}, {sql_escape(in_etlits)},
    {sql_escape(desc)}, TRUE, {sql_escape(search_text)}, {sql_escape(status)}
)
ON CONFLICT (breed_code) DO UPDATE SET
    breed_name = EXCLUDED.breed_name,
    species = EXCLUDED.species,
    breed_type = EXCLUDED.breed_type,
    abbreviation = EXCLUDED.abbreviation,
    primary_purpose = EXCLUDED.primary_purpose,
    in_national_standard = EXCLUDED.in_national_standard,
    in_etlits_registry = EXCLUDED.in_etlits_registry,
    description = EXCLUDED.description,
    search_text = EXCLUDED.search_text,
    record_status = EXCLUDED.record_status;"""
        sql_statements.append(reg_sql)

    # =========================================================================
    # 7. SEED CROPS (129 Crops into seed_crops)
    # =========================================================================
    scrop_data = fetch_json("/v1/catalogues/seed_crop/values?page_size=200")
    scrop_values = scrop_data.get("values", [])
    print(f"Fetched {len(scrop_values)} seed crops.")

    sql_statements.append("\n-- 7. SEED CROPS (129 CROPS)")
    for sc in scrop_values:
        code = str(sc['code'])
        display_name = sc['display_name']
        meta = sc.get("metadata") or {}
        desc = meta.get("description") or f"Seed crop parent taxonomy for {display_name}"
        status = sc.get("status", "ACTIVE")
        scid = f"scrop-{code}"

        sc_sql = f"""INSERT INTO public.seed_crops (
    crop_id, crop_code, crop_name, description, status, is_active
) VALUES (
    {sql_escape(scid)}, {sql_escape(code)}, {sql_escape(display_name)}, {sql_escape(desc)}, {sql_escape(status)}, TRUE
)
ON CONFLICT (crop_code) DO UPDATE SET
    crop_name = EXCLUDED.crop_name,
    description = EXCLUDED.description,
    status = EXCLUDED.status;"""
        sql_statements.append(sc_sql)

    # =========================================================================
    # 8. SEED VARIETIES (Top 500 varieties into seed_varieties & g2p_register_seed_catalogs)
    # =========================================================================
    svar_data = fetch_json("/v1/catalogues/seed_variety/values?page_size=500")
    svar_values = svar_data.get("values", [])
    print(f"Fetched {len(svar_values)} seed varieties.")

    sql_statements.append("\n-- 8. SEED VARIETIES & MASTER REGISTER (500 VARIETIES)")
    for sv in svar_values:
        code = str(sv['code'])
        display_name = sv['display_name']
        meta = sv.get("metadata") or {}
        relations = sv.get("relations") or []

        parent_crop_code = None
        parent_crop_name = "General Crop"
        for r in relations:
            if r.get("type") == "seed_crop":
                parent_crop_code = str(r.get("target_code"))
                parent_crop_name = r.get("target_display_name") or "General Crop"
                break

        match_status = meta.get("match_status") or "RESOLVED"
        status = sv.get("status", "ACTIVE")
        desc = f"Registered Ethiopian seed variety '{display_name}' derived from {parent_crop_name}."

        svid = f"svar-{code}"[:100]
        svar_sql = f"""INSERT INTO public.seed_varieties (
    variety_id, variety_code, variety_name, seed_crop_code, seed_crop_name,
    match_status, description, is_certified, status, is_active
) VALUES (
    {sql_escape(svid)}, {sql_escape(code[:100])}, {sql_escape(display_name)}, {sql_escape(parent_crop_code)}, {sql_escape(parent_crop_name)},
    {sql_escape(match_status)}, {sql_escape(desc)}, TRUE, {sql_escape(status)}, TRUE
)
ON CONFLICT (variety_code) DO UPDATE SET
    variety_name = EXCLUDED.variety_name,
    seed_crop_code = EXCLUDED.seed_crop_code,
    seed_crop_name = EXCLUDED.seed_crop_name,
    match_status = EXCLUDED.match_status,
    description = EXCLUDED.description,
    status = EXCLUDED.status;"""
        sql_statements.append(svar_sql)

        reg_seed_id = f"seed-reg-{code}"[:100]
        search_text = f"{code} {display_name} {parent_crop_name}".strip()
        reg_seed_sql = f"""INSERT INTO public.g2p_register_seed_catalogs (
    internal_record_id, record_name, seed_code, variety_name, crop_name, crop_code,
    match_status, is_certified, is_active, search_text, record_status
) VALUES (
    {sql_escape(reg_seed_id)}, {sql_escape(display_name)}, {sql_escape(code[:50])}, {sql_escape(display_name)}, {sql_escape(parent_crop_name)}, {sql_escape(parent_crop_code)},
    {sql_escape(match_status)}, TRUE, TRUE, {sql_escape(search_text)}, {sql_escape(status)}
)
ON CONFLICT (seed_code) DO UPDATE SET
    variety_name = EXCLUDED.variety_name,
    crop_name = EXCLUDED.crop_name,
    crop_code = EXCLUDED.crop_code,
    match_status = EXCLUDED.match_status,
    search_text = EXCLUDED.search_text,
    record_status = EXCLUDED.record_status;"""
        sql_statements.append(reg_seed_sql)

    # Write output SQL file
    output_path = Path(__file__).resolve().parent / "seed_reference_catalogs.sql"
    full_sql = "\n".join(sql_statements) + "\n"
    output_path.write_text(full_sql, encoding="utf-8")
    print(f"Generated SQL seed file: {output_path} ({len(sql_statements)} statements, {len(full_sql)} bytes)")

    # Execute against Postgres container
    print(f"Applying generated SQL to PostgreSQL container '{DB_CONTAINER}'...")
    p = subprocess.Popen(
        ["docker", "exec", "-i", DB_CONTAINER, "psql", "-U", DB_USER, "-d", DB_NAME],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(input=full_sql.encode("utf-8"))
    if p.returncode != 0:
        print(f"Error applying SQL: {stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    print("Database sync completed successfully!")


if __name__ == "__main__":
    sync_all()
