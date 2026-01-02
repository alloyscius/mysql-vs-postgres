import time
import mysql.connector
import psycopg2

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

# THE TEST CANDIDATES
tests = [
    {
        "name": "Test 1: Simple Integer Index (Booking Account)",
        "pg_query": "CREATE INDEX idx_bench_1 ON postgres_air.booking(account_id);",
        "mysql_query": "CREATE INDEX idx_bench_1 ON booking(account_id);",
        "cleanup_pg": "DROP INDEX IF EXISTS postgres_air.idx_bench_1;",
        "cleanup_mysql": "DROP INDEX idx_bench_1 ON booking;"
    },
    {
        "name": "Test 2: Text Column Index (Airport City)",
        "pg_query": "CREATE INDEX idx_bench_2 ON postgres_air.airport(city);",
        "mysql_query": "CREATE INDEX idx_bench_2 ON airport(city);",
        "cleanup_pg": "DROP INDEX IF EXISTS postgres_air.idx_bench_2;",
        "cleanup_mysql": "DROP INDEX idx_bench_2 ON airport;"
    },
    {
        "name": "Test 3: Composite Index (Flight Schedule)",
        "pg_query": "CREATE INDEX idx_bench_3 ON postgres_air.flight(departure_airport, arrival_airport, scheduled_departure);",
        "mysql_query": "CREATE INDEX idx_bench_3 ON flight(departure_airport, arrival_airport, scheduled_departure);",
        "cleanup_pg": "DROP INDEX IF EXISTS postgres_air.idx_bench_3;",
        "cleanup_mysql": "DROP INDEX idx_bench_3 ON flight;"
    }
]

def run_benchmark():
    print("="*60)
    print("Scenario 1: INDEX CREATION BENCHMARK (POSTGRESQL vs. MYSQL)")
    print("="*60 + "\n")

    pg_conn = None
    mysql_conn = None

    try:
        # 1. CONNECT TO POSTGRES
        pg_conn = psycopg2.connect(**PG_CONFIG)
        pg_conn.autocommit = True
        pg_cursor = pg_conn.cursor()

        # 2. CONNECT TO MYSQL & DISABLE CHECKS
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_conn.autocommit = True
        mysql_cursor = mysql_conn.cursor()
        
        # Disable Foreign Key Checks for safe index manipulation
        mysql_cursor.execute("SET SESSION FOREIGN_KEY_CHECKS=0") 

        # Run Tests
        for test in tests:
            print(f"--- {test['name']} ---")

            # MEASURE POSTGRESQL
            pg_duration = 0
            try:
                # Cleanup old index
                pg_cursor.execute(test['cleanup_pg']) 
                
                # Run Test
                start_time = time.time()
                pg_cursor.execute(test['pg_query'])
                end_time = time.time()
                
                pg_duration = round(end_time - start_time, 4)
                print(f"PostgreSQL Time: {pg_duration} seconds")
                
                # Cleanup result
                pg_cursor.execute(test['cleanup_pg'])

            except Exception as e:
                print(f"Postgres Error: {e}")
                pg_duration = 9999

            # MEASURE MYSQL
            mysql_duration = 0
            try:
                # Cleanup old index
                try:
                    mysql_cursor.execute(test['cleanup_mysql'])
                except:
                    pass # Ignore if it didn't exist

                # Run Test
                start_time = time.time()
                mysql_cursor.execute(test['mysql_query'])
                end_time = time.time()
                
                mysql_duration = round(end_time - start_time, 4)
                print(f"MySQL Time:      {mysql_duration} seconds")
                
                # Cleanup result
                mysql_cursor.execute(test['cleanup_mysql'])

            except Exception as e:
                print(f"MySQL Error: {e}")
                mysql_duration = 9999
            
            # Winner Logic
            if pg_duration != 9999 and mysql_duration != 9999:
                diff = abs(pg_duration - mysql_duration)
                winner = "Postgres" if pg_duration < mysql_duration else "MySQL"
                print(f">> WINNER: {winner} (by {round(diff, 4)}s)\n")
            else:
                print("\n")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        # Close connections cleanly
        if pg_conn: pg_conn.close()
        if mysql_conn: mysql_conn.close()
        print("Benchmark Complete.")

if __name__ == "__main__":
    run_benchmark()