INSERT INTO "public"."g2p_register_sections" (
    "register_id",
    "section_id",
    "section_register_id",
    "is_core_section",
    "section_mnemonic",
    "section_description",
    "documents_required",
    "no_of_verifications_required",
    "is_list",
    "section_weightage",
    "section_ui_schema",
    "cr_auto_approve_for_bene_portal",
    "cr_auto_approve_for_agent_portal",
    "cr_auto_approve_for_staff_portal",
    "cr_auto_approve_for_partner"
) VALUES 
-- 1. Crop Catalog Form Section
(
    'c1000000-0000-4000-8000-000000000001',
    'crop_catalog_details_section',
    'c1000000-0000-4000-8000-000000000001',
    'FALSE',
    'crop_catalog_details',
    'Crop Catalog Basic Information',
    'FALSE',
    0,
    'FALSE',
    10,
    '{
        "section-id": "crop_catalog_details",
        "section-title": "Crop Information",
        "section-editable": true,
        "panels": [
            {
                "panel-id": "crop_main_panel",
                "panel-orientation": "horizontal",
                "panels": [
                    {
                        "panel-id": "crop_col_1",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "crop_code", "widget-type": "input", "widget-label": "Crop Code", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000001.crop_code"},
                            {"widget": "text", "widget-id": "crop_name", "widget-type": "input", "widget-label": "Crop Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000001.crop_name"},
                            {"widget": "text", "widget-id": "scientific_name", "widget-type": "input", "widget-label": "Scientific Name", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.scientific_name"},
                            {"widget": "select", "widget-id": "crop_category", "widget-type": "input", "widget-label": "Crop Category", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.crop_category", "widget-data-source": {"type": "static", "options": [{"label": "Cereal Crops", "value": "Cereal Crops"}, {"label": "Pulse Crops", "value": "Pulse Crops"}, {"label": "Oil Crops", "value": "Oil Crops"}, {"label": "Tubers, Roots & Vegetable Crops", "value": "Tubers, Roots & Vegetable Crops"}, {"label": "Fruit Crops", "value": "Fruit Crops"}, {"label": "Forage and Pasture Crops", "value": "Forage and Pasture Crops"}, {"label": "Other Crops", "value": "Other Crops"}]}},
                            {"widget": "select", "widget-id": "preferred_ecological_zone", "widget-type": "input", "widget-label": "Preferred Ecological Zone", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.preferred_ecological_zone", "widget-data-source": {"type": "static", "options": [{"label": "Kolla (Lowland < 1,500 m)", "value": "Kolla"}, {"label": "Weyna Dega (Mid-altitude 1,500-2,300 m)", "value": "Weyna Dega"}, {"label": "Dega (Highland > 2,300 m)", "value": "Dega"}]}},
                            {"widget": "text", "widget-id": "centre", "widget-type": "input", "widget-label": "Research Centre", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.centre"}
                        ]
                    },
                    {
                        "panel-id": "crop_col_2",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "number", "widget-id": "growth_cycle_days", "widget-type": "input", "widget-label": "Growth Cycle (Days)", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.growth_cycle_days"},
                            {"widget": "select", "widget-id": "water_requirement", "widget-type": "input", "widget-label": "Water Requirement", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.water_requirement", "widget-data-source": {"type": "static", "options": [{"label": "LOW", "value": "LOW"}, {"label": "MEDIUM", "value": "MEDIUM"}, {"label": "HIGH", "value": "HIGH"}, {"label": "VERY_HIGH", "value": "VERY_HIGH"}]}},
                            {"widget": "text", "widget-id": "preferred_soil_type", "widget-type": "input", "widget-label": "Preferred Soil Type", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.preferred_soil_type"},
                            {"widget": "number", "widget-id": "varieties_count", "widget-type": "input", "widget-label": "Registered Varieties", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.varieties_count"},
                            {"widget": "text", "widget-id": "known_for", "widget-type": "input", "widget-label": "Special Traits / Known For", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.known_for"},
                            {"widget": "text", "widget-id": "description", "widget-type": "input", "widget-label": "Description", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000001.description"},
                            {"widget": "select", "widget-id": "is_active", "widget-type": "input", "widget-label": "Active Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000001.is_active", "widget-data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": true}, {"label": "INACTIVE", "value": false}]}}
                        ]
                    }
                ]
            }
        ]
    }',
    'FALSE',
    'FALSE',
    'FALSE',
    'FALSE'
),
-- 2. Seed Catalog Form Section
(
    'c1000000-0000-4000-8000-000000000002',
    'seed_catalog_details_section',
    'c1000000-0000-4000-8000-000000000002',
    'FALSE',
    'seed_catalog_details',
    'Seed Variety Basic Information',
    'FALSE',
    0,
    'FALSE',
    10,
    '{
        "section-id": "seed_catalog_details",
        "section-title": "Seed Variety Information",
        "section-editable": true,
        "panels": [
            {
                "panel-id": "seed_main_panel",
                "panel-orientation": "horizontal",
                "panels": [
                    {
                        "panel-id": "seed_col_1",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "seed_code", "widget-type": "input", "widget-label": "Seed Code", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000002.seed_code"},
                            {"widget": "text", "widget-id": "variety_name", "widget-type": "input", "widget-label": "Variety Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000002.variety_name"},
                            {"widget": "text", "widget-id": "crop_name", "widget-type": "input", "widget-label": "Parent Crop Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000002.crop_name"},
                            {"widget": "text", "widget-id": "breeder_source", "widget-type": "input", "widget-label": "Breeder / Research Center", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.breeder_source"},
                            {"widget": "number", "widget-id": "release_year", "widget-type": "input", "widget-label": "Release Year", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.release_year"},
                            {"widget": "text", "widget-id": "match_status", "widget-type": "input", "widget-label": "Reconciliation Status", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.match_status"}
                        ]
                    },
                    {
                        "panel-id": "seed_col_2",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "select", "widget-id": "is_certified", "widget-type": "input", "widget-label": "Certification Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000002.is_certified", "widget-data-source": {"type": "static", "options": [{"label": "CERTIFIED", "value": true}, {"label": "UNCERTIFIED", "value": false}]}},
                            {"widget": "number", "widget-id": "maturity_days", "widget-type": "input", "widget-label": "Days to Maturity", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.maturity_days"},
                            {"widget": "text", "widget-id": "potential_yield", "widget-type": "input", "widget-label": "Potential Yield", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.potential_yield"},
                            {"widget": "text", "widget-id": "description", "widget-type": "input", "widget-label": "Agronomic Traits / Remarks", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000002.description"},
                            {"widget": "select", "widget-id": "is_active", "widget-type": "input", "widget-label": "Active Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000002.is_active", "widget-data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": true}, {"label": "INACTIVE", "value": false}]}}
                        ]
                    }
                ]
            }
        ]
    }',
    'FALSE',
    'FALSE',
    'FALSE',
    'FALSE'
),
-- 3. Inputs Catalog (Agri-Inputs) Form Section
(
    'c1000000-0000-4000-8000-000000000003',
    'inputs_catalog_details_section',
    'c1000000-0000-4000-8000-000000000003',
    'FALSE',
    'inputs_catalog_details',
    'Agri-Inputs Basic Information',
    'FALSE',
    0,
    'FALSE',
    10,
    '{
        "section-id": "inputs_catalog_details",
        "section-title": "Input Information",
        "section-editable": true,
        "panels": [
            {
                "panel-id": "inp_main_panel",
                "panel-orientation": "horizontal",
                "panels": [
                    {
                        "panel-id": "inp_col_1",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "input_code", "widget-type": "input", "widget-label": "Input Code", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000003.input_code"},
                            {"widget": "text", "widget-id": "trade_name", "widget-type": "input", "widget-label": "Trade Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000003.trade_name"},
                            {"widget": "select", "widget-id": "input_category", "widget-type": "input", "widget-label": "Input Category", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000003.input_category", "widget-data-source": {"type": "static", "options": [{"label": "Inorganic Fertilizer", "value": "INORGANIC_FERTILIZER"}, {"label": "Organic Fertilizer", "value": "ORGANIC_FERTILIZER"}, {"label": "Bio-Fertilizer / Inoculant", "value": "BIO_FERTILIZER"}, {"label": "Micronutrient", "value": "MICRONUTRIENT"}, {"label": "Soil Amendment", "value": "SOIL_AMENDMENT"}, {"label": "Pesticide", "value": "PESTICIDE"}, {"label": "Insecticide", "value": "INSECTICIDE"}, {"label": "Herbicide", "value": "HERBICIDE"}, {"label": "Fungicide", "value": "FUNGICIDE"}, {"label": "Seed Treatment", "value": "SEED_TREATMENT"}, {"label": "Plant Growth Regulator", "value": "GROWTH_REGULATOR"}, {"label": "Other Agro-Inputs", "value": "OTHER"}]}},
                            {"widget": "text", "widget-id": "nutrient_composition", "widget-type": "input", "widget-label": "Composition / Active Ingredient", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.nutrient_composition"},
                            {"widget": "text", "widget-id": "manufacturer", "widget-type": "input", "widget-label": "Manufacturer / Supplier", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.manufacturer"},
                            {"widget": "text", "widget-id": "license_number", "widget-type": "input", "widget-label": "Registration / License No", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.license_number"}
                        ]
                    },
                    {
                        "panel-id": "inp_col_2",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "application_method", "widget-type": "input", "widget-label": "Application Method", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.application_method"},
                            {"widget": "text", "widget-id": "recommended_crops", "widget-type": "input", "widget-label": "Recommended Crops", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.recommended_crops"},
                            {"widget": "text", "widget-id": "recommended_dosage", "widget-type": "input", "widget-label": "Recommended Dosage / Rate", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.recommended_dosage"},
                            {"widget": "text", "widget-id": "safety_precautions", "widget-type": "input", "widget-label": "Safety Precautions", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.safety_precautions"},
                            {"widget": "text", "widget-id": "description", "widget-type": "input", "widget-label": "Description / Specifications", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000003.description"},
                            {"widget": "select", "widget-id": "is_active", "widget-type": "input", "widget-label": "Active Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000003.is_active", "widget-data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": true}, {"label": "INACTIVE", "value": false}]}}
                        ]
                    }
                ]
            }
        ]
    }',
    'FALSE',
    'FALSE',
    'FALSE',
    'FALSE'
),
-- 4. Livestock Breed Catalog Form Section
(
    'c1000000-0000-4000-8000-000000000004',
    'livestock_catalog_details_section',
    'c1000000-0000-4000-8000-000000000004',
    'FALSE',
    'livestock_catalog_details',
    'Livestock Breed Basic Information',
    'FALSE',
    0,
    'FALSE',
    10,
    '{
        "section-id": "livestock_catalog_details",
        "section-title": "Breed Information",
        "section-editable": true,
        "panels": [
            {
                "panel-id": "lstk_main_panel",
                "panel-orientation": "horizontal",
                "panels": [
                    {
                        "panel-id": "lstk_col_1",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "breed_code", "widget-type": "input", "widget-label": "Breed Code", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000004.breed_code"},
                            {"widget": "text", "widget-id": "breed_name", "widget-type": "input", "widget-label": "Breed Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000004.breed_name"},
                            {"widget": "text", "widget-id": "abbreviation", "widget-type": "input", "widget-label": "Abbreviation", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.abbreviation"},
                            {"widget": "select", "widget-id": "species", "widget-type": "input", "widget-label": "Species", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000004.species", "widget-data-source": {"type": "static", "options": [{"label": "CATTLE", "value": "CATTLE"}, {"label": "SHEEP", "value": "SHEEP"}, {"label": "GOAT", "value": "GOAT"}, {"label": "CAMEL", "value": "CAMEL"}, {"label": "BEEHIVE", "value": "BEEHIVE"}]}},
                            {"widget": "select", "widget-id": "breed_type", "widget-type": "input", "widget-label": "Breed Type", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.breed_type", "widget-data-source": {"type": "static", "options": [{"label": "Indigenous", "value": "Indigenous"}, {"label": "Exotic", "value": "Exotic"}, {"label": "Cross", "value": "Cross"}]}}
                        ]
                    },
                    {
                        "panel-id": "lstk_col_2",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "select", "widget-id": "primary_purpose", "widget-type": "input", "widget-label": "Primary Purpose", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.primary_purpose", "widget-data-source": {"type": "static", "options": [{"label": "DAIRY", "value": "DAIRY"}, {"label": "MEAT", "value": "MEAT"}, {"label": "DUAL_PURPOSE", "value": "DUAL_PURPOSE"}, {"label": "WOOL", "value": "WOOL"}, {"label": "EGG", "value": "EGG"}, {"label": "HONEY_POLLINATION", "value": "HONEY_POLLINATION"}, {"label": "DRAUGHT", "value": "DRAUGHT"}, {"label": "OTHER", "value": "OTHER"}]}},
                            {"widget": "text", "widget-id": "origin_country", "widget-type": "input", "widget-label": "Country / Region of Origin", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.origin_country"},
                            {"widget": "select", "widget-id": "in_national_standard", "widget-type": "input", "widget-label": "In National Standard", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.in_national_standard", "widget-data-source": {"type": "static", "options": [{"label": "YES", "value": true}, {"label": "NO", "value": false}]}},
                            {"widget": "select", "widget-id": "in_etlits_registry", "widget-type": "input", "widget-label": "In ET-LITS Registry", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.in_etlits_registry", "widget-data-source": {"type": "static", "options": [{"label": "YES", "value": true}, {"label": "NO", "value": false}]}},
                            {"widget": "text", "widget-id": "description", "widget-type": "input", "widget-label": "Description", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000004.description"},
                            {"widget": "select", "widget-id": "is_active", "widget-type": "input", "widget-label": "Active Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000004.is_active", "widget-data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": true}, {"label": "INACTIVE", "value": false}]}}
                        ]
                    }
                ]
            }
        ]
    }',
    'FALSE',
    'FALSE',
    'FALSE',
    'FALSE'
),
-- 4. Location Catalog Form Section
(
    'c1000000-0000-4000-8000-000000000005',
    'location_catalog_details_section',
    'c1000000-0000-4000-8000-000000000005',
    'FALSE',
    'location_catalog_details',
    'Location Basic Information',
    'FALSE',
    0,
    'FALSE',
    10,
    '{
        "section-id": "location_catalog_details",
        "section-title": "Location Information",
        "section-editable": true,
        "panels": [
            {
                "panel-id": "location_main_panel",
                "panel-orientation": "horizontal",
                "panels": [
                    {
                        "panel-id": "location_col_1",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "location_code", "widget-type": "input", "widget-label": "Location Code", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000005.location_code"},
                            {"widget": "text", "widget-id": "location_name", "widget-type": "input", "widget-label": "Location Name", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000005.location_name"},
                            {"widget": "select", "widget-id": "admin_level", "widget-type": "input", "widget-label": "Administrative Level", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000005.admin_level", "widget-data-source": {"type": "static", "options": [{"label": "Region", "value": "Region"}, {"label": "Zone", "value": "Zone"}, {"label": "Woreda", "value": "Woreda"}, {"label": "Kebele", "value": "Kebele"}]}},
                            {"widget": "text", "widget-id": "capital_city", "widget-type": "input", "widget-label": "Capital / Center", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.capital_city"}
                        ]
                    },
                    {
                        "panel-id": "location_col_2",
                        "panel-orientation": "vertical",
                        "widgets": [
                            {"widget": "text", "widget-id": "parent_location_name", "widget-type": "input", "widget-label": "Parent Location Name", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.parent_location_name"},
                            {"widget": "text", "widget-id": "parent_location_code", "widget-type": "input", "widget-label": "Parent Location Code", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.parent_location_code"},
                            {"widget": "text", "widget-id": "pcode", "widget-type": "input", "widget-label": "P-Code", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.pcode"},
                            {"widget": "number", "widget-id": "area_sq_km", "widget-type": "input", "widget-label": "Area (sq km)", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.area_sq_km"},
                            {"widget": "number", "widget-id": "population_estimate", "widget-type": "input", "widget-label": "Estimated Population", "widget-required": false, "widget-data-path": "c1000000-0000-4000-8000-000000000005.population_estimate"},
                            {"widget": "select", "widget-id": "is_active", "widget-type": "input", "widget-label": "Active Status", "widget-required": true, "widget-data-path": "c1000000-0000-4000-8000-000000000005.is_active", "widget-data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": true}, {"label": "INACTIVE", "value": false}]}}
                        ]
                    }
                ]
            }
        ]
    }',
    'FALSE',
    'FALSE',
    'FALSE',
    'FALSE'
)
ON CONFLICT ("section_id") DO UPDATE 
SET "section_ui_schema" = EXCLUDED."section_ui_schema";
