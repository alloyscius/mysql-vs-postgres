import time
import mysql.connector
import psycopg2
import statistics


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

# THE TEST QUERIES
queries = [
    {
        "name": "Query 1: Simple Lookup (Find Booking by Account ID)",
        "sql_pg": "SELECT * FROM postgres_air.booking WHERE account_id = 1500;",
        "sql_mysql": "SELECT * FROM booking WHERE account_id = 1500;"
    },
    {
        "name": "Query 2: Text Search (Find Airports in 'New York')",
        "sql_pg": "SELECT * FROM postgres_air.airport WHERE city = 'New York';",
        "sql_mysql": "SELECT * FROM airport WHERE city = 'New York';"
    },
    {
        "name": "Query 3: Complex Join (Flights departing from Chicago)",
        "sql_pg": """
            SELECT f.flight_id, f.scheduled_departure, a.city 
            FROM postgres_air.flight f 
            JOIN postgres_air.airport a ON f.departure_airport = a.airport_code 
            WHERE a.city = 'Chicago' 
            LIMIT 1000;
        """,
        "sql_mysql": """
            SELECT f.flight_id, f.scheduled_departure, a.city 
            FROM flight f 
            JOIN airport a ON f.departure_airport = a.airport_code 
            WHERE a.city = 'Chicago' 
            LIMIT 1000;
        """
    }
]

def run_benchmark():
    print("="*60)
    print("Scenario 2: QUERY EXECUTION BENCHMARK (Baseline / Unindexed)")
    print("="*60 + "\n")

    pg_conn = None
    mysql_conn = None

    try:
        # Connect
        pg_conn = psycopg2.connect(**PG_CONFIG)
        pg_cursor = pg_conn.cursor()

        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()

        for test in queries:
            print(f"--- {test['name']} ---")
            
            # Measure PostgreSQL (Run 5 times for Average)
            pg_times = []
            for _ in range(5):
                start = time.time()
                pg_cursor.execute(test['sql_pg'])
                pg_cursor.fetchall() # Fetch data to be fair
                end = time.time()
                pg_times.append(end - start)
            
            pg_avg = round(statistics.mean(pg_times), 4)
            print(f"PostgreSQL Avg Time: {pg_avg}s  (Runs: {[round(x,4) for x in pg_times]})")

            # Measure MySQL (Run 5 times for Average)
            mysql_times = []
            for _ in range(5):
                start = time.time()
                mysql_cursor.execute(test['sql_mysql'])
                mysql_cursor.fetchall()
                end = time.time()
                mysql_times.append(end - start)
            
            mysql_avg = round(statistics.mean(mysql_times), 4)
            print(f"MySQL Avg Time:      {mysql_avg}s  (Runs: {[round(x,4) for x in mysql_times]})")

            # Winner?
            diff = abs(pg_avg - mysql_avg)
            winner = "Postgres" if pg_avg < mysql_avg else "MySQL"
            print(f">> WINNER: {winner} (by {round(diff, 4)}s)\n")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        if pg_conn: pg_conn.close()
        if mysql_conn: mysql_conn.close()
        print("Benchmark Complete.")

if __name__ == "__main__":
    run_benchmark()