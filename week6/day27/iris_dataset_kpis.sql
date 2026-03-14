-- Iris dataset KPIs

-- Total Records
SELECT COUNT(*) AS total_records
FROM iris;

-- Species Distribution

-- Count of each species
SELECT 
species,
COUNT(*) AS species_count
FROM iris
GROUP BY species;

-- Percentage of each species
SELECT 
species,
COUNT(*) AS species_count,
ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM iris),2) AS percentage
FROM iris
GROUP BY species;

-- Average Feature Values by Species
SELECT 
species,
ROUND(AVG('sepal_length(cm)'),2) AS avg_sepal_length,
ROUND(AVG('sepal_width(cm)'),2) AS avg_sepal_width,
ROUND(AVG('petal_length(cm)'),2) AS avg_petal_length,
ROUND(AVG('petal_width(cm)'),2) AS avg_petal_width
FROM iris
GROUP BY species;

-- Feature Correlation Matrix

SELECT 
(
COUNT(*) * SUM('petal_length(cm)' * 'petal_width(cm)') -
SUM('petal_length(cm)') * SUM('petal_width(cm)')
)
/
SQRT(
(COUNT(*) * SUM(POWER('petal_length(cm)',2)) - POWER(SUM('petal_length(cm)'),2)) *
(COUNT(*) * SUM(POWER('petal_width(cm)',2)) - POWER(SUM('petal_width(cm)'),2))
) AS correlation_petal
FROM iris;

-- Example: Sepal Length vs Sepal Width
SELECT 
(
COUNT(*) * SUM('sepal_length(cm)'*' sepal_width(cm)') -
SUM('sepal_length(cm)') * SUM('sepal_width(cm)')
)
/
SQRT(
(COUNT(*) * SUM(POWER('sepal_length(cm)',2)) - POWER(SUM('sepal_length(cm)'),2)) *
(COUNT(*) * SUM(POWER('sepal_width(cm)',2)) - POWER(SUM('sepal_width(cm)'),2))
) AS correlation_sepal
FROM iris;

-- Outlier Detection Summary

-- Using **Z-score method (2 standard deviations)**.

-- Sepal Length Outliers

SELECT COUNT(*) AS sepal_length_outliers
FROM iris
WHERE 
'sepal_length(cm)' > (SELECT AVG('sepal_length(cm)') + 2*STDDEV('sepal_length(cm)') FROM iris)
OR
'sepal_length(cm)' < (SELECT AVG('sepal_length(cm)') - 2*STDDEV('sepal_length(cm)') FROM iris);


-- Percentage of Outliers

SELECT 
COUNT(*) AS outlier_count,
ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM iris),2) AS outlier_percentage
FROM iris
WHERE 
'sepal_length(cm)' > (SELECT AVG('sepal_length(cm)') + 2*STDDEV('sepal_length(cm)') FROM iris)
OR
'sepal_length(cm)' < (SELECT AVG('sepal_length(cm)') - 2*STDDEV('sepal_length(cm)') FROM iris);




SELECT 
    (SELECT COUNT(*) FROM iris) AS total_records,
    species,
    COUNT(*) AS species_count,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM iris),2) AS species_percentage,
    
    ROUND(AVG('sepal_length(cm)'),2) AS avg_sepal_length,
    ROUND(AVG('sepal_width(cm)'),2) AS avg_sepal_width,
    ROUND(AVG('petal_length(cm)'),2) AS avg_petal_length,
    ROUND(AVG('petal_width(cm)'),2) AS avg_petal_width

FROM iris
GROUP BY species;