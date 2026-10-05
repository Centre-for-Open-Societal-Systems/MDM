-- Sample Seed Data for Catalog Registers Aligned with Ethiopian National MDM
-- Ensures Staff Portal UI and APIs display realistic data right away

-- 1. CROP CATALOG SAMPLES
INSERT INTO public.g2p_register_crop_catalogs (
    internal_record_id, record_name, crop_code, crop_name, scientific_name, 
    crop_category, preferred_ecological_zone, centre, varieties_count, known_for,
    growth_cycle_days, water_requirement, preferred_soil_type, num_field_inspection_needed, isolation_distance,
    description, is_active, search_text, record_status
) VALUES 
(
    'crop-001', 'Bread Wheat (Kakaba)', 'WHEAT-001', 'Bread Wheat', 'Triticum aestivum',
    'CEREAL', 'Dega / Weyna Dega', 'KARC', 129, 'Specially for bread preparation, major cereal crop in high potential areas.',
    120, 'MEDIUM', 'Loam / Clay loam', 5, 3,
    'Major staple cereal for grain and flour production in Ethiopian highlands.',
    TRUE, 'WHEAT-001 Bread Wheat Triticum aestivum CEREAL Dega KARC', 'ACTIVE'
),
(
    'crop-002', 'Highland Teff', 'TEFF-001', 'Teff', 'Eragrostis tef',
    'CEREAL', 'Weyna Dega', 'DZARC', 52, 'Traditional Ethiopian staple food crop for injera, gluten-free cereal.',
    90, 'MEDIUM', 'Clay loam / Black soil', 3, 3,
    'Indigenous Ethiopian cereal grain with high calcium and iron content.',
    TRUE, 'TEFF-001 Teff Eragrostis tef CEREAL Weyna Dega DZARC', 'ACTIVE'
),
(
    'crop-003', 'Hybrid Maize', 'MAIZE-001', 'Maize (Corn)', 'Zea mays',
    'CEREAL', 'Kolla / Weyna Dega', 'BKARC', 99, 'High yielding hybrid and composite types, major food security crop.',
    140, 'HIGH', 'Deep well-drained loam', 2, 300,
    'High yielding hybrid white maize widely cultivated in sub-humid mid-altitudes.',
    TRUE, 'MAIZE-001 Maize (Corn) Zea mays CEREAL Kolla BKARC', 'ACTIVE'
),
(
    'crop-004', 'Arabica Coffee', 'COFFEE-001', 'Arabica Coffee', 'Coffea arabica',
    'CASH_CROP', 'Weyna Dega', 'JARC', 36, 'Ethiopian heirloom highland coffee, specialty export commodity.',
    365, 'HIGH', 'Humus-rich volcanic soil', 2, 10,
    'Premium highland washed and unwashed Arabica coffee from the birthplace of coffee.',
    TRUE, 'COFFEE-001 Arabica Coffee Coffea arabica CASH_CROP Weyna Dega JARC', 'ACTIVE'
),
(
    'crop-005', 'Desi Chickpea', 'CHICKPEA-001', 'Chickpea', 'Cicer arietinum',
    'PULSE', 'Weyna Dega', 'DZARC', 27, 'Desi and Kabuli types, premium export and protein food crop.',
    100, 'LOW', 'Sandy loam / Light clay', 2, 3,
    'Drought-tolerant leguminous protein source with atmospheric nitrogen-fixing capabilities.',
    TRUE, 'CHICKPEA-001 Chickpea Cicer arietinum PULSE Weyna Dega DZARC', 'ACTIVE'
),
(
    'crop-006', 'Highland Faba Bean', 'FABABEAN-001', 'Faba Bean', 'Vicia faba',
    'PULSE', 'Dega / Weyna Dega', 'HARC', 33, 'Major highland pulse, excellent atmospheric nitrogen fixing crop.',
    110, 'MEDIUM', 'Clay loam', 2, 0,
    'Highland food legume widely used in crop rotation to boost soil fertility.',
    TRUE, 'FABABEAN-001 Faba Bean Vicia faba PULSE Dega HARC', 'ACTIVE'
)
ON CONFLICT (crop_code) DO NOTHING;

-- 2. SEED VARIETY SAMPLES
INSERT INTO public.g2p_register_seed_catalogs (
    internal_record_id, record_name, seed_code, variety_name, crop_name,
    breeder_source, release_year, maturity_days, potential_yield, yield_unit,
    match_status, is_certified, description, search_text, record_status
) VALUES 
(
    'seed-001', 'Kakaba Wheat Seed', 'SEED-WHT-KAKABA', 'Kakaba (KARC-101)', 'Bread Wheat',
    'Kulumsa Agricultural Research Center', 2010, 105, '45 - 52', 'Quintal/Ha',
    'MATCHED', TRUE,
    'Stem and stripe rust resistant, early maturing bread wheat variety suitable for mid-to-high altitudes.',
    'SEED-WHT-KAKABA Kakaba (KARC-101) Bread Wheat Kulumsa MATCHED', 'ACTIVE'
),
(
    'seed-002', 'Quncho Teff Seed', 'SEED-TEF-QUNCHO', 'Quncho (DZ-Cr-387)', 'Teff',
    'Debre Zeit Agricultural Research Center', 2006, 95, '24 - 28', 'Quintal/Ha',
    'MATCHED', TRUE,
    'Very popular white teff with high grain quality and export market premium.',
    'SEED-TEF-QUNCHO Quncho (DZ-Cr-387) Teff Debre Zeit MATCHED', 'ACTIVE'
),
(
    'seed-003', 'BH-540 Hybrid Maize Seed', 'SEED-MAZ-BH540', 'BH-540 Hybrid', 'Maize (Corn)',
    'Bako Agricultural Research Center', 1995, 145, '80 - 90', 'Quintal/Ha',
    'MATCHED', TRUE,
    'Intermediate maturity white hybrid adapted to mid-altitude sub-humid agro-ecologies.',
    'SEED-MAZ-BH540 BH-540 Hybrid Maize Bako MATCHED', 'ACTIVE'
),
(
    'seed-004', 'Gesha Arabica Seed', 'SEED-COF-GEISHA', 'Gesha Selection 1931', 'Arabica Coffee',
    'Jimma Agricultural Research Center', 2007, 240, '15 - 20', 'Quintal/Ha',
    'UNRESOLVED', TRUE,
    'Exotic floral cup profile with strong resistance to Coffee Berry Disease (CBD).',
    'SEED-COF-GEISHA Gesha Selection Arabica Coffee Jimma UNRESOLVED', 'ACTIVE'
)
ON CONFLICT (seed_code) DO NOTHING;

-- 3. FERTILIZER SAMPLES
INSERT INTO public.g2p_register_fertilizer_catalogs (
    internal_record_id, record_name, input_code, trade_name, fertilizer_type,
    nutrient_composition, manufacturer, recommended_crops, application_method,
    is_active, search_text, record_status
) VALUES 
(
    'fert-001', 'NPSB Blend Fertilizer', 'FERT-NPSB', 'NPSB Soil Blend', 'INORGANIC_FERTILIZER',
    '18.9% N, 37.7% P2O5, 6.95% S, 0.1% B', 'OCP Group / Ministry of Agriculture',
    'Wheat, Teff, Barley, Maize', 'Basal row application at planting',
    TRUE, 'FERT-NPSB NPSB Soil Blend INORGANIC_FERTILIZER OCP', 'ACTIVE'
),
(
    'fert-002', 'Granular Urea 46%', 'FERT-UREA', 'Urea 46-0-0', 'INORGANIC_FERTILIZER',
    '46% Total Nitrogen (N)', 'Ethio-Agri Import Corp',
    'All Cereals, Horticultural Crops', 'Split top-dressing at active tillering',
    TRUE, 'FERT-UREA Urea 46-0-0 INORGANIC_FERTILIZER', 'ACTIVE'
),
(
    'fert-003', 'Rhizobium Bio-Inoculant', 'FERT-BIO-RHIZO', 'Legume Bio-Rhizobium', 'BIO_FERTILIZER',
    'Live Rhizobium leguminosarum strain (> 10^9 CFU/g)', 'National Soil Testing Lab',
    'Faba Bean, Chickpea, Lentils', 'Seed coating slurry before sowing',
    TRUE, 'FERT-BIO-RHIZO Legume Bio-Rhizobium BIO_FERTILIZER', 'ACTIVE'
),
(
    'fert-004', 'Organic Vermicompost', 'FERT-COMPOST', 'Bio-Green Vermicompost', 'ORGANIC_FERTILIZER',
    'Rich in humic acid, 2.5% N, 1.8% P, 2.0% K', 'EcoFarm Inputs PLC',
    'Vegetables, Seedlings, Coffee nurseries', 'Soil mixing at 2-5 tons/hectare',
    TRUE, 'FERT-COMPOST Bio-Green Vermicompost ORGANIC_FERTILIZER', 'ACTIVE'
)
ON CONFLICT (input_code) DO NOTHING;

-- 4. LIVESTOCK BREED SAMPLES
INSERT INTO public.g2p_register_livestock_catalogs (
    internal_record_id, record_name, breed_code, breed_name, species, breed_type, abbreviation,
    in_national_standard, in_etlits_registry, primary_purpose, origin_country, climate_tolerance,
    is_active, search_text, record_status
) VALUES 
(
    'lstk-001', 'Boran Zebu (BOR)', '1.01.01', 'Boran Zebu', 'CATTLE', 'Indigenous', 'BOR',
    TRUE, TRUE, 'BEEF_AND_DAIRY', 'Ethiopia (Borana Plateau)', 'Arid and semi-arid pastoral rangelands',
    TRUE, '1.01.01 Boran Zebu BOR CATTLE Indigenous BEEF_AND_DAIRY', 'ACTIVE'
),
(
    'lstk-002', 'Horro Cattle (HOR)', '1.01.02', 'Horro Cattle', 'CATTLE', 'Indigenous', 'HOR',
    TRUE, FALSE, 'DUAL_PURPOSE', 'Ethiopia (Western Oromia)', 'Highland sub-humid to moist plateau',
    TRUE, '1.01.02 Horro Cattle HOR CATTLE Indigenous DUAL_PURPOSE', 'ACTIVE'
),
(
    'lstk-003', 'Menz Sheep (MEN)', '2.01.01', 'Menz Highland Sheep', 'SHEEP', 'Indigenous', 'MEN',
    TRUE, TRUE, 'MEAT_AND_WOOL', 'Ethiopia (North Shewa Highlands)', 'Cold frost-prone afro-alpine highlands',
    TRUE, '2.01.01 Menz Highland Sheep MEN SHEEP Indigenous MEAT_AND_WOOL', 'ACTIVE'
),
(
    'lstk-004', 'Afar Goat (AFA)', '3.01.01', 'Afar / Danakil Goat', 'GOAT', 'Indigenous', 'AFA',
    TRUE, FALSE, 'MEAT_AND_MILK', 'Ethiopia (Afar Depression)', 'Extremely hot and arid lowlands',
    TRUE, '3.01.01 Afar / Danakil Goat AFA GOAT Indigenous MEAT_AND_MILK', 'ACTIVE'
)
ON CONFLICT (breed_code) DO NOTHING;
