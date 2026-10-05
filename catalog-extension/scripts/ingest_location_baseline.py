#!/usr/bin/env python3
"""
Baseline Geolocation Ingestion Script
Ingests 21,053 Ethiopian administrative units from farmer_master_data_db into catalog_registry_db:
  - geo_regions (14)
  - geo_zones (125)
  - geo_woredas (1,379)
  - geo_kebeles (19,535)
  - g2p_register_location_catalogs (21,053)
  - g2p_register_history_location_catalogs (21,053)
"""

import argparse
import os
import sys
import time
import psycopg2
from psycopg2.extras import execute_batch

def get_db_configs():
    parser = argparse.ArgumentParser(description="Ingest 21,053 Ethiopian admin units from master data into catalog registry.")
    parser.add_argument("--src-host", default=os.environ.get("MASTER_DATA_DB_HOSTNAME") or os.environ.get("COMMON_DB_HOSTNAME") or "farmer-registry-postgres")
    parser.add_argument("--src-port", type=int, default=int(os.environ.get("MASTER_DATA_DB_PORT") or os.environ.get("COMMON_DB_PORT") or 5432))
    parser.add_argument("--src-user", default=os.environ.get("MASTER_DATA_DB_USERNAME") or os.environ.get("COMMON_DB_USERNAME") or "postgres")
    parser.add_argument("--src-pass", default=os.environ.get("MASTER_DATA_DB_PASSWORD") or os.environ.get("COMMON_DB_PASSWORD") or "postgres")
    parser.add_argument("--src-db", default=os.environ.get("MASTER_DATA_DB_DBNAME") or "farmer_master_data_db")

    parser.add_argument("--tgt-host", default=os.environ.get("REGISTRY_EXTENSIONS_DB_HOSTNAME") or os.environ.get("COMMON_DB_HOSTNAME") or "farmer-registry-postgres")
    parser.add_argument("--tgt-port", type=int, default=int(os.environ.get("REGISTRY_EXTENSIONS_DB_PORT") or os.environ.get("COMMON_DB_PORT") or 5432))
    parser.add_argument("--tgt-user", default=os.environ.get("REGISTRY_EXTENSIONS_DB_USERNAME") or os.environ.get("COMMON_DB_USERNAME") or "postgres")
    parser.add_argument("--tgt-pass", default=os.environ.get("REGISTRY_EXTENSIONS_DB_PASSWORD") or os.environ.get("COMMON_DB_PASSWORD") or "postgres")
    parser.add_argument("--tgt-db", default=os.environ.get("REGISTRY_EXTENSIONS_DB_DBNAME") or os.environ.get("COMMON_DB_DBNAME") or "catalog_registry_db")

    args, _ = parser.parse_known_args()
    return args

def main():
    args = get_db_configs()
    print("=" * 70)
    print("STARTING GEOLOCATION BASELINE INGESTION (21,053 UNITS)")
    print("=" * 70)
    print(f"Source DB: {args.src_user}@{args.src_host}:{args.src_port}/{args.src_db}")
    print(f"Target DB: {args.tgt_user}@{args.tgt_host}:{args.tgt_port}/{args.tgt_db}")

    start_time = time.time()

    # 1. Connect to both databases
    print("Connecting to source and target databases...")
    src_conn = psycopg2.connect(
        host=args.src_host, port=args.src_port, user=args.src_user, password=args.src_pass, dbname=args.src_db
    )
    src_cur = src_conn.cursor()

    tgt_conn = psycopg2.connect(
        host=args.tgt_host, port=args.tgt_port, user=args.tgt_user, password=args.tgt_pass, dbname=args.tgt_db
    )
    tgt_cur = tgt_conn.cursor()

    # 2. Fetch all geo records from farmer_master_data_db
    print("Fetching geo records from farmer_master_data_db...")
    src_cur.execute("""
        SELECT level_value_id, level_id, level_value_mnemonic, parent_level_value_id, pcode, name
        FROM g2p_geo_level_values
        ORDER BY level_id, level_value_id;
    """)
    all_rows = src_cur.fetchall()
    print(f"Total rows retrieved from master data: {len(all_rows)}")

    # Index by level_id and level_value_id
    records_by_id = {}
    regions_raw = []
    zones_raw = []
    woredas_raw = []
    kebeles_raw = []

    for row in all_rows:
        rec = {
            "level_value_id": row[0],
            "level_id": row[1],
            "mnemonic": row[2],
            "parent_id": row[3],
            "pcode": row[4],
            "name": row[5] or row[2] or row[0],
        }
        records_by_id[rec["level_value_id"]] = rec
        if rec["level_id"] == "level-region":
            regions_raw.append(rec)
        elif rec["level_id"] == "level-zone":
            zones_raw.append(rec)
        elif rec["level_id"] == "level-woreda":
            woredas_raw.append(rec)
        elif rec["level_id"] == "level-kebele":
            kebeles_raw.append(rec)

    print(f"Counts: Regions={len(regions_raw)}, Zones={len(zones_raw)}, Woredas={len(woredas_raw)}, Kebeles={len(kebeles_raw)}")

    # Precompute child counts
    woredas_per_zone = {}
    kebeles_per_woreda = {}
    zones_per_region = {}
    woredas_per_region = {}
    kebeles_per_region = {}

    for k in kebeles_raw:
        w_id = k["parent_id"]
        kebeles_per_woreda[w_id] = kebeles_per_woreda.get(w_id, 0) + 1

    for w in woredas_raw:
        z_id = w["parent_id"]
        if z_id:
            woredas_per_zone[z_id] = woredas_per_zone.get(z_id, 0) + 1

    # Map zones to regions
    for z in zones_raw:
        r_id = z["parent_id"]
        if r_id:
            zones_per_region[r_id] = zones_per_region.get(r_id, 0) + 1

    for w in woredas_raw:
        z_id = w["parent_id"]
        r_id = None
        if z_id and z_id in records_by_id:
            r_id = records_by_id[z_id]["parent_id"]
        elif not z_id:
            # Special woreda
            # e.g. woreda-ET070001 -> region-ET07
            pcode = w["pcode"] or ""
            if len(pcode) >= 4:
                r_id = f"region-{pcode[:4]}"
        if r_id:
            woredas_per_region[r_id] = woredas_per_region.get(r_id, 0) + 1
            keb_count = kebeles_per_woreda.get(w["level_value_id"], 0)
            kebeles_per_region[r_id] = kebeles_per_region.get(r_id, 0) + keb_count

    # 3. Build data for geo_regions
    print("Preparing geo_regions data...")
    geo_regions_data = []
    for r in regions_raw:
        r_id = r["level_value_id"]
        pcode = r["pcode"] or r_id.replace("region-", "")
        name = r["name"]
        geo_regions_data.append((
            r_id, pcode, name, pcode, None, None,
            zones_per_region.get(r_id, 0),
            woredas_per_region.get(r_id, 0),
            kebeles_per_region.get(r_id, 0),
            f"Regional State of {name}, Federal Democratic Republic of Ethiopia",
            "ACTIVE", True
        ))

    # 4. Build data for geo_zones
    print("Preparing geo_zones data...")
    geo_zones_data = []
    kebeles_per_zone = {}
    for w in woredas_raw:
        z_id = w["parent_id"]
        if z_id:
            kebeles_per_zone[z_id] = kebeles_per_zone.get(z_id, 0) + kebeles_per_woreda.get(w["level_value_id"], 0)

    for z in zones_raw:
        z_id = z["level_value_id"]
        pcode = z["pcode"] or z_id.replace("zone-", "")
        name = z["name"]
        parent_r = records_by_id.get(z["parent_id"])
        r_code = parent_r["pcode"] if parent_r else ""
        r_name = parent_r["name"] if parent_r else ""
        geo_zones_data.append((
            z_id, pcode, name, pcode, r_code, r_name, None, None,
            woredas_per_zone.get(z_id, 0),
            kebeles_per_zone.get(z_id, 0),
            f"Zone {name} in {r_name} Region",
            "ACTIVE", True
        ))

    # 5. Build data for geo_woredas
    print("Preparing geo_woredas data...")
    geo_woredas_data = []
    woreda_lookup = {}  # woreda_id -> {woreda_code, woreda_name, zone_code, zone_name, region_code, region_name}

    for w in woredas_raw:
        w_id = w["level_value_id"]
        pcode = w["pcode"] or w_id.replace("woreda-", "")
        name = w["name"]
        z_rec = records_by_id.get(w["parent_id"])
        if z_rec:
            z_code = z_rec["pcode"]
            z_name = z_rec["name"]
            r_rec = records_by_id.get(z_rec["parent_id"])
            r_code = r_rec["pcode"] if r_rec else ""
            r_name = r_rec["name"] if r_rec else ""
        else:
            # Special woreda reporting directly to region
            z_code = None
            z_name = None
            # e.g. ET070001 -> ET07
            reg_code = pcode[:4] if len(pcode) >= 4 else "ET07"
            r_rec = records_by_id.get(f"region-{reg_code}")
            r_code = r_rec["pcode"] if r_rec else reg_code
            r_name = r_rec["name"] if r_rec else "Central Ethiopia"

        woreda_lookup[w_id] = {
            "woreda_code": pcode,
            "woreda_name": name,
            "zone_code": z_code,
            "zone_name": z_name,
            "region_code": r_code,
            "region_name": r_name,
        }

        geo_woredas_data.append((
            w_id, pcode, name, pcode, z_code, z_name, r_code, r_name,
            kebeles_per_woreda.get(w_id, 0),
            f"Woreda (District) {name}, {z_name or 'Special Woreda'}, {r_name}",
            "ACTIVE", True
        ))

    # 6. Build data for geo_kebeles
    print("Preparing geo_kebeles data...")
    geo_kebeles_data = []
    for k in kebeles_raw:
        k_id = k["level_value_id"]
        k_code = k_id.replace("kebele-", "")
        name = k["name"]
        w_info = woreda_lookup.get(k["parent_id"], {})
        w_code = w_info.get("woreda_code", "")
        w_name = w_info.get("woreda_name", "")
        z_code = w_info.get("zone_code")
        z_name = w_info.get("zone_name")
        r_code = w_info.get("region_code", "")
        r_name = w_info.get("region_name", "")

        geo_kebeles_data.append((
            k_id, k_code, name, k_code, w_code, w_name, z_code, z_name, r_code, r_name,
            f"Kebele {name} in {w_name} Woreda",
            "ACTIVE", True
        ))

    # 7. Build data for g2p_register_location_catalogs & history (all 21,053 units)
    print("Preparing g2p_register_location_catalogs data (21,053 records)...")
    register_data = []
    history_data = []

    TAB_ID = "c1000000-0000-4000-a000-000000000005"
    SEC_ID = "c1000000-0000-4000-b000-000000000005"

    # 7a. Regions (14)
    for r in regions_raw:
        pcode = r["pcode"] or r["level_value_id"].replace("region-", "")
        name = r["name"]
        internal_id = f"loc-reg-{pcode}"
        func_id = f"LOC-REG-{pcode}"
        rec_name = f"{name} (Region)"
        search_txt = f"{name} {pcode} REGION Ethiopia"

        # Register record tuple
        register_data.append((
            internal_id, func_id, rec_name, "SYSTEM", "ACTIVE", search_txt,
            pcode, name, "REGION", "1", "ET", "Ethiopia", None, None, pcode,
            f"Regional State of {name}", True, name, None, None, None, "ET"
        ))

        # History record tuple
        history_data.append((
            f"hist-{internal_id}", internal_id, TAB_ID, SEC_ID, "BASELINE", True,
            func_id, rec_name, "ACTIVE", "SYSTEM", "SYSTEM",
            pcode, name, "REGION", "1", "ET", "Ethiopia", None, None, pcode,
            f"Regional State of {name}", True, name, None, None, None, "ET"
        ))

    # 7b. Zones (125)
    for z in zones_raw:
        pcode = z["pcode"] or z["level_value_id"].replace("zone-", "")
        name = z["name"]
        parent_r = records_by_id.get(z["parent_id"])
        r_code = parent_r["pcode"] if parent_r else ""
        r_name = parent_r["name"] if parent_r else ""

        internal_id = f"loc-zone-{pcode}"
        func_id = f"LOC-ZONE-{pcode}"
        rec_name = f"{name} (Zone)"
        search_txt = f"{name} {pcode} ZONE {r_name}"

        register_data.append((
            internal_id, func_id, rec_name, "SYSTEM", "ACTIVE", search_txt,
            pcode, name, "ZONE", "2", r_code, r_name, None, None, pcode,
            f"Zone {name} in {r_name} Region", True, r_name, name, None, None, "ET"
        ))

        history_data.append((
            f"hist-{internal_id}", internal_id, TAB_ID, SEC_ID, "BASELINE", True,
            func_id, rec_name, "ACTIVE", "SYSTEM", "SYSTEM",
            pcode, name, "ZONE", "2", r_code, r_name, None, None, pcode,
            f"Zone {name} in {r_name} Region", True, r_name, name, None, None, "ET"
        ))

    # 7c. Woredas (1,379)
    for w in woredas_raw:
        w_id = w["level_value_id"]
        pcode = w["pcode"] or w_id.replace("woreda-", "")
        name = w["name"]
        w_info = woreda_lookup[w_id]
        r_code = w_info["region_code"]
        r_name = w_info["region_name"]
        z_code = w_info["zone_code"]
        z_name = w_info["zone_name"]

        parent_code = z_code if z_code else r_code
        parent_name = z_name if z_name else r_name

        internal_id = f"loc-wor-{pcode}"
        func_id = f"LOC-WOR-{pcode}"
        rec_name = f"{name} (Woreda)"
        search_txt = f"{name} {pcode} WOREDA {z_name or 'Special'} {r_name}"

        register_data.append((
            internal_id, func_id, rec_name, "SYSTEM", "ACTIVE", search_txt,
            pcode, name, "WOREDA", "3", parent_code, parent_name, None, None, pcode,
            f"Woreda {name}, {z_name or 'Special Woreda'}, {r_name}", True,
            r_name, z_name, name, None, "ET"
        ))

        history_data.append((
            f"hist-{internal_id}", internal_id, TAB_ID, SEC_ID, "BASELINE", True,
            func_id, rec_name, "ACTIVE", "SYSTEM", "SYSTEM",
            pcode, name, "WOREDA", "3", parent_code, parent_name, None, None, pcode,
            f"Woreda {name}, {z_name or 'Special Woreda'}, {r_name}", True,
            r_name, z_name, name, None, "ET"
        ))

    # 7d. Kebeles (19,535)
    for k in kebeles_raw:
        k_id = k["level_value_id"]
        k_code = k_id.replace("kebele-", "")
        name = k["name"]
        w_info = woreda_lookup.get(k["parent_id"], {})
        w_code = w_info.get("woreda_code", "")
        w_name = w_info.get("woreda_name", "")
        z_name = w_info.get("zone_name")
        r_name = w_info.get("region_name", "")

        internal_id = f"loc-keb-{k_code}"
        func_id = f"LOC-KEB-{k_code}"
        rec_name = f"{name} (Kebele)"
        search_txt = f"{name} {k_code} KEBELE {w_name} {r_name}"

        register_data.append((
            internal_id, func_id, rec_name, "SYSTEM", "ACTIVE", search_txt,
            k_code, name, "KEBELE", "4", w_code, w_name, None, None, k_code,
            f"Kebele {name} in {w_name} Woreda", True,
            r_name, z_name, w_name, name, "ET"
        ))

        history_data.append((
            f"hist-{internal_id}", internal_id, TAB_ID, SEC_ID, "BASELINE", True,
            func_id, rec_name, "ACTIVE", "SYSTEM", "SYSTEM",
            k_code, name, "KEBELE", "4", w_code, w_name, None, None, k_code,
            f"Kebele {name} in {w_name} Woreda", True,
            r_name, z_name, w_name, name, "ET"
        ))

    # 8. Insert into catalog_registry_db using execute_batch
    print("\nExecuting batch inserts into catalog_registry_db...")

    # 8a. geo_regions
    print(f"Inserting {len(geo_regions_data)} rows into geo_regions...")
    execute_batch(tgt_cur, """
        INSERT INTO public.geo_regions (
            region_id, region_code, region_name, pcode, capital, area_sq_km,
            zones_count, woredas_count, kebeles_count, description, status, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (region_code) DO UPDATE SET
            region_name = EXCLUDED.region_name,
            pcode = EXCLUDED.pcode,
            zones_count = EXCLUDED.zones_count,
            woredas_count = EXCLUDED.woredas_count,
            kebeles_count = EXCLUDED.kebeles_count,
            description = EXCLUDED.description,
            status = EXCLUDED.status,
            is_active = EXCLUDED.is_active;
    """, geo_regions_data, page_size=1000)

    # 8b. geo_zones
    print(f"Inserting {len(geo_zones_data)} rows into geo_zones...")
    execute_batch(tgt_cur, """
        INSERT INTO public.geo_zones (
            zone_id, zone_code, zone_name, pcode, region_code, region_name,
            capital, area_sq_km, woredas_count, kebeles_count, description, status, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (zone_code) DO UPDATE SET
            zone_name = EXCLUDED.zone_name,
            pcode = EXCLUDED.pcode,
            region_code = EXCLUDED.region_code,
            region_name = EXCLUDED.region_name,
            woredas_count = EXCLUDED.woredas_count,
            kebeles_count = EXCLUDED.kebeles_count,
            description = EXCLUDED.description,
            status = EXCLUDED.status,
            is_active = EXCLUDED.is_active;
    """, geo_zones_data, page_size=1000)

    # 8c. geo_woredas
    print(f"Inserting {len(geo_woredas_data)} rows into geo_woredas...")
    execute_batch(tgt_cur, """
        INSERT INTO public.geo_woredas (
            woreda_id, woreda_code, woreda_name, pcode, zone_code, zone_name,
            region_code, region_name, kebeles_count, description, status, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (woreda_code) DO UPDATE SET
            woreda_name = EXCLUDED.woreda_name,
            pcode = EXCLUDED.pcode,
            zone_code = EXCLUDED.zone_code,
            zone_name = EXCLUDED.zone_name,
            region_code = EXCLUDED.region_code,
            region_name = EXCLUDED.region_name,
            kebeles_count = EXCLUDED.kebeles_count,
            description = EXCLUDED.description,
            status = EXCLUDED.status,
            is_active = EXCLUDED.is_active;
    """, geo_woredas_data, page_size=1000)

    # 8d. geo_kebeles
    print(f"Inserting {len(geo_kebeles_data)} rows into geo_kebeles...")
    execute_batch(tgt_cur, """
        INSERT INTO public.geo_kebeles (
            kebele_id, kebele_code, kebele_name, pcode, woreda_code, woreda_name,
            zone_code, zone_name, region_code, region_name, description, status, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (kebele_code) DO UPDATE SET
            kebele_name = EXCLUDED.kebele_name,
            pcode = EXCLUDED.pcode,
            woreda_code = EXCLUDED.woreda_code,
            woreda_name = EXCLUDED.woreda_name,
            zone_code = EXCLUDED.zone_code,
            zone_name = EXCLUDED.zone_name,
            region_code = EXCLUDED.region_code,
            region_name = EXCLUDED.region_name,
            description = EXCLUDED.description,
            status = EXCLUDED.status,
            is_active = EXCLUDED.is_active;
    """, geo_kebeles_data, page_size=2000)

    tgt_conn.commit()
    print("Sub-category tables committed successfully.")

    # 8e. g2p_register_location_catalogs
    print(f"Inserting {len(register_data)} rows into g2p_register_location_catalogs...")
    execute_batch(tgt_cur, """
        INSERT INTO public.g2p_register_location_catalogs (
            internal_record_id, functional_record_id, record_name, created_by,
            record_status, search_text, location_code, location_name, admin_level,
            admin_level_code, parent_location_code, parent_location_name,
            area_sq_km, population_estimate, pcode, description, is_active,
            region_name, zone_name, woreda_name, kebele_name, country_code,
            last_approved_by, last_approved_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, 'SYSTEM', now() at time zone 'utc'
        )
        ON CONFLICT (location_code) DO UPDATE SET
            functional_record_id = EXCLUDED.functional_record_id,
            record_name = EXCLUDED.record_name,
            record_status = EXCLUDED.record_status,
            search_text = EXCLUDED.search_text,
            location_name = EXCLUDED.location_name,
            admin_level = EXCLUDED.admin_level,
            admin_level_code = EXCLUDED.admin_level_code,
            parent_location_code = EXCLUDED.parent_location_code,
            parent_location_name = EXCLUDED.parent_location_name,
            pcode = EXCLUDED.pcode,
            description = EXCLUDED.description,
            is_active = EXCLUDED.is_active,
            region_name = EXCLUDED.region_name,
            zone_name = EXCLUDED.zone_name,
            woreda_name = EXCLUDED.woreda_name,
            kebele_name = EXCLUDED.kebele_name,
            country_code = EXCLUDED.country_code;
    """, register_data, page_size=2000)

    # 8f. g2p_register_history_location_catalogs
    print(f"Inserting {len(history_data)} rows into g2p_register_history_location_catalogs...")
    execute_batch(tgt_cur, """
        INSERT INTO public.g2p_register_history_location_catalogs (
            history_record_id, internal_record_id, tab_id, section_id,
            change_request_source, is_primary_section, functional_record_id,
            record_name, record_status, created_by, created_at, approved_by, approved_at,
            location_code, location_name, admin_level, admin_level_code,
            parent_location_code, parent_location_name, area_sq_km, population_estimate,
            pcode, description, is_active, region_name, zone_name, woreda_name,
            kebele_name, country_code
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now() at time zone 'utc', %s, now() at time zone 'utc',
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (history_record_id) DO NOTHING;
    """, history_data, page_size=2000)

    tgt_conn.commit()
    print("Main register and history tables committed successfully.")

    # 9. Verify counts
    print("\n" + "=" * 50)
    print("VERIFICATION OF INGESTION COUNTS")
    print("=" * 50)

    tgt_cur.execute("SELECT count(*) FROM geo_regions;")
    print(f"geo_regions:                           {tgt_cur.fetchone()[0]}")

    tgt_cur.execute("SELECT count(*) FROM geo_zones;")
    print(f"geo_zones:                             {tgt_cur.fetchone()[0]}")

    tgt_cur.execute("SELECT count(*) FROM geo_woredas;")
    print(f"geo_woredas:                           {tgt_cur.fetchone()[0]}")

    tgt_cur.execute("SELECT count(*) FROM geo_kebeles;")
    print(f"geo_kebeles:                           {tgt_cur.fetchone()[0]}")

    tgt_cur.execute("SELECT count(*) FROM g2p_register_location_catalogs;")
    print(f"g2p_register_location_catalogs:        {tgt_cur.fetchone()[0]}")

    tgt_cur.execute("SELECT count(*) FROM g2p_register_history_location_catalogs;")
    print(f"g2p_register_history_location_catalogs:{tgt_cur.fetchone()[0]}")

    tgt_cur.execute("""
        SELECT admin_level, count(*) 
        FROM g2p_register_location_catalogs 
        GROUP BY admin_level 
        ORDER BY count(*) ASC;
    """)
    for row in tgt_cur.fetchall():
        print(f"  - Admin Level {row[0]:<10}: {row[1]} records")

    tgt_cur.close()
    tgt_conn.close()
    src_cur.close()
    src_conn.close()

    elapsed = time.time() - start_time
    print(f"\nCOMPLETED INGESTION IN {elapsed:.2f} SECONDS!")

if __name__ == "__main__":
    main()
