INSERT INTO "public"."g2p_intake_form_definitions" (
    "form_id",
    "register_id",
    "form_mnemonic",
    "form_description",
    "number_of_verifications",
    "used_only_in_ingestion_pipeline"
) VALUES 
('c1000000-0000-4000-9000-000000000001', 'c1000000-0000-4000-8000-000000000001', 'Crop Catalog Registration', 'Crop Catalog Registration Form', 0, 'FALSE'),
('c1000000-0000-4000-9000-000000000002', 'c1000000-0000-4000-8000-000000000002', 'Crop Variety Registration', 'Crop Variety Registration Form', 0, 'FALSE'),
('c1000000-0000-4000-9000-000000000003', 'c1000000-0000-4000-8000-000000000003', 'Inputs Catalog Registration', 'Inputs Catalog Registration Form', 0, 'FALSE'),
('c1000000-0000-4000-9000-000000000004', 'c1000000-0000-4000-8000-000000000004', 'Livestock Breed Registration', 'Livestock Breed Registration Form', 0, 'FALSE'),
('c1000000-0000-4000-9000-000000000005', 'c1000000-0000-4000-8000-000000000005', 'Location Registration', 'Location Catalog Registration Form', 0, 'FALSE')
ON CONFLICT ("form_id") DO UPDATE 
SET "register_id" = EXCLUDED."register_id",
    "form_mnemonic" = EXCLUDED."form_mnemonic",
    "form_description" = EXCLUDED."form_description",
    "number_of_verifications" = EXCLUDED."number_of_verifications",
    "used_only_in_ingestion_pipeline" = EXCLUDED."used_only_in_ingestion_pipeline";
