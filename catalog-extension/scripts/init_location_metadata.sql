-- OpenG2P Location Catalog Metadata Script
-- Inserts Register Definition, Schemas, Sections, Tabs, and Intake Form for LocationCatalog

-- 1. Register Definition
INSERT INTO "public"."g2p_register_definitions" (
    "register_id",
    "register_mnemonic",
    "register_subject",
    "register_description",
    "master_register_id",
    "register_rank",
    "functional_id_generation_required",
    "register_purpose",
    "program_id",
    "program_mnemonic",
    "register_icon",
    "has_image",
    "dedup_is_enabled",
    "dedup_threshold_score",
    "completion_score_required",
    "outgest_applicable",
    "requires_registrant_authentication",
    "registrant_authentication_validity_days",
    "registrant_re_auth_warning_days_before"
) VALUES 
('c1000000-0000-4000-8000-000000000005', 'LocationCatalog', 'Location Catalog', 'Administrative Geolocation Master Catalog', NULL, 40, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30)
ON CONFLICT ("register_id") DO UPDATE 
SET "register_mnemonic" = EXCLUDED."register_mnemonic",
    "register_subject" = EXCLUDED."register_subject",
    "register_description" = EXCLUDED."register_description";

-- 2. Register Schema (Search & Filter)
INSERT INTO "public"."g2p_register_schemas" ("register_id", "deduplicate_schema", "search_result_schema", "filter_schema") VALUES 
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

-- 3. Register Section (UI Schema with Geo Hierarchy)
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

-- 4. Register UI Tab & Tab Section
INSERT INTO "public"."g2p_register_ui_tabs" (
    "tab_id",
    "register_id",
    "tab_label",
    "tab_order",
    "is_active"
) VALUES 
('location_catalog_main_tab', 'c1000000-0000-4000-8000-000000000005', 'Location Details', 1, 'TRUE')
ON CONFLICT ("tab_id") DO UPDATE 
SET "tab_label" = EXCLUDED."tab_label",
    "is_active" = EXCLUDED."is_active";

INSERT INTO "public"."g2p_register_ui_tab_sections" (
    "tab_section_id",
    "register_id",
    "tab_id",
    "section_id",
    "section_order"
) VALUES 
('location_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000005', 'location_catalog_main_tab', 'location_catalog_details_section', 10)
ON CONFLICT ("tab_section_id") DO UPDATE 
SET "section_order" = EXCLUDED."section_order";

-- 5. Intake Form Definition & Tabs (for Maker-Checker proposals)
INSERT INTO "public"."g2p_intake_form_definitions" (
    "form_id",
    "register_id",
    "form_mnemonic",
    "form_description",
    "number_of_verifications",
    "used_only_in_ingestion_pipeline"
) VALUES 
('c1000000-0000-4000-9000-000000000005', 'c1000000-0000-4000-8000-000000000005', 'Location Registration', 'Location Catalog Registration Form', 0, 'FALSE')
ON CONFLICT ("form_id") DO UPDATE 
SET "register_id" = EXCLUDED."register_id",
    "form_mnemonic" = EXCLUDED."form_mnemonic",
    "form_description" = EXCLUDED."form_description";

INSERT INTO "public"."g2p_intake_form_ui_tabs" (
    "tab_id",
    "form_id",
    "tab_label",
    "tab_order"
) VALUES 
('c1000000-0000-4000-9000-000000000105', 'c1000000-0000-4000-9000-000000000005', 'Location Details', 10)
ON CONFLICT ("tab_id") DO UPDATE 
SET "form_id" = EXCLUDED."form_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order";

INSERT INTO "public"."g2p_intake_form_ui_tab_sections" (
    "tab_section_id",
    "tab_id",
    "section_id",
    "section_order"
) VALUES 
('location_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000105', 'location_catalog_details_section', 10)
ON CONFLICT ("tab_section_id") DO UPDATE 
SET "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
