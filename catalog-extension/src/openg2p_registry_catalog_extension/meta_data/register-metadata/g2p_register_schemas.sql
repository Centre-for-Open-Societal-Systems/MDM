INSERT INTO "public"."g2p_register_schemas" ("register_id", "deduplicate_schema", "search_result_schema", "filter_schema") VALUES 
-- 1. Crop Catalog
(
    'c1000000-0000-4000-8000-000000000001',
    '[]',
    '[
        {"field_name": "Crop Code", "display_label": "Crop Code", "order": 1},
        {"field_name": "Crop Name", "display_label": "Crop Name", "order": 2},
        {"field_name": "Scientific Name", "display_label": "Scientific Name", "order": 3},
        {"field_name": "Category", "display_label": "Category", "order": 4},
        {"field_name": "Ecological Zone", "display_label": "Ecological Zone", "order": 5},
        {"field_name": "Research Centre", "display_label": "Research Centre", "order": 6},
        {"field_name": "Varieties", "display_label": "Varieties", "order": 7},
        {"field_name": "Active Status", "display_label": "Active Status", "order": 8}
    ]',
    '[
        {"field_name": "crop_name", "display_label": "Crop Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]},
        {"field_name": "crop_category", "display_label": "Category", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]},
        {"field_name": "is_active", "display_label": "Is Active", "filter_type": "boolean", "order": 3, "allowed_operators": ["eq"]}
    ]'
),
-- 2. Seed Catalog
(
    'c1000000-0000-4000-8000-000000000002',
    '[]',
    '[
        {"field_name": "Seed Code", "display_label": "Seed Code", "order": 1},
        {"field_name": "Variety Name", "display_label": "Variety Name", "order": 2},
        {"field_name": "Parent Crop", "display_label": "Parent Crop", "order": 3},
        {"field_name": "Breeder / Source", "display_label": "Breeder / Source", "order": 4},
        {"field_name": "Release Year", "display_label": "Release Year", "order": 5},
        {"field_name": "Match Status", "display_label": "Match Status", "order": 6},
        {"field_name": "Maturity (Days)", "display_label": "Maturity (Days)", "order": 7},
        {"field_name": "Potential Yield", "display_label": "Potential Yield", "order": 8},
        {"field_name": "Certified", "display_label": "Certified", "order": 9},
        {"field_name": "Active Status", "display_label": "Active Status", "order": 10}
    ]',
    '[
        {"field_name": "variety_name", "display_label": "Variety Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]},
        {"field_name": "crop_name", "display_label": "Crop", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]},
        {"field_name": "is_certified", "display_label": "Certified", "filter_type": "boolean", "order": 3, "allowed_operators": ["eq"]}
    ]'
),
-- 3. Inputs Catalog (Agri-Inputs)
(
    'c1000000-0000-4000-8000-000000000003',
    '[]',
    '[
        {"field_name": "Input Code", "display_label": "Input Code", "order": 1},
        {"field_name": "Trade Name", "display_label": "Trade Name", "order": 2},
        {"field_name": "Category", "display_label": "Category", "order": 3},
        {"field_name": "Composition", "display_label": "Composition", "order": 4},
        {"field_name": "Manufacturer", "display_label": "Manufacturer", "order": 5},
        {"field_name": "Application Method", "display_label": "Application Method", "order": 6},
        {"field_name": "Recommended Crops", "display_label": "Recommended Crops", "order": 7},
        {"field_name": "Dosage", "display_label": "Dosage", "order": 8},
        {"field_name": "Active Status", "display_label": "Active Status", "order": 9}
    ]',
    '[
        {"field_name": "trade_name", "display_label": "Trade Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]},
        {"field_name": "input_category", "display_label": "Category", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]},
        {"field_name": "manufacturer", "display_label": "Manufacturer", "filter_type": "text", "order": 3, "allowed_operators": ["eq", "contains"]},
        {"field_name": "is_active", "display_label": "Is Active", "filter_type": "boolean", "order": 4, "allowed_operators": ["eq"]}
    ]'
),
-- 4. Livestock Catalog
(
    'c1000000-0000-4000-8000-000000000004',
    '[]',
    '[
        {"field_name": "Breed Code", "display_label": "Breed Code", "order": 1},
        {"field_name": "Breed Name", "display_label": "Breed Name", "order": 2},
        {"field_name": "Species", "display_label": "Species", "order": 3},
        {"field_name": "Breed Type", "display_label": "Breed Type", "order": 4},
        {"field_name": "Abbreviation", "display_label": "Abbreviation", "order": 5},
        {"field_name": "Primary Purpose", "display_label": "Primary Purpose", "order": 6},
        {"field_name": "National Standard", "display_label": "National Standard", "order": 7},
        {"field_name": "ET-LITS", "display_label": "ET-LITS", "order": 8},
        {"field_name": "Active Status", "display_label": "Active Status", "order": 9}
    ]',
    '[
        {"field_name": "breed_name", "display_label": "Breed Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]},
        {"field_name": "species", "display_label": "Species", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}
    ]'
),
-- 5. Location Catalog
(
    'c1000000-0000-4000-8000-000000000005',
    '[]',
    '[
        {"field_name": "Location Code", "display_label": "Location Code", "order": 1},
        {"field_name": "Location Name", "display_label": "Location Name", "order": 2},
        {"field_name": "Admin Level", "display_label": "Level", "order": 3},
        {"field_name": "Parent Location", "display_label": "Parent Location", "order": 4},
        {"field_name": "Capital City", "display_label": "Capital / Center", "order": 5},
        {"field_name": "Area (sq km)", "display_label": "Area (sq km)", "order": 6},
        {"field_name": "Active Status", "display_label": "Active Status", "order": 7}
    ]',
    '[
        {"field_name": "location_name", "display_label": "Location Name", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]},
        {"field_name": "admin_level", "display_label": "Admin Level", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]},
        {"field_name": "parent_location_name", "display_label": "Parent Location", "filter_type": "text", "order": 3, "allowed_operators": ["eq", "contains"]},
        {"field_name": "is_active", "display_label": "Is Active", "filter_type": "boolean", "order": 4, "allowed_operators": ["eq"]}
    ]'
)
ON CONFLICT ("register_id") DO UPDATE 
SET "search_result_schema" = EXCLUDED."search_result_schema",
    "filter_schema" = EXCLUDED."filter_schema";
