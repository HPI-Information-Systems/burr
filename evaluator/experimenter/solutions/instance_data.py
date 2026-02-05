import psycopg2
import pandas as pd
import os

def get_connection(database_name):
    DB_CONFIG = {
        "dbname": database_name,
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT")
    }
    return psycopg2.connect(**DB_CONFIG)

def get_table_names(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        return [row[0] for row in cur.fetchall()]

def get_sample_rows(conn, table_name, limit=5):
    return pd.read_sql_query(f'SELECT * FROM "{table_name}" LIMIT {limit};', conn)

def collect_samples(database_name, limit=5):
    conn = get_connection(database_name)
    try:
        tables = get_table_names(conn)
        samples = {}
        for table in tables:
            print(f"Collecting from table: {table} (limit={limit})")
            df = get_sample_rows(conn, table, limit)
            samples[table] = df
        return samples
    finally:
        conn.close()