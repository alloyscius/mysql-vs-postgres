import time
import mysql.connector
import psycopg2
from memory_profiler import memory_usage

# CONFIGURATION
PG_CONFIG = {
    "dbname": "postgres_air", 
    "user": "postgres",
    "password": "@XuanYL0119",
    "host": "localhost",
    "port": "5432"
}

MYSQL_CONFIG = {
    "database": "mysql_air",  
    "user": "root",           
    "password": "@XuanYL0119", 
    "host": "localhost"
}

# Test Complext Join Query fetching 50k rows
query_pg = """
    SELECT f.flight_id, f.scheduled_departure, a.city 
    FROM postgres_air.flight f 
    JOIN postgres_air.airport a ON f.departure_airport = a.airport_code 
    WHERE a.city = 'Chicago' 
    LIMIT 50000;
"""

query_mysql = """
    SELECT f.flight_id, f.scheduled_departure, a.city 
    FROM flight f 
    JOIN airport a ON f.departure_airport = a.airport_code 
    WHERE a.city = 'Chicago' 
    LIMIT 50000;
"""

def test_postgres():
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query_pg)
    rows = cursor.fetchall()
    conn.close()
    return len(rows)

def test_mysql():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query_mysql)
    rows = cursor.fetchall()
    conn.close()
    return len(rows)

def run_memory_test():
    print("="*60)
    print("MEMORY USAGE BENCHMARK (Peak RAM)")
    print("="*60 + "\n")

    # 1. Measure PostgreSQL
    print("Testing PostgreSQL Memory...")
    pg_mem_start = memory_usage()[0]
    pg_mem_peak = memory_usage((test_postgres,), max_usage=True)
    pg_usage = round(pg_mem_peak - pg_mem_start, 2)
    print(f"PostgreSQL Memory Usage: {pg_usage} MiB")

    # 2. Measure MySQL
    print("Testing MySQL Memory...")
    mysql_mem_start = memory_usage()[0]
    mysql_mem_peak = memory_usage((test_mysql,), max_usage=True)
    mysql_usage = round(mysql_mem_peak - mysql_mem_start, 2)
    print(f"MySQL Memory Usage:      {mysql_usage} MiB")

    # Winner?
    diff = abs(pg_usage - mysql_usage)
    winner = "Postgres" if pg_usage < mysql_usage else "MySQL"
    print(f"\n>> WINNER: {winner} (used {diff} MiB less RAM)")

if __name__ == "__main__":
    run_memory_test()