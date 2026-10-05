INSERT INTO "public"."g2p_intake_form_ui_tab_sections" (
    "tab_section_id",
    "tab_id",
    "section_id",
    "section_order"
) VALUES 
('crop_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000101', 'crop_catalog_details_section', 10),
('seed_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000102', 'seed_catalog_details_section', 10),
('inputs_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000103', 'inputs_catalog_details_section', 10),
('livestock_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000104', 'livestock_catalog_details_section', 10),
('location_catalog_intake_section_01', 'c1000000-0000-4000-9000-000000000105', 'location_catalog_details_section', 10)
ON CONFLICT ("tab_section_id") DO UPDATE 
SET "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
