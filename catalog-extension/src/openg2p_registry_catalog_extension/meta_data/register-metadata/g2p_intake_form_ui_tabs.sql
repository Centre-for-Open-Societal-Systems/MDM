INSERT INTO "public"."g2p_intake_form_ui_tabs" (
    "tab_id",
    "form_id",
    "tab_label",
    "tab_order"
) VALUES 
('c1000000-0000-4000-9000-000000000101', 'c1000000-0000-4000-9000-000000000001', 'Crop Details', 10),
('c1000000-0000-4000-9000-000000000102', 'c1000000-0000-4000-9000-000000000002', 'Seed Details', 10),
('c1000000-0000-4000-9000-000000000103', 'c1000000-0000-4000-9000-000000000003', 'Inputs Details', 10),
('c1000000-0000-4000-9000-000000000104', 'c1000000-0000-4000-9000-000000000004', 'Breed Details', 10),
('c1000000-0000-4000-9000-000000000105', 'c1000000-0000-4000-9000-000000000005', 'Location Details', 10)
ON CONFLICT ("tab_id") DO UPDATE 
SET "form_id" = EXCLUDED."form_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order";
