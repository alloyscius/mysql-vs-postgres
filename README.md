# PostgreSQL vs. MySQL Performance Benchmarking

A comprehensive benchmarking framework designed to compare **PostgreSQL** and **MySQL** performance characteristics using a large-scale relational airline dataset. This study evaluates index creation overhead, query execution speeds, storage efficiency, and memory consumption under controlled conditions.

--- 

## 📖 Overview
The primary objective of this project is to provide a side-by-side comparison of two of the most popular open-source relational database management systems. The framework automates the collection of performance metrics across four key areas:
1. **Index Overhead:** Time required to build B-Tree indexes on large tables.
2. **Query Performance:** Execution time differences between unindexed (baseline) and indexed queries.
3. **Storage Efficiency:** Disk usage analysis for raw data versus index structures.
4. **Resource Usage:** Client-side memory consumption during result fetching.

---

## 📂 Project Structure

```text
.
├── data/
│   └── postgres_air_2024.sql      # Dataset dump (PostgreSQL format)
├── tests/
│   ├── benchmark.py               # Index creation benchmark script
│   ├── benchmark_query.py         # Baseline query execution (Unindexed)
│   ├── benchmark_indexed.py       # Optimized query execution (Indexed)
│   ├── benchmark_memory.py        # Client-side memory usage profiling
│   ├── test_storage_post.py       # PostgreSQL storage analysis metrics
│   └── test_storage_my.py         # MySQL storage analysis metrics
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation

```
---

## 💽 Dataset
The project utilizes the **Postgres Air** database, a comprehensive airline dataset containing relational tables for bookings, flights, passengers, airports, and boarding passes.

* **Source:** Adapted from the [Postgres Air](https://github.com/hettie-d/postgres_air) repository.
* **Migration:** The data is initially imported into PostgreSQL and subsequently migrated to MySQL to ensure data consistency across both environments.
* **Schema Reference:** View the Entity Relationship Diagram (ERD) [here](https://github.com/hettie-d/postgres_air/blob/main/postgres_air_ERD.png).

---

## 📊 Benchmarks Implemented

### 1. Index Creation Time
Measures the wall-clock time required to create indexes on high-cardinality columns across various table sizes.

### 2. Query Execution Time
Compares read performance in two states:
* **Baseline:** Full table scans without indexes.
* **Indexed:** Execution using optimized B-Tree indexes.

### 3.  Storage Usage
Analyzes the disk footprint, distinguishing between:
* Table Data Size
* Index Size
  
### 4. Client-Side Memory Usage
Tracks peak RAM consumption on the client side (Python) while fetching and processing large result sets using `memory_profiler`.
