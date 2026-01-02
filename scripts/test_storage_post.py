# Query to be used in PostgreSQL to get storage size info

"""
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_schema) || '.' || quote_ident(table_name))) AS total_size,
    pg_size_pretty(pg_relation_size(quote_ident(table_schema) || '.' || quote_ident(table_name))) AS data_only_size,
    pg_size_pretty(pg_indexes_size(quote_ident(table_schema) || '.' || quote_ident(table_name))) AS index_only_size
FROM information_schema.tables
WHERE table_schema = 'postgres_air'
  AND table_name IN ('booking', 'flight', 'airport')
ORDER BY pg_total_relation_size(quote_ident(table_schema) || '.' || quote_ident(table_name)) DESC;

"""