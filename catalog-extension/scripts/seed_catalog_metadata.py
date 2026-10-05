#!/usr/bin/env python3
"""OpenG2P Catalog Extension - Metadata Seeder
Executes the SQL files under meta_data/register-metadata/ against the active registry database.
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError:
    psycopg2 = None

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = BASE_DIR / "src" / "openg2p_registry_catalog_extension" / "meta_data" / "register-metadata"

SQL_FILES = [
    ("register-metadata", "g2p_register_definitions.sql"),
    ("register-metadata", "g2p_register_schemas.sql"),
    ("register-metadata", "g2p_register_sections.sql"),
    ("register-metadata", "g2p_register_ui_tabs.sql"),
    ("register-metadata", "g2p_register_ui_tab_sections.sql"),
    ("register-metadata", "g2p_intake_form_definitions.sql"),
    ("register-metadata", "g2p_intake_form_ui_tabs.sql"),
    ("register-metadata", "g2p_intake_form_ui_tab_sections.sql"),
    ("registry-configurations", "registry_themes.sql"),
    ("registry-configurations", "registry_themes_values.sql"),
    ("registry-configurations", "registry_languages.sql"),
    ("registry-configurations", "g2p_registry_configuration.sql"),
]


def seed_metadata():
    db_host = os.getenv("PGHOST", "localhost")
    db_port = os.getenv("PGPORT", "5432")
    db_name = os.getenv("PGDATABASE", "catalog_registry_db")
    db_user = os.getenv("PGUSER", "postgres")
    db_pass = os.getenv("PGPASSWORD", "postgres")

    print(f"Connecting to PostgreSQL database '{db_name}' on {db_host}:{db_port}...")
    try:
        if psycopg2:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_pass,
            )
            conn.autocommit = True
            cursor = conn.cursor()

            for subdir, filename in SQL_FILES:
                filepath = BASE_DIR / "src" / "openg2p_registry_catalog_extension" / "meta_data" / subdir / filename
                if not filepath.exists():
                    print(f"Warning: File not found: {filepath}")
                    continue

                print(f"Applying {filename} from {subdir}...")
                sql_content = filepath.read_text(encoding="utf-8")
                cursor.execute(sql_content)
                print(f"Successfully applied {filename}")

            cursor.close()
            conn.close()
        else:
            # Fallback to docker exec or psql
            print("psycopg2 not found, using docker / psql fallback...")
            docker_container = os.getenv("PGCONTAINER", "farmer-registry-postgres")
            for subdir, filename in SQL_FILES:
                filepath = BASE_DIR / "src" / "openg2p_registry_catalog_extension" / "meta_data" / subdir / filename
                if not filepath.exists():
                    print(f"Warning: File not found: {filepath}")
                    continue

                print(f"Applying {filename} from {subdir}...")
                with open(filepath, "rb") as f:
                    cmd = ["docker", "exec", "-i", docker_container, "psql", "-U", db_user, "-d", db_name]
                    res = subprocess.run(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if res.returncode != 0:
                        raise RuntimeError(f"Error applying {filename}: {res.stderr.decode('utf-8')}")
                print(f"Successfully applied {filename}")

        print("\nAll catalog metadata seeded successfully!")
    except Exception as e:
        print(f"\nError seeding metadata: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    seed_metadata()
