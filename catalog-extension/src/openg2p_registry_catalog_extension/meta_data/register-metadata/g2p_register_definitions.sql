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
('c1000000-0000-4000-8000-000000000001', 'CropCatalog', 'Crop Catalog', 'Agricultural Crop Master Catalog', NULL, 10, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30),
('c1000000-0000-4000-8000-000000000002', 'SeedCatalog', 'Seed Varieties', 'Seed Variety Master Catalog', NULL, 20, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30),
('c1000000-0000-4000-8000-000000000003', 'InputsCatalog', 'Inputs Catalog', 'Agri-Inputs Master Catalog (Fertilizers, Pesticides, Herbicides, Soil Amendments, Seed Treatments)', NULL, 25, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30),
('c1000000-0000-4000-8000-000000000004', 'LivestockCatalog', 'Livestock Breeds', 'Livestock Breed Master Catalog', NULL, 30, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30),
('c1000000-0000-4000-8000-000000000005', 'LocationCatalog', 'Location Catalog', 'Administrative Geolocation Master Catalog', NULL, 40, 'FALSE', 'REGISTER', NULL, NULL, NULL, 'FALSE', 'FALSE', 0, 'FALSE', 'FALSE', 'FALSE', 730, 30)
ON CONFLICT ("register_id") DO UPDATE 
SET "register_mnemonic" = EXCLUDED."register_mnemonic",
    "register_subject" = EXCLUDED."register_subject",
    "register_description" = EXCLUDED."register_description";
