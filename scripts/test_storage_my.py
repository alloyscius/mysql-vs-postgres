# Query to be used in MySQL to get storage size info

"""
USE mysql_air;

ANALYZE TABLE booking, flight, airport;

SELECT 
    table_name AS `Table`, 
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS `Total Size (MB)`, 
    ROUND((data_length / 1024 / 1024), 2) AS `Data Size (MB)`, 
    ROUND((index_length / 1024 / 1024), 2) AS `Index Size (MB)` 
FROM information_schema.TABLES 
WHERE table_schema = 'mysql_air' 
    AND table_name IN ('booking', 'flight', 'airport');


"""