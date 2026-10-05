-- OpenG2P Reference Data Attributes and Attribute Values for Catalog Extension

INSERT INTO "public"."g2p_attributes" (
    "attribute_id",
    "attribute_code",
    "attribute_display",
    "is_hierarchical"
) VALUES 
('CROP_CATEGORY', 'CROP_CATEGORY', 'Crop Category', false),
('ECOLOGICAL_ZONE', 'ECOLOGICAL_ZONE', 'Ecological Zone', false),
('LIVESTOCK_SPECIES', 'LIVESTOCK_SPECIES', 'Livestock Species', false),
('FERTILIZER_TYPE', 'FERTILIZER_TYPE', 'Input / Fertilizer Category', false),
('INPUT_CATEGORY', 'INPUT_CATEGORY', 'Agri-Input Category', false),
('LOCATION_ADMIN_LEVEL', 'LOCATION_ADMIN_LEVEL', 'Administrative Level', false)
ON CONFLICT ("attribute_id") DO UPDATE 
SET "attribute_display" = EXCLUDED."attribute_display",
    "is_hierarchical" = EXCLUDED."is_hierarchical";

INSERT INTO "public"."g2p_attribute_values" (
    "value_id",
    "attribute_id",
    "value_code",
    "value_display",
    "parent_value_id",
    "sort_order"
) VALUES
-- Crop Categories
('CROP_CAT_1', 'CROP_CATEGORY', 'Cereal Crops', 'Cereal Crops', null, 1),
('CROP_CAT_2', 'CROP_CATEGORY', 'Pulse Crops', 'Pulse Crops', null, 2),
('CROP_CAT_3', 'CROP_CATEGORY', 'Oil Crops', 'Oil Crops', null, 3),
('CROP_CAT_4', 'CROP_CATEGORY', 'Tubers, Roots & Vegetable Crops', 'Tubers, Roots & Vegetable Crops', null, 4),
('CROP_CAT_5', 'CROP_CATEGORY', 'Fruit Crops', 'Fruit Crops', null, 5),
('CROP_CAT_6', 'CROP_CATEGORY', 'Forage and Pasture Crops', 'Forage and Pasture Crops', null, 6),
('CROP_CAT_7', 'CROP_CATEGORY', 'Other Crops', 'Other Crops', null, 7),

-- Ecological Zones
('ECO_ZONE_1', 'ECOLOGICAL_ZONE', 'Kolla', 'Kolla (Lowland < 1,500 m)', null, 1),
('ECO_ZONE_2', 'ECOLOGICAL_ZONE', 'Weyna Dega', 'Weyna Dega (Mid-altitude 1,500-2,300 m)', null, 2),
('ECO_ZONE_3', 'ECOLOGICAL_ZONE', 'Dega', 'Dega (Highland > 2,300 m)', null, 3),

-- Livestock Species
('LSTK_SPEC_1', 'LIVESTOCK_SPECIES', 'CATTLE', 'Cattle', null, 1),
('LSTK_SPEC_2', 'LIVESTOCK_SPECIES', 'SHEEP', 'Sheep', null, 2),
('LSTK_SPEC_3', 'LIVESTOCK_SPECIES', 'GOAT', 'Goat', null, 3),
('LSTK_SPEC_4', 'LIVESTOCK_SPECIES', 'CAMEL', 'Camel', null, 4),
('LSTK_SPEC_5', 'LIVESTOCK_SPECIES', 'BEEHIVE', 'Beehive', null, 5),

-- Fertilizer / Input Categories (FERTILIZER_TYPE for backward compatibility)
('FERT_TYPE_1', 'FERTILIZER_TYPE', 'INORGANIC_FERTILIZER', 'Inorganic Fertilizer', null, 1),
('FERT_TYPE_2', 'FERTILIZER_TYPE', 'ORGANIC_FERTILIZER', 'Organic Fertilizer', null, 2),
('FERT_TYPE_3', 'FERTILIZER_TYPE', 'BIO_FERTILIZER', 'Bio Fertilizer', null, 3),
('FERT_TYPE_4', 'FERTILIZER_TYPE', 'MICRONUTRIENT', 'Micronutrient', null, 4),
('FERT_TYPE_5', 'FERTILIZER_TYPE', 'SOIL_AMENDMENT', 'Soil Amendment', null, 5),
('FERT_TYPE_6', 'FERTILIZER_TYPE', 'PESTICIDE', 'Pesticide', null, 6),
('FERT_TYPE_7', 'FERTILIZER_TYPE', 'HERBICIDE', 'Herbicide', null, 7),
('FERT_TYPE_8', 'FERTILIZER_TYPE', 'OTHER', 'Other Inputs', null, 8),

-- Generalized Agri-Inputs Categories (INPUT_CATEGORY)
('INP_CAT_1', 'INPUT_CATEGORY', 'INORGANIC_FERTILIZER', 'Inorganic Fertilizer', null, 1),
('INP_CAT_2', 'INPUT_CATEGORY', 'ORGANIC_FERTILIZER', 'Organic Fertilizer', null, 2),
('INP_CAT_3', 'INPUT_CATEGORY', 'BIO_FERTILIZER', 'Bio-Fertilizer / Inoculant', null, 3),
('INP_CAT_4', 'INPUT_CATEGORY', 'MICRONUTRIENT', 'Micronutrient', null, 4),
('INP_CAT_5', 'INPUT_CATEGORY', 'SOIL_AMENDMENT', 'Soil Amendment / Conditioner', null, 5),
('INP_CAT_6', 'INPUT_CATEGORY', 'PESTICIDE', 'Chemical Pesticide', null, 6),
('INP_CAT_7', 'INPUT_CATEGORY', 'INSECTICIDE', 'Insecticide', null, 7),
('INP_CAT_8', 'INPUT_CATEGORY', 'HERBICIDE', 'Herbicide', null, 8),
('INP_CAT_9', 'INPUT_CATEGORY', 'FUNGICIDE', 'Fungicide', null, 9),
('INP_CAT_10', 'INPUT_CATEGORY', 'SEED_TREATMENT', 'Seed Treatment / Dressing', null, 10),
('INP_CAT_11', 'INPUT_CATEGORY', 'GROWTH_REGULATOR', 'Plant Growth Regulator', null, 11),
('INP_CAT_12', 'INPUT_CATEGORY', 'OTHER', 'Other Agro-Inputs', null, 12),

-- Administrative Levels
('ADMIN_LVL_1', 'LOCATION_ADMIN_LEVEL', 'Region', 'Region (Level 1)', null, 1),
('ADMIN_LVL_2', 'LOCATION_ADMIN_LEVEL', 'Zone', 'Zone (Level 2)', null, 2),
('ADMIN_LVL_3', 'LOCATION_ADMIN_LEVEL', 'Woreda', 'Woreda (Level 3)', null, 3),
('ADMIN_LVL_4', 'LOCATION_ADMIN_LEVEL', 'Kebele', 'Kebele (Level 4)', null, 4)
ON CONFLICT ("value_id") DO UPDATE 
SET "value_display" = EXCLUDED."value_display",
    "sort_order" = EXCLUDED."sort_order";
