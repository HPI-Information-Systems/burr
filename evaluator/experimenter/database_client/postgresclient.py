import os
import subprocess
import pandas as pd
import wandb
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from psycopg2 import OperationalError, ProgrammingError, InterfaceError

class PostgresClient:
    def __init__(self, database):
        load_dotenv()
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = database
        #self.engine = self.get_database_engine()

    def get_database_engine(self):
        """Creates and returns a SQLAlchemy engine for connecting to the database."""
        try:
            engine_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            print("Connecting to database:", engine_url)
            engine = create_engine(engine_url)
            return engine
        except Exception as e:
            print(f"Error creating SQLAlchemy engine: {e}")
            return None

    def update_database(self, script_path, add_primary_keys=False):
        """Runs an SQL script file using psql command line."""
        wandb.save(script_path, base_path=os.path.dirname(script_path))
        command = ['psql', '-f', script_path, '-U', self.user, '-d', self.database, '-h', self.host]
        print(command)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("Database updated successfully.")
        else:
            print("Database update failed with return code:", result.returncode)
            print("Error output:", result.stderr)
            raise ValueError("Database update failed")
        if add_primary_keys:
            self.add_primary_keys()

    def add_primary_keys(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        AND NOT EXISTS (
            SELECT 1
            FROM information_schema.table_constraints
            WHERE table_schema = 'public'
            AND table_name = tables.table_name
            AND constraint_type = 'PRIMARY KEY'
        );
        """
        try:
            engine = self.get_database_engine()
            tables_df = pd.read_sql(query, engine)
            print(tables_df)
            tables = tables_df['table_name'].tolist()
            
            # If no tables without primary keys, exit the function
            if not tables:
                print("All tables already have primary keys.")
                return

            # Add an `id` column as a primary key for each table without one
            with engine.connect() as connection:
                for table in tables:
                    try:
                        #verify_query = text(f'ALTER SCHEMA public OWNER TO lukaslaskowski;')
                        #result = connection.execute(verify_query)
                        alter_query = f"ALTER TABLE {table} ADD COLUMN artificial_id SERIAL PRIMARY KEY;"
                        res = connection.execute(text(alter_query))
                        connection.commit()
                        print(res)
                        verify_query = text(f"""
                            SELECT column_name, data_type
                            FROM information_schema.columns
                            WHERE table_name = '{table}'
                            AND column_name = 'artificial_id';
                        """)
                        result = connection.execute(verify_query)
                        row = result.fetchone()
                        print(row)
                        if row:
                            print("Column added successfully:", row)
                        else:
                            print("The column was not added.")
                        print(text(alter_query))
                        print(f"Primary key added to {table} successfully.")
                    except SQLAlchemyError as e:
                        connection.rollback()
                        print(f"Failed to add primary key to {table}. Error:", str(e))
                        raise

            print("Primary keys added to all applicable tables.")

        except SQLAlchemyError as e:
            print("Failed to retrieve tables or add primary keys:", str(e))
            raise

    def get_constraints(self):
        """Fetches all primary key, unique, and foreign key constraints."""
        query = """
            SELECT 
                tc.table_schema, 
                tc.table_name, 
                tc.constraint_name, 
                tc.constraint_type, 
                kcu.column_name AS column_name
            FROM 
                information_schema.table_constraints AS tc
            JOIN 
                information_schema.key_column_usage AS kcu 
            ON 
                tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE 
                tc.constraint_type IN ('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')
            ORDER BY 
                tc.table_name, 
                tc.constraint_type;
        """
        try:
            engine = self.get_database_engine()
            df = pd.read_sql(query, engine)
            if df.empty:
                print("No constraints found in the database.")
            else:
                print("Constraints successfully retrieved.")
            return df
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            print(f"Error fetching constraints: {e}")
            return pd.DataFrame()

    def get_all_tables(self):
        """Retrieves all tables from the database and returns a dictionary with DataFrames for each table."""
        tables = {}
        try:
            engine = self.get_database_engine()
            # Get the list of tables
            table_names = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", engine)
            table_names = table_names['table_name'].tolist()

            # Load each table into a DataFrame
            for table_name in table_names:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, engine)
                tables[table_name] = df
                print(f"Table '{table_name}' loaded successfully.")

            return tables

        except Exception as e:
            print(f"Error fetching tables: {e}")
            return {}

    def generate_description(self, df):
        """Generates a summary description of the database constraints."""
        if df.empty:
            return "No constraints found in the database."

        description = "Database Constraint Summary:\n"
        constraint_counts = df['constraint_type'].value_counts()
        
        for constraint_type, count in constraint_counts.items():
            description += f"- {count} {constraint_type.lower()} constraint(s) found.\n"
        
        description += "\nTables and Constraints Overview:\n"
        
        grouped = df.groupby(['table_schema', 'table_name', 'constraint_type'])
        for (schema, table, constraint_type), group in grouped:
            columns = ', '.join(group['column_name'])
            description += f"Table '{schema}.{table}' has a {constraint_type.lower()} constraint on columns: {columns}.\n"
        return description
