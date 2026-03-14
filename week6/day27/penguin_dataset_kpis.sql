-- KPI for penguin dataset using SQL

-- Total Penguins Count
SELECT COUNT(*) AS total_penguins
FROM penguins
WHERE species IS NOT NULL;

-- Species Distribution
SELECT species, COUNT(*) AS species_count
FROM penguins
GROUP BY species;

SELECT 
    species,
    COUNT(*) AS species_count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM penguins)),2) AS percentage
FROM penguins
GROUP BY species;

-- Total Penguins per Island
SELECT island, COUNT(*) AS total_penguins
FROM penguins
GROUP BY island;

SELECT 
    island,
    COUNT(*) AS total_penguins,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM penguins)),2) AS percentage
FROM penguins
GROUP BY island;

-- Average Body Mass

-- Overall Average
SELECT AVG(body_mass_g) AS avg_body_mass
FROM penguins;

-- Average by Species
SELECT species, AVG(body_mass_g) AS avg_body_mass
FROM penguins
GROUP BY species;

-- Average by Gender
SELECT sex, AVG(body_mass_g) AS avg_body_mass
FROM penguins
GROUP BY sex;

-- Average Flipper Length

-- Overall
SELECT AVG(flipper_length_mm) AS avg_flipper_length
FROM penguins;

-- By Species
SELECT species, AVG(flipper_length_mm) AS avg_flipper_length
FROM penguins
GROUP BY species;

-- By Gender
SELECT sex, AVG(flipper_length_mm) AS avg_flipper_length
FROM penguins
GROUP BY sex;

-- Average Bill Length

-- Overall
SELECT AVG(bill_length_mm) AS avg_bill_length
FROM penguins;

-- By Species
SELECT species, AVG(bill_length_mm) AS avg_bill_length
FROM penguins
GROUP BY species;

-- Average Bill Depth

-- Overall
SELECT AVG(bill_depth_mm) AS avg_bill_depth
FROM penguins;

-- By Species
SELECT species, AVG(bill_depth_mm) AS avg_bill_depth
FROM penguins
GROUP BY species;

-- Bill Ratio KPI

-- Bill Length / Bill Depth
SELECT 
    species,
    AVG(bill_length_mm / bill_depth_mm) AS avg_bill_ratio
FROM penguins
GROUP BY species;

-- Male vs Female Count

-- Total Males & Females
SELECT sex, COUNT(*) AS count_gender
FROM penguins
GROUP BY sex;

-- Percentage Split
SELECT 
    sex,
    COUNT(*) AS count_gender,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM penguins)),2) AS percentage
FROM penguins
GROUP BY sex;

-- Size Difference by Gender

-- Body Mass Difference
SELECT 
    MAX(CASE WHEN sex='male' THEN body_mass_g END) -
    MAX(CASE WHEN sex='female' THEN body_mass_g END) 
AS body_mass_difference
FROM penguins;

-- Flipper Length Difference
SELECT 
    MAX(CASE WHEN sex='male' THEN flipper_length_mm END) -
    MAX(CASE WHEN sex='female' THEN flipper_length_mm END)
AS flipper_length_difference
FROM penguins;

-- Correlation KPIs

-- Body Mass vs Flipper Length
-- SELECT CORR(body_mass_g, flipper_length_mm) AS correlation FROM penguins;

SELECT 
(
COUNT(*) * SUM(body_mass_g * flipper_length_mm) -
SUM(body_mass_g) * SUM(flipper_length_mm)
)
/
SQRT(
(COUNT(*) * SUM(POWER(body_mass_g,2)) - POWER(SUM(body_mass_g),2)) *
(COUNT(*) * SUM(POWER(flipper_length_mm,2)) - POWER(SUM(flipper_length_mm),2))
) AS correlation_bodymass_flipper
FROM penguins;

-- Bill Length vs Bill Depth
-- SELECT CORR(bill_length_mm, bill_depth_mm) AS correlation FROM penguins;

SELECT 
(
COUNT(*) * SUM(bill_length_mm * bill_depth_mm) -
SUM(bill_length_mm) * SUM(bill_depth_mm)
)
/
SQRT(
(COUNT(*) * SUM(POWER(bill_length_mm,2)) - POWER(SUM(bill_length_mm),2)) *
(COUNT(*) * SUM(POWER(bill_depth_mm,2)) - POWER(SUM(bill_depth_mm),2))
) AS correlation_bill
FROM penguins;


-- Species per Island
SELECT island, species, COUNT(*) AS species_count
FROM penguins
GROUP BY island, species
ORDER BY island;


-- Average Body Mass per Island
SELECT island, AVG(body_mass_g) AS avg_body_mass
FROM penguins
GROUP BY island;

-- Average Flipper Length per Island
SELECT island, AVG(flipper_length_mm) AS avg_flipper_length
FROM penguins
GROUP BY island;

-- Missing Value Percentage
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN bill_length_mm IS NULL THEN 1 ELSE 0 END) AS missing_values,
    ROUND((SUM(CASE WHEN bill_length_mm IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)),2) AS missing_percentage
FROM penguins;


-- Outlier Detection (Body Mass)
SELECT *
FROM penguins
WHERE body_mass_g > (
    SELECT AVG(body_mass_g) + 2 * STDDEV(body_mass_g) FROM penguins
)
OR body_mass_g < (
    SELECT AVG(body_mass_g) - 2 * STDDEV(body_mass_g) FROM penguins
);

-- Important kpis
SELECT 
    COUNT(*) AS total_penguins,
    
    ROUND(AVG(body_mass_g),2) AS avg_body_mass_g,
    
    ROUND(AVG(flipper_length_mm),2) AS avg_flipper_length_mm,
    
    ROUND(AVG(bill_length_mm),2) AS avg_bill_length_mm,

    ROUND(
        (SUM(CASE WHEN sex = 'male' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
        2
    ) AS male_percentage,

    ROUND(
        (SUM(CASE WHEN sex = 'female' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
        2
    ) AS female_percentage

FROM penguins;