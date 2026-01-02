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

# 1. THE INDEXES TO CREATE
# Add them to both to ensure a fair "Indexed" comparison
indexes = [
    # Query 1 Helper
    ("CREATE INDEX idx_booking_acct ON postgres_air.booking(account_id);", 
     "CREATE INDEX idx_booking_acct ON booking(account_id);"),
    
    # Query 2 Helper
    ("CREATE INDEX idx_airport_city ON postgres_air.airport(city);", 
     "CREATE INDEX idx_airport_city ON airport(city);"),
    
    # Query 3 Helper (Composite)
    ("CREATE INDEX idx_flight_sched ON postgres_air.flight(departure_airport, scheduled_departure);", 
     "CREATE INDEX idx_flight_sched ON flight(departure_airport, scheduled_departure);")
]

# 2. THE TEST QUERIES
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
    print("Scenario 3: QUERY EXECUTION BENCHMARK (INDEXED MODE)")
    print("="*60 + "\n")

    pg_conn = None
    mysql_conn = None

    try:
        # Connect
        pg_conn = psycopg2.connect(**PG_CONFIG)
        pg_conn.autocommit = True
        pg_cursor = pg_conn.cursor()

        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_conn.autocommit = True
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SET SESSION FOREIGN_KEY_CHECKS=0")

        # PART A: BUILD INDEXES
        print(">>> Building Indexes for Speed Test...")
        for pg_idx, mysql_idx in indexes:
            try:
                pg_cursor.execute(pg_idx)
            except: pass # Ignore if exists
            
            try:
                mysql_cursor.execute(mysql_idx)
            except: pass # Ignore if exists
        print(">>> Indexes Built!\n")

        # PART B: RUN BENCHMARK
        for test in queries:
            print(f"--- {test['name']} ---")
            
            # Measure PostgreSQL
            pg_times = []
            for _ in range(5):
                start = time.time()
                pg_cursor.execute(test['sql_pg'])
                pg_cursor.fetchall()
                end = time.time()
                pg_times.append(end - start)
            
            pg_avg = round(statistics.mean(pg_times), 5) # Increased precision
            print(f"PostgreSQL Avg Time: {pg_avg}s")

            # Measure MySQL
            mysql_times = []
            for _ in range(5):
                start = time.time()
                mysql_cursor.execute(test['sql_mysql'])
                mysql_cursor.fetchall()
                end = time.time()
                mysql_times.append(end - start)
            
            mysql_avg = round(statistics.mean(mysql_times), 5) # Increased precision
            print(f"MySQL Avg Time:      {mysql_avg}s")

            # Winner?
            diff = abs(pg_avg - mysql_avg)
            winner = "Postgres" if pg_avg < mysql_avg else "MySQL"
            print(f">> WINNER: {winner} (by {round(diff, 5)}s)\n")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        if pg_conn: pg_conn.close()
        if mysql_conn: mysql_conn.close()
        print("Benchmark Complete.")

if __name__ == "__main__":
    run_benchmark()