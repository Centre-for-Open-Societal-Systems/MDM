INSERT INTO "public"."g2p_register_ui_tabs" (
    "tab_id",
    "register_id",
    "tab_label",
    "tab_order",
    "is_active"
) VALUES 
('crop_catalog_main_tab', 'c1000000-0000-4000-8000-000000000001', 'Crop Details', 1, 'TRUE'),
('seed_catalog_main_tab', 'c1000000-0000-4000-8000-000000000002', 'Seed Details', 1, 'TRUE'),
('inputs_catalog_main_tab', 'c1000000-0000-4000-8000-000000000003', 'Inputs Details', 1, 'TRUE'),
('fertilizer_catalog_main_tab', 'c1000000-0000-4000-8000-000000000003', 'Inputs Details', 2, 'TRUE'),
('livestock_catalog_main_tab', 'c1000000-0000-4000-8000-000000000004', 'Breed Details', 1, 'TRUE'),
('location_catalog_main_tab', 'c1000000-0000-4000-8000-000000000005', 'Location Details', 1, 'TRUE')
ON CONFLICT ("tab_id") DO UPDATE 
SET "tab_label" = EXCLUDED."tab_label",
    "is_active" = EXCLUDED."is_active";
