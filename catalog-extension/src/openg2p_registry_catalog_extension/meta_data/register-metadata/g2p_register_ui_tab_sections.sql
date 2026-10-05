INSERT INTO "public"."g2p_register_ui_tab_sections" (
    "tab_section_id",
    "register_id",
    "tab_id",
    "section_id",
    "section_order"
) VALUES 
('crop_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000001', 'crop_catalog_main_tab', 'crop_catalog_details_section', 10),
('seed_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000002', 'seed_catalog_main_tab', 'seed_catalog_details_section', 10),
('inputs_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000003', 'inputs_catalog_main_tab', 'inputs_catalog_details_section', 10),
('fertilizer_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000003', 'fertilizer_catalog_main_tab', 'inputs_catalog_details_section', 10),
('livestock_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000004', 'livestock_catalog_main_tab', 'livestock_catalog_details_section', 10),
('location_catalog_main_tab_sec_01', 'c1000000-0000-4000-8000-000000000005', 'location_catalog_main_tab', 'location_catalog_details_section', 10)
ON CONFLICT ("tab_section_id") DO UPDATE 
SET "section_order" = EXCLUDED."section_order";
